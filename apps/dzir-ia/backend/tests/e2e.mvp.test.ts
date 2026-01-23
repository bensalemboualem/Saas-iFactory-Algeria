import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { applyAllMocks } from './mocks.js';
import { TEST_TOKEN, TEST_USER } from './setup.js';

// Apply mocks before importing app
applyAllMocks();

// Now import the app (after mocks are set up)
import { createApp } from '../src/app.js';
import { initializeDatabase, closeDatabase, resetDatabase } from '../src/services/sqlite.js';

const app = createApp({ enableLogger: false });

// Helper to make requests
async function request(
  method: string,
  path: string,
  body?: unknown,
  headers: Record<string, string> = {}
) {
  const req = new Request(`http://localhost${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${TEST_TOKEN}`,
      ...headers,
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

  return app.fetch(req);
}

describe('Dzir IA Backend E2E MVP', () => {
  beforeAll(() => {
    // Initialize test database
    initializeDatabase(':memory:');
  });

  afterAll(() => {
    closeDatabase();
  });

  beforeEach(() => {
    // Reset database state between tests if needed
    // resetDatabase();
  });

  // ============================================
  // Health Check
  // ============================================
  describe('Health Check', () => {
    it('GET /health returns 200', async () => {
      const res = await app.fetch(new Request('http://localhost/health'));
      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.status).toBe('healthy');
    });

    it('GET / returns API info', async () => {
      const res = await app.fetch(new Request('http://localhost/'));
      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.name).toBe('Dzir IA Backend');
      expect(data.endpoints).toBeDefined();
    });
  });

  // ============================================
  // Collections CRUD
  // ============================================
  describe('Collections', () => {
    let collectionId: string;

    it('POST /api/collections creates a collection', async () => {
      const res = await request('POST', '/api/collections', {
        name: 'Test Collection',
        description: 'A test collection for E2E',
        color: '#3B82F6',
      });

      expect(res.status).toBe(201);
      const data = await res.json();
      expect(data.collection).toBeDefined();
      expect(data.collection.name).toBe('Test Collection');
      expect(data.collection.id).toBeDefined();
      collectionId = data.collection.id;
    });

    it('GET /api/collections lists collections', async () => {
      const res = await request('GET', '/api/collections');

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.collections).toBeInstanceOf(Array);
      expect(data.count).toBeGreaterThanOrEqual(1);
    });

    it('GET /api/collections/:id returns a collection', async () => {
      const res = await request('GET', `/api/collections/${collectionId}`);

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.collection.id).toBe(collectionId);
    });

    it('returns 404 for non-existent collection', async () => {
      const res = await request('GET', '/api/collections/non-existent-id');

      expect(res.status).toBe(404);
    });
  });

  // ============================================
  // Capture Text
  // ============================================
  describe('Capture Text', () => {
    let collectionId: string;
    let documentId: string;

    beforeAll(async () => {
      // Create a collection first
      const res = await request('POST', '/api/collections', {
        name: 'Capture Test Collection',
      });
      const data = await res.json();
      collectionId = data.collection.id;
    });

    it('POST /api/capture captures text content', async () => {
      const res = await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        title: 'Test Document',
        content: `This is a test document about artificial intelligence and machine learning.

AI is transforming many industries. Machine learning algorithms can process vast amounts of data
and identify patterns that humans might miss. Deep learning, a subset of machine learning,
uses neural networks with multiple layers to learn complex representations.

Natural language processing (NLP) enables computers to understand and generate human language.
Vector databases like Qdrant store embeddings for semantic search applications.
RAG (Retrieval Augmented Generation) combines search with language models for better answers.`,
      });

      expect(res.status).toBe(201);
      const data = await res.json();
      expect(data.document).toBeDefined();
      expect(data.document.title).toBe('Test Document');
      expect(data.chunksCount).toBeGreaterThan(0);
      expect(data.message).toContain('captured');
      documentId = data.document.id;
    });

    it('rejects content that is too short', async () => {
      const res = await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        content: 'Too short',
      });

      expect(res.status).toBe(400);
      const data = await res.json();
      expect(data.error).toBe('Content too short');
    });

    it('rejects capture without collection', async () => {
      const res = await request('POST', '/api/capture', {
        collectionId: 'non-existent',
        sourceType: 'text',
        content: 'A sufficiently long content that should be accepted by the validator.',
      });

      expect(res.status).toBe(404);
    });
  });

  // ============================================
  // Documents
  // ============================================
  describe('Documents', () => {
    let collectionId: string;
    let documentId: string;

    beforeAll(async () => {
      // Create collection and document
      const colRes = await request('POST', '/api/collections', {
        name: 'Documents Test Collection',
      });
      collectionId = (await colRes.json()).collection.id;

      const docRes = await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        title: 'Document for Testing',
        content: 'This is a long enough document for testing the documents endpoint functionality and features.',
      });
      documentId = (await docRes.json()).document.id;
    });

    it('GET /api/documents lists documents', async () => {
      const res = await request('GET', '/api/documents');

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.documents).toBeInstanceOf(Array);
    });

    it('GET /api/documents?collectionId filters by collection', async () => {
      const res = await request('GET', `/api/documents?collectionId=${collectionId}`);

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.documents.every((d: any) => d.collectionId === collectionId)).toBe(true);
    });

    it('GET /api/documents/:id returns a document', async () => {
      const res = await request('GET', `/api/documents/${documentId}`);

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.document.id).toBe(documentId);
    });

    it('DELETE /api/documents/:id deletes a document', async () => {
      // Create a document to delete
      const createRes = await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        title: 'To Be Deleted',
        content: 'This document will be deleted in the test. It needs to be long enough to pass validation.',
      });
      const toDeleteId = (await createRes.json()).document.id;

      const res = await request('DELETE', `/api/documents/${toDeleteId}`);

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.success).toBe(true);

      // Verify it's gone
      const getRes = await request('GET', `/api/documents/${toDeleteId}`);
      expect(getRes.status).toBe(404);
    });
  });

  // ============================================
  // Search
  // ============================================
  describe('Search', () => {
    let collectionId: string;

    beforeAll(async () => {
      // Create collection with searchable content
      const colRes = await request('POST', '/api/collections', {
        name: 'Search Test Collection',
      });
      collectionId = (await colRes.json()).collection.id;

      await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        title: 'AI Overview',
        content: `Artificial intelligence is revolutionizing technology. Machine learning enables computers to learn from data.
        Deep learning uses neural networks for complex pattern recognition. Natural language processing helps computers understand text.`,
      });
    });

    it('POST /api/search searches documents', async () => {
      const res = await request('POST', '/api/search', {
        query: 'artificial intelligence machine learning',
      });

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.results).toBeInstanceOf(Array);
      expect(data.query).toBe('artificial intelligence machine learning');
    });

    it('POST /api/search filters by collectionIds', async () => {
      const res = await request('POST', '/api/search', {
        query: 'machine learning',
        collectionIds: [collectionId],
      });

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.results).toBeInstanceOf(Array);
    });

    it('GET /api/search works with query params', async () => {
      const res = await request('GET', '/api/search?query=neural+networks&limit=5');

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.results).toBeInstanceOf(Array);
    });
  });

  // ============================================
  // Ask (RAG)
  // ============================================
  describe('Ask (RAG)', () => {
    let collectionId: string;

    beforeAll(async () => {
      // Create collection with content for RAG
      const colRes = await request('POST', '/api/collections', {
        name: 'RAG Test Collection',
      });
      collectionId = (await colRes.json()).collection.id;

      await request('POST', '/api/capture', {
        collectionId,
        sourceType: 'text',
        title: 'RAG Technology Guide',
        content: `RAG (Retrieval Augmented Generation) is a technique that combines information retrieval with language generation.

It works by first searching a knowledge base for relevant documents, then using those documents as context for a language model.
This approach helps ground the model's responses in factual information and reduces hallucinations.

Key components of RAG:
1. Vector database for storing document embeddings
2. Embedding model to convert text to vectors
3. Language model for generating responses
4. Retrieval mechanism to find relevant chunks`,
      });
    });

    it('POST /api/ask answers questions with citations', async () => {
      const res = await request('POST', '/api/ask', {
        query: 'What is RAG and how does it work?',
        collectionIds: [collectionId],
      });

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.answer).toBeDefined();
      expect(data.answer.length).toBeGreaterThan(0);
      expect(data.sources).toBeInstanceOf(Array);
      expect(data.model).toBeDefined();
      expect(data.tokensUsed).toBeDefined();
      expect(data.tokensUsed.total).toBeGreaterThan(0);
    });

    it('POST /api/ask accepts custom model parameter', async () => {
      const res = await request('POST', '/api/ask', {
        query: 'Explain vector databases',
        model: 'gpt-4o',
      });

      expect(res.status).toBe(200);
      const data = await res.json();
      expect(data.answer).toBeDefined();
    });

    it('POST /api/ask returns sources with snippets', async () => {
      const res = await request('POST', '/api/ask', {
        query: 'What are the key components of RAG?',
        collectionIds: [collectionId],
      });

      expect(res.status).toBe(200);
      const data = await res.json();

      if (data.sources.length > 0) {
        const source = data.sources[0];
        expect(source.index).toBeDefined();
        expect(source.documentId).toBeDefined();
        expect(source.title).toBeDefined();
        expect(source.snippet).toBeDefined();
      }
    });
  });

  // ============================================
  // Auth Required
  // ============================================
  describe('Auth Required', () => {
    it('returns 401 without Authorization header', async () => {
      const req = new Request('http://localhost/api/collections', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const res = await app.fetch(req);

      expect(res.status).toBe(401);
    });

    it('returns 401 with invalid Authorization header', async () => {
      const req = new Request('http://localhost/api/collections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Invalid token',
        },
      });
      const res = await app.fetch(req);

      expect(res.status).toBe(401);
    });
  });

  // ============================================
  // 404 Handling
  // ============================================
  describe('404 Handling', () => {
    it('returns 404 for unknown routes', async () => {
      const res = await request('GET', '/api/unknown-endpoint');

      expect(res.status).toBe(404);
      const data = await res.json();
      expect(data.error).toBe('Not Found');
    });
  });
});
