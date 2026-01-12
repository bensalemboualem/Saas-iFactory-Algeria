// ============================================================
// IA FACTORY - INTERVIEW AGENTS - TYPES & INTERFACES
// ============================================================

export interface InterviewPhase {
  id: string;
  name: string;
  minExchanges: number;
  maxExchanges: number;
  objectives: string[];
}

export interface InterviewConfig {
  agentId: string;
  systemPrompt: string;
  phases: InterviewPhase[];
  model: {
    provider: "anthropic";
    modelId: string;
    temperature: number;
    maxTokens: number;
  };
}

export interface InterviewMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  phase?: string;
}

export interface InterviewSession {
  id: string;
  agentId: string;
  startedAt: Date;
  endedAt?: Date;
  currentPhase: string;
  messages: InterviewMessage[];
  status: "active" | "completed" | "abandoned";
}

export interface AgentConfig {
  id: string;
  name: string;
  nameAr: string;
  description: string;
  icon: string;
  color: string;
  category: string;
  phases: InterviewPhase[];
}
