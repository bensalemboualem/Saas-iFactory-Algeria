import Pino from 'pino';

const isDev = process.env.NODE_ENV === 'development';
const isTest = process.env.NODE_ENV === 'test';

/**
 * Logger structuré basé sur Pino
 *
 * Usage recommandé:
 * ```typescript
 * import { logger } from '@/libs/logger';
 *
 * logger.info('User logged in', { userId: '123' });
 * logger.error('Failed to fetch data', { error: err.message });
 * logger.warn('Deprecated API called', { endpoint: '/old' });
 * logger.debug('Cache hit', { key: 'user:123' });
 * ```
 *
 * NE PAS utiliser console.log/error/warn directement en production.
 * Le logger structuré permet:
 * - Filtrage par niveau (LOG_LEVEL env var)
 * - Format JSON pour agrégation (Datadog, ELK, etc.)
 * - Contexte structuré pour debugging
 */
export const pino = Pino({
  level: process.env.LOG_LEVEL || (isDev ? 'debug' : 'info'),
  // En dev, format lisible. En prod, JSON pour parsing
  ...(isDev && {
    transport: {
      options: {
        colorize: true,
        ignore: 'pid,hostname',
        translateTime: 'HH:MM:ss',
      },
      target: 'pino-pretty',
    },
  }),
});

// Alias pratiques
export const logger = {
  // Child logger avec contexte persistant
child: (bindings: Record<string, unknown>) => {
    const child = pino.child(bindings);
    return {
      debug: (msg: string, meta?: Record<string, unknown>) => child.debug(meta, msg),
      error: (msg: string, meta?: Record<string, unknown>) => child.error(meta, msg),
      info: (msg: string, meta?: Record<string, unknown>) => child.info(meta, msg),
      warn: (msg: string, meta?: Record<string, unknown>) => child.warn(meta, msg),
    };
  },
  
debug: (msg: string, meta?: Record<string, unknown>) => pino.debug(meta, msg),
  

error: (msg: string, meta?: Record<string, unknown>) => pino.error(meta, msg),
  

// Pour les erreurs avec stack trace
errorWithStack: (msg: string, error: Error, meta?: Record<string, unknown>) => {
    pino.error({ ...meta, err: error }, msg);
  },
  

info: (msg: string, meta?: Record<string, unknown>) => pino.info(meta, msg),

  
  
trace: (msg: string, meta?: Record<string, unknown>) => pino.trace(meta, msg),

  
  warn: (msg: string, meta?: Record<string, unknown>) => pino.warn(meta, msg),
};

// Silencer en mode test pour ne pas polluer la sortie
if (isTest) {
  pino.level = 'silent';
}

export default logger;
