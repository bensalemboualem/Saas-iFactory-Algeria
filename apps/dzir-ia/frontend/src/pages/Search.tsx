import { useState, FormEvent } from 'react';
import { useSearchStore, useTimelineStore } from '../store';
import { searchApi } from '../api/client';
import './Search.css';

export default function Search() {
  const { query, results, loading, setQuery, setResults, setLoading } = useSearchStore();
  const { addEvent } = useTimelineStore();
  const [localQuery, setLocalQuery] = useState(query);

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!localQuery.trim() || loading) return;

    setQuery(localQuery);
    setLoading(true);

    try {
      const response = await searchApi.search(localQuery);
      setResults(response.results);

      addEvent({
        type: 'search',
        title: localQuery.slice(0, 50),
        description: `Found ${response.count} results`,
      });
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <header className="page-header">
        <h1>Search</h1>
      </header>

      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-wrapper">
          <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            type="text"
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
            placeholder="Search your knowledge base..."
            className="search-input"
            disabled={loading}
          />
          <button type="submit" className="search-btn" disabled={loading || !localQuery.trim()}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      <div className="search-results">
        {results.length === 0 && query && !loading && (
          <div className="no-results">
            <p>No results found for "{query}"</p>
          </div>
        )}

        {results.map((result) => (
          <div key={result.chunkId} className="result-card">
            <div className="result-header">
              <span className="result-source">{result.document.sourceType}</span>
              <span className="result-score">{Math.round(result.score * 100)}% match</span>
            </div>
            <h3 className="result-title">{result.document.title}</h3>
            <p className="result-content">{result.content}</p>
            {result.document.sourceUrl && (
              <a
                href={result.document.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="result-link"
              >
                View source
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
