import { Hono } from 'hono';
import { getQdrantClient } from '../services/qdrant.js';
import { getDatabase } from '../services/sqlite.js';
import { getMinioClient } from '../services/minio.js';

const health = new Hono();

health.get('/', async (c) => {
  const checks: Record<string, { status: string; latency?: number; error?: string }> = {};

  // Check SQLite
  const sqliteStart = Date.now();
  try {
    const db = getDatabase();
    db.prepare('SELECT 1').get();
    checks.sqlite = { status: 'healthy', latency: Date.now() - sqliteStart };
  } catch (error) {
    checks.sqlite = { status: 'unhealthy', error: String(error) };
  }

  // Check Qdrant
  const qdrantStart = Date.now();
  try {
    const qdrant = getQdrantClient();
    await qdrant.getCollections();
    checks.qdrant = { status: 'healthy', latency: Date.now() - qdrantStart };
  } catch (error) {
    checks.qdrant = { status: 'unhealthy', error: String(error) };
  }

  // Check MinIO
  const minioStart = Date.now();
  try {
    const minio = getMinioClient();
    await minio.listBuckets();
    checks.minio = { status: 'healthy', latency: Date.now() - minioStart };
  } catch (error) {
    checks.minio = { status: 'unhealthy', error: String(error) };
  }

  const allHealthy = Object.values(checks).every((c) => c.status === 'healthy');

  return c.json(
    {
      status: allHealthy ? 'healthy' : 'degraded',
      version: process.env.npm_package_version || '0.1.0',
      timestamp: new Date().toISOString(),
      checks,
    },
    allHealthy ? 200 : 503
  );
});

health.get('/live', (c) => {
  return c.json({ status: 'ok' });
});

health.get('/ready', async (c) => {
  try {
    const db = getDatabase();
    db.prepare('SELECT 1').get();
    return c.json({ status: 'ready' });
  } catch {
    return c.json({ status: 'not ready' }, 503);
  }
});

export default health;
