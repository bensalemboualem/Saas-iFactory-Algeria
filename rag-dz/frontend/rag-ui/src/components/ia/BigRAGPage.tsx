/**
 * BigRAGPage - Page principale Assistant IA
 * ==========================================
 * Page wrapper avec titre et intégration du chat
 */

import React from "react";
import { BigRAGChat } from "./BigRAGChat";
import type { BigRAGChatProps } from "./types";

export interface BigRAGPageProps extends Omit<BigRAGChatProps, "className"> {
  /** Titre de la page */
  title?: string;
  /** Sous-titre de la page */
  subtitle?: string;
  /** Afficher les statistiques */
  showStats?: boolean;
}

export const BigRAGPage: React.FC<BigRAGPageProps> = ({
  title = "Assistant IA iaFactory Algérie 🇩🇿",
  subtitle = "3 Intelligences spécialisées : Business • Éducation • Religion",
  showStats = false,
  ...chatProps
}) => {
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)' }}>
      {/* ===== HEADER ===== */}
      <header style={{ background: 'var(--card)', borderBottom: '1px solid var(--border)' }}>
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Logo */}
              <div className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg" style={{ background: 'var(--iaf-green)' }}>
                <span className="text-2xl">🤖</span>
              </div>

              <div>
                <h1 className="text-2xl font-bold" style={{ color: 'var(--text)' }}>
                  {title}
                </h1>
                <p className="text-sm" style={{ color: 'var(--iaf-text-secondary)' }}>
                  {subtitle}
                </p>
              </div>
            </div>

            {/* RAG badges */}
            <div className="hidden md:flex items-center gap-2">
              <span className="px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
                💼 Business DZ
              </span>
              <span className="px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1" style={{ background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' }}>
                🎓 École
              </span>
              <span className="px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1" style={{ background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7' }}>
                ☪️ Islam
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* ===== MAIN CONTENT ===== */}
      <main className="max-w-6xl mx-auto px-4 py-6">
        {/* Stats bar (optional) */}
        {showStats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard icon="📄" label="Documents" value="1,234" color="blue" />
            <StatCard icon="🔍" label="Recherches" value="5,678" color="green" />
            <StatCard icon="🎯" label="Précision" value="94%" color="purple" />
            <StatCard icon="⚡" label="Temps moyen" value="0.8s" color="orange" />
          </div>
        )}

        {/* Chat container */}
        <div className="h-[calc(100vh-12rem)]">
          <BigRAGChat
            {...chatProps}
            className="h-full"
          />
        </div>
      </main>

      {/* ===== FOOTER ===== */}
      <footer className="absolute bottom-0 left-0 right-0 py-4 text-center text-sm" style={{ color: 'var(--iaf-text-muted)' }}>
        <p>
          Propulsé par{" "}
          <span className="font-medium" style={{ color: 'var(--iaf-green)' }}>iaFactory Algeria</span> •
          3 RAG Spécialisés •
          Business 💼 • Éducation 🎓 • Religion ☪️
        </p>
      </footer>
    </div>
  );
};

/**
 * Composant carte statistique
 */
interface StatCardProps {
  icon: string;
  label: string;
  value: string;
  color: "blue" | "green" | "purple" | "orange";
}

const StatCard: React.FC<StatCardProps> = ({ icon, label, value, color }) => {
  const colorStyles = {
    blue: { background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' },
    green: { background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' },
    purple: { background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7' },
    orange: { background: 'rgba(249, 115, 22, 0.1)', color: '#f97316' },
  };

  return (
    <div className="p-4 rounded-xl" style={colorStyles[color]}>
      <div className="flex items-center gap-2">
        <span className="text-xl">{icon}</span>
        <div>
          <p className="text-2xl font-bold">{value}</p>
          <p className="text-xs opacity-70">{label}</p>
        </div>
      </div>
    </div>
  );
};

/**
 * Version standalone pour route directe
 */
export const BigRAGStandalonePage: React.FC = () => {
  return (
    <BigRAGPage
      defaultCountry="DZ"
      enableVoice={false}
      showStats={false}
    />
  );
};

export default BigRAGPage;
