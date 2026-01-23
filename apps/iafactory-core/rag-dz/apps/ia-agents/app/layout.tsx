import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Agents IA Gratuits | IA Factory Algeria",
  description: "Agents IA conversationnels gratuits: Coach Motivation, Dev Helper, Tuteur Maths et plus. Propulsé par Claude AI.",
  keywords: ["IA", "agents", "gratuit", "Algérie", "coach", "motivation", "développement", "maths"],
  authors: [{ name: "IA Factory" }],
  openGraph: {
    title: "Agents IA Gratuits - IA Factory",
    description: "Agents IA conversationnels gratuits pour tous",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="dark">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg border-b border-slate-200 dark:border-slate-800">
            <div className="container-app">
              <div className="flex items-center justify-between h-16">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg"></div>
                  <span className="text-xl font-bold">
                    <span className="text-primary">IA</span>{" "}
                    <span className="text-slate-900 dark:text-white">Factory</span>
                  </span>
                </div>

                <nav className="hidden md:flex items-center space-x-6">
                  <a href="/" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    Accueil
                  </a>
                  <a href="/agents" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    Agents
                  </a>
                  <a href="https://iafactoryalgeria.com" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    Apps Gratuites
                  </a>
                </nav>

                <div className="flex items-center space-x-4">
                  <span className="hidden sm:inline text-sm text-slate-600 dark:text-slate-400">
                    🇩🇿 Made in Algeria
                  </span>
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1">
            {children}
          </main>

          {/* Footer */}
          <footer className="bg-slate-100 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 mt-auto">
            <div className="container-app py-8">
              <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                <p className="text-slate-600 dark:text-slate-400 text-sm">
                  © 2024 IA Factory Algeria - Agents IA Gratuits
                </p>
                <div className="flex items-center space-x-6 text-sm">
                  <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    À propos
                  </a>
                  <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    Confidentialité
                  </a>
                  <a href="#" className="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">
                    Contact
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
