import { useTheme } from '../../hooks';

export default function Privacy() {
  const { colors, accent } = useTheme();

  const sectionStyle = {
    marginBottom: '32px',
  };

  const h2Style = {
    color: colors.textPrimary,
    fontSize: '24px',
    fontWeight: 600,
    marginBottom: '16px',
    borderBottom: `2px solid ${accent.primary}`,
    paddingBottom: '8px',
  };

  const h3Style = {
    color: colors.textPrimary,
    fontSize: '18px',
    fontWeight: 600,
    marginBottom: '12px',
    marginTop: '24px',
  };

  const pStyle = {
    color: colors.textSecondary,
    fontSize: '16px',
    lineHeight: 1.8,
    marginBottom: '16px',
  };

  const listStyle = {
    color: colors.textSecondary,
    fontSize: '16px',
    lineHeight: 1.8,
    paddingLeft: '24px',
    marginBottom: '16px',
  };

  const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse' as const,
    marginBottom: '24px',
  };

  const thStyle = {
    background: colors.bgSecondary,
    color: colors.textPrimary,
    padding: '12px',
    textAlign: 'left' as const,
    borderBottom: `2px solid ${colors.borderColor}`,
  };

  const tdStyle = {
    padding: '12px',
    borderBottom: `1px solid ${colors.borderColor}`,
    color: colors.textSecondary,
  };

  return (
    <main
      style={{
        minHeight: '100vh',
        background: colors.bgPrimary,
        padding: '120px 24px 60px',
      }}
    >
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1
          style={{
            color: colors.textPrimary,
            fontSize: '36px',
            fontWeight: 700,
            marginBottom: '8px',
          }}
        >
          Politique de Confidentialité
        </h1>
        <p style={{ color: colors.textMuted, marginBottom: '40px' }}>
          Dernière mise à jour : 19 janvier 2026
        </p>

        <section style={sectionStyle}>
          <h2 style={h2Style}>1. Introduction</h2>
          <p style={pStyle}>
            IAFACTORY s'engage à protéger la vie privée de ses utilisateurs. Cette Politique de Confidentialité explique comment nous collectons, utilisons, stockons et protégeons vos données personnelles.
          </p>
          <p style={pStyle}>Cette politique est conforme au :</p>
          <ul style={listStyle}>
            <li>Règlement Général sur la Protection des Données (RGPD) - UE</li>
            <li>Loi 18-07 du 10 juin 2018 relative à la protection des données personnelles - Algérie</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>2. Responsable du traitement</h2>
          <ul style={listStyle}>
            <li><strong>IAFACTORY</strong></li>
            <li>Siège social : Algérie</li>
            <li>Email DPO : <a href="mailto:privacy@iafactory.ai" style={{ color: accent.primary }}>privacy@iafactory.ai</a></li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>3. Données collectées</h2>
          <h3 style={h3Style}>3.1 Données fournies par l'utilisateur</h3>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Catégorie</th>
                <th style={thStyle}>Données</th>
                <th style={thStyle}>Finalité</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={tdStyle}>Identification</td>
                <td style={tdStyle}>Nom, prénom, email</td>
                <td style={tdStyle}>Création de compte</td>
              </tr>
              <tr>
                <td style={tdStyle}>Authentification</td>
                <td style={tdStyle}>Mot de passe (haché)</td>
                <td style={tdStyle}>Sécurité du compte</td>
              </tr>
              <tr>
                <td style={tdStyle}>Paiement</td>
                <td style={tdStyle}>Informations de facturation</td>
                <td style={tdStyle}>Traitement des transactions</td>
              </tr>
            </tbody>
          </table>

          <h3 style={h3Style}>3.2 Cookies</h3>
          <p style={pStyle}>Nous utilisons des cookies pour :</p>
          <ul style={listStyle}>
            <li><strong>Essentiels</strong> : Fonctionnement du site (session, authentification)</li>
            <li><strong>Analytiques</strong> : Comprendre l'usage (anonymisés)</li>
            <li><strong>Préférences</strong> : Mémoriser vos choix (langue, thème)</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>4. Traitement des conversations IA</h2>
          <h3 style={h3Style}>Ce que nous NE faisons PAS</h3>
          <ul style={listStyle}>
            <li>Nous ne vendons pas vos conversations</li>
            <li>Nous n'entraînons pas nos modèles sur vos données privées sans consentement</li>
            <li>Nous ne partageons pas vos conversations avec des tiers</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>5. Durée de conservation</h2>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Données</th>
                <th style={thStyle}>Durée</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={tdStyle}>Compte actif</td>
                <td style={tdStyle}>Tant que le compte est actif</td>
              </tr>
              <tr>
                <td style={tdStyle}>Conversations</td>
                <td style={tdStyle}>2 ans ou sur suppression</td>
              </tr>
              <tr>
                <td style={tdStyle}>Données de facturation</td>
                <td style={tdStyle}>10 ans (obligation légale)</td>
              </tr>
              <tr>
                <td style={tdStyle}>Compte supprimé</td>
                <td style={tdStyle}>30 jours puis effacement</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>6. Sécurité</h2>
          <p style={pStyle}>Nous mettons en œuvre :</p>
          <ul style={listStyle}>
            <li>Chiffrement TLS 1.3 en transit</li>
            <li>Chiffrement AES-256 au repos</li>
            <li>Authentification multi-facteurs disponible</li>
            <li>Audits de sécurité réguliers</li>
            <li>Accès restreint aux données (principe du moindre privilège)</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>7. Vos droits</h2>
          <p style={pStyle}>Conformément au RGPD et à la loi algérienne, vous avez le droit de :</p>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Droit</th>
                <th style={thStyle}>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={tdStyle}><strong>Accès</strong></td>
                <td style={tdStyle}>Obtenir une copie de vos données</td>
              </tr>
              <tr>
                <td style={tdStyle}><strong>Rectification</strong></td>
                <td style={tdStyle}>Corriger des données inexactes</td>
              </tr>
              <tr>
                <td style={tdStyle}><strong>Effacement</strong></td>
                <td style={tdStyle}>Supprimer vos données</td>
              </tr>
              <tr>
                <td style={tdStyle}><strong>Portabilité</strong></td>
                <td style={tdStyle}>Recevoir vos données dans un format standard</td>
              </tr>
            </tbody>
          </table>
          <p style={pStyle}><strong>Délai de réponse</strong> : 30 jours maximum</p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>8. Contact</h2>
          <p style={pStyle}>
            <strong>Délégué à la Protection des Données (DPO)</strong><br />
            Email : <a href="mailto:dpo@iafactory.ai" style={{ color: accent.primary }}>dpo@iafactory.ai</a>
          </p>
          <p style={pStyle}>
            Pour toute question : <a href="mailto:privacy@iafactory.ai" style={{ color: accent.primary }}>privacy@iafactory.ai</a>
          </p>
        </section>
      </div>
    </main>
  );
}
