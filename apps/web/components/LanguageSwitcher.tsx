'use client';

import { useI18n, Lang } from '@/lib/i18n';

export function LanguageSwitcher() {
  const { lang, setLang } = useI18n();

  const languages: { code: Lang; label: string; flag: string }[] = [
    { code: 'fr', label: 'FR', flag: '🇫🇷' },
    { code: 'ar', label: 'AR', flag: '🇩🇿' },
    { code: 'en', label: 'EN', flag: '🇬🇧' },
  ];

  return (
    <div className="flex items-center gap-1 bg-secondary rounded-lg p-1">
      {languages.map(({ code, label, flag }) => (
        <button
          key={code}
          onClick={() => setLang(code)}
          className={`px-2 py-1 rounded text-sm font-medium transition-all ${
            lang === code
              ? 'bg-primary text-primary-foreground shadow-sm'
              : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
          }`}
          title={label}
        >
          <span className="hidden sm:inline">{flag} </span>
          {label}
        </button>
      ))}
    </div>
  );
}

export default LanguageSwitcher;
