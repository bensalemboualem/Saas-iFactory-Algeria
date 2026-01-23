'use client';

import { useEffect, useState } from 'react';
import { getDaysUntilStart, getDaysUntilAlgeriaMatch } from '@/data/can2025-data';

interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

export default function Countdown() {
  const [timeUntilTournament, setTimeUntilTournament] = useState<TimeLeft>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  const [timeUntilAlgeria, setTimeUntilAlgeria] = useState<TimeLeft>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);

    const calculateTimeLeft = (targetDate: string): TimeLeft => {
      const now = new Date().getTime();
      const target = new Date(targetDate).getTime();
      const difference = target - now;

      if (difference <= 0) {
        return { days: 0, hours: 0, minutes: 0, seconds: 0 };
      }

      return {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((difference % (1000 * 60)) / 1000),
      };
    };

    const updateCountdowns = () => {
      setTimeUntilTournament(calculateTimeLeft('2025-12-21T18:00:00'));
      setTimeUntilAlgeria(calculateTimeLeft('2025-12-24T17:00:00'));
    };

    // Initial update
    updateCountdowns();

    // Update every second
    const interval = setInterval(updateCountdowns, 1000);

    return () => clearInterval(interval);
  }, []);

  if (!mounted) {
    // Prevent hydration mismatch
    return (
      <div className="grid grid-cols-2 gap-6 mb-12">
        <div className="card text-center">
          <div className="text-slate-400 animate-pulse">Chargement...</div>
        </div>
        <div className="card text-center">
          <div className="text-slate-400 animate-pulse">Chargement...</div>
        </div>
      </div>
    );
  }

  const tournamentStarted = timeUntilTournament.days === 0 &&
                            timeUntilTournament.hours === 0 &&
                            timeUntilTournament.minutes === 0 &&
                            timeUntilTournament.seconds === 0;

  const algeriaStarted = timeUntilAlgeria.days === 0 &&
                         timeUntilAlgeria.hours === 0 &&
                         timeUntilAlgeria.minutes === 0 &&
                         timeUntilAlgeria.seconds === 0;

  return (
    <div className="space-y-8">
      {/* Tournament Countdown */}
      <div className="text-center">
        <h2 className="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white mb-6 flex items-center justify-center space-x-3">
          <span>🏆</span>
          <span>{tournamentStarted ? 'CAN 2025 EN COURS!' : 'Début CAN 2025'}</span>
        </h2>

        {tournamentStarted ? (
          <div className="bg-gradient-to-r from-primary to-secondary text-white rounded-2xl p-8 shadow-2xl animate-pulse-slow">
            <p className="text-3xl md:text-4xl font-bold">⚽ MATCH EN COURS! ⚽</p>
            <p className="text-lg mt-2">La CAN 2025 a commencé!</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="countdown-digit fade-in fade-in-delay-1">
              <div className="number">{timeUntilTournament.days}</div>
              <div className="label">Jours</div>
            </div>
            <div className="countdown-digit fade-in fade-in-delay-2">
              <div className="number">{timeUntilTournament.hours}</div>
              <div className="label">Heures</div>
            </div>
            <div className="countdown-digit fade-in fade-in-delay-3">
              <div className="number">{timeUntilTournament.minutes}</div>
              <div className="label">Minutes</div>
            </div>
            <div className="countdown-digit fade-in fade-in-delay-4">
              <div className="number">{timeUntilTournament.seconds}</div>
              <div className="label">Secondes</div>
            </div>
          </div>
        )}
      </div>

      {/* Algeria Match Countdown */}
      <div className="text-center">
        <h2 className="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white mb-6 flex items-center justify-center space-x-3">
          <span className="text-4xl">🇩🇿</span>
          <span>{algeriaStarted ? 'ALGÉRIE EN MATCH!' : 'Premier Match Algérie'}</span>
        </h2>

        {algeriaStarted ? (
          <div className="algeria-gradient text-white rounded-2xl p-8 shadow-2xl animate-bounce-slow">
            <p className="text-3xl md:text-4xl font-bold">🇩🇿 ALLEZ LES FENNECS! 🦊</p>
            <p className="text-lg mt-2">Algérie vs Guinée équatoriale</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="algeria-gradient countdown-digit fade-in fade-in-delay-1">
              <div className="number">{timeUntilAlgeria.days}</div>
              <div className="label">Jours</div>
            </div>
            <div className="algeria-gradient countdown-digit fade-in fade-in-delay-2">
              <div className="number">{timeUntilAlgeria.hours}</div>
              <div className="label">Heures</div>
            </div>
            <div className="algeria-gradient countdown-digit fade-in fade-in-delay-3">
              <div className="number">{timeUntilAlgeria.minutes}</div>
              <div className="label">Minutes</div>
            </div>
            <div className="algeria-gradient countdown-digit fade-in fade-in-delay-4">
              <div className="number">{timeUntilAlgeria.seconds}</div>
              <div className="label">Secondes</div>
            </div>
          </div>
        )}

        {!algeriaStarted && (
          <div className="mt-4 text-slate-600 dark:text-slate-400">
            <p className="text-sm">
              🏟️ <strong>Stade Prince Moulay Abdellah</strong> (Rabat) - 17:00
            </p>
            <p className="text-sm">
              🆚 Algérie vs Guinée équatoriale
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
