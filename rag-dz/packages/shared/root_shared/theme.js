/**
 * IAFactory Algeria - Theme Manager
 * Gestion unifiée du dark/light mode pour toutes les apps
 */

class ThemeManager {
  constructor() {
    this.body = document.body;
    this.themeBtn = null;
    this.currentTheme = this.getSavedTheme();

    this.init();
  }

  init() {
    // Apply saved theme
    this.applyTheme(this.currentTheme);

    // Setup theme toggle button if exists
    this.setupToggleButton();

    // Listen for system preference changes
    this.listenToSystemPreference();
  }

  getSavedTheme() {
    // Check localStorage first
    const saved = localStorage.getItem('theme');
    if (saved) return saved;

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light';
    }

    return 'dark'; // Default to dark
  }

  applyTheme(theme) {
    if (theme === 'light') {
      this.body.classList.add('light-theme');
    } else {
      this.body.classList.remove('light-theme');
    }

    this.currentTheme = theme;
    localStorage.setItem('theme', theme);

    // Update button if exists
    this.updateToggleButton();

    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
  }

  toggleTheme() {
    const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(newTheme);
  }

  setupToggleButton() {
    this.themeBtn = document.querySelector('.btn-theme') ||
                    document.querySelector('[data-theme-toggle]') ||
                    document.getElementById('theme-toggle');

    if (this.themeBtn) {
      this.themeBtn.addEventListener('click', () => this.toggleTheme());
      this.updateToggleButton();
    }
  }

  updateToggleButton() {
    if (!this.themeBtn) return;

    const isLight = this.currentTheme === 'light';
    this.themeBtn.textContent = isLight ? '☀️' : '🌙';
    this.themeBtn.setAttribute('aria-label',
      isLight ? 'Passer en thème sombre' : 'Passer en thème clair'
    );
  }

  listenToSystemPreference() {
    if (!window.matchMedia) return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: light)');
    mediaQuery.addEventListener('change', (e) => {
      // Only apply if user hasn't manually set a preference
      if (!localStorage.getItem('theme')) {
        this.applyTheme(e.matches ? 'light' : 'dark');
      }
    });
  }

  // Public API
  getTheme() {
    return this.currentTheme;
  }

  setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark') {
      console.error('Invalid theme. Use "light" or "dark"');
      return;
    }
    this.applyTheme(theme);
  }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeManager;
}
