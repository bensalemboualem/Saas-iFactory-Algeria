/**
 * Test: Abort → release restores full hold
 * Validates client disconnect/error handling
 */

import { describe, it, beforeEach, expect } from 'vitest';
import { prisma } from '../src/db/client.js';
import { CreditsService } from '../src/core/credits.service.js';
import { resetDb, setupTestUserWithBalance } from './helpers/db.js';

describe('Credits - Abort/Release', () => {
  const credits = new CreditsService(prisma);
  const userId = 'u_abort_test';
  const orgId = 'org_test_3';

  beforeEach(async () => {
    await resetDb();
    await setupTestUserWithBalance(userId, orgId, 5.0);
  });

  it('release restores full hold to wallet', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_abort_1',
      amount: 3.0,
      ttlSeconds: 300,
    });

    // Balance after reserve: 5 - 3 = 2
    const midBalance = await credits.getBalance(userId);
    expect(midBalance).toBeCloseTo(2.0);

    // Release (simulating client abort)
    const result = await credits.release({
      userId,
      requestId: 'req_abort_1',
      reason: 'client_close',
    });

    expect(result.status).toBe('OK');

    // Full balance restored: 2 + 3 = 5
    const finalBalance = await credits.getBalance(userId);
    expect(finalBalance).toBeCloseTo(5.0);

    // No debit transaction should exist
    const tx = await prisma.creditTransaction.findFirst({
      where: { userId, idempotencyKey: 'req_abort_1' },
    });
    expect(tx).toBeNull();

    // Reservation should be RELEASED
    const reservation = await prisma.creditReservation.findUnique({
      where: { requestId: 'req_abort_1' },
    });
    expect(reservation?.status).toBe('RELEASED');
  });

  it('release is idempotent (safe to call multiple times)', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_abort_2',
      amount: 2.0,
      ttlSeconds: 300,
    });

    // Call release multiple times
    const r1 = await credits.release({ userId, requestId: 'req_abort_2', reason: 'error' });
    const r2 = await credits.release({ userId, requestId: 'req_abort_2', reason: 'error' });
    const r3 = await credits.release({ userId, requestId: 'req_abort_2', reason: 'error' });

    expect(r1.status).toBe('OK');
    expect(r2.status).toBe('NOOP'); // Already released
    expect(r3.status).toBe('NOOP');

    // Balance should only be restored once
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(5.0);
  });

  it('release on non-existent reservation returns NOOP', async () => {
    const result = await credits.release({
      userId,
      requestId: 'req_nonexistent',
      reason: 'manual',
    });

    expect(result.status).toBe('NOOP');

    // Balance unchanged
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(5.0);
  });

  it('release fails if userId does not match reservation owner', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_abort_3',
      amount: 1.0,
      ttlSeconds: 300,
    });

    // Try to release with different userId
    await expect(
      credits.release({
        userId: 'other_user',
        requestId: 'req_abort_3',
        reason: 'manual',
      })
    ).rejects.toThrow(/RESERVATION_OWNER_MISMATCH/);

    // Original user's balance should still be reduced
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(4.0);
  });

  it('cannot release after finalize', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_abort_4',
      amount: 2.0,
      ttlSeconds: 300,
    });

    await credits.finalize({
      userId,
      requestId: 'req_abort_4',
      finalCost: 1.5,
      reason: 'chat_completion',
      orgId,
    });

    // Try to release after finalize
    const result = await credits.release({
      userId,
      requestId: 'req_abort_4',
      reason: 'manual',
    });

    expect(result.status).toBe('NOOP'); // Already finalized

    // Balance should reflect finalize, not release
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(3.5); // 5 - 2 + 0.5 refund = 3.5
  });
});
