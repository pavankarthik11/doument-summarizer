import { useState } from 'react';

export default function SummaryResult({ data, onNewAnalysis }) {
  const [copiedField, setCopiedField] = useState(null);

  const copy = async (text, field) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    } catch {
      /* clipboard not available */
    }
  };

  const formatCount = (n) => n.toLocaleString();

  return (
    <section className="results-section" aria-label="Summary Results">
      {/* ── Header ── */}
      <div className="results-header">
        <h2 className="results-title">
          <span className="results-title-icon">✨</span>
          Analysis Complete
        </h2>
        <div className="results-meta">
          <span className={`meta-badge type-${data.file_type}`}>
            {data.file_type === 'pdf' ? '📕 PDF' : '🖼️ Image'}
          </span>
          <span className="meta-badge">📝 {formatCount(data.word_count)} words</span>
          <span className="meta-badge">🔤 {formatCount(data.char_count)} chars</span>
        </div>
      </div>

      {/* ── Key Points ── */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-title-icon">🎯</span>
            Key Points
          </h3>
          <button
            id="copy-key-points-btn"
            className={`copy-btn ${copiedField === 'key_points' ? 'copied' : ''}`}
            onClick={() => copy(data.key_points.map((p, i) => `${i + 1}. ${p}`).join('\n'), 'key_points')}
            aria-label="Copy key points"
          >
            {copiedField === 'key_points' ? '✅ Copied!' : '📋 Copy'}
          </button>
        </div>
        <ul className="key-points-list" role="list">
          {data.key_points.map((point, idx) => (
            <li key={idx} className="key-point-item">
              <span className="key-point-number">{idx + 1}</span>
              <p className="key-point-text">{point}</p>
            </li>
          ))}
        </ul>
      </div>

      {/* ── Summary ── */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-title-icon">📄</span>
            Summary
          </h3>
          <button
            id="copy-summary-btn"
            className={`copy-btn ${copiedField === 'summary' ? 'copied' : ''}`}
            onClick={() => copy(data.summary, 'summary')}
            aria-label="Copy summary"
          >
            {copiedField === 'summary' ? '✅ Copied!' : '📋 Copy'}
          </button>
        </div>
        <p className="summary-text">{data.summary}</p>
      </div>

      {/* ── Improvement Suggestions ── */}
      {data.improvement_suggestions?.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <span className="card-title-icon">💡</span>
              Improvement Suggestions
            </h3>
          </div>
          <ul className="suggestions-list" role="list">
            {data.improvement_suggestions.map((suggestion, idx) => (
              <li key={idx} className="suggestion-item">
                <span className="suggestion-icon">💡</span>
                <p className="suggestion-text">{suggestion}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── New Analysis ── */}
      <button
        id="new-analysis-btn"
        className="new-analysis-btn"
        onClick={onNewAnalysis}
        aria-label="Start new document analysis"
      >
        ↩️ Analyze Another Document
      </button>
    </section>
  );
}
