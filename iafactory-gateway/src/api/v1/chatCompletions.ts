import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { authenticateRequest } from '../../core/auth.js';
import { checkAndDebitCredits } from '../../core/credits.js';
import { routeRequest } from '../../routing/router.js';
import { createSSEStream } from '../../core/sse.js';
import { GatewayError } from '../../core/errors.js';

const chatCompletionSchema = z.object({
  model: z.string(),
  messages: z.array(z.object({
    role: z.enum(['system', 'user', 'assistant']),
    content: z.string(),
  })),
  temperature: z.number().min(0).max(2).optional(),
  max_tokens: z.number().positive().optional(),
  stream: z.boolean().optional().default(false),
  top_p: z.number().min(0).max(1).optional(),
  frequency_penalty: z.number().min(-2).max(2).optional(),
  presence_penalty: z.number().min(-2).max(2).optional(),
});

export const chatCompletionsRoutes: FastifyPluginAsync = async (server) => {
  server.post('/chat/completions', {
    // Auth temporarily disabled for testing
    // preHandler: authenticateRequest,
  }, async (request, reply) => {
    // Mock user for testing
    const user = { id: 'test-user', orgId: 'test-org', email: 'test@iafactory.dz', role: 'admin' };
    // const user = (request as any).user;
    
    // Parse and validate request body
    const body = chatCompletionSchema.parse(request.body);

    // Credits check temporarily disabled for testing
    // const hasCredits = await checkAndDebitCredits(user.id, body.model, 'reserve');
    // if (!hasCredits) {
    //   throw new GatewayError('INSUFFICIENT_CREDITS', 'Insufficient credits to process this request');
    // }

    try {
      // Route request to appropriate provider
      const { provider, stream } = await routeRequest(body, user);

      if (body.stream) {
        // SSE Streaming
        reply.raw.writeHead(200, {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        });

        let totalTokens = 0;

        for await (const chunk of stream) {
          const sseData = createSSEStream(chunk);
          reply.raw.write(sseData);
          
          if (chunk.usage) {
            totalTokens = chunk.usage.total_tokens || 0;
          }
        }

        // Credits debit disabled for testing
        // await checkAndDebitCredits(user.id, body.model, 'debit', totalTokens);

        reply.raw.write('data: [DONE]\n\n');
        reply.raw.end();
        return;
      } else {
        // Non-streaming
        const response = await provider.complete(body);
        
        // Credits debit disabled for testing
        // await checkAndDebitCredits(
        //   user.id,
        //   body.model,
        //   'debit',
        //   response.usage?.total_tokens || 0
        // );

        return response;
      }
    } catch (error) {
      // Release reserved credits on error
      // await checkAndDebitCredits(user.id, body.model, 'release');
      throw error;
    }
  });
};
