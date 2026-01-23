// ThemeToggle.js - Toggle dark/light theme
(function() {
  function isDark() {
    return localStorage.getItem('theme') !== 'light';
  }

  function applyTheme() {
    if (isDark()) {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    }
  }

  function renderToggle() {
    const el = document.getElementById('theme-toggle');
    if (!el) return;

    const dark = isDark();
    el.innerHTML = `<button onclick="window.toggleTheme()"
      class="px-2 py-1 rounded text-sm transition-colors ${
        dark ? 'bg-slate-800 text-white hover:bg-slate-700' : 'bg-slate-200 text-slate-800 hover:bg-slate-300'
      }">${dark ? '🌙' : '☀️'}</button>`;
  }

  window.toggleTheme = function() {
    const newTheme = isDark() ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    applyTheme();
    renderToggle();
  };

  document.addEventListener('DOMContentLoaded', () => {
    applyTheme();
    renderToggle();
  });
})();
