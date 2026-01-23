import { createServer } from './server.js';
import { appConfig } from './config.js';
import { startCleanupWorker, stopCleanupWorker } from './workers/cleanupWorker.js';

async function start() {
  try {
    const server = await createServer();

    await server.listen({
      port: appConfig.PORT,
      host: appConfig.HOST,
    });

    const actualUrl = `http://${appConfig.HOST === '0.0.0.0' ? 'localhost' : appConfig.HOST}:${appConfig.PORT}`;
    server.log.info(`IAFactory Gateway running on ${actualUrl}`);
    server.log.info(`Environment: ${appConfig.NODE_ENV}`);

    // Start background workers
    startCleanupWorker();

    // Graceful shutdown
    const shutdown = async (signal: string) => {
      server.log.info(`${signal} received, shutting down...`);
      stopCleanupWorker();
      await server.close();
      process.exit(0);
    };

    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();
