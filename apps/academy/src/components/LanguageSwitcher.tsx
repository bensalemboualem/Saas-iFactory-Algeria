'use client';

import { useI18n, availableLangs } from '@/lib/i18n';

export default function LanguageSwitcher() {
  const { lang, setLang } = useI18n();

  return (
    <select
      value={lang}
      onChange={(e) => setLang(e.target.value as 'fr' | 'ar' | 'en')}
      className="px-3 py-2 rounded-lg border border-border bg-card text-foreground cursor-pointer transition-colors hover:bg-accent focus:outline-none focus:ring-2 focus:ring-primary"
      aria-label="Select language"
    >
      {availableLangs.map((l) => (
        <option key={l.code} value={l.code}>
          {l.flag} {l.label}
        </option>
      ))}
    </select>
  );
}
