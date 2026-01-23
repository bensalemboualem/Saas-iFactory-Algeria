'use client';

import Link from 'next/link';
import { Mail, ArrowLeft, Sparkles, Star, Send, FileText, GitBranch, Tag, MousePointer, RefreshCw, UserPlus, Target, Heart, Zap, Newspaper, ShoppingCart } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { emailTools, getCriticalTools } from '@/lib/tools-data';

export default function EmailToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(emailTools);
  const highPriorityTools = emailTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = emailTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const optimization = emailTools.filter(t => t.subcategory === 'optimization');
  const outreach = emailTools.filter(t => t.subcategory === 'outreach');
  const content = emailTools.filter(t => t.subcategory === 'content');
  const automation = emailTools.filter(t => t.subcategory === 'automation');
  const sales = emailTools.filter(t => t.subcategory === 'sales');
  const engagement = emailTools.filter(t => t.subcategory === 'engagement');

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
          icon={Mail}
          title="Email Marketing"
          description={`${emailTools.length} outils IA pour des campagnes email qui convertissent`}
          toolCount={emailTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-orange-600">{emailTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-amber-600">{highPriorityTools.length}</div>
            <div className="text-sm text-gray-500">Haute priorité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{automation.length}</div>
            <div className="text-sm text-gray-500">Automation</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">{sales.length}</div>
            <div className="text-sm text-gray-500">Ventes</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{outreach.length}</div>
            <div className="text-sm text-gray-500">Outreach</div>
          </div>
        </div>

        {/* Banner Email Marketing */}
        <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Mail className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Maîtrisez l'Email Marketing</h3>
              <p className="opacity-90 mt-1">
                Cold emails, newsletters, séquences automatisées, promotions - Créez des campagnes qui convertissent.
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-orange-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-orange-100 text-orange-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour tout email marketer</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
            ))}
          </div>
        </section>

        {/* Section Optimisation */}
        {optimization.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold">Optimisation</h2>
              <span className="text-sm font-normal text-gray-500">
                ({optimization.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Objets d'email, CTAs et signatures qui performent</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {optimization.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Section Outreach */}
        {outreach.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Send className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold">Outreach</h2>
              <span className="text-sm font-normal text-gray-500">
                ({outreach.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Cold emails, relances et emails d'excuses</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {outreach.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Section Contenu */}
        {content.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Newspaper className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Contenu</h2>
              <span className="text-sm font-normal text-gray-500">
                ({content.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Newsletters et invitations événement</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {content.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Section Automation */}
        {automation.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <GitBranch className="w-5 h-5 text-green-600" />
              <h2 className="text-xl font-semibold">Automation</h2>
              <span className="text-sm font-normal text-gray-500">
                ({automation.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Séquences email, bienvenue et milestones automatisés</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {automation.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Section Ventes */}
        {sales.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Tag className="w-5 h-5 text-emerald-600" />
              <h2 className="text-xl font-semibold">Ventes</h2>
              <span className="text-sm font-normal text-gray-500">
                ({sales.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Emails promotionnels, panier abandonné et lancement produit</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {sales.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Section Engagement */}
        {engagement.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Heart className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Engagement</h2>
              <span className="text-sm font-normal text-gray-500">
                ({engagement.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Ré-engagement, témoignages, parrainage et remerciements</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {engagement.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl p-6 border border-orange-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-orange-600" />
            Workflow Email Marketing Complet
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Objet accrocheur</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Email de bienvenue</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Séquence nurture</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Email promotionnel</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Relance intelligente</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow vous permet de convertir des prospects en clients fidèles avec des emails au bon moment.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils Email Marketing ({emailTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {emailTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/email" />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Conçu en Algérie
          </p>
        </div>
      </footer>
    </div>
  );
}
