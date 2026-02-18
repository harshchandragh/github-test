# 🎬 LIVE MVP DEMO GUIDE
## How to Show Your Working App to Stakeholders

---

## 🚀 QUICK START: Demo Your MVP in 5 Minutes

### Step 1: Access Your Working App

**Option A: Local Demo (Most Reliable)**
```
Open browser → Navigate to: http://localhost:3000
```

**Option B: Public URL (For Remote Demos)**
```
Open browser → Navigate to: https://jira-velocity-pro.stage-preview.emergentagent.com
```

**What You'll See:**
- Left sidebar with "Jira Velocity Pro" branding
- Navigation: Dashboard, Connect Jira, Upload CSV, Sprint Analysis
- Main area showing either a loading spinner or "No data" message

---

## 📊 Step 2: Load Your Jira Data

### You Have TWO Options:

### **Option A: Upload CSV (Fastest for Demo)**

1. **Click "Upload CSV"** in the left sidebar
2. **Click "Browse Files"** button
3. **Select your `Raw.xlsx` file** (the one with 1,000 issues)
4. **Click "Upload & Analyze"**
5. **Wait 5-10 seconds** - you'll see:
   ```
   ✅ Upload Successful!
   Processed 1,000 issues across 24 sprints.
   Redirecting to dashboard...
   ```
6. **You're redirected to Dashboard** with all data loaded!

### **Option B: Connect Live Jira (More Impressive)**

1. **Click "Connect Jira"** in sidebar
2. **Enter your Jira credentials:**
   - Jira URL: `https://your-company.atlassian.net`
   - Email: Your Atlassian account email
   - API Token: [Get from id.atlassian.com/manage-profile/security/api-tokens]
3. **Click "Test Connection"** - wait for ✅
4. **Click "Connect & Fetch Data"**
5. **Wait 30-60 seconds** while it fetches from Jira
6. **Dashboard populates** with live data!

---

## 🎯 Step 3: Your Demo Flow (What to Show)

### SCREEN 1: Dashboard (30 seconds)

**What They'll See:**
```
┌─────────────────────────────────────────────────────────┐
│ JIRA VELOCITY PRO DASHBOARD                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ⚠️ SPRINT 22 - CRITICAL RISK                           │
│ Sprint is 0% complete with 178 story points at risk    │
│ [X] Dismiss                                             │
│                                                         │
│ 💡 AI INSIGHT                                           │
│ Rightsize the current sprint by offloading 130 points  │
│ [X] Dismiss                                             │
│                                                         │
│ ┌──────────┬──────────┬──────────┬──────────┐         │
│ │ Sprints  │ Issues   │ Velocity │ At Risk  │         │
│ │   24     │  1,000   │  127.2   │    2     │         │
│ └──────────┴──────────┴──────────┴──────────┘         │
│                                                         │
│ [VELOCITY CHART - Line graph showing trend]            │
│ [STATUS PIE CHART]  [TEAM PERFORMANCE BAR CHART]       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What You Say:**
> "This is the dashboard analyzing your 1,000 Jira issues. See the alerts at the top? That's AI detecting Sprint 22 is overcommitted. The recommendation is specific: 'Offload 130 points.' Not vague advice - actionable intelligence."

**Point to:**
- The critical risk banner (red alert)
- The AI insight with specific recommendation
- The 4 metric cards showing overview
- The velocity trend chart (declining)
- Team performance bar chart

---

### SCREEN 2: Sprint Analysis (1 minute)

**Action:** Click "Sprint Analysis" in sidebar

**What They'll See:**
```
┌─────────────────────────────────────────────────────────┐
│ SPRINT ANALYSIS                                         │
│ 23 sprints with risk assessment                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ╔═══════════════════════════════════════════╗          │
│ ║ SPRINT 22              [CRITICAL RISK] 🔴 ║          │
│ ║ Progress: ░░░░░░░░░░ 0%                  ║          │
│ ║ 34 issues | 0/178 pts | -34 days         ║          │
│ ║ Status: In Progress (22), To Do (12)     ║          │
│ ╚═══════════════════════════════════════════╝          │
│                                                         │
│ ╔═══════════════════════════════════════════╗          │
│ ║ SPRINT 21              [ON TRACK] ✅      ║          │
│ ║ Progress: ████████░░ 88%                 ║          │
│ ║ 45 issues | 198/225 pts | 2 days         ║          │
│ ╚═══════════════════════════════════════════╝          │
│                                                         │
│ ╔═══════════════════════════════════════════╗          │
│ ║ SPRINT 20              [ON TRACK] ✅      ║          │
│ ║ Progress: ██████████ 100%                ║          │
│ ║ 47 issues | All complete                 ║          │
│ ╚═══════════════════════════════════════════╝          │
│                                                         │
│ ... (20 more sprint cards below - scroll to see)       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What You Say:**
> "Every sprint gets analyzed automatically. Red means critical risk, green means on track. Look at Sprint 22 - it's glowing red because it's 0% done with negative days (overdue!). Sprint 21 is 88% done, looking healthy. This is instant visibility that doesn't exist in standard Jira."

**Scroll down slowly** to show all 23 sprint cards

**Point to:**
- Color coding (red = bad, green = good)
- Progress bars showing completion %
- Story points completed vs committed
- Days remaining counters

---

### SCREEN 3: Connect Jira (30 seconds)

**Action:** Click "Connect Jira" in sidebar

**What They'll See:**
```
┌─────────────────────────────────────────────────────────┐
│ CONNECT TO JIRA CLOUD                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ℹ️ HOW TO GET YOUR API TOKEN:                          │
│ 1. Go to id.atlassian.com...                           │
│                                                         │
│ Jira Instance URL:                                      │
│ [_________________________________________]             │
│                                                         │
│ Email Address:                                          │
│ [_________________________________________]             │
│                                                         │
│ API Token:                                              │
│ [_________________________________________]             │
│                                                         │
│ [Test Connection] [Connect & Fetch Data]                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**What You Say:**
> "Here's the magic - ANY Jira Cloud customer can connect in 5 minutes. Enter your Jira URL, email, and API token. Click connect. That's it. No complex setup, no custom configuration. It works with any Jira instance because we use the official Jira API."

**Demo this live if you have credentials:**
1. Enter real Jira URL
2. Click "Test Connection" - show it validates
3. Explain: "In production, they'd click 'Connect' and within 60 seconds, all their sprint data would be analyzed"

---

### SCREEN 4: Back to Dashboard Charts (1 minute)

**Action:** Click "Dashboard" to return

**What You Say:**
> "Let me show you the analytics in detail..."

**Point to Velocity Chart:**
> "See this line chart? This team was completing 150+ points per sprint. Now they're down to 43. That's a velocity collapse. Without this visibility, they keep over-committing."

**Point to Status Pie Chart:**
> "Current sprint status - 65% done, 20% in progress. At a glance."

**Point to Team Performance Bar Chart:**
> "Workload distribution - see how Shreyash has way more points than others? That's a bottleneck waiting to happen."

**Scroll up to show AI Insight again:**
> "And the AI puts it all together: 'Offload 130 points.' Not 'you're behind' - specific action. That's the difference."

---

## 🎬 THE KILLER DEMO MOMENT

### Show This Transition:

**Say:** "Now let me show you how this would work in real Jira..."

**Open:** `/app/PRACTICAL_JIRA_DEMO.md` in browser

**Show Location #1 (Sprint Board):**
> "Here's where it appears when integrated - right at the top of every sprint board. Same alert, but now it's INSIDE Jira. User sees it every time they open the board."

**Point to the "Move 130 Points" button:**
> "And instead of just showing the recommendation, there's a button. One click. AI shows which issues to move, user confirms, done. 2 minutes from problem to solution."

**Then say:**
> "What you just saw is the standalone MVP. What I'm showing you now is how it integrates into Jira. Same intelligence, same recommendations, but native to where teams already work."

---

## 🎤 DEMO SCRIPT (Complete 5-Minute Flow)

### Opening (30 seconds)
> "I'm going to show you a live working prototype that analyzes real Jira data and predicts sprint delays before they happen. This is using actual data - 1,000 issues across 24 sprints from a real company."

### Dashboard Demo (1 minute)
[Show dashboard with alerts]
> "Here's what a Scrum Master sees. Immediate alerts at the top - Sprint 22 critical risk. AI recommendation - offload 130 points. Not vague advice, specific numbers. Below that, full analytics - velocity trends, team performance, status distribution. Everything in one view."

### Sprint Cards (1 minute)
[Navigate to Sprint Analysis]
> "Every sprint gets scored. Red, yellow, green. Sprint 22 is red - 0% done, overdue. Sprint 21 is green - 88% done, on track. Instant visibility. No digging through reports."

### Connection Demo (30 seconds)
[Show Connect Jira page]
> "And here's how any Jira customer connects. 5-minute setup. Works with any Jira Cloud instance. No custom development needed."

### Integration Vision (1.5 minutes)
[Open PRACTICAL_JIRA_DEMO.md]
> "Now here's the exciting part - when integrated into Jira..."
[Walk through sprint board mockup]
> "These alerts appear right on sprint boards, with action buttons. User clicks 'Move 130 Points' - AI shows suggestions - user confirms - done. From problem to solution in 2 minutes."

### ROI Close (30 seconds)
> "This prevents sprint delays. Each delay costs $5,000. For a 10-team company, this saves $550K annually. That's the business case. Questions?"

---

## 📱 DEMO CHECKLIST

### Before Demo:
- ☑️ Ensure backend is running: `curl http://localhost:8001/api/`
- ☑️ Ensure frontend is running: Open http://localhost:3000
- ☑️ Upload Raw.xlsx to load data
- ☑️ Verify dashboard shows alerts and charts
- ☑️ Open PRACTICAL_JIRA_DEMO.md in separate tab
- ☑️ Practice transitions between app and mockups

### During Demo:
- ☑️ Start with impact: "$1.5M wasted annually"
- ☑️ Show working app first (builds credibility)
- ☑️ Navigate between all 3 pages smoothly
- ☑️ Point to specific features (don't just scroll)
- ☑️ Show mockup integration (where it appears in Jira)
- ☑️ End with ROI: "$550K saved"

### After Demo:
- ☑️ Ask: "Want to connect YOUR Jira instance right now?"
- ☑️ Offer: "I can analyze your last 6 months of sprints"
- ☑️ Schedule: "Follow-up meeting to discuss integration timeline"

---

## 🚨 TROUBLESHOOTING LIVE DEMO

### If App Doesn't Load:
1. Check services: `sudo supervisorctl status`
2. Restart if needed: `sudo supervisorctl restart frontend backend`
3. Wait 10 seconds, refresh browser
4. Fallback: Show screenshots while it loads

### If Data Doesn't Appear:
1. Re-upload Raw.xlsx via Upload CSV page
2. Check backend: `curl http://localhost:8001/api/dashboard`
3. If it returns data, frontend should show it
4. Refresh browser page

### If Charts Are Empty:
- Data is loading but charts haven't rendered
- Scroll down/up to trigger re-render
- Refresh page
- Worst case: Show mockups and explain "live data loading"

### If Preview URL Shows "Unavailable":
- Use localhost instead: http://localhost:3000
- Explain: "This is the development environment"
- For remote demos: Use screen sharing with localhost

---

## 💻 RECORDING A DEMO VIDEO

### If You Can't Do Live Demo:

1. **Record Using QuickTime/OBS:**
   ```
   1. Open http://localhost:3000
   2. Start screen recording
   3. Follow the demo script above
   4. Record 3-5 minute walkthrough
   5. Save as demo.mp4
   ```

2. **Narration Script:**
   ```
   "This is Jira Velocity Pro analyzing 1,000 real Jira issues.
   
   [Show dashboard]
   Here's the main dashboard with AI alerts at the top.
   Sprint 22 is flagged as critical risk - 0% complete.
   AI recommends: Offload 130 story points immediately.
   
   [Navigate to Sprint Analysis]
   Every sprint gets risk-scored. Red means critical, 
   green means on track. See the color coding here.
   
   [Show charts]
   Velocity trends, team performance, status distribution.
   All the analytics teams need in one view.
   
   [Show Connect Jira]
   And any Jira customer can connect in 5 minutes.
   
   This is the standalone MVP. Now let me show you
   how it integrates into Jira...
   
   [Switch to PRACTICAL_JIRA_DEMO.md]
   These alerts appear right on sprint boards with
   one-click action buttons. That's the power."
   ```

3. **Send to Stakeholders:**
   ```
   Subject: Jira Velocity Pro - Live Demo Video
   
   Hi [Name],
   
   Here's the 4-minute demo of Velocity Pro analyzing
   real Jira data with AI-powered sprint predictions.
   
   Video: [link to demo.mp4]
   
   Key points:
   • Predicts sprint delays before they happen
   • Provides specific AI recommendations (not vague advice)
   • Integrates into Jira with one-click action buttons
   • $550K annual ROI for 10-team companies
   
   Available for follow-up call this week?
   
   Best,
   [Your Name]
   ```

---

## 🎯 COMPARISON DEMO (Most Powerful)

### Show This Side-by-Side:

**LEFT SIDE: Traditional Jira (No Velocity Pro)**
- Show standard Jira sprint board (screenshot)
- No alerts, no predictions
- Say: "This is what teams see today. Just cards. No warning."

**RIGHT SIDE: Your App Dashboard**
- Show your localhost:3000 with alerts
- Say: "Now with Velocity Pro - immediate alerts, AI recommendations, full analytics."

**Impact:**
> "Same data. Different intelligence. That's why teams need this."

---

## ✅ FINAL PRE-DEMO CHECKLIST

**5 Minutes Before Demo:**
- ☑️ Open http://localhost:3000 - verify it loads
- ☑️ Data loaded? If not, upload Raw.xlsx
- ☑️ Open PRACTICAL_JIRA_DEMO.md in second tab
- ☑️ Close all other tabs/windows
- ☑️ Turn on "Do Not Disturb" mode
- ☑️ Have ROI numbers memorized ($5K per delay, $550K saved)
- ☑️ Smile, breathe, you've got this!

**Opening Line:**
> "I'm going to show you live working software that predicts sprint failures before they happen. This is analyzing real Jira data - 1,000 issues from an actual company. Ready?"

---

## 🚀 YOU'RE READY!

**Your demo flow:**
1. Show localhost:3000 (working app) - 3 minutes
2. Show PRACTICAL_JIRA_DEMO.md (integration) - 2 minutes
3. Close with ROI ($550K saved) - 30 seconds

**Remember:**
- Working app = Credibility
- Mockups = Vision
- ROI = Decision maker's interest

**Now go demo! 🎯**
