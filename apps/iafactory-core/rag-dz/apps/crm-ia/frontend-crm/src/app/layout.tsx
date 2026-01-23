import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css"; // Correct path for App Router

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CRM IA - Client Management",
  description: "Intelligent CRM for managing clients and cases",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}