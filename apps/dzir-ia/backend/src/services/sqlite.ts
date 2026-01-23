import Database from 'better-sqlite3';
import { Collection, Document, Chunk } from '../types/index.js';

const DB_PATH = process.env.SQLITE_PATH || './data/dzir.db';

let db: Database.Database | null = null;
let dbPath: string = DB_PATH;

export function getDatabase(): Database.Database {
  if (!db) {
    db = new Database(dbPath);
    if (dbPath !== ':memory:') {
      db.pragma('journal_mode = WAL');
    }
    db.pragma('foreign_keys = ON');
  }
  return db;
}

/**
 * Initialize database with optional custom path
 * @param path - Database path (use ':memory:' for in-memory testing)
 */
export function initializeDatabase(path?: string): void {
  if (path) {
    dbPath = path;
  }
  const database = getDatabase();

  database.exec(`
    -- Collections table
    CREATE TABLE IF NOT EXISTS collections (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      name TEXT NOT NULL,
      description TEXT,
      color TEXT,
      icon TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_collections_user_id ON collections(user_id);

    -- Documents table
    CREATE TABLE IF NOT EXISTS documents (
      id TEXT PRIMARY KEY,
      collection_id TEXT NOT NULL,
      user_id TEXT NOT NULL,
      title TEXT NOT NULL,
      source_type TEXT NOT NULL,
      source_url TEXT,
      content TEXT NOT NULL,
      summary TEXT,
      metadata TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_documents_collection_id ON documents(collection_id);
    CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);

    -- Chunks table
    CREATE TABLE IF NOT EXISTS chunks (
      id TEXT PRIMARY KEY,
      document_id TEXT NOT NULL,
      user_id TEXT NOT NULL,
      content TEXT NOT NULL,
      position INTEGER NOT NULL,
      metadata TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);

    -- Sync queue table (for offline-first)
    CREATE TABLE IF NOT EXISTS sync_queue (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      type TEXT NOT NULL,
      action TEXT NOT NULL,
      data TEXT NOT NULL,
      timestamp TEXT NOT NULL,
      client_id TEXT NOT NULL,
      synced_at TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_sync_queue_user_id ON sync_queue(user_id);
    CREATE INDEX IF NOT EXISTS idx_sync_queue_synced_at ON sync_queue(synced_at);
  `);

  console.log('SQLite database initialized');
}

// ============ Collections ============
export function createCollection(userId: string, data: Omit<Collection, 'createdAt' | 'updatedAt'>): Collection {
  const database = getDatabase();
  const now = new Date().toISOString();

  const stmt = database.prepare(`
    INSERT INTO collections (id, user_id, name, description, color, icon, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);

  stmt.run(data.id, userId, data.name, data.description, data.color, data.icon, now, now);

  return { ...data, createdAt: now, updatedAt: now };
}

export function getCollections(userId: string): Collection[] {
  const database = getDatabase();
  const stmt = database.prepare(`
    SELECT id, name, description, color, icon, created_at as createdAt, updated_at as updatedAt
    FROM collections
    WHERE user_id = ?
    ORDER BY created_at DESC
  `);

  return stmt.all(userId) as Collection[];
}

export function getCollection(userId: string, id: string): Collection | null {
  const database = getDatabase();
  const stmt = database.prepare(`
    SELECT id, name, description, color, icon, created_at as createdAt, updated_at as updatedAt
    FROM collections
    WHERE id = ? AND user_id = ?
  `);

  return (stmt.get(id, userId) as Collection) || null;
}

export function deleteCollection(userId: string, id: string): boolean {
  const database = getDatabase();
  const stmt = database.prepare('DELETE FROM collections WHERE id = ? AND user_id = ?');
  const result = stmt.run(id, userId);
  return result.changes > 0;
}

// ============ Documents ============
export function createDocument(
  userId: string,
  data: Omit<Document, 'createdAt' | 'updatedAt'>
): Document {
  const database = getDatabase();
  const now = new Date().toISOString();

  const stmt = database.prepare(`
    INSERT INTO documents (id, collection_id, user_id, title, source_type, source_url, content, summary, metadata, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  stmt.run(
    data.id,
    data.collectionId,
    userId,
    data.title,
    data.sourceType,
    data.sourceUrl,
    data.content,
    data.summary,
    data.metadata ? JSON.stringify(data.metadata) : null,
    now,
    now
  );

  return { ...data, createdAt: now, updatedAt: now };
}

export function getDocuments(userId: string, collectionId?: string): Document[] {
  const database = getDatabase();

  let sql = `
    SELECT id, collection_id as collectionId, title, source_type as sourceType,
           source_url as sourceUrl, content, summary, metadata,
           created_at as createdAt, updated_at as updatedAt
    FROM documents
    WHERE user_id = ?
  `;

  const params: string[] = [userId];

  if (collectionId) {
    sql += ' AND collection_id = ?';
    params.push(collectionId);
  }

  sql += ' ORDER BY created_at DESC';

  const stmt = database.prepare(sql);
  const rows = stmt.all(...params) as Array<Document & { metadata: string | null }>;

  return rows.map((row) => ({
    ...row,
    metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
  }));
}

export function getDocument(userId: string, id: string): Document | null {
  const database = getDatabase();
  const stmt = database.prepare(`
    SELECT id, collection_id as collectionId, title, source_type as sourceType,
           source_url as sourceUrl, content, summary, metadata,
           created_at as createdAt, updated_at as updatedAt
    FROM documents
    WHERE id = ? AND user_id = ?
  `);

  const row = stmt.get(id, userId) as (Document & { metadata: string | null }) | undefined;
  if (!row) return null;

  return {
    ...row,
    metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
  };
}

export function deleteDocument(userId: string, id: string): boolean {
  const database = getDatabase();
  const stmt = database.prepare('DELETE FROM documents WHERE id = ? AND user_id = ?');
  const result = stmt.run(id, userId);
  return result.changes > 0;
}

// ============ Chunks ============
export function createChunks(userId: string, chunks: Omit<Chunk, 'embedding'>[]): void {
  const database = getDatabase();
  const stmt = database.prepare(`
    INSERT INTO chunks (id, document_id, user_id, content, position, metadata)
    VALUES (?, ?, ?, ?, ?, ?)
  `);

  const insertMany = database.transaction((items: typeof chunks) => {
    for (const chunk of items) {
      stmt.run(
        chunk.id,
        chunk.documentId,
        userId,
        chunk.content,
        chunk.position,
        chunk.metadata ? JSON.stringify(chunk.metadata) : null
      );
    }
  });

  insertMany(chunks);
}

export function getChunksByDocument(userId: string, documentId: string): Chunk[] {
  const database = getDatabase();
  const stmt = database.prepare(`
    SELECT id, document_id as documentId, content, position, metadata
    FROM chunks
    WHERE document_id = ? AND user_id = ?
    ORDER BY position ASC
  `);

  const rows = stmt.all(documentId, userId) as Array<Chunk & { metadata: string | null }>;

  return rows.map((row) => ({
    ...row,
    metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
  }));
}

export function closeDatabase(): void {
  if (db) {
    db.close();
    db = null;
  }
}

/**
 * Reset database (useful for testing)
 * Drops all data but keeps schema
 */
export function resetDatabase(): void {
  const database = getDatabase();
  database.exec(`
    DELETE FROM chunks;
    DELETE FROM documents;
    DELETE FROM collections;
    DELETE FROM sync_queue;
  `);
}
