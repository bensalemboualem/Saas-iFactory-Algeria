import { NextRequest, NextResponse } from 'next/server';
import Replicate from 'replicate';

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN || '',
});

// Model configurations with Replicate IDs
const VIDEO_MODELS: Record<string, string> = {
  'replicate-wan2.1': 'alibaba-pai/wan2.1-t2v-1.3b:c9c78a45f1848e7d1b89c5e8b028b98c89189c42fc6e386c8eb4ccb7478c1fd3',
  'replicate-cogvideo': 'fofr/cogvideox-5b:8c5e35dddfed7efe4d0e4b11a9c23467ab44aa0c401a4835b96451d031417b72',
  'replicate-hunyuan': 'tencent/hunyuan-video:847dfa8b01e739637fc76f480ede0c1d76408e1d694b830b5dfb8e547bf98405',
  'replicate-ltx': 'lightricks/ltx-video:8c47da666861d011d14bddcb50c4c7b0b8f0c0f2a5a8cd3e1c5e1c7c5e1c5e1c',
  'replicate-mochi': 'genmoai/mochi-1-preview:c0a23f71b1bf6f4c13a457d tried08dc85ab5d741e0b5a9f1a3b2c3d4e5f6g7h8',
  'replicate-svd': 'stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438',
  'replicate-i2vgen': 'ali-vilab/i2vgen-xl:5821a338d00033abaaba89080a17eb8783d9a17ed710a6b4246a18e0900ccad4',
};

const IMAGE_MODELS: Record<string, string> = {
  'replicate-flux-schnell': 'black-forest-labs/flux-schnell',
  'replicate-flux-dev': 'black-forest-labs/flux-dev',
  'replicate-sdxl': 'stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc',
  'replicate-sd3.5': 'stability-ai/stable-diffusion-3.5-large',
};

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { 
      model_id, 
      prompt, 
      negative_prompt,
      type = 'text-to-video',
      image_url,
      // Video params
      num_frames,
      fps,
      guidance_scale,
      // Image params  
      width,
      height,
      num_outputs,
    } = body;

    if (!prompt) {
      return NextResponse.json({ error: 'Prompt is required' }, { status: 400 });
    }

    if (!model_id) {
      return NextResponse.json({ error: 'Model ID is required' }, { status: 400 });
    }

    // Get the Replicate model ID
    const replicateModelId = type === 'text-to-image' 
      ? IMAGE_MODELS[model_id]
      : VIDEO_MODELS[model_id];

    if (!replicateModelId) {
      return NextResponse.json({ error: `Unknown model: ${model_id}` }, { status: 400 });
    }

    console.log(`[API] Generating ${type} with ${model_id} -> ${replicateModelId}`);

    let input: any = {
      prompt,
    };

    // Add negative prompt if provided
    if (negative_prompt) {
      input.negative_prompt = negative_prompt;
    }

    // Configure based on type
    if (type === 'text-to-video') {
      input = {
        ...input,
        num_frames: num_frames || 81,
        fps: fps || 16,
        guidance_scale: guidance_scale || 5.0,
      };
    } else if (type === 'image-to-video') {
      if (!image_url) {
        return NextResponse.json({ error: 'Image URL is required for image-to-video' }, { status: 400 });
      }
      input = {
        ...input,
        image: image_url,
        motion_bucket_id: 127,
        fps: fps || 6,
      };
    } else if (type === 'text-to-image') {
      input = {
        ...input,
        width: width || 1024,
        height: height || 1024,
        num_outputs: num_outputs || 1,
        output_format: 'webp',
        output_quality: 90,
      };
    }

    // Run the model
    const output = await replicate.run(
      replicateModelId as `${string}/${string}` | `${string}/${string}:${string}`,
      { input }
    );

    // Parse output
    let result: string | string[];
    if (Array.isArray(output)) {
      result = output;
    } else if (typeof output === 'string') {
      result = [output];
    } else if (output && typeof output === 'object') {
      // Handle ReadableStream or other formats
      if ('video' in output) {
        result = [(output as any).video];
      } else {
        result = [JSON.stringify(output)];
      }
    } else {
      throw new Error('Unexpected output format');
    }

    return NextResponse.json({
      success: true,
      type,
      model: model_id,
      output: result,
      url: Array.isArray(result) ? result[0] : result,
    });

  } catch (error: any) {
    console.error('[API] Replicate error:', error);
    return NextResponse.json(
      { 
        error: error.message || 'Generation failed',
        details: error.response?.data || null,
      }, 
      { status: 500 }
    );
  }
}

export async function GET() {
  // Return available models
  return NextResponse.json({
    video_models: Object.keys(VIDEO_MODELS),
    image_models: Object.keys(IMAGE_MODELS),
    status: 'active',
  });
}
