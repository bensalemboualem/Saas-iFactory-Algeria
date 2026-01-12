import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============================================
// VIDEO GENERATION
// ============================================

export interface GenerateVideoRequest {
  prompt: string;
  mode: "text-to-video" | "image-to-video";
  imageUrl?: string;
  duration: number;
  aspectRatio: "16:9" | "9:16" | "1:1";
  model?: string;
}

export interface GenerateVideoResponse {
  taskId: string;
  estimatedTime: number;
  credits: number;
}

export interface VideoStatus {
  taskId: string;
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  videoUrl?: string;
  error?: string;
}

export const videoApi = {
  generate: (data: GenerateVideoRequest) =>
    api.post<GenerateVideoResponse>("/api/v1/video/generate", data),

  getStatus: (taskId: string) =>
    api.get<VideoStatus>(`/api/v1/video/status/${taskId}`),

  list: () =>
    api.get("/api/v1/video/projects"),
};

// ============================================
// AUDIO / TTS
// ============================================

export interface Voice {
  id: string;
  name: string;
  language: string;
  gender: string;
  preview_url?: string;
  is_premium: boolean;
}

export interface TTSRequest {
  text: string;
  voice_id: string;
  language?: string;
  speed?: number;
  format?: "mp3" | "wav";
}

export interface TTSResponse {
  audio_url: string;
  duration: number;
  credits_used: number;
}

export interface DarijaTTSRequest {
  text: string;
  voice_id?: string;
  speed?: number;
}

export const audioApi = {
  // List all voices
  listVoices: (language?: string) =>
    api.get<Voice[]>("/api/v1/audio/voices", { params: { language } }),

  // List Darija voices only
  listDarijaVoices: () =>
    api.get<Voice[]>("/api/v1/audio/voices/darija"),

  // Generate TTS (unified)
  generateTTS: (data: TTSRequest) =>
    api.post<TTSResponse>("/api/v1/audio/tts", data),

  // Generate Darija TTS
  generateDarijaTTS: (data: DarijaTTSRequest) =>
    api.post<TTSResponse>("/api/v1/audio/tts/darija", data),

  // Generate multi-segment TTS
  generateMultiTTS: (segments: Array<{ text: string; language: string }>, voice_per_language?: Record<string, string>) =>
    api.post("/api/v1/audio/tts/multilingual", { segments, voice_per_language }),

  // Get supported languages
  getLanguages: () =>
    api.get("/api/v1/audio/languages"),

  // Get TTS pricing
  getPricing: () =>
    api.get("/api/v1/audio/pricing"),
};

// ============================================
// TEMPLATES
// ============================================

export interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  thumbnail_url: string;
  duration: number;
  credits: number;
  parameters: Record<string, unknown>;
}

export interface TemplateCategory {
  id: string;
  name: string;
  icon: string;
  count: number;
}

export const templateApi = {
  // List templates with filtering
  list: (params?: { category?: string; locale?: string; premium_only?: boolean; sort_by?: string }) =>
    api.get<Template[]>("/api/v1/templates", { params }),

  // Get single template
  get: (id: string, locale?: string) =>
    api.get<Template>(`/api/v1/templates/${id}`, { params: { locale } }),

  // Get full template with all locales
  getFull: (id: string) =>
    api.get(`/api/v1/templates/${id}/full`),

  // Get categories
  getCategories: (locale?: string) =>
    api.get<TemplateCategory[]>("/api/v1/templates/categories", { params: { locale } }),

  // Get popular templates
  getPopular: (limit?: number, locale?: string) =>
    api.get<Template[]>("/api/v1/templates/popular", { params: { limit, locale } }),

  // Get featured templates
  getFeatured: (locale?: string) =>
    api.get<Template[]>("/api/v1/templates/featured", { params: { locale } }),

  // Get seasonal templates
  getSeasonal: (locale?: string) =>
    api.get<Template[]>("/api/v1/templates/seasonal", { params: { locale } }),
};

// ============================================
// CREDITS
// ============================================

export interface CreditBalance {
  balance: number;
  last_updated: string;
}

export interface CreditTransaction {
  id: string;
  type: string;
  amount: number;
  description: string;
  created_at: string;
}

export interface CreditPack {
  id: string;
  name: string;
  credits: number;
  price: number;
  price_eur: number;
  is_popular?: boolean;
}

export interface CostEstimate {
  service: string;
  quantity: number;
  cost: number;
  currency: string;
}

export interface PipelineCostEstimate {
  duration: number;
  total_credits: number;
  breakdown: Record<string, number>;
}

export const creditsApi = {
  // Get balance
  getBalance: () =>
    api.get<CreditBalance>("/api/v1/credits/balance"),

  // Get full status
  getStatus: () =>
    api.get("/api/v1/credits/status"),

  // Check if enough credits
  checkCredits: (amount: number) =>
    api.get("/api/v1/credits/check", { params: { amount } }),

  // Get transaction history
  getHistory: (params?: { type?: string; limit?: number; offset?: number }) =>
    api.get<CreditTransaction[]>("/api/v1/credits/history", { params }),

  // Estimate cost
  estimateCost: (service: string, quantity?: number, options?: Record<string, unknown>) =>
    api.post<CostEstimate>("/api/v1/credits/estimate", { service, quantity, options }),

  // Estimate pipeline cost
  estimatePipelineCost: (duration: number, include_voice?: boolean, include_music?: boolean, model?: string) =>
    api.post<PipelineCostEstimate>("/api/v1/credits/estimate/pipeline", { duration, include_voice, include_music, model }),

  // Get pricing grid
  getPricing: () =>
    api.get("/api/v1/credits/pricing"),

  // Get available packs
  getPacks: (locale?: string) =>
    api.get<CreditPack[]>("/api/v1/credits/packs", { params: { locale } }),

  // Purchase credits
  purchase: (packId: string) =>
    api.post("/api/v1/credits/purchase", { pack_id: packId }),

  // Create Stripe checkout session
  createCheckout: (packId: string) =>
    api.post("/api/v1/credits/create-checkout-session", { pack_id: packId }),

  // Reserve credits (for pipeline)
  reserveCredits: (amount: number, description: string) =>
    api.post("/api/v1/credits/reserve", { amount, description }),

  // Confirm reservation
  confirmReservation: (reservationId: string) =>
    api.post(`/api/v1/credits/reserve/${reservationId}/confirm`),

  // Cancel reservation
  cancelReservation: (reservationId: string) =>
    api.post(`/api/v1/credits/reserve/${reservationId}/cancel`),

  // Get Stripe key
  getStripeKey: () =>
    api.get("/api/v1/credits/stripe-key"),
};

// ============================================
// AGENTS (Multi-Agent System)
// ============================================

export interface TrendReport {
  platform: string;
  trends: Array<{
    topic: string;
    hashtags: string[];
    engagement_level: string;
    content_suggestions: string[];
  }>;
  analysis_date: string;
}

export interface ContentIdea {
  title: string;
  description: string;
  hook: string;
  target_audience: string;
  estimated_engagement: string;
  hashtags: string[];
  content_pillars: string[];
}

export interface CoordinationResult {
  script: {
    title: string;
    sections: Array<{
      type: string;
      content: string;
      duration: number;
      visual_notes: string;
    }>;
    total_duration: number;
  };
  quality_report: {
    overall_score: number;
    issues: Array<{ type: string; message: string; severity: string }>;
    recommendations: string[];
  };
  metadata: {
    trend_used?: string;
    idea_used?: string;
    processing_time: number;
  };
}

export interface QualityReport {
  overall_score: number;
  passed: boolean;
  criteria_scores: Record<string, number>;
  issues: Array<{ type: string; message: string; severity: string; suggestion: string }>;
  recommendations: string[];
}

export const agentsApi = {
  // Trend Analyzer
  analyzeTrends: (params: { platforms?: string[]; niche?: string; region?: string }) =>
    api.post<TrendReport>("/api/v1/agents/trends/analyze", params),

  getQuickTrends: (niche?: string) =>
    api.get("/api/v1/agents/trends/quick", { params: { niche } }),

  // Idea Researcher
  generateIdeas: (params: { niche: string; target_audience: string; content_type: string; count?: number }) =>
    api.post<{ ideas: ContentIdea[] }>("/api/v1/agents/ideas/generate", params),

  getIdeasForTrend: (trend: string, niche?: string) =>
    api.get("/api/v1/agents/ideas/for-trend", { params: { trend, niche } }),

  // Script Coordinator (Full workflow)
  coordinateWorkflow: (params: {
    topic: string;
    niche?: string;
    target_audience?: string;
    style?: string;
    language?: string;
    duration?: number;
    analyze_trends?: boolean;
    generate_ideas?: boolean;
    quality_check?: boolean;
  }) =>
    api.post<CoordinationResult>("/api/v1/agents/coordinate", params),

  generateQuickScript: (params: { topic: string; style?: string; duration?: number; language?: string }) =>
    api.post("/api/v1/agents/coordinate/quick-script", params),

  // Quality Controller
  checkQuality: (params: { script: string; content_type?: string; target_platform?: string; language?: string }) =>
    api.post<QualityReport>("/api/v1/agents/quality/check", params),

  checkCulturalSensitivity: (content: string) =>
    api.post("/api/v1/agents/quality/cultural-check", { content }),

  // Agents status
  getAgentsStatus: () =>
    api.get("/api/v1/agents/status"),
};

// ============================================
// PIPELINE (Full Video Production)
// ============================================

export interface PipelineRequest {
  prompt: string;
  duration: number;
  model?: string;
  include_voice?: boolean;
  voice_language?: string;
  voice_id?: string;
  include_music?: boolean;
  music_preset?: string;
  include_subtitles?: boolean;
  aspect_ratio?: "16:9" | "9:16" | "1:1";
  use_agents?: boolean;
  style?: string;
}

export interface PipelineStatus {
  pipeline_id: string;
  status: "pending" | "scripting" | "generating" | "audio" | "montage" | "completed" | "error";
  current_step: number;
  total_steps: number;
  progress: number;
  segments: Array<{
    id: number;
    prompt: string;
    status: string;
    progress: number;
    video_url?: string;
  }>;
  script?: string;
  audio_url?: string;
  final_video_url?: string;
  error?: string;
  credits_used?: number;
  estimated_time_remaining?: number;
}

export const pipelineApi = {
  // Start full pipeline with agents
  start: (data: PipelineRequest) =>
    api.post<{ pipeline_id: string; estimated_time: number; credits_reserved: number }>("/api/v1/pipeline/start", data),

  // Start with coordination (uses all agents)
  startWithCoordination: (data: { topic: string; duration: number; niche?: string; target_audience?: string; language?: string }) =>
    api.post("/api/v1/pipeline/start-coordinated", data),

  // Get pipeline status
  getStatus: (pipelineId: string) =>
    api.get<PipelineStatus>(`/api/v1/pipeline/status/${pipelineId}`),

  // Cancel pipeline
  cancel: (pipelineId: string) =>
    api.post(`/api/v1/pipeline/cancel/${pipelineId}`),

  // Retry failed segment
  retrySegment: (pipelineId: string, segmentId: number) =>
    api.post(`/api/v1/pipeline/${pipelineId}/retry-segment/${segmentId}`),

  // List user pipelines
  list: (status?: string) =>
    api.get("/api/v1/pipeline/list", { params: { status } }),

  // Get pipeline result
  getResult: (pipelineId: string) =>
    api.get(`/api/v1/pipeline/result/${pipelineId}`),
};

// ============================================
// SCRIPTS
// ============================================

export interface Script {
  id: string;
  title: string;
  content: string;
  style: string;
  language: string;
  duration: number;
  created_at: string;
}

export const scriptsApi = {
  // Generate script with Claude
  generate: (params: { topic: string; style?: string; duration?: number; language?: string }) =>
    api.post<Script>("/api/v1/scripts/generate", params),

  // List user scripts
  list: () =>
    api.get<Script[]>("/api/v1/scripts"),

  // Get script
  get: (id: string) =>
    api.get<Script>(`/api/v1/scripts/${id}`),

  // Update script
  update: (id: string, content: string) =>
    api.put(`/api/v1/scripts/${id}`, { content }),

  // Delete script
  delete: (id: string) =>
    api.delete(`/api/v1/scripts/${id}`),
};

// ============================================
// STORYBOARD
// ============================================

export interface StoryboardScene {
  id: number;
  prompt: string;
  duration: number;
  visual_notes: string;
  audio_notes?: string;
  image_url?: string;
}

export interface Storyboard {
  id: string;
  title: string;
  scenes: StoryboardScene[];
  total_duration: number;
  created_at: string;
}

export const storyboardApi = {
  // Generate storyboard from script
  generateFromScript: (scriptId: string) =>
    api.post<Storyboard>("/api/v1/storyboard/generate", { script_id: scriptId }),

  // Generate storyboard from text
  generateFromText: (text: string, scenes_count?: number) =>
    api.post<Storyboard>("/api/v1/storyboard/generate-from-text", { text, scenes_count }),

  // List storyboards
  list: () =>
    api.get<Storyboard[]>("/api/v1/storyboard"),

  // Get storyboard
  get: (id: string) =>
    api.get<Storyboard>(`/api/v1/storyboard/${id}`),

  // Update scene
  updateScene: (storyboardId: string, sceneId: number, data: Partial<StoryboardScene>) =>
    api.put(`/api/v1/storyboard/${storyboardId}/scenes/${sceneId}`, data),
};

