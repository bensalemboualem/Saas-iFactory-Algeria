// Replicate API client for open-source model inference
import Replicate from 'replicate';

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN || '',
});

export interface ReplicateVideoParams {
  prompt: string;
  model: string;
  negative_prompt?: string;
  num_frames?: number;
  fps?: number;
  guidance_scale?: number;
  num_inference_steps?: number;
  seed?: number;
}

export interface ReplicateImageParams {
  prompt: string;
  model: string;
  negative_prompt?: string;
  width?: number;
  height?: number;
  num_outputs?: number;
  guidance_scale?: number;
  num_inference_steps?: number;
  seed?: number;
}

// Model-specific configurations
const MODEL_CONFIGS: Record<string, any> = {
  // Video Models
  'alibaba-pai/wan-2.1-t2v-1.3b': {
    defaultParams: {
      num_frames: 81,
      fps: 16,
      guidance_scale: 5.0,
      num_inference_steps: 50,
    },
  },
  'fofr/cogvideox-5b': {
    defaultParams: {
      num_frames: 49,
      fps: 8,
      guidance_scale: 6.0,
      num_inference_steps: 50,
    },
  },
  'tencent/hunyuan-video': {
    defaultParams: {
      num_frames: 129,
      fps: 24,
      guidance_scale: 6.0,
      num_inference_steps: 50,
    },
  },
  'lightricks/ltx-video': {
    defaultParams: {
      num_frames: 121,
      fps: 25,
      guidance_scale: 3.0,
      num_inference_steps: 40,
    },
  },
  'genmoai/mochi-1-preview': {
    defaultParams: {
      num_frames: 84,
      fps: 24,
    },
  },
  
  // Image Models
  'black-forest-labs/flux-schnell': {
    defaultParams: {
      num_outputs: 1,
      aspect_ratio: '1:1',
      output_format: 'webp',
      output_quality: 90,
    },
  },
  'black-forest-labs/flux-dev': {
    defaultParams: {
      num_outputs: 1,
      guidance: 3.5,
      num_inference_steps: 28,
      output_format: 'webp',
    },
  },
  'stability-ai/sdxl': {
    defaultParams: {
      width: 1024,
      height: 1024,
      num_outputs: 1,
      scheduler: 'K_EULER',
      num_inference_steps: 25,
      guidance_scale: 7.5,
    },
  },
};

/**
 * Generate video using Replicate API
 */
export async function generateVideoReplicate(params: ReplicateVideoParams): Promise<string> {
  const { prompt, model, negative_prompt, ...overrides } = params;
  
  const config = MODEL_CONFIGS[model] || { defaultParams: {} };
  const input = {
    prompt,
    negative_prompt: negative_prompt || 'blurry, low quality, distorted, ugly',
    ...config.defaultParams,
    ...overrides,
  };

  console.log(`[Replicate] Generating video with ${model}`, input);

  const output = await replicate.run(model as `${string}/${string}`, { input });
  
  // Handle different output formats
  if (Array.isArray(output)) {
    return output[0] as string;
  }
  if (typeof output === 'string') {
    return output;
  }
  if (output && typeof output === 'object' && 'video' in output) {
    return (output as any).video;
  }
  
  throw new Error('Unexpected output format from Replicate');
}

/**
 * Generate image using Replicate API
 */
export async function generateImageReplicate(params: ReplicateImageParams): Promise<string[]> {
  const { prompt, model, negative_prompt, ...overrides } = params;
  
  const config = MODEL_CONFIGS[model] || { defaultParams: {} };
  const input = {
    prompt,
    negative_prompt: negative_prompt || 'blurry, low quality, distorted',
    ...config.defaultParams,
    ...overrides,
  };

  console.log(`[Replicate] Generating image with ${model}`, input);

  const output = await replicate.run(model as `${string}/${string}`, { input });
  
  if (Array.isArray(output)) {
    return output as string[];
  }
  if (typeof output === 'string') {
    return [output];
  }
  
  throw new Error('Unexpected output format from Replicate');
}

/**
 * Generate image-to-video using Replicate
 */
export async function generateImageToVideoReplicate(params: {
  image_url: string;
  model: string;
  motion_bucket_id?: number;
  fps?: number;
  num_frames?: number;
}): Promise<string> {
  const { image_url, model, ...overrides } = params;
  
  const input = {
    image: image_url,
    motion_bucket_id: overrides.motion_bucket_id || 127,
    fps: overrides.fps || 6,
    num_frames: overrides.num_frames || 25,
  };

  console.log(`[Replicate] Generating I2V with ${model}`, input);

  const output = await replicate.run(model as `${string}/${string}`, { input });
  
  if (Array.isArray(output)) {
    return output[0] as string;
  }
  if (typeof output === 'string') {
    return output;
  }
  
  throw new Error('Unexpected output format from Replicate');
}

/**
 * Check prediction status
 */
export async function getPredictionStatus(id: string) {
  return replicate.predictions.get(id);
}

/**
 * Cancel a prediction
 */
export async function cancelPrediction(id: string) {
  return replicate.predictions.cancel(id);
}

export { replicate };
