import { FastifyPluginAsync } from 'fastify';
import { authenticateRequest } from '../../core/auth.js';
import { getAvailableModels } from '../../routing/profiles.js';

export const modelsRoutes: FastifyPluginAsync = async (server) => {
  server.get('/models', {
    // Auth temporarily disabled for testing
    // preHandler: authenticateRequest,
  }, async (request, reply) => {
    const models = getAvailableModels();
    
    return {
      object: 'list',
      data: models.map((model) => ({
        id: model.id,
        object: 'model',
        created: Math.floor(Date.now() / 1000),
        owned_by: 'iafactory',
        permission: [],
        root: model.id,
        parent: null,
        description: model.description,
        pricing: model.pricing,
      })),
    };
  });
};
