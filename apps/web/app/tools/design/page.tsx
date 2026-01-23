'use client';

import Link from 'next/link';
import { Palette, ArrowLeft, Sparkles, Star, ImageIcon, Paintbrush, Layout, Share2, Megaphone, Search, Zap, Wand2, Camera, Layers } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { designTools, getCriticalTools } from '@/lib/tools-data';

export default function DesignToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(designTools);
  const highPriorityTools = designTools.filter(t => t.priority === 'high');

  // Grouper par subcategory
  const aiImage = designTools.filter(t => t.subcategory === 'ai_image');
  const branding = designTools.filter(t => t.subcategory === 'branding');
  const uiUx = designTools.filter(t => t.subcategory === 'ui_ux');
  const social = designTools.filter(t => t.subcategory === 'social');
  const marketing = designTools.filter(t => t.subcategory === 'marketing');
  const seo = designTools.filter(t => t.subcategory === 'seo');

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
              <span className="text-gray-500">Credits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Header */}
        <CategoryHeader
          icon={Palette}
          title="Images & Design"
          description={`${designTools.length} outils IA pour creer des visuels et designs professionnels`}
          toolCount={designTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-fuchsia-600">{designTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{aiImage.length}</div>
            <div className="text-sm text-gray-500">IA Image</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-pink-600">{branding.length}</div>
            <div className="text-sm text-gray-500">Branding</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{uiUx.length}</div>
            <div className="text-sm text-gray-500">UI/UX</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-orange-600">{marketing.length}</div>
            <div className="text-sm text-gray-500">Marketing</div>
          </div>
        </div>

        {/* Banner Design */}
        <div className="bg-gradient-to-r from-fuchsia-500 via-purple-500 to-pink-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Palette className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Creez des visuels epoustouflants avec l'IA</h3>
              <p className="opacity-90 mt-1">
                Prompts Midjourney, DALL-E, Stable Diffusion, logos, palettes de couleurs, UI/UX - Tout pour vos designs.
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-fuchsia-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-fuchsia-100 text-fuchsia-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour tout designer et createur de contenu</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
            ))}
          </div>
        </section>

        {/* Section IA Image */}
        {aiImage.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Wand2 className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Generation d'Images IA</h2>
              <span className="text-sm font-normal text-gray-500">
                ({aiImage.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Prompts optimises pour Midjourney, DALL-E et Stable Diffusion</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {aiImage.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Section Branding */}
        {branding.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Paintbrush className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Branding & Identite Visuelle</h2>
              <span className="text-sm font-normal text-gray-500">
                ({branding.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Logos, palettes de couleurs et guides de style</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {branding.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Section UI/UX */}
        {uiUx.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Layout className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold">UI/UX Design</h2>
              <span className="text-sm font-normal text-gray-500">
                ({uiUx.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Composants UI, icones et interfaces</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {uiUx.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Section Social */}
        {social.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Share2 className="w-5 h-5 text-cyan-600" />
              <h2 className="text-xl font-semibold">Visuels Social Media</h2>
              <span className="text-sm font-normal text-gray-500">
                ({social.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Miniatures YouTube, images pour reseaux sociaux et legendes</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {social.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Section Marketing */}
        {marketing.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Megaphone className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold">Marketing & Publicite</h2>
              <span className="text-sm font-normal text-gray-500">
                ({marketing.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Infographies, bannieres publicitaires et mockups produit</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {marketing.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Section SEO */}
        {seo.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Search className="w-5 h-5 text-green-600" />
              <h2 className="text-xl font-semibold">SEO Images</h2>
              <span className="text-sm font-normal text-gray-500">
                ({seo.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Textes alternatifs et optimisation pour les moteurs de recherche</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {seo.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggere */}
        <section className="mb-10 bg-gradient-to-r from-fuchsia-50 to-purple-50 rounded-xl p-6 border border-fuchsia-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-fuchsia-600" />
            Workflow Creation Visuelle Complete
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Logo Concept</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Palette Couleurs</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Guide de Style</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Prompts Midjourney</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Social Media Images</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow vous permet de creer une identite visuelle complete, de la conception du logo jusqu'aux visuels pour vos reseaux sociaux.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils Design ({designTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {designTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/design" />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Concu en Algerie
          </p>
        </div>
      </footer>
    </div>
  );
}
