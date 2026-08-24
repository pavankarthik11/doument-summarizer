import { useState, useCallback, useEffect } from 'react';
import './index.css';
import UploadZone from './components/UploadZone';
import SummaryResult from './components/SummaryResult';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const SUMMARY_LENGTHS = ['short', 'medium', 'long'];

export default function App() {
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('gemini_api_key') || '');
  const [backendHasKey, setBackendHasKey] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [summaryLength, setSummaryLength] = useState('medium');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
          const data = await response.json();
          setBackendHasKey(!!data.has_api_key);
        }
      } catch (err) {
        console.error('Failed to connect to backend for health check:', err);
      }
    };
    checkBackendHealth();
  }, []);

  const hasLocalKey = apiKey.trim().length >= 10;
  const isApiKeyValid = hasLocalKey || backendHasKey;

  const handleFileSelect = useCallback((file) => {
    setSelectedFile(file);
    setResult(null);
    setError('');
  }, []);

  const handleClearFile = useCallback(() => {
    setSelectedFile(null);
    setResult(null);
    setError('');
  }, []);

  const handleProcess = async () => {
    if (!selectedFile) {
      setError('Please select a document to process.');
      return;
    }
    if (!isApiKeyValid) {
      setError('Please enter your Gemini API key above to proceed.');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('length', summaryLength);
      formData.append('api_key', apiKey.trim());

      const response = await fetch(`${API_BASE}/process`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Server error: ${response.status}`);
      }

      setResult(data);
    } catch (err) {
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        setError('Cannot connect to the backend server. Please ensure the backend is running on port 8000.');
      } else {
        setError(err.message || 'An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setResult(null);
    setSelectedFile(null);
    setError('');
  };

  const canProcess = selectedFile && isApiKeyValid && !isLoading;

  return (
    <>
      <div className="app-container">
        {/* ── Header ── */}
        <header className="app-header">
          <div className="app-logo">
            <div className="logo-icon">📄</div>
          </div>
          <h1 className="app-title">Doc Summarizer</h1>
          <p className="app-subtitle">
            AI-powered document analysis — extract insights from any PDF or image instantly
          </p>
        </header>

        {/* ── API Key Input ── */}
        {!backendHasKey && (
          <div className={`api-key-banner ${isApiKeyValid ? 'active' : ''}`} id="api-key-section">
            <label className="api-key-label" htmlFor="api-key-input">Gemini API Key</label>
            <div className="api-key-input-wrapper">
              <input
                id="api-key-input"
                type="password"
                className="api-key-input"
                placeholder="Enter your Google Gemini API key (AIza...)"
                value={apiKey}
                onChange={(e) => {
                  const val = e.target.value;
                  setApiKey(val);
                  localStorage.setItem('gemini_api_key', val);
                }}
                autoComplete="off"
                aria-label="Gemini API Key"
              />
            </div>
            <div className={`api-key-status ${isApiKeyValid ? 'valid' : 'invalid'}`}>
              <span className={`status-dot ${isApiKeyValid ? 'valid' : ''}`} />
              {hasLocalKey ? 'Key set (Browser)' : 'Required'}
            </div>
          </div>
        )}

        {/* ── Main Content ── */}
        {!result ? (
          <>
            {/* Upload Zone */}
            <UploadZone
              onFileSelect={handleFileSelect}
              selectedFile={selectedFile}
              onClear={handleClearFile}
            />

            {/* Controls */}
            <div className="controls-section">
              <div className="length-selector">
                <p className="length-label">Summary Length</p>
                <div className="length-tabs" role="tablist" aria-label="Summary length options">
                  {SUMMARY_LENGTHS.map((len) => (
                    <button
                      key={len}
                      id={`length-${len}-tab`}
                      role="tab"
                      aria-selected={summaryLength === len}
                      className={`length-tab ${summaryLength === len ? 'active' : ''}`}
                      onClick={() => setSummaryLength(len)}
                    >
                      {len.charAt(0).toUpperCase() + len.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <button
                id="process-document-btn"
                className="process-btn"
                onClick={handleProcess}
                disabled={!canProcess}
                aria-label="Generate document summary"
              >
                {isLoading ? (
                  <>
                    <span className="spinner" />
                    Analyzing...
                  </>
                ) : (
                  <>✨ Generate Summary</>
                )}
              </button>
            </div>

            {/* Loading State */}
            {isLoading && (
              <div className="loading-state" role="status" aria-live="polite">
                <div className="loading-orbs">
                  <div className="loading-orb" />
                  <div className="loading-orb" />
                  <div className="loading-orb" />
                </div>
                <p className="loading-text">Processing your document...</p>
                <p className="loading-subtext">
                  Extracting text & generating AI summary — this may take a moment
                </p>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="error-banner" role="alert">
                <span className="error-icon">❌</span>
                <div className="error-content">
                  <div className="error-title">Something went wrong</div>
                  <div className="error-message">{error}</div>
                </div>
              </div>
            )}
          </>
        ) : (
          <SummaryResult data={result} onNewAnalysis={handleNewAnalysis} />
        )}

        {/* ── Footer ── */}
        <footer className="app-footer">
          <p>Powered by Google Gemini 1.5 Flash &nbsp;•&nbsp; Built with FastAPI + React</p>
        </footer>
      </div>
    </>
  );
}
