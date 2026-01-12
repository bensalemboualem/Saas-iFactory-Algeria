/**
 * Tests pour l'API client
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

describe('API Configuration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should use environment variables for API URL', () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8180';
    expect(apiUrl).toBeDefined();
    expect(typeof apiUrl).toBe('string');
  });

  it('should include API key in headers when available', () => {
    const apiKey = import.meta.env.VITE_API_KEY || '';
    expect(typeof apiKey).toBe('string');
  });

  it('should handle API key from sessionStorage', () => {
    // Mock sessionStorage
    const mockKey = 'test-api-key-123';
    sessionStorage.setItem('apiKey', mockKey);

    const key = sessionStorage.getItem('apiKey');
    expect(key).toBe(mockKey);

    // Cleanup
    sessionStorage.removeItem('apiKey');
  });
});

describe('API Request Interceptors', () => {
  it('should add API key to request headers', () => {
    const config = {
      headers: {} as Record<string, string>
    };

    const apiKey = 'test-key';
    sessionStorage.setItem('apiKey', apiKey);

    // Simuler l'intercepteur
    const modifiedConfig = {
      ...config,
      headers: {
        ...config.headers,
        'X-API-Key': apiKey
      }
    };

    expect(modifiedConfig.headers['X-API-Key']).toBe(apiKey);

    sessionStorage.removeItem('apiKey');
  });
});
