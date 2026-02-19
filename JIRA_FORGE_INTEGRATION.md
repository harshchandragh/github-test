# 🔌 JIRA FORGE INTEGRATION GUIDE
## Converting Your App to Show Prompts Within Jira

---

## 🎯 GOAL: Prompts Appear INSIDE Jira

### **From This (Standalone):**
```
User workflow:
1. Open Jira → Work on sprint
2. Open your app separately → Check predictions
3. Go back to Jira → Take action

Problem: Context switching, not seamless
```

### **To This (Jira-Native):**
```
User workflow:
1. Open Jira sprint board
2. SEE predictions right there at top
3. Click action button → Done

Benefit: No context switch, immediate visibility
```

---

## 🛠️ IMPLEMENTATION OPTIONS

### **Option 1: Jira Forge App (Recommended for Atlassian Marketplace)**

**What is Forge?**
- Atlassian's official platform for building Jira apps
- Your app runs inside Jira's infrastructure
- Appears as native Jira features (panels, banners, pages)

**Architecture:**
```
┌─────────────────────────────────────────────────┐
│           JIRA CLOUD INTERFACE                  │
│  ┌───────────────────────────────────────────┐  │
│  │ Sprint Board                              │  │
│  ├───────────────────────────────────────────┤  │
│  │ ⚠️ YOUR FORGE APP BANNER ← Appears here  │  │
│  │ Sprint 22: 85% delay risk                 │  │
│  │ [Move 60 Points] [View Details]           │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  [TO DO] [IN PROGRESS] [DONE]                   │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

**How to Build:**

#### **Step 1: Install Forge CLI**
```bash
npm install -g @forge/cli

# Login with Atlassian account
forge login
```

#### **Step 2: Create Forge App**
```bash
# Create new Forge app
forge create

# Select options:
# → App template: Custom UI
# → App name: jira-velocity-pro
```

#### **Step 3: Port Your Backend Logic**

Your existing Python backend needs to become Forge backend (Node.js):

**Create `src/index.js`:**
```javascript
import Resolver from '@forge/resolver';
import api, { route } from '@forge/api';

const resolver = new Resolver();

// Your delay prediction logic (ported from Python)
async function predictDelays(projectKey) {
  // Fetch sprint data from Jira API
  const response = await api.asUser().requestJira(
    route`/rest/agile/1.0/board/{projectKey}/sprint`
  );
  
  const sprints = await response.json();
  
  // Apply your prediction algorithm
  const predictions = [];
  for (const sprint of sprints.values) {
    const issues = await getSprintIssues(sprint.id);
    const prediction = analyzeSprintDelay(issues, sprint);
    predictions.push(prediction);
  }
  
  return predictions;
}

// Your prediction algorithm
function analyzeSprintDelay(issues, sprint) {
  // Port your delay_predictor.py logic here
  const totalPoints = issues.reduce((sum, i) => sum + (i.fields.customfield_10016 || 0), 0);
  const completedPoints = issues
    .filter(i => i.fields.status.name === 'Done')
    .reduce((sum, i) => sum + (i.fields.customfield_10016 || 0), 0);
  
  const completionRate = completedPoints / totalPoints;
  
  // Calculate delay probability
  const delayProbability = completionRate < 0.5 ? 0.85 : 0.2;
  
  return {
    sprintName: sprint.name,
    delayProbability,
    riskLevel: delayProbability > 0.7 ? 'critical' : 'low',
    recommendations: generateRecommendations(completionRate, totalPoints)
  };
}

function generateRecommendations(rate, points) {
  if (rate < 0.3) {
    return [`Move ${Math.floor(points * 0.4)} points to next sprint`];
  }
  return ['Sprint on track'];
}

// Expose resolver
resolver.define('getPredictions', async (req) => {
  const { projectKey } = req.context;
  return await predictDelays(projectKey);
});

export const handler = resolver.getDefinitions();
```

#### **Step 4: Create UI Component**

**Create `src/frontend/index.jsx`:**
```jsx
import React, { useEffect, useState } from 'react';
import { invoke } from '@forge/bridge';

function App() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Call your Forge backend
    invoke('getPredictions').then(data => {
      setPredictions(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading predictions...</div>;

  // Show critical predictions as alerts
  const criticalPredictions = predictions.filter(p => p.riskLevel === 'critical');

  return (
    <div>
      {criticalPredictions.map(pred => (
        <div key={pred.sprintName} style={{
          background: '#FFEBE6',
          border: '1px solid #FF5630',
          padding: '16px',
          borderRadius: '3px',
          marginBottom: '8px'
        }}>
          <strong>⚠️ {pred.sprintName}</strong>
          <p>{(pred.delayProbability * 100).toFixed(0)}% chance of delay</p>
          <ul>
            {pred.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
          <button onClick={() => handleAction(pred)}>
            Move Issues
          </button>
        </div>
      ))}
    </div>
  );
}

export default App;
```

#### **Step 5: Configure Where Prompts Appear**

**Edit `manifest.yml`:**
```yaml
modules:
  jira:issuePanelPanel:
    - key: velocity-pro-panel
      title: Sprint Risk Analysis
      function: main
      description: Shows sprint delay predictions
  
  jira:globalPage:
    - key: velocity-pro-dashboard
      title: Velocity Pro Dashboard
      function: main
  
  # Sprint board banner (most visible!)
  jira:boardScope:
    - key: velocity-pro-board-banner
      function: main
      title: Sprint Health
      
function:
  - key: main
    handler: index.handler
  
  - key: frontend
    handler: index.render
    
permissions:
  scopes:
    - read:jira-work
    - read:sprint:jira
    - read:board:jira
```

#### **Step 6: Deploy to Jira**
```bash
# Test locally first
forge tunnel

# Deploy to Jira Cloud
forge deploy

# Install in your Jira instance
forge install

# Now open Jira → Your prompts appear!
```

---

### **Option 2: Jira Connect App (More Control, Self-Hosted)**

If you want to keep your Python backend:

**Architecture:**
```
Your Python Backend (on your server)
          ↓
     Jira Webhooks
          ↓
   Jira Connect iframe
          ↓
  Shows prompts in Jira UI
```

**How it works:**
1. Host your Python backend publicly
2. Create atlassian-connect.json descriptor
3. Jira embeds your UI via iframe
4. Your predictions show inside Jira

**Create `atlassian-connect.json`:**
```json
{
  "key": "jira-velocity-pro",
  "name": "Velocity Pro",
  "baseUrl": "https://your-app-url.com",
  "authentication": {
    "type": "jwt"
  },
  "lifecycle": {
    "installed": "/installed",
    "uninstalled": "/uninstalled"
  },
  "modules": {
    "webPanels": [
      {
        "key": "sprint-risk-banner",
        "location": "atl.jira.view.issue.right.context",
        "url": "/panel?issueKey={issue.key}",
        "name": {
          "value": "Sprint Risk"
        }
      }
    ],
    "generalPages": [
      {
        "key": "velocity-dashboard",
        "location": "system.top.navigation.bar",
        "url": "/dashboard",
        "name": {
          "value": "Velocity Pro"
        }
      }
    ]
  },
  "scopes": [
    "READ",
    "WRITE"
  ]
}
```

**Your backend serves the UI:**
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

@app.get("/panel")
async def sprint_risk_panel(issueKey: str):
    # Get predictions from your existing code
    predictions = delay_predictor.predict_delay(...)
    
    # Return HTML that Jira embeds
    return HTMLResponse(f"""
    <div style="padding: 16px; background: #FFEBE6; border: 1px solid #FF5630;">
      <strong>⚠️ Sprint Risk: {predictions['risk_level']}</strong>
      <p>{predictions['delay_probability']}% chance of delay</p>
      <button onclick="moveIssues()">Move Low Priority Issues</button>
    </div>
    """)
```

---

### **Option 3: Quick Interim Solution (Jira Dashboard Gadget)**

While you build Forge/Connect app, show predictions in Jira dashboard:

**Create iframe gadget:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Module>
  <ModulePrefs title="Velocity Pro Predictions">
    <Require feature="dynamic-height"/>
  </ModulePrefs>
  <Content type="html">
    <![CDATA[
      <iframe 
        src="https://your-app-url.com/dashboard" 
        width="100%" 
        height="600"
        frameborder="0">
      </iframe>
    ]]>
  </Content>
</Module>
```

**Users add this gadget to their Jira dashboard:**
1. Jira → Dashboards → Add Gadget
2. External Gadget → Enter your URL
3. Predictions now visible in Jira!

---

## 🎯 RECOMMENDED APPROACH

### **For Atlassian Marketplace (Long-term):**

**Phase 1: Build Forge App (2-4 weeks)**
- Port your delay_predictor.py logic to Node.js
- Create Forge app with sprint board banners
- Test with your Jira instance
- Submit to Atlassian Marketplace

**Phase 2: Enhance (Ongoing)**
- Add action buttons (move issues, unblock)
- Integrate with Jira automation rules
- Add email notifications
- ML model training in Forge

### **For Immediate Demo (This Week):**

**Quick Win: Dashboard Gadget**
1. Deploy your current app to public URL (Vercel/Heroku)
2. Create iframe gadget XML
3. Add to Jira dashboard
4. Show stakeholders: "Here's predictions IN Jira"

**Benefits:**
- No Forge development needed
- Works immediately
- Proves concept to Atlassian
- Buy time to build proper Forge app

---

## 📋 FORGE APP CONVERSION CHECKLIST

**Backend Logic (Keep Your Algorithms!):**
- [ ] Port delay_predictor.py → JavaScript
- [ ] Test prediction accuracy matches Python version
- [ ] Add Jira API data fetching
- [ ] Implement caching for performance

**Frontend (Forge UI):**
- [ ] Create banner component for sprint boards
- [ ] Add panel component for issue pages
- [ ] Build dashboard page
- [ ] Add action buttons

**Integration:**
- [ ] Configure manifest.yml with all module locations
- [ ] Set up authentication (automatic with Forge)
- [ ] Add webhooks for real-time updates
- [ ] Test with multiple Jira projects

**Deployment:**
- [ ] Test locally with forge tunnel
- [ ] Deploy to Forge infrastructure
- [ ] Install in test Jira instance
- [ ] Submit to Atlassian Marketplace

---

## 💡 BEST PATH FORWARD

**I recommend:**

**1. This Week: Quick Demo**
- Deploy your current app publicly
- Create Jira dashboard gadget
- Show predictions "in Jira" (via gadget)
- Use for Atlassian pitch

**2. Next Month: Build Forge App**
- Learn Forge (1 week)
- Port backend logic (1 week)
- Build UI components (1 week)
- Test and refine (1 week)

**3. After Launch: Enhance**
- Add ML training
- Action button automation
- Email/Slack integration
- Advanced analytics

---

## 🚀 WANT ME TO HELP?

I can help you with:

**A. Convert to Forge App**
- Port Python logic to JavaScript
- Create Forge manifest
- Build UI components

**B. Deploy Current App Publicly**
- Set up Vercel/Heroku deployment
- Create dashboard gadget
- Quick integration for demo

**C. Build Jira Connect App**
- Keep Python backend
- Add iframe integration
- Host on your infrastructure

**Which path do you want to take?** Let me know and I'll help you implement it! 🎯

---

## ✅ SUMMARY

**Your Question:** "I need prompts within Jira"

**Answer:** Build Jira Forge app to show predictions as native Jira features

**Current:** Standalone dashboard (separate from Jira)

**Goal:** Predictions appear inside Jira (sprint boards, issue panels, dashboards)

**Path:** Convert to Forge app OR use dashboard gadget as interim

**Timeline:** 
- Quick demo: This week (gadget)
- Full integration: 4 weeks (Forge app)

**I can help you implement either approach!** 🚀
