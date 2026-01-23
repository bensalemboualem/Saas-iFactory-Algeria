import { Link } from 'react-router-dom';
import { useTheme } from '../hooks';
import { useTranslation } from '../i18n';

export default function NotFound() {
  const { colors, accent } = useTheme();
  const { t } = useTranslation();

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: colors.bgPrimary,
        padding: '24px',
      }}
    >
      <div
        style={{
          maxWidth: '500px',
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontSize: '120px',
            fontWeight: 900,
            background: accent.gradient,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            lineHeight: 1,
            marginBottom: '16px',
          }}
        >
          404
        </div>
        <h1
          style={{
            fontSize: '28px',
            fontWeight: 700,
            color: colors.textPrimary,
            marginBottom: '12px',
          }}
        >
          {t('page_not_found') || 'Page non trouvée'}
        </h1>
        <p
          style={{
            color: colors.textMuted,
            fontSize: '16px',
            lineHeight: 1.6,
            marginBottom: '32px',
          }}
        >
          {t('page_not_found_desc') || 'La page que vous recherchez n\'existe pas ou a été déplacée.'}
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <Link
            to="/"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '14px 28px',
              background: accent.gradient,
              color: '#fff',
              fontSize: '15px',
              fontWeight: 600,
              textDecoration: 'none',
              borderRadius: '12px',
              boxShadow: `0 4px 12px rgba(0, 168, 107, 0.3)`,
            }}
          >
            <span>←</span>
            {t('back_home') || 'Retour à l\'accueil'}
          </Link>
          <Link
            to="/chat"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '14px 28px',
              background: 'transparent',
              color: colors.textPrimary,
              fontSize: '15px',
              fontWeight: 600,
              textDecoration: 'none',
              borderRadius: '12px',
              border: `1px solid ${colors.borderColor}`,
            }}
          >
            {t('launch_app') || 'Lancer l\'app'}
          </Link>
        </div>
      </div>
    </div>
  );
}
