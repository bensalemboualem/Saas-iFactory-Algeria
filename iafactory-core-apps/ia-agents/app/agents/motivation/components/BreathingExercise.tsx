'use client';

import { useState, useEffect, useRef } from 'react';

type Phase = 'inhale' | 'hold' | 'exhale' | 'idle';

const PHASES = {
  inhale: { duration: 4, label: 'Inspire', color: 'bg-blue-500' },
  hold: { duration: 7, label: 'Retiens', color: 'bg-purple-500' },
  exhale: { duration: 8, label: 'Expire', color: 'bg-green-500' },
};

export default function BreathingExercise() {
  const [isActive, setIsActive] = useState(false);
  const [phase, setPhase] = useState<Phase>('idle');
  const [countdown, setCountdown] = useState(0);
  const [cycles, setCycles] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    if (!isActive) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      return;
    }

    let currentPhase: 'inhale' | 'hold' | 'exhale' = 'inhale';
    let timeLeft = PHASES[currentPhase].duration;

    setPhase(currentPhase);
    setCountdown(timeLeft);

    intervalRef.current = setInterval(() => {
      timeLeft--;
      setCountdown(timeLeft);

      if (timeLeft <= 0) {
        // Move to next phase
        if (currentPhase === 'inhale') {
          currentPhase = 'hold';
        } else if (currentPhase === 'hold') {
          currentPhase = 'exhale';
        } else {
          // Complete cycle
          setCycles((c) => c + 1);
          currentPhase = 'inhale';
        }

        timeLeft = PHASES[currentPhase].duration;
        setPhase(currentPhase);
        setCountdown(timeLeft);
      }
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isActive]);

  const handleStart = () => {
    setIsActive(true);
    setCycles(0);
  };

  const handleStop = () => {
    setIsActive(false);
    setPhase('idle');
    setCountdown(0);
  };

  return (
    <div className="card bg-gradient-to-br from-blue-500/10 to-purple-500/10">
      <div className="text-center">
        <h3 className="text-2xl font-bold mb-2">Respiration 4-7-8</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
          Technique de respiration pour réduire le stress et l'anxiété
        </p>

        {/* Breathing Circle */}
        <div className="relative w-64 h-64 mx-auto mb-6">
          {/* Background Circle */}
          <div className="absolute inset-0 rounded-full bg-slate-200 dark:bg-slate-800"></div>

          {/* Animated Circle */}
          <div
            className={`absolute inset-0 rounded-full transition-all duration-1000 flex items-center justify-center ${
              phase === 'inhale'
                ? 'scale-110 bg-blue-500/30'
                : phase === 'hold'
                ? 'scale-110 bg-purple-500/30'
                : phase === 'exhale'
                ? 'scale-75 bg-green-500/30'
                : 'bg-slate-300/30 dark:bg-slate-700/30'
            }`}
            style={{
              animation: isActive ? 'breathe 4s ease-in-out infinite' : 'none',
            }}
          >
            <div className="text-center">
              {phase !== 'idle' && (
                <>
                  <div className="text-6xl font-bold text-slate-900 dark:text-white mb-2">
                    {countdown}
                  </div>
                  <div className="text-lg font-semibold text-slate-700 dark:text-slate-300">
                    {PHASES[phase].label}
                  </div>
                </>
              )}

              {phase === 'idle' && !isActive && (
                <div className="text-4xl">🧘</div>
              )}
            </div>
          </div>
        </div>

        {/* Stats */}
        {cycles > 0 && (
          <div className="mb-4 text-sm text-slate-600 dark:text-slate-400">
            Cycles complétés: <span className="font-bold text-primary">{cycles}</span>
          </div>
        )}

        {/* Controls */}
        <div className="space-y-3">
          {!isActive ? (
            <button onClick={handleStart} className="btn-primary w-full">
              Commencer
            </button>
          ) : (
            <button
              onClick={handleStop}
              className="w-full py-3 px-6 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors"
            >
              Arrêter
            </button>
          )}
        </div>

        {/* Instructions */}
        <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-800 text-left space-y-2 text-sm text-slate-600 dark:text-slate-400">
          <p className="font-semibold text-slate-900 dark:text-white mb-3">
            Comment pratiquer:
          </p>
          <div className="flex items-start space-x-2">
            <span className="text-blue-500 font-bold">1.</span>
            <p>Inspire par le nez pendant <strong>4 secondes</strong></p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-purple-500 font-bold">2.</span>
            <p>Retiens ta respiration pendant <strong>7 secondes</strong></p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-500 font-bold">3.</span>
            <p>Expire par la bouche pendant <strong>8 secondes</strong></p>
          </div>
          <p className="mt-4 text-xs">
            💡 Recommandé: 4 cycles minimum pour un effet optimal
          </p>
        </div>
      </div>
    </div>
  );
}
