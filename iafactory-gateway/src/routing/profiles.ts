export interface ModelProfile {
  id: string;
  name: string;
  description: string;
  provider: 'groq' | 'openrouter' | 'deepseek' | 'ollama';
  actualModel: string;
  pricing: {
    input: number;  // per 1M tokens
    output: number; // per 1M tokens
  };
  features: {
    streaming: boolean;
    functionCalling: boolean;
    vision: boolean;
  };
  latency: 'ultra-fast' | 'fast' | 'normal' | 'slow';
  contextWindow: number;
}

export const MODEL_PROFILES: ModelProfile[] = [
  // IAF-FAST: Groq (ultra-low latency)
  {
    id: 'iaf-fast-llama',
    name: 'IAFactory Fast (Llama 3.3 70B)',
    description: 'Ultra-fast responses with Groq, ideal for interactive chat',
    provider: 'groq',
    actualModel: 'llama-3.3-70b-versatile',
    pricing: { input: 0.1, output: 0.1 },
    features: { streaming: true, functionCalling: true, vision: false },
    latency: 'ultra-fast',
    contextWindow: 128000,
  },
  {
    id: 'iaf-fast-mixtral',
    name: 'IAFactory Fast (Mixtral 8x7B)',
    description: 'Fast multilingual model via Groq',
    provider: 'groq',
    actualModel: 'mixtral-8x7b-32768',
    pricing: { input: 0.05, output: 0.05 },
    features: { streaming: true, functionCalling: false, vision: false },
    latency: 'ultra-fast',
    contextWindow: 32768,
  },

  // IAF-SMART: OpenRouter (premium models)
  {
    id: 'iaf-smart-claude',
    name: 'IAFactory Smart (Claude 3.5 Sonnet)',
    description: 'Best reasoning and code quality via OpenRouter',
    provider: 'openrouter',
    actualModel: 'anthropic/claude-3.5-sonnet',
    pricing: { input: 3.0, output: 15.0 },
    features: { streaming: true, functionCalling: true, vision: true },
    latency: 'normal',
    contextWindow: 200000,
  },
  {
    id: 'iaf-smart-gpt4',
    name: 'IAFactory Smart (GPT-4 Turbo)',
    description: 'OpenAI flagship model via OpenRouter',
    provider: 'openrouter',
    actualModel: 'openai/gpt-4-turbo',
    pricing: { input: 10.0, output: 30.0 },
    features: { streaming: true, functionCalling: true, vision: true },
    latency: 'normal',
    contextWindow: 128000,
  },

  // IAF-CHEAP: DeepSeek & Chinese models
  {
    id: 'iaf-cheap-deepseek',
    name: 'IAFactory Cheap (DeepSeek V3)',
    description: 'Best price/performance ratio for coding',
    provider: 'deepseek',
    actualModel: 'deepseek-chat',
    pricing: { input: 0.14, output: 0.28 },
    features: { streaming: true, functionCalling: true, vision: false },
    latency: 'fast',
    contextWindow: 64000,
  },
  {
    id: 'iaf-cheap-qwen',
    name: 'IAFactory Cheap (Qwen 2.5 72B)',
    description: 'Alibaba model via OpenRouter',
    provider: 'openrouter',
    actualModel: 'qwen/qwen-2.5-72b-instruct',
    pricing: { input: 0.3, output: 0.3 },
    features: { streaming: true, functionCalling: true, vision: false },
    latency: 'fast',
    contextWindow: 32768,
  },

  // IAF-LOCAL: On-premise (future)
  {
    id: 'iaf-local-llama',
    name: 'IAFactory Local (Llama 3.1 8B)',
    description: 'On-premise model for RGPD compliance',
    provider: 'ollama',
    actualModel: 'llama3.1:8b',
    pricing: { input: 0, output: 0 },
    features: { streaming: true, functionCalling: false, vision: false },
    latency: 'slow',
    contextWindow: 128000,
  },
];

export function getAvailableModels(): ModelProfile[] {
  return MODEL_PROFILES;
}

export function getModelById(id: string): ModelProfile | undefined {
  return MODEL_PROFILES.find((m) => m.id === id);
}

export function getDefaultModel(): ModelProfile {
  return MODEL_PROFILES[0]; // iaf-fast-llama
}
