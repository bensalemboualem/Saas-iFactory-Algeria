// LangToggle.js - Sélecteur de langue trilingue
(function() {
  function renderLangToggle() {
    const el = document.getElementById('lang-toggle');
    if (!el || !window.i18n) return;

    const lang = window.i18n.getLang();
    const langs = [
      { code: 'fr', label: 'FR' },
      { code: 'en', label: 'EN' },
      { code: 'ar', label: 'ع' }
    ];

    el.innerHTML = `<div class="flex gap-2">${langs.map(l =>
      `<button onclick="window.i18n.setLang('${l.code}')"
        class="px-2 py-1 rounded text-sm font-medium transition-colors ${
          lang === l.code
            ? 'bg-violet-500 text-white'
            : 'bg-slate-700 text-slate-200 hover:bg-slate-600'
        }">${l.label}</button>`
    ).join('')}</div>`;
  }

  document.addEventListener('DOMContentLoaded', renderLangToggle);
  window.addEventListener('i18n:loaded', renderLangToggle);
})();
