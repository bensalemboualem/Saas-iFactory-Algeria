'use client';

import Link from 'next/link';
import { Youtube, ArrowLeft, Sparkles, Star, Search, ScrollText, MessageCircle, TrendingUp, Lightbulb, Play, Zap } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { youtubeTools, getCriticalTools } from '@/lib/tools-data';

export default function YoutubeToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(youtubeTools);
  const highPriorityTools = youtubeTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = youtubeTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const optimization = youtubeTools.filter(t => t.subcategory === 'optimization');
  const content = youtubeTools.filter(t => t.subcategory === 'content');
  const engagement = youtubeTools.filter(t => t.subcategory === 'engagement');
  const strategy = youtubeTools.filter(t => t.subcategory === 'strategy');
  const ideation = youtubeTools.filter(t => t.subcategory === 'ideation');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Header */}
        <CategoryHeader
          icon={Youtube}
          title="YouTube & Vidéo"
          description={`${youtubeTools.length} outils IA pour créer du contenu YouTube viral et optimisé`}
          toolCount={youtubeTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{youtubeTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-orange-600">{highPriorityTools.length}</div>
            <div className="text-sm text-gray-500">Haute priorité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-yellow-600">{mediumPriorityTools.length}</div>
            <div className="text-sm text-gray-500">Moyenne priorité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{content.length}</div>
            <div className="text-sm text-gray-500">Création</div>
          </div>
        </div>

        {/* Banner YouTube */}
        <div className="bg-gradient-to-r from-red-600 to-red-700 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Youtube className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Dominez YouTube avec l'IA</h3>
              <p className="opacity-90 mt-1">
                Titres accrocheurs, descriptions SEO, scripts engageants, miniatures cliquables.
                Tout ce qu'il faut pour faire décoller votre chaîne !
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-red-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour chaque vidéo</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>

        {/* Section Optimisation SEO */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Search className="w-5 h-5 text-red-600" />
            <h2 className="text-xl font-semibold">Optimisation SEO</h2>
            <span className="text-sm font-normal text-gray-500">
              ({optimization.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Titres, descriptions, tags et miniatures pour maximiser la visibilité</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {optimization.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>

        {/* Section Création de Contenu */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <ScrollText className="w-5 h-5 text-blue-600" />
            <h2 className="text-xl font-semibold">Création de Contenu</h2>
            <span className="text-sm font-normal text-gray-500">
              ({content.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Scripts, hooks, intros et autres contenus vidéo</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {content.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>

        {/* Section Engagement */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <MessageCircle className="w-5 h-5 text-green-600" />
            <h2 className="text-xl font-semibold">Engagement</h2>
            <span className="text-sm font-normal text-gray-500">
              ({engagement.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Commentaires, posts communauté et interactions</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {engagement.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>

        {/* Section Stratégie */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            <h2 className="text-xl font-semibold">Stratégie & Croissance</h2>
            <span className="text-sm font-normal text-gray-500">
              ({strategy.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Audits, monétisation, partenariats et analytics</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {strategy.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>

        {/* Section Idéation */}
        {ideation.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="w-5 h-5 text-yellow-600" />
              <h2 className="text-xl font-semibold">Idéation</h2>
              <span className="text-sm font-normal text-gray-500">
                ({ideation.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Trouver des idées de vidéos et de niches</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {ideation.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-red-50 to-orange-50 rounded-xl p-6 border border-red-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-red-600" />
            Workflow Publication Vidéo
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Idées de Contenu</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Script Complet</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Hook Accrocheur</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Titre Optimisé</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Description SEO</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">6. Tags + Miniature</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow garantit une vidéo optimisée de A à Z pour maximiser vues et engagement.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils YouTube ({youtubeTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {youtubeTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/youtube" />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria • Conçu en Algérie
          </p>
        </div>
      </footer>
    </div>
  );
}
