'use client';

import Link from 'next/link';
import { ShoppingCart, ArrowLeft, Sparkles, Star, Package, Megaphone, Search, TrendingUp, Headphones, FileText, Building, Zap, Truck, RotateCcw, Tag } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { ecommerceTools, getCriticalTools } from '@/lib/tools-data';

export default function EcommerceToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(ecommerceTools);
  const highPriorityTools = ecommerceTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = ecommerceTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const product = ecommerceTools.filter(t => t.subcategory === 'product');
  const advertising = ecommerceTools.filter(t => t.subcategory === 'advertising');
  const seo = ecommerceTools.filter(t => t.subcategory === 'seo');
  const conversion = ecommerceTools.filter(t => t.subcategory === 'conversion');
  const customerService = ecommerceTools.filter(t => t.subcategory === 'customer_service');
  const legal = ecommerceTools.filter(t => t.subcategory === 'legal');
  const b2b = ecommerceTools.filter(t => t.subcategory === 'b2b');

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
          icon={ShoppingCart}
          title="E-commerce"
          description={`${ecommerceTools.length} outils IA pour booster vos ventes en ligne`}
          toolCount={ecommerceTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-7 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">{ecommerceTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{product.length}</div>
            <div className="text-sm text-gray-500">Produits</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600">{advertising.length}</div>
            <div className="text-sm text-gray-500">Publicité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-amber-600">{conversion.length}</div>
            <div className="text-sm text-gray-500">Conversion</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-pink-600">{customerService.length}</div>
            <div className="text-sm text-gray-500">Service Client</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-gray-600">{legal.length}</div>
            <div className="text-sm text-gray-500">Légal</div>
          </div>
        </div>

        {/* Banner E-commerce */}
        <div className="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <ShoppingCart className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Boostez vos ventes en ligne</h3>
              <p className="opacity-90 mt-1">
                Fiches produit, publicités, SEO, conversion, service client - Tout pour réussir votre e-commerce.
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-green-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour tout e-commerçant</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
            ))}
          </div>
        </section>

        {/* Section Fiches Produit */}
        {product.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Package className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold">Fiches Produit</h2>
              <span className="text-sm font-normal text-gray-500">
                ({product.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Descriptions, titres, collections et comparatifs</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {product.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section Publicité */}
        {advertising.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Megaphone className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Publicité</h2>
              <span className="text-sm font-normal text-gray-500">
                ({advertising.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Facebook Ads, Google Ads, lancements et promos</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {advertising.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section SEO E-commerce */}
        {seo.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Search className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold">SEO E-commerce</h2>
              <span className="text-sm font-normal text-gray-500">
                ({seo.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Optimisation produits et marketplaces</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {seo.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section Conversion */}
        {conversion.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <h2 className="text-xl font-semibold">Conversion</h2>
              <span className="text-sm font-normal text-gray-500">
                ({conversion.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Upsell, cross-sell, popups et fidélité</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {conversion.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section Service Client */}
        {customerService.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Headphones className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Service Client</h2>
              <span className="text-sm font-normal text-gray-500">
                ({customerService.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Réponses avis, FAQ, guides et Q&A</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {customerService.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section Légal */}
        {legal.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-gray-600" />
              <h2 className="text-xl font-semibold">Légal</h2>
              <span className="text-sm font-normal text-gray-500">
                ({legal.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Politiques de livraison et retour</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {legal.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Section B2B */}
        {b2b.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Building className="w-5 h-5 text-indigo-600" />
              <h2 className="text-xl font-semibold">B2B / Wholesale</h2>
              <span className="text-sm font-normal text-gray-500">
                ({b2b.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Fournisseurs et vente en gros</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {b2b.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-green-600" />
            Workflow Lancement Produit E-commerce
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Fiche produit</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. SEO produit</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Ads Facebook/Google</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Upsell/Cross-sell</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. FAQ + Avis</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow vous permet de lancer un produit avec tous les éléments pour maximiser les conversions.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils E-commerce ({ecommerceTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {ecommerceTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/ecommerce" />
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
