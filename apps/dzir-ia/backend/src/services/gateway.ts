import { getCachedKeys, setCachedKeys, type UserKeys } from './byok_cache.js';

const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:3000';
const NODE_ENV = process.env.NODE_ENV || 'development';

export interface GatewayUserKeysResponse {
  keys: {
    openai?: string;
    anthropic?: string;
    ollama?: string;
  };
}

export class GatewayError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly cause?: unknown
  ) {
    super(message);
    this.name = 'GatewayError';
  }
}

/**
 * Fetch user's API keys from Gateway
 * Uses forward JWT auth (Option A)
 *
 * @param userToken - The user's JWT token (forwarded from request)
 * @param userId - User ID for caching
 */
export async function getUserKeys(
  userToken: string,
  userId: string
): Promise<UserKeys | null> {
  // Check cache first
  const cached = getCachedKeys(userId);
  if (cached) {
    return cached;
  }

  // Fetch from Gateway
  try {
    const response = await fetch(`${GATEWAY_URL}/api/user/keys`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${userToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token invalid/expired - don't cache this
        if (NODE_ENV === 'development') {
          console.warn('[Gateway] Unauthorized - user token may be expired');
        }
        return null;
      }

      if (response.status === 404) {
        // User has no keys configured - cache empty result
        const emptyKeys: Omit<UserKeys, 'fetchedAt'> = {};
        setCachedKeys(userId, emptyKeys);
        return { ...emptyKeys, fetchedAt: Date.now() };
      }

      const error = await response.text().catch(() => 'Unknown error');
      throw new GatewayError(
        `Gateway returned ${response.status}: ${error}`,
        response.status
      );
    }

    const data = (await response.json()) as GatewayUserKeysResponse;

    // Cache the keys
    const keys: Omit<UserKeys, 'fetchedAt'> = {
      openai: data.keys.openai,
      anthropic: data.keys.anthropic,
      ollama: data.keys.ollama,
    };

    setCachedKeys(userId, keys);

    return { ...keys, fetchedAt: Date.now() };
  } catch (error) {
    if (error instanceof GatewayError) {
      throw error;
    }

    // Network error or Gateway unavailable
    if (NODE_ENV === 'development') {
      console.error('[Gateway] Failed to fetch user keys:', error);
    }

    // Return null to allow fallback to server key
    return null;
  }
}

/**
 * Check if Gateway is available
 */
export async function isGatewayAvailable(): Promise<boolean> {
  try {
    const response = await fetch(`${GATEWAY_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(2000), // 2s timeout
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Get the configured Gateway URL
 */
export function getGatewayUrl(): string {
  return GATEWAY_URL;
}
