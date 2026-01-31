import { useState, useRef, FormEvent } from "react";
import { captureApi, ApiError } from "../api/client";
import { useCollectionsStore, useTimelineStore, useDocumentsStore } from "../store";
import ErrorBanner from "./ErrorBanner";
import "./CaptureModal.css";

interface CaptureModalProps {
  isOpen: boolean;
  onClose: () => void;
  preselectedCollectionId?: string;
}

type CaptureType = "text" | "url" | "pdf";

export default function CaptureModal({ isOpen, onClose, preselectedCollectionId }: CaptureModalProps) {
  const { collections } = useCollectionsStore();
  const { addDocument } = useDocumentsStore();
  const { addEvent } = useTimelineStore();

  const [captureType, setCaptureType] = useState<CaptureType>("text");
  const [collectionId, setCollectionId] = useState(preselectedCollectionId || "");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [url, setUrl] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | Error | null>(null);
  const [progressNote, setProgressNote] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const resetForm = () => {
    setCaptureType("text");
    setCollectionId(preselectedCollectionId || "");
    setTitle("");
    setContent("");
    setUrl("");
    setPdfFile(null);
    setError(null);
    setProgressNote(null);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setPdfFile(file);
      if (!title) {
        setTitle(file.name.replace(/\.pdf$/i, ""));
      }
    } else if (file) {
      setError(new Error("Only PDF files are supported here."));
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        const base64 = result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!collectionId) {
      setError(new Error("Please select a collection"));
      return;
    }

    setLoading(true);
    setError(null);
    setProgressNote(null);

    try {
      let captureData: Parameters<typeof captureApi.capture>[0];

      if (captureType === "text") {
        const normalized = content.trim();
        if (!normalized) {
          throw new Error("Please enter some content");
        }
        if (normalized.length < 50) {
          throw new Error("Content is too short (minimum 50 characters).");
        }
        captureData = {
          collectionId,
          sourceType: "text",
          title: title || "Text Note",
          content: normalized,
        };
      } else if (captureType === "url") {
        if (!url.trim()) {
          throw new Error("Please enter a URL");
        }
        try {
          new URL(url);
        } catch {
          throw new Error("Please enter a valid URL.");
        }
        captureData = {
          collectionId,
          sourceType: "url",
          sourceUrl: url,
          title: title || undefined,
        };
      } else if (captureType === "pdf") {
        if (!pdfFile) {
          throw new Error("Please select a PDF file");
        }
        setProgressNote("Preparing PDF…");
        const pdfBase64 = await fileToBase64(pdfFile);
        captureData = {
          collectionId,
          sourceType: "pdf",
          pdfBase64,
          filename: pdfFile.name,
          title: title || pdfFile.name.replace(/\.pdf$/i, ""),
        };
      } else {
        throw new Error("Invalid capture type");
      }

      setProgressNote("Uploading & indexing…");
      const result = await captureApi.capture(captureData);

      addDocument(result.document);
      addEvent({
        type: "capture",
        title: result.document.title,
        description: `Captured ${captureType} (${result.chunksCount} chunks)`,
        metadata: { vectorIndexed: result.vectorIndexed },
      });

      handleClose();
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Capture failed"));
    } finally {
      setLoading(false);
      setProgressNote(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content capture-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Capture Knowledge</h2>
          <button className="modal-close" onClick={handleClose} aria-label="Close">
            ✕
          </button>
        </div>

        <ErrorBanner error={error} onDismiss={() => setError(null)} />

        <form onSubmit={handleSubmit}>
          <div className="capture-tabs">
            <button
              type="button"
              className={`capture-tab ${captureType === "text" ? "active" : ""}`}
              onClick={() => setCaptureType("text")}
              disabled={loading}
            >
              📝 Text
            </button>
            <button
              type="button"
              className={`capture-tab ${captureType === "url" ? "active" : ""}`}
              onClick={() => setCaptureType("url")}
              disabled={loading}
            >
              🔗 URL
            </button>
            <button
              type="button"
              className={`capture-tab ${captureType === "pdf" ? "active" : ""}`}
              onClick={() => setCaptureType("pdf")}
              disabled={loading}
            >
              📄 PDF
            </button>
          </div>

          <div className="form-group">
            <label htmlFor="collection">Collection</label>
            <select
              id="collection"
              value={collectionId}
              onChange={(e) => setCollectionId(e.target.value)}
              required
              disabled={loading}
            >
              <option value="">Select a collection...</option>
              {collections.map((col) => (
                <option key={col.id} value={col.id}>
                  {col.icon || "📁"} {col.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="title">Title (optional)</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={captureType === "url" ? "Auto-detected from page" : "Enter a title..."}
              disabled={loading}
            />
          </div>

          {captureType === "text" && (
            <div className="form-group">
              <label htmlFor="content">Content</label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste or type your text content here..."
                rows={8}
                required
                disabled={loading}
              />
              <span className={`char-count ${content.trim().length > 0 && content.trim().length < 50 ? "warn" : ""}`}>
                {content.length} characters (min 50)
              </span>
            </div>
          )}

          {captureType === "url" && (
            <div className="form-group">
              <label htmlFor="url">URL</label>
              <input
                id="url"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onBlur={() => {
                  if (title.trim()) return;
                  try {
                    const u = new URL(url);
                    const host = u.hostname.replace(/^www\./, "");
                    if (host) setTitle(host);
                  } catch {
                    // ignore
                  }
                }}
                placeholder="https://example.com/article"
                required
                disabled={loading}
              />
              <span className="input-hint">We'll extract the main content from this page</span>
            </div>
          )}

          {captureType === "pdf" && (
            <div className="form-group">
              <label>PDF File</label>
              <div
                className={`file-dropzone ${pdfFile ? "has-file" : ""}`}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                  disabled={loading}
                />
                {pdfFile ? (
                  <div className="file-preview">
                    <span className="file-icon">📄</span>
                    <span className="file-name">{pdfFile.name}</span>
                    <span className="file-size">({(pdfFile.size / 1024).toFixed(1)} KB)</span>
                  </div>
                ) : (
                  <div className="dropzone-prompt">
                    <span className="dropzone-icon">📤</span>
                    <span>Click to select a PDF file</span>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={handleClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Capturing..." : "Capture"}
            </button>
          </div>
          {progressNote && <div className="capture-progress">{progressNote}</div>}
        </form>
      </div>
    </div>
  );
}
