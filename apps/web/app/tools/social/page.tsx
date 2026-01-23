'use client';

import Link from 'next/link';
import { Share2, ArrowLeft, Sparkles, Star, Instagram, Linkedin, Twitter, Facebook, Hash, Calendar, TrendingUp, Megaphone, MessageCircle, Zap, Music, Image } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { socialTools, getCriticalTools } from '@/lib/tools-data';

export default function SocialToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(socialTools);
  const highPriorityTools = socialTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = socialTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const instagram = socialTools.filter(t => t.subcategory === 'instagram');
  const tiktok = socialTools.filter(t => t.subcategory === 'tiktok');
  const linkedin = socialTools.filter(t => t.subcategory === 'linkedin');
  const twitter = socialTools.filter(t => t.subcategory === 'twitter');
  const facebook = socialTools.filter(t => t.subcategory === 'facebook');
  const pinterest = socialTools.filter(t => t.subcategory === 'pinterest');
  const strategy = socialTools.filter(t => t.subcategory === 'strategy');
  const advertising = socialTools.filter(t => t.subcategory === 'advertising');
  const messaging = socialTools.filter(t => t.subcategory === 'messaging');

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
          icon={Share2}
          title="Social Media"
          description={`${socialTools.length} outils IA pour dominer tous les réseaux sociaux`}
          toolCount={socialTools.length}
          criticalCount={criticalTools.length}
          isExclusive={false}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-pink-600">{socialTools.length}</div>
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
            <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">{instagram.length}</div>
            <div className="text-sm text-gray-500">Instagram</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-blue-600">{linkedin.length}</div>
            <div className="text-sm text-gray-500">LinkedIn</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-black">{tiktok.length}</div>
            <div className="text-sm text-gray-500">TikTok</div>
          </div>
        </div>

        {/* Banner Social Media */}
        <div className="bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-xl flex items-center justify-center">
              <Share2 className="w-10 h-10 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-xl">Maîtrisez tous les réseaux sociaux</h3>
              <p className="opacity-90 mt-1">
                Instagram, TikTok, LinkedIn, Twitter, Facebook, Pinterest - Créez du contenu viral qui convertit.
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-pink-500" />
            <h2 className="text-xl font-semibold">Outils Essentiels</h2>
            <span className="bg-pink-100 text-pink-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Must-Have
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les outils indispensables pour chaque social media manager</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
            ))}
          </div>
        </section>

        {/* Section Instagram */}
        {instagram.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Instagram className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Instagram</h2>
              <span className="text-sm font-normal text-gray-500">
                ({instagram.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Légendes, hashtags, bios, stories et Reels</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {instagram.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section TikTok */}
        {tiktok.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Music className="w-5 h-5 text-black" />
              <h2 className="text-xl font-semibold">TikTok</h2>
              <span className="text-sm font-normal text-gray-500">
                ({tiktok.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Captions virales et hashtags pour la FYP</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {tiktok.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section LinkedIn */}
        {linkedin.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Linkedin className="w-5 h-5 text-blue-700" />
              <h2 className="text-xl font-semibold">LinkedIn</h2>
              <span className="text-sm font-normal text-gray-500">
                ({linkedin.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Posts professionnels, headlines et résumés qui convertissent</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {linkedin.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Twitter/X */}
        {twitter.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Twitter className="w-5 h-5 text-sky-500" />
              <h2 className="text-xl font-semibold">Twitter / X</h2>
              <span className="text-sm font-normal text-gray-500">
                ({twitter.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Threads viraux et bios percutantes</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {twitter.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Facebook */}
        {facebook.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Facebook className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold">Facebook</h2>
              <span className="text-sm font-normal text-gray-500">
                ({facebook.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Posts pour pages, groupes et profils</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {facebook.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Pinterest */}
        {pinterest.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Image className="w-5 h-5 text-red-600" />
              <h2 className="text-xl font-semibold">Pinterest</h2>
              <span className="text-sm font-normal text-gray-500">
                ({pinterest.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Pins SEO-optimisés pour du trafic continu</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {pinterest.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Stratégie */}
        {strategy.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Stratégie & Planification</h2>
              <span className="text-sm font-normal text-gray-500">
                ({strategy.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Calendriers, audits, rapports et optimisation</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {strategy.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Publicité */}
        {advertising.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Megaphone className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold">Publicité Social</h2>
              <span className="text-sm font-normal text-gray-500">
                ({advertising.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Copies publicitaires pour Facebook, Instagram et TikTok Ads</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {advertising.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Section Messaging */}
        {messaging.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <MessageCircle className="w-5 h-5 text-green-600" />
              <h2 className="text-xl font-semibold">Messageries & Communautés</h2>
              <span className="text-sm font-normal text-gray-500">
                ({messaging.length} outils)
              </span>
            </div>
            <p className="text-gray-600 mb-4">WhatsApp Business, Telegram et Discord</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {messaging.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-pink-50 to-purple-50 rounded-xl p-6 border border-pink-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-pink-600" />
            Workflow Publication Multi-Plateformes
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. Calendrier Editorial</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Hook Viral</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. Légende + Hashtags</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Adapter par plateforme</span>
            <span className="text-gray-400">-&gt;</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. Programmer</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Ce workflow vous permet de créer du contenu cohérent sur toutes les plateformes en un temps record.
          </p>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les outils Social Media ({socialTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {socialTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/social" />
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
