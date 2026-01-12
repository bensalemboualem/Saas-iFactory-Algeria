/**
 * IAFactory Searcher - RAG Search Integration
 * Connects to backend API for document search
 */

// Dynamic API URL detection
const getApiUrl = () => (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : window.location.origin;

class IAFactorySearcher {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || getApiUrl();
        this.language = options.language || 'fr';
        this.searchHistory = [];

        this.init();
    }

    init() {
        this.searchInput = document.getElementById('search-input');
        this.searchButton = document.getElementById('search-button');
        this.resultsContainer = document.getElementById('search-results');
        this.answerContainer = document.getElementById('ai-answer');
        this.loadingIndicator = document.getElementById('loading');

        if (this.searchButton) {
            this.searchButton.addEventListener('click', () => this.search());
        }

        if (this.searchInput) {
            this.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.search();
                }
            });
        }
    }

    async search() {
        const query = this.searchInput?.value?.trim();
        if (!query) return;

        this.showLoading(true);
        this.clearResults();

        try {
            const searchResults = await this.searchDocuments(query);
            const aiAnswer = await this.getAIAnswer(query, searchResults);
            this.displayAnswer(aiAnswer);
            this.displayResults(searchResults);
            this.searchHistory.push({ query, timestamp: new Date() });
        } catch (error) {
            console.error('Search error:', error);
            this.displayError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async searchDocuments(query) {
        // Combined endpoint: /api/query returns both results and AI answer
        const response = await fetch(this.apiUrl + '/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Tenant-ID': 'default'
            },
            body: JSON.stringify({
                query: query,
                max_results: 10,
                score_threshold: 0.3,
                use_cache: true
            })
        });

        if (!response.ok) {
            throw new Error('Search failed: ' + response.status);
        }

        const data = await response.json();
        // Store the AI answer for later use
        this._lastAiAnswer = data.answer || null;
        return data.results || [];
    }

    async getAIAnswer(query, context) {
        // Return the cached answer from searchDocuments
        // The /api/query endpoint already returns the AI answer
        if (this._lastAiAnswer) {
            const answer = this._lastAiAnswer;
            this._lastAiAnswer = null;
            return answer;
        }
        return 'Aucune réponse disponible';
    }

    displayAnswer(answer) {
        if (!this.answerContainer) return;

        const labels = {
            fr: 'Reponse IA',
            ar: 'إجابة الذكاء الاصطناعي',
            en: 'AI Answer'
        };

        this.answerContainer.innerHTML = '<div class="ai-answer-card"><div class="answer-header"><i class="fas fa-robot"></i><span>' + (labels[this.language] || labels.fr) + '</span></div><div class="answer-content">' + this.formatAnswer(answer) + '</div></div>';
    }

    formatAnswer(answer) {
        if (!answer) return '<em>Aucune reponse</em>';
        return answer.replace(/\n/g, '<br>');
    }

    displayResults(results) {
        if (!this.resultsContainer) return;

        if (!results.length) {
            this.resultsContainer.innerHTML = '<div class="no-results"><i class="fas fa-search"></i><p>' + this.getNoResultsText() + '</p></div>';
            return;
        }

        const labels = {
            fr: { source: 'Source', score: 'Pertinence' },
            ar: { source: 'المصدر', score: 'الصلة' },
            en: { source: 'Source', score: 'Relevance' }
        };
        const l = labels[this.language] || labels.fr;

        this.resultsContainer.innerHTML = results.map((result, index) => '<div class="search-result-card" data-index="' + index + '"><div class="result-header"><span class="result-title">' + (result.title || 'Document ' + (index + 1)) + '</span><span class="result-score">' + l.score + ': ' + Math.round((result.score || 0) * 100) + '%</span></div><div class="result-content">' + this.truncate(result.text || result.content, 200) + '</div><div class="result-meta"><span>' + l.source + ': ' + (result.source || 'N/A') + '</span></div></div>').join('');
    }

    truncate(text, length) {
        if (!text) return '';
        if (text.length <= length) return text;
        return text.substring(0, length) + '...';
    }

    getNoResultsText() {
        const texts = {
            fr: 'Aucun resultat trouve',
            ar: 'لم يتم العثور على نتائج',
            en: 'No results found'
        };
        return texts[this.language] || texts.fr;
    }

    displayError(message) {
        if (this.answerContainer) {
            this.answerContainer.innerHTML = '<div class="error-card"><i class="fas fa-exclamation-triangle"></i><span>' + message + '</span></div>';
        }
    }

    showLoading(show) {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = show ? 'flex' : 'none';
        }
        if (this.searchButton) {
            this.searchButton.disabled = show;
        }
    }

    clearResults() {
        if (this.resultsContainer) this.resultsContainer.innerHTML = '';
        if (this.answerContainer) this.answerContainer.innerHTML = '';
    }

    setLanguage(lang) {
        this.language = lang;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.searcher = new IAFactorySearcher({
        apiUrl: window.API_URL || getApiUrl(),
        language: document.documentElement.lang || 'fr'
    });
});
