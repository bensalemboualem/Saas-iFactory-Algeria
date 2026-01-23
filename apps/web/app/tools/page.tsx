'use client';

import Link from 'next/link';
import { useState } from 'react';
import {
  FileText, Search, Share2, Youtube, Mail, ShoppingCart,
  Building, GraduationCap, Sparkles, Briefcase, Palette,
  Code, BarChart3, Scale, Pen, BookOpen
} from 'lucide-react';
import { ToolCard, StatCard } from '@/components/tools/ToolCard';
import {
  blogTools, seoTools, adminDzTools, educationDzTools, youtubeTools, socialTools, emailTools, ecommerceTools, businessTools, designTools,
  codeTools, juridiqueTools, analyseTools, redactionTools, formationTools, creatifTools,
  categories, getAllTools
} from '@/lib/tools-data';

const categoryIcons: Record<string, any> = {
  blog: FileText,
  seo: Search,
  social: Share2,
  youtube: Youtube,
  email: Mail,
  ecommerce: ShoppingCart,
  business: Briefcase,
  design: Palette,
  code: Code,
  analyse: BarChart3,
  redaction: Pen,
  formation: BookOpen,
  creatif: Sparkles,
  'admin-dz': Building,
  'education-dz': GraduationCap,
  'juridique-dz': Scale,
};

const categoryColors: Record<string, string> = {
  blog: 'bg-blue-600',
  seo: 'bg-purple-600',
  social: 'bg-pink-600',
  youtube: 'bg-red-600',
  email: 'bg-orange-600',
  ecommerce: 'bg-green-600',
  business: 'bg-indigo-600',
  design: 'bg-fuchsia-600',
  code: 'bg-cyan-600',
  analyse: 'bg-amber-600',
  redaction: 'bg-sky-600',
  formation: 'bg-violet-600',
  creatif: 'bg-rose-600',
  'admin-dz': 'bg-emerald-600',
  'education-dz': 'bg-teal-600',
  'juridique-dz': 'bg-slate-600',
};

// Map des outils par catégorie
const toolsMap: Record<string, typeof blogTools> = {
  blog: blogTools,
  seo: seoTools,
  social: socialTools,
  youtube: youtubeTools,
  email: emailTools,
  ecommerce: ecommerceTools,
  business: businessTools,
  design: designTools,
  code: codeTools,
  analyse: analyseTools,
  redaction: redactionTools,
  formation: formationTools,
  creatif: creatifTools,
  'admin-dz': adminDzTools,
  'education-dz': educationDzTools,
  'juridique-dz': juridiqueTools,
};

export default function AllToolsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const allTools = getAllTools();

  // Filtrer par recherche
  const filteredBySearch = searchQuery
    ? allTools.filter(tool =>
        tool.name.fr.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.description.fr.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : null;

  // Stats
  const totalTools = allTools.length;
  const exclusiveTools = allTools.filter(t => t.isAlgeriaExclusive).length;
  const criticalTools = allTools.filter(t => t.priority === 'critical').length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-green-600">IAFactory</span>
            <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
          </Link>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
            <Link href="/pricing" className="text-gray-600 hover:text-gray-900">Tarifs</Link>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            <span className="text-green-600">{totalTools}+</span> Outils IA
          </h1>
          <p className="text-gray-600 text-lg">
            La plateforme IA la plus complète pour le marché algérien 🇩🇿
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <StatCard number={`${totalTools}+`} label="Outils IA" color="blue" />
          <StatCard number={`${categories.length}`} label="Catégories" color="purple" />
          <StatCard number="4" label="Langues" color="green" />
          <StatCard number={`${exclusiveTools}`} label="Exclusifs 🇩🇿" color="red" />
        </div>

        {/* Search */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="🔍 Rechercher un outil..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full max-w-xl px-4 py-3 rounded-xl border border-gray-200 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition text-lg"
          />
        </div>

        {/* Search Results */}
        {filteredBySearch && (
          <div className="mb-12">
            <h2 className="text-xl font-semibold mb-4">
              Résultats pour "{searchQuery}" ({filteredBySearch.length} outils)
            </h2>
            {filteredBySearch.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filteredBySearch.map(tool => (
                  <ToolCard key={tool.id} tool={tool} basePath={`/tools/${tool.category}`} />
                ))}
              </div>
            ) : (
              <p className="text-gray-500">Aucun outil trouvé pour cette recherche.</p>
            )}
          </div>
        )}

        {/* Categories with Preview (when not searching) */}
        {!filteredBySearch && (
          <>
            {/* Blog & Contenu */}
            <CategorySection
              category="blog"
              title="Blog & Contenu"
              description="Rédaction d'articles, humanisation, réécriture"
              tools={blogTools}
              isExclusive={false}
            />

            {/* SEO */}
            <CategorySection
              category="seo"
              title="SEO & Optimisation"
              description="Meta tags, mots-clés, analyse concurrents"
              tools={seoTools}
              isExclusive={false}
            />

            {/* Admin Algérie */}
            <CategorySection
              category="admin-dz"
              title="Admin Algérie"
              description="CNAS, CNRC, Sonelgaz, impôts et plus"
              tools={adminDzTools}
              isExclusive={true}
            />

            {/* Education Algérie */}
            <CategorySection
              category="education-dz"
              title="Éducation Algérie"
              description="Bac, BEM, révisions, QCM"
              tools={educationDzTools}
              isExclusive={true}
            />

            {/* YouTube & Vidéo */}
            <CategorySection
              category="youtube"
              title="YouTube & Vidéo"
              description="Titres, descriptions, scripts, miniatures, SEO vidéo"
              tools={youtubeTools}
              isExclusive={false}
            />

            {/* Social Media */}
            <CategorySection
              category="social"
              title="Social Media"
              description="Instagram, TikTok, LinkedIn, Twitter, Facebook, Pinterest"
              tools={socialTools}
              isExclusive={false}
            />

            {/* Email Marketing */}
            <CategorySection
              category="email"
              title="Email Marketing"
              description="Cold emails, newsletters, séquences, promotions, automation"
              tools={emailTools}
              isExclusive={false}
            />

            {/* E-commerce */}
            <CategorySection
              category="ecommerce"
              title="E-commerce"
              description="Fiches produit, publicités, SEO, conversion, service client"
              tools={ecommerceTools}
              isExclusive={false}
            />

            {/* Business & Startup */}
            <CategorySection
              category="business"
              title="Business & Startup"
              description="Business plans, pitch decks, analyses stratégiques, documents"
              tools={businessTools}
              isExclusive={false}
            />

            {/* Images & Design */}
            <CategorySection
              category="design"
              title="Images & Design"
              description="Prompts Midjourney, DALL-E, logos, palettes, UI/UX"
              tools={designTools}
              isExclusive={false}
            />

            {/* Code & Développement */}
            <CategorySection
              category="code"
              title="Code & Développement"
              description="Génération de code, debugging, SQL, tests, documentation"
              tools={codeTools}
              isExclusive={false}
            />

            {/* Analyse & Data */}
            <CategorySection
              category="analyse"
              title="Analyse & Data"
              description="Données Excel/CSV, dashboards, KPIs, ML, sentiment"
              tools={analyseTools}
              isExclusive={false}
            />

            {/* Juridique Algérie */}
            <CategorySection
              category="juridique-dz"
              title="Juridique Algérie"
              description="Code commerce, statuts SARL/SPA, fiscalité DZ, droit travail"
              tools={juridiqueTools}
              isExclusive={true}
            />

            {/* Rédaction */}
            <CategorySection
              category="redaction"
              title="Rédaction & Communication"
              description="Emails, traduction, correction, résumés, slogans, storytelling"
              tools={redactionTools}
              isExclusive={false}
            />

            {/* Formation */}
            <CategorySection
              category="formation"
              title="Formation & Éducation"
              description="Tuteur IA, quiz, flashcards, aide devoirs, prépa BAC/BEM"
              tools={formationTools}
              isExclusive={false}
            />

            {/* Créatif */}
            <CategorySection
              category="creatif"
              title="Créatif & Multimédia"
              description="Prompts image, écriture créative, scripts vidéo, paroles"
              tools={creatifTools}
              isExclusive={false}
            />
          </>
        )}
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

interface CategorySectionProps {
  category: string;
  title: string;
  description: string;
  tools: typeof blogTools;
  isExclusive: boolean;
}

function CategorySection({ category, title, description, tools, isExclusive }: CategorySectionProps) {
  const Icon = categoryIcons[category] || Sparkles;
  const bgColor = categoryColors[category] || 'bg-gray-600';
  const preview = tools.slice(0, 4);
  const criticalCount = tools.filter(t => t.priority === 'critical').length;

  return (
    <section className="mb-12">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 ${bgColor} rounded-xl flex items-center justify-center`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-gray-900">{title}</h2>
              {isExclusive && (
                <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-medium">
                  🇩🇿 Exclusif
                </span>
              )}
            </div>
            <p className="text-sm text-gray-500">{description}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium">
            {tools.length} outils
          </span>
          {criticalCount > 0 && (
            <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium">
              🔥 {criticalCount} populaires
            </span>
          )}
          <Link
            href={`/tools/${category}`}
            className="text-green-600 hover:text-green-700 font-medium text-sm"
          >
            Voir tout →
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {preview.map(tool => (
          <ToolCard key={tool.id} tool={tool} basePath={`/tools/${category}`} />
        ))}
      </div>
    </section>
  );
}

