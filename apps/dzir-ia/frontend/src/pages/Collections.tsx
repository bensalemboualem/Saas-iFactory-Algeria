import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useCollectionsStore, useTimelineStore } from '../store';
import { collectionsApi } from '../api/client';
import { CreateCollectionModal } from '../components';
import './Collections.css';

export default function Collections() {
  const { collections, loading, error, setCollections, setLoading, setError } = useCollectionsStore();
  const { addEvent } = useTimelineStore();
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    async function fetchCollections() {
      setLoading(true);
      try {
        const response = await collectionsApi.list();
        setCollections(response.collections);
        setError(null);
      } catch (err) {
        setError('Failed to load collections');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchCollections();
  }, [setCollections, setLoading, setError]);

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Delete collection "${name}"? This cannot be undone.`)) return;

    try {
      await collectionsApi.delete(id);
      setCollections(collections.filter((c) => c.id !== id));
      addEvent({
        type: 'sync',
        title: `Deleted: ${name}`,
        description: 'Collection removed',
      });
    } catch (err) {
      console.error(err);
      alert('Failed to delete collection');
    }
  };

  if (loading) {
    return (
      <div className="collections-page">
        <div className="loading-state">Loading collections...</div>
      </div>
    );
  }

  return (
    <div className="collections-page">
      <header className="page-header">
        <h1>Collections</h1>
        <button className="btn-primary" onClick={() => setShowCreateModal(true)}>
          + New Collection
        </button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {collections.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <h2>No collections yet</h2>
          <p>Create your first collection to start organizing your knowledge.</p>
          <button className="btn-primary" onClick={() => setShowCreateModal(true)}>
            Create Collection
          </button>
        </div>
      ) : (
        <div className="collections-grid">
          {collections.map((collection) => (
            <div key={collection.id} className="collection-card">
              <div
                className="card-accent"
                style={{ backgroundColor: collection.color || '#00A86B' }}
              />
              <div className="card-content">
                <div className="card-header">
                  <span className="card-icon">{collection.icon || '📁'}</span>
                  <h3>{collection.name}</h3>
                </div>
                {collection.description && (
                  <p className="card-description">{collection.description}</p>
                )}
                <div className="card-meta">
                  <span>{collection.documentsCount || 0} documents</span>
                  <span>{new Date(collection.createdAt).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="card-actions">
                <Link to={`/collections/${collection.id}`} className="btn-ghost">
                  Open
                </Link>
                <button
                  className="btn-ghost btn-danger"
                  onClick={() => handleDelete(collection.id, collection.name)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <CreateCollectionModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
      />
    </div>
  );
}
