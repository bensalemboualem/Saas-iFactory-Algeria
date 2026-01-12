/**
 * Alertes juridiques importantes
 * Pour avertissements, mises en garde légales
 */

import React from 'react';
import type { LegalAlertProps } from './types';

export const LegalAlert: React.FC<LegalAlertProps> = ({
  type,
  title,
  content,
  legalBasis
}) => {
  const icons = {
    warning: '⚠️',
    info: 'ℹ️',
    success: '✅',
    error: '❌'
  };

  return (
    <div className={`legal-alert alert-${type}`}>
      <div className="alert-icon">{icons[type]}</div>
      <div className="alert-content">
        <h4>{title}</h4>
        <p>{content}</p>
        {legalBasis && (
          <small className="legal-basis">
            Base légale: {legalBasis}
          </small>
        )}
      </div>
    </div>
  );
};
