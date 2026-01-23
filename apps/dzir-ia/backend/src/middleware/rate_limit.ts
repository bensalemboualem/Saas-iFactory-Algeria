import { Context, Next, MiddlewareHandler } from 'hono';

// Rate limit enabled by default, can be disabled for tests
const RATE_LIMIT_ENABLED = process.env.RATE_LIMIT_ENABLED !== 'false';

// Default limits per 10 minutes (can be overridden via env for testing)
const WINDOW_MS = 10 * 60 * 1000; // 10 minutes

export const RATE_LIMITS: Record<string, number> = {
  ask: parseInt(process.env.RATE_LIMIT_ASK || '30', 10),
  search: parseInt(process.env.RATE_LIMIT_SEARCH || '120', 10),
  capture: parseInt(process.env.RATE_LIMIT_CAPTURE || '60', 10),
};

export type RateLimitBucket = keyof typeof RATE_LIMITS;

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

// In-memory store: key = `${userId}:${bucket}`
const store = new Map<string, RateLimitEntry>();

/**
 * Get rate limit entry for a user+bucket, creating if needed
 */
function getEntry(key: string): RateLimitEntry {
  const now = Date.now();
  let entry = store.get(key);

  // Create new entry or reset if window expired
  if (!entry || now >= entry.resetAt) {
    entry = {
      count: 0,
      resetAt: now + WINDOW_MS,
    };
    store.set(key, entry);
  }

  return entry;
}

/**
 * Clear all rate limit entries (for testing)
 */
export function clearRateLimits(): void {
  store.clear();
}

/**
 * Get current rate limit status for a user+bucket (for testing/debugging)
 */
export function getRateLimitStatus(
  userId: string,
  bucket: string
): { count: number; limit: number; remaining: number; resetAt: number } | null {
  const key = `${userId}:${bucket}`;
  const entry = store.get(key);
  const limit = RATE_LIMITS[bucket] || 30;

  if (!entry) {
    return null;
  }

  return {
    count: entry.count,
    limit,
    remaining: Math.max(0, limit - entry.count),
    resetAt: entry.resetAt,
  };
}

/**
 * Create rate limiting middleware for a specific bucket
 * Must be used AFTER auth middleware (needs userId from context)
 */
export function rateLimit(bucket: RateLimitBucket): MiddlewareHandler {
  const limit = RATE_LIMITS[bucket] || 30;

  return async (c: Context, next: Next) => {
    // Skip if rate limiting disabled
    if (!RATE_LIMIT_ENABLED) {
      await next();
      return;
    }

    // Get userId from auth context (set by auth middleware)
    const auth = c.get('auth');
    if (!auth?.userId) {
      // No auth context - let auth middleware handle this
      await next();
      return;
    }

    const key = `${auth.userId}:${bucket}`;
    const entry = getEntry(key);

    // Increment counter
    entry.count++;

    // Calculate seconds until reset
    const now = Date.now();
    const retryAfterSeconds = Math.ceil((entry.resetAt - now) / 1000);

    // Set rate limit headers
    c.header('X-RateLimit-Limit', String(limit));
    c.header('X-RateLimit-Remaining', String(Math.max(0, limit - entry.count)));
    c.header('X-RateLimit-Reset', String(Math.floor(entry.resetAt / 1000)));

    // Check if over limit
    if (entry.count > limit) {
      c.header('Retry-After', String(retryAfterSeconds));

      return c.json(
        {
          error: 'RATE_LIMITED',
          message: `Too many requests. Please try again in ${retryAfterSeconds} seconds.`,
          bucket,
          limit,
          resetAt: entry.resetAt,
          retryAfter: retryAfterSeconds,
        },
        429
      );
    }

    await next();
  };
}
