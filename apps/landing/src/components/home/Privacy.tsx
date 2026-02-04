import { useTranslation } from '../../i18n';
import './Privacy.css';

const PRIVACY_FEATURES = [
  {
    id: 'compliance',
    icon: (
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="22" fill="#2d2d2d" />
        <circle cx="24" cy="24" r="12" stroke="#ffffff" strokeWidth="2" fill="none" />
        <circle cx="24" cy="24" r="6" stroke="#ffffff" strokeWidth="2" fill="none" />
        <circle cx="24" cy="8" r="2" fill="#ffffff" />
        <circle cx="24" cy="40" r="2" fill="#ffffff" />
        <circle cx="8" cy="24" r="2" fill="#ffffff" />
        <circle cx="40" cy="24" r="2" fill="#ffffff" />
        <circle cx="12" cy="12" r="1.5" fill="#ffffff" />
        <circle cx="36" cy="12" r="1.5" fill="#ffffff" />
        <circle cx="12" cy="36" r="1.5" fill="#ffffff" />
        <circle cx="36" cy="36" r="1.5" fill="#ffffff" />
      </svg>
    ),
    titleKey: 'privacy.p1.title',
    descKey: 'privacy.p1.desc',
  },
  {
    id: 'notraining',
    icon: (
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="22" fill="#2d2d2d" />
        <rect x="16" y="22" width="16" height="12" rx="2" fill="#ffffff" />
        <path
          d="M18 22V18C18 14.6863 20.6863 12 24 12C27.3137 12 30 14.6863 30 18V22"
          stroke="#ffffff"
          strokeWidth="3"
          fill="none"
          strokeLinecap="round"
        />
        <circle cx="24" cy="28" r="2" fill="#2d2d2d" />
      </svg>
    ),
    titleKey: 'privacy.p2.title',
    descKey: 'privacy.p2.desc',
  },
  {
    id: 'datasecurity',
    icon: (
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="22" fill="#2d2d2d" />
        <ellipse cx="24" cy="16" rx="10" ry="4" fill="#ffffff" />
        <path d="M14 16v16c0 2.2 4.5 4 10 4s10-1.8 10-4V16" stroke="#ffffff" strokeWidth="2" fill="none" />
        <ellipse cx="24" cy="24" rx="10" ry="4" stroke="#ffffff" strokeWidth="2" fill="none" />
        <circle cx="34" cy="34" r="8" fill="#10b981" />
        <path d="M30 34l3 3 5-5" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    titleKey: 'privacy.p3.title',
    descKey: 'privacy.p3.desc',
  },
];

export default function Privacy() {
  const { t } = useTranslation();
  return (
    <section className="privacy-section">
      <div className="container">
        <div className="section-title">
          <h2 data-i18n="privacy.title">{t('privacy.title')}</h2>
          <p data-i18n="privacy.subtitle">{t('privacy.subtitle')}</p>
        </div>

        <div className="privacy-grid">
          {PRIVACY_FEATURES.map((feature) => (
            <div key={feature.id} className="privacy-card">
              <div className="privacy-icon">{feature.icon}</div>
              <h3 className="privacy-title" data-i18n={feature.titleKey}>
                {t(feature.titleKey)}
              </h3>
              <p className="privacy-desc" data-i18n={feature.descKey}>
                {t(feature.descKey)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
