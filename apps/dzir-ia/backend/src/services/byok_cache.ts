import { LRUCache } from 'lru-cache';

const NODE_ENV = process.env.NODE_ENV || 'development';

// Cache configuration
const DEFAULT_TTL_MS = 5 * 60 * 1000; // 5 minutes
const MAX_ENTRIES = 1000; // Max cached users

export interface UserKeys {
  openai?: string;
  anthropic?: string;
  ollama?: string;
  fetchedAt: number;
}

// LRU cache for user API keys
const cache = new LRUCache<string, UserKeys>({
  max: MAX_ENTRIES,
  ttl: DEFAULT_TTL_MS,
  updateAgeOnGet: false, // Don't extend TTL on access (security)
});

/**
 * Get cached keys for a user
 */
export function getCachedKeys(userId: string): UserKeys | undefined {
  const cached = cache.get(userId);

  if (NODE_ENV === 'development' && cached) {
    console.log(`[BYOKCache] HIT for user ${userId.slice(0, 8)}...`);
  }

  return cached;
}

/**
 * Store keys in cache
 */
export function setCachedKeys(userId: string, keys: Omit<UserKeys, 'fetchedAt'>): void {
  const entry: UserKeys = {
    ...keys,
    fetchedAt: Date.now(),
  };

  cache.set(userId, entry);

  if (NODE_ENV === 'development') {
    console.log(`[BYOKCache] STORED for user ${userId.slice(0, 8)}... (${cache.size} entries)`);
  }
}

/**
 * Invalidate cached keys for a user (e.g., after key rotation)
 */
export function invalidateKeys(userId: string): void {
  cache.delete(userId);

  if (NODE_ENV === 'development') {
    console.log(`[BYOKCache] INVALIDATED for user ${userId.slice(0, 8)}...`);
  }
}

/**
 * Clear all cached keys (useful for testing)
 */
export function clearBYOKCache(): void {
  cache.clear();

  if (NODE_ENV === 'development') {
    console.log('[BYOKCache] CLEARED');
  }
}

/**
 * Get cache stats
 */
export function getBYOKCacheStats(): { size: number; maxSize: number } {
  return {
    size: cache.size,
    maxSize: MAX_ENTRIES,
  };
}
