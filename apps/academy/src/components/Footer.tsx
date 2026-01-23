'use client';

import Link from 'next/link';
import { useI18n } from '@/lib/i18n';

export default function Footer() {
  const { t } = useI18n();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-card">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-lg">IA</span>
              </div>
              <span className="font-bold text-xl text-foreground">{t('app.name')}</span>
            </div>
            <p className="text-muted-foreground max-w-md">
              {t('app.description')}
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">{t('nav.courses')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/courses?category=ai" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('category.ai')}
                </Link>
              </li>
              <li>
                <Link href="/courses?category=ml" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('category.ml')}
                </Link>
              </li>
              <li>
                <Link href="/courses?category=dl" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('category.dl')}
                </Link>
              </li>
              <li>
                <Link href="/courses?category=python" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('category.python')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Legal</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/privacy" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('footer.privacy')}
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('footer.terms')}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-foreground transition-colors">
                  {t('nav.contact')}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-border text-center text-muted-foreground">
          <p>&copy; {currentYear} IAFactory Academy. {t('footer.rights')}.</p>
        </div>
      </div>
    </footer>
  );
}
