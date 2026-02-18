import { useEffect, useState } from "react";
import axios from "axios";
import { AlertCircle, TrendingUp, Clock, CheckCircle2 } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SprintCard = ({ sprint }) => {
  const getRiskColor = (risk) => {
    switch (risk) {
      case 'critical': return 'border-destructive bg-destructive/5';
      case 'high': return 'border-warning bg-warning/5';
      case 'medium': return 'border-warning/50 bg-warning/5';
      default: return 'border-success bg-success/5';
    }
  };

  const getRiskBadge = (risk) => {
    switch (risk) {
      case 'critical': return <span className="px-2 py-1 bg-destructive text-destructive-foreground text-xs font-medium rounded-sm">Critical</span>;
      case 'high': return <span className="px-2 py-1 bg-warning text-white text-xs font-medium rounded-sm">High Risk</span>;
      case 'medium': return <span className="px-2 py-1 bg-warning/70 text-white text-xs font-medium rounded-sm">Medium</span>;
      default: return <span className="px-2 py-1 bg-success text-white text-xs font-medium rounded-sm">On Track</span>;
    }
  };

  return (
    <div className={`bg-background border-2 rounded-sm p-4 shadow-sm ${getRiskColor(sprint.risk_level)}`} data-testid={`sprint-card-${sprint.sprint_name}`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-lg font-medium" data-testid="sprint-name">{sprint.sprint_name}</h3>
          <p className="text-xs text-muted-foreground mt-1">
            {sprint.start_date && new Date(sprint.start_date).toLocaleDateString()} - {sprint.end_date && new Date(sprint.end_date).toLocaleDateString()}
          </p>
        </div>
        {getRiskBadge(sprint.risk_level)}
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-muted-foreground">Progress</span>
          <span className="font-medium" data-testid="completion-percentage">{sprint.completion_percentage.toFixed(0)}%</span>
        </div>
        <div className="w-full bg-muted rounded-full h-2">
          <div
            className={`h-2 rounded-full ${
              sprint.completion_percentage >= 70 ? 'bg-success' :
              sprint.completion_percentage >= 40 ? 'bg-warning' : 'bg-destructive'
            }`}
            style={{ width: `${sprint.completion_percentage}%` }}
            data-testid="progress-bar"
          ></div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-muted-foreground">Total Issues</p>
          <p className="text-lg font-semibold" data-testid="total-issues">{sprint.total_issues}</p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground">Story Points</p>
          <p className="text-lg font-semibold" data-testid="story-points">
            {sprint.completed_story_points.toFixed(0)} / {sprint.total_story_points.toFixed(0)}
          </p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground">Velocity</p>
          <p className="text-lg font-semibold flex items-center gap-1" data-testid="velocity">
            <TrendingUp className="w-4 h-4 text-success" />
            {sprint.velocity.toFixed(0)}
          </p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground">Days Remaining</p>
          <p className="text-lg font-semibold flex items-center gap-1" data-testid="days-remaining">
            <Clock className="w-4 h-4" />
            {sprint.days_remaining !== null ? sprint.days_remaining : 'N/A'}
          </p>
        </div>
      </div>

      {/* Status Distribution */}
      <div className="border-t border-border pt-3">
        <p className="text-xs text-muted-foreground mb-2">Status Distribution</p>
        <div className="flex flex-wrap gap-2">
          {Object.entries(sprint.status_distribution).map(([status, count]) => (
            <span key={status} className="px-2 py-1 bg-secondary text-xs rounded-sm" data-testid={`status-${status.toLowerCase().replace(' ', '-')}`}>
              {status}: {count}
            </span>
          ))}
        </div>
      </div>

      {/* Blocked Issues Warning */}
      {sprint.blocked_story_points > 0 && (
        <div className="mt-3 bg-warning/10 border border-warning/20 rounded-sm p-2 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-warning" />
          <p className="text-xs text-warning">
            {sprint.blocked_story_points.toFixed(0)} story points blocked
          </p>
        </div>
      )}
    </div>
  );
};

const SprintAnalysis = () => {
  const [sprints, setSprints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSprints();
  }, []);

  const fetchSprints = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/sprints`);
      setSprints(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching sprints:', err);
      setError(err.response?.data?.detail || 'Failed to load sprint data');
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
            <h3 className="font-medium text-destructive">Error Loading Data</h3>
            <p className="text-sm text-destructive/80 mt-1">{error}</p>
            <a href="/upload" className="text-sm text-primary hover:underline mt-2 inline-block" data-testid="upload-link">
              Upload Jira Data →
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-[1600px] mx-auto" data-testid="sprint-analysis-page">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight" data-testid="page-title">Sprint Analysis</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Detailed analysis of {sprints.length} sprints with risk assessment and progress tracking
        </p>
      </div>

      {sprints.length === 0 ? (
        <div className="bg-accent border border-border rounded-sm p-8 text-center">
          <CheckCircle2 className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
          <p className="text-muted-foreground">No sprint data available. Upload Jira data to get started.</p>
          <a href="/upload" className="inline-block mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm font-medium hover:brightness-110" data-testid="upload-button">
            Upload Data
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {sprints.map((sprint) => (
            <SprintCard key={sprint.sprint_name} sprint={sprint} />
          ))}
        </div>
      )}
    </div>
  );
};

export default SprintAnalysis;