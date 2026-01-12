export interface SSEChunk {
  id?: string;
  event?: string;
  data: any;
}

export function createSSEStream(chunk: any): string {
  // OpenAI-compatible SSE format
  const data = {
    id: chunk.id || `chatcmpl-${Date.now()}`,
    object: 'chat.completion.chunk',
    created: Math.floor(Date.now() / 1000),
    model: chunk.model,
    choices: [
      {
        index: 0,
        delta: chunk.delta || {},
        finish_reason: chunk.finish_reason || null,
      },
    ],
  };

  return `data: ${JSON.stringify(data)}\n\n`;
}

export function createSSEError(error: string): string {
  return `data: ${JSON.stringify({ error })}\n\n`;
}

export function createSSEDone(): string {
  return 'data: [DONE]\n\n';
}
