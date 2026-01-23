'use client';

import { useState, useEffect } from 'react';
import { format, differenceInDays, startOfDay } from 'date-fns';

interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastCheckIn: string;
  checkInDates: string[];
}

export default function StreakCounter() {
  const [streakData, setStreakData] = useState<StreakData>({
    currentStreak: 0,
    longestStreak: 0,
    lastCheckIn: '',
    checkInDates: [],
  });

  useEffect(() => {
    const saved = localStorage.getItem('streak_data');
    if (saved) {
      setStreakData(JSON.parse(saved));
    }

    // Also check mood tracker for today's check-in
    const moodHistory = localStorage.getItem('mood_history');
    if (moodHistory) {
      const moods = JSON.parse(moodHistory);
      const today = format(new Date(), 'yyyy-MM-dd');
      const todayMood = moods.find((m: any) => m.date === today);

      if (todayMood && saved) {
        const data: StreakData = JSON.parse(saved);
        if (data.lastCheckIn !== today) {
          // Update streak
          updateStreak(data, today);
        }
      }
    }
  }, []);

  const updateStreak = (data: StreakData, today: string) => {
    const lastDate = data.lastCheckIn ? startOfDay(new Date(data.lastCheckIn)) : null;
    const todayDate = startOfDay(new Date(today));

    if (!lastDate) {
      // First check-in
      const newData = {
        currentStreak: 1,
        longestStreak: 1,
        lastCheckIn: today,
        checkInDates: [today],
      };
      setStreakData(newData);
      localStorage.setItem('streak_data', JSON.stringify(newData));
      return;
    }

    const daysDiff = differenceInDays(todayDate, lastDate);

    if (daysDiff === 1) {
      // Consecutive day
      const newStreak = data.currentStreak + 1;
      const newData = {
        currentStreak: newStreak,
        longestStreak: Math.max(newStreak, data.longestStreak),
        lastCheckIn: today,
        checkInDates: [...data.checkInDates, today].slice(-30),
      };
      setStreakData(newData);
      localStorage.setItem('streak_data', JSON.stringify(newData));
    } else if (daysDiff > 1) {
      // Streak broken
      const newData = {
        currentStreak: 1,
        longestStreak: data.longestStreak,
        lastCheckIn: today,
        checkInDates: [...data.checkInDates, today].slice(-30),
      };
      setStreakData(newData);
      localStorage.setItem('streak_data', JSON.stringify(newData));
    }
  };

  const getMotivationalMessage = (streak: number) => {
    if (streak === 0) return "Commence ta série! 🌱";
    if (streak === 1) return "Premier jour! Continue! 💪";
    if (streak === 3) return "3 jours consécutifs! 👏";
    if (streak === 7) return "Une semaine complète! 🔥";
    if (streak === 14) return "2 semaines! Incroyable! ✨";
    if (streak === 30) return "Un mois entier! Champion! 🏆";
    if (streak >= 50) return "Tu es une légende! 🌟";
    return `${streak} jours! Continue! 🔥`;
  };

  return (
    <div className="card bg-gradient-to-br from-orange-500/10 to-red-500/10 border-orange-200 dark:border-orange-900">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg">Streak</h3>
        <span className="text-2xl">🔥</span>
      </div>

      {/* Current Streak */}
      <div className="text-center py-6">
        <div className="text-6xl font-bold text-orange-500 dark:text-orange-400 mb-2">
          {streakData.currentStreak}
        </div>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          {streakData.currentStreak === 1 ? 'jour consécutif' : 'jours consécutifs'}
        </p>

        <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mt-3">
          {getMotivationalMessage(streakData.currentStreak)}
        </p>
      </div>

      {/* Stats */}
      <div className="pt-4 border-t border-orange-200 dark:border-orange-900 space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-600 dark:text-slate-400">Meilleure série:</span>
          <span className="font-bold text-orange-600 dark:text-orange-400">
            {streakData.longestStreak} {streakData.longestStreak === 1 ? 'jour' : 'jours'}
          </span>
        </div>

        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-600 dark:text-slate-400">Total check-ins:</span>
          <span className="font-bold text-slate-900 dark:text-white">
            {streakData.checkInDates.length}
          </span>
        </div>
      </div>

      {/* Milestones */}
      <div className="mt-4 pt-4 border-t border-orange-200 dark:border-orange-900">
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">Prochains jalons:</p>
        <div className="flex flex-wrap gap-2">
          {[3, 7, 14, 30].map((milestone) => (
            <div
              key={milestone}
              className={`text-xs px-2 py-1 rounded-full ${
                streakData.currentStreak >= milestone
                  ? 'bg-orange-500 text-white'
                  : 'bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
              }`}
            >
              {milestone}j {streakData.currentStreak >= milestone && '✓'}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
