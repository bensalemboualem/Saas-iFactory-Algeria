/**
 * Tableau comparatif Algérie vs Suisse
 * Pour comparaisons juridiques/administratives
 */

import React from 'react';
import type { ComparisonRow } from './types';

interface ComparisonTableProps {
  title: string;
  rows: ComparisonRow[];
  showFlags?: boolean;
}

export const ComparisonTable: React.FC<ComparisonTableProps> = ({
  title,
  rows,
  showFlags = true
}) => {
  return (
    <div className="comparison-table-container">
      <h3>{title}</h3>
      <div className="table-responsive">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Critère</th>
              <th>{showFlags ? '🇩🇿 ' : ''}Algérie</th>
              <th>{showFlags ? '🇨🇭 ' : ''}Suisse</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={index}>
                <td className="criterion">{row.criterion}</td>
                <td className="value-dz">{row.algerie}</td>
                <td className="value-ch">{row.suisse}</td>
                <td className="notes">{row.notes || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
