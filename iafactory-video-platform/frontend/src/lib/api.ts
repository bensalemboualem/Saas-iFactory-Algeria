/**
 * API Client for IAFactory Video Platform
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        return { error: error.detail || `HTTP ${response.status}` };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Network error' };
    }
  }

  // Projects
  async createProject(data: CreateProjectRequest) {
    return this.request<Project>('/api/v1/projects/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getProjects(params?: { status?: string; limit?: number; offset?: number }) {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Project[]>(`/api/v1/projects?${query}`);
  }

  async getProject(id: string) {
    return this.request<Project>(`/api/v1/projects/${id}`);
  }

  async startPipeline(id: string, options?: { auto_publish?: boolean }) {
    return this.request<PipelineStatus>(`/api/v1/projects/${id}/start`, {
      method: 'POST',
      body: JSON.stringify(options || {}),
    });
  }

  async getProjectStatus(id: string) {
    return this.request<ProjectStatus>(`/api/v1/projects/${id}/status`);
  }

  // Scripts
  async generateScript(data: GenerateScriptRequest) {
    return this.request<Script>('/api/v1/scripts/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getScript(id: string) {
    return this.request<Script>(`/api/v1/scripts/${id}`);
  }

  // Assets
  async generateImages(data: GenerateImagesRequest) {
    return this.request<Asset[]>('/api/v1/assets/images/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateVoice(data: GenerateVoiceRequest) {
    return this.request<Asset>('/api/v1/assets/voice/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateMusic(data: GenerateMusicRequest) {
    return this.request<Asset>('/api/v1/assets/music/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async listVoices(provider: string = 'elevenlabs') {
    return this.request<{ voices: Voice[] }>(`/api/v1/assets/voice/list?provider=${provider}`);
  }

  // Videos
  async renderVideo(data: RenderVideoRequest) {
    return this.request<Video>('/api/v1/videos/render', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getVideoStatus(id: string) {
    return this.request<VideoStatus>(`/api/v1/videos/${id}/status`);
  }

  async createVariants(id: string, formats: string[]) {
    return this.request<{ variants: VideoVariant[] }>(`/api/v1/videos/${id}/variants`, {
      method: 'POST',
      body: JSON.stringify({ formats }),
    });
  }

  // Publishing
  async publish(data: PublishRequest) {
    return this.request<PublishResult>('/api/v1/publish', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async batchPublish(data: BatchPublishRequest) {
    return this.request<BatchPublishResult>('/api/v1/publish/batch', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async schedulePublish(data: SchedulePublishRequest) {
    return this.request<PublishResult>('/api/v1/publish/schedule', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getConnectedAccounts() {
    return this.request<{ accounts: ConnectedAccount[] }>('/api/v1/publish/accounts');
  }

  // Agents
  async executeAgentTask(data: AgentTaskRequest) {
    return this.request<AgentTaskResult>('/api/v1/agents/execute', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async listAgents() {
    return this.request<{ agents: AgentInfo[] }>('/api/v1/agents');
  }

  async getProviders(type: 'image' | 'video' | 'avatar' | 'voice') {
    return this.request<ProviderList>(`/api/v1/agents/${type}/providers`);
  }

  // Health
  async healthCheck() {
    return this.request<{ status: string }>('/health');
  }
}

// Types
interface CreateProjectRequest {
  title: string;
  user_prompt: string;
  target_duration?: string;
  aspect_ratio?: string;
  style?: string;
  language?: string;
  target_platforms?: string[];
}

interface Project {
  id: string;
  title: string;
  description?: string;
  user_prompt: string;
  target_duration: string;
  aspect_ratio: string;
  style?: string;
  language: string;
  target_platforms: string[];
  platforms?: string[];
  status: string;
  progress: Record<string, number>;
  script_id?: string;
  thumbnail_url?: string;
  video_url?: string;
  duration?: number;
  published_urls?: Record<string, string>;
  created_at: string;
  updated_at?: string;
}

interface ProjectStatus {
  project_id: string;
  status: string;
  current_phase: string;
  progress: {
    overall: number;
    phases: Record<string, { status: string; progress: number }>;
  };
}

interface PipelineStatus {
  project_id: string;
  status: string;
  message: string;
}

interface GenerateScriptRequest {
  topic: string;
  duration?: number;
  style?: string;
  tone?: string;
  key_messages?: string[];
  language?: string;
}

interface Script {
  id: string;
  project_id: string;
  title: string;
  content?: string;
  synopsis?: string;
  scenes: Scene[];
  total_duration: number;
  version: number;
  is_approved: boolean;
}

interface Scene {
  scene_id: string;
  order: number;
  duration: number;
  type: string;
  narration: string;
  visual_prompt: string;
  music_mood: string;
  text_overlay?: string;
}

interface GenerateImagesRequest {
  prompt: string;
  provider?: string;
  size?: string;
  style?: string;
  num_images?: number;
}

interface GenerateVoiceRequest {
  text: string;
  provider?: string;
  voice_id?: string;
  language?: string;
  speed?: number;
}

interface GenerateMusicRequest {
  prompt: string;
  provider?: string;
  duration?: number;
  genre?: string;
  mood?: string;
  instrumental?: boolean;
}

interface Asset {
  id: string;
  type: string;
  provider: string;
  url?: string;
  local_path?: string;
  metadata: Record<string, unknown>;
}

interface Voice {
  id: string;
  name: string;
  gender: string;
  accent?: string;
}

interface RenderVideoRequest {
  project_id?: string;
  timeline_id?: string;
  format?: string;
  quality?: string;
}

interface Video {
  id: string;
  project_id: string;
  filename: string;
  duration: number;
  format: string;
  resolution: string;
  status: string;
  url?: string;
}

interface VideoStatus {
  video_id: string;
  status: string;
  progress: number;
  current_step?: string;
}

interface VideoVariant {
  format: string;
  specs: Record<string, unknown>;
  output_path: string;
  status: string;
}

interface PublishRequest {
  video_id: string;
  platform: string;
  title: string;
  description?: string;
  tags?: string[];
  privacy?: string;
}

interface BatchPublishRequest {
  video_id: string;
  platforms: string[];
  auto_optimize?: boolean;
  base_title: string;
  base_description?: string;
  base_tags?: string[];
}

interface SchedulePublishRequest extends PublishRequest {
  scheduled_time: string;
}

interface PublishResult {
  id: string;
  video_id: string;
  platform: string;
  status: string;
  platform_url?: string;
}

interface BatchPublishResult {
  batch_results: PublishResult[];
  total_platforms: number;
  successful: number;
  failed: number;
}

interface ConnectedAccount {
  platform: string;
  account_name: string;
  connected: boolean;
  expires_at?: string;
}

interface AgentTaskRequest {
  agent_type: string;
  task_type: string;
  input_data: Record<string, unknown>;
  priority?: number;
}

interface AgentTaskResult {
  task_id: string;
  agent_type: string;
  success: boolean;
  output_data: Record<string, unknown>;
  error_message?: string;
  execution_time_ms: number;
  cost_cents: number;
}

interface AgentInfo {
  type: string;
  capabilities: string[];
  status: string;
}

interface ProviderList {
  providers: string[];
  costs: Record<string, number>;
  default: string;
}

// Create singleton instance
const apiClient = new ApiClient(API_BASE_URL);

// Namespaced API for easier use
export const api = {
  // Projects namespace
  projects: {
    list: (params?: { status?: string; limit?: number; offset?: number }) =>
      apiClient.getProjects(params).then(r => r.data || []),
    get: (id: string) => apiClient.getProject(id).then(r => r.data!),
    create: (data: CreateProjectRequest) => apiClient.createProject(data).then(r => r.data!),
    startPipeline: (id: string, options?: { auto_publish?: boolean }) =>
      apiClient.startPipeline(id, options).then(r => r.data!),
    getStatus: (id: string) => apiClient.getProjectStatus(id).then(r => r.data!),
  },

  // Scripts namespace
  scripts: {
    get: (id: string) => apiClient.getScript(id).then(r => r.data!),
    generate: (data: GenerateScriptRequest) => apiClient.generateScript(data).then(r => r.data!),
    regenerate: (projectId: string) => apiClient.generateScript({ topic: projectId }).then(r => r.data!),
  },

  // Assets namespace
  assets: {
    generateImages: (data: GenerateImagesRequest) => apiClient.generateImages(data).then(r => r.data!),
    generateVoice: (data: GenerateVoiceRequest) => apiClient.generateVoice(data).then(r => r.data!),
    generateMusic: (data: GenerateMusicRequest) => apiClient.generateMusic(data).then(r => r.data!),
    listVoices: (provider?: string) => apiClient.listVoices(provider).then(r => r.data?.voices || []),
  },

  // Videos namespace
  videos: {
    render: (data: RenderVideoRequest) => apiClient.renderVideo(data).then(r => r.data!),
    getStatus: (id: string) => apiClient.getVideoStatus(id).then(r => r.data!),
    createVariants: (id: string, formats: string[]) =>
      apiClient.createVariants(id, formats).then(r => r.data?.variants || []),
  },

  // Publish namespace
  publish: {
    publish: (projectId: string, platforms: string[]) =>
      apiClient.batchPublish({
        video_id: projectId,
        platforms,
        base_title: '',
        auto_optimize: true
      }).then(r => r.data!),
    schedule: (data: SchedulePublishRequest) => apiClient.schedulePublish(data).then(r => r.data!),
    getAccounts: () => apiClient.getConnectedAccounts().then(r => r.data?.accounts || []),
  },

  // Agents namespace
  agents: {
    execute: (data: AgentTaskRequest) => apiClient.executeAgentTask(data).then(r => r.data!),
    list: () => apiClient.listAgents().then(r => r.data?.agents || []),
    getProviders: (type: 'image' | 'video' | 'avatar' | 'voice') =>
      apiClient.getProviders(type).then(r => r.data!),
  },

  // Health
  health: () => apiClient.healthCheck().then(r => r.data!),
};

// Export types
export type {
  Project,
  ProjectStatus,
  Script,
  Scene,
  Asset,
  Voice,
  Video,
  VideoStatus,
  PublishResult,
  ConnectedAccount,
  AgentInfo,
};
