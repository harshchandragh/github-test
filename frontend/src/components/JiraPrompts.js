import { useEffect, useState } from "react";
import axios from "axios";
import { AlertCircle, AlertTriangle, CheckCircle, Info, X } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const JiraPrompts = () => {
  const [prompts, setPrompts] = useState([]);
  const [dismissedPrompts, setDismissedPrompts] = useState(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`${API}/recommendations`);
      setPrompts(response.data);
    } catch (err) {
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const dismissPrompt = (id) => {
    setDismissedPrompts(prev => new Set([...prev, id]));
  };

  const getPromptIcon = (type) => {
    switch (type) {
      case 'critical': return <AlertCircle className="w-5 h-5" />;
      case 'warning': return <AlertTriangle className="w-5 h-5" />;
      case 'success': return <CheckCircle className="w-5 h-5" />;
      default: return <Info className="w-5 h-5" />;
    }
  };

  const getPromptStyles = (type) => {
    switch (type) {
      case 'critical':
        return 'bg-destructive/10 border-l-4 border-l-destructive text-destructive';
      case 'warning':
        return 'bg-warning/10 border-l-4 border-l-warning text-warning';
      case 'success':
        return 'bg-success/10 border-l-4 border-l-success text-success';
      default:
        return 'bg-accent border-l-4 border-l-primary text-primary';
    }
  };

  const visiblePrompts = prompts.filter(prompt => !dismissedPrompts.has(prompt.id));

  if (loading || visiblePrompts.length === 0) {
    return null;
  }

  return (
    <div className="mb-6 space-y-3" data-testid="jira-prompts-container">
      {visiblePrompts.map((prompt) => (
        <div
          key={prompt.id}
          className={`rounded-sm p-4 shadow-md flex items-start gap-3 alert-enter ${getPromptStyles(prompt.prompt_type)}`}
          data-testid={`jira-prompt-${prompt.prompt_type}`}
        >
          <div className="mt-0.5">{getPromptIcon(prompt.prompt_type)}</div>
          <div className="flex-1">
            <h4 className="font-medium text-sm" data-testid="prompt-title">{prompt.title}</h4>
            <p className="text-sm opacity-90 mt-1" data-testid="prompt-message">{prompt.message}</p>
            <p className="text-xs opacity-70 mt-2">{prompt.sprint_name}</p>
          </div>
          <button
            onClick={() => dismissPrompt(prompt.id)}
            className="text-current opacity-70 hover:opacity-100 transition-opacity"
            data-testid="dismiss-prompt-button"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};

export default JiraPrompts;