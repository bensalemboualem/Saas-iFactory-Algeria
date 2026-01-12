import { prisma } from '../db/client.js';
import { GatewayError } from './errors.js';
import { calculateCost } from './usage.js';

type CreditAction = 'reserve' | 'debit' | 'release';

export async function checkAndDebitCredits(
  userId: string,
  model: string,
  action: CreditAction,
  tokens: number = 0
): Promise<boolean> {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { wallet: true },
  });

  if (!user || !user.wallet) {
    throw new GatewayError('USER_NOT_FOUND', 'User or wallet not found');
  }

  const estimatedTokens = tokens || 1000; // Reserve estimate
  const cost = calculateCost(model, estimatedTokens);

  switch (action) {
    case 'reserve':
      // Check if user has enough credits
      if (user.wallet.balance < cost) {
        return false;
      }
      // Reserve credits (optional: track reserved credits separately)
      return true;

    case 'debit':
      // Actual debit
      const actualCost = calculateCost(model, tokens);
      
      if (user.wallet.balance < actualCost) {
        throw new GatewayError('INSUFFICIENT_CREDITS', 'Insufficient credits');
      }

      // Atomic transaction: debit wallet + create ledger entry
      await prisma.$transaction([
        prisma.creditWallet.update({
          where: { id: user.wallet.id },
          data: { balance: { decrement: actualCost } },
        }),
        prisma.usageLedger.create({
          data: {
            userId,
            orgId: user.orgId,
            model,
            tokens,
            cost: actualCost,
            provider: getProviderFromModel(model),
            metadata: {},
          },
        }),
      ]);

      return true;

    case 'release':
      // Release reserved credits (if tracking reserves)
      return true;

    default:
      throw new Error(`Invalid credit action: ${action}`);
  }
}

export async function addCredits(
  userId: string,
  amount: number,
  reason: string
): Promise<void> {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { wallet: true },
  });

  if (!user || !user.wallet) {
    throw new GatewayError('USER_NOT_FOUND', 'User or wallet not found');
  }

  await prisma.$transaction([
    prisma.creditWallet.update({
      where: { id: user.wallet.id },
      data: { balance: { increment: amount } },
    }),
    prisma.creditTransaction.create({
      data: {
        userId,
        orgId: user.orgId,
        amount,
        type: 'credit',
        reason,
      },
    }),
  ]);
}

export async function getBalance(userId: string): Promise<number> {
  const wallet = await prisma.creditWallet.findUnique({
    where: { userId },
  });

  return wallet?.balance || 0;
}

function getProviderFromModel(model: string): string {
  if (model.startsWith('iaf-fast')) return 'groq';
  if (model.startsWith('iaf-smart')) return 'openrouter';
  if (model.startsWith('iaf-cheap')) return 'deepseek';
  if (model.startsWith('iaf-local')) return 'ollama';
  return 'unknown';
}
