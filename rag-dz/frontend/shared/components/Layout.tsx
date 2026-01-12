/**
 * IAFactory Global Layout Component
 * Unified Header + Footer across all apps
 * Supports: Dark/Light mode, FR/AR/EN with RTL
 *
 * RTL SUPPORT:
 * - Uses Tailwind RTL utilities (rtl:, ltr:)
 * - Flexbox uses start/end instead of left/right
 * - Logo stays on start, controls on end
 */

import React, { useEffect, useState } from 'react';
import { useI18n, setLocale, Locale, LOCALES, isRTL } from '../i18n';

interface LayoutProps {
  children: React.ReactNode;
  showHeader?: boolean;
  showFooter?: boolean;
  className?: string;
}

export function Layout({
  children,
  showHeader = true,
  showFooter = true,
  className = ''
}: LayoutProps) {
  const { locale, t, isRTL: isRTLMode } = useI18n();
  const [isDark, setIsDark] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Initialize theme from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('iaf_theme');
    if (stored === 'light') {
      setIsDark(false);
      document.documentElement.classList.remove('dark');
    } else {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  // Toggle dark/light mode
  const toggleTheme = () => {
    setIsDark(!isDark);
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('iaf_theme', 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('iaf_theme', 'dark');
    }
  };

  // Handle language change
  const handleLocaleChange = (newLocale: Locale) => {
    setLocale(newLocale);
  };

  return (
    <div className={`min-h-screen bg-background text-foreground ${className}`} dir={isRTLMode ? 'rtl' : 'ltr'}>
      {/* === GLOBAL HEADER === */}
      {showHeader && (
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-16 items-center justify-between">
            {/* Logo - RTL: stays on logical start */}
            <a href="/" className="flex items-center gap-3 rtl:flex-row-reverse">
              <img
                src="/assets/img/logo-neon.png"
                alt="IAFactory"
                className="h-10"
                onError={(e) => { (e.target as HTMLImageElement).style.display = 'none' }}
              />
              <span className="text-xl font-bold text-primary">IAFactory</span>
            </a>

            {/* Desktop Navigation - RTL: uses gap which works both directions */}
            <nav className="hidden md:flex items-center gap-6 rtl:flex-row-reverse">
              <a href="/cockpit" className="text-muted-foreground hover:text-foreground transition-colors">
                {t('navigation.cockpit')}
              </a>
              <a href="/chat" className="text-muted-foreground hover:text-foreground transition-colors">
                {t('navigation.chat')}
              </a>
              <a href="/voice" className="text-muted-foreground hover:text-foreground transition-colors">
                {t('navigation.voice')}
              </a>
              <a href="/pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                {t('pricing.title').split(',')[0]}
              </a>
            </nav>

            {/* Controls - RTL: stays on logical end */}
            <div className="flex items-center gap-4 rtl:flex-row-reverse">
              {/* Language Selector */}
              <div className="flex rounded-lg overflow-hidden border border-border rtl:flex-row-reverse">
                {(Object.keys(LOCALES) as Locale[]).map((loc) => (
                  <button
                    key={loc}
                    onClick={() => handleLocaleChange(loc)}
                    className={`px-3 py-1.5 text-sm transition-colors ${
                      locale === loc
                        ? 'bg-primary text-primary-foreground'
                        : 'hover:bg-muted'
                    }`}
                  >
                    {loc === 'ar' ? 'ع' : loc.toUpperCase()}
                  </button>
                ))}
              </div>

              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg hover:bg-muted transition-colors"
                aria-label="Toggle theme"
              >
                {isDark ? (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="md:hidden p-2 rounded-lg hover:bg-muted"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Menu - RTL: text alignment handled by dir attribute */}
          {isMobileMenuOpen && (
            <div className="md:hidden border-t border-border bg-background p-4">
              <nav className="flex flex-col gap-4 rtl:items-end">
                <a href="/cockpit" className="text-muted-foreground hover:text-foreground">
                  {t('navigation.cockpit')}
                </a>
                <a href="/chat" className="text-muted-foreground hover:text-foreground">
                  {t('navigation.chat')}
                </a>
                <a href="/voice" className="text-muted-foreground hover:text-foreground">
                  {t('navigation.voice')}
                </a>
                <a href="/pricing" className="text-muted-foreground hover:text-foreground">
                  {t('pricing.title').split(',')[0]}
                </a>
              </nav>
            </div>
          )}
        </header>
      )}

      {/* === MAIN CONTENT === */}
      <main className="flex-1">
        {children}
      </main>

      {/* === GLOBAL FOOTER === RTL: grid auto-adjusts */}
      {showFooter && (
        <footer className="border-t border-border bg-muted/30">
          <div className="container py-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 rtl:text-right">
              {/* Brand */}
              <div>
                <h3 className="font-bold text-lg mb-4">IAFactory</h3>
                <p className="text-muted-foreground text-sm">
                  IA Souveraine pour l'Algérie et la Suisse
                </p>
              </div>

              {/* Links */}
              <div>
                <h4 className="font-semibold mb-4">{t('navigation.dashboard')}</h4>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="/cockpit" className="hover:text-foreground">{t('navigation.cockpit')}</a></li>
                  <li><a href="/chat" className="hover:text-foreground">{t('navigation.chat')}</a></li>
                  <li><a href="/voice" className="hover:text-foreground">{t('navigation.voice')}</a></li>
                </ul>
              </div>

              {/* Support */}
              <div>
                <h4 className="font-semibold mb-4">{t('footer.contact')}</h4>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="/pricing" className="hover:text-foreground">{t('pricing.title').split(',')[0]}</a></li>
                  <li><a href="/offre-institutionnelle" className="hover:text-foreground">Gouvernement</a></li>
                </ul>
              </div>

              {/* Legal */}
              <div>
                <h4 className="font-semibold mb-4">Legal</h4>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="/privacy" className="hover:text-foreground">{t('footer.privacy')}</a></li>
                  <li><a href="/terms" className="hover:text-foreground">{t('footer.terms')}</a></li>
                </ul>
              </div>
            </div>

            {/* Copyright */}
            <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
              {t('footer.copyright')}
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}

export default Layout;
