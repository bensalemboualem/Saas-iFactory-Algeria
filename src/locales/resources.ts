import { DEFAULT_LANG } from '@/const/locale';

import resources from './default';

// IAFactory Algeria - Langues supportées 🇩🇿
export const locales = [
  'fr-FR', // Français (principal)
  'ar', // Arabe
  'en-US', // Anglais (international)
] as const;

export type DefaultResources = typeof resources;
export type NS = keyof DefaultResources;
export type Locales = (typeof locales)[number];

export const normalizeLocale = (locale?: string): Locales => {
  if (!locale) return DEFAULT_LANG;

  // Arabe
  if (locale.startsWith('ar')) return 'ar';

  // Français
  if (locale.startsWith('fr')) return 'fr-FR';

  // Anglais
  if (locale.startsWith('en')) return 'en-US';

  for (const l of locales) {
    if (l.startsWith(locale)) {
      return l;
    }
  }

  return DEFAULT_LANG;
};

type LocaleOptions = {
  label: string;
  value: Locales;
}[];

// IAFactory Algeria - Options de langues
export const localeOptions: LocaleOptions = [
  {
    label: 'Français',
    value: 'fr-FR',
  },
  {
    label: 'العربية',
    value: 'ar',
  },
  {
    label: 'English',
    value: 'en-US',
  },
] as LocaleOptions;

export const supportLocales: string[] = [...locales, 'en', 'fr'];
