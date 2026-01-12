/**
 * ===================================================================
 * LANGUAGE SWITCHER COMPONENT - TRILINGUE
 * Sélecteur de langue réutilisable pour toutes les pages
 * Français | English | العربية
 * ===================================================================
 */

class LanguageSwitcher {
    constructor(container) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.currentLang = window.i18n?.getLanguage() || 'fr';
        this.labels = {
            fr: '🇫🇷 FR',
            en: '🇬🇧 EN',
            ar: '🇩🇿 AR'
        };
        this.fullLabels = {
            fr: '🇫🇷 Français',
            en: '🇬🇧 English',
            ar: '🇩🇿 العربية'
        };

        if (this.container) {
            this.render();
            this.attachEvents();
        }
    }

    render() {
        const html = `
            <div class="language-dropdown">
                <button class="lang-btn" aria-label="Changer de langue / Change language / تغيير اللغة">
                    <span class="lang-icon">🌐</span>
                    <span class="lang-text">${this.labels[this.currentLang]}</span>
                    <svg class="lang-arrow" width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                        <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="2" fill="none"/>
                    </svg>
                </button>
                <div class="lang-menu">
                    <button class="lang-option ${this.currentLang === 'fr' ? 'active' : ''}" data-lang="fr">
                        ${this.fullLabels.fr}
                    </button>
                    <button class="lang-option ${this.currentLang === 'en' ? 'active' : ''}" data-lang="en">
                        ${this.fullLabels.en}
                    </button>
                    <button class="lang-option ${this.currentLang === 'ar' ? 'active' : ''}" data-lang="ar">
                        ${this.fullLabels.ar}
                    </button>
                </div>
            </div>

            <style>
                .language-dropdown {
                    position: relative;
                    display: inline-block;
                }

                .lang-btn {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    padding: 8px 14px;
                    background: var(--iaf-card, #020617);
                    border: 1px solid var(--iaf-border, rgba(255, 255, 255, 0.12));
                    border-radius: var(--iaf-radius, 10px);
                    color: var(--iaf-text, #f8fafc);
                    font-size: 14px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 150ms ease;
                    outline: none;
                }

                .lang-btn:hover {
                    background: var(--iaf-card-hover, #0f172a);
                    border-color: var(--iaf-primary, #00a651);
                }

                [data-theme="light"] .lang-btn {
                    background: #ffffff;
                    color: #0f172a;
                }

                .lang-icon {
                    font-size: 16px;
                }

                .lang-text {
                    font-weight: 600;
                }

                .lang-arrow {
                    transition: transform 200ms ease;
                }

                .lang-btn:hover .lang-arrow,
                .lang-menu.show + .lang-btn .lang-arrow {
                    transform: rotate(180deg);
                }

                .lang-menu {
                    position: absolute;
                    top: calc(100% + 8px);
                    right: 0;
                    min-width: 160px;
                    background: var(--iaf-glass-bg, rgba(15, 23, 42, 0.7));
                    backdrop-filter: blur(14px);
                    border: 1px solid var(--iaf-glass-border, rgba(255, 255, 255, 0.15));
                    border-radius: var(--iaf-radius-lg, 16px);
                    padding: 6px;
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(-10px);
                    transition: all 200ms ease;
                    z-index: 1000;
                    box-shadow: var(--iaf-shadow, 0 20px 60px rgba(0, 0, 0, 0.55));
                }

                [data-theme="light"] .lang-menu {
                    background: rgba(255, 255, 255, 0.95);
                    border-color: rgba(0, 0, 0, 0.1);
                }

                .lang-menu.show {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }

                .lang-option {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    width: 100%;
                    padding: 10px 14px;
                    background: transparent;
                    border: none;
                    border-radius: var(--iaf-radius, 10px);
                    color: var(--iaf-text, #f8fafc);
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                    cursor: pointer;
                    transition: all 150ms ease;
                    outline: none;
                }

                [dir="rtl"] .lang-option {
                    text-align: right;
                }

                .lang-option:hover {
                    background: rgba(0, 166, 81, 0.15);
                    color: var(--iaf-primary, #00a651);
                }

                .lang-option.active {
                    background: var(--iaf-primary, #00a651);
                    color: white;
                    font-weight: 600;
                }

                .lang-option.active:hover {
                    background: var(--iaf-primary-dark, #008c45);
                }

                /* Animation d'entrée */
                @keyframes lang-fade-in {
                    from {
                        opacity: 0;
                        transform: translateY(-10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .lang-btn {
                        padding: 6px 12px;
                        font-size: 13px;
                    }

                    .lang-menu {
                        min-width: 140px;
                    }

                    .lang-option {
                        padding: 8px 12px;
                        font-size: 13px;
                    }
                }
            </style>
        `;

        this.container.innerHTML = html;
    }

    attachEvents() {
        const btn = this.container.querySelector('.lang-btn');
        const menu = this.container.querySelector('.lang-menu');
        const options = this.container.querySelectorAll('.lang-option');

        // Toggle menu
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });

        // Change language
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const lang = option.getAttribute('data-lang');
                this.setLanguage(lang);
                menu.classList.remove('show');
            });
        });

        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.language-dropdown')) {
                menu.classList.remove('show');
            }
        });

        // Close menu on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menu.classList.contains('show')) {
                menu.classList.remove('show');
                btn.focus();
            }
        });
    }

    setLanguage(lang) {
        if (!['fr', 'en', 'ar'].includes(lang)) return;

        this.currentLang = lang;

        // Update i18n instance
        if (window.i18n) {
            window.i18n.setLanguage(lang);
        }

        // Update button label
        const langText = this.container.querySelector('.lang-text');
        if (langText) {
            langText.textContent = this.labels[lang];
        }

        // Update active state
        const options = this.container.querySelectorAll('.lang-option');
        options.forEach(opt => {
            opt.classList.toggle('active', opt.getAttribute('data-lang') === lang);
        });

        // Update HTML lang attribute
        document.documentElement.lang = lang;

        // Update direction for Arabic
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';

        // Translate page
        if (window.i18n) {
            window.i18n.translatePage();
        }

        // Emit custom event
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { lang, previousLang: this.currentLang }
        }));

        // Save to localStorage
        localStorage.setItem('iaf_language', lang);

        // Log for debugging
        console.log(`[IAFactory i18n] Language changed to: ${lang}`);
    }

    getCurrentLanguage() {
        return this.currentLang;
    }

    destroy() {
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// Auto-init on elements with data-language-switcher attribute
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-language-switcher]').forEach(el => {
        new LanguageSwitcher(el);
    });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageSwitcher;
}

// Global export
window.LanguageSwitcher = LanguageSwitcher;
