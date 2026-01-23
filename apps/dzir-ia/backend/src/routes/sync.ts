import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { randomUUID } from 'node:crypto';
import { authMiddleware, getAuth } from '../middleware/auth.js';
import { SyncRequestSchema } from '../types/index.js';
import {
  getDatabase,
  createCollection,
  deleteCollection,
  createDocument,
  deleteDocument,
} from '../services/sqlite.js';

const sync = new Hono();

sync.use('*', authMiddleware);

/**
 * Apply a sync item to the database (client-wins strategy)
 */
function applySyncItem(
  db: ReturnType<typeof getDatabase>,
  userId: string,
  item: { type: string; action: string; data: Record<string, unknown> }
): { applied: boolean; message?: string } {
  const { type, action, data } = item;

  try {
    if (type === 'collection') {
      if (action === 'create') {
        createCollection(userId, {
          id: (data.id as string) || randomUUID(),
          name: data.name as string,
          description: data.description as string | undefined,
          color: data.color as string | undefined,
          icon: data.icon as string | undefined,
        });
        return { applied: true };
      } else if (action === 'update') {
        const stmt = db.prepare(`
          UPDATE collections
          SET name = COALESCE(?, name),
              description = COALESCE(?, description),
              color = COALESCE(?, color),
              icon = COALESCE(?, icon),
              updated_at = datetime('now')
          WHERE id = ? AND user_id = ?
        `);
        const result = stmt.run(
          data.name ?? null,
          data.description ?? null,
          data.color ?? null,
          data.icon ?? null,
          data.id,
          userId
        );
        return { applied: result.changes > 0, message: result.changes === 0 ? 'Collection not found' : undefined };
      } else if (action === 'delete') {
        const deleted = deleteCollection(userId, data.id as string);
        return { applied: deleted, message: deleted ? undefined : 'Collection not found' };
      }
    } else if (type === 'document') {
      if (action === 'create') {
        createDocument(userId, {
          id: (data.id as string) || randomUUID(),
          collectionId: data.collectionId as string,
          title: data.title as string,
          sourceType: data.sourceType as 'url' | 'pdf' | 'text' | 'image' | 'audio',
          sourceUrl: data.sourceUrl as string | undefined,
          content: data.content as string,
          summary: data.summary as string | undefined,
          metadata: data.metadata as Record<string, unknown> | undefined,
        });
        return { applied: true };
      } else if (action === 'update') {
        const stmt = db.prepare(`
          UPDATE documents
          SET title = COALESCE(?, title),
              content = COALESCE(?, content),
              summary = COALESCE(?, summary),
              metadata = COALESCE(?, metadata),
              updated_at = datetime('now')
          WHERE id = ? AND user_id = ?
        `);
        const result = stmt.run(
          data.title ?? null,
          data.content ?? null,
          data.summary ?? null,
          data.metadata ? JSON.stringify(data.metadata) : null,
          data.id,
          userId
        );
        return { applied: result.changes > 0, message: result.changes === 0 ? 'Document not found' : undefined };
      } else if (action === 'delete') {
        const deleted = deleteDocument(userId, data.id as string);
        return { applied: deleted, message: deleted ? undefined : 'Document not found' };
      }
    }

    return { applied: false, message: `Unknown type/action: ${type}/${action}` };
  } catch (error) {
    return { applied: false, message: String(error) };
  }
}

// POST /sync - Sync offline changes
sync.post('/', zValidator('json', SyncRequestSchema), async (c) => {
  const auth = getAuth(c);
  const body = c.req.valid('json');

  const db = getDatabase();
  const now = new Date().toISOString();

  const results: Array<{
    id: string;
    status: 'applied' | 'conflict' | 'error';
    message?: string;
  }> = [];

  // Process each sync item in a transaction
  const processItems = db.transaction(() => {
    for (const item of body.items) {
      try {
        // First, apply the actual change
        const applyResult = applySyncItem(db, auth.userId, item);

        if (applyResult.applied) {
          // Store in sync queue for history/audit
          const stmt = db.prepare(`
            INSERT INTO sync_queue (id, user_id, type, action, data, timestamp, client_id, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
          `);

          stmt.run(
            item.id,
            auth.userId,
            item.type,
            item.action,
            JSON.stringify(item.data),
            item.timestamp,
            item.clientId,
            now
          );

          results.push({
            id: item.id,
            status: 'applied',
          });
        } else {
          results.push({
            id: item.id,
            status: 'error',
            message: applyResult.message || 'Failed to apply change',
          });
        }
      } catch (error) {
        results.push({
          id: item.id,
          status: 'error',
          message: String(error),
        });
      }
    }
  });

  processItems();

  // Get any server-side changes since lastSyncTimestamp
  let serverChanges: Array<{
    id: string;
    type: string;
    action: string;
    data: Record<string, unknown>;
    timestamp: string;
  }> = [];

  if (body.lastSyncTimestamp) {
    const stmt = db.prepare(`
      SELECT id, type, action, data, timestamp
      FROM sync_queue
      WHERE user_id = ? AND synced_at > ? AND client_id != ?
      ORDER BY timestamp ASC
    `);

    const rows = stmt.all(auth.userId, body.lastSyncTimestamp, body.items[0]?.clientId || '') as Array<{
      id: string;
      type: string;
      action: string;
      data: string;
      timestamp: string;
    }>;

    serverChanges = rows.map((row) => ({
      ...row,
      data: JSON.parse(row.data),
    }));
  }

  return c.json({
    results,
    serverChanges,
    syncTimestamp: now,
    appliedCount: results.filter((r) => r.status === 'applied').length,
    errorCount: results.filter((r) => r.status === 'error').length,
  });
});

// GET /sync/status - Get sync status
sync.get('/status', async (c) => {
  const auth = getAuth(c);
  const db = getDatabase();

  const stmt = db.prepare(`
    SELECT
      COUNT(*) as totalItems,
      MAX(synced_at) as lastSync
    FROM sync_queue
    WHERE user_id = ?
  `);

  const result = stmt.get(auth.userId) as { totalItems: number; lastSync: string | null };

  return c.json({
    userId: auth.userId,
    totalSyncedItems: result.totalItems,
    lastSyncTimestamp: result.lastSync,
  });
});

export default sync;
