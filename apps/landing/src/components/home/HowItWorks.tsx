import { useTheme } from '../../hooks';
import './HowItWorks.css';

const STEPS = [
  {
    number: '1',
    title: 'Abonnez-vous',
    description: 'Choisissez votre forfait et recevez vos crédits mensuels',
    icon: '💳',
  },
  {
    number: '2',
    title: 'Choisissez votre IA',
    description: 'Accédez à +30 modèles : texte, image, vidéo, audio, code',
    icon: '🤖',
  },
  {
    number: '3',
    title: 'Utilisez vos crédits',
    description: 'Chaque utilisation consomme des crédits selon le modèle',
    icon: '✨',
  },
];

export default function HowItWorks() {
  const { colors, isDark } = useTheme();

  return (
    <section className="how-it-works-section" id="how-it-works">
      <div className="container">
        <div className="section-title">
          <h2>Comment ça marche ?</h2>
          <p style={{ color: colors.textMuted }}>
            Un système simple et transparent basé sur les crédits
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
                {step.title}
              </h3>
              <p className="step-description" style={{ color: colors.textMuted }}>
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
