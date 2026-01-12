import { createAnthropic } from '@ai-sdk/anthropic';
import { streamText } from 'ai';
import { SYSTEM_PROMPT } from '@/app/agents/motivation/prompts/system-prompt';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

// Initialize Anthropic (Claude)
const anthropic = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || '',
});

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    // Check if API key is configured
    if (!process.env.ANTHROPIC_API_KEY) {
      return new Response(
        JSON.stringify({
          error: 'API key not configured. Please add ANTHROPIC_API_KEY to .env.local',
        }),
        { status: 500 }
      );
    }

    // Stream the AI response
    const result = await streamText({
      model: anthropic('claude-3-5-sonnet-20241022'),
      system: SYSTEM_PROMPT,
      messages,
      temperature: 0.7,
      maxTokens: 1000,
    });

    return result.toAIStreamResponse();
  } catch (error) {
    console.error('Chat API Error:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to process chat request',
      }),
      { status: 500 }
    );
  }
}
