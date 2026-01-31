/**
 * PR-004: Secure Chat Completions Route
 *
 * Implements reserve-before-stream pattern to prevent:
 * - Streaming bypass (getting data without paying)
 * - Connection abort exploits
 * - TOCTOU race conditions
 *
 * Flow:
 * 1. Reserve credits BEFORE sending any bytes
 * 2. Stream response to client
 * 3. Finalize with actual usage cost
 * 4. On error/abort: release reservation
 */

import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { randomUUID } from 'node:crypto';

import { prisma } from '../../db/client.js';
import { authenticateRequest, type AuthUser } from '../../core/auth.js';
import { GatewayError } from '../../core/errors.js';
import { calculateCostEstimate, calculateFinalCostFromUsage } from '../../core/usage.js';
import { streamChatCompletion } from '../../core/llm/streamChatCompletion.js';
import { CreditsService } from '../../core/credits.service.js';
import { appConfig } from '../../config.js';

// Initialize credits service with prisma
const credits = new CreditsService(prisma);

// Development mode: Skip credit checks if SKIP_CREDIT_CHECK=true
const skipCreditCheck = appConfig.SKIP_CREDIT_CHECK && appConfig.NODE_ENV === 'development';

// Server-side limits to prevent DoS via huge requests
const SERVER_MAX_TOKENS = 16384; // Max completion tokens allowed (increased for large models)
const SERVER_MAX_MESSAGES = 100; // Max messages in context
const SERVER_MAX_MESSAGE_LENGTH = 32000; // Max chars per message (~8k tokens)

// Request validation schema with server-side limits
const chatCompletionSchema = z.object({
  model: z.string(),
  messages: z
    .array(
      z.object({
        role: z.enum(['system', 'user', 'assistant']),
        content: z.string().max(SERVER_MAX_MESSAGE_LENGTH, `Message too long (max ${SERVER_MAX_MESSAGE_LENGTH} chars)`),
      })
    )
    .max(SERVER_MAX_MESSAGES, `Too many messages (max ${SERVER_MAX_MESSAGES})`),
  temperature: z.number().min(0).max(2).optional(),
  max_tokens: z.number().positive().max(SERVER_MAX_TOKENS, `max_tokens exceeds limit (${SERVER_MAX_TOKENS})`).optional(),
  stream: z.boolean().optional().default(false),
  top_p: z.number().min(0).max(1).optional(),
  frequency_penalty: z.number().min(-2).max(2).optional(),
  presence_penalty: z.number().min(-2).max(2).optional(),
});

export const chatCompletionsRoutes: FastifyPluginAsync = async (server) => {
  server.post(
    '/chat/completions',
    {
      preHandler: authenticateRequest,
    },
    async (request, reply) => {
      const user = request.user as AuthUser;
      if (!user?.id) {
        throw new GatewayError('UNAUTHORIZED', 'User not authenticated', 401);
      }

      // Get idempotency key from header or generate one
      const requestId =
        (request.headers['idempotency-key'] as string) ||
        (request.headers['x-request-id'] as string) ||
        randomUUID();

      // Parse and validate request body
      const body = chatCompletionSchema.parse(request.body);

      // Calculate estimated hold amount
      const holdAmount = calculateCostEstimate(body);

      // ============================================================
      // STEP 1: RESERVE CREDITS BEFORE SENDING ANY BYTES
      // (Skipped in development mode if SKIP_CREDIT_CHECK=true)
      // ============================================================
      if (!skipCreditCheck) {
        try {
          await credits.reserve({
            userId: user.id,
            requestId,
            amount: holdAmount,
            ttlSeconds: 300, // 5 min TTL
          });
        } catch (error: any) {
          const msg = String(error?.message ?? '');

          if (msg.includes('INSUFFICIENT_CREDITS')) {
            return reply.status(402).send({
              error: {
                code: 'INSUFFICIENT_CREDITS',
                message: 'Insufficient credits to process this request',
                required: holdAmount,
              },
            });
          }

          request.log.error({ err: error, userId: user.id, requestId }, 'Credits reserve failed');
          throw new GatewayError('CREDITS_ERROR', 'Failed to reserve credits', 500);
        }
      } else {
        request.log.warn({ userId: user.id }, '[DEV MODE] Skipping credit check');
      }

      // ============================================================
      // STREAMING RESPONSE
      // ============================================================
      if (body.stream) {
        // Setup SSE headers
        reply.raw.writeHead(200, {
          'Content-Type': 'text/event-stream; charset=utf-8',
          'Cache-Control': 'no-cache, no-transform',
          Connection: 'keep-alive',
          'X-Request-Id': requestId,
        });

        let finalized = false;
        let clientClosed = false;

        // Handle client disconnect/abort
        request.raw.on('close', async () => {
          clientClosed = true;
          if (!finalized) {
            // Release reservation on abort
            await credits
              .release({ userId: user.id, requestId, reason: 'client_close' })
              .catch((e: unknown) => request.log.warn({ err: e, requestId }, 'Release on abort failed'));
          }
        });

        try {
          // STEP 2: Stream from provider
          const { stream, getUsage } = await streamChatCompletion({
            user,
            requestId,
            body,
          });

          for await (const chunk of stream) {
            if (clientClosed) break;

            // Send chunk to client
            const sseData = `data: ${JSON.stringify(chunk)}\n\n`;
            reply.raw.write(sseData);
          }

          // STEP 3: Finalize with actual usage
          const usage = await getUsage();
          const finalCost = calculateFinalCostFromUsage(usage, body);

          if (!skipCreditCheck) {
            await credits.finalize({
              userId: user.id,
              requestId,
              finalCost,
              reason: 'chat_completion',
              orgId: user.orgId,
            });
          }

          // Write usage ledger entry
          await prisma.usageLedger
            .create({
              data: {
                userId: user.id,
                orgId: user.orgId,
                requestId,
                model: body.model,
                provider: usage.provider,
                tokens: usage.tokens || usage.promptTokens + usage.completionTokens,
                cost: finalCost,
                metadata: {
                  promptTokens: usage.promptTokens,
                  completionTokens: usage.completionTokens,
                },
              },
            })
            .catch((e: unknown) => request.log.warn({ err: e, requestId }, 'UsageLedger write failed'));

          finalized = true;

          // Send done marker
          reply.raw.write(`data: [DONE]\n\n`);
          reply.raw.end();
        } catch (error: any) {
          request.log.error({ err: error, userId: user.id, requestId }, 'Chat stream failed');

          // Release on error
          if (!finalized && !skipCreditCheck) {
            await credits
              .release({ userId: user.id, requestId, reason: 'error' })
              .catch((e: unknown) => request.log.warn({ err: e, requestId }, 'Release on error failed'));
          }

          // Try to send error to client
          try {
            reply.raw.write(`data: ${JSON.stringify({ error: 'STREAM_FAILED' })}\n\n`);
            reply.raw.end();
          } catch {
            // Client already disconnected
          }
        }
      } else {
        // ============================================================
        // NON-STREAMING RESPONSE
        // Build proper completion format from streamed chunks
        // ============================================================
        try {
          const { stream, getUsage } = await streamChatCompletion({
            user,
            requestId,
            body: { ...body, stream: false },
          });

          // Accumulate content from all chunks to build complete response
          let fullContent = '';
          let lastChunk: any = null;
          let finishReason = 'stop';

          for await (const chunk of stream) {
            lastChunk = chunk;
            // Accumulate delta content
            const deltaContent = chunk?.choices?.[0]?.delta?.content;
            if (deltaContent) {
              fullContent += deltaContent;
            }
            // Capture finish reason
            const chunkFinishReason = chunk?.choices?.[0]?.finish_reason;
            if (chunkFinishReason) {
              finishReason = chunkFinishReason;
            }
          }

          // Get usage and finalize
          const usage = await getUsage();
          const finalCost = calculateFinalCostFromUsage(usage, body);

          if (!skipCreditCheck) {
            await credits.finalize({
              userId: user.id,
              requestId,
              finalCost,
              reason: 'chat_completion',
              orgId: user.orgId,
            });
          }

          // Write usage ledger
          await prisma.usageLedger
            .create({
              data: {
                userId: user.id,
                orgId: user.orgId,
                requestId,
                model: body.model,
                provider: usage.provider,
                tokens: usage.tokens || usage.promptTokens + usage.completionTokens,
                cost: finalCost,
                metadata: {
                  promptTokens: usage.promptTokens,
                  completionTokens: usage.completionTokens,
                },
              },
            })
            .catch((e: unknown) => request.log.warn({ err: e, requestId }, 'UsageLedger write failed'));

          // Build proper non-streaming response format (OpenAI spec)
          const response = {
            id: lastChunk?.id || `chatcmpl-${requestId}`,
            object: 'chat.completion',
            created: lastChunk?.created || Math.floor(Date.now() / 1000),
            model: lastChunk?.model || body.model,
            choices: [
              {
                index: 0,
                message: {
                  role: 'assistant',
                  content: fullContent,
                },
                finish_reason: finishReason,
              },
            ],
            usage: {
              prompt_tokens: usage.promptTokens,
              completion_tokens: usage.completionTokens,
              total_tokens: usage.tokens,
            },
          };

          return response;
        } catch (error: unknown) {
          // Release on error
          await credits
            .release({ userId: user.id, requestId, reason: 'error' })
            .catch((e: unknown) => request.log.warn({ err: e, requestId }, 'Release on error failed'));

          throw error;
        }
      }
    }
  );
};
