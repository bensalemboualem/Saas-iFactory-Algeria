import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "react-hot-toast";
import { Header, Footer, ChatHelp, SettingsPanel } from "@/components/layout";
import ClientProviders from "./providers";

export const metadata: Metadata = {
  title: "IA Factory Video Studio",
  description: "Générateur de vidéos IA pour le marché algérien - Text-to-Video, Image-to-Video avec support Darija",
  keywords: ["IA", "vidéo", "génération", "Algérie", "Darija", "text-to-video", "AI video"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" dir="ltr" suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Sora:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        <ClientProviders>
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: "#12121a",
                color: "#f4f4f5",
                border: "1px solid #2a2a3a",
              },
            }}
          />
          <Header />
          <main className="min-h-screen">{children}</main>
          <Footer />
          <ChatHelp />
          <SettingsPanel />
        </ClientProviders>
      </body>
    </html>
  );
}
