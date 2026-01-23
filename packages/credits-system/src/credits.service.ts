/**
 * PR-003: Production-ready Credits Service
 *
 * Implements atomic reserve/finalize/release pattern to prevent:
 * - TOCTOU (Time-of-Check-Time-of-Use) race conditions
 * - Streaming bypass (getting data without paying)
 * - Double-spend via concurrent requests
 *
 * All operations are idempotent via requestId.
 */

import type { PrismaClient } from '@prisma/client';

type ReservationStatus = 'RESERVED' | 'FINALIZED' | 'RELEASED';

export class CreditsService {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get current balance for a user
   */
  async getBalance(userId: string): Promise<number> {
    const wallet = await this.prisma.creditWallet.findUnique({
      where: { userId },
    });
    return wallet?.balance ?? 0;
  }

  /**
   * Ensure user has a wallet (creates if not exists)
   */
  async ensureWallet(userId: string): Promise<void> {
    await this.prisma.creditWallet.upsert({
      where: { userId },
      update: {},
      create: { userId, balance: 0 },
    });
  }

  /**
   * Reserve credits BEFORE doing any costly work (LLM streaming).
   *
   * - Atomic: check + decrement in single transaction (no TOCTOU)
   * - Idempotent: same requestId returns existing reservation
   * - TTL: reservation expires after ttlSeconds (default 5 min)
   *
   * @throws Error with message "INSUFFICIENT_CREDITS" if balance too low
   * @throws Error with message "WALLET_MISSING" if no wallet
   */
  async reserve(opts: {
    userId: string;
    requestId: string;
    amount: number;
    ttlSeconds?: number;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);
    const amount = Number(opts.amount);
    const ttlSeconds = opts.ttlSeconds ?? 300;

    if (!userId) throw new Error('userId required');
    if (!requestId) throw new Error('requestId required');
    if (!Number.isFinite(amount) || amount <= 0) throw new Error('amount must be > 0');

    return this.prisma.$transaction(async (tx) => {
      // Ensure wallet exists
      await tx.creditWallet.upsert({
        where: { userId },
        update: {},
        create: { userId, balance: 0 },
      });

      // Idempotency: if reservation already exists, return it
      const existing = await tx.creditReservation.findUnique({
        where: { requestId },
      });
      if (existing) return existing;

      // Get current balance
      const wallet = await tx.creditWallet.findUnique({
        where: { userId },
      });
      if (!wallet) throw new Error('WALLET_MISSING');

      // Check sufficient balance
      if (wallet.balance < amount) {
        throw new Error('INSUFFICIENT_CREDITS');
      }

      // Atomic decrement (hold)
      await tx.creditWallet.update({
        where: { userId },
        data: { balance: { decrement: amount } },
      });

      // Create reservation
      const expiresAt = new Date(Date.now() + ttlSeconds * 1000);

      return tx.creditReservation.create({
        data: {
          userId,
          requestId,
          amount,
          status: 'RESERVED',
          expiresAt,
        },
      });
    });
  }

  /**
   * Finalize: convert reserved credits into actual debit transaction.
   *
   * - If finalCost < reserved: refunds the difference
   * - If finalCost > reserved: only debits reserved amount (never goes negative)
   * - Idempotent via CreditTransaction.idempotencyKey
   *
   * @returns { status: 'OK' | 'OK_IDEMPOTENT', debit, refund }
   */
  async finalize(opts: {
    userId: string;
    requestId: string;
    finalCost: number;
    reason: string;
    orgId?: string;
    meta?: Record<string, any>;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);
    const finalCost = Number(opts.finalCost);
    const reason = String(opts.reason);
    const orgId = opts.orgId;

    if (!Number.isFinite(finalCost) || finalCost < 0) {
      throw new Error('finalCost must be >= 0');
    }

    return this.prisma.$transaction(async (tx) => {
      // Get reservation
      const resv = await tx.creditReservation.findUnique({
        where: { requestId },
      });
      if (!resv) throw new Error('RESERVATION_NOT_FOUND');
      if (resv.userId !== userId) throw new Error('RESERVATION_OWNER_MISMATCH');

      const status = resv.status as ReservationStatus;

      // Idempotent: already finalized
      if (status === 'FINALIZED') {
        return { status: 'OK_IDEMPOTENT' as const, debit: 0, refund: 0 };
      }

      // Cannot finalize a released reservation
      if (status === 'RELEASED') {
        throw new Error('RESERVATION_ALREADY_RELEASED');
      }

      const reserved = Number(resv.amount);
      const debit = Math.min(finalCost, reserved);
      const refund = reserved - debit;

      // Idempotent debit transaction (uses existing idempotencyKey field)
      const existingTx = await tx.creditTransaction.findFirst({
        where: {
          userId,
          idempotencyKey: requestId,
        },
      });

      if (!existingTx) {
        // Create debit transaction
        await tx.creditTransaction.create({
          data: {
            userId,
            orgId: orgId || userId, // fallback to userId if no orgId
            amount: -debit,
            type: 'debit',
            reason,
            idempotencyKey: requestId,
          },
        });
      }

      // Refund remainder to wallet
      if (refund > 0) {
        await tx.creditWallet.update({
          where: { userId },
          data: { balance: { increment: refund } },
        });
      }

      // Mark reservation as finalized
      await tx.creditReservation.update({
        where: { requestId },
        data: { status: 'FINALIZED' },
      });

      return { status: 'OK' as const, debit, refund };
    });
  }

  /**
   * Release: restore reserved credits back to wallet (e.g., on error/abort).
   *
   * - Safe to call multiple times (idempotent)
   * - Does nothing if already finalized or released
   */
  async release(opts: {
    userId: string;
    requestId: string;
    meta?: Record<string, any>;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);

    return this.prisma.$transaction(async (tx) => {
      // Get reservation
      const resv = await tx.creditReservation.findUnique({
        where: { requestId },
      });

      // No reservation found - nothing to release
      if (!resv) return { status: 'NOOP' as const };

      // Wrong owner
      if (resv.userId !== userId) {
        throw new Error('RESERVATION_OWNER_MISMATCH');
      }

      const status = resv.status as ReservationStatus;

      // Already finalized or released - nothing to do
      if (status !== 'RESERVED') {
        return { status: 'NOOP' as const };
      }

      // Restore balance
      await tx.creditWallet.update({
        where: { userId },
        data: { balance: { increment: resv.amount } },
      });

      // Mark as released
      await tx.creditReservation.update({
        where: { requestId },
        data: { status: 'RELEASED' },
      });

      return { status: 'OK' as const };
    });
  }

  /**
   * Add credits to a user's wallet (e.g., after payment webhook)
   *
   * - Idempotent via requestId (payment event ID)
   */
  async credit(opts: {
    userId: string;
    requestId: string;
    amount: number;
    reason: string;
    orgId?: string;
    meta?: Record<string, any>;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);
    const amount = Number(opts.amount);
    const reason = String(opts.reason);
    const orgId = opts.orgId;

    if (!Number.isFinite(amount) || amount <= 0) {
      throw new Error('amount must be > 0');
    }

    return this.prisma.$transaction(async (tx) => {
      // Ensure wallet exists
      await tx.creditWallet.upsert({
        where: { userId },
        update: {},
        create: { userId, balance: 0 },
      });

      // Idempotency check
      const existingTx = await tx.creditTransaction.findFirst({
        where: {
          userId,
          idempotencyKey: requestId,
        },
      });
      if (existingTx) {
        return { status: 'OK_IDEMPOTENT' as const };
      }

      // Add to balance
      await tx.creditWallet.update({
        where: { userId },
        data: { balance: { increment: amount } },
      });

      // Create credit transaction
      await tx.creditTransaction.create({
        data: {
          userId,
          orgId: orgId || userId,
          amount: amount,
          type: 'credit',
          reason,
          idempotencyKey: requestId,
        },
      });

      return { status: 'OK' as const };
    });
  }
}
