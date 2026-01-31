import Fastify from 'fastify';
import cors from '@fastify/cors';
import rateLimit from '@fastify/rate-limit';
import Redis from 'ioredis';
import { appConfig } from './config.js';
import { errorHandler } from './core/errors.js';

// Routes
import { healthRoutes } from './api/v1/health.js';
import { modelsRoutes } from './api/v1/models.js';
import { chatCompletionsRoutes } from './api/v1/chatCompletions.js';
import { creditsRoutes } from './api/v1/credits.js';
import { billingRoutes } from './api/v1/billing.js';
import { onboardingRoutes } from './api/v1/onboarding.js';
import { oauthRoutes } from './api/v1/oauth.js';

/**
 * Create Redis client for rate limiting (optional)
 * Returns undefined if Redis is not configured or unavailable
 */
function createRedisClient(): Redis | undefined {
  if (!appConfig.REDIS_URL) {
    console.log('[Server] No REDIS_URL configured, using in-memory rate limiting');
    return undefined;
  }

  try {
    const client = new Redis(appConfig.REDIS_URL, {
      maxRetriesPerRequest: 1,
      enableOfflineQueue: false,
      lazyConnect: true,
    });

    client.on('error', (err) => {
      console.warn('[Redis] Connection error:', err.message);
    });

    return client;
  } catch (err) {
    console.warn('[Redis] Failed to initialize:', err);
    return undefined;
  }
}

export async function createServer() {
  const server = Fastify({
    logger: {
      level: appConfig.LOG_LEVEL,
      transport: appConfig.LOG_PRETTY
        ? {
            target: 'pino-pretty',
            options: {
              colorize: true,
              translateTime: 'HH:MM:ss',
              ignore: 'pid,hostname',
            },
          }
        : undefined,
    },
    trustProxy: true,
  });

  // CORS
  await server.register(cors, {
    origin: appConfig.NODE_ENV === 'production'
      ? ['https://iafactory.dz', 'https://chat.iafactory.dz']
      : true,
    credentials: true,
  });

  // Rate Limiting (global) - uses Redis if available, otherwise in-memory
  const redisClient = createRedisClient();
  await server.register(rateLimit, {
    max: appConfig.RATE_LIMIT_MAX_REQUESTS || 100,
    timeWindow: appConfig.RATE_LIMIT_WINDOW_MS || 60000,
    ...(redisClient ? { redis: redisClient } : {}),
  });

  // Error handler
  server.setErrorHandler(errorHandler);

  // Root welcome
  server.get('/', async (request, reply) => {
    return {
      name: 'IAFactory Gateway',
      version: '1.0.0',
      status: 'running',
      billingMode: appConfig.BILLING_MODE,
      endpoints: {
        health: '/health',
        models: '/v1/models',
        chat: '/v1/chat/completions',
        credits: '/api/credits/*',
        billing: '/billing/*',
        onboarding: '/onboarding/*',
      },
      docs: 'https://github.com/iafactory/gateway',
    };
  });

  // Health check (no auth)
  await server.register(healthRoutes, { prefix: '/health' });

  // OpenAI-compatible API v1
  await server.register(modelsRoutes, { prefix: '/v1' });
  await server.register(chatCompletionsRoutes, { prefix: '/v1' });

  // Credits API
  await server.register(creditsRoutes, { prefix: '/api/credits' });

  // Billing API (disabled in beta mode)
  await server.register(billingRoutes, { prefix: '/billing' });

  // Onboarding API (signup credits, daily limits)
  await server.register(onboardingRoutes, { prefix: '/onboarding' });

  // OAuth routes (Google, GitHub)
  await server.register(oauthRoutes);

  return server;
}
