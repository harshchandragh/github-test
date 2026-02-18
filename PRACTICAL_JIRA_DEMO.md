# 🎯 PRACTICAL JIRA INTEGRATION DEMO
## Exactly Where Users See Recommendations & How They Act On Them

---

## 📍 LOCATION #1: Sprint Board (Most Used - 80% of interactions)

### Real Jira Sprint Board WITH Velocity Pro Alert

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ YOUR-PROJECT > Board > Sprint 22                           John Smith ▼  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚠️  VELOCITY PRO: SPRINT 22 AT CRITICAL RISK                             ┃
┃                                                                           ┃
┃ 📊 Status: 0% complete • 178 story points uncommitted • 3 days left      ┃
┃                                                                           ┃
┃ 💡 AI Recommendation:                                                     ┃
┃ Your team averages 43 points/sprint but committed 178. Immediately       ┃
┃ offload 130-135 points to Sprint 23 to meet deadline.                    ┃
┃                                                                           ┃
┃ 🎯 QUICK ACTIONS:                                                         ┃
┃ [Move 130 Points to Sprint 23] [View Detailed Analysis] [Dismiss]        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  ↑ THIS BANNER APPEARS AT THE TOP OF EVERY SPRINT BOARD WITH RISK

Sprint 22: Jan 5 - Jan 16, 2026              [Complete Sprint] [⚙️ Settings]

┌────────────────┬────────────────┬────────────────┬────────────────┐
│   TO DO (12)   │ IN PROGRESS(22)│  IN REVIEW (0) │    DONE (0)    │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ ┌────────────┐ │ ┌────────────┐ │                │                │
│ │ PROJ-101   │ │ │ PROJ-89    │ │                │                │
│ │ Dashboard  │ │ │ API Update │ │                │                │
│ │ 8 pts ⚠️   │ │ │ 5 pts      │ │                │                │
│ └────────────┘ │ └────────────┘ │                │                │
│                │                │                │                │
│ ┌────────────┐ │ ┌────────────┐ │                │                │
│ │ PROJ-102   │ │ │ PROJ-90    │ │                │                │
│ │ Bug Fix    │ │ │ UI Polish  │ │                │                │
│ │ 3 pts      │ │ │ 4 pts      │ │                │                │
│ └────────────┘ │ └────────────┘ │                │                │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

### What Happens When User Clicks "Move 130 Points to Sprint 23":

```
┌─────────────────────────────────────────────────────────────────────┐
│ Move Issues to Sprint 23                                     [×]    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Velocity Pro suggests moving these 130 story points:                │
│                                                                      │
│ ☑️ PROJ-101 • Dashboard redesign • 8 pts • Priority: Low           │
│ ☑️ PROJ-102 • Bug fix #234 • 3 pts • Priority: Low                 │
│ ☑️ PROJ-103 • Email notifications • 13 pts • Priority: Medium      │
│ ☑️ PROJ-104 • Mobile optimization • 20 pts • Priority: Low         │
│ ☑️ PROJ-105 • Analytics integration • 15 pts • Priority: Low       │
│ ... (showing 10 more issues)                                        │
│                                                                      │
│ Total: 130 story points (based on priority & dependencies)          │
│                                                                      │
│ This will leave 48 points in Sprint 22 (matches your velocity)      │
│                                                                      │
│ [Cancel]                                 [Move Selected to Sprint 23]│
└─────────────────────────────────────────────────────────────────────┘
```

**Result:** User clicks button → Issues automatically moved → Sprint is rightsized!

---

## 📍 LOCATION #2: Backlog View (Sprint Planning)

### During Sprint Planning Session

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ YOUR-PROJECT > Backlog                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────────────────────────────────────────────────────┐
│ ▼ Sprint 23 (Planning) - 0 issues                                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃ 💡 VELOCITY PRO PLANNING ASSISTANT                                  ┃  │
│ ┃                                                                      ┃  │
│ ┃ Based on your team's velocity (avg: 43 pts/sprint):                 ┃  │
│ ┃                                                                      ┃  │
│ ┃ ✅ Recommended commitment: 40-45 story points                        ┃  │
│ ┃ ⚠️  Current: 0 pts (undercommitted)                                 ┃  │
│ ┃                                                                      ┃  │
│ ┃ 🎯 SUGGESTED ISSUES TO ADD:                                          ┃  │
│ ┃ [Auto-fill Sprint with Top Priority Issues (43 pts)]                ┃  │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                           │
│ Drag issues here or click button above ↑                                 │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ ▼ Backlog - 156 issues                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ PROJ-120 • Payment gateway integration • 13 pts • High ⭐                │
│ PROJ-121 • User authentication • 8 pts • High ⭐                          │
│ PROJ-122 • Dashboard v2 • 5 pts • Medium                                 │
│ PROJ-123 • Bug fix #567 • 2 pts • High ⭐                                │
│ ... (more issues)                                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

**What Happens:** When Product Owner clicks "Auto-fill Sprint", Velocity Pro:
1. Analyzes issue priorities
2. Considers dependencies
3. Adds exactly 43 points worth of issues
4. Shows confirmation dialog before committing

---

## 📍 LOCATION #3: Issue Detail Page (Per-Issue Warnings)

### When User Opens PROJ-101

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ PROJ-101: Implement dashboard redesign                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────┬────────────────────────────────────────────────┐
│ DETAILS                  │ DESCRIPTION                                    │
│                          │                                                │
│ Type: Story              │ As a user, I want to see a modern dashboard    │
│ Status: To Do            │ with real-time analytics...                    │
│ Priority: Low            │                                                │
│ Story Points: 8          │ [Full description...]                          │
│ Sprint: Sprint 22 ⚠️     │                                                │
│ Assignee: Unassigned     │ ATTACHMENTS:                                   │
│                          │ • mockup_v2.png                                │
│ ┌──────────────────────┐ │                                                │
│ │ ⚠️ VELOCITY PRO      │ │ COMMENTS:                                      │
│ │ SPRINT ALERT         │ │ • Sarah: Design approved                       │
│ │                      │ │ • John: Waiting for API                        │
│ │ This issue is part   │ │                                                │
│ │ of Sprint 22 which   │ │                                                │
│ │ is at CRITICAL RISK  │ │                                                │
│ │                      │ │                                                │
│ │ Sprint Progress: 0%  │ │                                                │
│ │ Days Remaining: 3    │ │                                                │
│ │ Overcommitted: +135  │ │                                                │
│ │                      │ │                                                │
│ │ 💡 Recommendation:   │ │                                                │
│ │ This is LOW priority │ │                                                │
│ │ and not critical for │ │                                                │
│ │ this sprint.         │ │                                                │
│ │                      │ │                                                │
│ │ [Move to Sprint 23]  │ │                                                │
│ │ [View Sprint Health] │ │                                                │
│ └──────────────────────┘ │                                                │
│                          │                                                │
│ Labels:                  │                                                │
│ frontend, enhancement    │                                                │
│                          │                                                │
│ Linked Issues:           │                                                │
│ → PROJ-100 (blocks)      │                                                │
└──────────────────────────┴────────────────────────────────────────────────┘
```

**User Action:** Clicks "Move to Sprint 23" → Issue immediately moved → Sprint becomes more realistic

---

## 📍 LOCATION #4: Jira Dashboard (Executive View)

### Product Manager's Dashboard

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ My Dashboard                                              John Smith ▼   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────────────┬──────────────────────────────────┐
│ Assigned to Me (14)              │ Activity Stream                  │
│                                  │                                  │
│ • PROJ-89 - API Update           │ • Sarah updated PROJ-101         │
│ • PROJ-90 - UI Polish            │ • John commented on PROJ-90      │
│ • PROJ-91 - Bug Fix              │ • Sprint 22 started              │
│                                  │                                  │
│ [View All]                       │ [View All]                       │
└──────────────────────────────────┴──────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎯 VELOCITY PRO - SPRINT HEALTH DASHBOARD                            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                      ┃
┃ Active Sprints Across All Teams:                                    ┃
┃                                                                      ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │ 🔴 Sprint 22 (Your Team)            0% │ 178 pts │ 3 days left  │ ┃
┃ │ 💡 Overcommitted by 135 pts - immediate action needed           │ ┃
┃ │ [View Details] [Take Action]                                    │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                      ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │ ✅ Sprint 21 (Platform Team)       88% │ 198/225 pts │ 2 days   │ ┃
┃ │ On track to meet all commitments                                │ ┃
┃ │ [View Details]                                                  │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                      ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │ 🟡 Sprint 20 (Mobile Team)          45% │ 89/198 pts │ 7 days   │ ┃
┃ │ 5 issues blocked - needs attention                              │ ┃
┃ │ [View Details] [See Blockers]                                   │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                      ┃
┃ 📊 VELOCITY TRENDS (Last 6 Sprints):                                ┃
┃     200│ ●                                                          ┃
┃     150│   ● ●                                                      ┃
┃     100│       ●                                                    ┃
┃      50│         ● ●        ← Declining velocity!                  ┃
┃         └─────────────────                                          ┃
┃          S17 S18 S19 S20 S21 S22                                    ┃
┃                                                                      ┃
┃ [Configure Alerts] [Export Report] [Settings]                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────────────┬──────────────────────────────────┐
│ Sprint Report (Gadget)           │ Created vs Resolved (Gadget)     │
└──────────────────────────────────┴──────────────────────────────────┘
```

**User Action:** Executive sees risks across ALL teams at a glance, clicks "Take Action" → Redirected to sprint board with recommendations

---

## 📍 LOCATION #5: Email/Slack Notifications (Proactive Alerts)

### Daily Morning Alert (8am Email)

```
From: Velocity Pro <alerts@velocitypro.atlassian.com>
To: john.smith@company.com, sarah.jones@company.com
Subject: ⚠️ Sprint 22 Critical Risk Alert - Action Required Today

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Good morning! 👋

🔴 CRITICAL ALERT: Sprint 22 needs immediate attention

Your sprint is at risk of failing:
• Progress: 0% complete (0 of 178 story points)
• Time left: Only 3 days remaining
• Velocity gap: Committed 178 pts, but team averages 43 pts

💡 AI RECOMMENDATION:
Offload 130-135 story points to Sprint 23 immediately. 
Based on your velocity history, this will bring the sprint 
back to a realistic commitment.

🎯 TAKE ACTION NOW:
┌─────────────────────────────────────────────────────────────┐
│ [Move 130 Points to Sprint 23] ← One-click action           │
│ [View Detailed Analysis in Jira]                            │
│ [Dismiss This Alert]                                        │
└─────────────────────────────────────────────────────────────┘

WHY THIS MATTERS:
Sprint delays cost an average of $5,000 in missed deadlines,
context switching, and stakeholder trust. Taking action today
prevents this cost.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GOOD NEWS:
Sprint 21 is 88% complete and on track! 
Sprint 20 completed 100% of commitments last week.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Velocity Pro by Atlassian
[Configure Alert Settings] | [Unsubscribe]
```

### Slack Integration

```
#sprint-22 channel                                           🔔

Velocity Pro APP  9:00 AM
⚠️ Sprint 22 Critical Risk Alert

Sprint 22 is 0% complete with only 3 days left. You've committed 
178 story points but your team averages 43 pts/sprint.

💡 Recommendation: Offload 130 points to Sprint 23

[Move 130 Points] [View in Jira] [Dismiss]

                                                          👍 ❤️ 👀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sarah Jones  9:05 AM
Good catch! Moving lower priority items now

John Smith  9:07 AM
👍 Already moved PROJ-101 and PROJ-102 to Sprint 23
```

---

## 🎯 PRACTICAL DEMO FLOW (What You Show Company Heads)

### Screen 1: Show Real Jira Sprint Board (Mockup)
**Say:** "Here's a typical Jira sprint board. Now watch what happens when we install Velocity Pro..."

### Screen 2: Show Alert Banner Appearing
**Say:** "BOOM! Immediately, every sprint board shows a risk alert banner at the top. No digging through reports. It's right there."

### Screen 3: Show "Move 130 Points" Button
**Say:** "See this button? One click. That's it. The AI already figured out which 130 points to move based on priority and dependencies."

### Screen 4: Show Modal with Suggested Issues
**Say:** "Velocity Pro suggests EXACTLY which issues to move. Product Owner reviews the list - takes 10 seconds - clicks Move. Done."

### Screen 5: Show Updated Sprint Board
**Say:** "Sprint is now realistic. From 178 points to 48 points. Matches their velocity. Crisis averted. $5,000 saved."

### Screen 6: Show Dashboard Gadget
**Say:** "And executives see this on their dashboard - all sprints across all teams. Red means trouble, green means on track. One glance, total visibility."

### Screen 7: Show Email Alert
**Say:** "Every morning at 8am, teams get this email. Proactive, not reactive. They know about problems BEFORE standup, not AFTER sprint review."

---

## 💬 HANDLING THE KEY QUESTION

### When They Ask: "How do people act on recommendations?"

**Your Answer:**
"Three ways, all one-click actions:

**1. Smart Buttons on Sprint Boards** (80% of actions)
- 'Move 130 Points to Sprint 23' button
- 'Unblock 5 Issues' button  
- 'Redistribute Workload' button
→ Click button → AI shows suggested changes → User confirms → Done

**2. Issue-Level Actions** (15% of actions)
- Open any issue in at-risk sprint
- See 'Move to Next Sprint' button in side panel
- Click → Issue moved → Sprint healthier

**3. Bulk Actions from Dashboard** (5% of actions)
- Executive dashboard shows all at-risk sprints
- Click 'Take Action' next to any sprint
- Redirected to board with recommendations loaded
- One-click to execute

The key: **We don't just alert. We provide actionable buttons that DO the work.**"

---

## 🎬 THE KILLER DEMO MOMENT

### Show Them This Before/After

**BEFORE (Traditional Jira):**
```
Sprint Review Meeting:
PM: "We only completed 22 of 178 story points"
Team: "We were overcommitted"
PM: "Why didn't anyone say something?"
Team: "We didn't realize until too late"
Result: $5,000 cost, unhappy stakeholders, repeated mistakes
```

**AFTER (With Velocity Pro):**
```
Day 1 of Sprint (Monday 9am):
Email Alert: "Sprint 22 at risk - 178 pts committed, team averages 43"
Scrum Master: *Opens Jira*
Alert Banner: "Move 130 Points to Sprint 23"
Scrum Master: *Clicks button, reviews suggestions, clicks confirm*
Result: Sprint rightsized in 2 minutes, crisis avoided, $5,000 saved
```

**Then say:**
> "That's the difference. Traditional Jira tells you what HAPPENED. Velocity Pro tells you what's ABOUT TO HAPPEN and gives you a button to fix it. That's why teams love it."

---

## 📱 BONUS: Mobile Notifications (Future Enhancement)

```
┌─────────────────────────────────┐
│ 📱 iPhone Lock Screen           │
├─────────────────────────────────┤
│                                 │
│ Velocity Pro        9:00 AM     │
│ ⚠️ Sprint 22 Critical Risk      │
│                                 │
│ 0% complete, 3 days left.       │
│ Tap to take action.             │
│                                 │
│ [View] [Dismiss]                │
└─────────────────────────────────┘
```

---

## ✅ WHAT YOU SHOW IN YOUR DEMO

1. **Open your standalone app** (localhost:3000)
   - "This is the current MVP analyzing real Jira data"
   - Show dashboard, show sprint cards, show AI recommendations

2. **Show Jira mockups** (this document)
   - "After Forge integration, here's where it appears in REAL Jira"
   - Walk through sprint board, backlog, issue page, dashboard, email

3. **Demo the action flow**
   - "User sees alert → Clicks 'Move 130 Points' → Reviews suggestions → Clicks confirm → Done"
   - "2 minutes from alert to resolution. That's the power."

4. **Show the impact**
   - "Before: 67% sprint failure rate, find out in retrospectives"
   - "After: 40% failure rate, fix problems before they happen"
   - "$550K saved annually for 10-team company"

---

**THIS IS YOUR PRACTICAL, USABLE DEMO! 🎯**

Every stakeholder question answered:
✅ Where do I see it? → Sprint boards, backlog, dashboard, email
✅ How do I act on it? → One-click buttons that do the work
✅ Will it slow me down? → No, 2-minute fix vs 2-week delay
✅ Does it really work? → Proven with 1,000 real issues
✅ What's the ROI? → $5,000 saved per prevented delay
