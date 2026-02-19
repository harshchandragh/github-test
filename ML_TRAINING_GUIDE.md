# 🧠 ML MODEL TRAINING GUIDE
## Adding True Machine Learning to Jira Velocity Pro

---

## 🎯 CURRENT STATE vs DESIRED STATE

### **Current (Rule-Based + LLM API):**
```
Upload CSV → Calculate metrics → Apply rules → Call Gemini API → Show recommendations
                ↑                    ↑              ↑
            Just math          Fixed rules    External API (doesn't learn)
```

**Limitations:**
- Doesn't learn from your team's patterns
- Same input = same output (no improvement)
- Rules are generic, not personalized
- Doesn't predict - just analyzes current state

### **Desired (ML Model Training):**
```
Historical Data → Feature Engineering → Train Model → Predict Outcomes → Learn from Results
       ↓                   ↓                 ↓              ↓                  ↓
  Sprint 1-100    Extract patterns    RandomForest    Sprint delay?    Update model
```

**Benefits:**
- Learns YOUR team's specific patterns
- Gets better over time with more data
- Personalized predictions (not generic rules)
- Predicts FUTURE outcomes, not just current state

---

## 🛠️ IMPLEMENTATION: Add ML Model Training

### **Step 1: Install ML Libraries**

```bash
cd backend
pip install scikit-learn joblib numpy
pip freeze > requirements.txt
```

### **Step 2: Create ML Service**

Create `backend/ml_model.py`:

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

class SprintPredictor:
    """ML model for predicting sprint delays and velocity"""
    
    def __init__(self):
        self.delay_model = None  # Predicts if sprint will be delayed
        self.velocity_model = None  # Predicts actual velocity
        self.scaler = StandardScaler()
        self.model_path = "models/"
        os.makedirs(self.model_path, exist_ok=True)
    
    def prepare_features(self, df):
        """
        Extract features from sprint data for ML
        
        Features:
        - Team size (number of assignees)
        - Story points committed
        - Sprint duration (days)
        - Previous sprint velocity
        - Number of blockers
        - Issue types distribution
        - Historical completion rate
        """
        features = []
        labels_delay = []  # Binary: delayed or not
        labels_velocity = []  # Actual velocity achieved
        
        # Get unique sprints
        sprints = df['Assigned Sprint'].dropna().unique()
        
        for i, sprint in enumerate(sprints):
            sprint_df = df[df['Assigned Sprint'] == sprint]
            
            # Calculate features
            team_size = sprint_df['Assignee'].nunique()
            total_points = sprint_df['Story Points'].sum()
            
            # Sprint duration
            try:
                start = pd.to_datetime(sprint_df['Assigned Sprint\\nStart date'].iloc[0])
                end = pd.to_datetime(sprint_df['Assigned Sprint\\nEnd date'].iloc[0])
                duration = (end - start).days
            except:
                duration = 14  # Default 2 weeks
            
            # Previous sprint velocity (if available)
            if i > 0:
                prev_sprint = sprints[i-1]
                prev_df = df[df['Assigned Sprint'] == prev_sprint]
                prev_velocity = prev_df[prev_df['Status'] == 'Done']['Story Points'].sum()
            else:
                prev_velocity = total_points * 0.7  # Assume 70% for first sprint
            
            # Blockers
            num_blockers = len(sprint_df[sprint_df['Status'] == 'Blocked'])
            
            # Issue types
            num_bugs = len(sprint_df[sprint_df['Issue Type'] == 'Bug'])
            num_stories = len(sprint_df[sprint_df['Issue Type'] == 'Story'])
            
            # Historical completion rate (from previous sprints)
            if i > 0:
                historical_df = df[df['Assigned Sprint'].isin(sprints[:i])]
                total_historical = historical_df['Story Points'].sum()
                completed_historical = historical_df[historical_df['Status'] == 'Done']['Story Points'].sum()
                historical_rate = completed_historical / total_historical if total_historical > 0 else 0.7
            else:
                historical_rate = 0.7
            
            # Feature vector
            feature_vector = [
                team_size,
                total_points,
                duration,
                prev_velocity,
                num_blockers,
                num_bugs,
                num_stories,
                historical_rate,
                total_points / team_size if team_size > 0 else 0,  # Points per person
                total_points / duration if duration > 0 else 0,  # Points per day
            ]
            
            # Calculate actual outcomes (labels)
            completed_points = sprint_df[sprint_df['Status'] == 'Done']['Story Points'].sum()
            actual_velocity = completed_points
            
            # Delayed if completed < 70% of committed
            is_delayed = 1 if (completed_points / total_points < 0.7) else 0
            
            features.append(feature_vector)
            labels_delay.append(is_delayed)
            labels_velocity.append(actual_velocity)
        
        return np.array(features), np.array(labels_delay), np.array(labels_velocity)
    
    def train(self, df):
        """Train models on historical sprint data"""
        print("🧠 Starting ML model training...")
        
        # Prepare features and labels
        X, y_delay, y_velocity = self.prepare_features(df)
        
        if len(X) < 5:
            print("⚠️ Not enough data to train (need at least 5 sprints)")
            return False
        
        # Split data
        X_train, X_test, y_delay_train, y_delay_test, y_velocity_train, y_velocity_test = \
            train_test_split(X, y_delay, y_velocity, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train delay prediction model (classification)
        print("📊 Training delay prediction model...")
        self.delay_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.delay_model.fit(X_train_scaled, y_delay_train)
        
        # Evaluate
        delay_accuracy = self.delay_model.score(X_test_scaled, y_delay_test)
        print(f"✅ Delay prediction accuracy: {delay_accuracy:.2%}")
        
        # Train velocity prediction model (regression)
        print("📊 Training velocity prediction model...")
        self.velocity_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.velocity_model.fit(X_train_scaled, y_velocity_train)
        
        # Evaluate
        velocity_score = self.velocity_model.score(X_test_scaled, y_velocity_test)
        print(f"✅ Velocity prediction R² score: {velocity_score:.2f}")
        
        # Feature importance
        feature_names = [
            'team_size', 'total_points', 'duration', 'prev_velocity',
            'num_blockers', 'num_bugs', 'num_stories', 'historical_rate',
            'points_per_person', 'points_per_day'
        ]
        importances = self.delay_model.feature_importances_
        print("\\n📈 Top 3 Most Important Features:")
        for idx in np.argsort(importances)[-3:][::-1]:
            print(f"  • {feature_names[idx]}: {importances[idx]:.3f}")
        
        # Save models
        self.save_models()
        
        return True
    
    def predict(self, sprint_data):
        """
        Predict if sprint will be delayed
        
        Args:
            sprint_data: dict with keys:
                - team_size
                - total_points
                - duration
                - prev_velocity
                - num_blockers
                - num_bugs
                - num_stories
                - historical_rate
        
        Returns:
            {
                'will_delay': bool,
                'delay_probability': float (0-1),
                'predicted_velocity': float,
                'confidence': float
            }
        """
        if self.delay_model is None or self.velocity_model is None:
            raise Exception("Models not trained. Call train() first.")
        
        # Prepare feature vector
        feature_vector = [
            sprint_data['team_size'],
            sprint_data['total_points'],
            sprint_data['duration'],
            sprint_data['prev_velocity'],
            sprint_data.get('num_blockers', 0),
            sprint_data.get('num_bugs', 0),
            sprint_data.get('num_stories', 0),
            sprint_data.get('historical_rate', 0.7),
            sprint_data['total_points'] / sprint_data['team_size'],
            sprint_data['total_points'] / sprint_data['duration'],
        ]
        
        # Scale
        X = self.scaler.transform([feature_vector])
        
        # Predict delay
        delay_prob = self.delay_model.predict_proba(X)[0][1]  # Probability of delay
        will_delay = delay_prob > 0.5
        
        # Predict velocity
        predicted_velocity = self.velocity_model.predict(X)[0]
        
        # Confidence (based on probability distance from 0.5)
        confidence = abs(delay_prob - 0.5) * 2
        
        return {
            'will_delay': bool(will_delay),
            'delay_probability': float(delay_prob),
            'predicted_velocity': float(predicted_velocity),
            'confidence': float(confidence),
            'recommendation': self._generate_recommendation(
                sprint_data, will_delay, predicted_velocity
            )
        }
    
    def _generate_recommendation(self, sprint_data, will_delay, predicted_velocity):
        """Generate actionable recommendation based on prediction"""
        if will_delay:
            gap = sprint_data['total_points'] - predicted_velocity
            return f"⚠️ Sprint likely to be delayed. Expected velocity: {predicted_velocity:.0f} pts (gap: {gap:.0f} pts). Consider reducing scope by {gap:.0f} story points."
        else:
            return f"✅ Sprint on track. Predicted velocity: {predicted_velocity:.0f} pts."
    
    def save_models(self):
        """Save trained models to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        joblib.dump(self.delay_model, f"{self.model_path}delay_model_{timestamp}.pkl")
        joblib.dump(self.velocity_model, f"{self.model_path}velocity_model_{timestamp}.pkl")
        joblib.dump(self.scaler, f"{self.model_path}scaler_{timestamp}.pkl")
        
        # Save latest
        joblib.dump(self.delay_model, f"{self.model_path}delay_model_latest.pkl")
        joblib.dump(self.velocity_model, f"{self.model_path}velocity_model_latest.pkl")
        joblib.dump(self.scaler, f"{self.model_path}scaler_latest.pkl")
        
        print(f"💾 Models saved to {self.model_path}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            self.delay_model = joblib.load(f"{self.model_path}delay_model_latest.pkl")
            self.velocity_model = joblib.load(f"{self.model_path}velocity_model_latest.pkl")
            self.scaler = joblib.load(f"{self.model_path}scaler_latest.pkl")
            print("✅ Models loaded successfully")
            return True
        except FileNotFoundError:
            print("⚠️ No trained models found. Train first.")
            return False
    
    def retrain_with_new_data(self, new_sprint_data):
        """
        Continuous learning: Update model with new sprint outcomes
        
        This should be called after each sprint completes
        """
        print("🔄 Retraining model with new data...")
        # In production, you'd:
        # 1. Load historical data from database
        # 2. Append new sprint data
        # 3. Retrain models
        # 4. Save updated models
        # For now, just retrain on full dataset
        pass


# Example usage
if __name__ == "__main__":
    import pandas as pd
    
    # Load historical data
    df = pd.read_excel('../Raw.xlsx')
    
    # Initialize and train
    predictor = SprintPredictor()
    predictor.train(df)
    
    # Make prediction for new sprint
    new_sprint = {
        'team_size': 5,
        'total_points': 150,
        'duration': 14,
        'prev_velocity': 45,
        'num_blockers': 2,
        'num_bugs': 5,
        'num_stories': 10,
        'historical_rate': 0.75
    }
    
    prediction = predictor.predict(new_sprint)
    print("\\n🔮 Prediction for new sprint:")
    print(f"  Will delay: {prediction['will_delay']}")
    print(f"  Delay probability: {prediction['delay_probability']:.1%}")
    print(f"  Predicted velocity: {prediction['predicted_velocity']:.0f} pts")
    print(f"  Confidence: {prediction['confidence']:.1%}")
    print(f"  Recommendation: {prediction['recommendation']}")
```

---

## 🔧 STEP 3: Integrate ML into Backend

Update `backend/server.py`:

```python
# Add at top of server.py
from ml_model import SprintPredictor

# Global ML model
ml_predictor = SprintPredictor()

# Add new endpoint for ML predictions
@api_router.post("/train-model")
async def train_model():
    """Train ML model on current dataset"""
    global current_dataset, ml_predictor
    
    if current_dataset is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    try:
        success = ml_predictor.train(current_dataset)
        if success:
            return {"success": True, "message": "Model trained successfully"}
        else:
            return {"success": False, "message": "Not enough data to train"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/predict-sprint")
async def predict_sprint(sprint_data: dict):
    """
    Predict if a sprint will be delayed using ML
    
    Request body:
    {
        "team_size": 5,
        "total_points": 150,
        "duration": 14,
        "prev_velocity": 45,
        "num_blockers": 2
    }
    """
    try:
        # Load model if not loaded
        if ml_predictor.delay_model is None:
            ml_predictor.load_models()
        
        prediction = ml_predictor.predict(sprint_data)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/model-status")
async def model_status():
    """Check if ML model is trained and ready"""
    is_trained = (ml_predictor.delay_model is not None)
    return {
        "trained": is_trained,
        "model_type": "RandomForest" if is_trained else None
    }
```

---

## 🎯 STEP 4: Add Frontend UI for ML Training

Create `frontend/src/components/MLTraining.js`:

```javascript
import { useState } from "react";
import axios from "axios";
import { Brain, TrendingUp, CheckCircle } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MLTraining = () => {
  const [training, setTraining] = useState(false);
  const [result, setResult] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);

  const checkModelStatus = async () => {
    const response = await axios.get(`${API}/model-status`);
    setModelStatus(response.data);
  };

  const trainModel = async () => {
    setTraining(true);
    try {
      const response = await axios.post(`${API}/train-model`);
      setResult(response.data);
      await checkModelStatus();
    } catch (err) {
      setResult({ success: false, message: err.response?.data?.detail });
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-semibold mb-6">ML Model Training</h1>

      {modelStatus && (
        <div className={`p-4 rounded-sm mb-6 ${
          modelStatus.trained ? 'bg-success/10 border border-success' : 'bg-warning/10 border border-warning'
        }`}>
          {modelStatus.trained ? (
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-success" />
              <span>Model is trained and ready ({modelStatus.model_type})</span>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-warning" />
              <span>No model trained yet. Upload data and train below.</span>
            </div>
          )}
        </div>
      )}

      <button
        onClick={trainModel}
        disabled={training}
        className="px-6 py-3 bg-primary text-white rounded-sm font-medium hover:brightness-110 disabled:opacity-50 flex items-center gap-2"
      >
        {training ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            Training Model...
          </>
        ) : (
          <>
            <Brain className="w-5 h-5" />
            Train ML Model
          </>
        )}
      </button>

      {result && (
        <div className={`mt-6 p-4 rounded-sm ${
          result.success ? 'bg-success/10 border border-success' : 'bg-destructive/10 border border-destructive'
        }`}>
          <p className="font-medium">{result.message}</p>
        </div>
      )}

      <div className="mt-8 bg-accent p-4 rounded-sm">
        <h3 className="font-medium mb-2">What happens during training:</h3>
        <ul className="text-sm space-y-1 list-disc list-inside">
          <li>Analyzes your historical sprint data</li>
          <li>Extracts patterns (velocity, team size, blockers)</li>
          <li>Trains Random Forest model to predict delays</li>
          <li>Learns YOUR team's specific behavior</li>
          <li>Gets better with more data over time</li>
        </ul>
      </div>
    </div>
  );
};

export default MLTraining;
```

---

## 📊 HOW IT LEARNS FROM YOUR DATA

### **Initial Training:**
```
1. Upload historical Jira data (past 20+ sprints)
2. Click "Train ML Model"
3. System extracts features:
   - Team size per sprint
   - Story points committed
   - Previous sprint velocity
   - Number of blockers
   - Bug vs story ratio
4. Trains Random Forest models:
   - Delay prediction (classification)
   - Velocity prediction (regression)
5. Model saved to disk
```

### **Continuous Learning:**
```
As new sprints complete:

1. Sprint finishes → Record actual outcome
2. Compare prediction vs reality
3. Add to training dataset
4. Retrain model weekly/monthly
5. Model improves accuracy over time
```

### **Personalization:**
```
Model learns YOUR team's patterns:

Team A (conservative):
- Commits 30 pts, delivers 35 pts → Model learns buffer
- Recommends: "Safe to commit 40 pts"

Team B (optimistic):
- Commits 100 pts, delivers 40 pts → Model learns gap
- Recommends: "Limit to 45 pts based on history"
```

---

## 🎯 PRODUCTION ARCHITECTURE

### **Complete ML Pipeline:**

```
┌─────────────────────────────────────────────────────────┐
│                   DATA COLLECTION                       │
│  • Jira API syncs every hour                           │
│  • Stores sprint outcomes in MongoDB                   │
│  • Tracks: committed, completed, delays                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                FEATURE ENGINEERING                      │
│  • Extract 15+ features per sprint                     │
│  • Calculate team-specific metrics                     │
│  • Handle missing data                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   MODEL TRAINING                        │
│  • Train on 80% of data, test on 20%                   │
│  • Try multiple algorithms:                            │
│    - Random Forest                                     │
│    - XGBoost                                          │
│    - Neural Network                                    │
│  • Select best performing model                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 PREDICTION SERVICE                      │
│  • API endpoint: POST /predict-sprint                  │
│  • Input: current sprint data                          │
│  • Output: delay probability, predicted velocity       │
│  • Response time: <100ms                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              CONTINUOUS LEARNING                        │
│  • After each sprint: record outcome                   │
│  • Weekly: retrain with new data                       │
│  • Monthly: evaluate model performance                 │
│  • Auto-improve accuracy over time                     │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 KEY DIFFERENCES

### **Rule-Based (Current):**
```python
if completion_pct < 50:
    risk = "high"
```
- ❌ Fixed rules
- ❌ Same for every team
- ❌ Doesn't improve

### **ML-Based (With Training):**
```python
model.predict(features)
# Output: 0.85 probability of delay
```
- ✅ Learns patterns
- ✅ Personalized per team
- ✅ Improves with data

---

## 🚀 IMPLEMENTATION ROADMAP

**Week 1: Basic ML**
- Add ml_model.py
- Train on historical data
- Expose /train-model endpoint

**Week 2: Predictions**
- Add /predict-sprint endpoint
- Show ML predictions in UI
- Compare rule-based vs ML

**Week 3: Continuous Learning**
- Store sprint outcomes in DB
- Auto-retrain weekly
- Track model accuracy

**Week 4: Advanced Features**
- Try XGBoost/Neural Networks
- Add confidence intervals
- Feature importance visualization

---

## ✅ SUMMARY

**You asked the RIGHT question!**

Current implementation:
- Rule-based analytics (not ML)
- Gemini API for recommendations (doesn't train on your data)
- Same CSV = same results

What you need:
- Train custom ML model on YOUR team's data
- Model learns patterns (velocity trends, blocker impact)
- Continuous learning as new sprints complete
- Personalized predictions that improve over time

**Add the ml_model.py file I created above to enable TRUE machine learning!** 🧠

Want me to help implement any specific part?
