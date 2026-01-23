import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import PWAInstallPrompt from "./components/PWAInstallPrompt";
import NotificationPermission from "./components/NotificationPermission";
import Script from "next/script";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CAN 2025 🇩🇿 - Algérie en Live",
  description: "Suivez la Coupe d'Afrique des Nations 2025 au Maroc. Tous les matchs de l'Algérie, classements, et actualités en temps réel.",
  keywords: "CAN 2025, Algérie, Les Fennecs, Football, Coupe d'Afrique, Maroc, AFCON",
  authors: [{ name: "IA Factory" }],
  viewport: "width=device-width, initial-scale=1, maximum-scale=1",
  themeColor: "#007A3D",
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "CAN 2025",
  },
  openGraph: {
    title: "CAN 2025 🇩🇿 - Algérie en Live",
    description: "Suivez Les Fennecs à la CAN 2025",
    type: "website",
    locale: "fr_DZ",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="dark">
      <head>
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      </head>
      <body className={inter.className}>
        {/* Service Worker Registration */}
        <Script id="sw-register" strategy="afterInteractive">
          {`
            if ('serviceWorker' in navigator) {
              window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js').then(
                  (registration) => {
                    console.log('SW registered:', registration);
                  },
                  (error) => {
                    console.log('SW registration failed:', error);
                  }
                );
              });
            }
          `}
        </Script>

        {/* PWA Install Prompt */}
        <PWAInstallPrompt />

        {/* Notification Permission */}
        <NotificationPermission />

        {/* Header */}
        <header className="bg-gradient-to-r from-primary to-secondary text-white shadow-lg sticky top-0 z-50">
          <div className="container-app py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">🏆</span>
                <div>
                  <h1 className="text-2xl md:text-3xl font-bold">CAN 2025</h1>
                  <p className="text-sm text-white/80">Maroc 🇲🇦 | 21 Déc - 18 Jan</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/" className="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors">
                  <span className="text-3xl">🇩🇿</span>
                  <span className="hidden md:inline font-semibold">Algérie</span>
                </a>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="min-h-screen bg-slate-50 dark:bg-slate-950">
          {children}
        </main>

        {/* Footer */}
        <footer className="bg-slate-900 text-white py-8">
          <div className="container-app">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
              <div>
                <h3 className="text-lg font-bold mb-3 flex items-center justify-center md:justify-start space-x-2">
                  <span>🏆</span>
                  <span>CAN 2025</span>
                </h3>
                <p className="text-sm text-slate-400">
                  Suivez tous les matchs de la Coupe d'Afrique des Nations 2025
                </p>
              </div>
              <div>
                <h3 className="text-lg font-bold mb-3">🇩🇿 Algérie</h3>
                <p className="text-sm text-slate-400">
                  Champions d'Afrique 2019<br />
                  Objectif: 3ème étoile
                </p>
              </div>
              <div>
                <h3 className="text-lg font-bold mb-3">🔗 Liens</h3>
                <div className="space-y-2 text-sm">
                  <a href="/calendrier" className="block text-slate-400 hover:text-white transition-colors">
                    Calendrier complet
                  </a>
                  <a href="/groupes" className="block text-slate-400 hover:text-white transition-colors">
                    Groupes & Classements
                  </a>
                  <a href="/algerie" className="block text-slate-400 hover:text-white transition-colors">
                    Hub Algérie
                  </a>
                </div>
              </div>
            </div>
            <div className="mt-8 pt-6 border-t border-slate-800 text-center text-sm text-slate-400">
              <p>🇩🇿 Made with ❤️ in Algeria | IA Factory</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
