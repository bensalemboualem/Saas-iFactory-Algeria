import { useTheme } from '../../hooks';

export default function Mentions() {
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
          Mentions Légales
        </h1>
        <p style={{ color: colors.textMuted, marginBottom: '40px' }}>
          Dernière mise à jour : 19 janvier 2026
        </p>

        <section style={sectionStyle}>
          <h2 style={h2Style}>1. Éditeur du site</h2>
          <p style={pStyle}>Le site IAFACTORY est édité par :</p>
          <ul style={listStyle}>
            <li><strong>Raison sociale</strong> : IAFACTORY</li>
            <li><strong>Forme juridique</strong> : [À compléter]</li>
            <li><strong>Siège social</strong> : Algérie</li>
            <li><strong>Capital social</strong> : [À compléter]</li>
            <li><strong>Numéro d'immatriculation</strong> : [À compléter]</li>
            <li><strong>Directeur de la publication</strong> : [À compléter]</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>2. Contact</h2>
          <ul style={listStyle}>
            <li><strong>Email</strong> : <a href="mailto:contact@iafactory.ai" style={{ color: accent.primary }}>contact@iafactory.ai</a></li>
            <li><strong>Support</strong> : <a href="mailto:support@iafactory.ai" style={{ color: accent.primary }}>support@iafactory.ai</a></li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>3. Hébergement</h2>
          <p style={pStyle}>Le site est hébergé par :</p>
          <ul style={listStyle}>
            <li><strong>Hébergeur</strong> : [À compléter]</li>
            <li><strong>Adresse</strong> : [À compléter]</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>4. Propriété intellectuelle</h2>
          <p style={pStyle}>
            L'ensemble du contenu du site IAFACTORY (logos, textes, éléments graphiques, vidéos, etc.) est protégé par le droit d'auteur et le droit des marques.
          </p>
          <p style={pStyle}>
            Toute reproduction, représentation, modification, publication, transmission, dénaturation, totale ou partielle du site ou de son contenu, par quelque procédé que ce soit, et sur quelque support que ce soit est interdite sans l'autorisation écrite préalable d'IAFACTORY.
          </p>
          <p style={pStyle}>
            Toute exploitation non autorisée du site ou de son contenu sera considérée comme constitutive d'une contrefaçon et poursuivie conformément aux dispositions légales en vigueur.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>5. Données personnelles</h2>
          <p style={pStyle}>
            Les informations concernant la collecte et le traitement des données personnelles sont détaillées dans notre{' '}
            <a href="/privacy" style={{ color: accent.primary }}>Politique de Confidentialité</a>.
          </p>
          <p style={pStyle}>
            Conformément à la loi algérienne n° 18-07 du 10 juin 2018 relative à la protection des personnes physiques dans le traitement des données à caractère personnel, vous disposez d'un droit d'accès, de rectification et de suppression des données vous concernant.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>6. Cookies</h2>
          <p style={pStyle}>
            Le site utilise des cookies pour améliorer l'expérience utilisateur. Pour plus d'informations sur l'utilisation des cookies, veuillez consulter notre{' '}
            <a href="/privacy" style={{ color: accent.primary }}>Politique de Confidentialité</a>.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>7. Limitation de responsabilité</h2>
          <p style={pStyle}>
            IAFACTORY s'efforce d'assurer au mieux de ses possibilités l'exactitude et la mise à jour des informations diffusées sur son site. Toutefois, IAFACTORY décline toute responsabilité :
          </p>
          <ul style={listStyle}>
            <li>Pour toute imprécision, inexactitude ou omission portant sur des informations disponibles sur le site</li>
            <li>Pour tous dommages résultant d'une intrusion frauduleuse d'un tiers</li>
            <li>Pour tous dommages, directs ou indirects, résultant de l'accès ou de l'utilisation du site</li>
          </ul>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>8. Liens hypertextes</h2>
          <p style={pStyle}>
            Le site peut contenir des liens hypertextes vers d'autres sites. IAFACTORY n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant à leur contenu.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>9. Droit applicable</h2>
          <p style={pStyle}>
            Les présentes mentions légales sont soumises au droit algérien. En cas de litige, les tribunaux algériens seront seuls compétents.
          </p>
        </section>

        <section style={sectionStyle}>
          <h2 style={h2Style}>10. Crédits</h2>
          <ul style={listStyle}>
            <li><strong>Conception et développement</strong> : IAFACTORY</li>
            <li><strong>Technologies</strong> : React, TypeScript, Vite</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
