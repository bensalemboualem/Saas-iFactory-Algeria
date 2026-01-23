/**
 * PR-004: Wrapper for streaming chat completions
 * Provides a clean interface for reserve/finalize/release pattern
 */

import { routeRequest } from '../../routing/router.js';
import type { AuthUser } from '../auth.js';

// Token estimation bounds to prevent absurd values
const MIN_FALLBACK_TOKENS = 1;
const MAX_FALLBACK_TOKENS_MULTIPLIER = 2; // max = requested max_tokens * 2
const DEFAULT_MAX_TOKENS = 512;

/** Clamp a value between min and max */
function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

export interface StreamUsage {
  tokens: number;
  promptTokens: number;
  completionTokens: number;
  provider: string;
}

export interface StreamChatCompletionResult {
  stream: AsyncIterable<any>;
  getUsage: () => Promise<StreamUsage>;
}

export async function streamChatCompletion(opts: {
  user: AuthUser;
  requestId: string;
  body: any;
  holdAmount?: number; // PR-004 FIX 1: fallback amount if provider returns 0 tokens
}): Promise<StreamChatCompletionResult> {
  const { user, body, holdAmount: _holdAmount } = opts;

  // Force streaming mode
  const streamingBody = { ...body, stream: true };

  const { provider, stream } = await routeRequest(streamingBody, user);

  // Track usage from streaming chunks
  let totalTokens = 0;
  let promptTokens = 0;
  let completionTokens = 0;
  let chunkCount = 0;
  let totalContentLength = 0;
  const providerName = (provider as any).constructor?.name?.replace('Provider', '').toLowerCase() ?? 'unknown';

  async function* wrappedStream(): AsyncIterable<any> {
    for await (const chunk of stream) {
      chunkCount++;

      // Track content length for fallback estimation
      const content = chunk?.choices?.[0]?.delta?.content;
      if (content) {
        totalContentLength += String(content).length;
      }

      // Capture usage if present in chunk (OpenAI format)
      const usage = chunk?.usage;
      if (usage) {
        totalTokens = Number(usage.total_tokens ?? totalTokens);
        promptTokens = Number(usage.prompt_tokens ?? promptTokens);
        completionTokens = Number(usage.completion_tokens ?? completionTokens);
      }

      // Also check for delta usage (some providers)
      const delta = chunk?.choices?.[0]?.delta;
      if (delta?.usage) {
        totalTokens = Number(delta.usage.total_tokens ?? totalTokens);
        promptTokens = Number(delta.usage.prompt_tokens ?? promptTokens);
        completionTokens = Number(delta.usage.completion_tokens ?? completionTokens);
      }

      yield chunk;
    }
  }

  return {
    stream: wrappedStream(),
    getUsage: async () => {
      // FIX 1: Fallback if provider doesn't return usage
      // Estimate ~4 chars per token, with bounds to prevent absurd values
      const requestedMaxTokens = Number(body?.max_tokens ?? DEFAULT_MAX_TOKENS);
      const maxFallbackTokens = requestedMaxTokens * MAX_FALLBACK_TOKENS_MULTIPLIER;

      // Estimate prompt tokens from message content
      const rawPromptEstimate = Math.ceil(
        (body?.messages ?? []).reduce((acc: number, m: any) => acc + String(m?.content ?? '').length, 0) / 4
      );
      // Estimate completion tokens from streamed content
      const rawCompletionEstimate = Math.ceil(totalContentLength / 4);

      // Apply bounds: min 1 token, max = requested * 2
      const estimatedPromptTokens = clamp(rawPromptEstimate, MIN_FALLBACK_TOKENS, maxFallbackTokens);
      const estimatedCompletionTokens = clamp(rawCompletionEstimate, MIN_FALLBACK_TOKENS, maxFallbackTokens);

      // Use provider values if available, otherwise use bounded estimates
      const finalPromptTokens = promptTokens > 0 ? promptTokens : estimatedPromptTokens;
      const finalCompletionTokens = completionTokens > 0 ? completionTokens : estimatedCompletionTokens;
      const finalTokens = totalTokens > 0 ? totalTokens : (finalPromptTokens + finalCompletionTokens);

      const isFallback = totalTokens === 0;

      return {
        tokens: finalTokens,
        promptTokens: finalPromptTokens,
        completionTokens: finalCompletionTokens,
        provider: providerName,
        // Metadata for debugging/logging
        _fallback: isFallback,
        _chunkCount: chunkCount,
        _contentLength: totalContentLength,
        _bounded: isFallback && (rawCompletionEstimate !== estimatedCompletionTokens),
      };
    },
  };
}
