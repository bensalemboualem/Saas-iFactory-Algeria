import "./globals.css";

export const metadata = {
  title: "Interview Agents - IA Factory",
  description: "Agents d'interview IA spécialisés pour UX Research, Discovery et Recrutement",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
