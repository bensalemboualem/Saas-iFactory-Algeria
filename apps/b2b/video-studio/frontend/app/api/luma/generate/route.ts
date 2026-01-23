import { NextRequest, NextResponse } from 'next/server';

const LUMA_API_KEY = process.env.LUMA_API_KEY || '';
const LUMA_API_URL = 'https://api.lumalabs.ai/dream-machine/v1/generations';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { prompt, image_url, aspect_ratio = '16:9', loop = false } = body;

    if (!prompt && !image_url) {
      return NextResponse.json(
        { error: 'Prompt or image_url is required' },
        { status: 400 }
      );
    }

    if (!LUMA_API_KEY) {
      return NextResponse.json(
        { error: 'LUMA_API_KEY not configured' },
        { status: 500 }
      );
    }

    console.log('[LUMA API] Generating video with prompt:', prompt);

    // Call Luma API
    const response = await fetch(LUMA_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${LUMA_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'ray-3',
        prompt: prompt,
        ...(image_url && { keyframes: { frame0: { type: 'image', url: image_url } } }),
        aspect_ratio: aspect_ratio,
        loop: loop,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[LUMA API] Error:', response.status, errorData);
      return NextResponse.json(
        {
          error: 'Luma API error',
          details: errorData,
          status: response.status
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('[LUMA API] Generation started:', data.id);

    // Return job info
    return NextResponse.json({
      success: true,
      job_id: data.id,
      status: data.state || 'queued',
      message: 'Video generation started',
    });

  } catch (error: any) {
    console.error('[LUMA API] Exception:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const job_id = searchParams.get('job_id');

    if (!job_id) {
      return NextResponse.json(
        { error: 'job_id parameter is required' },
        { status: 400 }
      );
    }

    console.log('[LUMA API] Checking status for job:', job_id);

    // Check job status
    const response = await fetch(`${LUMA_API_URL}/${job_id}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${LUMA_API_KEY}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[LUMA API] Status check error:', response.status, errorData);
      return NextResponse.json(
        { error: 'Failed to check status', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();

    // Map Luma state to our format
    const statusMap: Record<string, string> = {
      'queued': 'queued',
      'dreaming': 'processing',
      'completed': 'completed',
      'failed': 'failed',
    };

    return NextResponse.json({
      success: true,
      job_id: data.id,
      status: statusMap[data.state] || 'processing',
      progress: data.state === 'completed' ? 100 : data.state === 'dreaming' ? 50 : 0,
      video_url: data.state === 'completed' ? data.assets?.video : null,
      thumbnail_url: data.assets?.thumbnail || null,
      created_at: data.created_at,
    });

  } catch (error: any) {
    console.error('[LUMA API] Status check exception:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
