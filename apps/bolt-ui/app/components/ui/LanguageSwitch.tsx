import { useStore } from '@nanostores/react';
import { memo, useState, useRef, useEffect } from 'react';
import { localeStore, setLocale, localeConfig, locales, type Locale } from '~/lib/i18n';

interface LanguageSwitchProps {
  className?: string;
}

export const LanguageSwitch = memo(({ className }: LanguageSwitchProps) => {
  const locale = useStore(localeStore);
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const currentConfig = localeConfig[locale];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (newLocale: Locale) => {
    setLocale(newLocale);
    setIsOpen(false);
  };

  return (
    <div className={`relative ${className || ''}`} ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 px-2 py-1.5 rounded-md
                   bg-bolt-elements-background-depth-2
                   hover:bg-bolt-elements-background-depth-3
                   border border-bolt-elements-borderColor
                   text-bolt-elements-textPrimary text-sm
                   transition-colors"
        title="Change language"
      >
        <span className="text-base">{currentConfig.flag}</span>
        <span className="font-medium uppercase">{locale}</span>
        <span className={`i-ph:caret-down text-xs transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full right-0 mt-1 min-w-[140px] z-50
                        bg-bolt-elements-background-depth-2
                        border border-bolt-elements-borderColor
                        rounded-lg shadow-lg overflow-hidden">
          {locales.map((l) => (
            <button
              key={l}
              onClick={() => handleSelect(l)}
              className={`w-full flex items-center gap-2 px-3 py-2
                         text-left text-sm transition-colors
                         ${l === locale
                           ? 'bg-bolt-elements-button-primary-background text-bolt-elements-button-primary-text'
                           : 'text-bolt-elements-textPrimary hover:bg-bolt-elements-background-depth-3'
                         }`}
            >
              <span className="text-base">{localeConfig[l].flag}</span>
              <span className="font-medium">{localeConfig[l].label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
});
