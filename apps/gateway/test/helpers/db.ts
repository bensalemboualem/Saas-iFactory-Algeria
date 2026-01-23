/**
 * Test database helpers
 * Provides reset and seed functions for isolated test runs
 */

import { prisma } from '../../src/db/client.js';

/**
 * Reset all credit-related tables for clean test state
 * Order matters due to foreign key constraints
 */
export async function resetDb() {
  // Delete in correct order (children first)
  await prisma.usageLedger.deleteMany();
  await prisma.creditTransaction.deleteMany();
  await prisma.creditReservation.deleteMany();
  await prisma.creditWallet.deleteMany();
}

/**
 * Seed a wallet with a specific balance
 */
export async function seedWallet(userId: string, balance: number) {
  await prisma.creditWallet.upsert({
    where: { userId },
    update: { balance },
    create: { userId, balance },
  });
}

/**
 * Create a test user with org (required for credit transactions)
 */
export async function seedTestUser(userId: string, orgId: string) {
  // Ensure org exists
  await prisma.org.upsert({
    where: { id: orgId },
    update: {},
    create: {
      id: orgId,
      name: 'Test Org',
      slug: `test-org-${orgId}`,
    },
  });

  // Ensure user exists
  await prisma.user.upsert({
    where: { id: userId },
    update: {},
    create: {
      id: userId,
      email: `test-${userId}@test.local`,
      orgId,
    },
  });
}

/**
 * Full test setup: user + org + wallet
 */
export async function setupTestUserWithBalance(
  userId: string,
  orgId: string,
  balance: number
) {
  await seedTestUser(userId, orgId);
  await seedWallet(userId, balance);
}
