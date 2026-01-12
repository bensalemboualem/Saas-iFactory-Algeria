/**
 * IAFactory Algeria Documentation Theme Manager
 * Gère le thème (dark/light) et la langue (fr/en/ar)
 */

class DocsThemeManager {
  constructor() {
    this.currentTheme = this.getStoredTheme() || 'light';
    this.currentLanguage = this.getStoredLanguage() || 'fr';
    this.init();
  }

  init() {
    this.applyTheme(this.currentTheme);
    this.applyLanguage(this.currentLanguage);
    this.setupEventListeners();
    this.updateActiveLinks();
    this.setupTableOfContents();
    this.setupCodeCopyButtons();
    this.setupSearch();
  }

  // Gestion du Thème
  getStoredTheme() {
    return localStorage.getItem('iafactory-docs-theme');
  }

  setStoredTheme(theme) {
    localStorage.setItem('iafactory-docs-theme', theme);
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.currentTheme = theme;
    this.setStoredTheme(theme);
    this.updateThemeToggle();
  }

  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.applyTheme(newTheme);
  }

  updateThemeToggle() {
    const toggleBtn = document.querySelector('.theme-toggle');
    const slider = document.querySelector('.theme-toggle-slider');
    
    if (toggleBtn && slider) {
      slider.textContent = this.currentTheme === 'dark' ? '🌙' : '☀️';
    }
  }

  // Gestion de la Langue
  getStoredLanguage() {
    return localStorage.getItem('iafactory-docs-language');
  }

  setStoredLanguage(language) {
    localStorage.setItem('iafactory-docs-language', language);
  }

  applyLanguage(language) {
    this.currentLanguage = language;
    this.setStoredLanguage(language);
    
    // Mettre à jour l'attribut dir pour RTL (arabe)
    if (language === 'ar') {
      document.documentElement.setAttribute('dir', 'rtl');
    } else {
      document.documentElement.setAttribute('dir', 'ltr');
    }
    
    this.updateLanguageButtons();
    this.loadLanguageContent(language);
  }

  switchLanguage(language) {
    if (language !== this.currentLanguage) {
      this.applyLanguage(language);
      
      // Rediriger vers la bonne page de langue
      const currentPath = window.location.pathname;
      const newPath = currentPath.replace(/\/(fr|en|ar)\//, `/${language}/`);
      
      if (newPath !== currentPath) {
        window.location.href = newPath;
      }
    }
  }

  updateLanguageButtons() {
    const buttons = document.querySelectorAll('.language-switcher button');
    buttons.forEach(btn => {
      const lang = btn.dataset.lang;
      if (lang === this.currentLanguage) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  loadLanguageContent(language) {
    // Charger les traductions dynamiquement si nécessaire
    const translations = {
      fr: {
        search: 'Rechercher...',
        toc: 'Sur cette page',
        copy: 'Copier',
        copied: 'Copié !',
      },
      en: {
        search: 'Search...',
        toc: 'On this page',
        copy: 'Copy',
        copied: 'Copied!',
      },
      ar: {
        search: 'بحث...',
        toc: 'في هذه الصفحة',
        copy: 'نسخ',
        copied: 'تم النسخ!',
      }
    };

    const t = translations[language];
    
    // Mettre à jour les placeholders et textes
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
      searchInput.placeholder = t.search;
    }

    const tocTitle = document.querySelector('.docs-toc-title');
    if (tocTitle) {
      tocTitle.textContent = t.toc;
    }

    // Mettre à jour les boutons de copie
    document.querySelectorAll('.code-copy-btn').forEach(btn => {
      btn.textContent = t.copy;
      btn.dataset.copiedText = t.copied;
    });
  }

  // Event Listeners
  setupEventListeners() {
    // Theme toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    // Language switcher
    const langButtons = document.querySelectorAll('.language-switcher button');
    langButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        this.switchLanguage(lang);
      });
    });

    // Sidebar menu
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    sidebarLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        sidebarLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
      });
    });

    // Mobile menu
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.docs-sidebar');
    
    if (mobileMenuBtn && sidebar) {
      mobileMenuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
      });
    }

    // Fermer le menu mobile au clic sur un lien
    if (sidebar) {
      sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
          }
        });
      });
    }

    // Scroll spy pour TOC
    this.setupScrollSpy();
  }

  // Table of Contents
  setupTableOfContents() {
    const content = document.querySelector('.docs-main');
    const toc = document.querySelector('.docs-toc ul');
    
    if (!content || !toc) return;

    const headings = content.querySelectorAll('h2, h3');
    toc.innerHTML = '';

    headings.forEach((heading, index) => {
      const id = heading.id || `heading-${index}`;
      heading.id = id;

      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${id}`;
      a.textContent = heading.textContent;
      a.dataset.target = id;
      
      if (heading.tagName === 'H3') {
        li.style.paddingLeft = '1rem';
      }

      li.appendChild(a);
      toc.appendChild(li);
    });
  }

  // Scroll Spy
  setupScrollSpy() {
    const tocLinks = document.querySelectorAll('.docs-toc a');
    
    if (tocLinks.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          tocLinks.forEach(link => {
            if (link.dataset.target === id) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }, {
      rootMargin: '-80px 0px -80% 0px'
    });

    document.querySelectorAll('.docs-main h2, .docs-main h3').forEach(heading => {
      observer.observe(heading);
    });

    // Smooth scroll
    tocLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.getElementById(link.dataset.target);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, null, `#${link.dataset.target}`);
        }
      });
    });
  }

  // Code Copy Buttons
  setupCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach((codeBlock) => {
      const pre = codeBlock.parentElement;
      
      // Créer le header
      const header = document.createElement('div');
      header.className = 'code-header';
      
      // Language badge
      const language = codeBlock.className.match(/language-(\w+)/)?.[1] || 'text';
      const langBadge = document.createElement('span');
      langBadge.className = 'code-language';
      langBadge.textContent = language;
      
      // Copy button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'code-copy-btn';
      copyBtn.textContent = this.getTranslation('copy');
      copyBtn.dataset.copiedText = this.getTranslation('copied');
      
      copyBtn.addEventListener('click', () => {
        const code = codeBlock.textContent;
        navigator.clipboard.writeText(code).then(() => {
          const originalText = copyBtn.textContent;
          copyBtn.textContent = copyBtn.dataset.copiedText;
          copyBtn.style.backgroundColor = 'var(--accent-secondary)';
          
          setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
          }, 2000);
        });
      });
      
      header.appendChild(langBadge);
      header.appendChild(copyBtn);
      pre.insertBefore(header, codeBlock);
    });
  }

  // Search
  setupSearch() {
    const searchInput = document.querySelector('.search-box input');
    
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      this.filterSidebarItems(query);
    });
  }

  filterSidebarItems(query) {
    const sidebarItems = document.querySelectorAll('.sidebar-menu li');
    
    sidebarItems.forEach(item => {
      const text = item.textContent.toLowerCase();
      if (text.includes(query)) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });
  }

  // Helpers
  updateActiveLinks() {
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    
    sidebarLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      }
    });
  }

  getTranslation(key) {
    const translations = {
      fr: { copy: 'Copier', copied: 'Copié !' },
      en: { copy: 'Copy', copied: 'Copied!' },
      ar: { copy: 'نسخ', copied: 'تم النسخ!' }
    };
    return translations[this.currentLanguage][key];
  }
}

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
  window.docsThemeManager = new DocsThemeManager();
});

// Détecter les changements de préférence système
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem('iafactory-docs-theme')) {
    window.docsThemeManager.applyTheme(e.matches ? 'dark' : 'light');
  }
});
