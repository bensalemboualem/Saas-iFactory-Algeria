import { useTheme } from '../lib/theme';
import { useI18n } from '../lib/i18n';

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const { t } = useI18n();

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      title={theme === 'dark' ? t('settings.theme.light') : t('settings.theme.dark')}
    >
      <span className="theme-icon">
        {theme === 'dark' ? '☀️' : '🌙'}
      </span>

      <style>{`
        .theme-toggle {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .theme-toggle:hover {
          border-color: rgba(0, 166, 81, 0.45);
          background: rgba(255, 255, 255, 0.1);
        }

        .theme-icon {
          font-size: 18px;
        }

        [data-theme="light"] .theme-toggle {
          background: rgba(0, 0, 0, 0.04);
          border-color: rgba(0, 0, 0, 0.1);
        }

        [data-theme="light"] .theme-toggle:hover {
          background: rgba(0, 0, 0, 0.08);
          border-color: rgba(0, 166, 81, 0.45);
        }
      `}</style>
    </button>
  );
}
