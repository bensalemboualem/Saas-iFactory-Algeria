import { createServer } from './server.js';
import { appConfig } from './config.js';

async function start() {
  try {
    const server = await createServer();

    await server.listen({
      port: appConfig.PORT,
      host: appConfig.HOST,
    });

    server.log.info(`🚀 IAFactory Gateway running on ${appConfig.API_BASE_URL}`);
    server.log.info(`📝 Environment: ${appConfig.NODE_ENV}`);
    server.log.info(`🔧 API Docs: ${appConfig.API_BASE_URL}/docs`);
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

start();
