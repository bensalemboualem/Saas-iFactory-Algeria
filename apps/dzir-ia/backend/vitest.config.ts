import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Use Node.js environment
    environment: 'node',

    // Test file patterns
    include: ['tests/**/*.test.ts'],

    // Setup files
    setupFiles: ['./tests/setup.ts'],

    // Global timeout
    testTimeout: 30000,

    // Enable globals (describe, it, expect)
    globals: true,

    // Coverage settings
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'tests/', 'dist/'],
    },

    // Isolate tests
    isolate: true,

    // Reporter
    reporters: ['verbose'],

    // Pool options for better performance
    pool: 'forks',
  },

  // Resolve aliases matching tsconfig
  resolve: {
    alias: {
      '@': './src',
    },
  },
});
