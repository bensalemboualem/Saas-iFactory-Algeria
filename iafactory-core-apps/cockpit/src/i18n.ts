import fr from './messages/fr.json';
import en from './messages/en.json';
import ar from './messages/ar.json';

export type Lang = 'fr' | 'en' | 'ar';

const resources = { fr, en, ar };

export function getLang(): Lang {
  return (localStorage.getItem('lang') as Lang) || 'fr';
}

export function setLang(lang: Lang) {
  localStorage.setItem('lang', lang);
  window.location.reload();
}

export function t(key: string): string {
  const lang = getLang();
  const dict = resources[lang] as Record<string, unknown>;

  // Support nested keys like "apps.legalAssistant"
  const keys = key.split('.');
  let value: unknown = dict;

  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = (value as Record<string, unknown>)[k];
    } else {
      return key; // Key not found, return original key
    }
  }

  return typeof value === 'string' ? value : key;
}

export const availableLangs: { code: Lang; label: string }[] = [
  { code: 'fr', label: 'FR' },
  { code: 'en', label: 'EN' },
  { code: 'ar', label: 'AR' },
];
