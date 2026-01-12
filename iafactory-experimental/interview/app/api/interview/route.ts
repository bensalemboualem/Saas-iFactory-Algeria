// ============================================================
// IA FACTORY - INTERVIEW AGENTS - API ROUTE (DeepSeek)
// ============================================================

import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import { AGENT_CONFIGS } from "@/src/modules/interview-agents/config/agents";

// In-memory session store (utiliser Redis en production)
const sessions: Record<string, any> = {};

// DeepSeek via OpenAI-compatible API
const openai = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com/v1",
});

export async function POST(request: NextRequest) {
  try {
    const { agentId, action, message, sessionId, systemPrompt } = await request.json();

    const config = AGENT_CONFIGS[agentId as keyof typeof AGENT_CONFIGS];
    if (!config) {
      return NextResponse.json({ error: "Agent non trouvé" }, { status: 404 });
    }

    switch (action) {
      case "start":
        return handleStart(agentId, config, systemPrompt);
      case "message":
        return handleMessage(agentId, config, message, sessionId, systemPrompt);
      case "report":
        return handleReport(agentId, systemPrompt, request);
      default:
        return NextResponse.json({ error: "Action non valide" }, { status: 400 });
    }
  } catch (error) {
    console.error("Interview API Error:", error);
    return NextResponse.json({ error: "Erreur serveur" }, { status: 500 });
  }
}

async function handleStart(agentId: string, config: any, systemPrompt: string) {
  const sessionId = Date.now().toString() + Math.random().toString(36).substr(2, 9);

  sessions[sessionId] = {
    agentId,
    messages: [],
    currentPhase: config.phases[0].id,
    phaseExchanges: 0,
    startedAt: new Date(),
  };

  const response = await openai.chat.completions.create({
    model: "deepseek-chat",
    max_tokens: 1024,
    temperature: 0.7,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: "Démarre interview avec ton message accueil." }
    ],
  });

  const initialMessage = response.choices[0]?.message?.content || "Bonjour";
  sessions[sessionId].messages.push({ role: "assistant", content: initialMessage });

  return NextResponse.json({
    sessionId,
    message: initialMessage,
    phase: config.phases[0].id,
    isComplete: false,
  });
}

async function handleMessage(
  agentId: string,
  config: any,
  userMessage: string,
  sessionId: string,
  systemPrompt: string
) {
  let session = sessions[sessionId];

  if (!session) {
    const newSessionId = Date.now().toString();
    sessions[newSessionId] = {
      agentId,
      messages: [],
      currentPhase: config.phases[0].id,
      phaseExchanges: 0,
      startedAt: new Date(),
    };
    session = sessions[newSessionId];
    sessionId = newSessionId;
  }

  session.messages.push({ role: "user", content: userMessage });
  session.phaseExchanges++;

  const currentPhaseConfig = config.phases.find((p: any) => p.id === session.currentPhase);
  if (currentPhaseConfig && session.phaseExchanges >= currentPhaseConfig.maxExchanges * 2) {
    const currentIndex = config.phases.findIndex((p: any) => p.id === session.currentPhase);
    if (currentIndex < config.phases.length - 1) {
      session.currentPhase = config.phases[currentIndex + 1].id;
      session.phaseExchanges = 0;
    }
  }

  const isLastPhase = session.currentPhase === config.phases[config.phases.length - 1].id;
  const isComplete = isLastPhase && session.phaseExchanges >= 4;

  const currentPhaseIndex = config.phases.findIndex((p: any) => p.id === session.currentPhase);
  const enhancedPrompt = systemPrompt + "\n\nPhase: " + session.currentPhase + " - Echange: " + session.phaseExchanges;

  const messages = [
    { role: "system", content: enhancedPrompt },
    ...session.messages.map((m: any) => ({ role: m.role, content: m.content }))
  ];

  const response = await openai.chat.completions.create({
    model: "deepseek-chat",
    max_tokens: 1024,
    temperature: 0.7,
    messages: messages as any,
  });

  const assistantMessage = response.choices[0]?.message?.content || "";
  session.messages.push({ role: "assistant", content: assistantMessage });

  return NextResponse.json({
    sessionId,
    message: assistantMessage,
    phase: session.currentPhase,
    isComplete,
  });
}

async function handleReport(agentId: string, systemPrompt: string, request: NextRequest) {
  const { messages } = await request.json();

  const reportPrompt = "Base sur cette interview, genere un rapport structure complet. Transcription: " + 
    messages.map((m: any) => m.role + ": " + m.content).join("\n");

  const response = await openai.chat.completions.create({
    model: "deepseek-chat",
    max_tokens: 4096,
    temperature: 0.7,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: reportPrompt }
    ],
  });

  return NextResponse.json({ report: response.choices[0]?.message?.content || "" });
}
