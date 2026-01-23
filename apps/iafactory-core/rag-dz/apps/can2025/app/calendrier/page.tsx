import Link from 'next/link';
import { ALL_MATCHES, getTeamById } from '@/data/can2025-data';

export default function CalendrierPage() {
  // Group matches by date
  const matchesByDate = ALL_MATCHES.reduce((acc, match) => {
    if (!acc[match.date]) {
      acc[match.date] = [];
    }
    acc[match.date].push(match);
    return acc;
  }, {} as Record<string, typeof ALL_MATCHES>);

  const sortedDates = Object.keys(matchesByDate).sort();

  return (
    <div className="py-8">
      {/* Hero */}
      <section className="container-app mb-12">
        <div className="text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
            📅 Calendrier Complet
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Tous les matchs de la CAN 2025 - 21 décembre 2025 au 18 janvier 2026
          </p>
        </div>
      </section>

      {/* Tournament Phases */}
      <section className="container-app mb-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card text-center">
            <div className="text-3xl mb-2">📋</div>
            <div className="text-2xl font-bold text-primary">36</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Matchs de groupes</div>
            <div className="text-xs text-slate-500 dark:text-slate-500 mt-1">21 Déc - 2 Jan</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl mb-2">🎯</div>
            <div className="text-2xl font-bold text-primary">8</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">8èmes de finale</div>
            <div className="text-xs text-slate-500 dark:text-slate-500 mt-1">5-8 Jan</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl mb-2">⚔️</div>
            <div className="text-2xl font-bold text-primary">4</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Quarts de finale</div>
            <div className="text-xs text-slate-500 dark:text-slate-500 mt-1">11-12 Jan</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl mb-2">🏆</div>
            <div className="text-2xl font-bold text-secondary">3</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Demi + Finale</div>
            <div className="text-xs text-slate-500 dark:text-slate-500 mt-1">15-18 Jan</div>
          </div>
        </div>
      </section>

      {/* Filter / Quick Jump */}
      <section className="container-app mb-8">
        <div className="card">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
            🔍 Accès Rapide
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Link href="#phase-groupes" className="btn-outline text-center">
              📋 Phase de groupes
            </Link>
            <Link href="/algerie" className="btn-primary text-center">
              🇩🇿 Matchs Algérie
            </Link>
            <Link href="/groupes" className="btn-outline text-center">
              📊 Classements
            </Link>
            <a href="#finale" className="btn-outline text-center">
              🏆 Finale (18 Jan)
            </a>
          </div>
        </div>
      </section>

      {/* Matches by Date */}
      <section className="container-app" id="phase-groupes">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-8">
          ⚽ Phase de Groupes
        </h2>

        <div className="space-y-12">
          {sortedDates.map((date) => {
            const matches = matchesByDate[date];
            const dateObj = new Date(date);

            return (
              <div key={date} className="space-y-4">
                {/* Date Header */}
                <div className="sticky top-20 z-10 bg-gradient-to-r from-primary to-secondary text-white rounded-xl p-4 shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">
                        {dateObj.toLocaleDateString('fr-FR', {
                          weekday: 'long',
                          day: 'numeric',
                          month: 'long',
                          year: 'numeric'
                        })}
                      </div>
                      <div className="text-sm text-white/80">
                        {matches.length} match{matches.length > 1 ? 's' : ''} programmé{matches.length > 1 ? 's' : ''}
                      </div>
                    </div>
                    <div className="text-4xl">
                      {matches.some(m => m.homeTeam === 'ALG' || m.awayTeam === 'ALG') && '🇩🇿'}
                    </div>
                  </div>
                </div>

                {/* Matches for this date */}
                <div className="space-y-4">
                  {matches.map((match) => {
                    const homeTeam = getTeamById(match.homeTeam);
                    const awayTeam = getTeamById(match.awayTeam);
                    const hasAlgeria = match.homeTeam === 'ALG' || match.awayTeam === 'ALG';

                    return (
                      <div
                        key={match.id}
                        className={`card ${hasAlgeria ? 'border-4 border-primary' : ''}`}
                      >
                        {hasAlgeria && (
                          <div className="mb-4 flex items-center justify-center space-x-2 bg-primary/10 dark:bg-primary/20 py-2 rounded-lg">
                            <span className="text-2xl">🇩🇿</span>
                            <span className="font-bold text-primary">ALGÉRIE EN MATCH</span>
                            <span className="text-2xl">🇩🇿</span>
                          </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-center">
                          {/* Match Info */}
                          <div className="text-center md:text-left space-y-1">
                            <div className="text-2xl font-bold text-primary">{match.time}</div>
                            <div className="badge badge-primary">{match.group ? `Groupe ${match.group}` : match.stage}</div>
                            <div className="text-xs text-slate-500 dark:text-slate-400">
                              🏟️ {match.stadium}
                            </div>
                            <div className="text-xs text-slate-500 dark:text-slate-400">
                              📍 {match.city}
                            </div>
                          </div>

                          {/* Home Team */}
                          <div className="text-center">
                            <div className="text-5xl mb-2">{homeTeam?.flag}</div>
                            <div className={`text-lg font-bold ${match.homeTeam === 'ALG' ? 'text-primary' : 'text-slate-900 dark:text-white'}`}>
                              {homeTeam?.nameFr}
                            </div>
                          </div>

                          {/* VS */}
                          <div className="text-center">
                            <div className="text-3xl font-bold text-slate-400">VS</div>
                          </div>

                          {/* Away Team */}
                          <div className="text-center">
                            <div className="text-5xl mb-2">{awayTeam?.flag}</div>
                            <div className={`text-lg font-bold ${match.awayTeam === 'ALG' ? 'text-primary' : 'text-slate-900 dark:text-white'}`}>
                              {awayTeam?.nameFr}
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Knockout Stages (Placeholder) */}
      <section className="container-app mt-16">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-8">
          🏆 Phases Finales
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card text-center">
            <div className="text-5xl mb-4">⚔️</div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">8èmes de finale</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              5-8 janvier 2026
            </p>
            <div className="text-xs text-slate-500 dark:text-slate-500">
              Disponible après la phase de groupes
            </div>
          </div>

          <div className="card text-center">
            <div className="text-5xl mb-4">🔥</div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Quarts & Demi</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              11-15 janvier 2026
            </p>
            <div className="text-xs text-slate-500 dark:text-slate-500">
              Les meilleurs s'affrontent
            </div>
          </div>

          <div className="card text-center algeria-gradient text-white" id="finale">
            <div className="text-5xl mb-4 trophy-gold">🏆</div>
            <h3 className="text-xl font-bold mb-2">FINALE</h3>
            <p className="text-sm text-white/90 mb-4">
              18 janvier 2026 - 20:00
            </p>
            <div className="text-xs text-white/80">
              Le sacre du champion d'Afrique!
            </div>
          </div>
        </div>
      </section>

      {/* Back Link */}
      <div className="container-app mt-12 text-center">
        <Link href="/" className="btn-outline">
          ← Retour à l'accueil
        </Link>
      </div>
    </div>
  );
}
