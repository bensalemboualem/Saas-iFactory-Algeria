'use client';

import Link from 'next/link';
import { Search, ArrowLeft, Sparkles, Zap, Star, Code, TrendingUp, FileText, Settings, BarChart3 } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { seoTools, getCriticalTools } from '@/lib/tools-data';

export default function SeoToolsPage() {
  // Grouper par sous-catégorie
  const researchTools = seoTools.filter(t => t.subcategory === 'research');
  const onPageTools = seoTools.filter(t => t.subcategory === 'on-page');
  const optimizationTools = seoTools.filter(t => t.subcategory === 'optimization');
  const technicalTools = seoTools.filter(t => t.subcategory === 'technical');
  const analysisTools = seoTools.filter(t => t.subcategory === 'analysis');

  // Stats
  const criticalTools = getCriticalTools(seoTools);
  const highPriorityTools = seoTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = seoTools.filter(t => t.priority === 'medium');
  const totalCredits = seoTools.reduce((acc, t) => acc + t.credits, 0);

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
          icon={Search}
          title="SEO & Optimisation"
          description={`${seoTools.length} outils IA pour dominer Google et booster votre trafic organique`}
          toolCount={seoTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-10">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{seoTools.length}</div>
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
            <div className="text-3xl font-bold text-green-600">{totalCredits}</div>
            <div className="text-sm text-gray-500">Crédits total</div>
          </div>
        </div>

        {/* Featured: Critical Tools */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-red-500" />
            <h2 className="text-xl font-semibold">Outils Critiques SEO</h2>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Essentiels
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour toute stratégie SEO</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
            ))}
          </div>
        </section>

        {/* Section Recherche de Mots-clés */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h2 className="text-xl font-semibold">Recherche de Mots-clés</h2>
            <span className="text-sm font-normal text-gray-500">
              ({researchTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Trouvez les meilleurs mots-clés pour votre niche et analysez la concurrence</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {researchTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
            ))}
          </div>
        </section>

        {/* Section On-Page */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-5 h-5 text-green-600" />
            <h2 className="text-xl font-semibold">Optimisation On-Page</h2>
            <span className="text-sm font-normal text-gray-500">
              ({onPageTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Meta tags, titres, URLs et structure de vos pages</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {onPageTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
            ))}
          </div>
        </section>

        {/* Section Optimisation */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-orange-600" />
            <h2 className="text-xl font-semibold">Analyse & Optimisation</h2>
            <span className="text-sm font-normal text-gray-500">
              ({optimizationTools.length + (analysisTools?.length || 0)} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Analysez et améliorez votre contenu pour un meilleur ranking</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[...optimizationTools, ...(analysisTools || [])].map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
            ))}
          </div>
        </section>

        {/* Section Technique */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Code className="w-5 h-5 text-purple-600" />
            <h2 className="text-xl font-semibold">SEO Technique</h2>
            <span className="text-sm font-normal text-gray-500">
              ({technicalTools.length} outils)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Schema markup, robots.txt, sitemap et configuration technique</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {technicalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
            ))}
          </div>
        </section>

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 border border-purple-100">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-purple-600" />
            Workflow SEO Recommandé
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Keyword Generator</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Longue Traîne</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Content Optimizer</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Meta Tags</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Schema Markup</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">6. Audit SEO</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow garantit un contenu parfaitement optimisé pour Google et les rich snippets.
          </p>
        </section>

        {/* Tips Section */}
        <section className="mb-10 bg-gradient-to-r from-green-50 to-teal-50 rounded-xl p-6 border border-green-100">
          <h3 className="font-semibold text-green-900 mb-3">Conseils SEO pour l'Algérie</h3>
          <ul className="text-sm text-green-800 space-y-2">
            <li>• Ciblez les mots-clés en français ET en arabe dialectal (darija)</li>
            <li>• Ajoutez des variantes locales : "Alger", "Oran", "Constantine", "DZD"</li>
            <li>• Utilisez le Schema LocalBusiness pour les entreprises algériennes</li>
            <li>• Optimisez pour mobile (80% du trafic en Algérie)</li>
          </ul>
        </section>

        {/* Tous les outils (grille complète) */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils SEO ({seoTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {seoTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/seo" />
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
