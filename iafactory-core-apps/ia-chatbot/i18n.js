// i18n.js - Gestion trilingue (fr/en/ar)
window.i18n = (function() {
  let lang = localStorage.getItem('lang') || 'fr';
  let messages = {};

  function setLang(l) {
    lang = l;
    localStorage.setItem('lang', l);
    document.documentElement.lang = l;
    document.documentElement.dir = l === 'ar' ? 'rtl' : 'ltr';
    loadMessages().then(updateTexts);
  }

  function getLang() {
    return lang;
  }

  async function loadMessages() {
    try {
      const response = await fetch(`./messages/${lang}.json`);
      messages = await response.json();
    } catch (e) {
      console.warn('i18n: Failed to load messages for', lang);
      messages = {};
    }
    return messages;
  }

  function t(key) {
    return messages[key] || key;
  }

  function updateTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const k = el.getAttribute('data-i18n');
      if (messages[k]) el.textContent = messages[k];
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const k = el.getAttribute('data-i18n-html');
      if (messages[k]) el.innerHTML = messages[k];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const k = el.getAttribute('data-i18n-placeholder');
      if (messages[k]) el.setAttribute('placeholder', messages[k]);
    });
    window.dispatchEvent(new CustomEvent('i18n:loaded', { detail: { lang, messages } }));
  }

  function init() {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    return loadMessages().then(updateTexts);
  }

  return { setLang, getLang, t, init, loadMessages };
})();

document.addEventListener('DOMContentLoaded', () => window.i18n.init());
