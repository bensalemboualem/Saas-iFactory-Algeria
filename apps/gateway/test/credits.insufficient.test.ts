/**
 * Test: Insufficient credits → reserve fails
 * Validates that TOCTOU protection works correctly
 */

import { describe, it, beforeEach, expect } from 'vitest';
import { prisma } from '../src/db/client.js';
import { CreditsService } from '../src/core/credits.service.js';
import { resetDb, setupTestUserWithBalance } from './helpers/db.js';

describe('Credits - Insufficient Balance', () => {
  const credits = new CreditsService(prisma);
  const userId = 'u_insufficient_test';
  const orgId = 'org_test_1';

  beforeEach(async () => {
    await resetDb();
    await setupTestUserWithBalance(userId, orgId, 0.5); // Only 0.5 credits
  });

  it('reserve fails with INSUFFICIENT_CREDITS if balance < amount', async () => {
    await expect(
      credits.reserve({
        userId,
        requestId: 'req_insufficient_1',
        amount: 1.0, // Requesting more than available
        ttlSeconds: 300,
      })
    ).rejects.toThrow(/INSUFFICIENT_CREDITS/);

    // Balance should remain unchanged
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(0.5);

    // No reservation should exist
    const reservation = await prisma.creditReservation.findUnique({
      where: { requestId: 'req_insufficient_1' },
    });
    expect(reservation).toBeNull();
  });

  it('reserve succeeds when balance equals exactly the amount', async () => {
    const reservation = await credits.reserve({
      userId,
      requestId: 'req_exact_1',
      amount: 0.5, // Exactly the available balance
      ttlSeconds: 300,
    });

    expect(reservation).toBeTruthy();
    expect(reservation.status).toBe('RESERVED');

    // Balance should now be 0
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(0);
  });

  it('concurrent reserves fail if combined amount exceeds balance', async () => {
    // Set balance to 1.0
    await prisma.creditWallet.update({
      where: { userId },
      data: { balance: 1.0 },
    });

    // Try to reserve 0.6 twice concurrently (total 1.2 > 1.0)
    const results = await Promise.allSettled([
      credits.reserve({ userId, requestId: 'req_concurrent_1', amount: 0.6, ttlSeconds: 300 }),
      credits.reserve({ userId, requestId: 'req_concurrent_2', amount: 0.6, ttlSeconds: 300 }),
    ]);

    // One should succeed, one should fail
    const successes = results.filter((r) => r.status === 'fulfilled');
    const failures = results.filter((r) => r.status === 'rejected');

    expect(successes.length).toBe(1);
    expect(failures.length).toBe(1);

    // Final balance should be 0.4 (1.0 - 0.6)
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(0.4);
  });
});
