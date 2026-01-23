/**
 * Test: Idempotency - replay protection
 * Validates that duplicate requests don't cause double-spend
 */

import { describe, it, beforeEach, expect } from 'vitest';
import { prisma } from '../src/db/client.js';
import { CreditsService } from '../src/core/credits.service.js';
import { resetDb, setupTestUserWithBalance } from './helpers/db.js';

describe('Credits - Idempotency', () => {
  const credits = new CreditsService(prisma);
  const userId = 'u_idempotent_test';
  const orgId = 'org_test_4';

  beforeEach(async () => {
    await resetDb();
    await setupTestUserWithBalance(userId, orgId, 10.0);
  });

  it('reserve is idempotent for same requestId', async () => {
    // Call reserve twice with same requestId
    const r1 = await credits.reserve({
      userId,
      requestId: 'req_idem_1',
      amount: 3.0,
      ttlSeconds: 300,
    });

    const r2 = await credits.reserve({
      userId,
      requestId: 'req_idem_1',
      amount: 3.0,
      ttlSeconds: 300,
    });

    // Both should return the same reservation
    expect(r1.id).toBe(r2.id);
    expect(r1.requestId).toBe(r2.requestId);

    // Balance should only be decremented once
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(7.0); // 10 - 3 = 7

    // Only one reservation should exist
    const reservations = await prisma.creditReservation.findMany({
      where: { userId },
    });
    expect(reservations.length).toBe(1);
  });

  it('finalize is idempotent for same requestId', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_idem_2',
      amount: 4.0,
      ttlSeconds: 300,
    });

    // Call finalize multiple times
    const f1 = await credits.finalize({
      userId,
      requestId: 'req_idem_2',
      finalCost: 2.5,
      reason: 'chat_completion',
      orgId,
    });

    const f2 = await credits.finalize({
      userId,
      requestId: 'req_idem_2',
      finalCost: 2.5,
      reason: 'chat_completion',
      orgId,
    });

    const f3 = await credits.finalize({
      userId,
      requestId: 'req_idem_2',
      finalCost: 2.5,
      reason: 'chat_completion',
      orgId,
    });

    expect(f1.status).toBe('OK');
    expect(f2.status).toBe('OK_IDEMPOTENT');
    expect(f3.status).toBe('OK_IDEMPOTENT');

    // Only one debit transaction
    const txs = await prisma.creditTransaction.findMany({
      where: { userId, idempotencyKey: 'req_idem_2' },
    });
    expect(txs.length).toBe(1);
    expect(Number(txs[0].amount)).toBeCloseTo(-2.5);

    // Final balance: 10 - 4 + 1.5 = 7.5
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(7.5);
  });

  it('concurrent finalize calls produce single debit', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_idem_3',
      amount: 5.0,
      ttlSeconds: 300,
    });

    // Concurrent finalize calls
    const results = await Promise.all([
      credits.finalize({ userId, requestId: 'req_idem_3', finalCost: 3.0, reason: 'chat', orgId }),
      credits.finalize({ userId, requestId: 'req_idem_3', finalCost: 3.0, reason: 'chat', orgId }),
      credits.finalize({ userId, requestId: 'req_idem_3', finalCost: 3.0, reason: 'chat', orgId }),
    ]);

    // One OK, rest OK_IDEMPOTENT
    const okCount = results.filter((r) => r.status === 'OK').length;
    const idemCount = results.filter((r) => r.status === 'OK_IDEMPOTENT').length;

    expect(okCount).toBe(1);
    expect(idemCount).toBe(2);

    // Only one transaction
    const txs = await prisma.creditTransaction.findMany({
      where: { userId, idempotencyKey: 'req_idem_3' },
    });
    expect(txs.length).toBe(1);

    // Correct final balance: 10 - 5 + 2 = 7
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(7.0);
  });

  it('different requestIds create separate reservations and debits', async () => {
    await credits.reserve({ userId, requestId: 'req_a', amount: 2.0, ttlSeconds: 300 });
    await credits.reserve({ userId, requestId: 'req_b', amount: 2.0, ttlSeconds: 300 });

    await credits.finalize({ userId, requestId: 'req_a', finalCost: 1.0, reason: 'chat', orgId });
    await credits.finalize({ userId, requestId: 'req_b', finalCost: 1.5, reason: 'chat', orgId });

    // Two separate transactions
    const txs = await prisma.creditTransaction.findMany({
      where: { userId },
      orderBy: { createdAt: 'asc' },
    });
    expect(txs.length).toBe(2);
    expect(Number(txs[0].amount)).toBeCloseTo(-1.0);
    expect(Number(txs[1].amount)).toBeCloseTo(-1.5);

    // Final balance: 10 - 4 (holds) + 1 + 0.5 (refunds) = 7.5
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(7.5);
  });
});
