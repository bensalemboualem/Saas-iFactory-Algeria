import { useEffect, useState } from 'react';
import { useTranslation } from '../i18n';

type Theme = 'dark' | 'light';

export default function B2B() {
  const { t } = useTranslation();
  const [theme, setTheme] = useState<Theme>('dark');

  const features = [
    { icon: '🏢', title: t('b2b_custom_solutions'), description: t('b2b_custom_solutions_desc') },
    { icon: '🔒', title: t('b2b_security'), description: t('b2b_security_desc') },
    { icon: '📊', title: t('b2b_analytics'), description: t('b2b_analytics_desc') },
    { icon: '🤝', title: t('b2b_support'), description: t('b2b_support_desc') },
    { icon: '🔌', title: t('b2b_api'), description: t('b2b_api_desc') },
    { icon: '💰', title: t('b2b_billing'), description: t('b2b_billing_desc') },
  ];

  const sectors = [
    { icon: '🏦', name: t('sector_banking') },
    { icon: '📡', name: t('sector_telecom') },
    { icon: '🏛️', name: t('sector_government') },
    { icon: '🎓', name: t('sector_education') },
    { icon: '🏥', name: t('sector_health') },
    { icon: '🏭', name: t('sector_industry') },
    { icon: '🛒', name: t('sector_commerce') },
    { icon: '💼', name: t('sector_services') },
  ];

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
        {/* Hero */}
        <div style={{ textAlign: 'center', marginBottom: '80px' }}>
          <h1
            style={{
              fontSize: 'clamp(32px, 5vw, 48px)',
              fontWeight: 700,
              color: textColor,
              marginBottom: '24px',
            }}
          >
            {t('b2b_title')}
          </h1>
          <p
            style={{
              fontSize: 'clamp(16px, 3vw, 20px)',
              color: textMuted,
              maxWidth: '700px',
              margin: '0 auto 32px',
            }}
          >
            {t('b2b_subtitle')}
          </p>
          <button
            type="button"
            style={{
              padding: 'clamp(12px, 2vw, 16px) clamp(24px, 4vw, 32px)',
              background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
              color: '#fff',
              fontSize: 'clamp(16px, 2.5vw, 18px)',
              fontWeight: 600,
              border: 'none',
              borderRadius: '12px',
              cursor: 'pointer',
              boxShadow: '0 4px 16px rgba(0, 168, 107, 0.3)',
            }}
          >
            {t('b2b_request_demo')}
          </button>
        </div>

        {/* Features Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '24px',
            marginBottom: '80px',
          }}
        >
          {features.map((feature, idx) => (
            <div
              key={idx}
              style={{
                background: cardBg,
                borderRadius: '16px',
                padding: '28px',
                border: `1px solid ${borderColor}`,
              }}
            >
              <div
                style={{
                  fontSize: 'clamp(32px, 5vw, 40px)',
                  marginBottom: '16px',
                }}
              >
                {feature.icon}
              </div>
              <h3
                style={{
                  fontSize: 'clamp(18px, 3vw, 20px)',
                  fontWeight: 600,
                  color: textColor,
                  marginBottom: '8px',
                }}
              >
                {feature.title}
              </h3>
              <p style={{ color: textMuted, fontSize: '15px', lineHeight: 1.6 }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Sectors */}
        <div style={{ textAlign: 'center', marginBottom: '80px' }}>
          <h2
            style={{
              fontSize: 'clamp(24px, 4vw, 32px)',
              fontWeight: 600,
              color: textColor,
              marginBottom: '32px',
            }}
          >
            {t('b2b_sectors_title')}
          </h2>
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              gap: '12px',
            }}
          >
            {sectors.map((sector) => (
              <span
                key={sector.name}
                style={{
                  background: cardBg,
                  padding: '12px 24px',
                  borderRadius: '30px',
                  color: textColor,
                  fontSize: '15px',
                  border: `1px solid ${borderColor}`,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <span>{sector.icon}</span>
                {sector.name}
              </span>
            ))}
          </div>
        </div>

        {/* Contact CTA */}
        <div
          style={{
            background: cardBg,
            borderRadius: '20px',
            padding: 'clamp(24px, 5vw, 48px)',
            textAlign: 'center',
            border: `1px solid ${borderColor}`,
          }}
        >
          <h2
            style={{
              fontSize: 'clamp(22px, 4vw, 28px)',
              fontWeight: 600,
              color: textColor,
              marginBottom: '16px',
            }}
          >
            {t('b2b_ready_to_start')}
          </h2>
          <p
            style={{
              color: textMuted,
              fontSize: 'clamp(14px, 2.5vw, 16px)',
              marginBottom: '24px',
            }}
          >
            {t('b2b_contact_team')}
          </p>
          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <a
              href="mailto:contact@iafactory.dz"
              style={{
                padding: '14px 28px',
                background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
                color: '#fff',
                fontSize: '16px',
                fontWeight: 600,
                textDecoration: 'none',
                borderRadius: '10px',
              }}
            >
              contact@iafactory.dz
            </a>
            <a
              href="tel:+213555000000"
              style={{
                padding: '14px 28px',
                background: 'transparent',
                color: textColor,
                fontSize: '16px',
                fontWeight: 600,
                textDecoration: 'none',
                borderRadius: '10px',
                border: `1px solid ${borderColor}`,
              }}
            >
              +213 555 00 00 00
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
