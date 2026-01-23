import OpenAI from 'openai';
import { appConfig } from '../config.js';
import type {
  BaseProvider,
  ChatCompletionRequest,
  ChatCompletionResponse,
  StreamChunk,
} from './types.js';

export class OpenRouterProvider implements BaseProvider {
  name = 'openrouter';
  private client: OpenAI;

  constructor() {
    if (!appConfig.OPENROUTER_API_KEY) {
      throw new Error('OPENROUTER_API_KEY not configured');
    }

    this.client = new OpenAI({
      apiKey: appConfig.OPENROUTER_API_KEY,
      baseURL: appConfig.OPENROUTER_BASE_URL,
      defaultHeaders: {
        'HTTP-Referer': appConfig.OPENROUTER_APP_URL || 'https://iafactory.dz',
        'X-Title': appConfig.OPENROUTER_APP_NAME,
      },
    });
  }

  async complete(request: ChatCompletionRequest): Promise<ChatCompletionResponse> {
    const response = await this.client.chat.completions.create({
      model: request.model,
      messages: request.messages,
      temperature: request.temperature,
      max_tokens: request.max_tokens,
      top_p: request.top_p,
      frequency_penalty: request.frequency_penalty,
      presence_penalty: request.presence_penalty,
      stream: false,
    });

    return {
      id: response.id,
      object: 'chat.completion',
      created: response.created,
      model: response.model,
      choices: response.choices.map((choice) => ({
        index: choice.index,
        message: {
          role: choice.message.role as 'assistant',
          content: choice.message.content || '',
        },
        finish_reason: choice.finish_reason || 'stop',
      })),
      usage: response.usage
        ? {
            prompt_tokens: response.usage.prompt_tokens,
            completion_tokens: response.usage.completion_tokens,
            total_tokens: response.usage.total_tokens,
          }
        : undefined,
    };
  }

  async *streamComplete(request: ChatCompletionRequest): AsyncGenerator<StreamChunk> {
    const stream = await this.client.chat.completions.create({
      model: request.model,
      messages: request.messages,
      temperature: request.temperature,
      max_tokens: request.max_tokens,
      top_p: request.top_p,
      stream: true,
    });

    for await (const chunk of stream) {
      const choice = chunk.choices[0];
      
      yield {
        id: chunk.id,
        object: 'chat.completion.chunk',
        created: chunk.created,
        model: chunk.model,
        delta: {
          role: choice.delta.role,
          content: choice.delta.content || '',
        },
        finish_reason: choice.finish_reason || undefined,
      };
    }
  }
}
