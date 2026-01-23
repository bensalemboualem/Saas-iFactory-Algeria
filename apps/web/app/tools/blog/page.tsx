'use client';

import Link from 'next/link';
import { FileText, ArrowLeft, Sparkles, Zap, Star } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { blogTools, getCriticalTools } from '@/lib/tools-data';

export default function BlogToolsPage() {
  // Grouper par sous-catégorie
  const writingTools = blogTools.filter(t => t.subcategory === 'writing');
  const rewritingTools = blogTools.filter(t => t.subcategory === 'rewriting');
  const optimizationTools = blogTools.filter(t => t.subcategory === 'optimization');
  const ideationTools = blogTools.filter(t => t.subcategory === 'ideation');

  // Stats
  const criticalTools = getCriticalTools(blogTools);
  const highPriorityTools = blogTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = blogTools.filter(t => t.priority === 'medium');
  const lowPriorityTools = blogTools.filter(t => t.priority === 'low');
  const totalCredits = blogTools.reduce((acc, t) => acc + t.credits, 0);

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
          icon={FileText}
          title="Blog & Rédaction"
          description={`${blogTools.length} outils IA pour créer du contenu qui se classe sur Google`}
          toolCount={blogTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-10">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{blogTools.length}</div>
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
            <div className="text-3xl font-bold text-green-600">{writingTools.length}</div>
            <div className="text-sm text-gray-500">Rédaction</div>
          </div>
        </div>

        {/* Featured: Critical Tools */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-red-500" />
            <h2 className="text-xl font-semibold">Outils Critiques</h2>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Essentiels
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils les plus utilisés pour la création de contenu</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Section Rédaction */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">✍️</span>
            <h2 className="text-xl font-semibold">Rédaction</h2>
            <span className="text-sm font-normal text-gray-500">
              ({writingTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Générez des articles complets, des sections, des introductions et conclusions</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {writingTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Section Réécriture & Humanisation */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">🔄</span>
            <h2 className="text-xl font-semibold">Réécriture & Humanisation</h2>
            <span className="text-sm font-normal text-gray-500">
              ({rewritingTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Transformez et améliorez votre contenu existant</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {rewritingTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Section Idéation */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">💡</span>
            <h2 className="text-xl font-semibold">Idéation & Planification</h2>
            <span className="text-sm font-normal text-gray-500">
              ({ideationTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Trouvez des idées et planifiez votre stratégie de contenu</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {ideationTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Section Optimisation */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">⚡</span>
            <h2 className="text-xl font-semibold">Optimisation</h2>
            <span className="text-sm font-normal text-gray-500">
              ({optimizationTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Améliorez et optimisez votre contenu</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {optimizationTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Section Moyenne Priorité - Nouveaux outils */}
        <section className="mb-10 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 border border-yellow-200">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">🔧</span>
            <h2 className="text-xl font-semibold">Outils Complémentaires</h2>
            <span className="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full text-xs font-medium">
              {mediumPriorityTools.length} outils
            </span>
          </div>
          <p className="text-gray-600 mb-4">Outils pratiques pour affiner et perfectionner votre contenu</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {mediumPriorityTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-600" />
            Workflow Recommandé
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Générateur de Sujets</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Générateur de Plan</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Rédacteur de Blog IA</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Humaniseur IA</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Correcteur Grammaire</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">6. Meta Description</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow complet produit du contenu SEO optimisé, corrigé et prêt à publier.
          </p>
        </section>

        {/* Tous les outils (grille complète) */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils Blog ({blogTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {blogTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/blog" />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria • Conçu en Algérie 🇩🇿
          </p>
        </div>
      </footer>
    </div>
  );
}
