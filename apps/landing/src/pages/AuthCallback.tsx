import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useTheme } from '../hooks';

// URL du chatbot principal (Bolt-UI)
const BOLT_UI_URL = import.meta.env.VITE_BOLT_UI_URL || 'http://localhost:5190';

export default function AuthCallback() {
  const { colors, accent } = useTheme();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = searchParams.get('token');
    const errorParam = searchParams.get('error');

    if (errorParam) {
      setError(getErrorMessage(errorParam));
      setTimeout(() => navigate('/login'), 3000);
      return;
    }

    if (token) {
      // Store token in localStorage
      localStorage.setItem('iaf_token', token);

      // Redirect to Bolt-UI with token
      window.location.href = `${BOLT_UI_URL}?token=${token}`;
    } else {
      setError('Token manquant');
      setTimeout(() => navigate('/login'), 3000);
    }
  }, [searchParams, navigate]);

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: colors.bgPrimary,
      }}
    >
      {error ? (
        <>
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              background: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '24px',
            }}
          >
            <span style={{ color: 'white', fontSize: '24px' }}>!</span>
          </div>
          <p style={{ color: '#ef4444', fontSize: '16px', marginBottom: '8px' }}>
            {error}
          </p>
          <p style={{ color: colors.textMuted, fontSize: '14px' }}>
            Redirection vers la page de connexion...
          </p>
        </>
      ) : (
        <>
          <div
            style={{
              width: '48px',
              height: '48px',
              border: `3px solid ${colors.borderColor}`,
              borderTopColor: accent.primary,
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite',
              marginBottom: '24px',
            }}
          />
          <p style={{ color: colors.textMuted, fontSize: '16px' }}>
            Connexion en cours...
          </p>
          <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
        </>
      )}
    </div>
  );
}

function getErrorMessage(error: string): string {
  switch (error) {
    case 'oauth_failed':
      return 'Erreur lors de la connexion OAuth';
    case 'no_email':
      return 'Aucun email associé à ce compte';
    case 'user_creation_failed':
      return 'Erreur lors de la création du compte';
    default:
      return 'Erreur inconnue';
  }
}
