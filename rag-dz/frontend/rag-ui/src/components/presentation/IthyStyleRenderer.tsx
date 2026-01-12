/**
 * Composant principal de rendu style ithy.ai
 * Transforme les réponses RAG en articles HTML riches
 * Adapté pour IA Factory (Algérie/Suisse)
 */

import React from 'react';
import { ChartRenderer } from './ChartRenderer';
import { ExpandableFAQ } from './ExpandableFAQ';
import { SourceCitation } from './SourceCitation';
import { ComparisonTable } from './ComparisonTable';
import { LegalAlert } from './LegalAlert';
import type { IthyResponseProps, Section } from './types';

const SectionRenderer: React.FC<{ section: Section }> = ({ section }) => {
  switch (section.type) {
    case 'text':
      return (
        <section className="ithy-section text-section">
          <h2>
            {section.icon && <span className="section-icon">{section.icon}</span>}
            {section.title}
          </h2>
          <div className="section-content"
            dangerouslySetInnerHTML={{ __html: section.content }}
          />
        </section>
      );

    case 'table':
      return (
        <section className="ithy-section table-section">
          <ComparisonTable {...section.content} />
        </section>
      );

    case 'chart':
      return (
        <section className="ithy-section chart-section">
          <ChartRenderer chart={section.content} />
        </section>
      );

    case 'alert':
      return (
        <section className="ithy-section alert-section">
          <LegalAlert {...section.content} />
        </section>
      );

    case 'faq':
      return (
        <section className="ithy-section faq-section">
          <h2>{section.title}</h2>
          <ExpandableFAQ items={section.content} />
        </section>
      );

    default:
      return null;
  }
};

export const IthyStyleRenderer: React.FC<IthyResponseProps> = ({
  title,
  sections,
  sources,
  charts,
  faqs,
  metadata
}) => {
  const formatDate = (date: Date) => {
    const lang = metadata.language === 'ar' ? 'ar-DZ' : metadata.language === 'fr' ? 'fr-FR' : 'en-US';
    return date.toLocaleDateString(lang, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <article className="ithy-article" dir={metadata.language === 'ar' ? 'rtl' : 'ltr'}>
      {/* Header avec métadonnées */}
      <header className="ithy-header">
        <h1>{title}</h1>
        <div className="ithy-meta">
          <span
            className="confidence-badge"
            title="Niveau de confiance basé sur les sources"
          >
            Fiabilité: {Math.round(metadata.confidence * 100)}%
          </span>
          {metadata.agents && metadata.agents.length > 0 && (
            <span className="agents-used" title="Agents consultés">
              🤖 Sources: {metadata.agents.join(', ')}
            </span>
          )}
          <span className="generated-at" title="Date de génération">
            🕐 {formatDate(metadata.generatedAt)}
          </span>
          <span className="language-badge">
            🌐 {metadata.language.toUpperCase()}
          </span>
        </div>
      </header>

      {/* Sections dynamiques */}
      <main className="ithy-content">
        {sections.map(section => (
          <SectionRenderer key={section.id} section={section} />
        ))}

        {/* Charts additionnels */}
        {charts && charts.length > 0 && (
          <section className="ithy-section charts-section">
            <h2>📊 Visualisations</h2>
            {charts.map((chart, index) => (
              <ChartRenderer key={index} chart={chart} />
            ))}
          </section>
        )}
      </main>

      {/* FAQ Expandable */}
      {faqs && faqs.length > 0 && (
        <section className="ithy-faq">
          <h2>❓ Questions Fréquentes</h2>
          <ExpandableFAQ items={faqs} />
        </section>
      )}

      {/* Sources et Citations */}
      {sources && sources.length > 0 && (
        <footer className="ithy-sources">
          <h2>📚 Sources et Références</h2>
          <SourceCitation sources={sources} />
        </footer>
      )}
    </article>
  );
};
