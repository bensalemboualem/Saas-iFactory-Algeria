// Configuration pour RAG.dz
export const API_BASE_URL = 'http://localhost:8180'
export const API_KEY = 'test-api-key-ragdz-2024'

export const getApiUrl = () => API_BASE_URL

export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  API_KEY: API_KEY,
  TIMEOUT: 30000,
  ENDPOINTS: {
    HEALTH: '/health',
    QUERY: '/api/query', 
    INGEST: '/api/ingest',
    TEST_EMBED: '/api/test/embed'
  }
}

// Compatibilité avec l'UI Archon existante
export default {
  baseURL: API_BASE_URL,
  apiKey: API_KEY,
  getApiUrl
}
