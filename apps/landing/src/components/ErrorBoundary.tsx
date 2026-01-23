import { Component, type ReactNode, type ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    // TODO: Envoyer à un service de monitoring (Sentry, etc.)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'var(--bg-primary, #1a1a1a)',
            color: 'var(--text-primary, #f0f0f0)',
            padding: '24px',
          }}
        >
          <div
            style={{
              maxWidth: '500px',
              textAlign: 'center',
              padding: '40px',
              background: 'var(--bg-card, #262626)',
              borderRadius: '16px',
              border: '1px solid var(--border-color, rgba(255,255,255,0.12))',
            }}
          >
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>⚠️</div>
            <h1
              style={{
                fontSize: '24px',
                fontWeight: 700,
                marginBottom: '12px',
              }}
            >
              Une erreur est survenue
            </h1>
            <p
              style={{
                color: 'var(--text-muted, #A3A3A3)',
                marginBottom: '24px',
                lineHeight: 1.6,
              }}
            >
              Nous nous excusons pour ce désagrément. Veuillez réessayer ou rafraîchir la page.
            </p>
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <pre
                style={{
                  background: 'rgba(255,0,0,0.1)',
                  padding: '12px',
                  borderRadius: '8px',
                  fontSize: '12px',
                  textAlign: 'left',
                  overflow: 'auto',
                  marginBottom: '24px',
                  color: '#ff6b6b',
                }}
              >
                {this.state.error.message}
              </pre>
            )}
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
              <button
                onClick={this.handleRetry}
                style={{
                  padding: '12px 24px',
                  background: 'linear-gradient(135deg, #00A86B, #2ECC71)',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '10px',
                  fontSize: '14px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Réessayer
              </button>
              <button
                onClick={() => window.location.reload()}
                style={{
                  padding: '12px 24px',
                  background: 'transparent',
                  color: 'var(--text-primary, #f0f0f0)',
                  border: '1px solid var(--border-color, rgba(255,255,255,0.12))',
                  borderRadius: '10px',
                  fontSize: '14px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Rafraîchir
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
