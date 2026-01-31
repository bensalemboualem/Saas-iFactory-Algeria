import { Link, useLocation } from 'react-router-dom';
import { useUIStore, useCollectionsStore } from '../store';
import './Sidebar.css';

const NAV_ITEMS = [
  { path: '/', label: 'Home', icon: '🏠' },
  { path: '/onboarding', label: 'Get Started', icon: '🚀' },
  { path: '/ask', label: 'Ask', icon: '💬' },
  { path: '/sources', label: 'Sources', icon: '📁' },
  { path: '/collections', label: 'Collections', icon: '🗂️' },
  { path: '/search', label: 'Search', icon: '🔍' },
  { path: '/timeline', label: 'Timeline', icon: '📅' },
  { path: '/graph', label: 'Graph', icon: '🕸️' },
];

interface SidebarProps {
  onCaptureClick?: () => void;
  onCreateCollectionClick?: () => void;
}

export default function Sidebar({ onCaptureClick, onCreateCollectionClick }: SidebarProps) {
  const location = useLocation();
  const { sidebarOpen, toggleSidebar } = useUIStore();
  const { collections } = useCollectionsStore();

  return (
    <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🧠</span>
          <span className="logo-text">Dzir IA</span>
        </div>
        <button className="toggle-btn" onClick={toggleSidebar} aria-label="Toggle sidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        </button>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* Capture Button */}
      {onCaptureClick && (
        <button className="capture-btn" onClick={onCaptureClick}>
          <span className="capture-icon">➕</span>
          <span className="capture-label">Capture</span>
        </button>
      )}

      <div className="sidebar-section">
        <div className="section-header">
          <span>Collections</span>
          <button
            className="add-btn"
            onClick={onCreateCollectionClick}
            aria-label="Add collection"
          >
            +
          </button>
        </div>
        <ul className="collections-list">
          {collections.length === 0 ? (
            <li className="empty-state">No collections yet</li>
          ) : (
            collections.slice(0, 10).map((collection) => (
              <li key={collection.id}>
                <Link
                  to={`/collections/${collection.id}`}
                  className="collection-item"
                  style={{ '--collection-color': collection.color } as React.CSSProperties}
                >
                  <span className="collection-dot" />
                  <span className="collection-name">{collection.name}</span>
                </Link>
              </li>
            ))
          )}
        </ul>
      </div>

      <div className="sidebar-footer">
        <div className="sync-status">
          <span className="sync-dot online" />
          <span>Synced</span>
        </div>
      </div>
    </aside>
  );
}
