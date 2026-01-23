'use client';

import Link from 'next/link';
import { Briefcase, ArrowLeft, Sparkles, Star, FileText, Target, DollarSign, Megaphone, FileCheck, Zap, Users, ClipboardList, TrendingUp, Building2, Lightbulb, BarChart3 } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { businessTools, getCriticalTools } from '@/lib/tools-data';

export default function BusinessToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(businessTools);
  const highPriorityTools = businessTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = businessTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const planning = businessTools.filter(t => t.subcategory === 'planning');
  const strategy = businessTools.filter(t => t.subcategory === 'strategy');
  const fundraising = businessTools.filter(t => t.subcategory === 'fundraising');
  const marketing = businessTools.filter(t => t.subcategory === 'marketing');
  const documents = businessTools.filter(t => t.subcategory === 'documents');
  const productivity = businessTools.filter(t => t.subcategory === 'productivity');
  const hr = businessTools.filter(t => t.subcategory === 'hr');

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
          icon={Briefcase}
          title="Business & Startup"
          description={`${businessTools.length} outils IA pour lancer et développer votre entreprise`}
          toolCount={businessTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-7 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-indigo-600">{businessTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{planning.length}</div>
            <div className="text-sm text-gray-500">Planning</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{strategy.length}</div>
            <div className="text-sm text-gray-500">Stratégie</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">{fundraising.length}</div>
            <div className="text-sm text-gray-500">Fundraising</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-orange-600">{documents.length}</div>
            <div className="text-sm text-gray-500">Documents</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-pink-600">{hr.length}</div>
            <div className="text-sm text-gray-500">RH</div>
          </div>
        </div>

        {/* Banner Business */}
        <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Briefcase className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Lancez et Développez Votre Business</h3>
              <p className="opacity-90 mt-1">
                Business plans, pitch decks, analyses stratégiques, documents professionnels - Tout pour réussir votre startup.
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-indigo-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour tout entrepreneur</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
            ))}
          </div>
        </section>

        {/* Section Planning */}
        {planning.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <ClipboardList className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold">Planning & Business Plans</h2>
              <span className="text-sm font-normal text-gray-500">
                ({planning.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Business plans, résumés exécutifs et planification stratégique</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {planning.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section Stratégie */}
        {strategy.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Stratégie & Analyse</h2>
              <span className="text-sm font-normal text-gray-500">
                ({strategy.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">SWOT, analyse concurrentielle, buyer personas et propositions de valeur</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {strategy.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section Fundraising */}
        {fundraising.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <DollarSign className="w-5 h-5 text-green-600" />
              <h2 className="text-xl font-semibold">Fundraising & Pitch</h2>
              <span className="text-sm font-normal text-gray-500">
                ({fundraising.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Pitch decks et propositions de partenariat pour lever des fonds</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {fundraising.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section Marketing */}
        {marketing.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Megaphone className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold">Marketing & Communication</h2>
              <span className="text-sm font-normal text-gray-500">
                ({marketing.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Descriptions d'entreprise, mission/vision et communiqués de presse</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {marketing.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section Documents */}
        {documents.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <FileCheck className="w-5 h-5 text-emerald-600" />
              <h2 className="text-xl font-semibold">Documents Professionnels</h2>
              <span className="text-sm font-normal text-gray-500">
                ({documents.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Propositions commerciales, factures et contrats</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {documents.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section Productivité */}
        {productivity.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="w-5 h-5 text-cyan-600" />
              <h2 className="text-xl font-semibold">Productivité & KPIs</h2>
              <span className="text-sm font-normal text-gray-500">
                ({productivity.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">OKRs, KPIs, briefs projet et agendas de réunion</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {productivity.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Section RH */}
        {hr.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Users className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Ressources Humaines</h2>
              <span className="text-sm font-normal text-gray-500">
                ({hr.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Fiches de poste et checklists d'onboarding</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {hr.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-indigo-600" />
            Workflow Lancement Startup
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Business Plan</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Analyse SWOT</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Buyer Personas</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Pitch Deck</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. OKRs & KPIs</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow vous permet de structurer votre startup de l'idée au lancement avec tous les documents essentiels.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils Business ({businessTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {businessTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/business" />
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
