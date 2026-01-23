import { useState, useRef, FormEvent } from 'react';
import { useUIStore, useTimelineStore } from '../store';
import { askApi, ApiError } from '../api/client';
import type { AskSource, AskResponse } from '../types';
import ErrorBanner from './ErrorBanner';
import './AskPanel.css';

interface AskPanelProps {
  expanded: boolean;
}

export default function AskPanel({ expanded }: AskPanelProps) {
  const { toggleAskPanel } = useUIStore();
  const { addEvent } = useTimelineStore();
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | Error | null>(null);
  const [highlightedSource, setHighlightedSource] = useState<number | null>(null);

  const sourcesRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    setResponse(null);
    setError(null);
    setHighlightedSource(null);

    try {
      const result = await askApi.ask(query);
      setResponse(result);

      addEvent({
        type: 'ask',
        title: query.slice(0, 50),
        description: `Found ${result.sources.length} sources`,
        metadata: { tokensUsed: result.tokensUsed, model: result.model },
      });
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err);
      } else {
        setError(err instanceof Error ? err : new Error('Failed to get answer'));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCitationClick = (index: number) => {
    setHighlightedSource(index);
    // Scroll to the source card
    const sourceCard = sourcesRef.current?.querySelector(`[data-source-index="${index}"]`);
    if (sourceCard) {
      sourceCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  // Parse answer and make citations clickable
  const renderAnswer = (answer: string) => {
    // Match citation patterns like [1], [2], etc.
    const parts = answer.split(/(\[\d+\])/g);
    return parts.map((part, i) => {
      const match = part.match(/^\[(\d+)\]$/);
      if (match) {
        const index = parseInt(match[1], 10);
        return (
          <button
            key={i}
            className="citation-link"
            onClick={() => handleCitationClick(index)}
            title={`View source ${index}`}
          >
            [{index}]
          </button>
        );
      }
      return <span key={i}>{part}</span>;
    });
  };

  return (
    <div className={`ask-panel ${expanded ? 'expanded' : ''}`}>
      <div className="ask-panel-header" onClick={toggleAskPanel}>
        <div className="header-content">
          <span className="header-icon">💬</span>
          <span className="header-title">Ask your knowledge base</span>
        </div>
        <button className="expand-btn" aria-label={expanded ? 'Collapse' : 'Expand'}>
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            style={{ transform: expanded ? 'rotate(180deg)' : 'none' }}
          >
            <path d="M18 15l-6-6-6 6" />
          </svg>
        </button>
      </div>

      {expanded && (
        <div className="ask-panel-body">
          <ErrorBanner error={error} onDismiss={() => setError(null)} />

          <form onSubmit={handleSubmit} className="ask-form">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about your documents..."
              className="ask-input"
              disabled={loading}
            />
            <button type="submit" className="ask-submit" disabled={loading || !query.trim()}>
              {loading ? (
                <span className="spinner" />
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                </svg>
              )}
            </button>
          </form>

          {response && (
            <div className="response-area">
              <div className="answer-section">
                <h4 className="section-title">Answer</h4>
                <p className="answer-text">{renderAnswer(response.answer)}</p>
                <div className="answer-meta">
                  <span className="meta-item">Model: {response.model}</span>
                  <span className="meta-item">Tokens: {response.tokensUsed.total}</span>
                </div>
              </div>

              {response.sources.length > 0 && (
                <div className="sources-section" ref={sourcesRef}>
                  <h4 className="section-title">Sources ({response.sources.length})</h4>
                  <div className="sources-list">
                    {response.sources.map((source) => (
                      <SourceCard
                        key={source.chunkId}
                        source={source}
                        isHighlighted={highlightedSource === source.index}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

interface SourceCardProps {
  source: AskSource;
  isHighlighted: boolean;
}

function SourceCard({ source, isHighlighted }: SourceCardProps) {
  return (
    <div
      className={`source-card ${isHighlighted ? 'highlighted' : ''}`}
      data-source-index={source.index}
    >
      <div className="source-header">
        <span className="source-index">[{source.index}]</span>
        <span className="source-title">{source.title}</span>
        <span className="source-score">{Math.round(source.score * 100)}%</span>
      </div>
      <p className="source-snippet">{source.snippet}</p>
      {source.sourceUrl && (
        <a
          href={source.sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="source-link"
        >
          View original →
        </a>
      )}
    </div>
  );
}
