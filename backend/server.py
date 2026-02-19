from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import pandas as pd
import io
from emergentintegrations.llm.chat import LlmChat, UserMessage
from jira_client import JiraAPIClient
from jira_service import JiraService
from delay_predictor import DelayPredictor

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class SprintData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    sprint_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_issues: int = 0
    total_story_points: float = 0
    completed_story_points: float = 0
    in_progress_story_points: float = 0
    todo_story_points: float = 0
    blocked_story_points: float = 0
    completion_percentage: float = 0
    days_remaining: Optional[int] = None
    days_elapsed: Optional[int] = None
    risk_level: str = "low"  # low, medium, high, critical
    velocity: float = 0
    status_distribution: Dict[str, int] = {}

class JiraPrompt(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sprint_name: str
    prompt_type: str  # warning, critical, success, info
    title: str
    message: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class DashboardStats(BaseModel):
    total_sprints: int
    total_issues: int
    average_velocity: float
    at_risk_sprints: int
    completion_rate: float

class TeamMember(BaseModel):
    name: str
    assigned_points: float
    completed_points: float
    completion_rate: float

class JiraConnection(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    jira_url: str
    email: str
    api_token: str
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class JiraConnectionRequest(BaseModel):
    jira_url: str
    email: str
    api_token: str

class JiraConnectionTest(BaseModel):
    success: bool
    message: str

# Global storage for current dataset
current_dataset = None
current_jira_connection = None

@api_router.get("/")
async def root():
    return {"message": "Jira Analytics API"}

@api_router.post("/jira/test-connection", response_model=JiraConnectionTest)
async def test_jira_connection(connection: JiraConnectionRequest):
    """Test Jira connection credentials."""
    try:
        async with JiraAPIClient(
            instance_url=connection.jira_url,
            email=connection.email,
            api_token=connection.api_token
        ) as client:
            is_valid = await client.test_connection()
            
            if is_valid:
                return JiraConnectionTest(
                    success=True,
                    message="Connection successful! Credentials are valid."
                )
            else:
                return JiraConnectionTest(
                    success=False,
                    message="Connection failed. Please check your credentials."
                )
    except Exception as e:
        logging.error(f"Connection test error: {str(e)}")
        return JiraConnectionTest(
            success=False,
            message=f"Connection error: {str(e)}"
        )

@api_router.post("/jira/connect")
async def connect_jira(connection: JiraConnectionRequest):
    """Save Jira connection and fetch data."""
    global current_dataset, current_jira_connection
    
    try:
        # Test connection first
        async with JiraAPIClient(
            instance_url=connection.jira_url,
            email=connection.email,
            api_token=connection.api_token
        ) as client:
            is_valid = await client.test_connection()
            
            if not is_valid:
                raise HTTPException(status_code=401, detail="Invalid Jira credentials")
            
            # Save connection
            current_jira_connection = {
                "jira_url": connection.jira_url,
                "email": connection.email,
                "api_token": connection.api_token
            }
            
            # Store in database
            conn_doc = JiraConnection(**current_jira_connection).model_dump()
            await db.jira_connections.insert_one(conn_doc)
            
            # Fetch data from Jira
            jira_service = JiraService(client)
            df = await jira_service.fetch_all_data()
            
            if df.empty:
                raise HTTPException(status_code=404, detail="No data found in Jira instance")
            
            current_dataset = df
            
            return {
                "success": True,
                "message": "Connected to Jira successfully",
                "total_issues": len(df),
                "total_sprints": df['Assigned Sprint'].nunique() if 'Assigned Sprint' in df.columns else 0
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error connecting to Jira: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error connecting to Jira: {str(e)}")

@api_router.post("/jira/refresh")
async def refresh_jira_data():
    """Refresh data from connected Jira instance."""
    global current_dataset, current_jira_connection
    
    if not current_jira_connection:
        raise HTTPException(status_code=404, detail="No Jira connection found. Please connect first.")
    
    try:
        async with JiraAPIClient(
            instance_url=current_jira_connection["jira_url"],
            email=current_jira_connection["email"],
            api_token=current_jira_connection["api_token"]
        ) as client:
            jira_service = JiraService(client)
            df = await jira_service.fetch_all_data()
            
            if df.empty:
                raise HTTPException(status_code=404, detail="No data found in Jira")
            
            current_dataset = df
            
            return {
                "success": True,
                "message": "Data refreshed successfully",
                "total_issues": len(df),
                "total_sprints": df['Assigned Sprint'].nunique()
            }
    
    except Exception as e:
        logging.error(f"Error refreshing Jira data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error refreshing data: {str(e)}")

@api_router.get("/jira/status")
async def get_jira_connection_status():
    """Get current Jira connection status."""
    global current_jira_connection
    
    if current_jira_connection:
        return {
            "connected": True,
            "jira_url": current_jira_connection["jira_url"],
            "email": current_jira_connection["email"]
        }
    else:
        return {"connected": False}

@api_router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    global current_dataset
    
    try:
        contents = await file.read()
        
        # Read Excel file
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(contents))
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel file.")
        
        current_dataset = df
        
        # Store upload info in database
        upload_doc = {
            "filename": file.filename,
            "upload_time": datetime.now(timezone.utc).isoformat(),
            "total_rows": len(df),
            "columns": list(df.columns)
        }
        await db.uploads.insert_one(upload_doc)
        
        return {
            "success": True,
            "filename": file.filename,
            "total_issues": len(df),
            "total_sprints": df['Assigned Sprint'].nunique() if 'Assigned Sprint' in df.columns else 0
        }
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@api_router.get("/sprints", response_model=List[SprintData])
async def get_sprints():
    global current_dataset
    
    if current_dataset is None:
        raise HTTPException(status_code=404, detail="No data uploaded. Please upload a Jira CSV file first.")
    
    df = current_dataset
    sprints_data = []
    
    # Get unique sprints
    sprints = df['Assigned Sprint'].dropna().unique()
    
    for sprint in sprints:
        if sprint == 'None( Backlog)':
            continue
            
        sprint_df = df[df['Assigned Sprint'] == sprint]
        
        # Calculate metrics
        total_issues = len(sprint_df)
        total_story_points = sprint_df['Story Points'].sum()
        
        # Status-based calculations
        done_df = sprint_df[sprint_df['Status'] == 'Done']
        in_progress_df = sprint_df[sprint_df['Status'] == 'In Progress']
        todo_df = sprint_df[sprint_df['Status'] == 'To Do']
        blocked_df = sprint_df[sprint_df['Status'] == 'Blocked']
        
        completed_points = done_df['Story Points'].sum()
        in_progress_points = in_progress_df['Story Points'].sum()
        todo_points = todo_df['Story Points'].sum()
        blocked_points = blocked_df['Story Points'].sum()
        
        completion_pct = (completed_points / total_story_points * 100) if total_story_points > 0 else 0
        
        # Get sprint dates
        start_date = sprint_df['Assigned Sprint\nStart date'].iloc[0] if len(sprint_df) > 0 else None
        end_date = sprint_df['Assigned Sprint\nEnd date'].iloc[0] if len(sprint_df) > 0 else None
        
        # Calculate days remaining
        days_remaining = None
        days_elapsed = None
        if pd.notna(end_date) and pd.notna(start_date):
            try:
                end_dt = pd.to_datetime(end_date)
                start_dt = pd.to_datetime(start_date)
                now = pd.Timestamp.now()
                days_remaining = (end_dt - now).days
                days_elapsed = (now - start_dt).days
            except:
                pass
        
        # Risk assessment
        risk_level = "low"
        if completion_pct < 30:
            risk_level = "critical"
        elif completion_pct < 50:
            risk_level = "high"
        elif completion_pct < 70:
            risk_level = "medium"
        
        # If sprint is near end and not complete
        if days_remaining is not None and days_remaining < 3 and completion_pct < 80:
            risk_level = "critical"
        
        # Status distribution
        status_dist = sprint_df['Status'].value_counts().to_dict()
        
        sprints_data.append(SprintData(
            sprint_name=sprint,
            start_date=str(start_date) if pd.notna(start_date) else None,
            end_date=str(end_date) if pd.notna(end_date) else None,
            total_issues=int(total_issues),
            total_story_points=float(total_story_points),
            completed_story_points=float(completed_points),
            in_progress_story_points=float(in_progress_points),
            todo_story_points=float(todo_points),
            blocked_story_points=float(blocked_points),
            completion_percentage=float(completion_pct),
            days_remaining=days_remaining,
            days_elapsed=days_elapsed,
            risk_level=risk_level,
            velocity=float(completed_points),
            status_distribution=status_dist
        ))
    
    return sprints_data

@api_router.get("/dashboard")
async def get_dashboard():
    global current_dataset
    
    if current_dataset is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    df = current_dataset
    
    # Overall stats
    total_sprints = df['Assigned Sprint'].nunique()
    total_issues = len(df)
    
    # Calculate average velocity
    sprints = df['Assigned Sprint'].dropna().unique()
    velocities = []
    at_risk_count = 0
    
    for sprint in sprints:
        if sprint == 'None( Backlog)':
            continue
        sprint_df = df[df['Assigned Sprint'] == sprint]
        done_df = sprint_df[sprint_df['Status'] == 'Done']
        velocity = done_df['Story Points'].sum()
        velocities.append(velocity)
        
        # Check risk
        total_points = sprint_df['Story Points'].sum()
        completion_pct = (velocity / total_points * 100) if total_points > 0 else 0
        if completion_pct < 50:
            at_risk_count += 1
    
    avg_velocity = sum(velocities) / len(velocities) if velocities else 0
    
    # Overall completion rate
    total_points = df['Story Points'].sum()
    completed_points = df[df['Status'] == 'Done']['Story Points'].sum()
    completion_rate = (completed_points / total_points * 100) if total_points > 0 else 0
    
    return DashboardStats(
        total_sprints=int(total_sprints),
        total_issues=int(total_issues),
        average_velocity=float(avg_velocity),
        at_risk_sprints=int(at_risk_count),
        completion_rate=float(completion_rate)
    )

@api_router.get("/recommendations", response_model=List[JiraPrompt])
async def get_recommendations():
    global current_dataset
    
    if current_dataset is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    df = current_dataset
    prompts = []
    
    # Analyze sprints and generate prompts
    sprints = df['Assigned Sprint'].dropna().unique()
    
    for sprint in sprints:
        if sprint == 'None( Backlog)':
            continue
            
        sprint_df = df[df['Assigned Sprint'] == sprint]
        total_points = sprint_df['Story Points'].sum()
        completed_points = sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()
        blocked_points = sprint_df[sprint_df['Status'] == 'Blocked']['Story Points'].sum()
        completion_pct = (completed_points / total_points * 100) if total_points > 0 else 0
        
        # Get sprint dates
        end_date = sprint_df['Assigned Sprint\nEnd date'].iloc[0] if len(sprint_df) > 0 else None
        days_remaining = None
        
        if pd.notna(end_date):
            try:
                end_dt = pd.to_datetime(end_date)
                now = pd.Timestamp.now()
                days_remaining = (end_dt - now).days
            except:
                pass
        
        # Critical: Sprint at risk
        if completion_pct < 50 and days_remaining is not None and days_remaining < 5:
            prompts.append(JiraPrompt(
                sprint_name=sprint,
                prompt_type="critical",
                title=f"⚠️ {sprint} - Critical Risk",
                message=f"Sprint is {completion_pct:.0f}% complete with only {days_remaining} days remaining. {total_points - completed_points:.0f} story points at risk. Immediate action required."
            ))
        
        # Warning: Low completion
        elif completion_pct < 60:
            prompts.append(JiraPrompt(
                sprint_name=sprint,
                prompt_type="warning",
                title=f"⚡ {sprint} - Attention Needed",
                message=f"Sprint completion is at {completion_pct:.0f}%. Consider reprioritizing or descoping to meet sprint goals."
            ))
        
        # Blocked issues
        if blocked_points > 0:
            blocked_count = len(sprint_df[sprint_df['Status'] == 'Blocked'])
            prompts.append(JiraPrompt(
                sprint_name=sprint,
                prompt_type="warning",
                title=f"🚧 {sprint} - Blocked Issues",
                message=f"{blocked_count} issues ({blocked_points:.0f} story points) are blocked. Review and unblock to maintain velocity."
            ))
        
        # Success: Good progress
        if completion_pct >= 80:
            prompts.append(JiraPrompt(
                sprint_name=sprint,
                prompt_type="success",
                title=f"✅ {sprint} - On Track",
                message=f"Great progress! Sprint is {completion_pct:.0f}% complete. Keep up the momentum."
            ))
    
    # Use AI to generate additional insights
    try:
        if prompts and os.environ.get('EMERGENT_LLM_KEY'):
            # Prepare data for AI analysis
            sprint_summary = []
            for sprint in sprints[:3]:  # Analyze top 3 sprints
                if sprint == 'None( Backlog)':
                    continue
                sprint_df = df[df['Assigned Sprint'] == sprint]
                total_points = sprint_df['Story Points'].sum()
                completed_points = sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()
                completion_pct = (completed_points / total_points * 100) if total_points > 0 else 0
                sprint_summary.append(f"{sprint}: {completion_pct:.0f}% complete, {total_points:.0f} total points, {completed_points:.0f} completed")
            
            chat = LlmChat(
                api_key=os.environ.get('EMERGENT_LLM_KEY'),
                session_id=str(uuid.uuid4()),
                system_message="You are a Jira sprint analytics expert. Provide brief, actionable recommendations in 1-2 sentences."
            ).with_model("gemini", "gemini-3-flash-preview")
            
            user_message = UserMessage(
                text=f"Analyze these sprint metrics and provide ONE concise recommendation for the team:\n\n{chr(10).join(sprint_summary)}\n\nProvide a single actionable insight in 1 sentence."
            )
            
            response = await chat.send_message(user_message)
            
            if response:
                prompts.append(JiraPrompt(
                    sprint_name="Overall",
                    prompt_type="info",
                    title="💡 AI Insight",
                    message=response
                ))
    except Exception as e:
        logging.error(f"Error generating AI recommendations: {str(e)}")
    
    return prompts

@api_router.get("/team-performance", response_model=List[TeamMember])
async def get_team_performance():
    global current_dataset
    
    if current_dataset is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    df = current_dataset
    team_members = []
    
    # Get unique assignees
    assignees = df['Assignee'].dropna().unique()
    
    for assignee in assignees:
        assignee_df = df[df['Assignee'] == assignee]
        assigned_points = assignee_df['Story Points'].sum()
        completed_points = assignee_df[assignee_df['Status'] == 'Done']['Story Points'].sum()
        completion_rate = (completed_points / assigned_points * 100) if assigned_points > 0 else 0
        
        team_members.append(TeamMember(
            name=assignee,
            assigned_points=float(assigned_points),
            completed_points=float(completed_points),
            completion_rate=float(completion_rate)
        ))
    
    # Sort by assigned points
    team_members.sort(key=lambda x: x.assigned_points, reverse=True)
    
    return team_members[:10]  # Top 10

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()