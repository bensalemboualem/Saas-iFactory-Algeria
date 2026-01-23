import { useTheme } from '../../hooks';

export default function About() {
  const { colors, accent } = useTheme();

  const sectionStyle = {
    marginBottom: '48px',
  };

  const h2Style = {
    color: colors.textPrimary,
    fontSize: '28px',
    fontWeight: 600,
    marginBottom: '20px',
  };

  const pStyle = {
    color: colors.textSecondary,
    fontSize: '17px',
    lineHeight: 1.9,
    marginBottom: '16px',
  };

  const cardStyle = {
    background: colors.bgSecondary,
    borderRadius: '16px',
    padding: '32px',
    marginBottom: '24px',
    border: `1px solid ${colors.borderColor}`,
  };

  const valueCardStyle = {
    background: colors.bgSecondary,
    borderRadius: '12px',
    padding: '24px',
    textAlign: 'center' as const,
    border: `1px solid ${colors.borderColor}`,
  };

  return (
    <main
      style={{
        minHeight: '100vh',
        background: colors.bgPrimary,
        padding: '120px 24px 60px',
      }}
    >
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Hero */}
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h1
            style={{
              color: colors.textPrimary,
              fontSize: '48px',
              fontWeight: 700,
              marginBottom: '16px',
            }}
          >
            À propos d'<span style={{ color: accent.primary }}>IAFACTORY</span>
          </h1>
          <p style={{ color: colors.textMuted, fontSize: '20px', maxWidth: '600px', margin: '0 auto' }}>
            Plateforme d'Intelligence Artificielle souveraine pour l'Algérie et l'Afrique du Nord
          </p>
        </div>

        {/* Mission */}
        <section style={sectionStyle}>
          <div style={cardStyle}>
            <h2 style={{ ...h2Style, display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ fontSize: '32px' }}>🎯</span> Notre Mission
            </h2>
            <p style={pStyle}>
              IAFACTORY a pour mission de démocratiser l'accès à l'intelligence artificielle en Algérie et dans toute l'Afrique du Nord. Nous croyons que l'IA doit être accessible à tous : entreprises, étudiants, professionnels et particuliers.
            </p>
            <p style={pStyle}>
              Notre plateforme offre des outils IA de pointe adaptés aux besoins locaux, avec un support multilingue complet (Arabe, Français, Anglais) et des solutions de paiement locales.
            </p>
          </div>
        </section>

        {/* Vision */}
        <section style={sectionStyle}>
          <div style={cardStyle}>
            <h2 style={{ ...h2Style, display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ fontSize: '32px' }}>🔮</span> Notre Vision
            </h2>
            <p style={pStyle}>
              Nous envisageons un futur où l'Algérie devient un hub technologique majeur en Afrique, où les talents locaux peuvent créer et innover grâce à l'IA, et où les entreprises algériennes peuvent rivaliser à l'échelle mondiale.
            </p>
            <p style={pStyle}>
              IAFACTORY aspire à être le pont entre les avancées mondiales de l'IA et les besoins spécifiques du marché algérien et africain.
            </p>
          </div>
        </section>

        {/* Values */}
        <section style={sectionStyle}>
          <h2 style={{ ...h2Style, textAlign: 'center', marginBottom: '32px' }}>Nos Valeurs</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
            <div style={valueCardStyle}>
              <div style={{ fontSize: '40px', marginBottom: '12px' }}>🇩🇿</div>
              <h3 style={{ color: colors.textPrimary, fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Souveraineté</h3>
              <p style={{ color: colors.textMuted, fontSize: '14px' }}>Données hébergées localement, respect de la vie privée</p>
            </div>
            <div style={valueCardStyle}>
              <div style={{ fontSize: '40px', marginBottom: '12px' }}>💡</div>
              <h3 style={{ color: colors.textPrimary, fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Innovation</h3>
              <p style={{ color: colors.textMuted, fontSize: '14px' }}>Technologies de pointe accessibles à tous</p>
            </div>
            <div style={valueCardStyle}>
              <div style={{ fontSize: '40px', marginBottom: '12px' }}>🤝</div>
              <h3 style={{ color: colors.textPrimary, fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Accessibilité</h3>
              <p style={{ color: colors.textMuted, fontSize: '14px' }}>Tarifs adaptés au marché local</p>
            </div>
            <div style={valueCardStyle}>
              <div style={{ fontSize: '40px', marginBottom: '12px' }}>🔒</div>
              <h3 style={{ color: colors.textPrimary, fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Sécurité</h3>
              <p style={{ color: colors.textMuted, fontSize: '14px' }}>Protection des données de niveau entreprise</p>
            </div>
          </div>
        </section>

        {/* Team */}
        <section style={sectionStyle}>
          <div style={cardStyle}>
            <h2 style={{ ...h2Style, display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ fontSize: '32px' }}>👥</span> Notre Équipe
            </h2>
            <p style={pStyle}>
              IAFACTORY est fondée et développée par une équipe passionnée d'ingénieurs et d'entrepreneurs algériens, combinant expertise technique mondiale et connaissance approfondie du marché local.
            </p>
            <p style={pStyle}>
              Nous sommes basés à Alger et travaillons avec des partenaires technologiques de premier plan pour offrir les meilleures solutions IA disponibles.
            </p>
          </div>
        </section>

        {/* CTA */}
        <section style={{ textAlign: 'center', marginTop: '60px' }}>
          <h2 style={{ color: colors.textPrimary, fontSize: '28px', fontWeight: 600, marginBottom: '16px' }}>
            Prêt à commencer ?
          </h2>
          <p style={{ color: colors.textMuted, marginBottom: '24px' }}>
            Rejoignez des milliers d'utilisateurs qui font confiance à IAFACTORY
          </p>
          <a
            href="/login"
            style={{
              display: 'inline-block',
              background: accent.primary,
              color: '#fff',
              padding: '14px 32px',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: 600,
              fontSize: '16px',
            }}
          >
            Essayer gratuitement
          </a>
        </section>
      </div>
    </main>
  );
}
