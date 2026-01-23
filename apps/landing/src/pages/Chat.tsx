import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth';
import { useTheme } from '../hooks';

export default function Chat() {
  const { colors, accent } = useTheme();
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate('/login?next=/chat');
    }
  }, [isAuthenticated, isLoading, navigate]);

  if (isLoading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: colors.bgPrimary,
        }}
      >
        <div
          style={{
            width: '40px',
            height: '40px',
            border: `3px solid ${colors.borderColor}`,
            borderTopColor: accent.primary,
            borderRadius: '50%',
            animation: 'spin 0.8s linear infinite',
          }}
        />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  // Redirect to main LobeChat app
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
        paddingTop: '100px',
        background: colors.bgPrimary,
      }}
    >
      <h1
        style={{
          fontSize: '32px',
          fontWeight: 700,
          color: colors.textPrimary,
          marginBottom: '16px',
        }}
      >
        IAFactory Chat
      </h1>

      <p
        style={{
          fontSize: '16px',
          color: colors.textMuted,
          marginBottom: '32px',
          textAlign: 'center',
        }}
      >
        Vous allez etre redirige vers l'application principale...
      </p>

      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <a
          href="http://localhost:3010"
          style={{
            padding: '14px 28px',
            borderRadius: '10px',
            background: accent.gradient,
            color: '#fff',
            fontSize: '16px',
            fontWeight: 600,
            textDecoration: 'none',
          }}
        >
          Ouvrir LobeChat
        </a>

        <a
          href="http://localhost:3001"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            padding: '14px 28px',
            borderRadius: '10px',
            border: `1px solid ${colors.borderColor}`,
            background: 'transparent',
            color: colors.textPrimary,
            fontSize: '16px',
            fontWeight: 500,
            textDecoration: 'none',
          }}
        >
          API Gateway
        </a>
      </div>

      <div
        style={{
          marginTop: '48px',
          padding: '24px',
          borderRadius: '12px',
          background: colors.bgSecondary,
          border: `1px solid ${colors.borderColor}`,
          maxWidth: '500px',
          width: '100%',
        }}
      >
        <h3
          style={{
            fontSize: '16px',
            fontWeight: 600,
            color: colors.textPrimary,
            marginBottom: '12px',
          }}
        >
          Services disponibles
        </h3>
        <ul
          style={{
            listStyle: 'none',
            padding: 0,
            margin: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          {[
            { name: 'Landing Page', url: 'http://localhost:5173', status: 'online' },
            { name: 'LobeChat Frontend', url: 'http://localhost:3010', status: 'online' },
            { name: 'Gateway API', url: 'http://localhost:3001', status: 'online' },
          ].map((service) => (
            <li
              key={service.name}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '8px 0',
                borderBottom: `1px solid ${colors.borderColor}`,
              }}
            >
              <span style={{ color: colors.textPrimary, fontSize: '14px' }}>
                {service.name}
              </span>
              <a
                href={service.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: accent.primary,
                  fontSize: '13px',
                  textDecoration: 'none',
                }}
              >
                {service.url}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
