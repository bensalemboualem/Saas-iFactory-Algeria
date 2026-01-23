/**
 * Test: Happy path - reserve → finalize with refund
 * Validates the complete successful flow
 */

import { describe, it, beforeEach, expect } from 'vitest';
import { prisma } from '../src/db/client.js';
import { CreditsService } from '../src/core/credits.service.js';
import { resetDb, setupTestUserWithBalance } from './helpers/db.js';

describe('Credits - Happy Path', () => {
  const credits = new CreditsService(prisma);
  const userId = 'u_happy_test';
  const orgId = 'org_test_2';

  beforeEach(async () => {
    await resetDb();
    await setupTestUserWithBalance(userId, orgId, 10.0);
  });

  it('reserve decrements balance and creates RESERVED reservation', async () => {
    const reservation = await credits.reserve({
      userId,
      requestId: 'req_happy_1',
      amount: 5.0,
      ttlSeconds: 300,
    });

    expect(reservation.status).toBe('RESERVED');
    expect(Number(reservation.amount)).toBeCloseTo(5.0);

    // Balance should be reduced by hold amount
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(5.0); // 10 - 5 = 5
  });

  it('finalize creates debit transaction and refunds remainder', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_happy_2',
      amount: 5.0,
      ttlSeconds: 300,
    });

    const result = await credits.finalize({
      userId,
      requestId: 'req_happy_2',
      finalCost: 3.0, // Actual cost less than hold
      reason: 'chat_completion',
      orgId,
    });

    expect(result.status).toBe('OK');
    expect(result.debit).toBeCloseTo(3.0);
    expect(result.refund).toBeCloseTo(2.0); // 5 - 3 = 2 refunded

    // Final balance: 10 - 5 (hold) + 2 (refund) = 7
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(7.0);

    // Verify debit transaction was created
    const tx = await prisma.creditTransaction.findUnique({
      where: {
        userId_idempotencyKey: {
          userId,
          idempotencyKey: 'req_happy_2',
        },
      },
    });
    expect(tx).toBeTruthy();
    expect(Number(tx!.amount)).toBeCloseTo(-3.0);
    expect(tx!.type).toBe('debit');

    // Verify reservation is FINALIZED
    const reservation = await prisma.creditReservation.findUnique({
      where: { requestId: 'req_happy_2' },
    });
    expect(reservation?.status).toBe('FINALIZED');
  });

  it('finalize with finalCost > reserved only debits reserved amount', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_happy_3',
      amount: 2.0,
      ttlSeconds: 300,
    });

    // Try to finalize with cost higher than hold
    const result = await credits.finalize({
      userId,
      requestId: 'req_happy_3',
      finalCost: 5.0, // More than reserved
      reason: 'chat_completion',
      orgId,
    });

    expect(result.status).toBe('OK');
    expect(result.debit).toBeCloseTo(2.0); // Capped at reserved
    expect(result.refund).toBeCloseTo(0); // No refund

    // Final balance: 10 - 2 = 8 (not 10 - 5)
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(8.0);
  });

  it('finalize with finalCost = 0 refunds entire hold', async () => {
    await credits.reserve({
      userId,
      requestId: 'req_happy_4',
      amount: 3.0,
      ttlSeconds: 300,
    });

    const result = await credits.finalize({
      userId,
      requestId: 'req_happy_4',
      finalCost: 0, // Zero cost (e.g., cache hit)
      reason: 'chat_completion',
      orgId,
    });

    expect(result.status).toBe('OK');
    expect(result.debit).toBeCloseTo(0);
    expect(result.refund).toBeCloseTo(3.0);

    // Full balance restored
    const balance = await credits.getBalance(userId);
    expect(balance).toBeCloseTo(10.0);
  });
});
