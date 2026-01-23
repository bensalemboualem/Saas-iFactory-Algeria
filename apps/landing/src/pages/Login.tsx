import { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../auth';
import { useTheme } from '../hooks';

// SVG Icons for OAuth providers
const GoogleIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24">
    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
  </svg>
);

const FacebookIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="#1877F2">
    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
  </svg>
);

export default function Login() {
  const { isDark, colors, accent } = useTheme();
  const { login, signup, loginWithGoogle, loginWithFacebook, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [oauthLoading, setOauthLoading] = useState<'google' | 'facebook' | null>(null);

  const nextUrl = searchParams.get('next') || '/chat';

  // Redirect if already authenticated
  if (isAuthenticated) {
    navigate(nextUrl);
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isSignup) {
        await signup(email, password, name);
      } else {
        await login(email, password);
      }
      navigate(nextUrl);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOAuthLogin = async (provider: 'google' | 'facebook') => {
    setError('');
    setOauthLoading(provider);

    try {
      if (provider === 'google') {
        await loginWithGoogle();
      } else {
        await loginWithFacebook();
      }
      navigate(nextUrl);
    } catch (err) {
      setError(err instanceof Error ? err.message : `Connexion ${provider} echouee`);
    } finally {
      setOauthLoading(null);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
        paddingTop: '100px',
        background: colors.bgPrimary,
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '400px',
          background: isDark ? '#262626' : '#ffffff',
          borderRadius: '16px',
          padding: '32px',
          border: `1px solid ${colors.borderColor}`,
          boxShadow: isDark
            ? '0 8px 32px rgba(0, 0, 0, 0.4)'
            : '0 8px 32px rgba(0, 0, 0, 0.08)',
        }}
      >
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <Link to="/" style={{ textDecoration: 'none' }}>
            <span style={{ fontSize: '24px', fontWeight: 700 }}>
              <span style={{ color: accent.primary }}>iA</span>
              <span style={{ color: colors.textPrimary }}>Factory</span>
            </span>
          </Link>
        </div>

        <h1
          style={{
            fontSize: '24px',
            fontWeight: 600,
            color: colors.textPrimary,
            textAlign: 'center',
            marginBottom: '8px',
          }}
        >
          {isSignup ? 'Creer un compte' : 'Se connecter'}
        </h1>

        <p
          style={{
            fontSize: '14px',
            color: colors.textMuted,
            textAlign: 'center',
            marginBottom: '24px',
          }}
        >
          {isSignup
            ? 'Commencez avec 5 credits gratuits'
            : 'Accedez a l\'IA mondiale'}
        </p>

        {error && (
          <div
            style={{
              padding: '12px',
              borderRadius: '8px',
              background: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              color: '#ef4444',
              fontSize: '14px',
              marginBottom: '16px',
            }}
          >
            {error}
          </div>
        )}

        {/* OAuth Buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
          <button
            type="button"
            onClick={() => handleOAuthLogin('google')}
            disabled={oauthLoading !== null}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
              width: '100%',
              padding: '12px 16px',
              borderRadius: '10px',
              border: `1px solid ${colors.borderColor}`,
              background: isDark ? '#1a1a1a' : '#ffffff',
              color: colors.textPrimary,
              fontSize: '15px',
              fontWeight: 500,
              cursor: oauthLoading ? 'not-allowed' : 'pointer',
              opacity: oauthLoading && oauthLoading !== 'google' ? 0.5 : 1,
              transition: 'all 0.2s',
            }}
          >
            {oauthLoading === 'google' ? (
              <div
                style={{
                  width: '20px',
                  height: '20px',
                  border: '2px solid transparent',
                  borderTopColor: colors.textPrimary,
                  borderRadius: '50%',
                  animation: 'spin 0.8s linear infinite',
                }}
              />
            ) : (
              <GoogleIcon />
            )}
            Continuer avec Google
          </button>

          <button
            type="button"
            onClick={() => handleOAuthLogin('facebook')}
            disabled={oauthLoading !== null}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
              width: '100%',
              padding: '12px 16px',
              borderRadius: '10px',
              border: 'none',
              background: '#1877F2',
              color: '#ffffff',
              fontSize: '15px',
              fontWeight: 500,
              cursor: oauthLoading ? 'not-allowed' : 'pointer',
              opacity: oauthLoading && oauthLoading !== 'facebook' ? 0.5 : 1,
              transition: 'all 0.2s',
            }}
          >
            {oauthLoading === 'facebook' ? (
              <div
                style={{
                  width: '20px',
                  height: '20px',
                  border: '2px solid transparent',
                  borderTopColor: '#ffffff',
                  borderRadius: '50%',
                  animation: 'spin 0.8s linear infinite',
                }}
              />
            ) : (
              <FacebookIcon />
            )}
            Continuer avec Facebook
          </button>
        </div>

        {/* Divider */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            marginBottom: '24px',
          }}
        >
          <div style={{ flex: 1, height: '1px', background: colors.borderColor }} />
          <span style={{ fontSize: '13px', color: colors.textMuted }}>ou</span>
          <div style={{ flex: 1, height: '1px', background: colors.borderColor }} />
        </div>

        <form onSubmit={handleSubmit}>
          {isSignup && (
            <div style={{ marginBottom: '16px' }}>
              <label
                htmlFor="name"
                style={{
                  display: 'block',
                  fontSize: '14px',
                  fontWeight: 500,
                  color: colors.textPrimary,
                  marginBottom: '6px',
                }}
              >
                Nom
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Votre nom"
                style={{
                  width: '100%',
                  padding: '12px 14px',
                  borderRadius: '10px',
                  border: `1px solid ${colors.borderColor}`,
                  background: isDark ? '#1a1a1a' : '#f9f9f9',
                  color: colors.textPrimary,
                  fontSize: '15px',
                  outline: 'none',
                  boxSizing: 'border-box',
                }}
              />
            </div>
          )}

          <div style={{ marginBottom: '16px' }}>
            <label
              htmlFor="email"
              style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: 500,
                color: colors.textPrimary,
                marginBottom: '6px',
              }}
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="vous@exemple.com"
              required
              style={{
                width: '100%',
                padding: '12px 14px',
                borderRadius: '10px',
                border: `1px solid ${colors.borderColor}`,
                background: isDark ? '#1a1a1a' : '#f9f9f9',
                color: colors.textPrimary,
                fontSize: '15px',
                outline: 'none',
                boxSizing: 'border-box',
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label
              htmlFor="password"
              style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: 500,
                color: colors.textPrimary,
                marginBottom: '6px',
              }}
            >
              Mot de passe
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              minLength={6}
              style={{
                width: '100%',
                padding: '12px 14px',
                borderRadius: '10px',
                border: `1px solid ${colors.borderColor}`,
                background: isDark ? '#1a1a1a' : '#f9f9f9',
                color: colors.textPrimary,
                fontSize: '15px',
                outline: 'none',
                boxSizing: 'border-box',
              }}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            style={{
              width: '100%',
              padding: '14px',
              borderRadius: '10px',
              border: 'none',
              background: accent.gradient,
              color: '#fff',
              fontSize: '16px',
              fontWeight: 600,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.7 : 1,
            }}
          >
            {isLoading
              ? 'Chargement...'
              : isSignup
              ? 'Creer mon compte'
              : 'Se connecter'}
          </button>
        </form>

        <div
          style={{
            marginTop: '24px',
            textAlign: 'center',
            fontSize: '14px',
            color: colors.textMuted,
          }}
        >
          {isSignup ? 'Deja un compte ?' : 'Pas encore de compte ?'}{' '}
          <button
            type="button"
            onClick={() => {
              setIsSignup(!isSignup);
              setError('');
            }}
            style={{
              background: 'none',
              border: 'none',
              color: accent.primary,
              fontWeight: 500,
              cursor: 'pointer',
              padding: 0,
            }}
          >
            {isSignup ? 'Se connecter' : 'Creer un compte'}
          </button>
        </div>
      </div>

      {/* Spinner animation */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
