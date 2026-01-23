import { appConfig } from '../config.js';

export function calculateCost(model: string, tokens: number): number {
  // Cost per 1M tokens, converted to actual tokens
  const pricePerMillion = getPricePerMillion(model);
  return (tokens / 1_000_000) * pricePerMillion;
}

function getPricePerMillion(model: string): number {
  // Normalized model pricing
  if (model.includes('gpt-4')) return appConfig.PRICING_GPT4;
  if (model.includes('gpt-3.5')) return appConfig.PRICING_GPT35;
  if (model.includes('claude')) return appConfig.PRICING_CLAUDE;
  if (model.includes('groq') || model.includes('iaf-fast')) return appConfig.PRICING_GROQ_FAST;
  if (model.includes('deepseek') || model.includes('iaf-cheap')) return appConfig.PRICING_DEEPSEEK;
  
  // Default pricing for unknown models
  return 1.0;
}

export function estimateTokens(text: string): number {
  // Rough estimation: ~4 chars per token
  return Math.ceil(text.length / 4);
}

export function estimateMessagesTokens(messages: Array<{ role: string; content: string }>): number {
  let total = 0;

  for (const message of messages) {
    total += estimateTokens(message.content);
    // Add overhead for role and formatting
    total += 4;
  }

  return total;
}

// PR-003/004: Estimate hold cost before streaming (used by gateway SSE handler)
// FIX 3: Added safety margin (1.3x) to protect against final cost > hold
const HOLD_SAFETY_MARGIN = 1.3; // 30% buffer for estimation errors

export function calculateCostEstimate(body: any): number {
  const maxTokens = Number(body?.max_tokens ?? 512);
  const model = String(body?.model ?? '');
  // Estimate based on max_tokens + prompt tokens estimation
  const messages = body?.messages ?? [];
  const promptTokens = estimateMessagesTokens(messages);
  const baseCost = calculateCost(model, maxTokens + promptTokens);

  // Apply safety margin to handle estimation errors
  // Surplus is refunded in finalize(), so over-reserving is safe
  return baseCost * HOLD_SAFETY_MARGIN;
}

// PR-003/004: Compute final cost from provider usage (prompt+completion tokens)
export function calculateFinalCostFromUsage(
  usage: { promptTokens?: number; completionTokens?: number; tokens?: number; total_tokens?: number },
  body?: any
): number {
  const tokens =
    usage?.tokens ??
    usage?.total_tokens ??
    ((usage?.promptTokens ?? 0) + (usage?.completionTokens ?? 0));
  const model = String(body?.model ?? '');
  return calculateCost(model, tokens);
}
