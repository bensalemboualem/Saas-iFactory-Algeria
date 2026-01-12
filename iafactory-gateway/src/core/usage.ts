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
