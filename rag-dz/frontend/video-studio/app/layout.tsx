import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AppHeader } from "@/components/app-header";
import { AppFooter } from "@/components/app-footer";
import { HelpChatbot } from "@/components/help-chatbot";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Dzir IA Video Studio Pro | IAFactory Algeria",
  description: "Plateforme professionnelle de création vidéo IA avec 10 générateurs - Runway, Luma AI, Kling AI, Alibaba, Pika Labs et plus",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <link
          rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
          crossOrigin="anonymous"
          referrerPolicy="no-referrer"
        />
        {/* Theme initialization script - runs before hydration */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                var theme = localStorage.getItem('iafactory_theme') || 'dark';
                document.documentElement.setAttribute('data-theme', theme);
                document.documentElement.classList.toggle('dark', theme === 'dark');
              })();
            `,
          }}
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        suppressHydrationWarning
      >
        <div className="flex min-h-screen flex-col">
          {/* Header */}
          <AppHeader />

          {/* Main Content */}
          <main className="container flex-1 px-4 py-8">
            {children}
          </main>

          {/* Footer */}
          <AppFooter />
        </div>

        {/* Help Chatbot (floating) */}
        <HelpChatbot />
      </body>
    </html>
  );
}
