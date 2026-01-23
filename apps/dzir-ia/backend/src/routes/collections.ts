import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';
import { nanoid } from 'nanoid';
import { authMiddleware, getAuth } from '../middleware/auth.js';
import * as db from '../services/sqlite.js';
import * as qdrant from '../services/qdrant.js';

const collections = new Hono();

// Apply auth middleware to all routes
collections.use('*', authMiddleware);

// Create collection schema
const CreateCollectionSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  color: z.string().optional(),
  icon: z.string().optional(),
});

// GET /collections - List all collections
collections.get('/', async (c) => {
  const auth = getAuth(c);
  const userCollections = db.getCollections(auth.userId);

  return c.json({
    collections: userCollections,
    count: userCollections.length,
  });
});

// POST /collections - Create new collection
collections.post('/', zValidator('json', CreateCollectionSchema), async (c) => {
  const auth = getAuth(c);
  const body = c.req.valid('json');

  const collection = db.createCollection(auth.userId, {
    id: nanoid(),
    name: body.name,
    description: body.description,
    color: body.color || '#00A86B',
    icon: body.icon || 'folder',
  });

  return c.json({ collection }, 201);
});

// GET /collections/:id - Get single collection
collections.get('/:id', async (c) => {
  const auth = getAuth(c);
  const id = c.req.param('id');

  const collection = db.getCollection(auth.userId, id);

  if (!collection) {
    return c.json({ error: 'Collection not found' }, 404);
  }

  // Get documents count
  const documents = db.getDocuments(auth.userId, id);

  return c.json({
    collection,
    documentsCount: documents.length,
  });
});

// DELETE /collections/:id - Delete collection
collections.delete('/:id', async (c) => {
  const auth = getAuth(c);
  const id = c.req.param('id');

  // Delete vectors from Qdrant first
  await qdrant.deleteVectorsByCollection(id);

  // Delete from SQLite (cascade deletes documents and chunks)
  const deleted = db.deleteCollection(auth.userId, id);

  if (!deleted) {
    return c.json({ error: 'Collection not found' }, 404);
  }

  return c.json({ success: true });
});

export default collections;
