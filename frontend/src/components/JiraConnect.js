import { useState, useEffect } from "react";
import axios from "axios";
import { Link2, AlertCircle, CheckCircle, RefreshCw, ExternalLink } from "lucide-react";
import { useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const JiraConnect = () => {
  const [formData, setFormData] = useState({
    jira_url: "",
    email: "",
    api_token: ""
  });
  const [testing, setTesting] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [connectResult, setConnectResult] = useState(null);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    checkConnectionStatus();
  }, []);

  const checkConnectionStatus = async () => {
    try {
      const response = await axios.get(`${API}/jira/status`);
      setConnectionStatus(response.data);
    } catch (err) {
      console.error("Error checking connection status:", err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setTestResult(null);
    setError(null);
  };

  const handleTestConnection = async () => {
    if (!formData.jira_url || !formData.email || !formData.api_token) {
      setError("Please fill in all fields");
      return;
    }

    setTesting(true);
    setError(null);
    setTestResult(null);

    try {
      const response = await axios.post(`${API}/jira/test-connection`, formData);
      setTestResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to test connection");
    } finally {
      setTesting(false);
    }
  };

  const handleConnect = async () => {
    if (!formData.jira_url || !formData.email || !formData.api_token) {
      setError("Please fill in all fields");
      return;
    }

    setConnecting(true);
    setError(null);

    try {
      const response = await axios.post(`${API}/jira/connect`, formData);
      setConnectResult(response.data);
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to connect to Jira");
    } finally {
      setConnecting(false);
    }
  };

  const handleRefresh = async () => {
    setConnecting(true);
    setError(null);

    try {
      const response = await axios.post(`${API}/jira/refresh`);
      setConnectResult(response.data);
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to refresh data");
    } finally {
      setConnecting(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto" data-testid="jira-connect-page">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight" data-testid="page-title">
          Connect to Jira
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          Connect your Jira Cloud instance to analyze sprint data in real-time
        </p>
      </div>

      {/* Connection Status */}
      {connectionStatus?.connected && (
        <div className="bg-success/10 border border-success/20 rounded-sm p-4 mb-6 flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-success mt-0.5" />
          <div className="flex-1">
            <h3 className="font-medium text-success">Connected to Jira</h3>
            <p className="text-sm text-success/80 mt-1">
              {connectionStatus.jira_url} ({connectionStatus.email})
            </p>
            <button
              onClick={handleRefresh}
              disabled={connecting}
              className="mt-3 px-4 py-2 bg-success text-white rounded-sm text-sm font-medium hover:brightness-110 disabled:opacity-50 flex items-center gap-2"
              data-testid="refresh-data-button"
            >
              {connecting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Refreshing...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4" />
                  Refresh Data
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-accent border border-border rounded-sm p-4 mb-6">
        <h3 className="text-sm font-medium mb-2 flex items-center gap-2">
          <Link2 className="w-4 h-4" />
          How to get your Jira API token:
        </h3>
        <ol className="text-xs text-muted-foreground space-y-1 list-decimal list-inside">
          <li>Go to <a href="https://id.atlassian.com/manage-profile/security/api-tokens" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline inline-flex items-center gap-1">Atlassian Account Settings <ExternalLink className="w-3 h-3 inline" /></a></li>
          <li>Click "Create API token"</li>
          <li>Give it a label (e.g., "Velocity Pro")</li>
          <li>Copy the token and paste it below</li>
        </ol>
      </div>

      {/* Connection Form */}
      <div className="bg-background border border-border rounded-sm p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2" data-testid="jira-url-label">
              Jira Instance URL
            </label>
            <input
              type="url"
              name="jira_url"
              value={formData.jira_url}
              onChange={handleChange}
              placeholder="https://your-company.atlassian.net"
              className="w-full px-3 py-2 border border-border rounded-sm text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              data-testid="jira-url-input"
            />
            <p className="text-xs text-muted-foreground mt-1">Your Jira Cloud domain (must end with .atlassian.net)</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" data-testid="email-label">
              Email Address
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your-email@company.com"
              className="w-full px-3 py-2 border border-border rounded-sm text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              data-testid="email-input"
            />
            <p className="text-xs text-muted-foreground mt-1">Email associated with your Atlassian account</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" data-testid="api-token-label">
              API Token
            </label>
            <input
              type="password"
              name="api_token"
              value={formData.api_token}
              onChange={handleChange}
              placeholder="••••••••••••••••••••••••"
              className="w-full px-3 py-2 border border-border rounded-sm text-sm focus:outline-none focus:ring-2 focus:ring-primary font-mono"
              data-testid="api-token-input"
            />
            <p className="text-xs text-muted-foreground mt-1">API token from your Atlassian account settings</p>
          </div>
        </div>

        {/* Test Connection Button */}
        <div className="mt-6 flex gap-3">
          <button
            onClick={handleTestConnection}
            disabled={testing}
            className="px-4 py-2 bg-secondary text-foreground border border-border rounded-sm text-sm font-medium hover:bg-accent disabled:opacity-50 flex items-center gap-2"
            data-testid="test-connection-button"
          >
            {testing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-foreground"></div>
                Testing...
              </>
            ) : (
              <>
                <Link2 className="w-4 h-4" />
                Test Connection
              </>
            )}
          </button>

          {testResult?.success && (
            <button
              onClick={handleConnect}
              disabled={connecting}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm font-medium hover:brightness-110 disabled:opacity-50 flex items-center gap-2"
              data-testid="connect-button"
            >
              {connecting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Connecting...
                </>
              ) : (
                "Connect & Fetch Data"
              )}
            </button>
          )}
        </div>

        {/* Test Result */}
        {testResult && (
          <div className={`mt-4 p-4 rounded-sm border flex items-start gap-3 ${
            testResult.success
              ? 'bg-success/10 border-success/20'
              : 'bg-destructive/10 border-destructive/20'
          }`} data-testid="test-result">
            {testResult.success ? (
              <CheckCircle className="w-5 h-5 text-success mt-0.5" />
            ) : (
              <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
            )}
            <div>
              <h3 className={`font-medium text-sm ${testResult.success ? 'text-success' : 'text-destructive'}`}>
                {testResult.success ? 'Connection Successful' : 'Connection Failed'}
              </h3>
              <p className={`text-sm mt-1 ${testResult.success ? 'text-success/80' : 'text-destructive/80'}`}>
                {testResult.message}
              </p>
            </div>
          </div>
        )}

        {/* Connect Result */}
        {connectResult && (
          <div className="mt-4 bg-success/10 border border-success/20 rounded-sm p-4 flex items-start gap-3 alert-enter" data-testid="connect-success">
            <CheckCircle className="w-5 h-5 text-success mt-0.5" />
            <div>
              <h3 className="font-medium text-success">Connected Successfully!</h3>
              <p className="text-sm text-success/80 mt-1">
                Fetched {connectResult.total_issues} issues across {connectResult.total_sprints} sprints.
              </p>
              <p className="text-xs text-success/60 mt-2">Redirecting to dashboard...</p>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 bg-destructive/10 border border-destructive/20 rounded-sm p-4 flex items-start gap-3" data-testid="error-message">
            <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
            <div>
              <h3 className="font-medium text-destructive">Error</h3>
              <p className="text-sm text-destructive/80 mt-1">{error}</p>
            </div>
          </div>
        )}
      </div>

      {/* Alternative Option */}
      <div className="mt-6 text-center">
        <p className="text-sm text-muted-foreground">
          Don't have API access? <a href="/upload" className="text-primary hover:underline" data-testid="upload-csv-link">Upload CSV instead</a>
        </p>
      </div>
    </div>
  );
};

export default JiraConnect;
