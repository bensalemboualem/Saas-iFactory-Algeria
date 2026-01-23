import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';

// Routes
import health from './routes/health.js';
import collections from './routes/collections.js';
import documents from './routes/documents.js';
import capture from './routes/capture.js';
import search from './routes/search.js';
import ask from './routes/ask.js';
import sync from './routes/sync.js';

export interface AppOptions {
  enableLogger?: boolean;
}

/**
 * Create the Hono app instance
 * Separated from index.ts for testability
 */
export function createApp(options: AppOptions = {}): Hono {
  const app = new Hono();

  // Global middleware
  if (options.enableLogger !== false) {
    app.use('*', logger());
  }
  app.use('*', prettyJSON());
  app.use(
    '*',
    cors({
      origin: ['http://localhost:5173', 'http://localhost:3000', 'https://iafactory.dz'],
      credentials: true,
      allowHeaders: ['Content-Type', 'Authorization'],
      allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    })
  );

  // Mount routes
  app.route('/health', health);
  app.route('/api/collections', collections);
  app.route('/api/documents', documents);
  app.route('/api/capture', capture);
  app.route('/api/search', search);
  app.route('/api/ask', ask);
  app.route('/api/sync', sync);

  // Root endpoint
  app.get('/', (c) => {
    return c.json({
      name: 'Dzir IA Backend',
      version: '0.1.0',
      description: 'Second Brain / Knowledge Management API',
      docs: '/health',
      endpoints: {
        health: 'GET /health',
        collections: 'GET/POST /api/collections',
        documents: 'GET/DELETE /api/documents',
        capture: 'POST /api/capture',
        search: 'GET/POST /api/search',
        ask: 'POST /api/ask',
        sync: 'POST /api/sync',
      },
    });
  });

  // 404 handler
  app.notFound((c) => {
    return c.json({ error: 'Not Found', path: c.req.path }, 404);
  });

  // Error handler
  app.onError((err, c) => {
    console.error('Unhandled error:', err);
    return c.json(
      {
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined,
      },
      500
    );
  });

  return app;
}
