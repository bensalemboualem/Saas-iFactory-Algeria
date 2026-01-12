import Link from 'next/link';

const agents = [
  {
    id: 'motivation',
    name: 'Coach Motivation',
    persona: 'Amine',
    emoji: '💪',
    description: 'Ton coach bien-être quotidien. Gestion du stress, motivation, objectifs et développement personnel.',
    color: 'from-green-500 to-emerald-600',
    status: 'active',
    features: ['Mood Tracker', 'Breathing Exercises', 'Streaks', 'Achievements'],
  },
  {
    id: 'dev-helper',
    name: 'Dev Helper',
    persona: 'DevBot',
    emoji: '💻',
    description: 'Ton senior dev personnel. Debug, explications de code, optimisations et snippets prêts à copier.',
    color: 'from-blue-500 to-cyan-600',
    status: 'active',
    features: ['Debug rapide', 'Code Snippets', 'Optimisation', 'Best Practices'],
  },
  {
    id: 'tuteur-maths',
    name: 'Tuteur Maths',
    persona: 'Prof. Karim',
    emoji: '📐',
    description: 'Tuteur de maths collège à université. Explications étape par étape, préparation BEM/BAC.',
    color: 'from-purple-500 to-pink-600',
    status: 'active',
    features: ['Étape par étape', 'BEM/BAC', 'Formules', 'Programme DZ'],
  },
  {
    id: 'journaliste',
    name: 'Journaliste Pro',
    persona: 'Karim Khabari',
    emoji: '📰',
    description: 'Expert rédaction et fact-checking. Articles de qualité, vérification sources, optimisation SEO.',
    color: 'from-blue-600 to-blue-700',
    status: 'active',
    features: ['Rédaction', 'Fact-Checking', 'SEO', 'Déontologie'],
  },
  {
    id: 'commentateur',
    name: 'Commentateur Sport',
    persona: 'Hakim El Koora',
    emoji: '⚽',
    description: 'Expert foot algérien et mondial. Analyses tactiques, pronostics, histoire des Fennecs 🇩🇿',
    color: 'from-primary to-secondary',
    status: 'active',
    features: ['Tactique', 'Pronostics', 'Fennecs 🇩🇿', 'Stats'],
  },
];

export default function Home() {
  return (
    <div className="py-12 md:py-20">
      {/* Hero Section */}
      <section className="container-app mb-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            Agents IA Gratuits
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-8">
            Assistants intelligents conversationnels pour t'accompagner au quotidien.
            <br />
            <span className="text-primary font-semibold">100% gratuit</span> · Propulsé par Claude AI
          </p>

          <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-600 dark:text-slate-400">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🤖</span>
              <span>Conversations naturelles</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🇩🇿</span>
              <span>Adapté Algérie</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🔒</span>
              <span>Données privées</span>
            </div>
          </div>
        </div>
      </section>

      {/* Agents Grid */}
      <section className="container-app">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="card card-hover relative overflow-hidden"
            >
              {/* Gradient Background */}
              <div className={`absolute top-0 left-0 w-full h-2 bg-gradient-to-r ${agent.color}`}></div>

              {/* Status Badge */}
              {agent.status === 'coming-soon' && (
                <div className="absolute top-4 right-4">
                  <span className="badge badge-warning text-xs">Bientôt</span>
                </div>
              )}

              {/* Content */}
              <div className="relative pt-2">
                <div className="flex items-center space-x-3 mb-4">
                  <span className="text-5xl">{agent.emoji}</span>
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                      {agent.name}
                    </h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {agent.persona}
                    </p>
                  </div>
                </div>

                <p className="text-slate-600 dark:text-slate-400 mb-4">
                  {agent.description}
                </p>

                {/* Features */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {agent.features.map((feature) => (
                    <span key={feature} className="text-xs px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded-full text-slate-600 dark:text-slate-400">
                      {feature}
                    </span>
                  ))}
                </div>

                {/* CTA */}
                {agent.status === 'active' ? (
                  <Link
                    href={`/agents/${agent.id}`}
                    className="btn-primary w-full text-center inline-block"
                  >
                    Démarrer une conversation
                  </Link>
                ) : (
                  <button
                    disabled
                    className="w-full py-2 px-6 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-400 cursor-not-allowed"
                  >
                    Bientôt disponible
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="container-app mt-16">
        <div className="card bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <p className="text-3xl font-bold text-primary mb-2">3</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Agents IA</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-primary mb-2">100%</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Gratuit</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-primary mb-2">24/7</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Disponible</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-primary mb-2">🇩🇿</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Made in DZ</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
