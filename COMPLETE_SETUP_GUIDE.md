# 🚀 JIRA VELOCITY PRO - COMPLETE SETUP GUIDE
## Run This Project on Your Own Computer

---

## 📋 PROJECT STRUCTURE

Your complete codebase:

```
jira-velocity-pro/
├── backend/
│   ├── server.py                 # Main FastAPI application
│   ├── jira_client.py           # Jira API client
│   ├── jira_service.py          # Jira data processing
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React app
│   │   ├── App.css             # App styles
│   │   ├── index.js            # Entry point
│   │   ├── index.css           # Global styles
│   │   └── components/
│   │       ├── Dashboard.js         # Main dashboard
│   │       ├── SprintAnalysis.js    # Sprint cards view
│   │       ├── JiraConnect.js       # Jira connection
│   │       ├── JiraPrompts.js       # Alert banners
│   │       └── UploadData.js        # CSV upload
│   ├── package.json            # Node dependencies
│   ├── tailwind.config.js      # Tailwind CSS config
│   └── .env                    # Frontend env vars
│
├── Raw.xlsx                     # Sample Jira data
├── README.md                    # Project documentation
└── SETUP_GUIDE.md              # This file!
```

---

## ⚙️ PREREQUISITES (Install These First)

Before you start, install:

### 1. **Node.js** (v18 or higher)
- Download: https://nodejs.org/
- Install and verify:
  ```bash
  node --version   # Should show v18.x or higher
  npm --version    # Should show 9.x or higher
  ```

### 2. **Python** (v3.9 or higher)
- Download: https://www.python.org/downloads/
- Install and verify:
  ```bash
  python --version   # Should show 3.9+
  pip --version      # Should be installed with Python
  ```

### 3. **MongoDB** (Database)

**Option A: Install Locally**
- Mac: `brew install mongodb-community`
- Windows: Download from https://www.mongodb.com/try/download/community
- Linux: `sudo apt-get install mongodb`

**Option B: Use MongoDB Atlas (Cloud - Easier)**
- Go to https://www.mongodb.com/cloud/atlas
- Create free account
- Create free cluster
- Get connection string (looks like: `mongodb+srv://user:pass@cluster.mongodb.net/`)

### 4. **Code Editor** (Recommended)
- VS Code: https://code.visualstudio.com/

---

## 📥 STEP 1: DOWNLOAD THE CODE

### **Option A: From Emergent Platform**

1. **Contact Emergent Support:**
   ```
   Email: support@emergent.sh
   Subject: Export code for jira-velocity-pro
   
   Hi, I need to export my project "jira-velocity-pro" 
   to run locally. Can you provide a download link or 
   push to GitHub?
   ```

2. **Or use Emergent's GitHub integration:**
   - Go to your Emergent dashboard
   - Find "Push to GitHub" option
   - Connect your GitHub account
   - Push the code

### **Option B: Manual Copy (If you have server access)**

If you have terminal access to the Emergent server:

```bash
# Create zip of your project
cd /app
tar -czf jira-velocity-pro.tar.gz \
  --exclude=node_modules \
  --exclude=__pycache__ \
  --exclude=.git \
  backend/ frontend/ Raw.xlsx *.md

# Download using your preferred method
```

---

## 🛠️ STEP 2: SET UP THE PROJECT LOCALLY

Once you have the code on your computer:

### **1. Extract and Navigate**
```bash
# If you have a zip/tar file
unzip jira-velocity-pro.zip
# or
tar -xzf jira-velocity-pro.tar.gz

# Go to project directory
cd jira-velocity-pro
```

### **2. Set Up Backend**

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install additional required packages
pip install fastapi uvicorn motor pymongo pandas openpyxl httpx tenacity python-jose[cryptography] python-dotenv python-multipart emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### **3. Configure Backend Environment**

Create/edit `backend/.env`:

```bash
# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=jira_analytics
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-94512E272549bF64f4
```

**If using MongoDB Atlas:**
```bash
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=jira_analytics
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-94512E272549bF64f4
```

### **4. Set Up Frontend**

```bash
# Open new terminal
cd jira-velocity-pro/frontend

# Install dependencies
npm install
# or if you prefer yarn:
yarn install

# This will install:
# - React, React Router
# - Tailwind CSS
# - Recharts (for charts)
# - Lucide React (icons)
# - Axios (API calls)
# - All other dependencies from package.json
```

### **5. Configure Frontend Environment**

Create/edit `frontend/.env`:

```bash
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🚀 STEP 3: RUN THE APPLICATION

### **Start Backend Server**

```bash
# In backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Start FastAPI server
python server.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8001
# INFO:     Application startup complete
```

**Backend will run on:** `http://localhost:8001`

**Test it:**
```bash
# Open new terminal
curl http://localhost:8001/api/
# Should return: {"message":"Jira Analytics API"}
```

### **Start Frontend Server**

```bash
# In NEW terminal
cd jira-velocity-pro/frontend

# Start React development server
npm start
# or
yarn start

# Browser should automatically open to http://localhost:3000
```

**Frontend will run on:** `http://localhost:3000`

---

## ✅ STEP 4: VERIFY IT'S WORKING

### **1. Open Browser**
Navigate to: `http://localhost:3000`

You should see:
- ✅ Jira Velocity Pro logo
- ✅ Sidebar with navigation
- ✅ Dashboard (empty until you load data)

### **2. Load Sample Data**

1. Click "Upload CSV" in sidebar
2. Upload the `Raw.xlsx` file
3. Wait for success message
4. Click "Dashboard"
5. You should see:
   - AI alerts
   - Charts
   - Sprint statistics

### **3. Check All Pages**

- ✅ Dashboard - Shows alerts, charts, metrics
- ✅ Connect Jira - Form for Jira credentials
- ✅ Upload CSV - File upload interface
- ✅ Sprint Analysis - 23 sprint cards with risk levels

---

## 🛠️ DEVELOPMENT WORKFLOW

Now you can develop on your own!

### **Making Changes**

**Backend Changes:**
1. Edit files in `backend/`
2. Save file
3. Server auto-reloads (hot reload enabled)
4. Test at `http://localhost:8001/api/`

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Save file
3. Browser auto-refreshes
4. See changes immediately at `http://localhost:3000`

### **Key Files to Modify**

**Backend:**
- `server.py` - Add new API endpoints, modify analytics
- `jira_client.py` - Modify Jira API integration
- `jira_service.py` - Change data processing logic

**Frontend:**
- `src/components/Dashboard.js` - Modify dashboard layout/features
- `src/components/SprintAnalysis.js` - Change sprint card design
- `src/App.js` - Add new routes/pages
- `src/index.css` - Modify global styles

---

## 📚 UNDERSTANDING THE CODE

### **Backend Architecture (FastAPI)**

```python
# server.py - Main API endpoints:

@api_router.post("/upload-csv")
# Accepts CSV/Excel upload, processes with pandas

@api_router.get("/sprints")
# Returns all sprints with risk analysis

@api_router.get("/dashboard")
# Returns overall statistics

@api_router.get("/recommendations")
# Generates AI recommendations using Gemini

@api_router.post("/jira/connect")
# Connects to live Jira instance via API
```

**How Analytics Work:**
1. Upload CSV or connect to Jira
2. Pandas processes data into sprints
3. Calculate: velocity, completion %, risk level
4. Gemini AI generates recommendations
5. Return data as JSON to frontend

### **Frontend Architecture (React)**

```javascript
// App.js - Main routing
- Dashboard (/) - Shows alerts, charts, metrics
- Upload (/upload) - CSV upload interface  
- Connect Jira (/connect) - Live Jira connection
- Sprint Analysis (/sprints) - Individual sprint cards

// Components communicate via:
- API calls to backend (axios)
- State management (useState)
- React Router for navigation
```

**How It Works:**
1. User uploads data or connects Jira
2. Frontend calls backend API
3. Backend processes and returns JSON
4. Frontend displays in charts/cards
5. AI recommendations shown as alert banners

---

## 🔧 COMMON ISSUES & FIXES

### **Issue: "Module not found" errors**

**Fix:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### **Issue: "Port 8001 already in use"**

**Fix:**
```bash
# Find and kill process
# Mac/Linux:
lsof -ti:8001 | xargs kill -9

# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Or change port in server.py:
# uvicorn.run(app, host="0.0.0.0", port=8002)
```

### **Issue: MongoDB connection failed**

**Fix:**
```bash
# Make sure MongoDB is running
# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb

# Or use MongoDB Atlas (cloud) instead
# Update MONGO_URL in backend/.env
```

### **Issue: CORS errors in browser**

**Fix:**
Ensure `backend/.env` has:
```bash
CORS_ORIGINS=http://localhost:3000
```

And restart backend server.

### **Issue: Charts not displaying**

**Fix:**
```bash
# Install chart library
cd frontend
npm install recharts

# Restart frontend
npm start
```

---

## 🎨 CUSTOMIZATION IDEAS

Now that you have full control, you can:

### **1. Add More Analytics**
- Burndown charts
- Issue age analysis
- Cycle time metrics
- Predictive sprint completion date

### **2. Enhance AI Recommendations**
- Use different AI models (GPT-4, Claude)
- Add sentiment analysis on comments
- Predict individual issue completion
- Suggest optimal sprint commitments

### **3. Improve UI**
- Dark mode toggle
- Custom color themes
- More chart types
- Export reports to PDF

### **4. Add Features**
- User authentication
- Team management
- Historical trend analysis
- Email/Slack notifications
- Webhook integrations

### **5. Jira Integration**
- Direct Jira Cloud API (no CSV needed)
- Real-time sync
- Two-way sync (update Jira from app)
- Convert to Forge app for Marketplace

---

## 📦 DEPLOYING TO PRODUCTION

Once you're ready to share:

### **Option 1: Deploy to Vercel (Easiest for Frontend)**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel

# Follow prompts, get URL like:
# https://jira-velocity-pro.vercel.app
```

### **Option 2: Deploy to Heroku (Full Stack)**

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Create app
heroku create jira-velocity-pro

# Add MongoDB addon
heroku addons:create mongolab

# Deploy
git push heroku main

# Get URL: https://jira-velocity-pro.herokuapp.com
```

### **Option 3: Deploy on AWS/GCP/Azure**

Use services like:
- AWS Elastic Beanstalk
- Google App Engine  
- Azure App Service

---

## 📖 LEARNING RESOURCES

To understand and modify the code:

**Backend (Python/FastAPI):**
- FastAPI Docs: https://fastapi.tiangolo.com/
- Pandas Tutorial: https://pandas.pydata.org/docs/
- MongoDB with Python: https://pymongo.readthedocs.io/

**Frontend (React):**
- React Docs: https://react.dev/
- React Router: https://reactrouter.com/
- Recharts: https://recharts.org/

**Jira API:**
- Jira REST API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

**AI Integration:**
- Gemini API: https://ai.google.dev/

---

## 🎯 NEXT STEPS

**Week 1: Get It Running**
- ✅ Install prerequisites
- ✅ Download code
- ✅ Set up environment
- ✅ Run locally
- ✅ Load sample data

**Week 2: Understand the Code**
- Read through server.py
- Understand data flow
- Modify a simple feature
- Test changes locally

**Week 3: Customize**
- Add your own features
- Improve UI
- Enhance analytics
- Test with real Jira data

**Week 4: Prepare for Demo**
- Polish UI
- Test all features
- Deploy to public URL
- Create demo presentation

---

## 💡 PRO TIPS

1. **Use Git for version control:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create branches for new features:**
   ```bash
   git checkout -b feature/new-analytics
   ```

3. **Test before deploying:**
   - Upload different CSV files
   - Try with real Jira data
   - Test on mobile browser

4. **Document your changes:**
   - Update README.md
   - Comment complex code
   - Keep a changelog

5. **Backup regularly:**
   - Push to GitHub
   - Keep local backups
   - Save working versions

---

## ✅ CHECKLIST

Before you start developing:

- [ ] Node.js installed and working
- [ ] Python installed and working
- [ ] MongoDB installed or Atlas account created
- [ ] Code downloaded from Emergent
- [ ] Backend .env file configured
- [ ] Frontend .env file configured
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on localhost:8001
- [ ] Frontend running on localhost:3000
- [ ] Sample data uploads successfully
- [ ] Dashboard displays correctly
- [ ] All pages accessible

---

## 🆘 NEED HELP?

If you get stuck:

1. **Check error messages carefully**
2. **Google the error** - Usually someone has solved it
3. **Check official docs** for the tool you're using
4. **Ask ChatGPT/Claude** - Share the error message
5. **Stack Overflow** - Search or ask questions
6. **Reddit communities:**
   - r/reactjs
   - r/FastAPI
   - r/learnpython

---

## 🚀 YOU'RE READY!

You now have:
- ✅ Complete working codebase
- ✅ Step-by-step setup instructions
- ✅ Understanding of architecture
- ✅ Development workflow
- ✅ Deployment options
- ✅ Customization ideas

**Go build something amazing! 🎯**

Remember: This is YOUR project now. Modify it, improve it, make it your own!

Good luck with your Atlassian pitch! 💪
