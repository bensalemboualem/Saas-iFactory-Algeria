interface UsageLimitBannerProps {
  messagesUsed: number;
  dailyLimit?: number;
}

export default function UsageLimitBanner({ messagesUsed, dailyLimit = 10 }: UsageLimitBannerProps) {
  const remaining = dailyLimit - messagesUsed;
  const percentage = (messagesUsed / dailyLimit) * 100;

  if (messagesUsed === 0) return null;

  return (
    <div className={`px-4 py-2 border-b ${
      remaining <= 2
        ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-900'
        : remaining <= 5
        ? 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-900'
        : 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-900'
    }`}>
      <div className="flex items-center justify-between text-sm">
        <span className={`font-medium ${
          remaining <= 2
            ? 'text-red-700 dark:text-red-300'
            : remaining <= 5
            ? 'text-yellow-700 dark:text-yellow-300'
            : 'text-blue-700 dark:text-blue-300'
        }`}>
          {messagesUsed}/{dailyLimit} messages utilisés aujourd'hui
        </span>

        {remaining <= 2 && (
          <span className="text-xs text-red-600 dark:text-red-400 font-semibold">
            {remaining} restants!
          </span>
        )}
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 mt-2">
        <div
          className={`h-1.5 rounded-full transition-all ${
            remaining <= 2
              ? 'bg-red-500'
              : remaining <= 5
              ? 'bg-yellow-500'
              : 'bg-blue-500'
          }`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      {remaining === 0 && (
        <p className="text-xs text-red-600 dark:text-red-400 mt-2">
          Limite quotidienne atteinte. Passe à Premium pour continuer! 🚀
        </p>
      )}
    </div>
  );
}
