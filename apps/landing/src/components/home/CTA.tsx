import { Link } from 'react-router-dom';
import { useTranslation } from '../../i18n';
import './CTA.css';

const MOCKUP_MODELS = [
  { emoji: '', name: 'Mistral' },
  { emoji: '', name: 'GPT' },
  { emoji: '', name: 'Claude' },
  { emoji: '', name: 'Grok' },
  { emoji: '', name: 'Gemini' },
];

const MOCKUP_IMAGE_MODELS = [
  { emoji: '', name: 'FLUX' },
  { emoji: '', name: 'GPT Image' },
  { emoji: '', name: 'Recraft' },
];

export default function CTA() {
  const { t } = useTranslation();
  return (
    <section className="cta-section">
      <div className="container">
        <div className="cta-wrapper">
          <div className="cta-content">
            <div className="logo-big">
              <img
                src="./assets/images/logo-header-light.png"
                className="cta-logo-img logo-light"
                alt="IAFactory"
              />
              <img
                src="./assets/images/logo-header-dark.png"
                className="cta-logo-img logo-dark"
                alt="IAFactory"
              />
            </div>
            <h3 data-i18n="cta.text">{t('cta_text')}</h3>
            <div className="cta-buttons">
              <Link to="/chat" className="btn-secondary" data-i18n="cta.signup">
                {t('cta_signup')}
              </Link>
              <Link to="/pricing" className="btn-secondary" data-i18n="cta.plans">
                {t('cta_plans')}
              </Link>
            </div>
          </div>
          <div className="cta-mockup">
            <div className="mockup-header">
              <img
                src="./assets/images/logo-header-light.png"
                className="mockup-logo-img logo-light"
                alt="IAFactory"
              />
              <img
                src="./assets/images/logo-header-dark.png"
                className="mockup-logo-img logo-dark"
                alt="IAFactory"
              />
            </div>
            <div className="mockup-input">{t('cta_mockup_input')}</div>
            <div className="mockup-models">
              {MOCKUP_MODELS.map((model) => (
                <span key={model.name} className="mockup-model">
                  {model.emoji} {model.name}
                </span>
              ))}
            </div>
            <div className="mockup-models" style={{ marginTop: 8 }}>
              {MOCKUP_IMAGE_MODELS.map((model) => (
                <span key={model.name} className="mockup-model">
                  {model.emoji} {model.name}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
