import { Hono } from 'hono';
import { authMiddleware, getAuth } from '../middleware/auth.js';
import * as db from '../services/sqlite.js';
import * as qdrant from '../services/qdrant.js';

const documents = new Hono();

// Apply auth middleware to all routes
documents.use('*', authMiddleware);

// GET /documents - List all documents (optionally filtered by collection)
documents.get('/', async (c) => {
  const auth = getAuth(c);
  const collectionId = c.req.query('collectionId');

  // If collectionId provided, verify it belongs to user
  if (collectionId) {
    const collection = db.getCollection(auth.userId, collectionId);
    if (!collection) {
      return c.json({ error: 'Collection not found' }, 404);
    }
  }

  const userDocuments = db.getDocuments(auth.userId, collectionId);

  return c.json({
    documents: userDocuments,
    count: userDocuments.length,
  });
});

// GET /documents/:id - Get a single document
documents.get('/:id', async (c) => {
  const auth = getAuth(c);
  const id = c.req.param('id');

  const document = db.getDocument(auth.userId, id);

  if (!document) {
    return c.json({ error: 'Document not found' }, 404);
  }

  // Get chunks for this document
  const chunks = db.getChunksByDocument(auth.userId, id);

  return c.json({
    document,
    chunksCount: chunks.length,
  });
});

// DELETE /documents/:id - Delete a document
documents.delete('/:id', async (c) => {
  const auth = getAuth(c);
  const id = c.req.param('id');

  // Verify document exists
  const document = db.getDocument(auth.userId, id);
  if (!document) {
    return c.json({ error: 'Document not found' }, 404);
  }

  // Delete vectors from Qdrant first
  try {
    await qdrant.deleteVectorsByDocument(id);
  } catch (error) {
    console.warn('Failed to delete vectors from Qdrant:', error);
    // Continue with deletion even if Qdrant fails
  }

  // Delete from SQLite (cascade deletes chunks)
  const deleted = db.deleteDocument(auth.userId, id);

  if (!deleted) {
    return c.json({ error: 'Failed to delete document' }, 500);
  }

  return c.json({ success: true });
});

export default documents;
