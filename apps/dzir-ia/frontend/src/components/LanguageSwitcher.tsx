import { useState, useRef, useEffect } from 'react';
import { useI18n, availableLangs, Lang } from '../lib/i18n';

export default function LanguageSwitcher() {
  const { lang, setLang, t } = useI18n();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const currentLang = availableLangs.find(l => l.code === lang) || availableLangs[0];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (code: Lang) => {
    setLang(code);
    setIsOpen(false);
  };

  return (
    <div className="lang-switcher" ref={menuRef}>
      <button
        className="lang-btn"
        onClick={() => setIsOpen(!isOpen)}
        title={t('settings.language')}
      >
        <span className="lang-flag">{currentLang.flag}</span>
        <span className="lang-code">{currentLang.code.toUpperCase()}</span>
        <span className="lang-arrow">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="lang-menu">
          {availableLangs.map((l) => (
            <button
              key={l.code}
              className={`lang-option ${l.code === lang ? 'active' : ''}`}
              onClick={() => handleSelect(l.code)}
            >
              <span className="lang-flag">{l.flag}</span>
              <span className="lang-label">{l.label}</span>
            </button>
          ))}
        </div>
      )}

      <style>{`
        .lang-switcher {
          position: relative;
          display: inline-block;
        }

        .lang-btn {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 10px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 8px;
          color: var(--text-primary, #f8fafc);
          cursor: pointer;
          font-size: 13px;
          font-weight: 600;
          transition: all 0.2s ease;
        }

        .lang-btn:hover {
          border-color: rgba(0, 166, 81, 0.45);
          background: rgba(255, 255, 255, 0.1);
        }

        .lang-flag {
          font-size: 16px;
        }

        .lang-code {
          font-weight: 700;
        }

        .lang-arrow {
          font-size: 8px;
          opacity: 0.7;
        }

        .lang-menu {
          position: absolute;
          top: 100%;
          right: 0;
          margin-top: 4px;
          background: var(--bg-secondary, #262626);
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 10px;
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
          min-width: 140px;
          z-index: 1000;
          overflow: hidden;
        }

        [dir="rtl"] .lang-menu {
          right: auto;
          left: 0;
        }

        .lang-option {
          display: flex;
          align-items: center;
          gap: 10px;
          width: 100%;
          padding: 10px 14px;
          background: transparent;
          border: none;
          color: var(--text-primary, #f8fafc);
          cursor: pointer;
          font-size: 14px;
          text-align: left;
          transition: all 0.15s ease;
        }

        [dir="rtl"] .lang-option {
          text-align: right;
        }

        .lang-option:hover {
          background: rgba(0, 166, 81, 0.15);
        }

        .lang-option.active {
          background: rgba(0, 166, 81, 0.2);
          color: #00a651;
        }

        .lang-label {
          font-weight: 500;
        }
      `}</style>
    </div>
  );
}
