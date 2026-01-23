import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { z } from 'zod';
import { authenticateRequest, AuthUser } from '../../core/auth.js';
import { SignupService } from '../../core/signup.service.js';
import { GatewayError } from '../../core/errors.js';
import { prisma } from '../../db/client.js';
import { appConfig } from '../../config.js';

const signupService = new SignupService(prisma);

/**
 * Onboarding routes - user self-service endpoints
 */
export async function onboardingRoutes(fastify: FastifyInstance) {
  // All routes require auth
  fastify.addHook('preHandler', authenticateRequest);

  /**
   * POST /onboarding/claim-credits
   * Claim initial signup credits (beta mode)
   * Idempotent: can be called multiple times safely
   */
  fastify.post('/claim-credits', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;

    // Only available in beta mode
    if (appConfig.BILLING_MODE !== 'beta') {
      throw new GatewayError(
        'NOT_AVAILABLE',
        'Credit claiming is only available in beta mode. Use /billing/checkout instead.',
        400
      );
    }

    const result = await signupService.grantSignupCredits(user.id);

    if (result.alreadyGranted) {
      return reply.send({
        success: true,
        message: 'Credits already claimed',
        balance: result.balance,
        alreadyClaimed: true,
      });
    }

    return reply.send({
      success: true,
      message: `Welcome! You received ${result.amount} credits to get started.`,
      granted: result.amount,
      balance: result.balance,
      alreadyClaimed: false,
    });
  });

  /**
   * GET /onboarding/daily-limit
   * Check daily usage limit status (beta mode)
   */
  fastify.get('/daily-limit', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;

    if (appConfig.BILLING_MODE !== 'beta') {
      return reply.send({
        dailyLimit: null,
        message: 'Daily limits only apply in beta mode',
      });
    }

    const limit = await signupService.checkDailyLimit(user.id);

    return reply.send({
      dailyLimit: limit.dailyLimit,
      usedToday: limit.usedToday,
      remaining: limit.remaining,
      allowed: limit.allowed,
      resetsAt: getNextMidnightUTC(),
    });
  });

  /**
   * GET /onboarding/status
   * Get user onboarding status
   */
  fastify.get('/status', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;

    // Check if user has claimed credits
    const signupGrant = await prisma.creditTransaction.findFirst({
      where: {
        userId: user.id,
        idempotencyKey: `signup_grant_${user.id}`,
      },
    });

    const wallet = await prisma.creditWallet.findUnique({
      where: { userId: user.id },
    });

    return reply.send({
      userId: user.id,
      billingMode: appConfig.BILLING_MODE,
      hasClaimedCredits: !!signupGrant,
      hasWallet: !!wallet,
      balance: wallet?.balance ?? 0,
      signupCreditsAmount: appConfig.BETA_SIGNUP_CREDITS,
      dailyLimit: appConfig.BILLING_MODE === 'beta' ? appConfig.BETA_DAILY_LIMIT : null,
    });
  });
}

function getNextMidnightUTC(): string {
  const tomorrow = new Date();
  tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
  tomorrow.setUTCHours(0, 0, 0, 0);
  return tomorrow.toISOString();
}
