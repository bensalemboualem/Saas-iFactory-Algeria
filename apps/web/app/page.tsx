'use client';

import Link from 'next/link';
import ThemeToggle from '@/components/ThemeToggle';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import { useI18n } from '@/lib/i18n';

const categories = [
  { id: 'blog', name: 'Blog & Contenu', count: 20, icon: '📝', href: '/tools/blog' },
  { id: 'seo', name: 'SEO', count: 15, icon: '🔍', href: '/tools/seo' },
  { id: 'social', name: 'Réseaux Sociaux', count: 30, icon: '📱', href: '/tools/social' },
  { id: 'youtube', name: 'YouTube', count: 25, icon: '🎬', href: '/tools/youtube' },
  { id: 'email', name: 'Email Marketing', count: 20, icon: '📧', href: '/tools/email' },
  { id: 'ecommerce', name: 'E-commerce', count: 25, icon: '🛒', href: '/tools/ecommerce' },
  { id: 'admin-dz', name: 'Admin Algérie', count: 17, icon: '🏛️', href: '/tools/admin-dz', exclusive: true },
  { id: 'education-dz', name: 'Éducation Algérie', count: 10, icon: '🎓', href: '/tools/education-dz', exclusive: true },
];

const plans = [
  { name: 'Gratuit', credits: 100, price: 0 },
  { name: 'Starter', credits: 1000, price: 1990 },
  { name: 'Pro', credits: 5000, price: 4990, popular: true },
  { name: 'Business', credits: 20000, price: 14990 },
  { name: 'Entreprise', credits: 100000, price: 49990 },
];

export default function HomePage() {
  const { t } = useI18n();

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-card shadow-sm sticky top-0 z-50 border-b border-border">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-primary">IAFactory</span>
            <span className="text-sm bg-primary/10 text-primary px-2 py-0.5 rounded">Algeria</span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <Link href="/tools" className="text-muted-foreground hover:text-foreground">{t('nav.tools')}</Link>
            <Link href="/pricing" className="text-muted-foreground hover:text-foreground">{t('nav.pricing')}</Link>
            <Link href="/docs" className="text-muted-foreground hover:text-foreground">Documentation</Link>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <LanguageSwitcher />
            <Link href="/login" className="text-muted-foreground hover:text-foreground hidden sm:inline">Connexion</Link>
            <Link href="/signup" className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition">
              Commencer
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full mb-6">
            <span className="text-2xl">🇩🇿</span>
            <span className="font-medium">Conçu pour l'Algérie</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6">
            <span className="text-primary">250+ Outils IA</span>
            <br />
            pour Créer du Contenu
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Plateforme tout-en-un de génération de contenu IA avec des outils exclusifs
            pour l'administration et l'éducation algérienne.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup" className="bg-primary text-primary-foreground px-8 py-4 rounded-xl text-lg font-semibold hover:bg-primary/90 transition shadow-lg">
              Essayer gratuitement - 100 crédits offerts
            </Link>
            <Link href="/tools" className="bg-card text-foreground px-8 py-4 rounded-xl text-lg font-semibold border-2 border-border hover:border-primary transition">
              Voir tous les outils
            </Link>
          </div>
          <p className="text-sm text-muted-foreground mt-4">Aucune carte bancaire requise • Paiement CCP, BaridiMob, DAHABIA</p>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-16 px-4 bg-secondary/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4 text-foreground">Catégories d'Outils</h2>
          <p className="text-muted-foreground text-center mb-12">
            Découvrez nos outils organisés par catégorie
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category) => (
              <Link
                key={category.id}
                href={category.href}
                className="bg-card rounded-xl p-6 shadow-sm hover:shadow-lg transition group relative overflow-hidden border border-border"
              >
                {category.exclusive && (
                  <div className="absolute top-0 right-0 bg-destructive text-destructive-foreground text-xs px-2 py-1 rounded-bl-lg">
                    🇩🇿 Exclusif
                  </div>
                )}
                <span className="text-4xl mb-4 block">{category.icon}</span>
                <h3 className="text-lg font-semibold text-foreground mb-1 group-hover:text-primary transition">
                  {category.name}
                </h3>
                <p className="text-sm text-muted-foreground">{category.count} outils</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Algeria Exclusive Section */}
      <section className="py-16 px-4 bg-gradient-to-r from-green-600 to-green-700">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-3xl font-bold mb-6">🇩🇿 Outils Exclusifs Algérie</h2>
          <p className="text-lg opacity-90 mb-8">
            Des outils spécialement conçus pour les démarches administratives
            et l'éducation en Algérie.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="text-2xl mb-2">🏥</div>
              <div className="text-sm font-medium">Agent CNAS</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="text-2xl mb-2">💼</div>
              <div className="text-sm font-medium">Agent CNRC</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="text-2xl mb-2">⚡</div>
              <div className="text-sm font-medium">Agent Sonelgaz</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="text-2xl mb-2">🎓</div>
              <div className="text-sm font-medium">Révision Bac</div>
            </div>
          </div>
          <Link
            href="/tools/admin-dz"
            className="inline-block bg-white text-green-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Découvrir les outils Algérie
          </Link>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4 text-foreground">Tarifs en Dinars Algériens</h2>
          <p className="text-muted-foreground text-center mb-12">
            Payez avec CCP, BaridiMob ou DAHABIA via Chargily Pay
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`rounded-xl p-6 ${
                  plan.popular
                    ? 'bg-primary text-primary-foreground ring-4 ring-primary/20 scale-105'
                    : 'bg-card border border-border'
                }`}
              >
                {plan.popular && (
                  <div className="text-xs font-semibold bg-white/20 px-2 py-1 rounded mb-4 inline-block">
                    Plus populaire
                  </div>
                )}
                <h3 className={`text-lg font-bold mb-2 ${plan.popular ? '' : 'text-foreground'}`}>
                  {plan.name}
                </h3>
                <div className={`text-3xl font-bold mb-1 ${plan.popular ? '' : 'text-foreground'}`}>
                  {plan.price.toLocaleString('fr-DZ')} <span className="text-lg">DA</span>
                </div>
                <p className={`text-sm mb-4 ${plan.popular ? 'opacity-90' : 'text-muted-foreground'}`}>
                  {plan.credits.toLocaleString('fr-DZ')} crédits/mois
                </p>
                <button
                  className={`w-full py-2 rounded-lg font-medium transition ${
                    plan.popular
                      ? 'bg-white text-primary hover:bg-gray-100'
                      : 'bg-primary text-primary-foreground hover:bg-primary/90'
                  }`}
                >
                  {plan.price === 0 ? 'Commencer' : 'Choisir'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="text-lg font-bold mb-4">IAFactory Algeria</h4>
              <p className="text-gray-400 text-sm">
                Plateforme SaaS de génération de contenu IA pour l'Algérie.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Outils</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/tools/blog" className="hover:text-white">Blog & Contenu</Link></li>
                <li><Link href="/tools/seo" className="hover:text-white">SEO</Link></li>
                <li><Link href="/tools/social" className="hover:text-white">Réseaux Sociaux</Link></li>
                <li><Link href="/tools/admin-dz" className="hover:text-white">Admin Algérie</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/docs" className="hover:text-white">Documentation</Link></li>
                <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
                <li><Link href="/faq" className="hover:text-white">FAQ</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Légal</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/privacy" className="hover:text-white">Confidentialité</Link></li>
                <li><Link href="/terms" className="hover:text-white">Conditions</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">
              © 2026 IAFactory Algeria. Tous droits réservés.
            </p>
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span>🇩🇿 Conçu en Algérie</span>
              <span>•</span>
              <span>Paiement Chargily Pay</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
