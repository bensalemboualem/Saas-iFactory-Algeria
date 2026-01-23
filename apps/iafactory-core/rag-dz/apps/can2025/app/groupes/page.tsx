import Link from 'next/link';
import { GROUPS, getTeamById } from '@/data/can2025-data';

export default function GroupesPage() {
  return (
    <div className="py-8">
      {/* Hero */}
      <section className="container-app mb-12">
        <div className="text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
            📊 Groupes & Classements
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Phase de groupes - CAN 2025 Maroc
          </p>
        </div>
      </section>

      {/* Qualification Rules */}
      <section className="container-app mb-12">
        <div className="card bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4 flex items-center space-x-2">
            <span>🎯</span>
            <span>Règles de Qualification</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="p-4 bg-white dark:bg-slate-800 rounded-lg">
              <div className="font-bold text-primary mb-2">🥇 1er & 2ème de chaque groupe</div>
              <div className="text-slate-600 dark:text-slate-400">
                Qualification directe aux 8èmes de finale (12 équipes)
              </div>
            </div>
            <div className="p-4 bg-white dark:bg-slate-800 rounded-lg">
              <div className="font-bold text-yellow-600 mb-2">🥉 4 meilleurs 3èmes</div>
              <div className="text-slate-600 dark:text-slate-400">
                Repêchage pour compléter le tableau des 8èmes (4 équipes)
              </div>
            </div>
            <div className="p-4 bg-white dark:bg-slate-800 rounded-lg">
              <div className="font-bold text-slate-600 dark:text-slate-400 mb-2">❌ Autres</div>
              <div className="text-slate-600 dark:text-slate-400">
                Élimination (8 équipes)
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* All Groups */}
      <section className="container-app">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {GROUPS.map((group) => {
            const hasAlgeria = group.teams.includes('ALG');

            return (
              <div key={group.name} className="space-y-4">
                <div className={`card ${hasAlgeria ? 'border-4 border-primary' : ''}`}>
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
                      Groupe {group.name}
                    </h2>
                    {hasAlgeria && (
                      <div className="flex items-center space-x-2 bg-primary/10 dark:bg-primary/20 px-4 py-2 rounded-full">
                        <span className="text-2xl">🇩🇿</span>
                        <span className="font-bold text-primary">Algérie</span>
                      </div>
                    )}
                  </div>

                  <div className="overflow-x-auto">
                    <table className="group-table">
                      <thead>
                        <tr>
                          <th className="w-12">#</th>
                          <th>Équipe</th>
                          <th className="text-center">J</th>
                          <th className="text-center">V</th>
                          <th className="text-center">N</th>
                          <th className="text-center">D</th>
                          <th className="text-center">Diff</th>
                          <th className="text-center font-bold">Pts</th>
                        </tr>
                      </thead>
                      <tbody>
                        {group.teams.map((teamId, index) => {
                          const team = getTeamById(teamId);
                          const isAlgeria = teamId === 'ALG';

                          return (
                            <tr key={teamId} className={isAlgeria ? 'algeria' : ''}>
                              <td className="font-bold">
                                {index + 1}
                                {index < 2 && <span className="ml-1 text-primary">✓</span>}
                              </td>
                              <td>
                                <div className="flex items-center space-x-2">
                                  <span className="text-2xl">{team?.flag}</span>
                                  <span className={isAlgeria ? 'font-bold' : ''}>
                                    {team?.nameFr}
                                  </span>
                                </div>
                              </td>
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
                  </div>

                  <div className="mt-4 text-xs text-slate-500 dark:text-slate-400 flex items-center justify-between">
                    <span>J = Joués | V = Victoires | N = Nuls | D = Défaites | Diff = Différence | Pts = Points</span>
                    {hasAlgeria && (
                      <Link href="/algerie" className="text-primary hover:underline font-semibold">
                        Voir tout sur l'Algérie →
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div className="mt-8 card bg-slate-50 dark:bg-slate-900">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
            📋 Légende
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <span className="text-primary font-bold text-xl">✓</span>
              <span className="text-slate-700 dark:text-slate-300">
                Qualifié pour les 8èmes (1er et 2ème)
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="bg-primary/10 dark:bg-primary/20 px-3 py-1 rounded font-bold text-primary">
                🇩🇿
              </span>
              <span className="text-slate-700 dark:text-slate-300">
                Équipe d'Algérie
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600 font-bold text-xl">🥉</span>
              <span className="text-slate-700 dark:text-slate-300">
                Repêchage possible (meilleurs 3èmes)
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Best Third Places */}
      <section className="container-app mt-12">
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6 text-center">
          🥉 Meilleurs Troisièmes (Repêchage)
        </h2>

        <div className="card">
          <p className="text-center text-slate-600 dark:text-slate-400 mb-6">
            Les 4 meilleures équipes classées 3ème se qualifient également pour les 8èmes de finale.
            <br />
            <span className="text-sm">Classement selon: Points → Différence de buts → Buts marqués → Fair-play</span>
          </p>

          <div className="overflow-x-auto">
            <table className="group-table">
              <thead>
                <tr>
                  <th className="w-12">#</th>
                  <th>Équipe</th>
                  <th className="text-center">Groupe</th>
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
                {[1, 2, 3, 4, 5, 6].map((position) => (
                  <tr key={position} className={position <= 4 ? 'bg-yellow-50 dark:bg-yellow-900/10' : ''}>
                    <td className="font-bold">
                      {position}
                      {position <= 4 && <span className="ml-1 text-yellow-600">✓</span>}
                    </td>
                    <td className="text-slate-400">-</td>
                    <td className="text-center text-slate-400">-</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center">0</td>
                    <td className="text-center font-bold">0</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/10 rounded-lg">
            <div className="flex items-start space-x-2 text-sm text-slate-700 dark:text-slate-300">
              <span className="text-yellow-600 font-bold">⚠️</span>
              <p>
                <strong>Important:</strong> Ce classement sera mis à jour après chaque journée de matchs.
                Les 4 premières équipes (surlignées en jaune) se qualifient pour les 8èmes de finale.
              </p>
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
