// ============================================================
// IA FACTORY - INTERVIEW AGENTS - CONFIGURATIONS
// ============================================================

import { AgentConfig } from "../types/interview";

export const AGENT_CONFIGS: Record<string, AgentConfig> = {
  "ia-ux-research": {
    id: "ia-ux-research",
    name: "IA UX Research",
    nameAr: "ذكاء بحث المستخدم",
    description: "Collectez les feedbacks utilisateurs pour améliorer vos produits",
    icon: "🔬",
    color: "#6366F1",
    category: "Interne",
    phases: [
      {
        id: "accueil",
        name: "Accueil",
        minExchanges: 1,
        maxExchanges: 2,
        objectives: ["presentation", "context"],
      },
      {
        id: "exploration",
        name: "Exploration Usage",
        minExchanges: 3,
        maxExchanges: 5,
        objectives: ["usage_patterns"],
      },
      {
        id: "friction",
        name: "Points de Friction",
        minExchanges: 3,
        maxExchanges: 5,
        objectives: ["pain_points"],
      },
      {
        id: "suggestions",
        name: "Suggestions",
        minExchanges: 2,
        maxExchanges: 3,
        objectives: ["improvements"],
      },
      {
        id: "cloture",
        name: "Clôture",
        minExchanges: 1,
        maxExchanges: 2,
        objectives: ["summary"],
      },
    ],
  },

  "ia-discovery-dz": {
    id: "ia-discovery-dz",
    name: "IA Discovery DZ",
    nameAr: "ذكاء اكتشاف السوق",
    description: "Validez votre marché et découvrez les besoins clients",
    icon: "🎯",
    color: "#10B981",
    category: "Startups & Entreprises",
    phases: [
      {
        id: "qualification",
        name: "Qualification",
        minExchanges: 2,
        maxExchanges: 3,
        objectives: ["profile"],
      },
      {
        id: "problem",
        name: "Exploration Problème",
        minExchanges: 4,
        maxExchanges: 6,
        objectives: ["validation"],
      },
      {
        id: "solutions",
        name: "Solutions Actuelles",
        minExchanges: 3,
        maxExchanges: 4,
        objectives: ["alternatives"],
      },
      {
        id: "value",
        name: "Validation Valeur",
        minExchanges: 2,
        maxExchanges: 3,
        objectives: ["willingness_to_pay"],
      },
      {
        id: "closing",
        name: "Clôture",
        minExchanges: 1,
        maxExchanges: 2,
        objectives: ["engagement"],
      },
    ],
  },

  "ia-recruteur-dz": {
    id: "ia-recruteur-dz",
    name: "IA Recruteur DZ",
    nameAr: "ذكاء التوظيف",
    description: "Pré-qualifiez les candidats ou préparez vos entretiens",
    icon: "👔",
    color: "#8B5CF6",
    category: "RH & Recrutement",
    phases: [
      {
        id: "introduction",
        name: "Introduction",
        minExchanges: 1,
        maxExchanges: 2,
        objectives: ["ice_breaker"],
      },
      {
        id: "experience",
        name: "Expérience",
        minExchanges: 3,
        maxExchanges: 4,
        objectives: ["background"],
      },
      {
        id: "technical",
        name: "Technique",
        minExchanges: 3,
        maxExchanges: 5,
        objectives: ["hard_skills"],
      },
      {
        id: "soft_skills",
        name: "Soft Skills",
        minExchanges: 2,
        maxExchanges: 3,
        objectives: ["behavior"],
      },
      {
        id: "motivation",
        name: "Motivation",
        minExchanges: 2,
        maxExchanges: 3,
        objectives: ["career_goals"],
      },
      {
        id: "closing",
        name: "Clôture",
        minExchanges: 1,
        maxExchanges: 2,
        objectives: ["next_steps"],
      },
    ],
  },
};

// Helper pour récupérer un agent par ID
export function getAgentConfig(agentId: string): AgentConfig | undefined {
  return AGENT_CONFIGS[agentId];
}

// Liste de tous les agents
export function getAllAgents(): AgentConfig[] {
  return Object.values(AGENT_CONFIGS);
}
