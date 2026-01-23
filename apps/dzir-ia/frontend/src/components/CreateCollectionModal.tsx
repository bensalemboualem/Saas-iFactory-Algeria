import { useState, FormEvent } from 'react';
import { collectionsApi, ApiError } from '../api/client';
import { useCollectionsStore, useTimelineStore } from '../store';
import ErrorBanner from './ErrorBanner';
import './CreateCollectionModal.css';

interface CreateCollectionModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const COLORS = [
  '#00A86B', // Primary green
  '#3B82F6', // Blue
  '#8B5CF6', // Purple
  '#EC4899', // Pink
  '#F59E0B', // Amber
  '#EF4444', // Red
  '#10B981', // Emerald
  '#6366F1', // Indigo
];

const ICONS = ['📁', '📚', '💡', '🎯', '📝', '🔬', '💼', '🎨', '🏠', '🌍', '🤖', '📊'];

export default function CreateCollectionModal({ isOpen, onClose }: CreateCollectionModalProps) {
  const { addCollection } = useCollectionsStore();
  const { addEvent } = useTimelineStore();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [color, setColor] = useState(COLORS[0]);
  const [icon, setIcon] = useState(ICONS[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | Error | null>(null);

  const resetForm = () => {
    setName('');
    setDescription('');
    setColor(COLORS[0]);
    setIcon(ICONS[0]);
    setError(null);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError(new Error('Please enter a collection name'));
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await collectionsApi.create({
        name: name.trim(),
        description: description.trim() || undefined,
        color,
        icon,
      });

      addCollection(result.collection);
      addEvent({
        type: 'sync',
        title: `Created: ${result.collection.name}`,
        description: 'New collection created',
      });

      handleClose();
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create collection'));
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content create-collection-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create Collection</h2>
          <button className="modal-close" onClick={handleClose} aria-label="Close">
            ✕
          </button>
        </div>

        <ErrorBanner error={error} onDismiss={() => setError(null)} />

        <form onSubmit={handleSubmit}>
          {/* Preview */}
          <div className="collection-preview">
            <div className="preview-card">
              <div className="preview-accent" style={{ backgroundColor: color }} />
              <span className="preview-icon">{icon}</span>
              <span className="preview-name">{name || 'Collection Name'}</span>
            </div>
          </div>

          {/* Name */}
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="My Knowledge Base"
              required
              autoFocus
            />
          </div>

          {/* Description */}
          <div className="form-group">
            <label htmlFor="description">Description (optional)</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="What kind of knowledge will this collection hold?"
              rows={3}
            />
          </div>

          {/* Icon Picker */}
          <div className="form-group">
            <label>Icon</label>
            <div className="icon-picker">
              {ICONS.map((i) => (
                <button
                  key={i}
                  type="button"
                  className={`icon-option ${icon === i ? 'active' : ''}`}
                  onClick={() => setIcon(i)}
                >
                  {i}
                </button>
              ))}
            </div>
          </div>

          {/* Color Picker */}
          <div className="form-group">
            <label>Color</label>
            <div className="color-picker">
              {COLORS.map((c) => (
                <button
                  key={c}
                  type="button"
                  className={`color-option ${color === c ? 'active' : ''}`}
                  style={{ backgroundColor: c }}
                  onClick={() => setColor(c)}
                  aria-label={`Select color ${c}`}
                />
              ))}
            </div>
          </div>

          {/* Submit */}
          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={handleClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Collection'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
