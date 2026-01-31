import { useEffect, useMemo, useState } from "react";
import { collectionsApi, documentsApi } from "../api/client";
import { useCollectionsStore, useDocumentsStore, useTimelineStore } from "../store";
import CaptureModal from "../components/CaptureModal";
import "./Sources.css";

export default function Sources() {
  const { collections, setCollections } = useCollectionsStore();
  const { documents, setDocuments, removeDocument, loading, setLoading } = useDocumentsStore();
  const { addEvent } = useTimelineStore();

  const [selectedCollectionId, setSelectedCollectionId] = useState<string>("");
  const [captureOpen, setCaptureOpen] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await collectionsApi.list();
        setCollections(res.collections);
      } catch {
        // non-blocking
      }
    })();
  }, [setCollections]);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const res = await documentsApi.list(selectedCollectionId || undefined);
        setDocuments(res.documents);
      } catch {
        setDocuments([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [selectedCollectionId, setDocuments, setLoading]);

  const filterLabel = useMemo(() => {
    if (!selectedCollectionId) return "Toutes les collections";
    const col = collections.find((c) => c.id === selectedCollectionId);
    return col ? col.name : "Collection";
  }, [collections, selectedCollectionId]);

  const handleDelete = async (id: string, title: string) => {
    if (!confirm(`Supprimer "${title}" ?`)) return;
    try {
      await documentsApi.delete(id);
      removeDocument(id);
      addEvent({
        type: "sync",
        title: `Deleted: ${title}`,
        description: "Document removed",
      });
    } catch {
      alert("Suppression échouée");
    }
  };

  return (
    <div className="sources-page">
      <header className="page-header">
        <div>
          <h1>Sources</h1>
          <p className="sources-sub">{filterLabel}</p>
        </div>
        <div className="sources-actions">
          <select
            value={selectedCollectionId}
            onChange={(e) => setSelectedCollectionId(e.target.value)}
            className="sources-select"
          >
            <option value="">Toutes les collections</option>
            {collections.map((c) => (
              <option key={c.id} value={c.id}>
                {c.icon || "📁"} {c.name}
              </option>
            ))}
          </select>
          <button className="btn-primary" onClick={() => setCaptureOpen(true)}>
            + Capture
          </button>
        </div>
      </header>

      {loading ? (
        <div className="sources-empty">Chargement…</div>
      ) : documents.length === 0 ? (
        <div className="sources-empty">
          <div className="empty-icon">📄</div>
          <h2>Aucune source</h2>
          <p>Ajoute une URL, un PDF ou une note pour commencer.</p>
          <button className="btn-primary" onClick={() => setCaptureOpen(true)}>
            Capturer une source
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
                  Ouvrir la source
                </a>
              )}
              <div className="source-actions">
                <button className="btn-ghost" onClick={() => handleDelete(doc.id, doc.title)}>
                  Supprimer
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <CaptureModal isOpen={captureOpen} onClose={() => setCaptureOpen(false)} />
    </div>
  );
}
