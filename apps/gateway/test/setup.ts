/**
 * Vitest setup file
 * Runs before all tests
 */

import { beforeAll, afterAll } from 'vitest';
import { prisma } from '../src/db/client.js';

beforeAll(async () => {
  // Verify database connection
  try {
    await prisma.$connect();
    console.log('[Test Setup] Database connected');
  } catch (error) {
    console.error('[Test Setup] Failed to connect to database:', error);
    throw error;
  }
});

afterAll(async () => {
  // Disconnect from database
  await prisma.$disconnect();
  console.log('[Test Setup] Database disconnected');
});
