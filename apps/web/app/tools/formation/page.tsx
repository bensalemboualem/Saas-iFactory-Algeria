'use client';

import Link from 'next/link';
import { BookOpen, ArrowLeft, GraduationCap, Brain, ClipboardList, HelpCircle, Languages, Layers } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { formationTools, getCriticalTools } from '@/lib/tools-data';

export default function FormationToolsPage() {
  const criticalTools = getCriticalTools(formationTools);
  const dzExclusive = formationTools.filter(t => t.isAlgeriaExclusive);

  return (
    <div className="min-h-screen bg-gray-50">
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
              <span className="text-gray-500">Credits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <CategoryHeader
          icon={BookOpen}
          title="Formation & Education"
          description={`${formationTools.length} outils IA pour apprendre et enseigner`}
          toolCount={formationTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-violet-600">{formationTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">{dzExclusive.length}</div>
            <div className="text-sm text-gray-500">Exclusif DZ</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">3</div>
            <div className="text-sm text-gray-500">Langues</div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <GraduationCap className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Apprenez Plus Efficacement</h3>
              <p className="opacity-90 mt-1">
                Tuteur IA personnalise, quiz, flashcards, aide aux devoirs et preparation BAC/BEM algerien.
              </p>
            </div>
          </div>
        </div>

        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-violet-600" />
            Tous les Outils Formation ({formationTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {formationTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/formation" />
            ))}
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-white py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">© 2026 IAFactory Algeria - Formation & Education</p>
        </div>
      </footer>
    </div>
  );
}
