'use client';

import { useState } from 'react';
import { FORMULAS } from '../data/formulas';

export default function FormulaLibrary() {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const categories = ['all', 'geometrie', 'algebre', 'analyse', 'trigonometrie'];

  const filteredFormulas = FORMULAS.filter(formula => {
    const matchesSearch =
      formula.name.toLowerCase().includes(search.toLowerCase()) ||
      formula.formula.toLowerCase().includes(search.toLowerCase());

    const matchesCategory = selectedCategory === 'all' || formula.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">
          📐 Formules
        </h3>

        {/* Search */}
        <input
          type="text"
          placeholder="Chercher une formule..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input-field text-sm mb-3"
        />

        {/* Category filter */}
        <div className="flex flex-wrap gap-1">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`text-xs px-2 py-1 rounded ${
                selectedCategory === category
                  ? 'bg-purple-500 text-white'
                  : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-700'
              }`}
            >
              {category === 'all' ? 'Toutes' : category}
            </button>
          ))}
        </div>
      </div>

      {/* Formulas list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filteredFormulas.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-8">
            Aucune formule trouvée
          </p>
        ) : (
          filteredFormulas.map((formula) => (
            <div
              key={formula.id}
              className="p-3 border border-slate-200 dark:border-slate-800 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
            >
              <h4 className="text-sm font-medium text-slate-900 dark:text-white mb-1">
                {formula.name}
              </h4>
              <div className="font-mono text-sm bg-slate-100 dark:bg-slate-900 p-2 rounded my-2 text-purple-700 dark:text-purple-300">
                {formula.formula}
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-400">
                {formula.description}
              </p>
              <div className="flex gap-1 mt-2">
                <span className="text-xs px-2 py-0.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded">
                  {formula.level}
                </span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div className="p-3 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 text-center">
        {filteredFormulas.length} formule{filteredFormulas.length !== 1 ? 's' : ''}
        {search && ' trouvée(s)'}
      </div>
    </div>
  );
}
