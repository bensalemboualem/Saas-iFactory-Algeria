import 'dotenv/config';
import { serve } from '@hono/node-server';
import { createApp } from './app.js';

// Services
import { initializeDatabase, closeDatabase } from './services/sqlite.js';
import { initializeQdrant } from './services/qdrant.js';
import { initializeMinio } from './services/minio.js';

const app = createApp();

// Initialize services and start server
async function main() {
  const PORT = parseInt(process.env.PORT || '4000');

  console.log('Initializing services...');

  try {
    // Initialize SQLite
    initializeDatabase();
    console.log('SQLite initialized');

    // Initialize Qdrant (may fail if not running - that's ok for dev)
    try {
      await initializeQdrant();
      console.log('Qdrant initialized');
    } catch (error) {
      console.warn('Qdrant not available:', error);
      console.warn('Vector search will not work until Qdrant is started');
    }

    // Initialize MinIO (may fail if not running - that's ok for dev)
    try {
      await initializeMinio();
      console.log('MinIO initialized');
    } catch (error) {
      console.warn('MinIO not available:', error);
      console.warn('File storage will not work until MinIO is started');
    }

    // Start server
    console.log(`Starting Dzir IA Backend on port ${PORT}...`);
    serve({
      fetch: app.fetch,
      port: PORT,
    });

    console.log(`
╔══════════════════════════════════════════╗
║         Dzir IA Backend Ready            ║
║──────────────────────────────────────────║
║  Local:   http://localhost:${PORT}          ║
║  Health:  http://localhost:${PORT}/health   ║
╚══════════════════════════════════════════╝
    `);
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  closeDatabase();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\nShutting down...');
  closeDatabase();
  process.exit(0);
});

main();
