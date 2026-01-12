/* ============================================
   IAFactory Algeria - Theme Manager
   Gestion du thème dark/light pour toutes les apps
   ============================================ */

(function() {
    // Initialize theme on load
    function initTheme() {
        const savedTheme = localStorage.getItem('iafactory-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    // Toggle theme
    window.toggleTheme = function() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('iafactory-theme', newTheme);
        updateThemeIcon(newTheme);
    }

    // Update theme icon
    function updateThemeIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '🌙' : '☀️';
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }
})();
