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

import { prisma } from '../db/client.js';

type ReservationStatus = 'RESERVED' | 'FINALIZED' | 'RELEASED';

/** Logger interface for structured logging */
interface Logger {
  info: (obj: Record<string, unknown>, msg: string) => void;
  warn: (obj: Record<string, unknown>, msg: string) => void;
  error: (obj: Record<string, unknown>, msg: string) => void;
}

/** Default console logger */
const defaultLogger: Logger = {
  info: (obj, msg) => console.log(`[CreditsService] ${msg}`, JSON.stringify(obj)),
  warn: (obj, msg) => console.warn(`[CreditsService] ${msg}`, JSON.stringify(obj)),
  error: (obj, msg) => console.error(`[CreditsService] ${msg}`, JSON.stringify(obj)),
};

export class CreditsService {
  private db: typeof prisma;
  private log: Logger;

  constructor(db: typeof prisma, logger?: Logger) {
    this.db = db;
    this.log = logger ?? defaultLogger;
  }

  /**
   * Get current balance for a user
   */
  async getBalance(userId: string): Promise<number> {
    const wallet = await this.db.creditWallet.findUnique({
      where: { userId },
    });
    return wallet?.balance ?? 0;
  }

  /**
   * Ensure user has a wallet (creates if not exists)
   */
  async ensureWallet(userId: string): Promise<void> {
    await this.db.creditWallet.upsert({
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

    return this.db.$transaction(async (tx) => {
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

      const reservation = await tx.creditReservation.create({
        data: {
          userId,
          requestId,
          amount,
          status: 'RESERVED',
          expiresAt,
        },
      });

      // Log successful reservation
      this.log.info(
        { requestId, userId, holdAmount: amount, expiresAt: expiresAt.toISOString() },
        'reserve_ok'
      );

      return reservation;
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
    meta?: Record<string, unknown>;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);
    const finalCost = Number(opts.finalCost);
    const reason = String(opts.reason);
    const orgId = opts.orgId;

    if (!Number.isFinite(finalCost) || finalCost < 0) {
      throw new Error('finalCost must be >= 0');
    }

    return this.db.$transaction(async (tx) => {
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

      // Idempotent debit transaction (uses composite unique index)
      const existingTx = await tx.creditTransaction.findUnique({
        where: {
          userId_idempotencyKey: {
            userId,
            idempotencyKey: requestId,
          },
        },
      });

      if (!existingTx && orgId) {
        // Create debit transaction
        await tx.creditTransaction.create({
          data: {
            userId,
            orgId,
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

      // Log successful finalization
      this.log.info(
        { requestId, userId, finalCost, debit, refund, reserved, reason },
        'finalize_ok'
      );

      return { status: 'OK' as const, debit, refund };
    });
  }

  /**
   * FIX 2: Cleanup expired reservations (TTL leak prevention)
   *
   * Should be called periodically (e.g., cron every 5 min) to release
   * reservations that have expired without being finalized.
   *
   * @returns { cleaned: number } - number of expired reservations released
   */
  async cleanupExpired(): Promise<{ cleaned: number }> {
    const now = new Date();

    // Find all expired RESERVED reservations
    const expired = await this.db.creditReservation.findMany({
      where: {
        status: 'RESERVED',
        expiresAt: { lt: now },
      },
    });

    if (expired.length === 0) {
      return { cleaned: 0 };
    }

    // Release each expired reservation
    let cleaned = 0;
    for (const resv of expired) {
      try {
        await this.db.$transaction(async (tx) => {
          // Double-check still RESERVED (avoid race with finalize)
          const current = await tx.creditReservation.findUnique({
            where: { requestId: resv.requestId },
          });

          if (current?.status !== 'RESERVED') return;

          // Restore balance
          await tx.creditWallet.update({
            where: { userId: resv.userId },
            data: { balance: { increment: resv.amount } },
          });

          // Mark as released (expired)
          await tx.creditReservation.update({
            where: { requestId: resv.requestId },
            data: { status: 'RELEASED' },
          });
        });

        cleaned++;
      } catch {
        // Log but continue with other reservations
        console.warn(`[CreditsService] Failed to cleanup reservation ${resv.requestId}`);
      }
    }

    // Log cleanup results
    if (cleaned > 0) {
      this.log.info(
        { cleaned, total: expired.length },
        'cleanup_expired_ok'
      );
    }

    return { cleaned };
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
    reason?: 'client_close' | 'error' | 'ttl_expired' | 'manual';
    meta?: Record<string, unknown>;
  }) {
    const userId = String(opts.userId);
    const requestId = String(opts.requestId);
    const reason = opts.reason ?? 'manual';

    return this.db.$transaction(async (tx) => {
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

      // Log successful release
      this.log.info(
        { requestId, userId, amount: resv.amount, reason },
        'release_ok'
      );

      return { status: 'OK' as const };
    });
  }
}
