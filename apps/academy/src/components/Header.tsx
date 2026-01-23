'use client';

import Link from 'next/link';
import { useI18n } from '@/lib/i18n';
import ThemeToggle from './ThemeToggle';
import LanguageSwitcher from './LanguageSwitcher';

export default function Header() {
  const { t } = useI18n();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-lg">IA</span>
          </div>
          <span className="font-bold text-xl text-foreground">{t('app.name')}</span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/" className="text-muted-foreground hover:text-foreground transition-colors">
            {t('nav.home')}
          </Link>
          <Link href="/courses" className="text-muted-foreground hover:text-foreground transition-colors">
            {t('nav.courses')}
          </Link>
          <Link href="/certifications" className="text-muted-foreground hover:text-foreground transition-colors">
            {t('nav.certifications')}
          </Link>
          <Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">
            {t('nav.about')}
          </Link>
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <LanguageSwitcher />
          <Link
            href="/login"
            className="hidden sm:inline-flex px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:opacity-90 transition-opacity"
          >
            {t('auth.login')}
          </Link>
        </div>
      </div>
    </header>
  );
}
