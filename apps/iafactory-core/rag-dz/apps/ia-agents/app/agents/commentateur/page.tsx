'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';
import { Send, Trophy, TrendingUp, Target, Award } from 'lucide-react';

export default function CommentateurPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/commentateur',
  });

  const [streak, setStreak] = useState(12);
  const [pronosticAccuracy, setPronosticAccuracy] = useState(73);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <div className="container-app py-8">
        {/* Hero */}
        <div className="hero-gradient text-white rounded-2xl p-8 mb-8">
          <div className="flex items-start space-x-4">
            <div className="bg-white/20 backdrop-blur rounded-full p-4">
              <Trophy className="w-12 h-12" />
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-2">⚽ Hakim El Koora</h1>
              <p className="text-xl opacity-90 mb-4">
                Commentateur Sportif - Expert Tactique
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Analyses Tactiques
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Pronostics
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Histoire Fennecs 🇩🇿
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Ligue 1 DZ
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat */}
          <div className="lg:col-span-2">
            <div className="card h-[600px] flex flex-col">
              <div className="border-b border-slate-200 dark:border-slate-800 p-4">
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Analyses & Pronostics ⚽
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Tactique • Stats • Prédictions • Histoire du foot
                </p>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                  <div className="text-center py-12">
                    <Trophy className="w-16 h-16 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
                    <p className="text-slate-600 dark:text-slate-400 mb-2">
                      Ahla! Je suis Hakim El Koora ⚽
                    </p>
                    <p className="text-sm text-slate-500 mb-4">
                      Expert en tactique, pronostics et histoire des Fennecs! 🇩🇿
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-2xl mx-auto">
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  "Analyse tactique du dernier match de l'Algérie",
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-primary dark:hover:border-primary transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Analyse tactique
                        </div>
                        <div className="text-xs text-slate-500">
                          Formations, systèmes, points clés
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  'Pronostic Algérie vs Maroc pour la CAN 2025',
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-primary dark:hover:border-primary transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Pronostic match
                        </div>
                        <div className="text-xs text-slate-500">
                          Prédiction avec stats et analyse
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  "Raconte-moi le parcours de l'Algérie en CAN 2019",
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-primary dark:hover:border-primary transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Histoire Fennecs 🦊
                        </div>
                        <div className="text-xs text-slate-500">
                          Moments légendaires, joueurs
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  'Qui sont les meilleurs joueurs algériens à l\'étranger?',
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-primary dark:hover:border-primary transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Algériens à l'étranger
                        </div>
                        <div className="text-xs text-slate-500">
                          Mahrez, Bennacer, Slimani...
                        </div>
                      </button>
                    </div>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                          message.role === 'user'
                            ? 'bg-primary text-white'
                            : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white'
                        }`}
                      >
                        <div className="whitespace-pre-wrap">{message.content}</div>
                      </div>
                    </div>
                  ))
                )}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-4 py-3">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <form
                onSubmit={handleSubmit}
                className="border-t border-slate-200 dark:border-slate-800 p-4"
              >
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Pose ta question foot..."
                    className="input-field flex-1"
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || isLoading}
                    className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Sidebar Widgets */}
          <div className="space-y-6">
            {/* Pronostic Accuracy */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <Target className="w-6 h-6 text-primary" />
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  Précision Pronostics
                </h3>
              </div>
              <div className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600 dark:text-slate-400">Taux réussite</span>
                  <span className="font-bold text-primary">{pronosticAccuracy}%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${pronosticAccuracy}%` }}
                  ></div>
                </div>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Pronostics totaux</span>
                  <span className="text-primary font-medium">147</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Réussis</span>
                  <span className="text-green-600 font-medium">107</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Échoués</span>
                  <span className="text-red-600 font-medium">40</span>
                </div>
              </div>
            </div>

            {/* Streak */}
            <div className="card bg-gradient-to-br from-orange-500 to-red-600 text-white">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-bold">🔥 Streak Analyses</h3>
                <Award className="w-6 h-6" />
              </div>
              <div className="text-4xl font-bold mb-1">{streak} jours</div>
              <p className="text-sm opacity-90">
                Continue comme ça! Prochain badge à 15 jours
              </p>
            </div>

            {/* Formation Widget */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  Formation ALG 🇩🇿
                </h3>
              </div>
              <div className="bg-primary/10 rounded-lg p-4">
                <div className="text-center text-sm font-mono space-y-2">
                  <div className="text-slate-900 dark:text-white">Slimani</div>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="text-slate-900 dark:text-white">Mahrez</div>
                    <div className="text-slate-900 dark:text-white">Bennacer</div>
                    <div className="text-slate-900 dark:text-white">Brahimi</div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="text-slate-900 dark:text-white">Bentaleb</div>
                    <div className="text-slate-900 dark:text-white">Zeffane</div>
                  </div>
                  <div className="grid grid-cols-4 gap-1">
                    <div className="text-slate-900 dark:text-white text-xs">Bensebaini</div>
                    <div className="text-slate-900 dark:text-white text-xs">Mandi</div>
                    <div className="text-slate-900 dark:text-white text-xs">Benlamri</div>
                    <div className="text-slate-900 dark:text-white text-xs">Atal</div>
                  </div>
                  <div className="text-slate-900 dark:text-white">M'Bolhi</div>
                </div>
                <div className="text-center text-xs text-slate-600 dark:text-slate-400 mt-3">
                  Système: 4-2-3-1
                </div>
              </div>
            </div>

            {/* Stats Widget */}
            <div className="card">
              <h3 className="font-semibold text-slate-900 dark:text-white mb-4">
                📊 Stats Clés ALG
              </h3>
              <div className="space-y-3 text-sm">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Possession</span>
                    <span className="font-medium text-slate-900 dark:text-white">57%</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-1.5">
                    <div className="bg-primary h-1.5 rounded-full" style={{ width: '57%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Tirs cadrés/match</span>
                    <span className="font-medium text-slate-900 dark:text-white">5.8</span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Buts/match</span>
                    <span className="font-medium text-slate-900 dark:text-white">1.9</span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-600 dark:text-slate-400">Clean sheets</span>
                    <span className="font-medium text-slate-900 dark:text-white">42%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Premium */}
            <div className="card hero-gradient text-white">
              <h3 className="font-bold mb-2">🚀 Version Premium</h3>
              <p className="text-sm opacity-90 mb-4">
                Pronostics avancés + stats détaillées + analyses vidéo
              </p>
              <button className="w-full bg-white text-primary hover:bg-slate-100 font-semibold py-2 px-4 rounded-lg transition-colors">
                Passer Premium - 3000 DA/mois
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
