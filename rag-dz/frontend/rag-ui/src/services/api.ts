import axios from 'axios'
import { API_CONFIG } from '../config/api'

const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_CONFIG.API_KEY
  }
})

export const ragApi = {
  health: () => apiClient.get(API_CONFIG.ENDPOINTS.HEALTH),
  
  testEmbed: () => apiClient.post(API_CONFIG.ENDPOINTS.TEST_EMBED),
  
  query: (data: { query: string, project_id?: string }) => 
    apiClient.post(API_CONFIG.ENDPOINTS.QUERY, {
      project_id: data.project_id || 'default',
      query: data.query,
      search: { k: 10, rerank_top_k: 5 }
    })
}

export default apiClient
