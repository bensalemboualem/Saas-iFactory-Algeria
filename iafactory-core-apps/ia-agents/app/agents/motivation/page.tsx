'use client';

import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import MoodTracker from './components/MoodTracker';
import StreakCounter from './components/StreakCounter';
import BreathingExercise from './components/BreathingExercise';
import AchievementBadges from './components/AchievementBadges';

export default function MotivationAgentPage() {
  const [showBreathing, setShowBreathing] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-500/10 to-emerald-600/10 border-b border-slate-200 dark:border-slate-800">
        <div className="container-app py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-6xl">💪</div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                  Coach Motivation
                </h1>
                <p className="text-slate-600 dark:text-slate-400">
                  Amine - Ton coach bien-être quotidien
                </p>
              </div>
            </div>

            <button
              onClick={() => setShowBreathing(!showBreathing)}
              className="hidden md:flex items-center space-x-2 px-4 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-lg transition-colors"
            >
              <span className="text-2xl">🧘</span>
              <span className="text-sm text-slate-700 dark:text-slate-300">
                Exercice Respiration
              </span>
            </button>
          </div>
        </div>
      </section>

      {/* Main Content - 3 Column Layout */}
      <div className="container-app py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Sidebar - Mood Tracker */}
          <aside className="lg:col-span-3 space-y-6">
            <MoodTracker />

            {/* Mobile Breathing Button */}
            <button
              onClick={() => setShowBreathing(!showBreathing)}
              className="lg:hidden w-full btn-primary"
            >
              🧘 Exercice Respiration
            </button>
          </aside>

          {/* Center - Chat Interface */}
          <main className="lg:col-span-6">
            <ChatInterface />
          </main>

          {/* Right Sidebar - Stats & Tools */}
          <aside className="lg:col-span-3 space-y-6">
            <StreakCounter />
            <AchievementBadges />
          </aside>
        </div>
      </div>

      {/* Breathing Exercise Modal */}
      {showBreathing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="relative w-full max-w-md">
            <button
              onClick={() => setShowBreathing(false)}
              className="absolute -top-12 right-0 text-white hover:text-slate-300 text-xl"
            >
              ✕ Fermer
            </button>
            <BreathingExercise />
          </div>
        </div>
      )}
    </div>
  );
}
