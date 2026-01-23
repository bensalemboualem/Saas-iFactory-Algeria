import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { appConfig } from '../../config.js';
import { authenticateRequest, AuthUser } from '../../core/auth.js';
import { GatewayError } from '../../core/errors.js';

/**
 * Billing routes - disabled in beta mode
 * These will be enabled when BILLING_MODE=chargily or stripe
 */
export async function billingRoutes(fastify: FastifyInstance) {
  // Check billing mode on all routes
  fastify.addHook('preHandler', async (request, reply) => {
    if (appConfig.BILLING_MODE === 'beta') {
      throw new GatewayError(
        'BILLING_DISABLED',
        'Billing is disabled in beta mode. Contact admin for credits.',
        501
      );
    }
  });

  // Apply auth
  fastify.addHook('preHandler', authenticateRequest);

  /**
   * POST /billing/checkout
   * Create a checkout session (Chargily/Stripe)
   * Disabled in beta mode
   */
  fastify.post('/checkout', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;

    // This will be implemented when BILLING_MODE != beta
    // For now, return placeholder
    return reply.status(501).send({
      error: 'NOT_IMPLEMENTED',
      message: 'Checkout not yet implemented. Set BILLING_MODE=chargily to enable.',
    });
  });

  /**
   * POST /billing/webhook
   * Handle payment provider webhooks
   * Disabled in beta mode
   */
  fastify.post('/webhook', async (request: FastifyRequest, reply: FastifyReply) => {
    // This will be implemented when BILLING_MODE != beta
    return reply.status(501).send({
      error: 'NOT_IMPLEMENTED',
      message: 'Webhook not yet implemented.',
    });
  });

  /**
   * GET /billing/history
   * Get payment history
   */
  fastify.get('/history', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;

    // Placeholder - will return real history when billing is enabled
    return reply.send({
      payments: [],
      message: 'Billing is in beta mode. No payment history available.',
    });
  });
}
