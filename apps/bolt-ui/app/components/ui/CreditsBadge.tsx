import { useCredits } from '~/lib/hooks/useCredits';

export function CreditsBadge() {
  const { balance, loading, error, refresh } = useCredits();

  if (error) {
    return (
      <button
        onClick={refresh}
        className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-red-500/10 text-red-500 text-xs hover:bg-red-500/20 transition-colors"
        title={`Error: ${error}. Click to retry.`}
      >
        <div className="i-ph:warning text-sm" />
        <span>Offline</span>
      </button>
    );
  }

  return (
    <button
      onClick={refresh}
      className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-bolt-elements-background-depth-2 text-bolt-elements-textSecondary text-xs hover:bg-bolt-elements-background-depth-3 transition-colors border border-bolt-elements-borderColor"
      title="Your IAFactory credits. Click to refresh."
    >
      <div className="i-ph:currency-circle-dollar text-sm text-yellow-500" />
      {loading ? (
        <span className="animate-pulse">...</span>
      ) : (
        <span className="font-medium text-bolt-elements-textPrimary">{balance.toFixed(2)}</span>
      )}
      <span className="text-bolt-elements-textTertiary">credits</span>
    </button>
  );
}
