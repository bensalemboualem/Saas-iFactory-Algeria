import type {
  BaseProvider,
  ChatCompletionRequest,
  ChatCompletionResponse,
  StreamChunk,
} from './types.js';

export class OllamaProvider implements BaseProvider {
  name = 'ollama';
  private baseURL: string;

  constructor(baseURL: string = 'http://localhost:11434') {
    this.baseURL = baseURL;
  }

  async complete(request: ChatCompletionRequest): Promise<ChatCompletionResponse> {
    const response = await fetch(`${this.baseURL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
        stream: false,
        options: {
          temperature: request.temperature,
          num_predict: request.max_tokens,
          top_p: request.top_p,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama error: ${response.statusText}`);
    }

    const data = await response.json();

    return {
      id: `ollama-${Date.now()}`,
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: request.model,
      choices: [
        {
          index: 0,
          message: {
            role: 'assistant',
            content: (data as any).message.content,
          },
          finish_reason: 'stop',
        },
      ],
      usage: (data as any).prompt_eval_count
        ? {
            prompt_tokens: (data as any).prompt_eval_count,
            completion_tokens: (data as any).eval_count,
            total_tokens: (data as any).prompt_eval_count + (data as any).eval_count,
          }
        : undefined,
    };
  }

  async *streamComplete(request: ChatCompletionRequest): AsyncGenerator<StreamChunk> {
    const response = await fetch(`${this.baseURL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
        stream: true,
        options: {
          temperature: request.temperature,
          num_predict: request.max_tokens,
          top_p: request.top_p,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama error: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error('No response body');

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.trim()) continue;

        const data = JSON.parse(line);
        
        yield {
          id: `ollama-${Date.now()}`,
          object: 'chat.completion.chunk',
          created: Math.floor(Date.now() / 1000),
          model: request.model,
          delta: {
            content: (data as any).message?.content || '',
          },
          finish_reason: data.done ? 'stop' : undefined,
        };
      }
    }
  }
}
