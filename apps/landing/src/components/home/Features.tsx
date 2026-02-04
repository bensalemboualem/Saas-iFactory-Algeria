import { useTranslation } from '../../i18n';
import './Features.css';

const FEATURES = [
  {
    id: 'reprompting',
    icon: (
      <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#00A86B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 2L11 13" />
        <path d="M22 2L15 22L11 13L2 9L22 2Z" />
      </svg>
    ),
    titleKey: 'features.f1.title',
    title: 'REPROMPTING EN UN CLIC',
    descKey: 'features.f1.desc',
    desc: "Envoyez rapidement votre prompt à un autre modèle et exploitez la diversité des IA. L'avenir est multi-modèle.",
  },
  {
    id: 'projects',
    icon: (
      <>
        <img src="./assets/images/logodarkiafa.png" alt="IAFactory" className="feature-logo logo-light" />
        <img src="./assets/images/logoclaireiafa.png" alt="IAFactory" className="feature-logo logo-dark" />
      </>
    ),
    titleKey: 'features.f2.title',
    title: 'PROJETS IA FACTORY',
    descKey: 'features.f2.desc',
    desc: 'Configurez votre IA Factory personnalisé avec un contexte adapté pour soutenir vos projets plus efficacement.',
  },
  {
    id: 'uploads',
    icon: (
      <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#00A86B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="17 8 12 3 7 8" />
        <line x1="12" y1="3" x2="12" y2="15" />
      </svg>
    ),
    titleKey: 'features.f3.title',
    title: "TÉLÉCHARGEMENTS D'IMAGES ET DE FICHIERS",
    descKey: 'features.f3.desc',
    desc: "Téléchargez facilement des images et des documents pour extraire des informations grâce à l'analyse IA.",
  },
  {
    id: 'multidevice',
    icon: (
      <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#00A86B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="12" height="9" rx="1" />
        <line x1="8" y1="12" x2="8" y2="14" />
        <line x1="5" y1="14" x2="11" y2="14" />
        <rect x="15" y="5" width="7" height="10" rx="1" />
        <rect x="17" y="16" width="5" height="7" rx="1" />
        <line x1="19.5" y1="21" x2="19.5" y2="21.01" />
      </svg>
    ),
    titleKey: 'features.f4.title',
    title: 'MULTI-APPAREIL',
    descKey: 'features.f4.desc',
    desc: "Installez l'application sur n'importe quel appareil : Android, iPhone et ordinateur de bureau.",
  },
  {
    id: 'websearch',
    icon: (
      <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#00A86B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="2" y1="12" x2="22" y2="12" />
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
        <circle cx="18" cy="18" r="3" fill="none" />
        <line x1="21" y1="21" x2="23" y2="23" />
      </svg>
    ),
    titleKey: 'features.f5.title',
    title: 'RECHERCHE WEB AI',
    descKey: 'features.f5.desc',
    desc: 'Trouvez des réponses bien sourcées à partir de contenus web récents.',
  },
  {
    id: 'voice',
    icon: (
      <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#00A86B" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="23" />
        <line x1="8" y1="23" x2="16" y2="23" />
      </svg>
    ),
    titleKey: 'features.f6.title',
    title: 'CHAT VOCAL',
    descKey: 'features.f6.desc',
    desc: "Ayez des conversations vocales en temps réel avec l'IA.",
  },
];

export default function Features() {
  const { t } = useTranslation();
  return (
    <section className="features-section" id="features">
      <div className="container">
        <div className="section-title">
          <h2 data-i18n="features.title">{t('features.title')}</h2>
          <p data-i18n="features.subtitle">{t('features.subtitle')}</p>
        </div>

        <div className="features-grid">
          {FEATURES.map((feature) => (
            <div key={feature.id} className="feature-card">
              <div className="feature-image">{feature.icon}</div>
              <h3 className="feature-title" data-i18n={feature.titleKey}>
                {t(feature.titleKey)}
              </h3>
              <p className="feature-desc" data-i18n={feature.descKey}>
                {t(feature.descKey)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
