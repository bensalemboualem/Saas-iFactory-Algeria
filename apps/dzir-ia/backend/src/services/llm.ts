// D:\iafactorychatgpt\dzir-ia\backend\src\services\llm.ts
import { chatLLM } from "./llm/router.js";

// Types utilisés par le backend
export interface ChatMessage {
  content: string;
  role: "system" | "user" | "assistant";
}

export interface LLMResponse {
  content: string;
  model: string;
  usage?: {
    completion_tokens?: number;
    prompt_tokens?: number;
    total_tokens?: number;
  };
}

/**
 * Generate a chat completion using the LLM router (OpenAI/Claude/Gemini/DeepSeek/Qwen/xAI/OpenRouter/Local Ollama)
 *
 * IMPORTANT:
 * - `provider` can be "openai" | "anthropic" | "gemini" | "deepseek" | "qwen" | "xai" | "openrouter" | "moonshot" | "local"
 * - `model` is provider-specific (for local ollama use "llama3.2:3b" etc.)
 */
export async function generateChatCompletion(opts: {
  maxTokens?: number;
  messages: ChatMessage[];
  model?: string;
  provider?: string;
}): Promise<LLMResponse> {
  const { messages, provider, model, maxTokens } = opts;

  try {
    const res = await chatLLM({
      maxTokens,
      messages,
      model,
      provider: provider as any,
    });

    // Normalize response
    return {
      content: res.text ?? "",
      model: model ?? process.env.LOCAL_LLM_MODEL ?? process.env.OPENAI_MODEL ?? "unknown",
      // If you want to pass tokens, you can parse res.raw usage when present.
      usage: (res.raw && (res.raw.usage || res.raw.tokensUsed)) || undefined,
    };
  } catch (error: any) {
    // Keep very explicit log so we can debug quickly
    console.error("Failed to generate chat completion (router):", error?.message || error);
    throw error;
  }
}

/**
 * Helper to build messages in the same format as before.
 * If you already have message building elsewhere, you can ignore this.
 */
export function buildChatMessages(params: {
  context?: string;
  systemPrompt?: string;
  userPrompt: string;
}): ChatMessage[] {
  const { systemPrompt, userPrompt, context } = params;

  const msgs: ChatMessage[] = [];

  if (systemPrompt && systemPrompt.trim()) {
    msgs.push({ content: systemPrompt.trim(), role: "system" });
  }

  if (context && context.trim()) {
    msgs.push({
      content:
        "CONTEXT (use this to answer, cite sources by [index]):\n" + context.trim(),
      role: "system",
    });
  }

  msgs.push({ content: userPrompt, role: "user" });

  return msgs;
}
