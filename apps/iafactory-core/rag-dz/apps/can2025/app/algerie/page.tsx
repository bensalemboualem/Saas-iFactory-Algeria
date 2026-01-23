import Link from 'next/link';
import { ALGERIA_MATCHES, ALGERIA_SQUAD, getTeamById, GROUPS } from '@/data/can2025-data';

export default function AlgeriaPage() {
  const groupE = GROUPS.find(g => g.name === 'E');

  return (
    <div className="py-8">
      {/* Hero Section */}
      <section className="container-app mb-12">
        <div className="algeria-gradient text-white rounded-2xl p-8 md:p-12 shadow-2xl">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-center md:text-left mb-6 md:mb-0">
              <h1 className="text-5xl md:text-6xl font-bold mb-4 flex items-center justify-center md:justify-start space-x-4">
                <span className="text-7xl">🇩🇿</span>
                <span>LES FENNECS</span>
              </h1>
              <p className="text-xl md:text-2xl text-white/90 mb-2">
                Équipe Nationale d'Algérie
              </p>
              <p className="text-lg text-white/80">
                Champions d'Afrique 🏆 1990 · 2019
              </p>
            </div>
            <div className="text-center">
              <div className="text-6xl mb-3">🦊</div>
              <div className="text-4xl font-bold">Groupe E</div>
              <div className="text-sm text-white/80 mt-2">CAN 2025 - Maroc</div>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="container-app mb-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card text-center">
            <div className="text-4xl mb-2">🏆</div>
            <div className="text-3xl font-bold text-primary">{ALGERIA_SQUAD.titles.canWins}</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Titres CAN</div>
          </div>
          <div className="card text-center">
            <div className="text-4xl mb-2">⭐</div>
            <div className="text-3xl font-bold text-primary">{ALGERIA_SQUAD.titles.lastTitle}</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Dernier titre</div>
          </div>
          <div className="card text-center">
            <div className="text-4xl mb-2">⚽</div>
            <div className="text-3xl font-bold text-primary">3</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Matchs (Phase groupes)</div>
          </div>
          <div className="card text-center">
            <div className="text-4xl mb-2">🎯</div>
            <div className="text-3xl font-bold text-secondary">1/8</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Objectif minimum</div>
          </div>
        </div>
      </section>

      {/* Coaching Staff */}
      <section className="container-app mb-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">
          ⚡ Staff Technique
        </h2>
        <div className="card">
          <div className="flex items-center space-x-4 mb-4">
            <div className="text-5xl">👔</div>
            <div>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">
                {ALGERIA_SQUAD.coach}
              </div>
              <div className="text-slate-600 dark:text-slate-400">
                Sélectionneur National
              </div>
            </div>
          </div>
          <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg">
            <p className="text-sm text-slate-600 dark:text-slate-400">
              <strong>Capitaines:</strong> {ALGERIA_SQUAD.captains.join(', ')}
            </p>
          </div>
        </div>
      </section>

      {/* Matchs */}
      <section className="container-app mb-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6 flex items-center space-x-3">
          <span>📅</span>
          <span>Calendrier Algérie - Groupe E</span>
        </h2>

        <div className="space-y-6">
          {ALGERIA_MATCHES.map((match, index) => {
            const homeTeam = getTeamById(match.homeTeam);
            const awayTeam = getTeamById(match.awayTeam);
            const isFirstMatch = index === 0;

            return (
              <div
                key={match.id}
                className={`card ${isFirstMatch ? 'border-4 border-secondary' : ''}`}
              >
                {isFirstMatch && (
                  <div className="mb-4 flex items-center justify-center space-x-2 text-secondary font-bold">
                    <span>⚡</span>
                    <span>MATCH D'OUVERTURE ALGÉRIE</span>
                    <span>⚡</span>
                  </div>
                )}

                <div className="text-center mb-4">
                  <div className="text-lg font-semibold text-slate-900 dark:text-white mb-1">
                    {new Date(match.date).toLocaleDateString('fr-FR', {
                      weekday: 'long',
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </div>
                  <div className="text-2xl font-bold text-primary">{match.time}</div>
                </div>

                <div className="grid grid-cols-3 gap-4 items-center mb-4">
                  {/* Home Team (Algérie) */}
                  <div className="text-center">
                    <div className="text-6xl mb-3">{homeTeam?.flag}</div>
                    <div className="text-xl font-bold text-slate-900 dark:text-white">
                      {homeTeam?.nameFr}
                    </div>
                  </div>

                  {/* VS */}
                  <div className="text-center">
                    <div className="text-4xl font-bold text-slate-400 mb-2">VS</div>
                    <div className="badge badge-primary">Groupe E - Match {index + 1}</div>
                  </div>

                  {/* Away Team */}
                  <div className="text-center">
                    <div className="text-6xl mb-3">{awayTeam?.flag}</div>
                    <div className="text-xl font-bold text-slate-900 dark:text-white">
                      {awayTeam?.nameFr}
                    </div>
                  </div>
                </div>

                <div className="text-center p-4 bg-slate-50 dark:bg-slate-900 rounded-lg">
                  <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                    🏟️ <strong>{match.stadium}</strong>
                  </div>
                  <div className="text-sm text-slate-600 dark:text-slate-400">
                    📍 {match.city}, Maroc
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 p-6 bg-gradient-to-r from-primary/10 to-secondary/10 dark:from-primary/20 dark:to-secondary/20 rounded-xl border-2 border-primary/20">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3 flex items-center space-x-2">
            <span>🎯</span>
            <span>Objectif Phase de Groupes</span>
          </h3>
          <p className="text-slate-700 dark:text-slate-300 mb-3">
            Pour se qualifier aux 8èmes de finale, l'Algérie doit finir dans les <strong>2 premières places du Groupe E</strong>, ou être parmi les 4 meilleurs 3èmes.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
            <div className="p-3 bg-primary/10 dark:bg-primary/20 rounded-lg">
              <div className="font-bold text-primary mb-1">🥇 1er du groupe</div>
              <div className="text-slate-600 dark:text-slate-400">Qualification directe + meilleure position</div>
            </div>
            <div className="p-3 bg-primary/10 dark:bg-primary/20 rounded-lg">
              <div className="font-bold text-primary mb-1">🥈 2ème du groupe</div>
              <div className="text-slate-600 dark:text-slate-400">Qualification directe</div>
            </div>
            <div className="p-3 bg-yellow-500/10 dark:bg-yellow-500/20 rounded-lg">
              <div className="font-bold text-yellow-700 dark:text-yellow-500 mb-1">🥉 3ème (4 meilleurs)</div>
              <div className="text-slate-600 dark:text-slate-400">Repêchage possible</div>
            </div>
          </div>
        </div>
      </section>

      {/* Groupe E */}
      <section className="container-app mb-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">
          📊 Groupe E - Classement
        </h2>

        <div className="card overflow-x-auto">
          <table className="group-table">
            <thead>
              <tr>
                <th className="w-12">#</th>
                <th>Équipe</th>
                <th className="text-center">J</th>
                <th className="text-center">V</th>
                <th className="text-center">N</th>
                <th className="text-center">D</th>
                <th className="text-center">BP</th>
                <th className="text-center">BC</th>
                <th className="text-center">Diff</th>
                <th className="text-center font-bold">Pts</th>
              </tr>
            </thead>
            <tbody>
              {groupE?.teams.map((teamId, index) => {
                const team = getTeamById(teamId);
                const isAlgeria = teamId === 'ALG';

                return (
                  <tr key={teamId} className={isAlgeria ? 'algeria' : ''}>
                    <td className="font-bold">
                      {index + 1}
                      {isAlgeria && <span className="ml-2">🇩🇿</span>}
                    </td>
                    <td className="flex items-center space-x-2">
                      <span className="text-2xl">{team?.flag}</span>
                      <span>{team?.nameFr}</span>
                    </td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center font-bold">0</td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <div className="mt-4 text-xs text-slate-500 dark:text-slate-400">
            J = Joués | V = Victoires | N = Nuls | D = Défaites | BP = Buts pour | BC = Buts contre | Diff = Différence | Pts = Points
          </div>
        </div>
      </section>

      {/* Key Players */}
      <section className="container-app mb-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">
          ⭐ Joueurs Clés
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ALGERIA_SQUAD.keyPlayers.map((player, index) => (
            <div key={index} className="card card-hover">
              <div className="flex items-start space-x-4">
                <div className="text-4xl">⚽</div>
                <div className="flex-1">
                  <div className="text-xl font-bold text-slate-900 dark:text-white mb-1">
                    {player.name}
                  </div>
                  <div className="text-sm text-primary font-semibold mb-1">
                    {player.position}
                  </div>
                  <div className="text-sm text-slate-600 dark:text-slate-400">
                    🏟️ {player.club}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* History */}
      <section className="container-app">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">
          🏆 Palmarès CAN
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card algeria-gradient text-white">
            <div className="flex items-center space-x-4 mb-4">
              <div className="text-6xl trophy-gold">🏆</div>
              <div>
                <div className="text-3xl font-bold">1990</div>
                <div className="text-lg text-white/80">Alger, Algérie</div>
              </div>
            </div>
            <p className="text-sm text-white/90">
              Premier titre historique à domicile. L'Algérie bat le Nigeria 1-0 en finale.
            </p>
          </div>

          <div className="card algeria-gradient text-white">
            <div className="flex items-center space-x-4 mb-4">
              <div className="text-6xl trophy-gold">🏆</div>
              <div>
                <div className="text-3xl font-bold">2019</div>
                <div className="text-lg text-white/80">Le Caire, Égypte</div>
              </div>
            </div>
            <p className="text-sm text-white/90">
              Deuxième étoile! L'Algérie bat le Sénégal 1-0 en finale. Riyad Mahrez MVP du tournoi.
            </p>
          </div>
        </div>

        <div className="mt-6 card bg-gradient-to-br from-yellow-500/10 to-yellow-600/10 border-yellow-500/20">
          <div className="text-center">
            <div className="text-5xl mb-3">⭐⭐⭐</div>
            <div className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
              CAN 2025 - Objectif 3ème Étoile
            </div>
            <p className="text-slate-700 dark:text-slate-300">
              Les Fennecs visent un troisième sacre continental au Maroc!
            </p>
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
