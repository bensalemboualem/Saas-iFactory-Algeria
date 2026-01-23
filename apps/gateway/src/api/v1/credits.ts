import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { randomUUID } from 'crypto';
import { z } from 'zod';
import { authenticateRequest, AuthUser } from '../../core/auth.js';
import { getBalance } from '../../core/credits.js';
import { CreditsService } from '../../core/credits.service.js';
import { GatewayError } from '../../core/errors.js';
import { prisma } from '../../db/client.js';
import { appConfig } from '../../config.js';

// Initialize credits service
const creditsService = new CreditsService(prisma);

// ============ Schemas ============

const CheckCreditsSchema = z.object({
  operation: z.string().min(1),
  cost: z.number().positive(),
});

const DeductCreditsSchema = z.object({
  operation: z.string().min(1),
  cost: z.number().positive(),
  idempotencyKey: z.string().min(1),
});

// PR-003: Reserve/Finalize/Release schemas
const ReserveCreditsSchema = z.object({
  amount: z.number().positive(),
  ttlSeconds: z.number().int().positive().max(600).optional(), // max 10 min
});

const FinalizeCreditsSchema = z.object({
  requestId: z.string().min(1),
  finalCost: z.number().nonnegative(),
  reason: z.string().optional(),
});

const ReleaseCreditsSchema = z.object({
  requestId: z.string().min(1),
  reason: z.enum(['client_abort', 'error', 'timeout', 'manual']).optional(),
});

type CheckCreditsBody = z.infer<typeof CheckCreditsSchema>;
type DeductCreditsBody = z.infer<typeof DeductCreditsSchema>;
type ReserveCreditsBody = z.infer<typeof ReserveCreditsSchema>;
type FinalizeCreditsBody = z.infer<typeof FinalizeCreditsSchema>;
type ReleaseCreditsBody = z.infer<typeof ReleaseCreditsSchema>;

// ============ Routes ============

export async function creditsRoutes(fastify: FastifyInstance) {
  // Apply auth to all routes
  fastify.addHook('preHandler', authenticateRequest);

  /**
   * GET /api/credits/balance
   * Get current user's credit balance
   */
  fastify.get('/balance', async (request: FastifyRequest, reply: FastifyReply) => {
    const user = request.user as AuthUser;
    const balance = await getBalance(user.id);

    return reply.send({
      balance,
    });
  });

  /**
   * POST /api/credits/check
   * Check if user has sufficient credits (read-only)
   */
  fastify.post<{ Body: CheckCreditsBody }>(
    '/check',
    {
      schema: {
        body: {
          type: 'object',
          required: ['operation', 'cost'],
          properties: {
            operation: { type: 'string', minLength: 1 },
            cost: { type: 'number', minimum: 0.01 },
          },
        },
      },
    },
    async (request, reply) => {
      const user = request.user as AuthUser;

      // Validate with zod for better error messages
      const parsed = CheckCreditsSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { cost } = parsed.data;
      const balance = await getBalance(user.id);
      const allowed = balance >= cost;

      if (!allowed) {
        return reply.status(402).send({
          error: 'INSUFFICIENT_CREDITS',
          message: `Insufficient credits. Required: ${cost}, available: ${balance}`,
          allowed: false,
          balance,
          required: cost,
        });
      }

      return reply.send({
        allowed: true,
        balance,
      });
    }
  );

  /**
   * POST /api/credits/deduct
   * Deduct credits from user's wallet (with idempotency)
   */
  fastify.post<{ Body: DeductCreditsBody }>(
    '/deduct',
    {
      schema: {
        body: {
          type: 'object',
          required: ['operation', 'cost', 'idempotencyKey'],
          properties: {
            operation: { type: 'string', minLength: 1 },
            cost: { type: 'number', minimum: 0.01 },
            idempotencyKey: { type: 'string', minLength: 1 },
          },
        },
      },
    },
    async (request, reply) => {
      const user = request.user as AuthUser;

      // Validate with zod
      const parsed = DeductCreditsSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { operation, cost, idempotencyKey } = parsed.data;

      // Check for existing transaction with same idempotency key
      const existing = await prisma.creditTransaction.findFirst({
        where: {
          userId: user.id,
          idempotencyKey,
        },
      });

      if (existing) {
        // Already processed - return success with current balance
        const balance = await getBalance(user.id);
        return reply.send({
          success: true,
          newBalance: balance,
          transactionId: existing.id,
          idempotent: true,
        });
      }

      // Get wallet
      const wallet = await prisma.creditWallet.findUnique({
        where: { userId: user.id },
      });

      if (!wallet) {
        throw new GatewayError('USER_NOT_FOUND', 'User wallet not found', 404);
      }

      // Check balance
      if (wallet.balance < cost) {
        return reply.status(402).send({
          error: 'INSUFFICIENT_CREDITS',
          message: `Insufficient credits. Required: ${cost}, available: ${wallet.balance}`,
          success: false,
          balance: wallet.balance,
          required: cost,
        });
      }

      // Atomic transaction: debit wallet + create transaction record
      const transactionId = randomUUID();
      const [updatedWallet] = await prisma.$transaction([
        prisma.creditWallet.update({
          where: { id: wallet.id },
          data: { balance: { decrement: cost } },
        }),
        prisma.creditTransaction.create({
          data: {
            id: transactionId,
            userId: user.id,
            orgId: user.orgId,
            amount: -cost,
            type: 'debit',
            reason: operation,
            idempotencyKey,
          },
        }),
        prisma.usageLedger.create({
          data: {
            userId: user.id,
            orgId: user.orgId,
            model: 'dzir-ia',
            provider: 'dzir-ia',
            tokens: 0,
            cost,
            metadata: { operation, idempotencyKey },
          },
        }),
      ]);

      return reply.send({
        success: true,
        newBalance: updatedWallet.balance,
        transactionId,
      });
    }
  );

  // ============ Atomic Reserve/Finalize/Release (PR-003) ============
  // These endpoints enable the atomic pattern used by dzir-ia and other services

  /**
   * POST /api/credits/reserve
   * Reserve credits BEFORE starting costly work (LLM streaming).
   * Returns a requestId that MUST be passed to finalize/release.
   */
  fastify.post<{ Body: ReserveCreditsBody }>(
    '/reserve',
    {
      schema: {
        body: {
          type: 'object',
          required: ['amount'],
          properties: {
            amount: { type: 'number', minimum: 0.01 },
            ttlSeconds: { type: 'number', minimum: 1, maximum: 600 },
          },
        },
      },
    },
    async (request, reply) => {
      const user = request.user as AuthUser;

      const parsed = ReserveCreditsSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { amount, ttlSeconds } = parsed.data;

      // Generate unique request ID (client can also provide via header)
      const requestId = request.headers['idempotency-key'] as string || randomUUID();

      try {
        const reservation = await creditsService.reserve({
          userId: user.id,
          requestId,
          amount,
          ttlSeconds,
        });

        return reply.status(201).send({
          requestId: reservation.requestId,
          userId: reservation.userId,
          amount: reservation.amount,
          status: reservation.status,
          expiresAt: reservation.expiresAt,
        });
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error';

        if (message === 'INSUFFICIENT_CREDITS') {
          const balance = await getBalance(user.id);
          return reply.status(402).send({
            error: 'INSUFFICIENT_CREDITS',
            message: `Insufficient credits. Required: ${amount}, available: ${balance}`,
            balance,
            required: amount,
          });
        }

        throw new GatewayError('RESERVATION_FAILED', message, 500);
      }
    }
  );

  /**
   * GET /api/credits/reservation/:requestId
   * Get reservation status (used by dzir-ia to validate x-reservation-id header).
   */
  fastify.get<{ Params: { requestId: string } }>(
    '/reservation/:requestId',
    async (request, reply) => {
      const user = request.user as AuthUser;
      const { requestId } = request.params;

      const reservation = await prisma.creditReservation.findUnique({
        where: { requestId },
      });

      if (!reservation) {
        return reply.status(404).send({
          error: 'NOT_FOUND',
          message: 'Reservation not found',
        });
      }

      // Ownership check
      if (reservation.userId !== user.id) {
        return reply.status(403).send({
          error: 'FORBIDDEN',
          message: 'Reservation belongs to another user',
        });
      }

      return reply.send({
        requestId: reservation.requestId,
        userId: reservation.userId,
        amount: reservation.amount,
        status: reservation.status,
        expiresAt: reservation.expiresAt,
        createdAt: reservation.createdAt,
      });
    }
  );

  /**
   * POST /api/credits/finalize
   * Convert reserved credits to actual debit. Refunds any unused portion.
   */
  fastify.post<{ Body: FinalizeCreditsBody }>(
    '/finalize',
    {
      schema: {
        body: {
          type: 'object',
          required: ['requestId', 'finalCost'],
          properties: {
            requestId: { type: 'string', minLength: 1 },
            finalCost: { type: 'number', minimum: 0 },
            reason: { type: 'string' },
          },
        },
      },
    },
    async (request, reply) => {
      const user = request.user as AuthUser;

      const parsed = FinalizeCreditsSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { requestId, finalCost, reason } = parsed.data;

      try {
        const result = await creditsService.finalize({
          userId: user.id,
          requestId,
          finalCost,
          reason: reason || 'api_call',
          orgId: user.orgId,
        });

        return reply.send({
          status: result.status,
          debit: result.debit,
          refund: result.refund,
        });
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error';

        if (message === 'RESERVATION_NOT_FOUND') {
          return reply.status(404).send({
            error: 'RESERVATION_NOT_FOUND',
            message: 'Reservation not found. It may have expired.',
          });
        }

        if (message === 'RESERVATION_OWNER_MISMATCH') {
          return reply.status(403).send({
            error: 'FORBIDDEN',
            message: 'Reservation belongs to another user',
          });
        }

        if (message === 'RESERVATION_ALREADY_RELEASED') {
          return reply.status(409).send({
            error: 'ALREADY_RELEASED',
            message: 'Reservation was already released (refunded)',
          });
        }

        throw new GatewayError('FINALIZE_FAILED', message, 500);
      }
    }
  );

  /**
   * POST /api/credits/release
   * Release reserved credits (full refund). Use on error/abort.
   */
  fastify.post<{ Body: ReleaseCreditsBody }>(
    '/release',
    {
      schema: {
        body: {
          type: 'object',
          required: ['requestId'],
          properties: {
            requestId: { type: 'string', minLength: 1 },
            reason: { type: 'string', enum: ['client_abort', 'error', 'timeout', 'manual'] },
          },
        },
      },
    },
    async (request, reply) => {
      const user = request.user as AuthUser;

      const parsed = ReleaseCreditsSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { requestId, reason } = parsed.data;

      try {
        const result = await creditsService.release({
          userId: user.id,
          requestId,
          reason: reason as 'client_close' | 'error' | 'ttl_expired' | 'manual' | undefined,
        });

        return reply.send({
          status: result.status,
          message: result.status === 'OK' ? 'Credits released successfully' : 'Nothing to release',
        });
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error';

        if (message === 'RESERVATION_OWNER_MISMATCH') {
          return reply.status(403).send({
            error: 'FORBIDDEN',
            message: 'Reservation belongs to another user',
          });
        }

        throw new GatewayError('RELEASE_FAILED', message, 500);
      }
    }
  );

  // ============ Admin Endpoints (PR-003 FIX 2) ============
  // Rate limited and auth protected

  /** Admin auth check helper */
  function requireAdmin(user: AuthUser) {
    // In production: use proper RBAC with roles from DB
    const isAdmin = user.email?.includes('admin') || user.email?.includes('@iafactory');
    if (!isAdmin) {
      throw new GatewayError('FORBIDDEN', 'Admin access required', 403);
    }
  }

  /** Check admin API key (for machine-to-machine calls) */
  function checkAdminApiKey(request: FastifyRequest): boolean {
    if (!appConfig.ADMIN_API_KEY) return false;
    const authHeader = request.headers['x-admin-api-key'];
    return authHeader === appConfig.ADMIN_API_KEY;
  }

  /** Check if request IP is in admin allowlist */
  function checkAdminIp(request: FastifyRequest): boolean {
    const allowedIps = appConfig.ADMIN_ALLOWED_IPS.split(',').map((ip) => ip.trim());
    const clientIp = request.ip || request.headers['x-forwarded-for'] || '';
    const ipStr = Array.isArray(clientIp) ? clientIp[0] : clientIp;
    return allowedIps.includes(ipStr) || allowedIps.includes('*');
  }

  /**
   * GET /api/credits/admin/reservations
   * Get stats about current reservations (requires admin)
   * Rate limit: 10 requests per minute
   */
  fastify.get(
    '/admin/reservations',
    {
      config: {
        rateLimit: {
          max: 10,
          timeWindow: '1 minute',
        },
      },
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      const user = request.user as AuthUser;
      requireAdmin(user);

      const now = new Date();

      const [total, reserved, finalized, released, expired] = await Promise.all([
        prisma.creditReservation.count(),
        prisma.creditReservation.count({ where: { status: 'RESERVED' } }),
        prisma.creditReservation.count({ where: { status: 'FINALIZED' } }),
        prisma.creditReservation.count({ where: { status: 'RELEASED' } }),
        prisma.creditReservation.count({
          where: { status: 'RESERVED', expiresAt: { lt: now } },
        }),
      ]);

      // Log admin access for audit
      request.log.info({ userId: user.id, action: 'view_reservations' }, 'Admin action');

      return reply.send({
        total,
        reserved,
        finalized,
        released,
        expiredPending: expired,
      });
    }
  );

  /**
   * POST /api/credits/admin/cleanup
   * Manually trigger cleanup of expired reservations (requires admin)
   * Rate limit: 2 requests per minute (destructive action)
   */
  fastify.post(
    '/admin/cleanup',
    {
      config: {
        rateLimit: {
          max: 2,
          timeWindow: '1 minute',
        },
      },
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      const user = request.user as AuthUser;
      requireAdmin(user);

      const result = await creditsService.cleanupExpired();

      // Log admin action for audit
      request.log.info(
        { userId: user.id, action: 'cleanup_reservations', cleaned: result.cleaned },
        'Admin action'
      );

      return reply.send({
        success: true,
        cleaned: result.cleaned,
      });
    }
  );

  // ============ Admin Top-Up Endpoint (PR-BETA-003) ============

  const AdminTopUpSchema = z.object({
    userId: z.string().optional(),
    email: z.string().email().optional(),
    amount: z.number().positive().max(1000),
    reason: z.string().min(1).max(200),
  }).refine((data) => data.userId || data.email, {
    message: 'Either userId or email must be provided',
  });

  type AdminTopUpBody = z.infer<typeof AdminTopUpSchema>;

  /**
   * POST /api/credits/admin/topup
   * Add credits to a user's wallet (admin only)
   * Auth: Either admin user JWT OR x-admin-api-key header + IP allowlist
   * Rate limit: 20 requests per minute
   */
  fastify.post<{ Body: AdminTopUpBody }>(
    '/admin/topup',
    {
      config: {
        rateLimit: {
          max: 20,
          timeWindow: '1 minute',
        },
      },
    },
    async (request: FastifyRequest<{ Body: AdminTopUpBody }>, reply: FastifyReply) => {
      // Auth: check either user is admin OR valid API key + IP
      const hasApiKeyAuth = checkAdminApiKey(request) && checkAdminIp(request);
      const user = request.user as AuthUser | undefined;

      if (!hasApiKeyAuth) {
        if (!user) {
          throw new GatewayError('UNAUTHORIZED', 'Authentication required', 401);
        }
        requireAdmin(user);
      }

      // Validate body
      const parsed = AdminTopUpSchema.safeParse(request.body);
      if (!parsed.success) {
        throw new GatewayError('INVALID_REQUEST', parsed.error.message, 400);
      }

      const { userId, email, amount, reason } = parsed.data;

      // Find user by id or email
      let targetUserId = userId;
      if (!targetUserId && email) {
        const targetUser = await prisma.user.findFirst({
          where: { email },
          select: { id: true },
        });
        if (!targetUser) {
          throw new GatewayError('USER_NOT_FOUND', `User with email ${email} not found`, 404);
        }
        targetUserId = targetUser.id;
      }

      if (!targetUserId) {
        throw new GatewayError('INVALID_REQUEST', 'Could not determine target user', 400);
      }

      // Ensure wallet exists
      let wallet = await prisma.creditWallet.findUnique({
        where: { userId: targetUserId },
      });

      if (!wallet) {
        // Create wallet with 0 balance
        wallet = await prisma.creditWallet.create({
          data: { userId: targetUserId, balance: 0 },
        });
      }

      // Idempotency key for admin top-up
      const idempotencyKey = `admin_topup_${targetUserId}_${Date.now()}`;
      const transactionId = randomUUID();

      // Atomic credit transaction
      const [updatedWallet] = await prisma.$transaction([
        prisma.creditWallet.update({
          where: { id: wallet.id },
          data: { balance: { increment: amount } },
        }),
        prisma.creditTransaction.create({
          data: {
            id: transactionId,
            userId: targetUserId,
            amount: amount,
            type: 'credit',
            reason: `[ADMIN] ${reason}`,
            idempotencyKey,
          },
        }),
      ]);

      // Audit log
      const adminId = user?.id || 'api_key';
      request.log.info(
        {
          adminId,
          action: 'admin_topup',
          targetUserId,
          amount,
          reason,
          transactionId,
          newBalance: updatedWallet.balance,
        },
        '[Admin] Credit top-up'
      );

      return reply.send({
        success: true,
        transactionId,
        targetUserId,
        amount,
        newBalance: updatedWallet.balance,
      });
    }
  );

  /**
   * GET /api/credits/admin/user/:userId
   * Get a user's credit info (admin only)
   */
  fastify.get<{ Params: { userId: string } }>(
    '/admin/user/:userId',
    {
      config: {
        rateLimit: {
          max: 30,
          timeWindow: '1 minute',
        },
      },
    },
    async (request: FastifyRequest<{ Params: { userId: string } }>, reply: FastifyReply) => {
      const hasApiKeyAuth = checkAdminApiKey(request) && checkAdminIp(request);
      const user = request.user as AuthUser | undefined;

      if (!hasApiKeyAuth) {
        if (!user) {
          throw new GatewayError('UNAUTHORIZED', 'Authentication required', 401);
        }
        requireAdmin(user);
      }

      const { userId: targetUserId } = request.params;

      const wallet = await prisma.creditWallet.findUnique({
        where: { userId: targetUserId },
      });

      const recentTransactions = await prisma.creditTransaction.findMany({
        where: { userId: targetUserId },
        orderBy: { createdAt: 'desc' },
        take: 10,
      });

      const activeReservations = await prisma.creditReservation.findMany({
        where: { userId: targetUserId, status: 'RESERVED' },
      });

      return reply.send({
        userId: targetUserId,
        balance: wallet?.balance ?? 0,
        walletExists: !!wallet,
        recentTransactions,
        activeReservations,
      });
    }
  );
}
