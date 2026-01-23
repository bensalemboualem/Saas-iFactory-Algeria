/**
 * PR-003: In-process cleanup worker
 *
 * Periodically cleans up expired credit reservations.
 * Runs as a background interval when the server starts.
 *
 * Note: For multi-replica deployments, use a proper cron/scheduler
 * with distributed locking instead.
 */

import { prisma } from '../db/client.js';
import { CreditsService } from '../core/credits.service.js';

// Configuration
const CLEANUP_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes
const ENABLE_CLEANUP_WORKER = process.env.ENABLE_CLEANUP_WORKER !== 'false';

let cleanupInterval: NodeJS.Timeout | null = null;
let isRunning = false;

const credits = new CreditsService(prisma);

/**
 * Run a single cleanup cycle
 */
async function runCleanup(): Promise<void> {
  if (isRunning) {
    console.log('[CleanupWorker] Previous cleanup still running, skipping');
    return;
  }

  isRunning = true;
  const start = Date.now();

  try {
    const result = await credits.cleanupExpired();

    if (result.cleaned > 0) {
      console.log(
        `[CleanupWorker] Cleaned ${result.cleaned} expired reservations in ${Date.now() - start}ms`
      );
    }
  } catch (error) {
    console.error('[CleanupWorker] Cleanup failed:', error);
  } finally {
    isRunning = false;
  }
}

/**
 * Start the cleanup worker
 * Called at server startup
 */
export function startCleanupWorker(): void {
  if (!ENABLE_CLEANUP_WORKER) {
    console.log('[CleanupWorker] Disabled via ENABLE_CLEANUP_WORKER=false');
    return;
  }

  if (cleanupInterval) {
    console.warn('[CleanupWorker] Already running');
    return;
  }

  console.log(`[CleanupWorker] Starting (interval: ${CLEANUP_INTERVAL_MS / 1000}s)`);

  // Run immediately on start
  runCleanup();

  // Then run periodically
  cleanupInterval = setInterval(runCleanup, CLEANUP_INTERVAL_MS);

  // Prevent interval from keeping Node.js alive if server shuts down
  cleanupInterval.unref();
}

/**
 * Stop the cleanup worker
 * Called at server shutdown
 */
export function stopCleanupWorker(): void {
  if (cleanupInterval) {
    clearInterval(cleanupInterval);
    cleanupInterval = null;
    console.log('[CleanupWorker] Stopped');
  }
}

/**
 * Get worker status (for health checks)
 */
export function getCleanupWorkerStatus(): {
  enabled: boolean;
  running: boolean;
  intervalMs: number;
} {
  return {
    enabled: ENABLE_CLEANUP_WORKER,
    running: cleanupInterval !== null,
    intervalMs: CLEANUP_INTERVAL_MS,
  };
}
