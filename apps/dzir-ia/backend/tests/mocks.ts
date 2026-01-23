import { vi } from 'vitest';

// Hoist test constants and helpers so they are available in vi.mock factories
const { TEST_USER, mockEmbedding, MOCK_LLM_RESPONSE } = vi.hoisted(() => ({
  TEST_USER: {
    userId: 'test-user-123',
    email: 'test@example.com',
    plan: 'pro' as const,
  },
  mockEmbedding: (seed: string): number[] => {
    const vector = new Array(1536).fill(0);
    for (let i = 0; i < seed.length; i++) {
      const charCode = seed.charCodeAt(i);
      vector[i % 1536] = (vector[i % 1536] + charCode / 1000) % 1;
    }
    const norm = Math.sqrt(vector.reduce((sum: number, v: number) => sum + v * v, 0)) || 1;
    return vector.map((v: number) => v / norm);
  },
  MOCK_LLM_RESPONSE: {
    content: 'Based on the provided sources [1], this is a test answer about the topic.',
    model: 'gpt-4o-mini-test',
    tokensUsed: {
      prompt: 100,
      completion: 50,
      total: 150,
    },
    finishReason: 'stop',
  },
}));

/**
 * Mock auth middleware to bypass JWT verification in tests
 */
export function mockAuthMiddleware() {
  vi.mock('../src/middleware/auth.js', () => ({
    authMiddleware: vi.fn(async (c, next) => {
      // Check for Authorization header presence
      const authHeader = c.req.header('Authorization');
      if (!authHeader?.startsWith('Bearer ')) {
        return c.json({ error: 'Unauthorized', message: 'Missing token' }, 401);
      }
      // Set mock auth context
      c.set('auth', TEST_USER);
      await next();
    }),
    getAuth: vi.fn((c) => {
      const auth = c.get('auth');
      if (!auth) {
        throw new Error('Auth context not found');
      }
      return auth;
    }),
    requirePlan: vi.fn((...plans: string[]) => {
      return async (c: any, next: any) => {
        const auth = c.get('auth');
        if (!plans.includes(auth.plan)) {
          return c.json({ error: 'Forbidden' }, 403);
        }
        await next();
      };
    }),
    clearKeyCache: vi.fn(),
  }));
}

/**
 * Mock embeddings service (with BYOK support)
 */
export function mockEmbeddingsService() {
  vi.mock('../src/services/embeddings.js', () => ({
    generateEmbedding: vi.fn(async (text: string, _byokContext?: any) => mockEmbedding(text)),
    generateEmbeddings: vi.fn(async (texts: string[], _byokContext?: any) => ({
      embeddings: texts.map((text, index) => ({
        embedding: mockEmbedding(text),
        index,
        tokensUsed: Math.ceil(text.length / 4),
      })),
      totalTokensUsed: texts.reduce((sum, t) => sum + Math.ceil(t.length / 4), 0),
      model: 'text-embedding-3-small-mock',
      keySource: 'server',
    })),
    isEmbeddingsAvailable: vi.fn(() => true),
    hasServerKey: vi.fn(() => true),
    resolveEmbeddingsConfig: vi.fn(async (_byokContext?: any) => ({
      apiKey: 'mock-api-key',
      model: 'text-embedding-3-small',
      baseUrl: 'https://api.openai.com/v1/embeddings',
      keySource: 'server',
    })),
    getEmbeddingsConfig: vi.fn(() => ({
      apiKey: 'mock-api-key',
      model: 'text-embedding-3-small',
      baseUrl: 'https://api.openai.com/v1/embeddings',
      keySource: 'server',
    })),
    getVectorDimensions: vi.fn(() => 1536),
    cosineSimilarity: vi.fn((a: number[], b: number[]) => {
      let dot = 0, normA = 0, normB = 0;
      for (let i = 0; i < a.length; i++) {
        dot += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
      }
      return dot / (Math.sqrt(normA) * Math.sqrt(normB));
    }),
  }));
}

/**
 * Mock embedding cache
 */
export function mockEmbeddingCache() {
  vi.mock('../src/services/embedding_cache.js', () => ({
    getOrComputeEmbedding: vi.fn(async (query: string, computeFn: Function) => {
      return mockEmbedding(query);
    }),
    getCachedEmbedding: vi.fn(() => undefined),
    setCachedEmbedding: vi.fn(),
    normalizeQuery: vi.fn((q: string) => q.trim().toLowerCase()),
    clearEmbeddingCache: vi.fn(),
    getCacheStats: vi.fn(() => ({ size: 0, maxSize: 500 })),
  }));
}

/**
 * Mock LLM service (with BYOK support)
 */
export function mockLLMService() {
  vi.mock('../src/services/llm.js', () => ({
    chatCompletion: vi.fn(async (_messages: any, _options?: any, _byokContext?: any) => ({
      ...MOCK_LLM_RESPONSE,
      keySource: 'server',
    })),
    buildRAGPrompt: vi.fn((query, sources, systemPrompt) => [
      { role: 'system', content: systemPrompt || 'You are a helpful assistant.' },
      { role: 'user', content: `Question: ${query}` },
    ]),
    isLLMAvailable: vi.fn(() => true),
    hasServerKey: vi.fn(() => true),
    resolveLLMConfig: vi.fn(async (_byokContext?: any) => ({
      apiKey: 'mock-api-key',
      model: 'gpt-4o-mini',
      baseUrl: 'https://api.openai.com/v1/chat/completions',
      keySource: 'server',
    })),
    getLLMConfig: vi.fn(() => ({
      apiKey: 'mock-api-key',
      model: 'gpt-4o-mini',
      baseUrl: 'https://api.openai.com/v1/chat/completions',
      keySource: 'server',
    })),
  }));
}

/**
 * Mock Gateway service (for BYOK key resolution)
 */
export function mockGatewayService() {
  vi.mock('../src/services/gateway.js', () => ({
    getUserKeys: vi.fn(async (_userToken: string, _userId: string) => null), // Server key takes priority in tests
    isGatewayAvailable: vi.fn(async () => false),
    getGatewayUrl: vi.fn(() => 'http://localhost:3000'),
  }));
}

/**
 * Mock BYOK cache
 */
export function mockByokCache() {
  vi.mock('../src/services/byok_cache.js', () => ({
    getCachedKeys: vi.fn((_userId: string) => undefined),
    setCachedKeys: vi.fn(),
    invalidateKeys: vi.fn(),
    clearAllKeys: vi.fn(),
  }));
}

/**
 * Module-level vector storage for Qdrant mock
 * Hoisted so it's available in vi.mock factory
 */
const qdrantVectors = vi.hoisted(() => new Map<string, { id: string; vector: number[]; payload: any }>());

/**
 * Mock Qdrant service with in-memory storage
 */
export function mockQdrantService() {
  vi.mock('../src/services/qdrant.js', () => ({
    initializeQdrant: vi.fn(async () => {}),
    getQdrantClient: vi.fn(() => ({
      getCollections: vi.fn(async () => ({ collections: [] })),
    })),
    upsertVectors: vi.fn(async (points: any[]) => {
      for (const point of points) {
        qdrantVectors.set(point.id, point);
      }
    }),
    searchVectors: vi.fn(async (queryVector: number[], userId: string, collectionIds?: string[], limit = 10) => {
      // Simple mock search - return vectors matching userId
      const results = Array.from(qdrantVectors.values())
        .filter((v) => v.payload.userId === userId)
        .filter((v) => !collectionIds || collectionIds.includes(v.payload.collectionId))
        .slice(0, limit)
        .map((v) => ({
          id: v.id,
          score: 0.85, // Mock score
          payload: v.payload,
        }));
      return results;
    }),
    deleteVectorsByDocument: vi.fn(async (documentId: string) => {
      for (const [id, v] of qdrantVectors.entries()) {
        if (v.payload.documentId === documentId) {
          qdrantVectors.delete(id);
        }
      }
    }),
    deleteVectorsByCollection: vi.fn(async (collectionId: string) => {
      for (const [id, v] of qdrantVectors.entries()) {
        if (v.payload.collectionId === collectionId) {
          qdrantVectors.delete(id);
        }
      }
    }),
  }));
}

/**
 * Clear Qdrant mock storage (call between tests)
 */
export function clearQdrantVectors() {
  qdrantVectors.clear();
}

/**
 * Get Qdrant mock storage (for test assertions)
 */
export function getQdrantVectors() {
  return qdrantVectors;
}

/**
 * Mock MinIO service
 */
export function mockMinioService() {
  vi.mock('../src/services/minio.js', () => ({
    getMinioClient: vi.fn(() => ({
      listBuckets: vi.fn(async () => []),
      bucketExists: vi.fn(async () => true),
      makeBucket: vi.fn(async () => {}),
      putObject: vi.fn(async () => ({ etag: 'mock-etag', versionId: null })),
      getObject: vi.fn(async () => ({ read: vi.fn() })),
      removeObject: vi.fn(async () => {}),
    })),
    initializeMinio: vi.fn(async () => {}),
    uploadDocument: vi.fn(async () => 'mock-object-name'),
    getDocument: vi.fn(async () => Buffer.from('mock-content')),
    deleteDocument: vi.fn(async () => {}),
  }));
}

/**
 * Mock credits middleware - allows all operations in tests
 */
export function mockCreditsMiddleware() {
  vi.mock('../src/middleware/credits.js', () => ({
    creditsMiddleware: vi.fn(() => {
      return async (_c: any, next: any) => {
        await next();
      };
    }),
    chargeCredits: vi.fn(async () => ({ success: true })),
    finalizeCredits: vi.fn(async () => {}),
    getCaptureCost: vi.fn((sourceType: string) => {
      const costs: Record<string, number> = { text: 1, url: 2, pdf: 3 };
      return costs[sourceType] || 1;
    }),
    getCreditsFromContext: vi.fn(() => 1000),
    getUserBalance: vi.fn(async () => 1000),
  }));
}

/**
 * Mock rate limit middleware - allows all operations in tests
 */
export function mockRateLimitMiddleware() {
  vi.mock('../src/middleware/rate_limit.js', () => ({
    rateLimit: vi.fn(() => {
      return async (_c: any, next: any) => {
        await next();
      };
    }),
    clearRateLimits: vi.fn(),
    getRateLimitStatus: vi.fn(() => null),
    RATE_LIMITS: { ask: 30, search: 120, capture: 60 },
  }));
}

/**
 * Apply all mocks for E2E testing
 */
export function applyAllMocks() {
  mockAuthMiddleware();
  mockGatewayService();
  mockByokCache();
  mockRateLimitMiddleware();
  mockCreditsMiddleware();
  mockEmbeddingsService();
  mockEmbeddingCache();
  mockLLMService();
  mockQdrantService();
  mockMinioService();
}
