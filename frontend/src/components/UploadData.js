import { useState } from "react";
import axios from "axios";
import { Upload, CheckCircle, AlertCircle, FileSpreadsheet } from "lucide-react";
import { useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const UploadData = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadResult(null);
      setError(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.name.endsWith('.csv') || droppedFile.name.endsWith('.xlsx') || droppedFile.name.endsWith('.xls'))) {
      setFile(droppedFile);
      setUploadResult(null);
      setError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API}/upload-csv`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadResult(response.data);
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'Failed to upload file. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto" data-testid="upload-page">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight" data-testid="upload-title">Upload Jira Data</h1>
        <p className="text-sm text-muted-foreground mt-1">Upload your Jira CSV or Excel export to analyze sprint performance</p>
      </div>

      {/* Instructions */}
      <div className="bg-accent border border-border rounded-sm p-4 mb-6">
        <h3 className="text-sm font-medium mb-2">How to export Jira data:</h3>
        <ol className="text-xs text-muted-foreground space-y-1 list-decimal list-inside">
          <li>Go to your Jira project</li>
          <li>Navigate to Issues → Search for issues</li>
          <li>Click Export → Export Excel (All Fields)</li>
          <li>Upload the exported file here</li>
        </ol>
      </div>

      {/* Upload Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="border-2 border-dashed border-border rounded-sm p-12 text-center bg-background hover:bg-accent/50 transition-colors cursor-pointer"
        data-testid="upload-dropzone"
      >
        <div className="flex flex-col items-center">
          {file ? (
            <FileSpreadsheet className="w-16 h-16 text-primary mb-4" />
          ) : (
            <Upload className="w-16 h-16 text-muted-foreground mb-4" />
          )}
          
          {file ? (
            <div>
              <p className="text-sm font-medium mb-1" data-testid="selected-file-name">{file.name}</p>
              <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          ) : (
            <div>
              <p className="text-sm font-medium mb-1">Drop your Jira export here</p>
              <p className="text-xs text-muted-foreground">or click to browse</p>
            </div>
          )}
          
          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileChange}
            className="hidden"
            id="file-input"
            data-testid="file-input"
          />
          <label
            htmlFor="file-input"
            className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm font-medium hover:brightness-110 cursor-pointer"
            data-testid="browse-button"
          >
            Browse Files
          </label>
        </div>
      </div>

      {/* Upload Button */}
      {file && (
        <div className="mt-6 flex justify-end">
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-sm text-sm font-medium hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            data-testid="upload-submit-button"
          >
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Uploading...
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" />
                Upload & Analyze
              </>
            )}
          </button>
        </div>
      )}

      {/* Success Message */}
      {uploadResult && (
        <div className="mt-6 bg-success/10 border border-success/20 rounded-sm p-4 flex items-start gap-3 alert-enter" data-testid="upload-success">
          <CheckCircle className="w-5 h-5 text-success mt-0.5" />
          <div>
            <h3 className="font-medium text-success">Upload Successful!</h3>
            <p className="text-sm text-success/80 mt-1">
              Processed {uploadResult.total_issues} issues across {uploadResult.total_sprints} sprints.
            </p>
            <p className="text-xs text-success/60 mt-2">Redirecting to dashboard...</p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-6 bg-destructive/10 border border-destructive/20 rounded-sm p-4 flex items-start gap-3" data-testid="upload-error">
          <AlertCircle className="w-5 h-5 text-destructive mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Upload Failed</h3>
            <p className="text-sm text-destructive/80 mt-1">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadData;