// Multi-provider configuration for AI video/image generation
// Supports: Fal.ai, Replicate, and Open-Source models

export type ProviderType = 'fal' | 'replicate' | 'opensource';
export type ModelTier = 'free' | 'standard' | 'premium';

export interface AIModel {
  id: string;
  name: string;
  provider: ProviderType;
  type: 'text-to-video' | 'image-to-video' | 'text-to-image';
  tier: ModelTier;
  vram: string;
  maxDuration: number; // seconds
  resolution: string;
  description: string;
  replicateId?: string; // For Replicate hosted models
  huggingfaceId?: string; // For direct HF inference
  icon: string;
  isAvailable: boolean;
}

// ============================================
// 🎬 VIDEO GENERATION MODELS
// ============================================

export const VIDEO_MODELS: AIModel[] = [
  // ===== FAL.AI MODELS =====
  {
    id: 'fal-kling-1.6',
    name: 'Kling 1.6 Pro',
    provider: 'fal',
    type: 'text-to-video',
    tier: 'premium',
    vram: 'Cloud',
    maxDuration: 10,
    resolution: '1080p',
    description: 'Modèle Kling 1.6 de haute qualité via Fal.ai',
    icon: '⚡',
    isAvailable: false, // Disabled - no credits
  },
  {
    id: 'fal-minimax',
    name: 'MiniMax Video',
    provider: 'fal',
    type: 'text-to-video',
    tier: 'standard',
    vram: 'Cloud',
    maxDuration: 6,
    resolution: '720p',
    description: 'Génération rapide avec MiniMax',
    icon: '🚀',
    isAvailable: false,
  },

  // ===== REPLICATE MODELS (Hosted Open-Source) =====
  {
    id: 'replicate-wan2.1',
    name: 'Wan 2.1 (Alibaba)',
    provider: 'replicate',
    type: 'text-to-video',
    tier: 'free',
    vram: '8GB',
    maxDuration: 5,
    resolution: '480p',
    description: 'Meilleur rapport qualité/accessibilité - #1 VBench',
    replicateId: 'alibaba-pai/wan-2.1-t2v-1.3b',
    huggingfaceId: 'Wan-AI/Wan2.1-T2V-1.3B',
    icon: '🥇',
    isAvailable: true,
  },
  {
    id: 'replicate-cogvideo',
    name: 'CogVideoX-5B',
    provider: 'replicate',
    type: 'text-to-video',
    tier: 'standard',
    vram: '12GB',
    maxDuration: 6,
    resolution: '720p',
    description: 'Stable et économique - Très bon support LoRA',
    replicateId: 'fofr/cogvideox-5b',
    huggingfaceId: 'THUDM/CogVideoX-5b',
    icon: '🎯',
    isAvailable: true,
  },
  {
    id: 'replicate-hunyuan',
    name: 'HunyuanVideo 1.5',
    provider: 'replicate',
    type: 'text-to-video',
    tier: 'premium',
    vram: '16GB',
    maxDuration: 5,
    resolution: '720p',
    description: 'Meilleure qualité cinématique - Tencent',
    replicateId: 'tencent/hunyuan-video',
    huggingfaceId: 'tencent/HunyuanVideo',
    icon: '🎬',
    isAvailable: true,
  },
  {
    id: 'replicate-ltx',
    name: 'LTX Video 2',
    provider: 'replicate',
    type: 'text-to-video',
    tier: 'standard',
    vram: '12GB',
    maxDuration: 5,
    resolution: '720p 30fps',
    description: 'Lightricks - Génération rapide',
    replicateId: 'lightricks/ltx-video',
    huggingfaceId: 'Lightricks/LTX-Video',
    icon: '✨',
    isAvailable: true,
  },
  {
    id: 'replicate-mochi',
    name: 'Mochi 1',
    provider: 'replicate',
    type: 'text-to-video',
    tier: 'premium',
    vram: '24GB',
    maxDuration: 5,
    resolution: '848x480',
    description: 'Genmo AI - Mouvements naturels',
    replicateId: 'genmoai/mochi-1-preview',
    icon: '🍡',
    isAvailable: true,
  },

  // ===== IMAGE TO VIDEO =====
  {
    id: 'replicate-svd',
    name: 'Stable Video Diffusion',
    provider: 'replicate',
    type: 'image-to-video',
    tier: 'standard',
    vram: '16GB',
    maxDuration: 4,
    resolution: '576x1024',
    description: 'Animation d\'images - Stability AI',
    replicateId: 'stability-ai/stable-video-diffusion',
    icon: '🖼️',
    isAvailable: true,
  },
  {
    id: 'replicate-i2vgen',
    name: 'I2VGen-XL',
    provider: 'replicate',
    type: 'image-to-video',
    tier: 'free',
    vram: '8GB',
    maxDuration: 4,
    resolution: '512x512',
    description: 'Alibaba DAMO - Image vers vidéo',
    replicateId: 'ali-vilab/i2vgen-xl',
    icon: '🎞️',
    isAvailable: true,
  },
];

// ============================================
// 🖼️ IMAGE GENERATION MODELS
// ============================================

export const IMAGE_MODELS: AIModel[] = [
  {
    id: 'replicate-flux-schnell',
    name: 'FLUX Schnell',
    provider: 'replicate',
    type: 'text-to-image',
    tier: 'free',
    vram: '8GB',
    maxDuration: 0,
    resolution: '1024x1024',
    description: 'Ultra-rapide - Apache 2.0 gratuit',
    replicateId: 'black-forest-labs/flux-schnell',
    huggingfaceId: 'black-forest-labs/FLUX.1-schnell',
    icon: '⚡',
    isAvailable: true,
  },
  {
    id: 'replicate-flux-dev',
    name: 'FLUX Dev',
    provider: 'replicate',
    type: 'text-to-image',
    tier: 'standard',
    vram: '12GB',
    maxDuration: 0,
    resolution: '1024x1024',
    description: 'Haute qualité - Non commercial',
    replicateId: 'black-forest-labs/flux-dev',
    huggingfaceId: 'black-forest-labs/FLUX.1-dev',
    icon: '🎨',
    isAvailable: true,
  },
  {
    id: 'replicate-sdxl',
    name: 'SDXL 1.0',
    provider: 'replicate',
    type: 'text-to-image',
    tier: 'free',
    vram: '8GB',
    maxDuration: 0,
    resolution: '1024x1024',
    description: 'Stability AI - Très polyvalent',
    replicateId: 'stability-ai/sdxl',
    huggingfaceId: 'stabilityai/stable-diffusion-xl-base-1.0',
    icon: '🌟',
    isAvailable: true,
  },
  {
    id: 'replicate-sd3.5',
    name: 'SD 3.5 Large',
    provider: 'replicate',
    type: 'text-to-image',
    tier: 'standard',
    vram: '12GB',
    maxDuration: 0,
    resolution: '1024x1024',
    description: 'Dernière version Stability AI',
    replicateId: 'stability-ai/stable-diffusion-3.5-large',
    icon: '💎',
    isAvailable: true,
  },
];

// ============================================
// 🛠️ HELPER FUNCTIONS
// ============================================

export function getAvailableModels(type: 'text-to-video' | 'image-to-video' | 'text-to-image'): AIModel[] {
  const models = type === 'text-to-image' ? IMAGE_MODELS : VIDEO_MODELS;
  return models.filter(m => m.type === type && m.isAvailable);
}

export function getModelById(id: string): AIModel | undefined {
  return [...VIDEO_MODELS, ...IMAGE_MODELS].find(m => m.id === id);
}

export function getModelsByProvider(provider: ProviderType): AIModel[] {
  return [...VIDEO_MODELS, ...IMAGE_MODELS].filter(m => m.provider === provider && m.isAvailable);
}

export function getModelsByTier(tier: ModelTier): AIModel[] {
  return [...VIDEO_MODELS, ...IMAGE_MODELS].filter(m => m.tier === tier && m.isAvailable);
}

export const DEFAULT_VIDEO_MODEL = 'replicate-wan2.1';
export const DEFAULT_IMAGE_MODEL = 'replicate-flux-schnell';

// Provider status
export const PROVIDER_STATUS = {
  fal: {
    name: 'Fal.ai',
    status: 'disabled' as const,
    reason: 'Crédits épuisés - Recharger sur fal.ai/dashboard/billing',
  },
  replicate: {
    name: 'Replicate',
    status: 'active' as const,
    reason: 'Modèles open-source hébergés',
  },
  opensource: {
    name: 'Self-Hosted',
    status: 'coming' as const,
    reason: 'Bientôt disponible - Nécessite GPU local',
  },
};
