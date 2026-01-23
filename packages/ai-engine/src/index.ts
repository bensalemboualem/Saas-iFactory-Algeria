import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';

export interface AIExecutionRequest {
    model: 'claude' | 'gpt4' | 'mistral' | 'image' | 'video';
    prompt: string;
    outputs?: any[]; // Output definition
    maxTokens?: number;
}

export class AIEngine {
    private anthropic: Anthropic;
    private openai: OpenAI;

    constructor(apiKeyAnthropic?: string, apiKeyOpenAI?: string) {
        this.anthropic = new Anthropic({
            apiKey: apiKeyAnthropic || process.env.ANTHROPIC_API_KEY,
        });
        this.openai = new OpenAI({
            apiKey: apiKeyOpenAI || process.env.OPENAI_API_KEY,
        });
    }

    async execute(request: AIExecutionRequest): Promise<string> {
        const { model, prompt, maxTokens = 4096 } = request;

        console.log(`[AI-ENGINE] Executing with ${model}...`);

        try {
            if (model === 'claude') {
                const msg = await this.anthropic.messages.create({
                    model: "claude-3-5-sonnet-20240620",
                    max_tokens: maxTokens,
                    messages: [{ role: "user", content: prompt }]
                });
                // Handle ContentBlock text extraction
                const block = msg.content[0];
                if (block.type === 'text') {
                    return block.text;
                }
                return JSON.stringify(msg.content);

            } else if (model === 'gpt4') {
                const completion = await this.openai.chat.completions.create({
                    messages: [{ role: "user", content: prompt }],
                    model: "gpt-4-turbo",
                });
                return completion.choices[0].message.content || '';
            }

            throw new Error(`Model ${model} not implemented yet`);

        } catch (error) {
            console.error("[AI-ENGINE] Error:", error);
            throw error;
        }
    }
}

export const aiEngine = new AIEngine();
