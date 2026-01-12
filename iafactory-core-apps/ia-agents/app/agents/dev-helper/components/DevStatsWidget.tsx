'use client';

import { useEffect, useState } from 'react';
import { format } from 'date-fns';

interface DevStats {
  questionsAsked: number;
  bugsFixed: number;
  snippetsUsed: number;
  streak: number;
  lastActive: string;
}

export default function DevStatsWidget() {
  const [stats, setStats] = useState<DevStats>({
    questionsAsked: 0,
    bugsFixed: 0,
    snippetsUsed: 0,
    streak: 0,
    lastActive: format(new Date(), 'yyyy-MM-dd'),
  });

  useEffect(() => {
    const saved = localStorage.getItem('dev_stats');
    if (saved) {
      setStats(JSON.parse(saved));
    }
  }, []);

  const getStreakEmoji = (streak: number) => {
    if (streak === 0) return '💤';
    if (streak < 3) return '🔥';
    if (streak < 7) return '🔥🔥';
    if (streak < 30) return '🔥🔥🔥';
    return '🔥🔥🔥🔥';
  };

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
        📊 Your Stats
      </h3>

      <div className="space-y-4">
        {/* Streak */}
        <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-700 dark:text-slate-300">Coding Streak</span>
            <span className="text-2xl">{getStreakEmoji(stats.streak)}</span>
          </div>
          <p className="text-2xl font-bold text-orange-600 dark:text-orange-400 mt-1">
            {stats.streak} {stats.streak === 1 ? 'day' : 'days'}
          </p>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-3">
          {/* Questions Asked */}
          <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-xs text-slate-600 dark:text-slate-400">Questions</p>
            <p className="text-xl font-bold text-blue-600 dark:text-blue-400">
              {stats.questionsAsked}
            </p>
          </div>

          {/* Bugs Fixed */}
          <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <p className="text-xs text-slate-600 dark:text-slate-400">Bugs Fixed</p>
            <p className="text-xl font-bold text-green-600 dark:text-green-400">
              {stats.bugsFixed}
            </p>
          </div>

          {/* Snippets Used */}
          <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg col-span-2">
            <p className="text-xs text-slate-600 dark:text-slate-400">Snippets Used</p>
            <p className="text-xl font-bold text-purple-600 dark:text-purple-400">
              {stats.snippetsUsed}
            </p>
          </div>
        </div>

        {/* Motivational message */}
        <div className="p-3 bg-slate-100 dark:bg-slate-800 rounded-lg text-center">
          {stats.questionsAsked === 0 ? (
            <p className="text-sm text-slate-600 dark:text-slate-400">
              🚀 Start coding and track your progress!
            </p>
          ) : stats.questionsAsked < 10 ? (
            <p className="text-sm text-slate-600 dark:text-slate-400">
              💪 You're getting started! Keep going!
            </p>
          ) : stats.questionsAsked < 50 ? (
            <p className="text-sm text-slate-600 dark:text-slate-400">
              🎯 Great progress! You're learning fast!
            </p>
          ) : (
            <p className="text-sm text-slate-600 dark:text-slate-400">
              🏆 Coding champion! Impressive dedication!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
