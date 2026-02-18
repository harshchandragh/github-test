import { useEffect, useState } from "react";
import axios from "axios";
import { AlertCircle, TrendingUp, Target, Users, Activity } from "lucide-react";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import JiraPrompts from "./JiraPrompts";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StatCard = ({ icon: Icon, label, value, color = "primary" }) => (
  <div className="bg-background border border-border rounded-sm p-4 shadow-sm" data-testid={`stat-card-${label.toLowerCase().replace(' ', '-')}`}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-xs text-muted-foreground font-medium">{label}</p>
        <p className="text-2xl font-semibold mt-1">{value}</p>
      </div>
      <div className={`p-3 rounded-sm bg-${color}/10`}>
        <Icon className={`w-6 h-6 text-${color}`} />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [sprints, setSprints] = useState([]);
  const [teamData, setTeamData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [dashRes, sprintsRes, teamRes] = await Promise.all([
        axios.get(`${API}/dashboard`),
        axios.get(`${API}/sprints`),
        axios.get(`${API}/team-performance`)
      ]);
      
      setDashboardData(dashRes.data);
      setSprints(sprintsRes.data);
      setTeamData(teamRes.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
      setError(err.response?.data?.detail || "No data available. Please upload Jira data first.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen" data-testid="loading-spinner">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-destructive/10 border border-destructive/20 rounded-sm p-4 flex items-start gap-3" data-testid="error-message">
          <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">No Data Available</h3>
            <p className="text-sm text-destructive/80 mt-1">{error}</p>
            <a href="/upload" className="text-sm text-primary hover:underline mt-2 inline-block" data-testid="upload-link">
              Upload Jira Data →
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Prepare velocity chart data
  const velocityData = sprints.slice(0, 10).map(sprint => ({
    name: sprint.sprint_name,
    velocity: sprint.completed_story_points,
    committed: sprint.total_story_points
  }));

  // Prepare status distribution data
  const statusData = sprints.slice(0, 1).flatMap(sprint => 
    Object.entries(sprint.status_distribution).map(([status, count]) => ({
      name: status,
      value: count
    }))
  );

  const STATUS_COLORS = {
    "Done": "hsl(154, 54%, 46%)",
    "In Progress": "hsl(216, 100%, 40%)",
    "To Do": "hsl(220, 13%, 93%)",
    "Blocked": "hsl(14, 100%, 59%)",
    "In Review": "hsl(40, 100%, 50%)",
    "Cancelled": "hsl(218, 17%, 44%)"
  };

  return (
    <div className="p-6 max-w-[1600px] mx-auto" data-testid="dashboard">
      {/* Jira Prompts */}
      <JiraPrompts />

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight" data-testid="dashboard-title">Dashboard</h1>
        <p className="text-sm text-muted-foreground mt-1">Overview of sprint performance and team metrics</p>
      </div>

      {/* Stats Grid */}
      {dashboardData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon={Target} label="Total Sprints" value={dashboardData.total_sprints} />
          <StatCard icon={Activity} label="Total Issues" value={dashboardData.total_issues} />
          <StatCard icon={TrendingUp} label="Avg Velocity" value={dashboardData.average_velocity.toFixed(1)} />
          <StatCard icon={AlertCircle} label="At Risk Sprints" value={dashboardData.at_risk_sprints} color="destructive" />
        </div>
      )}

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        {/* Velocity Chart */}
        <div className="bg-background border border-border rounded-sm p-4 shadow-sm" data-testid="velocity-chart">
          <h3 className="text-lg font-medium mb-4">Sprint Velocity Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={velocityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 13%, 93%)" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="velocity" stroke="hsl(216, 100%, 40%)" strokeWidth={2} name="Completed" />
              <Line type="monotone" dataKey="committed" stroke="hsl(220, 13%, 93%)" strokeWidth={2} strokeDasharray="5 5" name="Committed" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Status Distribution */}
        <div className="bg-background border border-border rounded-sm p-4 shadow-sm" data-testid="status-chart">
          <h3 className="text-lg font-medium mb-4">Current Sprint Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={STATUS_COLORS[entry.name] || "hsl(218, 17%, 44%)"} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Team Performance */}
      <div className="bg-background border border-border rounded-sm p-4 shadow-sm" data-testid="team-performance">
        <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
          <Users className="w-5 h-5" />
          Team Performance
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={teamData.slice(0, 8)}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 13%, 93%)" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="assigned_points" fill="hsl(220, 13%, 93%)" name="Assigned" />
            <Bar dataKey="completed_points" fill="hsl(154, 54%, 46%)" name="Completed" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Dashboard;