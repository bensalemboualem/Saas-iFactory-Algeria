/**
 * Reservation Guard Middleware
 *
 * Rejects any request without a valid x-reservation-id from Gateway.
 * This ensures ALL credits are managed atomically by the Gateway.
 *
 * Pattern: Client → Gateway.reserve() → dzir-ia (with x-reservation-id) → Gateway.finalize()
 *
 * Includes circuit-breaker for Gateway unavailability.
 */

import { Context, Next, MiddlewareHandler } from 'hono';

// ============================================================================
// CONFIGURATION
// ============================================================================

const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:3001';
const CREDITS_ENABLED = process.env.CREDITS_ENABLED !== 'false';

// Circuit breaker settings
const CIRCUIT_BREAKER_THRESHOLD = 5;        // Failures before opening circuit
const CIRCUIT_BREAKER_TIMEOUT_MS = 30_000;  // Time to wait before half-open
const REQUEST_TIMEOUT_MS = 5_000;           // Max wait for Gateway response

// ============================================================================
// CIRCUIT BREAKER STATE
// ============================================================================

interface CircuitBreakerState {
  failures: number;
  lastFailure: number;
  state: 'CLOSED' | 'OPEN' | 'HALF_OPEN';
}

const circuitBreaker: CircuitBreakerState = {
  failures: 0,
  lastFailure: 0,
  state: 'CLOSED',
};

function recordSuccess(): void {
  circuitBreaker.failures = 0;
  circuitBreaker.state = 'CLOSED';
}

function recordFailure(): void {
  circuitBreaker.failures++;
  circuitBreaker.lastFailure = Date.now();

  if (circuitBreaker.failures >= CIRCUIT_BREAKER_THRESHOLD) {
    circuitBreaker.state = 'OPEN';
    console.warn(`[reservation-guard] Circuit OPEN after ${circuitBreaker.failures} failures`);
  }
}

function canAttempt(): boolean {
  if (circuitBreaker.state === 'CLOSED') {
    return true;
  }

  if (circuitBreaker.state === 'OPEN') {
    const elapsed = Date.now() - circuitBreaker.lastFailure;
    if (elapsed >= CIRCUIT_BREAKER_TIMEOUT_MS) {
      circuitBreaker.state = 'HALF_OPEN';
      console.info('[reservation-guard] Circuit HALF_OPEN, attempting probe');
      return true;
    }
    return false;
  }

  // HALF_OPEN: allow one request through
  return true;
}

// ============================================================================
// TYPES
// ============================================================================

export interface ReservationInfo {
  requestId: string;
  userId: string;
  amount: number;
  status: 'RESERVED' | 'FINALIZED' | 'RELEASED';
  expiresAt: string;
}

export interface ValidationResult {
  valid: boolean;
  reservation?: ReservationInfo;
  error?: string;
}

// ============================================================================
// MAIN MIDDLEWARE
// ============================================================================

/**
 * Middleware that rejects requests without valid x-reservation-id.
 *
 * Usage:
 *   app.use('/ask', reservationGuard());
 *   app.use('/search', reservationGuard());
 *   app.use('/capture', reservationGuard());
 */
export function reservationGuard(): MiddlewareHandler {
  return async (c: Context, next: Next) => {
    // Skip if credits disabled (dev/test mode)
    if (!CREDITS_ENABLED) {
      await next();
      return;
    }

    // Extract reservation ID from header
    const reservationId = c.req.header('x-reservation-id');

    if (!reservationId) {
      return c.json({
        error: 'MISSING_RESERVATION',
        message: 'x-reservation-id header required. Call Gateway POST /api/credits/reserve first.',
        hint: 'Flow: 1) POST Gateway /api/credits/reserve → get requestId, 2) Call this endpoint with x-reservation-id: {requestId}',
      }, 400);
    }

    // Extract auth token (needed to verify ownership)
    const token = c.req.header('authorization')?.replace(/^Bearer\s+/i, '');
    if (!token) {
      return c.json({ error: 'UNAUTHORIZED', message: 'Authorization header required' }, 401);
    }

    // Check circuit breaker
    if (!canAttempt()) {
      return c.json({
        error: 'CREDITS_SERVICE_UNAVAILABLE',
        message: 'Credits service temporarily unavailable. Circuit breaker OPEN.',
        retryAfter: Math.ceil((CIRCUIT_BREAKER_TIMEOUT_MS - (Date.now() - circuitBreaker.lastFailure)) / 1000),
      }, 503);
    }

    // Validate reservation with Gateway
    const validation = await validateReservation(token, reservationId);

    if (!validation.valid) {
      return c.json({
        error: 'INVALID_RESERVATION',
        message: validation.error || 'Reservation not found, expired, or unauthorized.',
        reservationId,
      }, 402);
    }

    const reservation = validation.reservation!;

    if (reservation.status !== 'RESERVED') {
      return c.json({
        error: 'RESERVATION_NOT_ACTIVE',
        message: `Reservation status is '${reservation.status}', expected 'RESERVED'.`,
        reservationId,
        status: reservation.status,
      }, 409);
    }

    // Check expiration client-side (defense in depth)
    if (new Date(reservation.expiresAt) < new Date()) {
      return c.json({
        error: 'RESERVATION_EXPIRED',
        message: 'Reservation has expired. Create a new reservation.',
        reservationId,
        expiresAt: reservation.expiresAt,
      }, 410);
    }

    // Store reservation info for handler use
    c.set('reservationId', reservationId);
    c.set('reservationAmount', reservation.amount);
    c.set('reservationUserId', reservation.userId);

    // Execute the handler
    await next();
  };
}

// ============================================================================
// GATEWAY COMMUNICATION
// ============================================================================

/**
 * Validate a reservation ID with the Gateway
 */
async function validateReservation(
  token: string,
  reservationId: string
): Promise<ValidationResult> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${GATEWAY_URL}/api/credits/reservation/${reservationId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
      },
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (response.status === 404) {
      recordSuccess(); // Gateway is up, reservation just doesn't exist
      return { valid: false, error: 'Reservation not found' };
    }

    if (response.status === 403) {
      recordSuccess();
      return { valid: false, error: 'Reservation belongs to another user' };
    }

    if (!response.ok) {
      recordFailure();
      return { valid: false, error: `Gateway error: ${response.status}` };
    }

    const data = await response.json();
    recordSuccess();

    return {
      valid: true,
      reservation: {
        requestId: data.requestId,
        userId: data.userId,
        amount: data.amount,
        status: data.status,
        expiresAt: data.expiresAt,
      },
    };
  } catch (error) {
    clearTimeout(timeout);

    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error(`[reservation-guard] Gateway validation failed: ${message}`);

    recordFailure();
    return { valid: false, error: `Gateway unavailable: ${message}` };
  }
}

/**
 * Finalize a reservation after successful operation.
 * Call this at the END of your handler after success.
 *
 * @param c - Hono context
 * @param actualCost - The real cost (may differ from reserved amount)
 */
export async function finalizeReservation(
  c: Context,
  actualCost: number
): Promise<{ success: boolean; refund?: number; error?: string }> {
  if (!CREDITS_ENABLED) {
    return { success: true };
  }

  const reservationId = c.get('reservationId') as string | undefined;
  const token = c.req.header('authorization')?.replace(/^Bearer\s+/i, '');

  if (!reservationId || !token) {
    return { success: false, error: 'No reservation in context' };
  }

  if (!canAttempt()) {
    console.warn('[reservation-guard] Cannot finalize: circuit OPEN');
    return { success: false, error: 'Circuit breaker OPEN' };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${GATEWAY_URL}/api/credits/finalize`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        requestId: reservationId,
        finalCost: actualCost,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      recordFailure();
      return {
        success: false,
        error: errorData.error || `Finalize failed: ${response.status}`
      };
    }

    const data = await response.json();
    recordSuccess();

    return {
      success: true,
      refund: data.refund || 0,
    };
  } catch (error) {
    clearTimeout(timeout);
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error(`[reservation-guard] Finalize failed: ${message}`);
    recordFailure();
    return { success: false, error: message };
  }
}

/**
 * Release a reservation (refund all held credits).
 * Call this on ERROR or CLIENT ABORT.
 *
 * @param c - Hono context
 * @param reason - Why we're releasing (for audit logs)
 */
export async function releaseReservation(
  c: Context,
  reason: 'error' | 'client_abort' | 'timeout' | 'validation_failed'
): Promise<{ success: boolean; error?: string }> {
  if (!CREDITS_ENABLED) {
    return { success: true };
  }

  const reservationId = c.get('reservationId') as string | undefined;
  const token = c.req.header('authorization')?.replace(/^Bearer\s+/i, '');

  if (!reservationId || !token) {
    return { success: true }; // Nothing to release
  }

  if (!canAttempt()) {
    console.warn('[reservation-guard] Cannot release: circuit OPEN (will be cleaned up by TTL)');
    return { success: false, error: 'Circuit breaker OPEN, TTL will cleanup' };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${GATEWAY_URL}/api/credits/release`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        requestId: reservationId,
        reason,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      // Don't record failure for release - it's best-effort
      // TTL cleanup will handle it if this fails
      console.warn(`[reservation-guard] Release returned ${response.status}`);
    }

    recordSuccess();
    return { success: true };
  } catch (error) {
    clearTimeout(timeout);
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.warn(`[reservation-guard] Release failed (TTL will cleanup): ${message}`);
    // Don't record failure - release is best-effort
    return { success: false, error: message };
  }
}

// ============================================================================
// HELPERS
// ============================================================================

/**
 * Get reservation info from context (after guard passed)
 */
export function getReservationFromContext(c: Context): {
  reservationId: string | undefined;
  amount: number;
  userId: string | undefined;
} {
  return {
    reservationId: c.get('reservationId'),
    amount: c.get('reservationAmount') || 0,
    userId: c.get('reservationUserId'),
  };
}

/**
 * Get circuit breaker status (for health checks)
 */
export function getCircuitBreakerStatus(): {
  state: string;
  failures: number;
  lastFailure: number | null;
} {
  return {
    state: circuitBreaker.state,
    failures: circuitBreaker.failures,
    lastFailure: circuitBreaker.lastFailure || null,
  };
}
