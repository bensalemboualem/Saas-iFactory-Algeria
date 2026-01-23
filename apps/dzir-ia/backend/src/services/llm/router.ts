// D:\iafactorychatgpt\dzir-ia\backend\src\services\llm\router.ts
import type { ChatMsg } from "./openai_compat.js";
import { chatOpenAICompat } from "./openai_compat.js";
import { chatAnthropic } from "./anthropic.js";
import { chatGemini } from "./gemini.js";

export type LLMProvider =
  | "openai"
  | "deepseek"
  | "moonshot"
  | "qwen"
  | "xai"
  | "openrouter"
  | "anthropic"
  | "gemini"
  | "local";

function reqEnv(name: string, optional = false) {
  const v = process.env[name];
  if (!v && !optional) throw new Error(`Missing env: ${name}`);
  return v;
}

export async function chatLLM(opts: {
  provider?: LLMProvider;
  model?: string;
  messages: ChatMsg[];
  maxTokens?: number;
}) {
  const provider = (opts.provider ??
    (process.env.LLM_DEFAULT_PROVIDER as LLMProvider) ??
    "openai") as LLMProvider;

  // ===== Claude =====
  if (provider === "anthropic") {
    return chatAnthropic({
      apiKey: reqEnv("ANTHROPIC_API_KEY")!,
      model: opts.model || "claude-3-5-sonnet-20241022",
      messages: opts.messages,
      maxTokens: opts.maxTokens,
    });
  }

  // ===== Gemini =====
  if (provider === "gemini") {
    return chatGemini({
      apiKey: reqEnv("GEMINI_API_KEY")!,
      model: opts.model || "gemini-2.0-flash",
      messages: opts.messages,
    });
  }

  // ===== Local (Ollama / vLLM / LM Studio) =====
  if (provider === "local") {
    const baseUrl = reqEnv("LOCAL_LLM_BASE_URL")!;
    const model = opts.model || reqEnv("LOCAL_LLM_MODEL", true) || "llama3.2:3b";

    return chatOpenAICompat({
      baseUrl,
      apiKey: "", // 🚫 NO AUTH HEADER for local
      model,
      messages: opts.messages,
      maxTokens: opts.maxTokens,
      extraHeaders: {}, // no Authorization
    });
  }

  // ===== OpenAI-compatible providers =====
  const map: Record<
    string,
    { key: string; base: string; extra?: Record<string, string> }
  > = {
    openai: {
      key: "OPENAI_API_KEY",
      base:
        process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
    },
    deepseek: {
      key: "DEEPSEEK_API_KEY",
      base: reqEnv("DEEPSEEK_BASE_URL")!,
    },
    moonshot: {
      key: "MOONSHOT_API_KEY",
      base: reqEnv("MOONSHOT_BASE_URL")!,
    },
    qwen: {
      key: "DASHSCOPE_API_KEY",
      base: reqEnv("QWEN_BASE_URL")!,
    },
    xai: {
      key: "XAI_API_KEY",
      base: reqEnv("XAI_BASE_URL")!,
    },
    openrouter: {
      key: "OPENROUTER_API_KEY",
      base: reqEnv("OPENROUTER_BASE_URL")!,
      extra: {
        ...(process.env.OPENROUTER_REFERRER
          ? { "HTTP-Referer": process.env.OPENROUTER_REFERRER }
          : {}),
        ...(process.env.OPENROUTER_TITLE
          ? { "X-Title": process.env.OPENROUTER_TITLE }
          : {}),
      },
    },
  };

  const cfg = map[provider];
  if (!cfg) throw new Error(`Unknown provider: ${provider}`);

  return chatOpenAICompat({
    baseUrl: cfg.base,
    apiKey: reqEnv(cfg.key)!,
    model: opts.model || "gpt-4o-mini",
    messages: opts.messages,
    maxTokens: opts.maxTokens,
    extraHeaders: cfg.extra,
  });
}
