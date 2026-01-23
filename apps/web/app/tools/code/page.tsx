'use client';

import Link from 'next/link';
import { Code, ArrowLeft } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { LanguageSwitcher } from '@/components/LanguageSwitcher';
import { codeTools, getCriticalTools } from '@/lib/tools-data';
import { useI18n } from '@/lib/i18n';

export default function CodeToolsPage() {
  const { t, lang } = useI18n();
  const criticalTools = getCriticalTools(codeTools);

  // Grouper par subcategory
  const generation = codeTools.filter(t => t.subcategory === 'generation');
  const debugging = codeTools.filter(t => t.subcategory === 'debugging');

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
            <LanguageSwitcher />
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
          icon={Code}
          title={t('cat.code')}
          description={t('cat.code.desc')}
          toolCount={codeTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-cyan-600">{codeTools.length}</div>
            <div className="text-sm text-gray-500">{t('common.tools')} {t('common.total')}</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">{t('common.critical')}</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{generation.length}</div>
            <div className="text-sm text-gray-500">Generation</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{debugging.length}</div>
            <div className="text-sm text-gray-500">Debugging</div>
          </div>
        </div>

        {/* Banner */}
        <div className="bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Code className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">{t('banner.code')}</h3>
              <p className="opacity-90 mt-1">{t('banner.code.desc')}</p>
            </div>
          </div>
        </div>

        {/* All Tools */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Code className="w-6 h-6 text-cyan-600" />
            {t('page.tools.all')} ({codeTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {codeTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/code" lang={lang} />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            {t('footer.copyright')} - {t('cat.code')}
          </p>
        </div>
      </footer>
    </div>
  );
}
