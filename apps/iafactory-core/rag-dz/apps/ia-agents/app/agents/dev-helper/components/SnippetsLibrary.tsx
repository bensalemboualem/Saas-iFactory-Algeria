'use client';

import { useState } from 'react';
import { SNIPPETS } from '../data/snippets';
import CodeBlock from './CodeBlock';

export default function SnippetsLibrary() {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [expandedSnippet, setExpandedSnippet] = useState<string | null>(null);

  const categories = ['all', 'react', 'nextjs', 'nodejs', 'python', 'typescript', 'utils'];

  const filteredSnippets = SNIPPETS.filter(snippet => {
    const matchesSearch =
      snippet.name.toLowerCase().includes(search.toLowerCase()) ||
      snippet.description.toLowerCase().includes(search.toLowerCase()) ||
      snippet.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()));

    const matchesCategory = selectedCategory === 'all' || snippet.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">
          💻 Snippets
        </h3>

        {/* Search */}
        <input
          type="text"
          placeholder="Search snippets..."
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
                  ? 'bg-blue-500 text-white'
                  : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-700'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Snippets list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filteredSnippets.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-8">
            No snippets found
          </p>
        ) : (
          filteredSnippets.map((snippet) => (
            <div key={snippet.id} className="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
              <button
                onClick={() => setExpandedSnippet(expandedSnippet === snippet.id ? null : snippet.id)}
                className="w-full text-left p-3 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-slate-900 dark:text-white">
                      {snippet.name}
                    </h4>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                      {snippet.description}
                    </p>
                    <div className="flex gap-1 mt-2">
                      <span className="text-xs px-2 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded">
                        {snippet.language}
                      </span>
                    </div>
                  </div>
                  <span className="text-slate-400">
                    {expandedSnippet === snippet.id ? '−' : '+'}
                  </span>
                </div>
              </button>

              {expandedSnippet === snippet.id && (
                <div className="border-t border-slate-200 dark:border-slate-800 p-3">
                  <CodeBlock code={snippet.code} language={snippet.language} />
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div className="p-3 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 text-center">
        {filteredSnippets.length} snippet{filteredSnippets.length !== 1 ? 's' : ''}
        {search && ' found'}
      </div>
    </div>
  );
}
