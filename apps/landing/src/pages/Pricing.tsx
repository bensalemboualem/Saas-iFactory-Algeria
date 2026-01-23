import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

type Theme = 'dark' | 'light';

const PLANS = [
  {
    id: 'dz_starter',
    name: 'Starter',
    price: 0,
    credits: 100,
    features: [
      '100 crédits/mois',
      'Accès aux modèles essentiels',
      'Génération texte & image basique',
      'Support communautaire',
    ],
    cta: 'Commencer gratuitement',
    ctaLink: '/login',
    popular: false,
  },
  {
    id: 'dz_pro',
    name: 'Pro',
    price: 1990,
    credits: 1000,
    features: [
      '1 000 crédits/mois',
      'Accès à tous les modèles IA',
      'Texte, Image, Audio, Code & Vidéo',
      'Support prioritaire',
      'Accès API',
      'Gestion des crédits en temps réel',
    ],
    cta: 'Choisir Pro',
    ctaLink: '/login?plan=pro',
    popular: true,
  },
  {
    id: 'dz_business',
    name: 'Business',
    price: 5990,
    credits: 5000,
    features: [
      '5 000 crédits/mois',
      'Accès aux modèles premium',
      'Agents IA personnalisés',
      'Accès API étendu',
      'Support dédié (SLA)',
      'Facturation entreprise',
    ],
    cta: 'Contacter ventes',
    ctaLink: '/contact',
    popular: false,
  },
];

const CREDIT_EXAMPLES = [
  { category: 'Texte', usage: '~1 crédit / réponse courte', icon: '💬' },
  { category: 'Image', usage: '~10–20 crédits / image', icon: '🖼️' },
  { category: 'Vidéo', usage: '~100–300 crédits / génération', icon: '🎬' },
  { category: 'Audio', usage: '~5–15 crédits / action', icon: '🎵' },
  { category: 'Code', usage: '~1–5 crédits / requête', icon: '💻' },
];

export default function Pricing() {
  const [theme, setTheme] = useState<Theme>('dark');

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setTheme(savedTheme);

    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.dataset.theme as Theme;
      if (currentTheme) setTheme(currentTheme);
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => observer.disconnect();
  }, []);

  const isDark = theme === 'dark';
  const bgColor = isDark ? '#1a1a1a' : '#FAF9F7';
  const cardBg = isDark ? '#262626' : '#ffffff';
  const textColor = isDark ? '#f0f0f0' : '#1F1F1F';
  const textMuted = isDark ? '#A3A3A3' : '#5D5D5D';
  const borderColor = isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)';
  const sectionBg = isDark ? '#1f1f1f' : '#f5f5f0';

  return (
    <div
      style={{
        paddingTop: '120px',
        paddingBottom: '80px',
        minHeight: '100vh',
        background: bgColor,
      }}
    >
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 48px)',
              fontWeight: 700,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            Tarifs simples & transparents
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto',
              lineHeight: 1.6,
            }}
          >
            Tous les plans fonctionnent avec un système de crédits mensuels utilisables sur l'ensemble des modèles IA.
          </p>
        </div>

        {/* Plans Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '24px',
            marginBottom: '80px',
          }}
        >
          {PLANS.map((plan) => (
            <div
              key={plan.id}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '32px',
                border: plan.popular
                  ? '2px solid #00A86B'
                  : `1px solid ${borderColor}`,
                position: 'relative',
                boxShadow: plan.popular
                  ? '0 8px 32px rgba(0, 168, 107, 0.2)'
                  : 'none',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              {plan.popular && (
                <div
                  style={{
                    position: 'absolute',
                    top: '-12px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
                    color: '#fff',
                    padding: '4px 16px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 600,
                    whiteSpace: 'nowrap',
                  }}
                >
                  Plus populaire
                </div>
              )}

              <h3
                style={{
                  fontSize: '24px',
                  fontWeight: 600,
                  color: textColor,
                  marginBottom: '8px',
                }}
              >
                {plan.name}
              </h3>

              <div style={{ marginBottom: '8px' }}>
                <span
                  style={{
                    fontSize: '48px',
                    fontWeight: 700,
                    color: textColor,
                  }}
                >
                  {plan.price.toLocaleString()}
                </span>
                <span style={{ color: textMuted, fontSize: '16px' }}>
                  {' '}DZD/mois
                </span>
              </div>

              <div
                style={{
                  background: 'rgba(0, 168, 107, 0.1)',
                  color: '#00A86B',
                  padding: '8px 16px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 600,
                  marginBottom: '24px',
                  display: 'inline-block',
                  alignSelf: 'flex-start',
                }}
              >
                {plan.credits.toLocaleString()} crédits/mois
              </div>

              <ul
                style={{
                  listStyle: 'none',
                  padding: 0,
                  margin: '0 0 32px 0',
                  flex: 1,
                }}
              >
                {plan.features.map((feature, idx) => (
                  <li
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      color: textMuted,
                      fontSize: '15px',
                      marginBottom: '12px',
                      lineHeight: 1.4,
                    }}
                  >
                    <span style={{ color: '#00A86B', flexShrink: 0 }}>✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <Link
                to={plan.ctaLink}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '14px',
                  borderRadius: '10px',
                  border: plan.popular ? 'none' : `1px solid ${borderColor}`,
                  background: plan.popular
                    ? 'linear-gradient(135deg, #00A86B, #2ECC71)'
                    : 'transparent',
                  color: plan.popular ? '#fff' : textColor,
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  textAlign: 'center',
                  textDecoration: 'none',
                  transition: 'all 0.2s ease',
                }}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>

        {/* Credit Examples Section */}
        <div
          style={{
            background: sectionBg,
            borderRadius: '16px',
            padding: '48px 32px',
            marginBottom: '48px',
          }}
        >
          <h2
            style={{
              fontSize: '28px',
              fontWeight: 700,
              color: textColor,
              textAlign: 'center',
              marginBottom: '12px',
            }}
          >
            Exemples de consommation de crédits
          </h2>
          <p
            style={{
              color: textMuted,
              textAlign: 'center',
              marginBottom: '32px',
              fontSize: '15px',
            }}
          >
            Estimations indicatives pour chaque type de génération
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '16px',
            }}
          >
            {CREDIT_EXAMPLES.map((example) => (
              <div
                key={example.category}
                style={{
                  background: cardBg,
                  borderRadius: '12px',
                  padding: '20px',
                  textAlign: 'center',
                  border: `1px solid ${borderColor}`,
                }}
              >
                <div style={{ fontSize: '32px', marginBottom: '12px' }}>
                  {example.icon}
                </div>
                <div
                  style={{
                    fontSize: '16px',
                    fontWeight: 600,
                    color: textColor,
                    marginBottom: '4px',
                  }}
                >
                  {example.category}
                </div>
                <div
                  style={{
                    fontSize: '13px',
                    color: '#00A86B',
                    fontWeight: 500,
                  }}
                >
                  {example.usage}
                </div>
              </div>
            ))}
          </div>

          <p
            style={{
              color: textMuted,
              textAlign: 'center',
              marginTop: '24px',
              fontSize: '13px',
              fontStyle: 'italic',
            }}
          >
            Les valeurs peuvent évoluer selon la charge et la version des modèles.
          </p>
        </div>

        {/* Payment Methods */}
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <p style={{ color: textMuted, marginBottom: '16px', fontSize: '15px' }}>
            Moyens de paiement acceptés
          </p>
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '16px',
              flexWrap: 'wrap',
            }}
          >
            {['Chargily', 'CIB', 'BaridiMob', 'Dahabia'].map((method) => (
              <span
                key={method}
                style={{
                  background: cardBg,
                  padding: '10px 24px',
                  borderRadius: '8px',
                  color: textColor,
                  fontSize: '14px',
                  fontWeight: 500,
                  border: `1px solid ${borderColor}`,
                }}
              >
                {method}
              </span>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div
          style={{
            background: sectionBg,
            borderRadius: '12px',
            padding: '24px',
            textAlign: 'center',
          }}
        >
          <p
            style={{
              color: textMuted,
              fontSize: '13px',
              lineHeight: 1.6,
              margin: 0,
            }}
          >
            Les modèles et services tiers sont accessibles via notre plateforme d'orchestration IA.
            L'accès dépend de la disponibilité et des quotas des fournisseurs.
          </p>
        </div>
      </div>
    </div>
  );
}
