import { useTheme } from '../../hooks';

export default function CGU() {
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
          Conditions Générales d'Utilisation
        </h1>
        <p style={{ color: colors.textMuted, marginBottom: '40px' }}>
          Dernière mise à jour : 19 janvier 2026
        </p>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 1 - Objet</h2>
          <p style={pStyle}>
            Les présentes Conditions Générales d'Utilisation (ci-après "CGU") ont pour objet de définir les modalités et conditions d'utilisation des services proposés par IAFACTORY (ci-après "la Plateforme"), ainsi que de définir les droits et obligations des parties dans ce cadre.
          </p>
          <p style={pStyle}>
            L'utilisation de la Plateforme implique l'acceptation pleine et entière des présentes CGU.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 2 - Mentions légales</h2>
          <p style={pStyle}><strong>Éditeur de la Plateforme :</strong></p>
          <ul style={listStyle}>
            <li>Raison sociale : IAFACTORY</li>
            <li>Siège social : Algérie</li>
            <li>Email : contact@iafactory.ai</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 3 - Définitions</h2>
          <ul style={listStyle}>
            <li><strong>Utilisateur</strong> : Toute personne physique ou morale accédant à la Plateforme</li>
            <li><strong>Compte</strong> : Espace personnel créé par l'Utilisateur pour accéder aux Services</li>
            <li><strong>Services</strong> : Ensemble des fonctionnalités proposées par la Plateforme</li>
            <li><strong>Crédits</strong> : Unités de consommation permettant d'utiliser les Services</li>
            <li><strong>Contenu Utilisateur</strong> : Tout contenu soumis par l'Utilisateur</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 4 - Accès à la Plateforme</h2>
          <h3 style={h3Style}>4.1 Inscription</h3>
          <p style={pStyle}>L'accès aux Services nécessite la création d'un Compte. L'Utilisateur s'engage à :</p>
          <ul style={listStyle}>
            <li>Fournir des informations exactes et complètes</li>
            <li>Maintenir la confidentialité de ses identifiants</li>
            <li>Informer immédiatement IAFACTORY de toute utilisation non autorisée</li>
          </ul>
          <h3 style={h3Style}>4.2 Conditions d'âge</h3>
          <p style={pStyle}>L'Utilisateur doit être âgé d'au moins 18 ans ou avoir l'autorisation d'un représentant légal.</p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 5 - Description des Services</h2>
          <p style={pStyle}>La Plateforme propose :</p>
          <ul style={listStyle}>
            <li><strong>Assistant IA conversationnel</strong> : Interaction avec des modèles d'intelligence artificielle</li>
            <li><strong>Génération de contenu</strong> : Textes, images, code</li>
            <li><strong>Outils spécialisés</strong> : Traduction, résumé, analyse</li>
            <li><strong>Agents automatisés</strong> : Workflows et automatisations</li>
            <li><strong>API</strong> : Intégration dans des applications tierces</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 6 - Tarification et paiement</h2>
          <h3 style={h3Style}>6.1 Modèle tarifaire</h3>
          <ul style={listStyle}>
            <li><strong>Plan Gratuit</strong> : Accès limité aux fonctionnalités de base</li>
            <li><strong>Plan Pro</strong> : Accès étendu avec crédits mensuels</li>
            <li><strong>Plan Entreprise</strong> : Sur mesure avec support dédié</li>
          </ul>
          <h3 style={h3Style}>6.2 Moyens de paiement</h3>
          <ul style={listStyle}>
            <li>Carte bancaire (Visa, Mastercard)</li>
            <li>Chargily Pay (Algérie)</li>
            <li>Virement bancaire (Entreprise)</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 7 - Obligations de l'Utilisateur</h2>
          <h3 style={h3Style}>7.1 Usages interdits</h3>
          <p style={pStyle}>Il est strictement interdit de :</p>
          <ul style={listStyle}>
            <li>Générer du contenu illégal, haineux, discriminatoire ou pornographique</li>
            <li>Utiliser les Services pour du harcèlement ou de la désinformation</li>
            <li>Tenter de contourner les mesures de sécurité</li>
            <li>Revendre l'accès aux Services sans autorisation</li>
            <li>Extraire massivement des données (scraping)</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 8 - Propriété intellectuelle</h2>
          <p style={pStyle}>
            La Plateforme, son code, son design et ses contenus sont protégés par le droit de la propriété intellectuelle. Toute reproduction non autorisée est interdite.
          </p>
          <p style={pStyle}>
            L'Utilisateur conserve les droits sur le contenu qu'il soumet. Le contenu généré par l'IA appartient à l'Utilisateur dans les limites de la loi applicable.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 9 - Responsabilité</h2>
          <p style={pStyle}>IAFACTORY ne peut être tenue responsable :</p>
          <ul style={listStyle}>
            <li>Des erreurs ou inexactitudes dans le contenu généré par l'IA</li>
            <li>Des dommages indirects résultant de l'utilisation des Services</li>
            <li>Des interruptions de service dues à des cas de force majeure</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Article 10 - Droit applicable</h2>
          <p style={pStyle}>
            Les présentes CGU sont soumises au droit algérien. En cas de litige, les parties s'efforceront de trouver une solution amiable. À défaut, les tribunaux compétents seront ceux du siège social d'IAFACTORY.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>Contact</h2>
          <p style={pStyle}>
            Pour toute question relative aux présentes CGU : <a href="mailto:legal@iafactory.ai" style={{ color: accent.primary }}>legal@iafactory.ai</a>
          </p>
        </section>
      </div>
    </main>
  );
}
