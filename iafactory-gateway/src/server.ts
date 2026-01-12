import Fastify from 'fastify';
import cors from '@fastify/cors';
import rateLimit from '@fastify/rate-limit';
import { appConfig } from './config.js';
import { errorHandler } from './core/errors.js';

// Routes
import { healthRoutes } from './api/v1/health.js';
import { modelsRoutes } from './api/v1/models.js';
import { chatCompletionsRoutes } from './api/v1/chatCompletions.js';

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

  // Rate Limiting (global) - Disabled until Redis is running
  // await server.register(rateLimit, {
  //   max: appConfig.RATE_LIMIT_MAX_REQUESTS,
  //   timeWindow: appConfig.RATE_LIMIT_WINDOW_MS,
  //   redis: appConfig.REDIS_URL,
  // });

  // Error handler
  server.setErrorHandler(errorHandler);

  // Root welcome
  server.get('/', async (request, reply) => {
    return {
      name: 'IAFactory Gateway',
      version: '1.0.0',
      status: 'running',
      endpoints: {
        health: '/health',
        models: '/v1/models',
        chat: '/v1/chat/completions',
      },
      docs: 'https://github.com/iafactory/gateway',
    };
  });

  // Health check (no auth)
  await server.register(healthRoutes, { prefix: '/health' });

  // OpenAI-compatible API v1
  await server.register(modelsRoutes, { prefix: '/v1' });
  await server.register(chatCompletionsRoutes, { prefix: '/v1' });

  return server;
}
