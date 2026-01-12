// ========================================
// LANGUAGE SWITCHER + RTL FIX
// ========================================

document.addEventListener('DOMContentLoaded', function() {
  const html = document.documentElement;
  
  // Get saved language or default to French
  const savedLang = localStorage.getItem('language') || 'fr';
  const savedTheme = localStorage.getItem('theme') || 'dark';
  
  // Set initial language and direction
  setLanguage(savedLang);
  html.setAttribute('data-theme', savedTheme);
  
  // Create language selector if not exists
  createLanguageSwitcher();
  
  function setLanguage(lang) {
    html.setAttribute('lang', lang);
    html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    localStorage.setItem('language', lang);
    
    // Update all text content
    updateContent(lang);
  }
  
  function createLanguageSwitcher() {
    // Check if switcher already exists
    if (document.getElementById('langSwitcher')) return;
    
    // Find navigation
    const nav = document.querySelector('.nav-right') || document.querySelector('nav');
    if (!nav) return;
    
    // Create switcher HTML
    const switcher = document.createElement('select');
    switcher.id = 'langSwitcher';
    switcher.className = 'lang-switcher';
    switcher.innerHTML = `
      <option value="fr">Français</option>
      <option value="ar">العربية</option>
      <option value="en">English</option>
    `;
    switcher.value = localStorage.getItem('language') || 'fr';
    
    // Add change event
    switcher.addEventListener('change', function(e) {
      setLanguage(e.target.value);
    });
    
    // Add to nav
    nav.insertBefore(switcher, nav.firstChild);
  }
  
  function updateContent(lang) {
    const translations = {
      fr: {
        title: "IA Factory Algeria - L'IA mondiale, payée en Dinars",
        description: "Accédez à Claude, GPT, Gemini, Mistral, Grok, DeepSeek et plus encore"
      },
      ar: {
        title: "IA Factory الجزائر - الذكاء الاصطناعي العالمي، الدفع بالدينار",
        description: "الوصول إلى Claude و GPT و Gemini و Mistral و Grok و DeepSeek والمزيد"
      },
      en: {
        title: "IA Factory Algeria - Global AI, paid in Dinars",
        description: "Access Claude, GPT, Gemini, Mistral, Grok, DeepSeek and more"
      }
    };
    
    // Update meta tags
    document.title = translations[lang].title;
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.content = translations[lang].description;
  }
});

// Theme toggle
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}
