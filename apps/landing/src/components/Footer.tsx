import { Link } from 'react-router-dom';
import { useTranslation } from '../i18n';
import { useTheme } from '../hooks';
import { socialLinksConfig } from './icons/SocialIcons';

export default function Footer() {
  const { t } = useTranslation();
  const { colors, accent, isDark } = useTheme();
  const currentYear = new Date().getFullYear();

  const columns = [
    {
      title: t('footer_products') || 'Produits',
      links: [
        { label: t('footer_tools') || 'Outils IA', to: '/tools' },
        { label: t('footer_agents') || 'Agents IA', to: '/agents' },
        { label: t('footer_apps') || 'Applications', to: '/apps' },
      ],
    },
    {
      title: t('footer_resources') || 'Ressources',
      links: [
        { label: t('footer_docs') || 'Documentation', to: '/tools' },
        { label: t('footer_start') || 'Démarrage rapide', to: '/login' },
        { label: 'Support', to: '/contact' },
      ],
    },
    {
      title: t('footer_company') || 'Entreprise',
      links: [
        { label: t('footer_about') || 'À propos', to: '/about' },
        { label: t('footer_pricing') || 'Tarifs', to: '/pricing' },
        { label: 'Contact', to: '/contact' },
      ],
    },
    {
      title: t('footer_legal') || 'Légal',
      links: [
        { label: t('footer_privacy') || 'Confidentialité', to: '/privacy' },
        { label: t('footer_terms') || 'CGU', to: '/cgu' },
      ],
    },
  ];

  const styles = {
    footer: {
      background: 'transparent',
      borderTop: `1px solid ${colors.borderColor}`,
      padding: '32px 20px',
      marginTop: '0',
    },
    footerTop: {
      display: 'grid',
      gridTemplateColumns: '2fr repeat(4, 1fr)',
      gap: '40px',
      maxWidth: '1100px',
      margin: '0 auto 40px',
    },
    footerBrand: {
      maxWidth: '280px',
    },
    logo: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '16px',
      textDecoration: 'none',
    },
    logoText: {
      marginLeft: '10px',
      fontWeight: 700,
      fontSize: '18px',
    },
    description: {
      fontSize: '14px',
      color: colors.textMuted,
      marginBottom: '12px',
      lineHeight: 1.6,
    },
    location: {
      fontSize: '13px',
      color: colors.textMuted,
      marginBottom: '16px',
    },
    socialLinks: {
      display: 'grid',
      gridTemplateColumns: 'repeat(6, 32px)',
      gap: '8px',
    },
    socialLink: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '32px',
      height: '32px',
      borderRadius: '8px',
      background: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
      color: colors.textMuted,
      transition: 'all 0.2s',
    },
    column: {
      minWidth: '120px',
    },
    columnTitle: {
      fontSize: '14px',
      fontWeight: 600,
      color: colors.textPrimary,
      marginBottom: '16px',
      textTransform: 'uppercase' as const,
    },
    columnList: {
      listStyle: 'none',
      padding: 0,
      margin: 0,
    },
    columnItem: {
      marginBottom: '10px',
    },
    columnLink: {
      fontSize: '14px',
      color: colors.textMuted,
      textDecoration: 'none',
    },
    footerBottom: {
      display: 'flex',
      justifyContent: 'space-between',
      flexWrap: 'wrap' as const,
      gap: '16px',
      paddingTop: '24px',
      borderTop: `1px solid ${colors.borderColor}`,
      maxWidth: '1200px',
      margin: '0 auto',
    },
    footerText: {
      fontSize: '13px',
      color: colors.textMuted,
    },
  };

  return (
    <>
      <footer style={styles.footer}>
        <div style={styles.footerTop}>
          {/* Brand Column */}
          <div style={styles.footerBrand}>
            <Link to="/" style={styles.logo}>
              <svg width="40" height="40" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="32" fill={accent.primary} />
                <text x="50" y="52" fontFamily="Arial Black, sans-serif" fontSize="28" fontWeight="900" textAnchor="middle" dominantBaseline="middle" fill="white">
                  <tspan fontSize="22">i</tspan><tspan fontSize="28">AF</tspan>
                </text>
              </svg>
              <span style={styles.logoText}>
                <span style={{ color: accent.primary }}>iA</span>
                <span style={{ color: colors.textPrimary }}>Factory</span>
                <span style={{ color: accent.primary }}> Algeria</span>
              </span>
            </Link>
            <p style={styles.description}>
              {t('footer_description') || "Plateforme IA souveraine pour l'Algérie. Applications intelligentes, agents IA et workflows automatisés."}
            </p>
            <p style={styles.location}>
              <span style={{ color: accent.primary }}>📍</span> Alger, Algérie
            </p>

            {/* Social Links */}
            <div style={styles.socialLinks}>
              {socialLinksConfig.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  title={social.name}
                  target={social.href.startsWith('http') ? '_blank' : undefined}
                  rel={social.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  style={styles.socialLink}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d={social.icon} />
                  </svg>
                </a>
              ))}
            </div>
          </div>

          {/* Link Columns */}
          {columns.map((column) => (
            <div key={column.title} style={styles.column}>
              <h4 style={styles.columnTitle}>{column.title}</h4>
              <ul style={styles.columnList}>
                {column.links.map((link) => (
                  <li key={link.label} style={styles.columnItem}>
                    <Link to={link.to} style={styles.columnLink}>
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Footer Bottom */}
        <div style={styles.footerBottom}>
          <p style={styles.footerText}>
            © {currentYear} IAFactory Algeria. {t('footer_rights') || 'Tous droits réservés.'}
          </p>
          <p style={styles.footerText}>
            {t('footer_made') || 'Fait avec'} ❤️ {t('footer_for_algeria') || "pour l'Algérie"}
          </p>
        </div>
      </footer>

      {/* Responsive CSS */}
      <style>{`
        @media (max-width: 1024px) {
          footer > div:first-child {
            grid-template-columns: repeat(3, 1fr) !important;
          }
        }
        @media (max-width: 640px) {
          footer > div:first-child {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </>
  );
}
