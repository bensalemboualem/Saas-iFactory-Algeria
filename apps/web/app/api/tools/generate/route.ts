import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';
import prisma from '@/lib/prisma';

// Types
interface GenerateRequest {
  toolSlug: string;
  toolName: string;
  category: string;
  inputs: Record<string, any>;
  systemPrompt: string;
  userPrompt: string;
  model?: 'claude-sonnet' | 'gpt-4o' | 'gpt-4o-mini';
}

// SECURITY: Credits calculated server-side based on model - NEVER trust client
const MODEL_CREDITS: Record<string, number> = {
  'claude-sonnet': 5,
  'gpt-4o': 4,
  'gpt-4o-mini': 1,
} as const;

// Initialize AI clients
const anthropic = process.env.ANTHROPIC_API_KEY
  ? new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
  : null;

const openai = process.env.OPENAI_API_KEY
  ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
  : null;

export async function POST(request: NextRequest) {
  try {
    // 1. Check authentication
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Non authentifié. Veuillez vous connecter.' },
        { status: 401 }
      );
    }

    const userId = session.user.id;

    // 2. Parse request body
    const body: GenerateRequest = await request.json();
    const {
      toolSlug,
      toolName,
      category,
      inputs,
      systemPrompt,
      userPrompt,
      model = 'claude-sonnet',
    } = body;

    // SECURITY: Calculate credits server-side based on model - NEVER trust client
    const credits = MODEL_CREDITS[model] ?? MODEL_CREDITS['gpt-4o-mini'];

    // 3. Check user credits
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { credits: true, plan: true },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'Utilisateur non trouvé' },
        { status: 404 }
      );
    }

    if (user.credits < credits) {
      return NextResponse.json(
        {
          error: 'Crédits insuffisants',
          required: credits,
          available: user.credits,
          upgradeUrl: '/pricing'
        },
        { status: 402 }
      );
    }

    // 4. Generate content based on model
    let content: string;
    let tokensUsed: number = 0;

    if (model === 'claude-sonnet' && anthropic) {
      const response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        system: systemPrompt,
        messages: [{ role: 'user', content: userPrompt }],
      });

      content = response.content[0].type === 'text' ? response.content[0].text : '';
      tokensUsed = response.usage.input_tokens + response.usage.output_tokens;

    } else if ((model === 'gpt-4o' || model === 'gpt-4o-mini') && openai) {
      const response = await openai.chat.completions.create({
        model: model === 'gpt-4o' ? 'gpt-4o' : 'gpt-4o-mini',
        max_tokens: 4096,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt },
        ],
      });

      content = response.choices[0]?.message?.content || '';
      tokensUsed = response.usage?.total_tokens || 0;

    } else {
      // Fallback: Check which client is available
      if (anthropic) {
        const response = await anthropic.messages.create({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 4096,
          system: systemPrompt,
          messages: [{ role: 'user', content: userPrompt }],
        });
        content = response.content[0].type === 'text' ? response.content[0].text : '';
        tokensUsed = response.usage.input_tokens + response.usage.output_tokens;
      } else if (openai) {
        const response = await openai.chat.completions.create({
          model: 'gpt-4o-mini',
          max_tokens: 4096,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
        });
        content = response.choices[0]?.message?.content || '';
        tokensUsed = response.usage?.total_tokens || 0;
      } else {
        return NextResponse.json(
          { error: 'Aucun provider IA configuré. Contactez le support.' },
          { status: 503 }
        );
      }
    }

    // 5. Deduct credits and save generation
    const [updatedUser, generation] = await prisma.$transaction([
      prisma.user.update({
        where: { id: userId },
        data: { credits: { decrement: credits } },
      }),
      prisma.generation.create({
        data: {
          userId,
          toolSlug,
          toolName,
          category,
          inputs: JSON.stringify(inputs),
          output: content,
          credits,
          model,
          tokens: tokensUsed,
        },
      }),
    ]);

    // 6. Update tool usage count (fire and forget)
    prisma.tool.upsert({
      where: { slug: toolSlug },
      create: { slug: toolSlug, name: toolName, category, usageCount: 1 },
      update: { usageCount: { increment: 1 } },
    }).catch(() => {}); // Non-blocking

    // 7. Return response
    return NextResponse.json({
      success: true,
      content,
      generation: {
        id: generation.id,
        createdAt: generation.createdAt,
      },
      credits: {
        used: credits,
        remaining: updatedUser.credits,
      },
      tokens: tokensUsed,
      model,
    });

  } catch (error: any) {
    console.error('Generation error:', error);

    // Handle specific API errors
    if (error.status === 429) {
      return NextResponse.json(
        { error: 'Limite de requêtes atteinte. Réessayez dans quelques secondes.' },
        { status: 429 }
      );
    }

    if (error.status === 401) {
      return NextResponse.json(
        { error: 'Erreur d\'authentification API. Contactez le support.' },
        { status: 500 }
      );
    }

    return NextResponse.json(
      { error: 'Erreur lors de la génération. Veuillez réessayer.' },
      { status: 500 }
    );
  }
}

// GET - Check generation status or get user's generations
export async function GET(request: NextRequest) {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Non authentifié' },
        { status: 401 }
      );
    }

    const userId = session.user.id;
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '10');
    const category = searchParams.get('category');

    const generations = await prisma.generation.findMany({
      where: {
        userId,
        ...(category ? { category } : {}),
      },
      orderBy: { createdAt: 'desc' },
      take: limit,
      select: {
        id: true,
        toolSlug: true,
        toolName: true,
        category: true,
        credits: true,
        model: true,
        createdAt: true,
      },
    });

    return NextResponse.json({ generations });

  } catch (error) {
    console.error('Get generations error:', error);
    return NextResponse.json(
      { error: 'Erreur lors de la récupération' },
      { status: 500 }
    );
  }
}
