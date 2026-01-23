import Link from 'next/link';
import Countdown from './components/Countdown';
import { ALGERIA_MATCHES, GROUPS, getTeamById } from '@/data/can2025-data';

export default function Home() {
  return (
    <div className="py-8">
      {/* Hero Section with Countdown */}
      <section className="container-app mb-12">
        <Countdown />
      </section>

      {/* Quick Stats */}
      <section className="container-app mb-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card text-center fade-in">
            <div className="text-4xl mb-2">🏆</div>
            <div className="text-3xl font-bold text-primary">24</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Équipes</div>
          </div>
          <div className="card text-center fade-in fade-in-delay-1">
            <div className="text-4xl mb-2">⚽</div>
            <div className="text-3xl font-bold text-primary">36</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Matchs (Phase groupes)</div>
          </div>
          <div className="card text-center fade-in fade-in-delay-2">
            <div className="text-4xl mb-2">🇩🇿</div>
            <div className="text-3xl font-bold text-secondary">2×</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Champions (1990, 2019)</div>
          </div>
          <div className="card text-center fade-in fade-in-delay-3">
            <div className="text-4xl mb-2">🦊</div>
            <div className="text-3xl font-bold text-primary">E</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Groupe Algérie</div>
          </div>
        </div>
      </section>

      {/* Algeria Matches */}
      <section className="container-app mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center space-x-3">
            <span className="text-4xl">🇩🇿</span>
            <span>Matchs de l'Algérie</span>
          </h2>
          <Link href="/algerie" className="btn-primary">
            Hub Algérie →
          </Link>
        </div>

        <div className="space-y-4">
          {ALGERIA_MATCHES.map((match, index) => {
            const homeTeam = getTeamById(match.homeTeam);
            const awayTeam = getTeamById(match.awayTeam);

            return (
              <div key={match.id} className={`match-card fade-in fade-in-delay-${index + 1}`}>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-3">
                    <div className="text-sm text-slate-600 dark:text-slate-400">
                      {new Date(match.date).toLocaleDateString('fr-FR', {
                        weekday: 'long',
                        day: 'numeric',
                        month: 'long'
                      })} - {match.time}
                    </div>
                    <div className="badge badge-primary">Groupe E</div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 items-center">
                    {/* Home Team */}
                    <div className="text-center">
                      <div className="text-5xl mb-2">{homeTeam?.flag}</div>
                      <div className="font-bold text-slate-900 dark:text-white">
                        {homeTeam?.nameFr}
                      </div>
                    </div>

                    {/* VS */}
                    <div className="text-center">
                      <div className="text-2xl font-bold text-slate-400">VS</div>
                    </div>

                    {/* Away Team */}
                    <div className="text-center">
                      <div className="text-5xl mb-2">{awayTeam?.flag}</div>
                      <div className="font-bold text-slate-900 dark:text-white">
                        {awayTeam?.nameFr}
                      </div>
                    </div>
                  </div>

                  <div className="mt-3 text-sm text-slate-600 dark:text-slate-400 text-center">
                    🏟️ {match.stadium} ({match.city})
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 text-center">
          <Link href="/algerie" className="btn-outline">
            Voir tout sur l'Algérie 🇩🇿
          </Link>
        </div>
      </section>

      {/* All Groups Preview */}
      <section className="container-app mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
            Les 6 Groupes
          </h2>
          <Link href="/groupes" className="btn-primary">
            Classements →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {GROUPS.map((group, index) => (
            <div
              key={group.name}
              className={`card card-hover fade-in fade-in-delay-${index + 1}`}
            >
              <h3 className="text-2xl font-bold text-center mb-4 text-slate-900 dark:text-white">
                Groupe {group.name}
              </h3>
              <div className="space-y-3">
                {group.teams.map((teamId) => {
                  const team = getTeamById(teamId);
                  const isAlgeria = teamId === 'ALG';

                  return (
                    <div
                      key={teamId}
                      className={`flex items-center space-x-3 p-2 rounded-lg ${
                        isAlgeria
                          ? 'bg-primary/10 dark:bg-primary/20 font-bold'
                          : 'hover:bg-slate-50 dark:hover:bg-slate-800'
                      } transition-colors`}
                    >
                      <span className="text-3xl">{team?.flag}</span>
                      <span className="flex-1 text-slate-900 dark:text-white">
                        {team?.nameFr}
                      </span>
                      {isAlgeria && <span className="text-xl">⭐</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Quick Links */}
      <section className="container-app mb-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6 text-center">
          Navigation Rapide
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/algerie" className="card card-hover text-center group">
            <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">🇩🇿</div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Hub Algérie
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Matchs, effectif, statistiques, et toute l'actu des Fennecs
            </p>
          </Link>

          <Link href="/calendrier" className="card card-hover text-center group">
            <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">📅</div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Calendrier Complet
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Tous les matchs de la CAN 2025, phases de groupes et finales
            </p>
          </Link>

          <Link href="/groupes" className="card card-hover text-center group">
            <div className="text-6xl mb-4 group-hover:scale-110 transition-transform">🏆</div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Classements
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Groupes A à F, classements en direct, qualifications
            </p>
          </Link>
        </div>
      </section>

      {/* Fun Facts */}
      <section className="container-app">
        <div className="card algeria-gradient text-white">
          <h2 className="text-2xl font-bold mb-4 text-center">🦊 Le Savais-tu?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-4xl mb-2">🏆</div>
              <div className="text-3xl font-bold mb-1">1990</div>
              <div className="text-sm text-white/80">Premier titre CAN (Algérie)</div>
            </div>
            <div>
              <div className="text-4xl mb-2">⚽</div>
              <div className="text-3xl font-bold mb-1">2019</div>
              <div className="text-sm text-white/80">Deuxième titre (Égypte)</div>
            </div>
            <div>
              <div className="text-4xl mb-2">🌟</div>
              <div className="text-3xl font-bold mb-1">2025</div>
              <div className="text-sm text-white/80">Objectif: 3ème étoile!</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
