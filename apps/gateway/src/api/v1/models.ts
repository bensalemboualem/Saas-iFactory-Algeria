import { FastifyPluginAsync } from 'fastify';
import { authenticateRequest } from '../../core/auth.js';
import { getAvailableModels } from '../../routing/profiles.js';

export const modelsRoutes: FastifyPluginAsync = async (server) => {
  server.get('/models', {
    preHandler: authenticateRequest,
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
        // Return proper display name for UI
        name: model.name,
        description: `${model.name} - ${model.description}`,
        pricing: model.pricing,
        category: model.category,
        contextWindow: model.contextWindow,
        features: model.features,
      })),
    };
  });
};
