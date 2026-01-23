import { Context, Next } from 'hono';
import {
  jwtVerify,
  importSPKI,
  createRemoteJWKSet,
  type KeyLike,
  type JWTVerifyGetKey,
  type JWTVerifyOptions,
} from 'jose';
import type { AuthContext, JWTPayload } from '../types/index.js';

// Environment configuration
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:3000';
const JWT_PUBLIC_KEY = process.env.JWT_PUBLIC_KEY || '';
const JWT_ISSUER = process.env.JWT_ISSUER || '';
const JWT_AUDIENCE = process.env.JWT_AUDIENCE || '';
const NODE_ENV = process.env.NODE_ENV || 'development';

// Dev-only: bypass auth for local testing (NEVER enable in production)
const AUTH_BYPASS_ENABLED = process.env.AUTH_BYPASS === 'true' && NODE_ENV === 'development';
const AUTH_BYPASS_USER_ID = process.env.AUTH_BYPASS_USER_ID || 'dev-user-001';

// Verification mode
type VerifyMode = 'local' | 'remote';

// Cached key/keyset
let cachedLocalKey: KeyLike | null = null;
let cachedRemoteJWKS: JWTVerifyGetKey | null = null;
let verifyMode: VerifyMode | null = null;

/**
 * Initialize and cache the local PEM key
 */
async function getLocalKey(): Promise<KeyLike> {
  if (!cachedLocalKey) {
    try {
      cachedLocalKey = await importSPKI(JWT_PUBLIC_KEY, 'RS256');
      console.log('Using local PEM public key for JWT verification');
    } catch (error) {
      console.error('Failed to import JWT_PUBLIC_KEY:', error);
      throw new Error('Invalid JWT_PUBLIC_KEY format. Expected PEM public key.');
    }
  }
  return cachedLocalKey;
}

/**
 * Initialize and cache the remote JWKS
 */
function getRemoteJWKS(): JWTVerifyGetKey {
  if (!cachedRemoteJWKS) {
    const jwksUrl = new URL(`${GATEWAY_URL}/.well-known/jwks.json`);
    cachedRemoteJWKS = createRemoteJWKSet(jwksUrl);
    console.log(`Using remote JWKS from ${jwksUrl.toString()}`);
  }
  return cachedRemoteJWKS;
}

/**
 * Determine which verification mode to use
 */
function getVerifyMode(): VerifyMode {
  if (verifyMode === null) {
    verifyMode = JWT_PUBLIC_KEY ? 'local' : 'remote';
  }
  return verifyMode;
}

/**
 * Build JWT verification options
 */
function getVerifyOptions(): JWTVerifyOptions {
  const options: JWTVerifyOptions = {};

  if (JWT_ISSUER) {
    options.issuer = JWT_ISSUER;
  } else if (NODE_ENV === 'production') {
    console.warn('WARNING: JWT_ISSUER not set in production. This is a security risk.');
  }

  if (JWT_AUDIENCE) {
    options.audience = JWT_AUDIENCE;
  } else if (NODE_ENV === 'production') {
    console.warn('WARNING: JWT_AUDIENCE not set in production. Consider setting it.');
  }

  return options;
}

/**
 * Auth middleware - validates JWT and sets auth context
 */
export async function authMiddleware(c: Context, next: Next) {
  // Dev-only bypass for local testing
  if (AUTH_BYPASS_ENABLED) {
    console.warn('⚠️  AUTH BYPASS ENABLED - dev mode only');
    const authContext: AuthContext = {
      userId: AUTH_BYPASS_USER_ID,
      email: 'dev@test.local',
      plan: 'pro',
    };
    c.set('auth', authContext);
    await next();
    return;
  }

  const authHeader = c.req.header('Authorization');

  if (!authHeader?.startsWith('Bearer ')) {
    return c.json(
      {
        error: 'Unauthorized',
        message: 'Missing or invalid Authorization header. Expected: Bearer <token>',
      },
      401
    );
  }

  const token = authHeader.slice(7);

  if (!token || token.length < 10) {
    return c.json(
      {
        error: 'Unauthorized',
        message: 'Invalid token format',
      },
      401
    );
  }

  try {
    const mode = getVerifyMode();
    const options = getVerifyOptions();

    // Verify JWT based on mode (different overloads for KeyLike vs JWTVerifyGetKey)
    const { payload } = mode === 'local'
      ? await jwtVerify(token, await getLocalKey(), options)
      : await jwtVerify(token, getRemoteJWKS(), options);

    // Validate required claims
    if (!payload.sub) {
      console.warn('JWT missing sub claim');
      return c.json(
        {
          error: 'Unauthorized',
          message: 'Invalid token: missing subject',
        },
        401
      );
    }

    // Extract and validate payload
    const jwtPayload = payload as unknown as JWTPayload;

    // Build auth context with required and optional fields
    const authContext: AuthContext = {
      userId: jwtPayload.sub,
      email: jwtPayload.email || '',
      plan: jwtPayload.plan || 'free',
    };

    // Set auth context for downstream handlers
    c.set('auth', authContext);

    await next();
  } catch (error) {
    // Log detailed error for debugging (not exposed to client)
    if (error instanceof Error) {
      console.error('JWT verification failed:', {
        name: error.name,
        message: error.message,
        // Don't log the full error in production
        ...(NODE_ENV === 'development' && { stack: error.stack }),
      });
    }

    // Return generic error to client
    return c.json(
      {
        error: 'Unauthorized',
        message: 'Invalid or expired token',
      },
      401
    );
  }
}

/**
 * Get auth context from request
 * Call this in route handlers after authMiddleware
 */
export function getAuth(c: Context): AuthContext {
  const auth = c.get('auth') as AuthContext | undefined;

  if (!auth) {
    // This should never happen if authMiddleware ran first
    throw new Error('Auth context not found. Ensure authMiddleware is applied.');
  }

  return auth;
}

/**
 * Optional: Check if user has specific plan
 */
export function requirePlan(...allowedPlans: string[]) {
  return async (c: Context, next: Next) => {
    const auth = getAuth(c);

    if (!allowedPlans.includes(auth.plan)) {
      return c.json(
        {
          error: 'Forbidden',
          message: `This endpoint requires one of these plans: ${allowedPlans.join(', ')}`,
          currentPlan: auth.plan,
        },
        403
      );
    }

    await next();
  };
}

/**
 * Clear cached keys (useful for testing or key rotation)
 */
export function clearKeyCache(): void {
  cachedLocalKey = null;
  cachedRemoteJWKS = null;
}
