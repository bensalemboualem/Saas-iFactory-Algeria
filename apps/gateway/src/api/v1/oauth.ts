import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import oauthPlugin from '@fastify/oauth2';
import cookie from '@fastify/cookie';
import { appConfig } from '../../config.js';
import { prisma } from '../../db/client.js';
import { generateJWT } from '../../core/auth.js';

interface GoogleUserInfo {
  id: string;
  email: string;
  name: string;
  picture?: string;
}

interface GitHubUserInfo {
  id: number;
  login: string;
  email: string | null;
  name: string | null;
  avatar_url?: string;
}

interface GitHubEmail {
  email: string;
  primary: boolean;
  verified: boolean;
}

export async function oauthRoutes(server: FastifyInstance) {
  // Register cookie plugin
  await server.register(cookie, {
    secret: appConfig.AUTH_SECRET || appConfig.JWT_SECRET,
  });

  // Google OAuth
  if (appConfig.AUTH_GOOGLE_ID && appConfig.AUTH_GOOGLE_SECRET) {
    await server.register(oauthPlugin, {
      name: 'googleOAuth2',
      scope: ['profile', 'email'],
      credentials: {
        client: {
          id: appConfig.AUTH_GOOGLE_ID,
          secret: appConfig.AUTH_GOOGLE_SECRET,
        },
        auth: oauthPlugin.GOOGLE_CONFIGURATION,
      },
      startRedirectPath: '/auth/google',
      callbackUri: `${appConfig.API_BASE_URL}/auth/google/callback`,
    });

    server.get('/auth/google/callback', async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { token } = await (server as any).googleOAuth2.getAccessTokenFromAuthorizationCodeFlow(request);

        // Get user info from Google
        const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
          headers: { Authorization: `Bearer ${token.access_token}` },
        });

        const googleUser = (await response.json()) as GoogleUserInfo;

        // Find or create user
        const user = await findOrCreateUser({
          email: googleUser.email,
          name: googleUser.name,
          provider: 'google',
          providerId: googleUser.id,
          avatar: googleUser.picture,
        });

        if (!user) {
          return reply.redirect(`${appConfig.LANDING_URL}/login?error=user_creation_failed`);
        }

        // Generate JWT
        const jwt = generateJWT(user.id);

        // Redirect to Landing auth callback with token
        return reply.redirect(`${appConfig.LANDING_URL}/auth/callback?token=${jwt}`);
      } catch (error) {
        server.log.error(error, 'Google OAuth callback failed');
        return reply.redirect(`${appConfig.LANDING_URL}/login?error=oauth_failed`);
      }
    });

    server.log.info('Google OAuth enabled');
  }

  // GitHub OAuth
  if (appConfig.AUTH_GITHUB_ID && appConfig.AUTH_GITHUB_SECRET) {
    await server.register(oauthPlugin, {
      name: 'githubOAuth2',
      scope: ['user:email'],
      credentials: {
        client: {
          id: appConfig.AUTH_GITHUB_ID,
          secret: appConfig.AUTH_GITHUB_SECRET,
        },
        auth: oauthPlugin.GITHUB_CONFIGURATION,
      },
      startRedirectPath: '/auth/github',
      callbackUri: `${appConfig.API_BASE_URL}/auth/github/callback`,
    });

    server.get('/auth/github/callback', async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        const { token } = await (server as any).githubOAuth2.getAccessTokenFromAuthorizationCodeFlow(request);

        const headers = {
          Authorization: `Bearer ${token.access_token}`,
          'User-Agent': 'IAFactory-Gateway',
        };

        // Parallel fetch: user info + emails at the same time
        const [userResponse, emailResponse] = await Promise.all([
          fetch('https://api.github.com/user', { headers }),
          fetch('https://api.github.com/user/emails', { headers }),
        ]);

        const [githubUser, emails] = await Promise.all([
          userResponse.json() as Promise<GitHubUserInfo>,
          emailResponse.json() as Promise<GitHubEmail[]>,
        ]);

        // Get email: prefer public, then primary verified, then any
        let email = githubUser.email;
        if (!email && Array.isArray(emails)) {
          const primaryEmail = emails.find(e => e.primary && e.verified);
          email = primaryEmail?.email || emails[0]?.email;
        }

        if (!email) {
          return reply.redirect(`${appConfig.LANDING_URL}/login?error=no_email`);
        }

        // Find or create user
        const user = await findOrCreateUser({
          email,
          name: githubUser.name || githubUser.login,
          provider: 'github',
          providerId: String(githubUser.id),
          avatar: githubUser.avatar_url,
        });

        if (!user) {
          return reply.redirect(`${appConfig.LANDING_URL}/login?error=user_creation_failed`);
        }

        // Generate JWT
        const jwt = generateJWT(user.id);

        // Redirect to Landing auth callback with token
        return reply.redirect(`${appConfig.LANDING_URL}/auth/callback?token=${jwt}`);
      } catch (error) {
        server.log.error(error, 'GitHub OAuth callback failed');
        return reply.redirect(`${appConfig.LANDING_URL}/login?error=oauth_failed`);
      }
    });

    server.log.info('GitHub OAuth enabled');
  }

  // Check if any OAuth is configured
  if (!appConfig.AUTH_GOOGLE_ID && !appConfig.AUTH_GITHUB_ID) {
    server.log.warn('No OAuth providers configured');
  }
}

interface CreateUserInput {
  email: string;
  name: string;
  provider: string;
  providerId: string;
  avatar?: string;
}

async function findOrCreateUser(input: CreateUserInput) {
  // Check if user exists first (fast path)
  const existingUser = await prisma.user.findUnique({
    where: { email: input.email },
    include: { org: true, wallet: true },
  });

  if (existingUser) {
    return existingUser;
  }

  // Create new user with org and wallet in a single transaction
  return prisma.$transaction(async (tx) => {
    // Create default organization
    const org = await tx.org.create({
      data: {
        name: `${input.name}'s Organization`,
        plan: 'free',
      },
    });

    // Create user and wallet in parallel
    const [user] = await Promise.all([
      tx.user.create({
        data: {
          email: input.email,
          name: input.name,
          avatar: input.avatar,
          provider: input.provider,
          providerId: input.providerId,
          orgId: org.id,
          role: 'owner',
          isActive: true,
        },
        include: { org: true, wallet: true },
      }),
    ]);

    // Create wallet (needs user.id so must be after)
    await tx.creditWallet.create({
      data: {
        userId: user.id,
        balance: appConfig.BETA_SIGNUP_CREDITS,
      },
    });

    return user;
  });
}
