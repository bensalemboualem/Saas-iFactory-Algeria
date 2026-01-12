/**
 * FAQ Expandable/Collapsible
 * Avec animation smooth
 */

import React, { useState } from 'react';
import type { FAQ } from './types';

interface ExpandableFAQProps {
  items: FAQ[];
}

export const ExpandableFAQ: React.FC<ExpandableFAQProps> = ({ items }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  return (
    <div className="faq-container">
      {items.map((item, index) => (
        <div
          key={index}
          className={`faq-item ${expandedIndex === index ? 'expanded' : ''}`}
        >
          <button
            className="faq-question"
            onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
          >
            <span>{item.question}</span>
            <span className="faq-icon">
              {expandedIndex === index ? '▲' : '▼'}
            </span>
          </button>

          <div className={`faq-answer ${expandedIndex === index ? 'show' : ''}`}>
            <p>{item.answer}</p>
            {item.category && (
              <div className="faq-category">
                <small>Catégorie: {item.category}</small>
              </div>
            )}
            {item.relatedSources && item.relatedSources.length > 0 && (
              <div className="faq-sources">
                <small>Sources: {item.relatedSources.join(', ')}</small>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
