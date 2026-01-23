/**
 * Tests for SignupService (beta credit grants)
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { prisma } from '../src/db/client.js';
import { SignupService } from '../src/core/signup.service.js';
import { resetDb, seedTestUser, seedWallet } from './helpers/db.js';

const signupService = new SignupService(prisma);

describe('SignupService - Beta Credits', () => {
  const userId = 'u_signup_test';
  const orgId = 'org_signup_test';

  beforeEach(async () => {
    await resetDb();
    await seedTestUser(userId, orgId);
  });

  it('grants signup credits to new user', async () => {
    const result = await signupService.grantSignupCredits(userId);

    expect(result.granted).toBe(true);
    expect(result.amount).toBeGreaterThan(0);
    expect(result.balance).toBe(result.amount);
    expect(result.alreadyGranted).toBe(false);

    // Verify wallet exists
    const wallet = await prisma.creditWallet.findUnique({
      where: { userId },
    });
    expect(wallet).toBeTruthy();
    expect(wallet?.balance).toBe(result.amount);
  });

  it('is idempotent - second call returns alreadyGranted', async () => {
    // First grant
    const first = await signupService.grantSignupCredits(userId);
    expect(first.granted).toBe(true);

    // Second grant - should be idempotent
    const second = await signupService.grantSignupCredits(userId);
    expect(second.granted).toBe(false);
    expect(second.alreadyGranted).toBe(true);
    expect(second.balance).toBe(first.balance);

    // Verify only one transaction exists
    const transactions = await prisma.creditTransaction.findMany({
      where: {
        userId,
        idempotencyKey: `signup_grant_${userId}`,
      },
    });
    expect(transactions.length).toBe(1);
  });

  it('creates wallet if not exists', async () => {
    // Verify no wallet exists (seedTestUser doesn't create wallet)
    const before = await prisma.creditWallet.findUnique({
      where: { userId },
    });
    expect(before).toBeNull();

    // Grant credits
    await signupService.grantSignupCredits(userId);

    // Verify wallet created
    const after = await prisma.creditWallet.findUnique({
      where: { userId },
    });
    expect(after).toBeTruthy();
  });
});

describe('SignupService - Daily Limits', () => {
  const userId = 'u_daily_limit_test';
  const orgId = 'org_daily_test';

  beforeEach(async () => {
    await resetDb();
    await seedTestUser(userId, orgId);
    await seedWallet(userId, 100);
  });

  it('returns full limit when no usage today', async () => {
    const limit = await signupService.checkDailyLimit(userId);

    expect(limit.dailyLimit).toBeGreaterThan(0);
    expect(limit.usedToday).toBe(0);
    expect(limit.remaining).toBe(limit.dailyLimit);
    expect(limit.allowed).toBe(true);
  });

  it('tracks usage correctly', async () => {
    // Simulate some usage (debit transactions)
    await prisma.creditTransaction.create({
      data: {
        userId,
        orgId,
        amount: -0.5, // Negative for debit
        type: 'debit',
        reason: 'test usage',
        idempotencyKey: `test_usage_${Date.now()}`,
      },
    });

    const limit = await signupService.checkDailyLimit(userId);

    expect(limit.usedToday).toBe(0.5);
    expect(limit.remaining).toBe(limit.dailyLimit - 0.5);
  });

  it('returns allowed=false when limit exceeded', async () => {
    // Get daily limit
    const initial = await signupService.checkDailyLimit(userId);
    const dailyLimit = initial.dailyLimit;

    // Exceed the limit
    await prisma.creditTransaction.create({
      data: {
        userId,
        orgId,
        amount: -(dailyLimit + 0.1),
        type: 'debit',
        reason: 'exceed limit test',
        idempotencyKey: `exceed_${Date.now()}`,
      },
    });

    const limit = await signupService.checkDailyLimit(userId);

    expect(limit.usedToday).toBeGreaterThan(dailyLimit);
    expect(limit.remaining).toBe(0);
    expect(limit.allowed).toBe(false);
  });
});
