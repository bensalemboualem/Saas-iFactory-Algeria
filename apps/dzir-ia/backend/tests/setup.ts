import { vi } from 'vitest';

// Mock environment variables for testing
process.env.NODE_ENV = 'test';
process.env.JWT_PUBLIC_KEY = ''; // Will use mock auth
process.env.GATEWAY_URL = 'http://localhost:3000';
process.env.JWT_ISSUER = 'test-issuer';
process.env.JWT_AUDIENCE = 'test-audience';

// Test user for mocked auth
export const TEST_USER = {
  userId: 'test-user-123',
  email: 'test@example.com',
  plan: 'pro' as const,
};

// Generate a mock JWT token (not cryptographically valid, but works with mocked middleware)
export const TEST_TOKEN = 'test-jwt-token-for-e2e';

// Mock embeddings - deterministic 1536-dimensional vector
export function mockEmbedding(seed: string): number[] {
  const vector = new Array(1536).fill(0);
  // Simple deterministic "hash" based on string
  for (let i = 0; i < seed.length; i++) {
    const charCode = seed.charCodeAt(i);
    vector[i % 1536] = (vector[i % 1536] + charCode / 1000) % 1;
  }
  // Normalize
  const norm = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0)) || 1;
  return vector.map((v) => v / norm);
}

// Mock LLM response
export const MOCK_LLM_RESPONSE = {
  content: 'Based on the provided sources [1], this is a test answer about the topic.',
  model: 'gpt-4o-mini-test',
  tokensUsed: {
    prompt: 100,
    completion: 50,
    total: 150,
  },
  finishReason: 'stop',
};
