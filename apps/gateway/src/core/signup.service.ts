import { PrismaClient } from '../generated/prisma/index.js';
import { appConfig } from '../config.js';

/**
 * Signup Service
 * Handles user onboarding including initial credit grant
 */
export class SignupService {
  constructor(private prisma: PrismaClient) {}

  /**
   * Grant initial credits to a new user (beta mode)
   * Idempotent: will not grant twice for the same user
   *
   * @param userId - The user's ID
   * @returns Object with grant status and balance
   */
  async grantSignupCredits(userId: string): Promise<{
    granted: boolean;
    amount: number;
    balance: number;
    alreadyGranted: boolean;
  }> {
    const amount = appConfig.BETA_SIGNUP_CREDITS;

    // Idempotency key ensures we don't grant twice
    const idempotencyKey = `signup_grant_${userId}`;

    // Check if already granted
    const existing = await this.prisma.creditTransaction.findFirst({
      where: {
        userId,
        idempotencyKey,
      },
    });

    if (existing) {
      const wallet = await this.prisma.creditWallet.findUnique({
        where: { userId },
      });
      console.log(`[SignupService] signup_grant_already_exists ${JSON.stringify({ userId })}`);
      return {
        granted: false,
        amount: 0,
        balance: wallet?.balance ?? 0,
        alreadyGranted: true,
      };
    }

    // Create wallet if doesn't exist, then grant credits
    const result = await this.prisma.$transaction(async (tx) => {
      // Get user's orgId
      const user = await tx.user.findUnique({
        where: { id: userId },
        select: { orgId: true },
      });

      if (!user) {
        throw new Error(`User ${userId} not found`);
      }

      // Upsert wallet
      let wallet = await tx.creditWallet.findUnique({
        where: { userId },
      });

      if (!wallet) {
        wallet = await tx.creditWallet.create({
          data: { userId, balance: 0 },
        });
      }

      // Credit the wallet
      const updatedWallet = await tx.creditWallet.update({
        where: { id: wallet.id },
        data: { balance: { increment: amount } },
      });

      // Record transaction
      await tx.creditTransaction.create({
        data: {
          userId,
          orgId: user.orgId,
          amount,
          type: 'credit',
          reason: 'Beta signup grant',
          idempotencyKey,
        },
      });

      return updatedWallet;
    });

    console.log(
      `[SignupService] signup_grant_ok ${JSON.stringify({
        userId,
        amount,
        newBalance: result.balance,
      })}`
    );

    return {
      granted: true,
      amount,
      balance: result.balance,
      alreadyGranted: false,
    };
  }

  /**
   * Check daily usage limit (beta mode)
   * Returns remaining credits for today
   *
   * @param userId - The user's ID
   * @returns Object with limit info
   */
  async checkDailyLimit(userId: string): Promise<{
    dailyLimit: number;
    usedToday: number;
    remaining: number;
    allowed: boolean;
  }> {
    const dailyLimit = appConfig.BETA_DAILY_LIMIT;

    // Get today's start (UTC)
    const todayStart = new Date();
    todayStart.setUTCHours(0, 0, 0, 0);

    // Sum debits for today
    const todayUsage = await this.prisma.creditTransaction.aggregate({
      where: {
        userId,
        type: 'debit',
        createdAt: { gte: todayStart },
      },
      _sum: { amount: true },
    });

    // amount is negative for debits, so we negate
    const usedToday = Math.abs(todayUsage._sum.amount ?? 0);
    const remaining = Math.max(0, dailyLimit - usedToday);

    return {
      dailyLimit,
      usedToday,
      remaining,
      allowed: remaining > 0,
    };
  }
}
