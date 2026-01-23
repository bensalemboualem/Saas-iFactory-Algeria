import { useState, useEffect } from 'react';
import { ApiError } from '../api/client';
import './ErrorBanner.css';

interface ErrorBannerProps {
  error: ApiError | Error | null;
  onDismiss?: () => void;
  onRetry?: () => void;
}

export default function ErrorBanner({ error, onDismiss, onRetry }: ErrorBannerProps) {
  const [countdown, setCountdown] = useState<number | null>(null);

  // Handle rate limit countdown
  useEffect(() => {
    if (error instanceof ApiError && error.isRateLimited()) {
      const retryAfter = error.getRetryAfter();
      if (retryAfter) {
        setCountdown(retryAfter);
        const interval = setInterval(() => {
          setCountdown((prev) => {
            if (prev === null || prev <= 1) {
              clearInterval(interval);
              return null;
            }
            return prev - 1;
          });
        }, 1000);
        return () => clearInterval(interval);
      }
    }
  }, [error]);

  if (!error) return null;

  // Determine error type and content
  let type: 'credits' | 'rateLimit' | 'unavailable' | 'generic' = 'generic';
  let title = 'Error';
  let message = error.message;
  let actionLabel: string | null = null;

  if (error instanceof ApiError) {
    if (error.isInsufficientCredits()) {
      type = 'credits';
      title = 'Insufficient Credits';
      const required = error.getRequiredCredits();
      const balance = error.getBalance();
      message = `This operation requires ${required} credits, but you only have ${balance} credits available.`;
      actionLabel = 'Add Credits';
    } else if (error.isRateLimited()) {
      type = 'rateLimit';
      title = 'Rate Limited';
      message = countdown
        ? `Too many requests. Please wait ${countdown} seconds before trying again.`
        : 'Too many requests. Please try again later.';
      actionLabel = countdown ? null : 'Retry';
    } else if (error.isServiceUnavailable()) {
      type = 'unavailable';
      title = 'Service Unavailable';
      message = error.details?.message || 'The service is temporarily unavailable. Please check your API key configuration or try again later.';
      actionLabel = 'Configure BYOK';
    }
  }

  const handleAction = () => {
    if (type === 'credits') {
      // TODO: Open credits purchase modal or redirect
      window.open('/settings/credits', '_blank');
    } else if (type === 'unavailable') {
      // TODO: Open BYOK settings
      window.open('/settings/keys', '_blank');
    } else if (onRetry) {
      onRetry();
    }
  };

  return (
    <div className={`error-banner error-${type}`}>
      <div className="error-icon">
        {type === 'credits' && '💳'}
        {type === 'rateLimit' && '⏱️'}
        {type === 'unavailable' && '🔌'}
        {type === 'generic' && '⚠️'}
      </div>
      <div className="error-content">
        <h4 className="error-title">{title}</h4>
        <p className="error-message">{message}</p>
      </div>
      <div className="error-actions">
        {actionLabel && (
          <button className="error-action-btn" onClick={handleAction}>
            {actionLabel}
          </button>
        )}
        {onDismiss && (
          <button className="error-dismiss-btn" onClick={onDismiss} aria-label="Dismiss">
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
