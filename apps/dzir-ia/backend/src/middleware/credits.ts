import { Context, Next, MiddlewareHandler } from 'hono';
import { nanoid } from 'nanoid';
import { getOperationCost, OPERATION_COSTS, type Operation, type CaptureSourceType } from '../config/costs.js';

const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:3000';

// Skip credits check in test mode or when disabled
const CREDITS_ENABLED = process.env.CREDITS_ENABLED !== 'false';

// Fail closed in production (deny if Gateway down), fail open in dev
const FAIL_OPEN = process.env.CREDITS_FAIL_OPEN === 'true';

export interface CreditsCheckResult {
  allowed: boolean;
  balance: number;
}

export interface CreditsDeductResult {
  success: boolean;
  newBalance: number;
  transactionId: string;
  idempotent?: boolean;
}

/**
 * Create credits middleware for a specific operation
 * Checks credits before operation, deducts after success
 */
export function creditsMiddleware(
  operation: Operation,
  subType?: CaptureSourceType
): MiddlewareHandler {
  return async (c: Context, next: Next) => {
    // Skip if credits disabled
    if (!CREDITS_ENABLED) {
      await next();
      return;
    }

    const token = c.req.header('Authorization')?.slice(7);
    if (!token) {
      return c.json({ error: 'Missing token' }, 401);
    }

    const cost = getOperationCost(operation, subType);

    // Use client-provided idempotency key or generate one
    const idempotencyKey = c.req.header('Idempotency-Key') || nanoid();
    c.set('idempotencyKey', idempotencyKey);
    c.set('creditsCost', cost);
    c.set('creditsOperation', operation);

    try {
      // Step 1: Check credits
      const checkResult = await checkCredits(token, operation, cost);

      if (!checkResult.allowed) {
        return c.json(
          {
            error: 'INSUFFICIENT_CREDITS',
            message: `Insufficient credits. Required: ${cost}, available: ${checkResult.balance}`,
            required: cost,
            balance: checkResult.balance,
          },
          402
        );
      }

      // Store check result for later use
      c.set('creditsBalance', checkResult.balance);

      // Step 2: Execute the operation
      await next();

      // Step 3: Deduct credits after successful operation
      // Only deduct if response status is 2xx
      const status = c.res?.status || 200;
      if (status >= 200 && status < 300) {
        await deductCredits(token, operation, cost, idempotencyKey);
      }
    } catch (error) {
      console.error('Credits check failed:', error);

      if (FAIL_OPEN) {
        // Dev mode: allow operation if Gateway is down
        await next();
      } else {
        // Prod mode: fail closed - deny if Gateway is down
        return c.json(
          {
            error: 'CREDITS_SERVICE_UNAVAILABLE',
            message: 'Credits service is temporarily unavailable. Please try again later.',
          },
          503
        );
      }
    }
  };
}

/**
 * Charge credits for dynamic operations (like capture with variable source type)
 * Use this inside a route handler when cost depends on request data
 */
export async function chargeCredits(
  c: Context,
  operation: string,
  cost: number
): Promise<{ success: boolean; error?: string }> {
  // Skip if credits disabled
  if (!CREDITS_ENABLED) {
    return { success: true };
  }

  const token = c.req.header('Authorization')?.slice(7);
  if (!token) {
    return { success: false, error: 'Missing token' };
  }

  // Use client-provided idempotency key or generate one
  const idempotencyKey = c.req.header('Idempotency-Key') || c.get('idempotencyKey') || nanoid();
  c.set('idempotencyKey', idempotencyKey);

  try {
    // Check credits
    const checkResult = await checkCredits(token, operation, cost);

    if (!checkResult.allowed) {
      return {
        success: false,
        error: `Insufficient credits. Required: ${cost}, available: ${checkResult.balance}`,
      };
    }

    // Store for context
    c.set('creditsBalance', checkResult.balance);
    c.set('creditsCost', cost);
    c.set('creditsOperation', operation);

    return { success: true };
  } catch (error) {
    console.error('Credits check failed:', error);

    if (FAIL_OPEN) {
      return { success: true }; // Allow in dev
    }

    return { success: false, error: 'Credits service unavailable' };
  }
}

/**
 * Finalize credits deduction after successful operation
 * Call this at the end of a handler that used chargeCredits
 */
export async function finalizeCredits(c: Context): Promise<void> {
  if (!CREDITS_ENABLED) return;

  const token = c.req.header('Authorization')?.slice(7);
  const idempotencyKey = c.get('idempotencyKey');
  const operation = c.get('creditsOperation');
  const cost = c.get('creditsCost');

  if (!token || !idempotencyKey || !operation || !cost) return;

  await deductCredits(token, operation, cost, idempotencyKey);
}

/**
 * Get capture cost based on source type
 */
export function getCaptureCost(sourceType: string): number {
  const costs = OPERATION_COSTS.capture;
  return costs[sourceType as CaptureSourceType] || costs.text;
}

/**
 * Check if user has sufficient credits
 */
async function checkCredits(
  token: string,
  operation: string,
  cost: number
): Promise<CreditsCheckResult> {
  const response = await fetch(`${GATEWAY_URL}/api/credits/check`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      operation,
      cost,
    }),
  });

  if (response.status === 402) {
    const data = await response.json();
    return {
      allowed: false,
      balance: data.balance || 0,
    };
  }

  if (!response.ok) {
    throw new Error(`Credits check failed: ${response.status}`);
  }

  const data = await response.json();
  return {
    allowed: data.allowed,
    balance: data.balance,
  };
}

/**
 * Deduct credits from user's wallet
 */
async function deductCredits(
  token: string,
  operation: string,
  cost: number,
  idempotencyKey: string
): Promise<CreditsDeductResult | null> {
  try {
    const response = await fetch(`${GATEWAY_URL}/api/credits/deduct`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        operation,
        cost,
        idempotencyKey,
      }),
    });

    if (!response.ok) {
      console.error('Failed to deduct credits:', response.status);
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to deduct credits:', error);
    return null;
  }
}

/**
 * Get user's current credit balance
 */
export async function getUserBalance(token: string): Promise<number> {
  try {
    const response = await fetch(`${GATEWAY_URL}/api/credits/balance`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      return 0;
    }

    const data = await response.json();
    return data.balance || 0;
  } catch {
    return 0;
  }
}

/**
 * Get credits balance stored in context (from check)
 */
export function getCreditsFromContext(c: Context): number {
  return c.get('creditsBalance') || 0;
}
