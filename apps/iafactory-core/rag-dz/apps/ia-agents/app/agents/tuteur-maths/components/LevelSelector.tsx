'use client';

import { useEffect, useState } from 'react';

type Level = 'college' | 'lycee' | 'universite';

export default function LevelSelector() {
  const [selectedLevel, setSelectedLevel] = useState<Level>('lycee');

  useEffect(() => {
    const saved = localStorage.getItem('math_level');
    if (saved) {
      setSelectedLevel(saved as Level);
    }
  }, []);

  const handleLevelChange = (level: Level) => {
    setSelectedLevel(level);
    localStorage.setItem('math_level', level);
  };

  const levels: { value: Level; label: string; emoji: string; description: string }[] = [
    {
      value: 'college',
      label: 'Collège',
      emoji: '🎒',
      description: '1AM - 4AM (BEM)',
    },
    {
      value: 'lycee',
      label: 'Lycée',
      emoji: '📚',
      description: '1AS - 3AS (BAC)',
    },
    {
      value: 'universite',
      label: 'Université',
      emoji: '🎓',
      description: '1ère année',
    },
  ];

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
        📊 Ton Niveau
      </h3>

      <div className="space-y-2">
        {levels.map((level) => (
          <button
            key={level.value}
            onClick={() => handleLevelChange(level.value)}
            className={`w-full text-left p-3 rounded-lg transition-colors ${
              selectedLevel === level.value
                ? 'bg-purple-500 text-white'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{level.emoji}</span>
              <div className="flex-1">
                <p className="font-medium">{level.label}</p>
                <p className={`text-xs ${selectedLevel === level.value ? 'text-purple-100' : 'text-slate-500 dark:text-slate-400'}`}>
                  {level.description}
                </p>
              </div>
              {selectedLevel === level.value && (
                <span className="text-xl">✓</span>
              )}
            </div>
          </button>
        ))}
      </div>

      <div className="mt-4 p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
        <p className="text-xs text-slate-600 dark:text-slate-400">
          💡 Prof. Karim adapte ses explications selon ton niveau
        </p>
      </div>
    </div>
  );
}
