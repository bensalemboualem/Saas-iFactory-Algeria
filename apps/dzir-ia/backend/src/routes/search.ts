import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { authMiddleware, getAuth } from '../middleware/auth.js';
import { rateLimit } from '../middleware/rate_limit.js';
import { creditsMiddleware } from '../middleware/credits.js';
import { SearchRequestSchema, SearchQuerySchema, type SearchResult } from '../types/index.js';
import * as db from '../services/sqlite.js';
import * as qdrant from '../services/qdrant.js';
import {
  generateEmbedding,
  resolveEmbeddingsConfig,
  type BYOKContext,
} from '../services/embeddings.js';
import { getOrComputeEmbedding } from '../services/embedding_cache.js';

const search = new Hono();

search.use('*', authMiddleware);
search.use('*', rateLimit('search'));
search.use('*', creditsMiddleware('search'));

/**
 * Extract user token from Authorization header
 */
function extractToken(c: any): string | null {
  const authHeader = c.req.header('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }
  return authHeader.slice(7);
}

// GET /search - Search documents
search.get('/', zValidator('query', SearchQuerySchema), async (c) => {
  const auth = getAuth(c);
  const query = c.req.valid('query');
  const userToken = extractToken(c);

  // Build BYOK context
  const byokContext: BYOKContext | undefined = userToken
    ? { userId: auth.userId, userToken }
    : undefined;

  // Check if embeddings are available (server key or BYOK)
  const embeddingsConfig = await resolveEmbeddingsConfig(byokContext);
  if (!embeddingsConfig) {
    return c.json(
      {
        error: 'Service unavailable',
        message: 'No API key available. Configure server key or add your own via settings.',
      },
      503
    );
  }

  // Generate embedding for the search query (with LRU cache)
  const queryVector = await getOrComputeEmbedding(
    query.query,
    (text) => generateEmbedding(text, byokContext)
  );

  if (!queryVector) {
    return c.json(
      {
        error: 'Embedding failed',
        message: 'Failed to generate embedding for search query.',
      },
      500
    );
  }

  // Search in Qdrant
  const vectorResults = await qdrant.searchVectors(
    queryVector,
    auth.userId,
    query.collectionIds,
    query.limit,
    query.threshold
  );

  // Enrich results with document metadata
  const results: SearchResult[] = [];

  for (const result of vectorResults) {
    const document = db.getDocument(auth.userId, result.payload.documentId);

    if (document) {
      results.push({
        documentId: result.payload.documentId,
        chunkId: result.payload.chunkId,
        content: result.payload.content,
        score: result.score,
        document: {
          title: document.title,
          sourceType: document.sourceType,
          sourceUrl: document.sourceUrl,
        },
      });
    }
  }

  return c.json({
    results,
    count: results.length,
    query: query.query,
  });
});

// POST /search - Search with body (for longer queries)
search.post('/', zValidator('json', SearchRequestSchema), async (c) => {
  const auth = getAuth(c);
  const body = c.req.valid('json');
  const userToken = extractToken(c);

  // Build BYOK context
  const byokContext: BYOKContext | undefined = userToken
    ? { userId: auth.userId, userToken }
    : undefined;

  // Check if embeddings are available (server key or BYOK)
  const embeddingsConfig = await resolveEmbeddingsConfig(byokContext);
  if (!embeddingsConfig) {
    return c.json(
      {
        error: 'Service unavailable',
        message: 'No API key available. Configure server key or add your own via settings.',
      },
      503
    );
  }

  // Generate embedding for the search query (with LRU cache)
  const queryVector = await getOrComputeEmbedding(
    body.query,
    (text) => generateEmbedding(text, byokContext)
  );

  if (!queryVector) {
    return c.json(
      {
        error: 'Embedding failed',
        message: 'Failed to generate embedding for search query.',
      },
      500
    );
  }

  const vectorResults = await qdrant.searchVectors(
    queryVector,
    auth.userId,
    body.collectionIds,
    body.limit,
    body.threshold
  );

  const results: SearchResult[] = [];

  for (const result of vectorResults) {
    const document = db.getDocument(auth.userId, result.payload.documentId);

    if (document) {
      results.push({
        documentId: result.payload.documentId,
        chunkId: result.payload.chunkId,
        content: result.payload.content,
        score: result.score,
        document: {
          title: document.title,
          sourceType: document.sourceType,
          sourceUrl: document.sourceUrl,
        },
      });
    }
  }

  return c.json({
    results,
    count: results.length,
    query: body.query,
  });
});

export default search;
