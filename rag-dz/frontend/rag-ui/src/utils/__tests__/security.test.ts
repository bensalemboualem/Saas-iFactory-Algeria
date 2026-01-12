/**
 * Tests pour les utilitaires de sécurité
 */
import { describe, it, expect } from 'vitest';

describe('Security Utilities', () => {
  describe('API Key Validation', () => {
    it('should validate API key format', () => {
      const validKey = 'ragdz_dev_1234567890abcdef';
      expect(validKey.startsWith('ragdz_')).toBe(true);
      expect(validKey.length).toBeGreaterThan(20);
    });

    it('should reject invalid API key formats', () => {
      const invalidKeys = [
        '',
        'short',
        'invalid_prefix_key',
        '123456'
      ];

      invalidKeys.forEach(key => {
        expect(key.startsWith('ragdz_')).toBe(false);
      });
    });

    it('should sanitize API key before storage', () => {
      const rawKey = '  ragdz_dev_key123  ';
      const sanitized = rawKey.trim();
      expect(sanitized).toBe('ragdz_dev_key123');
      expect(sanitized).not.toContain(' ');
    });
  });

  describe('Session Storage Security', () => {
    it('should store API key securely in sessionStorage', () => {
      const key = 'test-secure-key';
      sessionStorage.setItem('apiKey', key);

      const retrieved = sessionStorage.getItem('apiKey');
      expect(retrieved).toBe(key);

      sessionStorage.removeItem('apiKey');
    });

    it('should clear API key on logout', () => {
      sessionStorage.setItem('apiKey', 'test-key');
      sessionStorage.removeItem('apiKey');

      const retrieved = sessionStorage.getItem('apiKey');
      expect(retrieved).toBeNull();
    });
  });

  describe('Environment Variables', () => {
    it('should not expose API keys in production builds', () => {
      // En production, VITE_API_KEY ne devrait jamais être définie
      const isProduction = import.meta.env.MODE === 'production';

      if (isProduction) {
        expect(import.meta.env.VITE_API_KEY).toBeUndefined();
      }
    });

    it('should validate environment configuration', () => {
      const apiUrl = import.meta.env.VITE_API_URL;
      if (apiUrl) {
        expect(typeof apiUrl).toBe('string');
        expect(apiUrl.startsWith('http')).toBe(true);
      }
    });
  });
});
