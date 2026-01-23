/**
 * PR-003 FIX 2: Cleanup expired credit reservations
 *
 * This job should be run periodically (every 5 minutes recommended)
 * to release credits held by reservations that expired without being finalized.
 *
 * Usage:
 *   - As cron: `node -r tsx dist/jobs/cleanupExpiredReservations.js`
 *   - Or call `runCleanup()` from your scheduler
 */

import { prisma } from '../db/client.js';
import { CreditsService } from '../core/credits.service.js';

const credits = new CreditsService(prisma);

export async function runCleanup(): Promise<{ cleaned: number }> {
  const start = Date.now();
  const result = await credits.cleanupExpired();

  if (result.cleaned > 0) {
    console.log(
      `[CleanupJob] Released ${result.cleaned} expired reservations in ${Date.now() - start}ms`
    );
  }

  return result;
}

// Run directly if executed as script
const isMainModule = import.meta.url.endsWith(process.argv[1]?.replace(/\\/g, '/') ?? '');
if (isMainModule) {
  runCleanup()
    .then((result) => {
      console.log(`[CleanupJob] Done. Cleaned: ${result.cleaned}`);
      process.exit(0);
    })
    .catch((err) => {
      console.error('[CleanupJob] Failed:', err);
      process.exit(1);
    });
}
