import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { collectionsApi, documentsApi } from "../api/client";
import { useDocumentsStore, useTimelineStore } from "../store";
import CaptureModal from "../components/CaptureModal";
import "./CollectionDetail.css";

export default function CollectionDetail() {
  const { id } = useParams();
  const collectionId = id || "";
  const { documents, setDocuments, removeDocument, loading, setLoading } = useDocumentsStore();
  const { addEvent } = useTimelineStore();

  const [collectionName, setCollectionName] = useState("Collection");
  const [collectionDescription, setCollectionDescription] = useState<string | null>(null);
  const [collectionIcon, setCollectionIcon] = useState("📁");
  const [collectionColor, setCollectionColor] = useState("#00A86B");
  const [captureOpen, setCaptureOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!collectionId) return;
    (async () => {
      try {
        const res = await collectionsApi.get(collectionId);
        setCollectionName(res.collection.name);
        setCollectionDescription(res.collection.description || null);
        setCollectionIcon(res.collection.icon || "📁");
        setCollectionColor(res.collection.color || "#00A86B");
      } catch (err) {
        console.error(err);
        setError("Failed to load collection");
      }
    })();
  }, [collectionId]);

  useEffect(() => {
    if (!collectionId) return;
    (async () => {
      setLoading(true);
      try {
        const res = await documentsApi.list(collectionId);
        setDocuments(res.documents);
      } catch (err) {
        console.error(err);
        setDocuments([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [collectionId, setDocuments, setLoading]);

  const documentsCount = useMemo(() => documents.length, [documents]);
  const typeStats = useMemo(() => {
    const stats = documents.reduce<Record<string, number>>((acc, doc) => {
      acc[doc.sourceType] = (acc[doc.sourceType] || 0) + 1;
      return acc;
    }, {});
    return stats;
  }, [documents]);

  const handleDelete = async (docId: string, title: string) => {
    if (!confirm(`Delete "${title}"?`)) return;
    try {
      await documentsApi.delete(docId);
      removeDocument(docId);
      addEvent({
        type: "sync",
        title: `Deleted: ${title}`,
        description: "Document removed",
      });
    } catch {
      alert("Delete failed");
    }
  };

  if (!collectionId) {
    return (
      <div className="collection-detail-page">
        <div className="empty-state">
          <h2>Collection not found</h2>
          <Link to="/collections" className="btn-primary">
            Back to Collections
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="collection-detail-page">
      <header className="page-header">
        <div className="collection-header">
          <Link to="/collections" className="btn-ghost">
            ← Back
          </Link>
          <div className="collection-title">
            <span className="collection-icon" style={{ backgroundColor: collectionColor }}>
              {collectionIcon}
            </span>
            <div>
              <h1>{collectionName}</h1>
              {collectionDescription && (
                <p className="collection-subtitle">{collectionDescription}</p>
              )}
              <p className="collection-meta">{documentsCount} sources</p>
            </div>
          </div>
        </div>
        <div className="collection-actions">
          <Link className="btn-ghost" to="/ask">
            Ask
          </Link>
          <Link className="btn-ghost" to="/search">
            Search
          </Link>
          <button className="btn-primary" onClick={() => setCaptureOpen(true)}>
            + Capture
          </button>
        </div>
      </header>

      <section className="collection-overview">
        <div className="overview-card">
          <div className="overview-label">Total sources</div>
          <div className="overview-value">{documentsCount}</div>
        </div>
        <div className="overview-card">
          <div className="overview-label">Notes</div>
          <div className="overview-value">{typeStats.text || 0}</div>
        </div>
        <div className="overview-card">
          <div className="overview-label">URLs</div>
          <div className="overview-value">{typeStats.url || 0}</div>
        </div>
        <div className="overview-card">
          <div className="overview-label">PDFs</div>
          <div className="overview-value">{typeStats.pdf || 0}</div>
        </div>
      </section>

      {error && <div className="error-banner">{error}</div>}

      {loading ? (
        <div className="sources-empty">Loading…</div>
      ) : documents.length === 0 ? (
        <div className="sources-empty">
          <div className="empty-icon">📄</div>
          <h2>No sources yet</h2>
          <p>Add a URL, PDF, or note to start building this collection.</p>
          <button className="btn-primary" onClick={() => setCaptureOpen(true)}>
            Capture a source
          </button>
        </div>
      ) : (
        <div className="sources-grid">
          {documents.map((doc) => (
            <div key={doc.id} className="source-card">
              <div className="source-header">
                <span className="source-type">{doc.sourceType}</span>
                <span className="source-date">
                  {new Date(doc.createdAt).toLocaleDateString()}
                </span>
              </div>
              <h3 className="source-title">{doc.title}</h3>
              {doc.sourceUrl && (
                <a href={doc.sourceUrl} target="_blank" rel="noreferrer">
                  Open source
                </a>
              )}
              <div className="source-actions">
                <button className="btn-ghost" onClick={() => handleDelete(doc.id, doc.title)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <CaptureModal
        isOpen={captureOpen}
        onClose={() => setCaptureOpen(false)}
        preselectedCollectionId={collectionId}
      />
    </div>
  );
}
