import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth';
import { useTheme } from '../hooks';

// URL du chatbot principal (Bolt-UI)
const BOLT_UI_URL = 'http://localhost:5190';

export default function Chat() {
  const { colors, accent } = useTheme();
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        // Pas connecté → page login
        navigate('/login?next=/chat');
      } else {
        // Connecté → redirection directe vers Bolt-UI (chatbot principal)
        window.location.href = BOLT_UI_URL;
      }
    }
  }, [isAuthenticated, isLoading, navigate]);

  // Affichage pendant le chargement ou la redirection
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
        Redirection vers l'application...
      </p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
