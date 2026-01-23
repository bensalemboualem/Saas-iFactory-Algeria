'use client';

import Link from 'next/link';
import { Scale, ArrowLeft, Building, FileText, Landmark, Briefcase, Users, Receipt } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { juridiqueTools, getCriticalTools } from '@/lib/tools-data';

export default function JuridiqueToolsPage() {
  const criticalTools = getCriticalTools(juridiqueTools);

  // Grouper par subcategory
  const commerce = juridiqueTools.filter(t => t.subcategory === 'commerce');
  const creation = juridiqueTools.filter(t => t.subcategory === 'creation');
  const compliance = juridiqueTools.filter(t => t.subcategory === 'compliance');
  const investment = juridiqueTools.filter(t => t.subcategory === 'investment');
  const labor = juridiqueTools.filter(t => t.subcategory === 'labor');
  const tax = juridiqueTools.filter(t => t.subcategory === 'tax');

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
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
              🇩🇿 Exclusif Algerie
            </span>
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Credits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Header */}
        <CategoryHeader
          icon={Scale}
          title="Juridique Algerie"
          description={`${juridiqueTools.length} outils IA specialises droit algerien`}
          toolCount={juridiqueTools.length}
          criticalCount={criticalTools.length}
          isExclusive={true}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-slate-600">{juridiqueTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{creation.length}</div>
            <div className="text-sm text-gray-500">Creation</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">{tax.length}</div>
            <div className="text-sm text-gray-500">Fiscalite</div>
          </div>
        </div>

        {/* Banner Algerie */}
        <div className="bg-gradient-to-r from-green-600 via-green-500 to-emerald-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <span className="text-4xl">🇩🇿</span>
            </div>
            <div>
              <h3 className="font-bold text-xl">Droit des Affaires Algerien</h3>
              <p className="opacity-90 mt-1">
                Code de commerce, statuts SARL/SPA/EURL, fiscalite (TVA, IBS, IRG, TAP), droit du travail, ANDI.
              </p>
            </div>
          </div>
        </div>

        {/* All Tools */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Scale className="w-6 h-6 text-slate-600" />
            Tous les Outils Juridiques DZ ({juridiqueTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {juridiqueTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/juridique-dz" />
            ))}
          </div>
        </section>

        {/* Disclaimer */}
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-8">
          <p className="text-amber-800 text-sm">
            <strong>Avertissement:</strong> Ces outils fournissent des informations generales et ne constituent pas un avis juridique.
            Consultez un professionnel du droit pour des conseils specifiques a votre situation.
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Juridique Algerie 🇩🇿
          </p>
        </div>
      </footer>
    </div>
  );
}
