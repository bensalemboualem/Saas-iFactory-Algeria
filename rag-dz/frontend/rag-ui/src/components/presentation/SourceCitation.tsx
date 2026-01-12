/**
 * Citations et références légales
 * Format académique/juridique pour IA Factory
 */

import React from 'react';
import type { Source } from './types';

const getCountryFlag = (country: string) => {
  return country === 'DZ' ? '🇩🇿' : '🇨🇭';
};

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'law': 'Loi',
    'decree': 'Décret',
    'circular': 'Circulaire',
    'jurisprudence': 'Jurisprudence',
    'official': 'Document officiel',
    'academic': 'Source académique'
  };
  return labels[type] || type;
};

interface SourceCitationProps {
  sources: Source[];
}

export const SourceCitation: React.FC<SourceCitationProps> = ({ sources }) => {
  // Trier par relevance
  const sortedSources = [...sources].sort((a, b) => b.relevance - a.relevance);

  return (
    <div className="sources-container">
      <ol className="sources-list">
        {sortedSources.map((source) => (
          <li key={source.id} className={`source-item type-${source.type}`}>
            <span className="source-country">{getCountryFlag(source.country)}</span>
            <span className="source-type">[{getTypeLabel(source.type)}]</span>
            <span className="source-title">{source.title}</span>
            {source.reference && (
              <span className="source-reference">({source.reference})</span>
            )}
            {source.date && (
              <span className="source-date"> - {source.date}</span>
            )}
            {source.url && (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
              >
                 🔗
              </a>
            )}
            <span
              className="source-relevance"
              title="Pertinence"
              style={{
                background: `rgba(16, 185, 129, ${source.relevance})`
              }}
            >
              {Math.round(source.relevance * 100)}%
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
};
