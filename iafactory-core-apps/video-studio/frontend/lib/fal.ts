import { fal } from "@fal-ai/client";

// Configure Fal client (proxy through our backend for security)
fal.config({
  proxyUrl: "/api/fal/proxy",
});

export const MODELS = {
  "kling-1.6": "fal-ai/kling-video/v1.6/standard/text-to-video",
  "kling-i2v": "fal-ai/kling-video/v1.6/standard/image-to-video",
  "minimax": "fal-ai/minimax-video/video-01/text-to-video",
  "luma": "fal-ai/luma-dream-machine",
} as const;

export type ModelId = keyof typeof MODELS;

export interface TextToVideoInput {
  prompt: string;
  duration?: "5" | "10";
  aspect_ratio?: "16:9" | "9:16" | "1:1";
}

export interface ImageToVideoInput {
  prompt?: string;
  image_url: string;
  duration?: "5" | "10";
  aspect_ratio?: "16:9" | "9:16" | "1:1";
}

export interface VideoOutput {
  video: {
    url: string;
    content_type: string;
    file_name: string;
    file_size: number;
  };
}

export async function generateTextToVideo(
  input: TextToVideoInput,
  model: ModelId = "kling-1.6",
  onProgress?: (progress: number) => void
): Promise<VideoOutput> {
  const result = await fal.subscribe(MODELS[model], {
    input: {
      prompt: input.prompt,
      duration: input.duration || "5",
      aspect_ratio: input.aspect_ratio || "16:9",
    },
    logs: true,
    onQueueUpdate: (update) => {
      if (update.status === "IN_PROGRESS" && onProgress) {
        // Estimate progress based on logs
        const logs = update.logs || [];
        const progress = Math.min(logs.length * 10, 90);
        onProgress(progress);
      }
    },
  });

  return result.data as VideoOutput;
}

export async function generateImageToVideo(
  input: ImageToVideoInput,
  onProgress?: (progress: number) => void
): Promise<VideoOutput> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const result = await fal.subscribe(MODELS["kling-i2v"] as any, {
    input: {
      prompt: input.prompt || "",
      image_url: input.image_url,
      duration: input.duration || "5",
    },
    logs: true,
    onQueueUpdate: (update) => {
      if (update.status === "IN_PROGRESS" && onProgress) {
        const logs = update.logs || [];
        const progress = Math.min(logs.length * 10, 90);
        onProgress(progress);
      }
    },
  });

  return result.data as VideoOutput;
}

// Upload image and get URL
export async function uploadImage(file: File): Promise<string> {
  const url = await fal.storage.upload(file);
  return url;
}
