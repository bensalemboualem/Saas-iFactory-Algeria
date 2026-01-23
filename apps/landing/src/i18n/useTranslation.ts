import { useState, useEffect, useCallback } from 'react';
import { translations, Language, Translation } from './translations';

export function useTranslation() {
  const [lang, setLang] = useState<Language>(() => {
    const saved = localStorage.getItem('lang') as Language;
    return saved && ['fr', 'ar', 'en'].includes(saved) ? saved : 'fr';
  });

  useEffect(() => {
    // Observer les changements de langue depuis le Header
    const handleLangChange = () => {
      const currentLang = localStorage.getItem('lang') as Language;
      if (currentLang && currentLang !== lang) {
        setLang(currentLang);
      }
    };

    // Écouter les changements de localStorage
    window.addEventListener('storage', handleLangChange);

    // Écouter un événement custom pour les changements dans la même fenêtre
    window.addEventListener('languageChanged', handleLangChange as EventListener);

    return () => {
      window.removeEventListener('storage', handleLangChange);
      window.removeEventListener('languageChanged', handleLangChange as EventListener);
    };
  }, [lang]);

  const t = useCallback((key: string): string => {
    const translation = translations[key] as Translation | undefined;
    if (!translation) {
      console.warn(`Translation not found for key: ${key}`);
      return key;
    }
    return translation[lang] || translation['fr'] || key;
  }, [lang]);

  const changeLanguage = useCallback((newLang: Language) => {
    setLang(newLang);
    localStorage.setItem('lang', newLang);
    document.documentElement.lang = newLang;
    document.documentElement.dir = newLang === 'ar' ? 'rtl' : 'ltr';
    // Dispatch custom event pour notifier les autres composants
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: newLang } }));
  }, []);

  return { t, lang, changeLanguage };
}
