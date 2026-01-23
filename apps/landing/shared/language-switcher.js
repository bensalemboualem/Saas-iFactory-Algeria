/**
 * IAFactory Language Switcher Component
 * Provides a dropdown for switching between FR/AR/EN
 * Version: 1.0.0
 */

(function() {
    'use strict';

    // Language configuration
    const languages = {
        fr: { name: 'Francais', flag: '🇫🇷', code: 'FR' },
        en: { name: 'English', flag: '🇬🇧', code: 'EN' },
        ar: { name: 'العربية', flag: '🇩🇿', code: 'AR' }
    };

    /**
     * Create language switcher HTML
     * @returns {string} HTML string for the language switcher
     */
    function createSwitcherHTML() {
        const currentLang = localStorage.getItem('iafactory_lang') || 'fr';
        const current = languages[currentLang] || languages.fr;

        return `
            <div class="iaf-lang-switcher">
                <button class="iaf-lang-btn lang-btn" onclick="IAFactoryLangSwitcher.toggle(event)">
                    ${current.flag} ${current.code}
                </button>
                <div class="iaf-lang-menu" id="langMenu">
                    ${Object.entries(languages).map(([code, lang]) => `
                        <div class="iaf-lang-option" onclick="IAFactoryLangSwitcher.setLanguage('${code}')">
                            ${lang.flag} ${lang.name}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Toggle language menu visibility
     * @param {Event} event - Click event
     */
    function toggleMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('langMenu');
        if (menu) {
            menu.classList.toggle('show');
        }
    }

    /**
     * Set the current language
     * @param {string} lang - Language code (fr, en, ar)
     */
    function setLanguage(lang) {
        // Close the menu
        const menu = document.getElementById('langMenu');
        if (menu) {
            menu.classList.remove('show');
        }

        // Update button display
        const langBtn = document.querySelector('.lang-btn');
        if (langBtn && languages[lang]) {
            langBtn.textContent = `${languages[lang].flag} ${languages[lang].code}`;
        }

        // Save to localStorage
        localStorage.setItem('iafactory_lang', lang);

        // Call i18n system if available
        if (typeof IAFactoryI18n !== 'undefined') {
            IAFactoryI18n.setLanguage(lang);
        }
    }

    /**
     * Initialize the language switcher
     * @param {string} containerId - ID of the container element (optional)
     */
    function init(containerId) {
        // Add click outside listener to close menu
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.iaf-lang-switcher')) {
                const menu = document.getElementById('langMenu');
                if (menu) {
                    menu.classList.remove('show');
                }
            }
        });

        // If container ID is provided, inject the switcher
        if (containerId) {
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = createSwitcherHTML();
            }
        }
    }

    // Expose to global scope
    window.IAFactoryLangSwitcher = {
        init: init,
        toggle: toggleMenu,
        setLanguage: setLanguage,
        createHTML: createSwitcherHTML,
        languages: languages
    };

    // Auto-init on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            init();
        });
    } else {
        init();
    }
})();
