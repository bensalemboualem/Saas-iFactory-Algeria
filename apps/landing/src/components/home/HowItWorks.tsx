import { useTranslation } from '../../i18n';
import { useTheme } from '../../hooks';
import './HowItWorks.css';

const STEPS = [
  {
    number: '1',
    titleKey: 'how_it_works_step1_title',
    descKey: 'how_it_works_step1_desc',
    icon: '💳',
  },
  {
    number: '2',
    titleKey: 'how_it_works_step2_title',
    descKey: 'how_it_works_step2_desc',
    icon: '🤖',
  },
  {
    number: '3',
    titleKey: 'how_it_works_step3_title',
    descKey: 'how_it_works_step3_desc',
    icon: '✨',
  },
];

export default function HowItWorks() {
  const { t } = useTranslation();
  const { colors, isDark } = useTheme();

  return (
    <section className="how-it-works-section" id="how-it-works">
      <div className="container">
        <div className="section-title">
          <h2>{t('how_it_works_title')}</h2>
          <p style={{ color: colors.textMuted }}>
            {t('how_it_works_subtitle')}
          </p>
        </div>

        <div className="steps-grid">
          {STEPS.map((step) => (
            <div
              key={step.number}
              className="step-card"
              style={{
                background: isDark ? colors.bgSecondary : '#ffffff',
                border: `1px solid ${colors.borderColor}`,
              }}
            >
              <div className="step-number">{step.number}</div>
              <div className="step-icon">{step.icon}</div>
              <h3 className="step-title" style={{ color: colors.textPrimary }}>
                {t(step.titleKey)}
              </h3>
              <p className="step-description" style={{ color: colors.textMuted }}>
                {t(step.descKey)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
