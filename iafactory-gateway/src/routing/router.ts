import { getModelById, getDefaultModel, ModelProfile } from './profiles.js';
import { GatewayError } from '../core/errors.js';
import { GroqProvider } from '../providers/groq.js';
import { OpenRouterProvider } from '../providers/openrouter.js';
import { DeepSeekProvider } from '../providers/deepseek.js';
import { OllamaProvider } from '../providers/local.js';
import type { BaseProvider } from '../providers/types.js';
import type { AuthUser } from '../core/auth.js';

export async function routeRequest(
  request: any,
  user: AuthUser
): Promise<{ provider: BaseProvider; stream: any }> {
  // Get model profile
  const modelId = request.model || getDefaultModel().id;
  const profile = getModelById(modelId);

  if (!profile) {
    throw new GatewayError('INVALID_MODEL', `Model ${modelId} not found`, 400);
  }

  // Select provider based on profile
  const provider = getProvider(profile);

  // Map IAFactory model to actual provider model
  const providerRequest = {
    ...request,
    model: profile.actualModel,
  };

  // Execute request with fallback
  try {
    if (request.stream) {
      const stream = provider.streamComplete(providerRequest);
      return { provider, stream };
    } else {
      const response = await provider.complete(providerRequest);
      return { provider, stream: null };
    }
  } catch (error: any) {
    // Fallback logic (optional)
    if (shouldFallback(error, profile)) {
      return await fallbackRequest(providerRequest, profile, user);
    }
    throw error;
  }
}

function getProvider(profile: ModelProfile): BaseProvider {
  switch (profile.provider) {
    case 'groq':
      return new GroqProvider();
    case 'openrouter':
      return new OpenRouterProvider();
    case 'deepseek':
      return new DeepSeekProvider();
    case 'ollama':
      return new OllamaProvider();
    default:
      throw new GatewayError('INVALID_PROVIDER', `Provider ${profile.provider} not supported`, 500);
  }
}

function shouldFallback(error: any, profile: ModelProfile): boolean {
  // Fallback on rate limits or provider outages
  return error.status === 429 || error.status === 503;
}

async function fallbackRequest(
  request: any,
  originalProfile: ModelProfile,
  user: AuthUser
): Promise<{ provider: BaseProvider; stream: any }> {
  // Fallback chain: groq -> deepseek -> openrouter
  const fallbackChain = ['iaf-fast-llama', 'iaf-cheap-deepseek', 'iaf-smart-claude'];
  
  for (const modelId of fallbackChain) {
    if (modelId === originalProfile.id) continue;

    const fallbackProfile = getModelById(modelId);
    if (!fallbackProfile) continue;

    try {
      const provider = getProvider(fallbackProfile);
      const fallbackRequest = {
        ...request,
        model: fallbackProfile.actualModel,
      };

      if (request.stream) {
        const stream = provider.streamComplete(fallbackRequest);
        return { provider, stream };
      } else {
        const response = await provider.complete(fallbackRequest);
        return { provider, stream: null };
      }
    } catch (error) {
      // Continue to next fallback
      continue;
    }
  }

  throw new GatewayError('ALL_PROVIDERS_FAILED', 'All providers failed', 503);
}
