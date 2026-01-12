/**
 * IAFACTORY DESIGN SYSTEM - THEME TOGGLE UTILITY
 * Version: 3.0 - Décembre 2025
 *
 * Usage:
 * 1. Include this script in your HTML: <script src="shared/theme-toggle.js"></script>
 * 2. Add toggle button: <button onclick="IAFTheme.toggle()">Toggle Theme</button>
 * 3. Or use programmatically: IAFTheme.setTheme('dark') / IAFTheme.setTheme('light')
 */

const IAFTheme = {
  // Storage key for persistence
  STORAGE_KEY: 'iafactory_theme',

  // Get current theme
  getTheme() {
    // Check localStorage first
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) return stored;

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light';
    }

    // Default to dark
    return 'dark';
  },

  // Set theme
  setTheme(theme) {
    const validTheme = theme === 'light' ? 'light' : 'dark';

    // Update document attributes
    document.documentElement.setAttribute('data-theme', validTheme);
    document.documentElement.classList.remove('dark', 'light');
    document.documentElement.classList.add(validTheme);

    // Update body class for legacy support
    document.body.classList.remove('dark', 'light');
    document.body.classList.add(validTheme);

    // Save to localStorage
    localStorage.setItem(this.STORAGE_KEY, validTheme);

    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme: validTheme }
    }));

    // Update any theme toggle buttons
    this.updateToggleButtons(validTheme);

    return validTheme;
  },

  // Toggle between themes
  toggle() {
    const current = this.getTheme();
    const newTheme = current === 'dark' ? 'light' : 'dark';
    return this.setTheme(newTheme);
  },

  // Update toggle button states
  updateToggleButtons(theme) {
    // Update data-theme-current attribute on toggle buttons
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.setAttribute('data-theme-current', theme);

      // Update icon if present
      const sunIcon = btn.querySelector('.theme-icon-sun, [data-icon="sun"]');
      const moonIcon = btn.querySelector('.theme-icon-moon, [data-icon="moon"]');

      if (sunIcon && moonIcon) {
        if (theme === 'dark') {
          sunIcon.style.display = 'none';
          moonIcon.style.display = 'block';
        } else {
          sunIcon.style.display = 'block';
          moonIcon.style.display = 'none';
        }
      }
    });
  },

  // Initialize theme on page load
  init() {
    // Apply saved theme immediately (before DOMContentLoaded to prevent flash)
    const theme = this.getTheme();
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.classList.add(theme);

    // Listen for system theme changes
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Only auto-switch if user hasn't manually set a preference
        if (!localStorage.getItem(this.STORAGE_KEY)) {
          this.setTheme(e.matches ? 'dark' : 'light');
        }
      });
    }

    // When DOM is ready, update UI elements
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.setTheme(theme); // Reapply to update all elements
      });
    } else {
      this.setTheme(theme);
    }
  },

  // Check if dark mode
  isDark() {
    return this.getTheme() === 'dark';
  },

  // Check if light mode
  isLight() {
    return this.getTheme() === 'light';
  },
};

// Auto-initialize
IAFTheme.init();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = IAFTheme;
}

// Also make available globally
window.IAFTheme = IAFTheme;
