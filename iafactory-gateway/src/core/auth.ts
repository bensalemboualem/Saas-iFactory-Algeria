import { FastifyRequest, FastifyReply } from 'fastify';
import jwt from 'jsonwebtoken';
import { appConfig } from '../config.js';
import { GatewayError } from './errors.js';
import { prisma } from '../db/client.js';

export interface AuthUser {
  id: string;
  orgId: string;
  email: string;
  role: string;
}

declare module 'fastify' {
  interface FastifyRequest {
    user?: AuthUser;
  }
}

export async function authenticateRequest(
  request: FastifyRequest,
  reply: FastifyReply
): Promise<void> {
  const authHeader = request.headers.authorization;

  if (!authHeader) {
    throw new GatewayError('UNAUTHORIZED', 'Missing authorization header');
  }

  const [type, token] = authHeader.split(' ');

  if (type === 'Bearer' && token.startsWith('iaf_')) {
    // API Key authentication
    await authenticateApiKey(token, request);
  } else if (type === 'Bearer') {
    // JWT authentication
    await authenticateJWT(token, request);
  } else {
    throw new GatewayError('UNAUTHORIZED', 'Invalid authorization type');
  }
}

async function authenticateApiKey(apiKey: string, request: FastifyRequest): Promise<void> {
  const key = await prisma.apiKey.findUnique({
    where: { key: apiKey, isActive: true },
    include: {
      user: {
        include: {
          org: true,
        },
      },
    },
  });

  if (!key || !key.user.isActive) {
    throw new GatewayError('UNAUTHORIZED', 'Invalid or inactive API key');
  }

  // Update last used
  await prisma.apiKey.update({
    where: { id: key.id },
    data: { lastUsedAt: new Date() },
  });

  request.user = {
    id: key.user.id,
    orgId: key.user.orgId,
    email: key.user.email,
    role: key.user.role,
  };
}

async function authenticateJWT(token: string, request: FastifyRequest): Promise<void> {
  try {
    const decoded = jwt.verify(token, appConfig.JWT_SECRET) as any;

    const user = await prisma.user.findUnique({
      where: { id: decoded.userId, isActive: true },
      include: { org: true },
    });

    if (!user) {
      throw new GatewayError('UNAUTHORIZED', 'User not found or inactive');
    }

    request.user = {
      id: user.id,
      orgId: user.orgId,
      email: user.email,
      role: user.role,
    };
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      throw new GatewayError('UNAUTHORIZED', 'Invalid JWT token');
    }
    throw error;
  }
}

export function generateJWT(userId: string, expiresIn: string = '7d'): string {
  return jwt.sign({ userId }, appConfig.JWT_SECRET as string, { expiresIn });
}
