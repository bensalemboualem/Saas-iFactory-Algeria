import { getUserKeys } from './gateway.js';

const OPENAI_API_URL = 'https://api.openai.com/v1/embeddings';
const DEFAULT_MODEL = 'text-embedding-3-small';
const VECTOR_DIMENSIONS = 1536;

// Batch limits
const MAX_BATCH_SIZE = 100;
const MAX_TOKENS_PER_BATCH = 8000;

// Server key from environment
const SERVER_OPENAI_KEY = process.env.OPENAI_API_KEY || '';

export interface EmbeddingResult {
  embedding: number[];
  index: number;
  tokensUsed: number;
}

export interface EmbeddingsResponse {
  embeddings: EmbeddingResult[];
  totalTokensUsed: number;
  model: string;
  keySource: 'server' | 'byok';
}

export interface EmbeddingsConfig {
  apiKey: string;
  model: string;
  baseUrl: string;
  keySource: 'server' | 'byok';
}

export interface BYOKContext {
  userId: string;
  userToken: string;
}

/**
 * Check if server has its own OpenAI key configured
 */
export function hasServerKey(): boolean {
  return SERVER_OPENAI_KEY.length > 0;
}

/**
 * Check if embeddings service is available (server key exists)
 * For BYOK, use resolveEmbeddingsConfig with user context
 */
export function isEmbeddingsAvailable(): boolean {
  return hasServerKey();
}

/**
 * Resolve embeddings config - tries server key first, then BYOK
 */
export async function resolveEmbeddingsConfig(
  byokContext?: BYOKContext
): Promise<EmbeddingsConfig | null> {
  // Priority 1: Server key
  if (SERVER_OPENAI_KEY) {
    return {
      apiKey: SERVER_OPENAI_KEY,
      model: process.env.OPENAI_EMBEDDING_MODEL || DEFAULT_MODEL,
      baseUrl: process.env.OPENAI_API_BASE_URL || OPENAI_API_URL,
      keySource: 'server',
    };
  }

  // Priority 2: BYOK via Gateway
  if (byokContext) {
    try {
      const userKeys = await getUserKeys(byokContext.userToken, byokContext.userId);
      if (userKeys?.openai) {
        return {
          apiKey: userKeys.openai,
          model: process.env.OPENAI_EMBEDDING_MODEL || DEFAULT_MODEL,
          baseUrl: process.env.OPENAI_API_BASE_URL || OPENAI_API_URL,
          keySource: 'byok',
        };
      }
    } catch (error) {
      console.warn('Failed to get BYOK keys for embeddings:', error);
    }
  }

  // No key available
  return null;
}

/**
 * Legacy: Get embeddings configuration from environment only
 * @deprecated Use resolveEmbeddingsConfig for BYOK support
 */
export function getEmbeddingsConfig(): EmbeddingsConfig | null {
  if (!SERVER_OPENAI_KEY) {
    return null;
  }

  return {
    apiKey: SERVER_OPENAI_KEY,
    model: process.env.OPENAI_EMBEDDING_MODEL || DEFAULT_MODEL,
    baseUrl: process.env.OPENAI_API_BASE_URL || OPENAI_API_URL,
    keySource: 'server',
  };
}

/**
 * Get the expected vector dimensions for the current model
 */
export function getVectorDimensions(): number {
  return VECTOR_DIMENSIONS;
}

/**
 * Generate embeddings for a single text
 * @param text - Text to embed
 * @param byokContext - Optional BYOK context for user key resolution
 */
export async function generateEmbedding(
  text: string,
  byokContext?: BYOKContext
): Promise<number[] | null> {
  const result = await generateEmbeddings([text], byokContext);
  if (!result || result.embeddings.length === 0) {
    return null;
  }
  return result.embeddings[0].embedding;
}

/**
 * Generate embeddings for multiple texts
 * @param texts - Array of texts to embed
 * @param byokContext - Optional BYOK context for user key resolution
 */
export async function generateEmbeddings(
  texts: string[],
  byokContext?: BYOKContext
): Promise<EmbeddingsResponse | null> {
  const config = await resolveEmbeddingsConfig(byokContext);

  if (!config) {
    console.warn('No API key available for embeddings (server or BYOK)');
    return null;
  }

  if (texts.length === 0) {
    return { embeddings: [], totalTokensUsed: 0, model: config.model, keySource: config.keySource };
  }

  // Clean and prepare texts
  const cleanedTexts = texts.map((t) => cleanTextForEmbedding(t));

  // Process in batches if needed
  const batches = createBatches(cleanedTexts);
  const allResults: EmbeddingResult[] = [];
  let totalTokens = 0;

  for (const batch of batches) {
    const batchResult = await callOpenAIEmbeddings(
      batch.texts,
      batch.originalIndices,
      config
    );

    if (!batchResult) {
      // If any batch fails, return null
      return null;
    }

    allResults.push(...batchResult.embeddings);
    totalTokens += batchResult.tokensUsed;
  }

  // Sort by original index
  allResults.sort((a, b) => a.index - b.index);

  return {
    embeddings: allResults,
    totalTokensUsed: totalTokens,
    model: config.model,
    keySource: config.keySource,
  };
}

/**
 * Create batches respecting size limits
 */
function createBatches(texts: string[]): Array<{ texts: string[]; originalIndices: number[] }> {
  const batches: Array<{ texts: string[]; originalIndices: number[] }> = [];
  let currentBatch: { texts: string[]; originalIndices: number[] } = {
    texts: [],
    originalIndices: [],
  };
  let currentTokenEstimate = 0;

  for (let i = 0; i < texts.length; i++) {
    const text = texts[i];
    // Rough token estimate: ~4 chars per token
    const tokenEstimate = Math.ceil(text.length / 4);

    // Check if we need to start a new batch
    if (
      currentBatch.texts.length >= MAX_BATCH_SIZE ||
      currentTokenEstimate + tokenEstimate > MAX_TOKENS_PER_BATCH
    ) {
      if (currentBatch.texts.length > 0) {
        batches.push(currentBatch);
      }
      currentBatch = { texts: [], originalIndices: [] };
      currentTokenEstimate = 0;
    }

    currentBatch.texts.push(text);
    currentBatch.originalIndices.push(i);
    currentTokenEstimate += tokenEstimate;
  }

  // Don't forget the last batch
  if (currentBatch.texts.length > 0) {
    batches.push(currentBatch);
  }

  return batches;
}

/**
 * Call OpenAI embeddings API
 */
async function callOpenAIEmbeddings(
  texts: string[],
  originalIndices: number[],
  config: EmbeddingsConfig
): Promise<{ embeddings: EmbeddingResult[]; tokensUsed: number } | null> {
  try {
    const response = await fetch(config.baseUrl!, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${config.apiKey}`,
      },
      body: JSON.stringify({
        model: config.model,
        input: texts,
        encoding_format: 'float',
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      console.error(`OpenAI API error: ${response.status} - ${error}`);

      // Handle rate limiting
      if (response.status === 429) {
        console.warn('Rate limited by OpenAI - will retry on next request');
      }

      return null;
    }

    const data = (await response.json()) as {
      data: Array<{ embedding: number[]; index: number }>;
      usage: { total_tokens: number };
    };

    const embeddings: EmbeddingResult[] = data.data.map((item) => ({
      embedding: item.embedding,
      index: originalIndices[item.index],
      tokensUsed: 0, // Token breakdown not available per item
    }));

    return {
      embeddings,
      tokensUsed: data.usage.total_tokens,
    };
  } catch (error) {
    console.error('Failed to generate embeddings:', error);
    return null;
  }
}

/**
 * Clean text for embedding generation
 */
function cleanTextForEmbedding(text: string): string {
  return text
    // Remove excessive whitespace
    .replace(/\s+/g, ' ')
    // Truncate if too long (OpenAI has 8191 token limit)
    .slice(0, 30000)
    .trim();
}

/**
 * Calculate cosine similarity between two vectors
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error('Vectors must have the same dimensions');
  }

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  const magnitude = Math.sqrt(normA) * Math.sqrt(normB);
  if (magnitude === 0) return 0;

  return dotProduct / magnitude;
}
