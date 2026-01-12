'use client';

import { useState, useEffect } from 'react';

interface Achievement {
  id: string;
  emoji: string;
  name: string;
  description: string;
  condition: (data: any) => boolean;
  unlocked: boolean;
}

const ACHIEVEMENTS: Achievement[] = [
  {
    id: 'first-session',
    emoji: '🌱',
    name: 'Première session',
    description: 'Commencer ton voyage de développement personnel',
    condition: (data) => data.totalMessages >= 1,
    unlocked: false,
  },
  {
    id: 'week-streak',
    emoji: '🔥',
    name: 'Semaine de feu',
    description: 'Maintenir un streak de 7 jours',
    condition: (data) => data.currentStreak >= 7,
    unlocked: false,
  },
  {
    id: 'goal-reached',
    emoji: '🎯',
    name: 'Objectif atteint',
    description: 'Définir et atteindre un objectif',
    condition: (data) => data.goalsCompleted >= 1,
    unlocked: false,
  },
  {
    id: 'breathing-master',
    emoji: '🧘',
    name: 'Maître de la respiration',
    description: 'Pratiquer 10 exercices de respiration',
    condition: (data) => data.breathingSessions >= 10,
    unlocked: false,
  },
  {
    id: 'consistent',
    emoji: '💪',
    name: 'Constance',
    description: '30 conversations avec Amine',
    condition: (data) => data.totalMessages >= 30,
    unlocked: false,
  },
];

export default function AchievementBadges() {
  const [achievements, setAchievements] = useState<Achievement[]>(ACHIEVEMENTS);
  const [newlyUnlocked, setNewlyUnlocked] = useState<string | null>(null);

  useEffect(() => {
    // Load achievement data
    const saved = localStorage.getItem('achievements');
    if (saved) {
      const savedAchievements = JSON.parse(saved);
      setAchievements(savedAchievements);
    }

    // Check achievements
    checkAchievements();
  }, []);

  const checkAchievements = () => {
    // Gather user data
    const moodHistory = localStorage.getItem('mood_history');
    const streakData = localStorage.getItem('streak_data');
    const messagesUsed = localStorage.getItem('messages_used_today');

    const data = {
      totalMessages: moodHistory ? JSON.parse(moodHistory).length : 0,
      currentStreak: streakData ? JSON.parse(streakData).currentStreak : 0,
      goalsCompleted: 0, // TODO: Track goals
      breathingSessions: parseInt(localStorage.getItem('breathing_sessions') || '0'),
    };

    const updated = achievements.map((achievement) => {
      const shouldUnlock = achievement.condition(data) && !achievement.unlocked;

      if (shouldUnlock) {
        setNewlyUnlocked(achievement.id);
        setTimeout(() => setNewlyUnlocked(null), 3000);
      }

      return {
        ...achievement,
        unlocked: achievement.unlocked || shouldUnlock,
      };
    });

    setAchievements(updated);
    localStorage.setItem('achievements', JSON.stringify(updated));
  };

  const unlockedCount = achievements.filter((a) => a.unlocked).length;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg">Achievements</h3>
        <span className="badge badge-success">
          {unlockedCount}/{achievements.length}
        </span>
      </div>

      {/* Achievement List */}
      <div className="space-y-3">
        {achievements.map((achievement) => (
          <div
            key={achievement.id}
            className={`p-3 rounded-lg transition-all ${
              achievement.unlocked
                ? 'bg-gradient-to-r from-primary/20 to-emerald-500/20 border-2 border-primary/30'
                : 'bg-slate-100 dark:bg-slate-800 opacity-60'
            } ${newlyUnlocked === achievement.id ? 'animate-pulse-slow' : ''}`}
          >
            <div className="flex items-start space-x-3">
              <div
                className={`text-3xl ${achievement.unlocked ? 'grayscale-0' : 'grayscale'}`}
              >
                {achievement.emoji}
              </div>
              <div className="flex-1">
                <h4 className={`font-semibold text-sm ${
                  achievement.unlocked
                    ? 'text-slate-900 dark:text-white'
                    : 'text-slate-500 dark:text-slate-400'
                }`}>
                  {achievement.name}
                </h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                  {achievement.description}
                </p>
              </div>
              {achievement.unlocked && (
                <div className="text-primary">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Progress */}
      <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-slate-600 dark:text-slate-400">Progression:</span>
          <span className="font-bold text-primary">
            {Math.round((unlockedCount / achievements.length) * 100)}%
          </span>
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2">
          <div
            className="bg-gradient-to-r from-primary to-emerald-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${(unlockedCount / achievements.length) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}
