import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../../i18n';
import './Solutions.css';
import { solutions, solutionTags } from '../../data/solutions';

function normalizeText(text: string) {
  return text
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

export default function Solutions() {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [expandedTitle, setExpandedTitle] = useState<string | null>(null);

  const filteredSolutions = useMemo(() => {
    const query = normalizeText(searchTerm);
    return solutions.filter((solution) => {
      const matchesSearch =
        query.length === 0 ||
        normalizeText(
          `${solution.title} ${solution.description} ${solution.tags.join(' ')}`
        ).includes(query);
      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.every((tag) => solution.tags.includes(tag));
      return matchesSearch && matchesTags;
    });
  }, [searchTerm, selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedTags([]);
    setExpandedTitle(null);
  };

  return (
    <section className="solutions-section" id="solutions">
      <div className="container">
        <div className="solutions-header">
          <div className="solutions-title">
            <h2>{t('solutions_title')}</h2>
            <p>{t('solutions_subtitle')}</p>
          </div>

          <div className="solutions-toolbar">
            <div className="solutions-count">
              {filteredSolutions.length} {t('solutions_count_label')}
            </div>
            <div className="solutions-actions">
              <span>{t('solutions_filter_label')}</span>
              <button type="button" className="solutions-clear" onClick={clearFilters}>
                {t('solutions_clear')}
              </button>
            </div>
          </div>
        </div>

        <div className="solutions-controls">
          <div className="solutions-search">
            <input
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder={t('solutions_search_placeholder')}
              aria-label={t('solutions_search_placeholder')}
            />
          </div>

          <div className="solutions-tags">
            {solutionTags.map((tag) => (
              <button
                key={tag}
                type="button"
                className={`solution-chip ${selectedTags.includes(tag) ? 'active' : ''}`}
                onClick={() => toggleTag(tag)}
                aria-pressed={selectedTags.includes(tag)}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>

        <div className="solutions-grid">
          {filteredSolutions.map((solution) => {
            const isExpanded = expandedTitle === solution.title;
            const visibleTags = solution.tags.slice(0, 4);
            const remainingTags = solution.tags.length - visibleTags.length;
            return (
              <article key={solution.title} className="solution-card">
                <h3>{solution.title}</h3>
                <p>{solution.description}</p>

                <div className="solution-tags-inline">
                  {visibleTags.map((tag) => (
                    <span key={tag} className="solution-tag">
                      {tag}
                    </span>
                  ))}
                  {remainingTags > 0 && (
                    <span className="solution-tag">+{remainingTags}</span>
                  )}
                </div>

                <div className="solution-actions">
                  <Link to="/chat" className="btn-primary">
                    {t('solutions_try')}
                  </Link>
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => setExpandedTitle(isExpanded ? null : solution.title)}
                    aria-expanded={isExpanded}
                  >
                    {isExpanded ? t('solutions_close') : t('solutions_view')}
                  </button>
                </div>

                {isExpanded && (
                  <div className="solution-details">
                    <strong>{t('solutions_use_case')}</strong>
                    <div>{solution.example}</div>
                    <strong>{t('solutions_outcome')}</strong>
                    <div>{solution.outcome}</div>
                  </div>
                )}
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
