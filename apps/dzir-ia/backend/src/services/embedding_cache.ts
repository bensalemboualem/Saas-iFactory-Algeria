import { LRUCache } from 'lru-cache';

const NODE_ENV = process.env.NODE_ENV || 'development';

// Cache configuration
const DEFAULT_TTL_MS = 10 * 60 * 1000; // 10 minutes
const MAX_ENTRIES = 500; // Max cached queries

// Cache key format: `${model}:${normalizedQuery}`
type CacheKey = string;
type CacheValue = number[]; // embedding vector

// LRU cache instance
const cache = new LRUCache<CacheKey, CacheValue>({
  max: MAX_ENTRIES,
  ttl: DEFAULT_TTL_MS,
  updateAgeOnGet: true, // Reset TTL on access
});

/**
 * Normalize query for consistent cache keys
 * - trim whitespace
 * - collapse multiple spaces
 * - lowercase
 */
export function normalizeQuery(query: string): string {
  return query.trim().replace(/\s+/g, ' ').toLowerCase();
}

/**
 * Build cache key from model and normalized query
 */
function buildKey(model: string, normalizedQuery: string): CacheKey {
  return `${model}:${normalizedQuery}`;
}

/**
 * Get cached embedding for a query
 * Returns undefined if not found or expired
 */
export function getCachedEmbedding(
  query: string,
  model: string = 'text-embedding-3-small'
): number[] | undefined {
  const normalizedQuery = normalizeQuery(query);
  const key = buildKey(model, normalizedQuery);
  const cached = cache.get(key);

  if (NODE_ENV === 'development') {
    if (cached) {
      console.log(`[EmbeddingCache] HIT: "${normalizedQuery.slice(0, 50)}..."`);
    } else {
      console.log(`[EmbeddingCache] MISS: "${normalizedQuery.slice(0, 50)}..."`);
    }
  }

  return cached;
}

/**
 * Store embedding in cache
 */
export function setCachedEmbedding(
  query: string,
  embedding: number[],
  model: string = 'text-embedding-3-small'
): void {
  const normalizedQuery = normalizeQuery(query);
  const key = buildKey(model, normalizedQuery);
  cache.set(key, embedding);

  if (NODE_ENV === 'development') {
    console.log(`[EmbeddingCache] STORED: "${normalizedQuery.slice(0, 50)}..." (${cache.size} entries)`);
  }
}

/**
 * Get or compute embedding with caching
 * This is the main function to use in routes
 */
export async function getOrComputeEmbedding(
  query: string,
  computeFn: (text: string) => Promise<number[] | null>,
  model: string = 'text-embedding-3-small'
): Promise<number[] | null> {
  // Check cache first
  const cached = getCachedEmbedding(query, model);
  if (cached) {
    return cached;
  }

  // Compute embedding
  const embedding = await computeFn(query);

  // Cache if successful
  if (embedding) {
    setCachedEmbedding(query, embedding, model);
  }

  return embedding;
}

/**
 * Clear the embedding cache (useful for testing)
 */
export function clearEmbeddingCache(): void {
  cache.clear();
  if (NODE_ENV === 'development') {
    console.log('[EmbeddingCache] CLEARED');
  }
}

/**
 * Get cache stats (for monitoring/debugging)
 */
export function getCacheStats(): { size: number; maxSize: number } {
  return {
    size: cache.size,
    maxSize: MAX_ENTRIES,
  };
}
