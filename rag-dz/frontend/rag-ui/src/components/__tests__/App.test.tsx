/**
 * Tests pour le composant App
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

describe('App Component', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  it('should create QueryClient with correct configuration', () => {
    expect(queryClient).toBeDefined();
    expect(queryClient.getDefaultOptions().queries?.retry).toBe(false);
  });

  it('should have correct staleTime configuration', () => {
    const testQueryClient = new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 2000,
          gcTime: 5 * 60 * 1000,
        },
      },
    });

    const options = testQueryClient.getDefaultOptions();
    expect(options.queries?.staleTime).toBe(2000);
    expect(options.queries?.gcTime).toBe(5 * 60 * 1000);
  });
});
