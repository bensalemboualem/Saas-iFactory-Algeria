/**
 * IAFactory i18n System
 * Support: FR (LTR), AR (RTL), EN (LTR)
 */

import fr from './fr.json';
import ar from './ar.json';
import en from './en.json';

export type Locale = 'fr' | 'ar' | 'en';
export type Direction = 'ltr' | 'rtl';

// Translation dictionaries
const translations: Record<Locale, typeof fr> = { fr, ar, en };

// Language configuration
export const LOCALES: Record<Locale, { name: string; nativeName: string; dir: Direction }> = {
  fr: { name: 'French', nativeName: 'Français', dir: 'ltr' },
  ar: { name: 'Arabic', nativeName: 'العربية', dir: 'rtl' },
  en: { name: 'English', nativeName: 'English', dir: 'ltr' },
};

// Current locale state
let currentLocale: Locale = 'fr';

/**
 * Get current locale
 */
export function getLocale(): Locale {
  return currentLocale;
}

/**
 * Set locale and update document direction
 */
export function setLocale(locale: Locale): void {
  currentLocale = locale;

  // Update document direction for RTL support
  document.documentElement.dir = LOCALES[locale].dir;
  document.documentElement.lang = locale;

  // Store preference
  localStorage.setItem('iaf_locale', locale);

  // Dispatch event for components to react
  window.dispatchEvent(new CustomEvent('localechange', { detail: { locale } }));
}

/**
 * Get direction for current locale
 */
export function getDirection(): Direction {
  return LOCALES[currentLocale].dir;
}

/**
 * Check if current locale is RTL
 */
export function isRTL(): boolean {
  return LOCALES[currentLocale].dir === 'rtl';
}

/**
 * Translate a key with optional interpolation
 * Usage: t('dashboard.welcome') or t('common.error', { code: 404 })
 */
export function t(key: string, params?: Record<string, string | number>): string {
  const keys = key.split('.');
  let value: unknown = translations[currentLocale];

  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = (value as Record<string, unknown>)[k];
    } else {
      // Fallback to French if key not found
      value = translations.fr;
      for (const fk of keys) {
        if (value && typeof value === 'object' && fk in value) {
          value = (value as Record<string, unknown>)[fk];
        } else {
          return key; // Return key if not found
        }
      }
    }
  }

  let result = String(value);

  // Interpolate params
  if (params) {
    Object.entries(params).forEach(([paramKey, paramValue]) => {
      result = result.replace(`{${paramKey}}`, String(paramValue));
    });
  }

  return result;
}

/**
 * Initialize i18n from stored preference or browser
 */
export function initI18n(): Locale {
  // Check stored preference
  const stored = localStorage.getItem('iaf_locale') as Locale | null;
  if (stored && stored in LOCALES) {
    setLocale(stored);
    return stored;
  }

  // Auto-detect from browser
  const browserLang = navigator.language.split('-')[0] as Locale;
  if (browserLang in LOCALES) {
    setLocale(browserLang);
    return browserLang;
  }

  // Default to French
  setLocale('fr');
  return 'fr';
}

/**
 * React hook for i18n (if using React)
 */
export function useI18n() {
  return {
    locale: currentLocale,
    direction: getDirection(),
    isRTL: isRTL(),
    t,
    setLocale,
  };
}

// RTL-aware CSS class helper
export function rtlClass(ltrClass: string, rtlClass: string): string {
  return isRTL() ? rtlClass : ltrClass;
}

// Export translations for direct access
export { translations };
