/**
 * SourceList - Liste des sources RAG
 * ===================================
 * Affiche les sources utilisées pour la réponse
 */

import React, { useState } from "react";
import type { SourceListProps, RAGSource } from "./types";
import { getCountryEmoji } from "./types";

/**
 * Carte individuelle d'une source
 */
const SourceCard: React.FC<{ source: RAGSource; index: number }> = ({
  source,
  index,
}) => {
  const [expanded, setExpanded] = useState(false);

  const title = source.title || source.source_name || source.source || `Source ${index + 1}`;
  const snippet = source.snippet || source.text || "";
  const url = source.source_url || source.url;
  const country = source.country;

  return (
    <div
      className="rounded-xl p-3 hover:shadow-md transition-shadow cursor-pointer"
      style={{ background: 'var(--card)', border: '1px solid var(--border)' }}
      onClick={() => setExpanded(!expanded)}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h4 className="font-medium text-sm truncate" style={{ color: 'var(--text)' }}>
            {title}
          </h4>

          {/* Meta badges */}
          <div className="flex flex-wrap gap-1.5 mt-1.5">
            {country && (
              <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-xs" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
                {getCountryEmoji(country as any)} {country}
              </span>
            )}
            {source.theme && (
              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
                📁 {source.theme}
              </span>
            )}
            {source.is_official && (
              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
                ✅ Officiel
              </span>
            )}
            {source.score && (
              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs" style={{ background: 'var(--bg)', color: 'var(--iaf-text-secondary)' }}>
                📊 {(source.score * 100).toFixed(0)}%
              </span>
            )}
            {source.date && (
              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs" style={{ background: 'var(--bg)', color: 'var(--iaf-text-secondary)' }}>
                📅 {source.date}
              </span>
            )}
          </div>
        </div>

        {/* Expand icon */}
        <button
          className={`p-1 rounded-lg transition-transform ${expanded ? "rotate-180" : ""}`}
          style={{ color: 'var(--iaf-text-secondary)' }}
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* Snippet preview (collapsed) */}
      {!expanded && snippet && (
        <p className="mt-2 text-xs line-clamp-2" style={{ color: 'var(--iaf-text-secondary)' }}>
          {snippet.substring(0, 150)}...
        </p>
      )}

      {/* Full content (expanded) */}
      {expanded && (
        <div className="mt-3 pt-3" style={{ borderTop: '1px solid var(--border)' }}>
          {/* Full snippet */}
          <p className="text-sm whitespace-pre-wrap" style={{ color: 'var(--text)' }}>
            {snippet}
          </p>

          {/* Tags */}
          {source.tags && source.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {source.tags.map((tag, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded-full text-xs"
                  style={{ background: 'var(--bg)', color: 'var(--iaf-text-secondary)' }}
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}

          {/* Link */}
          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="inline-flex items-center gap-1 mt-3 text-sm hover:underline"
              style={{ color: 'var(--iaf-green)' }}
            >
              🔗 Voir la source
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * Liste des sources
 */
export const SourceList: React.FC<SourceListProps> = ({
  sources,
  maxItems = 5,
  maxVisible,
  collapsed: initialCollapsed,
  collapsedByDefault = true,
  onToggle,
  className = "",
}) => {
  const [collapsed, setCollapsed] = useState(initialCollapsed ?? collapsedByDefault);
  const [showAll, setShowAll] = useState(false);

  // Support both maxItems and maxVisible
  const limit = maxVisible ?? maxItems ?? 5;

  if (!sources || sources.length === 0) {
    return null;
  }

  const displayedSources = showAll ? sources : sources.slice(0, limit);
  const hasMore = sources.length > limit;

  const handleToggle = () => {
    setCollapsed(!collapsed);
    onToggle?.();
  };

  return (
    <div className={`mt-4 ${className}`}>
      {/* Header */}
      <button
        onClick={handleToggle}
        className="flex items-center justify-between w-full px-4 py-2 rounded-xl transition-colors"
        style={{ background: 'var(--card)', border: '1px solid var(--border)' }}
      >
        <div className="flex items-center gap-2">
          <span className="text-lg">📚</span>
          <span className="font-medium" style={{ color: 'var(--text)' }}>
            Sources utilisées
          </span>
          <span className="px-2 py-0.5 rounded-full text-xs font-medium" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
            {sources.length}
          </span>
        </div>
        <svg
          className={`w-5 h-5 transition-transform ${collapsed ? "" : "rotate-180"}`}
          style={{ color: 'var(--iaf-text-secondary)' }}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Sources list */}
      {!collapsed && (
        <div className="mt-3 space-y-2">
          {displayedSources.map((source, index) => (
            <SourceCard key={index} source={source} index={index} />
          ))}

          {/* Show more button */}
          {hasMore && !showAll && (
            <button
              onClick={() => setShowAll(true)}
              className="w-full py-2 text-sm hover:underline"
              style={{ color: 'var(--iaf-green)' }}
            >
              Voir {sources.length - limit} sources de plus...
            </button>
          )}
          {hasMore && showAll && (
            <button
              onClick={() => setShowAll(false)}
              className="w-full py-2 text-sm hover:underline"
              style={{ color: 'var(--iaf-text-secondary)' }}
            >
              Réduire
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default SourceList;
