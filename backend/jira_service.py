import logging
from typing import List, Optional, Dict, Any
import pandas as pd
from jira_client import JiraAPIClient

logger = logging.getLogger(__name__)

class JiraService:
    """Service layer for Jira data fetching and transformation."""
    
    def __init__(self, client: JiraAPIClient):
        self.client = client
    
    def _extract_story_points(self, fields: dict) -> Optional[float]:
        """Extract story points from issue fields (handles different custom field IDs)."""
        for field_id in ["customfield_10016", "customfield_10106", "customfield_10002", "customfield_10004"]:
            if field_id in fields and fields[field_id] is not None:
                try:
                    return float(fields[field_id])
                except (ValueError, TypeError):
                    continue
        return None
    
    async def fetch_all_data(self) -> pd.DataFrame:
        """Fetch all sprint data and convert to DataFrame matching CSV format."""
        all_data = []
        
        # Get all boards
        boards_response = await self.client.get_boards()
        boards = boards_response.get("values", [])
        
        logger.info(f"Found {len(boards)} boards")
        
        for board in boards:
            board_id = board["id"]
            board_name = board["name"]
            
            try:
                # Get sprints for this board
                sprints_response = await self.client.get_sprints(board_id)
                sprints = sprints_response.get("values", [])
                
                for sprint in sprints:
                    sprint_id = sprint["id"]
                    sprint_name = sprint["name"]
                    sprint_state = sprint.get("state", "unknown")
                    sprint_start = sprint.get("startDate")
                    sprint_end = sprint.get("endDate")
                    
                    # Get issues for this sprint
                    start_at = 0
                    while True:
                        issues_response = await self.client.get_sprint_issues(sprint_id, start_at)
                        issues = issues_response.get("issues", [])
                        
                        if not issues:
                            break
                        
                        for issue in issues:
                            fields = issue.get("fields", {})
                            status_obj = fields.get("status", {})
                            assignee_obj = fields.get("assignee", {})
                            issuetype_obj = fields.get("issuetype", {})
                            
                            story_points = self._extract_story_points(fields)
                            
                            # Build row matching CSV format
                            row = {
                                "Jira ID": issue["key"],
                                "Summary": fields.get("summary", ""),
                                "Status": status_obj.get("name", "Unknown"),
                                "Story Points": story_points if story_points else 0,
                                "Assigned Sprint": sprint_name,
                                "Assigned Sprint\nStart date": sprint_start,
                                "Assigned Sprint\nEnd date": sprint_end,
                                "Assignee": assignee_obj.get("displayName") if assignee_obj else None,
                                "Priority": fields.get("priority", {}).get("name", "Medium"),
                                "Issue Type": issuetype_obj.get("name", "Task"),
                                "Created": fields.get("created"),
                                "Resolved": fields.get("resolutiondate")
                            }
                            all_data.append(row)
                        
                        # Check pagination
                        if issues_response.get("isLast", True):
                            break
                        start_at += len(issues)
            
            except Exception as e:
                logger.error(f"Error fetching data for board {board_name}: {str(e)}")
                continue
        
        if not all_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        logger.info(f"Fetched {len(df)} issues from Jira")
        return df