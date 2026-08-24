import { useState, useRef, useCallback } from 'react';

const ACCEPTED_TYPES = [
  'application/pdf',
  'image/png', 'image/jpeg', 'image/jpg',
  'image/webp', 'image/tiff', 'image/bmp',
];
const ACCEPTED_EXT = ['.pdf', '.png', '.jpg', '.jpeg', '.webp', '.tiff', '.bmp'];

function getFileIcon(file) {
  if (!file) return '📄';
  if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) return '📕';
  return '🖼️';
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function UploadZone({ onFileSelect, selectedFile, onClear }) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const validateFile = (file) => {
    const validType = ACCEPTED_TYPES.includes(file.type) ||
      ACCEPTED_EXT.some(ext => file.name.toLowerCase().endsWith(ext));
    if (!validType) {
      setError(`Unsupported file type. Please upload: ${ACCEPTED_EXT.join(', ')}`);
      return false;
    }
    if (file.size > 20 * 1024 * 1024) {
      setError('File is too large. Maximum size is 20MB.');
      return false;
    }
    setError('');
    return true;
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file && validateFile(file)) onFileSelect(file);
  }, [onFileSelect]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    if (!e.currentTarget.contains(e.relatedTarget)) setIsDragging(false);
  }, []);

  const handleInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file && validateFile(file)) onFileSelect(file);
    e.target.value = '';
  };

  const zoneClass = [
    'upload-zone',
    isDragging ? 'drag-active' : '',
    selectedFile ? 'has-file' : '',
  ].filter(Boolean).join(' ');

  return (
    <div>
      <div
        id="upload-drop-zone"
        className={zoneClass}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !selectedFile && inputRef.current?.click()}
        role="button"
        tabIndex={0}
        aria-label="Upload document area"
        onKeyDown={(e) => e.key === 'Enter' && !selectedFile && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          id="file-input"
          type="file"
          accept={ACCEPTED_EXT.join(',')}
          onChange={handleInputChange}
          style={{ display: 'none' }}
          aria-label="Choose file to upload"
        />

        {!selectedFile ? (
          <>
            <div className="upload-icon-wrapper">
              <span className="upload-icon">{isDragging ? '🎯' : '📤'}</span>
            </div>
            <p className="upload-title">
              {isDragging ? 'Drop your document here!' : 'Drag & drop your document'}
            </p>
            <p className="upload-subtitle">or click to browse your files</p>
            <div className="upload-formats">
              {['PDF', 'PNG', 'JPG', 'WEBP', 'TIFF', 'BMP'].map(fmt => (
                <span key={fmt} className="format-badge">{fmt}</span>
              ))}
            </div>
            <button
              className="upload-btn"
              onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
              id="browse-files-btn"
            >
              📂 Browse Files
            </button>
          </>
        ) : (
          <div style={{ pointerEvents: 'none' }}>
            <div className="upload-icon-wrapper">
              <span className="upload-icon">✅</span>
            </div>
            <p className="upload-title">Document ready to process</p>
            <p className="upload-subtitle">Click the button below to generate your summary</p>
          </div>
        )}
      </div>

      {selectedFile && (
        <div className="file-preview">
          <span className="file-icon">{getFileIcon(selectedFile)}</span>
          <div className="file-info">
            <div className="file-name" title={selectedFile.name}>{selectedFile.name}</div>
            <div className="file-size">{formatBytes(selectedFile.size)}</div>
          </div>
          <button
            className="file-remove-btn"
            onClick={onClear}
            title="Remove file"
            id="remove-file-btn"
            aria-label="Remove selected file"
          >
            ✕
          </button>
        </div>
      )}

      {error && (
        <div className="error-banner" style={{ marginTop: '12px' }}>
          <span className="error-icon">⚠️</span>
          <div className="error-content">
            <div className="error-title">Invalid File</div>
            <div className="error-message">{error}</div>
          </div>
        </div>
      )}
    </div>
  );
}
