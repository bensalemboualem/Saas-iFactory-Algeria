import type { Metadata } from 'next';
import { Inter, Tajawal } from 'next/font/google';
import './globals.css';
import { I18nProvider } from '@/lib/i18n';
import { ThemeProvider } from '@/lib/theme';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const tajawal = Tajawal({ subsets: ['arabic'], weight: ['400', '500', '700'], variable: '--font-tajawal' });

export const metadata: Metadata = {
  title: 'IAFactory Algeria - 294+ Outils IA | أدوات الذكاء الاصطناعي',
  description: 'Plateforme SaaS de génération de contenu IA avec outils exclusifs pour le marché algérien. Blog, SEO, réseaux sociaux, administration, éducation. | منصة SaaS لتوليد المحتوى بالذكاء الاصطناعي',
  keywords: ['IA', 'Intelligence Artificielle', 'Algérie', 'Blog', 'SEO', 'Content', 'CNAS', 'Bac', 'BEM', 'الذكاء الاصطناعي', 'الجزائر'],
  authors: [{ name: 'IAFactory Algeria' }],
  openGraph: {
    title: 'IAFactory Algeria - 294+ Outils IA',
    description: 'Plateforme SaaS tout-en-un pour la génération de contenu IA',
    url: 'https://iafactoryalgeria.com',
    siteName: 'IAFactory Algeria',
    locale: 'fr_DZ',
    alternateLocale: ['ar_DZ', 'en_US'],
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" dir="ltr" suppressHydrationWarning>
      <body className={`${inter.variable} ${tajawal.variable} font-sans`}>
        <ThemeProvider>
          <I18nProvider>
            <div className="min-h-screen bg-background text-foreground">
              {children}
            </div>
          </I18nProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
