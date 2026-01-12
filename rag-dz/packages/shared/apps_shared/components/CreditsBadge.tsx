import React, { useState, useEffect, useCallback } from 'react';

// ============================================
// Types
// ============================================
interface CreditsData {
  used: number;
  total: number;
  plan: string;
  reset_date?: string;
  low_threshold?: number;
}

interface CreditsBadgeProps {
  /** URL de l'API crédits (défaut: /api/billing/credits) */
  apiUrl?: string;
  /** Rafraîchir toutes les X secondes (0 = désactivé) */
  refreshInterval?: number;
  /** Seuil d'alerte en % (défaut: 20) */
  warningThreshold?: number;
  /** Afficher le plan */
  showPlan?: boolean;
  /** Mode compact (juste les chiffres) */
  compact?: boolean;
  /** Position fixed (coin supérieur droit) */
  fixed?: boolean;
  /** Callback quand crédits épuisés */
  onCreditsExhausted?: () => void;
  /** Callback pour acheter des crédits */
  onBuyCredits?: () => void;
  /** Style personnalisé */
  className?: string;
}

// ============================================
// Helpers
// ============================================
const formatNumber = (n: number): string => {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return n.toString();
};

const getPercentage = (used: number, total: number): number => {
  if (total === 0) return 0;
  return Math.round((used / total) * 100);
};

const getRemainingPercentage = (used: number, total: number): number => {
  return 100 - getPercentage(used, total);
};

// ============================================
// Composant Principal
// ============================================
export const CreditsBadge: React.FC<CreditsBadgeProps> = ({
  apiUrl = '/api/billing/credits',
  refreshInterval = 60,
  warningThreshold = 20,
  showPlan = true,
  compact = false,
  fixed = false,
  onCreditsExhausted,
  onBuyCredits,
  className = '',
}) => {
  // State
  const [credits, setCredits] = useState<CreditsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isHovered, setIsHovered] = useState(false);

  // Fetch credits
  const fetchCredits = useCallback(async () => {
    try {
      const response = await fetch(apiUrl, {
        credentials: 'include',
      });

      if (!response.ok) {
        if (response.status === 401) {
          setCredits(null);
          return;
        }
        throw new Error(`Erreur ${response.status}`);
      }

      const data = await response.json();
      setCredits(data);
      setError(null);

      // Check si épuisé
      if (data.used >= data.total && onCreditsExhausted) {
        onCreditsExhausted();
      }

    } catch (err) {
      console.error('Erreur fetch credits:', err);
      setError(err instanceof Error ? err.message : 'Erreur');
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl, onCreditsExhausted]);

  // Initial fetch + interval
  useEffect(() => {
    fetchCredits();

    if (refreshInterval > 0) {
      const interval = setInterval(fetchCredits, refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [fetchCredits, refreshInterval]);

  // Calculs
  const remaining = credits ? credits.total - credits.used : 0;
  const remainingPercent = credits ? getRemainingPercentage(credits.used, credits.total) : 100;
  const isLow = remainingPercent <= warningThreshold;
  const isExhausted = credits ? credits.used >= credits.total : false;

  // Couleur selon le niveau
  const getColor = () => {
    if (isExhausted) return 'red';
    if (isLow) return 'amber';
    return 'emerald';
  };
  const color = getColor();

  // Classes de couleur
  const colorClasses = {
    emerald: {
      bg: 'bg-emerald-500/20',
      border: 'border-emerald-500/50',
      text: 'text-emerald-400',
      bar: 'bg-emerald-500',
      glow: 'shadow-emerald-500/20',
    },
    amber: {
      bg: 'bg-amber-500/20',
      border: 'border-amber-500/50',
      text: 'text-amber-400',
      bar: 'bg-amber-500',
      glow: 'shadow-amber-500/20',
    },
    red: {
      bg: 'bg-red-500/20',
      border: 'border-red-500/50',
      text: 'text-red-400',
      bar: 'bg-red-500',
      glow: 'shadow-red-500/20',
    },
  };
  const colors = colorClasses[color];

  // Si pas connecté ou erreur, ne rien afficher
  if (!credits && !isLoading) return null;

  // Mode compact
  if (compact) {
    return (
      <div 
        className={`
          inline-flex items-center gap-2 px-3 py-1.5 rounded-full
          ${colors.bg} ${colors.border} border
          ${fixed ? 'fixed top-4 right-4 z-50' : ''}
          ${className}
        `}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {isLoading ? (
          <span className="text-slate-400 text-sm">...</span>
        ) : (
          <>
            <span className={`text-sm font-semibold ${colors.text}`}>
              {formatNumber(remaining)}
            </span>
            <span className="text-slate-500 text-xs">crédits</span>
          </>
        )}
      </div>
    );
  }

  // Mode complet
  return (
    <div 
      className={`
        ${colors.bg} ${colors.border} border rounded-xl p-3
        shadow-lg ${colors.glow}
        ${fixed ? 'fixed top-4 right-4 z-50' : ''}
        transition-all duration-200
        ${isHovered ? 'scale-105' : ''}
        ${className}
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{ minWidth: '180px' }}
    >
      {isLoading ? (
        <div className="flex items-center justify-center py-2">
          <span className="text-slate-400 text-sm animate-pulse">Chargement...</span>
        </div>
      ) : error ? (
        <div className="text-red-400 text-xs text-center">
          ⚠️ {error}
        </div>
      ) : credits && (
        <>
          {/* Header avec plan */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-lg">💳</span>
              <span className="text-white font-semibold text-sm">Crédits</span>
            </div>
            {showPlan && (
              <span className={`text-xs px-2 py-0.5 rounded-full ${colors.bg} ${colors.text}`}>
                {credits.plan}
              </span>
            )}
          </div>

          {/* Chiffres */}
          <div className="flex items-baseline gap-1 mb-2">
            <span className={`text-2xl font-bold ${colors.text}`}>
              {formatNumber(remaining)}
            </span>
            <span className="text-slate-500 text-sm">
              / {formatNumber(credits.total)}
            </span>
          </div>

          {/* Barre de progression */}
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden mb-2">
            <div 
              className={`h-full ${colors.bar} transition-all duration-500`}
              style={{ width: `${remainingPercent}%` }}
            />
          </div>

          {/* Message selon état */}
          {isExhausted && (
            <div className="text-center">
              <p className="text-red-400 text-xs mb-2">
                ⚠️ Crédits épuisés
              </p>
              {onBuyCredits && (
                <button
                  onClick={onBuyCredits}
                  className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 text-white text-xs font-semibold py-1.5 px-3 rounded-lg hover:opacity-90 transition-opacity"
                >
                  Recharger →
                </button>
              )}
            </div>
          )}

          {isLow && !isExhausted && (
            <p className="text-amber-400 text-xs text-center">
              ⚡ {remainingPercent}% restants
            </p>
          )}

          {/* Date de reset */}
          {credits.reset_date && !isExhausted && (
            <p className="text-slate-500 text-xs text-center mt-1">
              Reset : {new Date(credits.reset_date).toLocaleDateString('fr-FR')}
            </p>
          )}
        </>
      )}
    </div>
  );
};

// ============================================
// Version inline pour header
// ============================================
export const CreditsBadgeInline: React.FC<Omit<CreditsBadgeProps, 'compact' | 'fixed'>> = (props) => {
  return <CreditsBadge {...props} compact fixed={false} />;
};

// ============================================
// Hook pour accéder aux crédits
// ============================================
export const useCredits = (apiUrl = '/api/billing/credits') => {
  const [credits, setCredits] = useState<CreditsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCredits = useCallback(async () => {
    try {
      const response = await fetch(apiUrl, { credentials: 'include' });
      if (!response.ok) throw new Error(`Erreur ${response.status}`);
      const data = await response.json();
      setCredits(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur');
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchCredits();
  }, [fetchCredits]);

  const remaining = credits ? credits.total - credits.used : 0;
  const isLow = credits ? (remaining / credits.total) < 0.2 : false;
  const isExhausted = credits ? remaining <= 0 : false;

  return {
    credits,
    remaining,
    isLow,
    isExhausted,
    isLoading,
    error,
    refresh: fetchCredits,
  };
};

export default CreditsBadge;
