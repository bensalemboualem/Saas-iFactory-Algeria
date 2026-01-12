// ============================================================
// IA FACTORY - INTERVIEW AGENTS - DASHBOARD PAGE
// Styled to match IAFactory landing page branding
// ============================================================

"use client";

import React, { useState } from "react";
import { getAllAgents } from "@/src/modules/interview-agents/config/agents";
import InterviewChat from "@/src/modules/interview-agents/components/InterviewChat";
import type { AgentConfig } from "@/src/modules/interview-agents/types/interview";

// System prompts
const SYSTEM_PROMPTS: Record<string, string> = {
  "ia-ux-research": `Tu es IA UX Research, un agent d'interview spécialisé dans la collecte de feedbacks utilisateurs pour améliorer les produits de IA Factory.

## Structure d'interview

### Phase 1 : Accueil (1-2 échanges)
- Présentation chaleureuse
- Expliquer le but de l'interview
- Mettre à l'aise

### Phase 2 : Exploration Usage (3-5 échanges)
- Comment utilisez-vous IA Factory ?
- Quelles fonctionnalités utilisez-vous le plus ?
- Dans quel contexte ?

### Phase 3 : Points de Friction (3-5 échanges)
- Qu'est-ce qui vous freine ?
- Qu'est-ce qui vous frustre ?
- Qu'avez-vous essayé de faire sans succès ?

### Phase 4 : Suggestions (2-3 échanges)
- Quelles améliorations souhaiteriez-vous ?
- Quelle fonctionnalité manque ?

### Phase 5 : Clôture (1-2 échanges)
- Récapitulatif
- Remerciements

Reste bienveillant, écoute activement, pose des questions ouvertes. Génère un rapport UX structuré à la fin.`,

  "ia-discovery-dz": `Tu es IA Discovery DZ, un agent d'interview spécialisé dans la validation de marché pour les startups algériennes, utilisant la méthode Mom Test.

## Principes Mom Test
- Pose des questions sur le passé concret, pas l'avenir hypothétique
- Demande des exemples précis
- Détecte les signaux faibles vs forts

## Structure d'interview

### Phase 1 : Qualification (2-3 échanges)
- Profil de l'interviewé
- Contexte professionnel

### Phase 2 : Exploration Problème (4-6 échanges)
- Comment gérez-vous [problème] actuellement ?
- Racontez-moi la dernière fois que [situation]
- Combien de temps/argent perdez-vous ?

### Phase 3 : Solutions Actuelles (3-4 échanges)
- Qu'avez-vous essayé ?
- Pourquoi avez-vous arrêté ?
- Qu'est-ce qui manque ?

### Phase 4 : Validation Valeur (2-3 échanges)
- Combien seriez-vous prêt à payer ?
- À quelle fréquence ?

### Phase 5 : Clôture (1-2 échanges)
- Synthèse
- Next steps

Adapte ton langage au contexte algérien. Génère un rapport Discovery avec signaux détectés.`,

  "ia-recruteur-dz": `Tu es IA Recruteur DZ, un agent d'interview spécialisé dans la pré-qualification des candidats pour le marché de l'emploi algérien.

## Structure d'entretien

### Phase 1 : Introduction (1-2 échanges)
- Présentation chaleureuse
- Expliquer le déroulement
- "Pouvez-vous vous présenter brièvement ?"

### Phase 2 : Parcours & Expérience (3-4 échanges)
- "Parlez-moi de votre poste actuel/dernier poste"
- "Quelle a été votre plus grande réalisation ?"
- "Pourquoi ce changement ?"

### Phase 3 : Compétences Techniques (3-5 échanges)
- Questions adaptées au poste
- Utiliser la méthode STAR
- "Décrivez un projet complexe que vous avez géré"

### Phase 4 : Soft Skills (2-3 échanges)
- "Comment gérez-vous le stress ?"
- "Parlez-moi d'un conflit au travail"
- "Quel est votre style de travail ?"

### Phase 5 : Motivations (2-3 échanges)
- "Où vous voyez-vous dans 3-5 ans ?"
- "Qu'est-ce qui vous motive ?"
- "Quelles sont vos attentes salariales ?"

### Phase 6 : Clôture (1-2 échanges)
- Questions du candidat
- Prochaines étapes

Reste professionnel et bienveillant. Génère un rapport d'évaluation avec scoring (Hard Skills, Soft Skills, Culture Fit).`,
};

export default function InterviewDashboardPage() {
  const [selectedAgent, setSelectedAgent] = useState<AgentConfig | null>(null);
  const agents = getAllAgents();

  const handleSelectAgent = (agent: AgentConfig) => {
    setSelectedAgent(agent);
  };

  const handleBackToDashboard = () => {
    setSelectedAgent(null);
  };

  const handleComplete = (report: string) => {
    console.log("Interview completed, report:", report);
  };

  if (selectedAgent) {
    return (
      <div className="min-h-screen" style={{ background: "#020617" }}>
        <div className="container mx-auto px-4 py-6">
          <button
            onClick={handleBackToDashboard}
            className="mb-4 flex items-center gap-2 transition-colors"
            style={{ color: "rgba(248, 250, 252, 0.75)" }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#00a651")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(248, 250, 252, 0.75)")}
          >
            <span>←</span>
            <span>Retour au tableau de bord</span>
          </button>
          <div className="h-[calc(100vh-120px)]">
            <InterviewChat
              agentId={selectedAgent.id}
              agentName={selectedAgent.name}
              agentIcon={selectedAgent.icon}
              agentColor="#00a651"
              systemPrompt={SYSTEM_PROMPTS[selectedAgent.id]}
              phases={selectedAgent.phases}
              onComplete={handleComplete}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen"
      style={{ background: "#020617", color: "#f8fafc" }}
    >
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="mb-4">
            <span className="text-sm font-semibold tracking-wider" style={{ color: "#00a651" }}>
              🎙️ IA FACTORY ALGERIA
            </span>
          </div>
          <h1 className="text-4xl font-bold mb-3" style={{ color: "#f8fafc" }}>
            Agents d'Interview IA
          </h1>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "rgba(248, 250, 252, 0.75)" }}>
            Conduisez des interviews structurées avec nos agents IA spécialisés.
            Collectez des insights, validez votre marché ou évaluez des candidats.
          </p>
        </div>

        {/* Agent Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {agents.map((agent) => (
            <div
              key={agent.id}
              onClick={() => handleSelectAgent(agent)}
              className="rounded-2xl cursor-pointer transition-all duration-300 overflow-hidden"
              style={{
                background: "linear-gradient(135deg, rgba(0, 166, 81, 0.08) 0%, rgba(0, 166, 81, 0.02) 100%)",
                border: "2px solid rgba(0, 166, 81, 0.3)",
                boxShadow: "0 4px 16px rgba(0, 166, 81, 0.15)"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "linear-gradient(135deg, rgba(0, 166, 81, 0.12) 0%, rgba(0, 166, 81, 0.04) 100%)";
                e.currentTarget.style.borderColor = "#00a651";
                e.currentTarget.style.boxShadow = "0 8px 32px rgba(0, 166, 81, 0.3)";
                e.currentTarget.style.transform = "translateY(-8px) scale(1.02)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "linear-gradient(135deg, rgba(0, 166, 81, 0.08) 0%, rgba(0, 166, 81, 0.02) 100%)";
                e.currentTarget.style.borderColor = "rgba(0, 166, 81, 0.3)";
                e.currentTarget.style.boxShadow = "0 4px 16px rgba(0, 166, 81, 0.15)";
                e.currentTarget.style.transform = "translateY(0) scale(1)";
              }}
            >
              {/* Card Header */}
              <div
                className="p-6 text-white relative overflow-hidden"
                style={{
                  background: "linear-gradient(135deg, #00a651 0%, #008c45 100%)",
                }}
              >
                <div className="text-5xl mb-3">{agent.icon}</div>
                <h2 className="text-xl font-bold mb-1">{agent.name}</h2>
                <p className="text-sm opacity-90">{agent.nameAr}</p>
              </div>

              {/* Card Body */}
              <div className="p-6">
                <p className="mb-4 min-h-[60px]" style={{ color: "rgba(248, 250, 252, 0.75)" }}>
                  {agent.description}
                </p>

                {/* Category Badge */}
                <div className="mb-4">
                  <span
                    className="inline-block px-3 py-1 text-xs rounded-full font-semibold"
                    style={{
                      backgroundColor: "rgba(0, 166, 81, 0.15)",
                      color: "#00a651",
                      border: "1px solid rgba(0, 166, 81, 0.3)"
                    }}
                  >
                    📂 {agent.category}
                  </span>
                </div>

                {/* Phases */}
                <div className="space-y-2 mb-6">
                  <p className="text-sm font-semibold" style={{ color: "#f8fafc" }}>
                    Phases de l'interview :
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {agent.phases.map((phase, idx) => (
                      <span
                        key={phase.id}
                        className="text-xs px-2 py-1 rounded"
                        style={{
                          backgroundColor: "rgba(255, 255, 255, 0.05)",
                          border: "1px solid rgba(255, 255, 255, 0.1)",
                          color: "rgba(248, 250, 252, 0.75)"
                        }}
                      >
                        {idx + 1}. {phase.name}
                      </span>
                    ))}
                  </div>
                </div>

                {/* CTA Button */}
                <button
                  className="w-full py-3 rounded-xl font-semibold transition-all duration-300"
                  style={{
                    background: "#00a651",
                    color: "#021014"
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "translateY(-1px)";
                    e.currentTarget.style.boxShadow = "0 4px 12px rgba(0, 166, 81, 0.4)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "translateY(0)";
                    e.currentTarget.style.boxShadow = "none";
                  }}
                >
                  Démarrer l'Interview →
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center">
          <div
            className="inline-block rounded-xl px-6 py-4"
            style={{
              background: "rgba(0, 166, 81, 0.08)",
              border: "1px solid rgba(0, 166, 81, 0.2)"
            }}
          >
            <p className="text-sm" style={{ color: "rgba(248, 250, 252, 0.75)" }}>
              💡 <span className="font-semibold" style={{ color: "#00a651" }}>Astuce :</span> Chaque interview
              génère un rapport structuré que vous pouvez télécharger en fin de session.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
