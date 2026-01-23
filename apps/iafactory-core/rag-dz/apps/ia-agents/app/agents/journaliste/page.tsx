'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';
import { Send, Newspaper, CheckCircle, Search, TrendingUp } from 'lucide-react';

export default function JournalistePage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/journaliste',
  });

  const [factCheckScore, setFactCheckScore] = useState(85);
  const [seoScore, setSeoScore] = useState(92);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <div className="container-app py-8">
        {/* Hero */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-2xl p-8 mb-8">
          <div className="flex items-start space-x-4">
            <div className="bg-white/20 backdrop-blur rounded-full p-4">
              <Newspaper className="w-12 h-12" />
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-2">📰 Karim Khabari</h1>
              <p className="text-xl opacity-90 mb-4">
                Journaliste Professionnel - Mentor en Rédaction
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Investigation
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Fact-Checking
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  SEO
                </span>
                <span className="bg-white/20 backdrop-blur px-3 py-1 rounded-full text-sm">
                  Déontologie
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
                  Assistant Rédaction
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Rédaction • Fact-checking • SEO • Déontologie
                </p>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                  <div className="text-center py-12">
                    <Newspaper className="w-16 h-16 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
                    <p className="text-slate-600 dark:text-slate-400 mb-2">
                      Bonjour! Je suis Karim Khabari 📰
                    </p>
                    <p className="text-sm text-slate-500 mb-4">
                      Comment puis-je t'aider dans ta rédaction aujourd'hui?
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-2xl mx-auto">
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  "J'ai besoin d'aide pour écrire un article sur l'inflation en Algérie",
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Rédiger un article
                        </div>
                        <div className="text-xs text-slate-500">
                          Structure et conseils de rédaction
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  'Comment fact-checker une information sur les réseaux sociaux?',
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Fact-checking
                        </div>
                        <div className="text-xs text-slate-500">
                          Vérifier sources et informations
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  'Comment optimiser mon article pour le SEO?',
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Optimisation SEO
                        </div>
                        <div className="text-xs text-slate-500">
                          Keywords, meta tags, structure
                        </div>
                      </button>
                      <button
                        onClick={() =>
                          handleSubmit({
                            preventDefault: () => {},
                            currentTarget: {
                              message: {
                                value:
                                  'Quelles sont les règles déontologiques pour citer une source?',
                              },
                            },
                          } as any)
                        }
                        className="text-left p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:border-blue-500 dark:hover:border-blue-500 transition-colors"
                      >
                        <div className="font-medium text-sm text-slate-900 dark:text-white">
                          Déontologie
                        </div>
                        <div className="text-xs text-slate-500">
                          Éthique et bonnes pratiques
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
                            ? 'bg-blue-600 text-white'
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
                    placeholder="Pose ta question journalistique..."
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
            {/* Fact-Check Score */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <CheckCircle className="w-6 h-6 text-green-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  Fact-Check Score
                </h3>
              </div>
              <div className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600 dark:text-slate-400">Fiabilité</span>
                  <span className="font-bold text-green-600">{factCheckScore}%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${factCheckScore}%` }}
                  ></div>
                </div>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">
                    Sources vérifiées
                  </span>
                  <span className="text-green-600 font-medium">4/5</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">
                    Citations correctes
                  </span>
                  <span className="text-green-600 font-medium">✓</span>
                </div>
              </div>
            </div>

            {/* SEO Score */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  SEO Score
                </h3>
              </div>
              <div className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600 dark:text-slate-400">
                    Optimisation
                  </span>
                  <span className="font-bold text-blue-600">{seoScore}%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${seoScore}%` }}
                  ></div>
                </div>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Keywords</span>
                  <span className="text-blue-600 font-medium">✓</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Meta tags</span>
                  <span className="text-blue-600 font-medium">✓</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">
                    Structure H1-H3
                  </span>
                  <span className="text-blue-600 font-medium">✓</span>
                </div>
              </div>
            </div>

            {/* Sources Citées */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <Search className="w-6 h-6 text-purple-500" />
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  Sources Citées
                </h3>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-1.5"></div>
                  <div>
                    <div className="font-medium text-slate-900 dark:text-white">
                      El Watan (3)
                    </div>
                    <div className="text-slate-500">Fiabilité: 90%</div>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-1.5"></div>
                  <div>
                    <div className="font-medium text-slate-900 dark:text-white">
                      TSA (2)
                    </div>
                    <div className="text-slate-500">Fiabilité: 85%</div>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-1.5"></div>
                  <div>
                    <div className="font-medium text-slate-900 dark:text-white">
                      Réseaux sociaux (1)
                    </div>
                    <div className="text-slate-500">Fiabilité: 50%</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Premium */}
            <div className="card bg-gradient-to-br from-blue-600 to-blue-700 text-white">
              <h3 className="font-bold mb-2">🚀 Version Premium</h3>
              <p className="text-sm opacity-90 mb-4">
                Accès illimité + fact-checking automatique + SEO avancé
              </p>
              <button className="w-full bg-white text-blue-600 hover:bg-slate-100 font-semibold py-2 px-4 rounded-lg transition-colors">
                Passer Premium - 3500 DA/mois
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
