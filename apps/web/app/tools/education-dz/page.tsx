'use client';

import Link from 'next/link';
import { GraduationCap, ArrowLeft } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { educationDzTools, getCriticalTools } from '@/lib/tools-data';

export default function EducationDzToolsPage() {
  const criticalCount = getCriticalTools(educationDzTools).length;

  // Grouper par niveau (matching actual slugs in tools-data.ts)
  const examTools = educationDzTools.filter(t =>
    ['revision-bac-algerie', 'preparation-bem-algerie', 'preparation-5eme-annee', 'preparation-concours-dz'].includes(t.slug)
  );
  const studyTools = educationDzTools.filter(t =>
    ['generateur-qcm-algerie', 'fiches-cours-algerie', 'exercices-corriges-algerie', 'aide-dissertation-algerie'].includes(t.slug)
  );
  const supportTools = educationDzTools.filter(t =>
    ['traducteur-academique-dz', 'orientation-universitaire-dz'].includes(t.slug)
  );

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
          icon={GraduationCap}
          title="Éducation Algérie"
          description="10 outils IA pour réussir vos examens (Bac, BEM, 5ème année)"
          toolCount={educationDzTools.length}
          criticalCount={criticalCount}
          isExclusive={true}
        />

        {/* Banner Exclusif */}
        <div className="bg-gradient-to-r from-teal-600 to-cyan-600 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <span className="text-4xl">🎓</span>
            <div>
              <h3 className="font-bold text-lg">Programme Algérien</h3>
              <p className="opacity-90">
                Tous les outils sont basés sur le programme officiel du Ministère de l'Éducation Nationale algérien.
                Parfait pour Bac, BEM et examens de 5ème année.
              </p>
            </div>
          </div>
        </div>

        {/* Section Examens */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            📝 Préparation aux Examens
            <span className="text-sm font-normal text-gray-500">
              ({examTools.length} outils)
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {examTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/education-dz" />
            ))}
          </div>
        </section>

        {/* Section Révisions */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            📚 Outils de Révision
            <span className="text-sm font-normal text-gray-500">
              ({studyTools.length} outils)
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {studyTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/education-dz" />
            ))}
          </div>
        </section>

        {/* Section Support */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            🧭 Orientation & Support
            <span className="text-sm font-normal text-gray-500">
              ({supportTools.length} outils)
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {supportTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/education-dz" />
            ))}
          </div>
        </section>

        {/* Filières Bac */}
        <section className="mb-10 bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="font-semibold text-lg mb-4">Filières Bac supportées</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="bg-blue-50 text-blue-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Sciences Expérimentales
            </div>
            <div className="bg-purple-50 text-purple-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Mathématiques
            </div>
            <div className="bg-green-50 text-green-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Technique Math
            </div>
            <div className="bg-orange-50 text-orange-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Gestion Économie
            </div>
            <div className="bg-red-50 text-red-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Lettres & Philo
            </div>
            <div className="bg-teal-50 text-teal-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Langues Étrangères
            </div>
            <div className="bg-pink-50 text-pink-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              Lettres & Langues
            </div>
            <div className="bg-gray-50 text-gray-700 px-3 py-2 rounded-lg text-sm font-medium text-center">
              + Autres
            </div>
          </div>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4">
            Tous les outils Éducation ({educationDzTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {educationDzTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/education-dz" />
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
