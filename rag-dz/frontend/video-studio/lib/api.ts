/**
 * API Client for Dzir IA Video Backend
 * Connects to FastAPI backend at https://www.iafactoryalgeria.com/dzirvideo
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://www.iafactoryalgeria.com/dzirvideo"

export interface GeneratorInfo {
  name: string
  class_name: string
  tier: "free" | "standard" | "premium"
  quality_score: number
  avg_generation_time: number
  max_duration: number
  max_resolution: string
  cost_per_second: number
  free_tier: boolean
  daily_quota?: number
  supports_negative_prompts: boolean
  supports_aspect_ratios: boolean
  supports_style_presets: boolean
}

export interface VideoGenerationRequest {
  generator_name: string
  prompt: string
  negative_prompt?: string
  duration_seconds?: number
  aspect_ratio?: string
  style?: string
  seed?: number
}

export interface VideoGenerationStatus {
  task_id: string
  status: "processing" | "completed" | "failed"
  progress?: number
  output_url?: string
  thumbnail_url?: string
  error_message?: string
  estimated_completion_time?: number
  metadata?: Record<string, any>
}

/**
 * API Client class
 */
class DzirvdeoAPI {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  /**
   * Fetch wrapper with error handling
   */
  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
      })

      if (!response.ok) {
        const error = await response.text()
        throw new Error(`API Error ${response.status}: ${error}`)
      }

      return response.json() as Promise<T>
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      throw error
    }
  }

  /**
   * Health check
   */
  async health(): Promise<{ status: string; version: string; generators_count: number }> {
    return this.fetch("/health")
  }

  /**
   * List all available generators
   */
  async listGenerators(): Promise<GeneratorInfo[]> {
    return this.fetch("/generators")
  }

  /**
   * Get generator details by name
   */
  async getGenerator(name: string): Promise<GeneratorInfo> {
    return this.fetch(`/generators/${encodeURIComponent(name)}`)
  }

  /**
   * Generate a video
   */
  async generateVideo(request: VideoGenerationRequest): Promise<VideoGenerationStatus> {
    return this.fetch("/generate", {
      method: "POST",
      body: JSON.stringify(request),
    })
  }

  /**
   * Check video generation status
   */
  async checkStatus(taskId: string): Promise<VideoGenerationStatus> {
    return this.fetch(`/status/${taskId}`)
  }

  /**
   * Cancel a video generation task
   */
  async cancelGeneration(taskId: string): Promise<{ success: boolean }> {
    return this.fetch(`/cancel/${taskId}`, {
      method: "POST",
    })
  }

  /**
   * Get quota information (if implemented)
   */
  async getQuota(): Promise<{
    total_free_videos_today: number
    used_videos_today: number
    remaining_videos_today: number
    generators_quota: Record<string, { used: number; total: number }>
  }> {
    return this.fetch("/quota")
  }
}

// Export singleton instance
export const api = new DzirvdeoAPI()

// Export for use in components
export default api
