'use client';

import { useState, useEffect } from 'react';
import { format } from 'date-fns';

const MOODS = [
  { emoji: '😞', value: 1, label: 'Très mal', color: 'text-red-500' },
  { emoji: '😔', value: 2, label: 'Pas bien', color: 'text-orange-500' },
  { emoji: '😐', value: 3, label: 'Neutre', color: 'text-yellow-500' },
  { emoji: '🙂', value: 4, label: 'Bien', color: 'text-green-500' },
  { emoji: '😊', value: 5, label: 'Très bien', color: 'text-emerald-500' },
];

interface MoodEntry {
  date: string;
  mood: number;
  note?: string;
}

export default function MoodTracker() {
  const [todayMood, setTodayMood] = useState<number | null>(null);
  const [moodHistory, setMoodHistory] = useState<MoodEntry[]>([]);
  const [showNote, setShowNote] = useState(false);
  const [note, setNote] = useState('');

  const today = format(new Date(), 'yyyy-MM-dd');

  // Load from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('mood_history');
    if (saved) {
      const history: MoodEntry[] = JSON.parse(saved);
      setMoodHistory(history);

      // Check if mood already set today
      const todayEntry = history.find((entry) => entry.date === today);
      if (todayEntry) {
        setTodayMood(todayEntry.mood);
        setNote(todayEntry.note || '');
      }
    }
  }, [today]);

  const handleMoodSelect = (value: number) => {
    setTodayMood(value);
    setShowNote(true);
  };

  const saveMood = () => {
    const newEntry: MoodEntry = {
      date: today,
      mood: todayMood!,
      note: note.trim() || undefined,
    };

    // Remove existing entry for today if any
    const updatedHistory = moodHistory.filter((entry) => entry.date !== today);
    updatedHistory.unshift(newEntry);

    // Keep last 30 days
    const limitedHistory = updatedHistory.slice(0, 30);

    setMoodHistory(limitedHistory);
    localStorage.setItem('mood_history', JSON.stringify(limitedHistory));
    setShowNote(false);
  };

  // Calculate average mood for last 7 days
  const recentMoods = moodHistory.slice(0, 7);
  const avgMood = recentMoods.length > 0
    ? (recentMoods.reduce((sum, entry) => sum + entry.mood, 0) / recentMoods.length).toFixed(1)
    : null;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg">Mood Tracker</h3>
        <span className="text-2xl">📊</span>
      </div>

      {/* Today's Check-in */}
      <div className="mb-4">
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">
          Comment tu te sens aujourd'hui ?
        </p>

        <div className="grid grid-cols-5 gap-2">
          {MOODS.map((mood) => (
            <button
              key={mood.value}
              onClick={() => handleMoodSelect(mood.value)}
              disabled={todayMood !== null && !showNote}
              className={`p-3 rounded-lg transition-all ${
                todayMood === mood.value
                  ? 'bg-primary/20 scale-110'
                  : 'bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700'
              } ${todayMood !== null && todayMood !== mood.value && !showNote ? 'opacity-50' : ''}`}
            >
              <div className="text-2xl">{mood.emoji}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Note Input */}
      {showNote && (
        <div className="mb-4 space-y-2 animate-fade-in">
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Ajouter une note (optionnel)..."
            className="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm resize-none"
            rows={2}
          />
          <button onClick={saveMood} className="btn-primary w-full text-sm py-2">
            Enregistrer
          </button>
        </div>
      )}

      {/* Stats */}
      {avgMood && (
        <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-600 dark:text-slate-400">
              Moyenne 7 jours:
            </span>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-primary">{avgMood}</span>
              <span className="text-lg">
                {MOODS.find((m) => m.value === Math.round(parseFloat(avgMood)))?.emoji}
              </span>
            </div>
          </div>

          <div className="mt-3 text-xs text-slate-500 dark:text-slate-400">
            {recentMoods.length} check-ins cette semaine
          </div>
        </div>
      )}

      {todayMood && !showNote && (
        <p className="text-xs text-center text-slate-500 dark:text-slate-400 mt-3">
          ✓ Check-in fait pour aujourd'hui
        </p>
      )}
    </div>
  );
}
