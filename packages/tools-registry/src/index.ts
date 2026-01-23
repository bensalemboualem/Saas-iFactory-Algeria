import { AITool, ToolCategory } from './types';
import { blogTools } from './tools/blog';
import { seoTools } from './tools/seo';
import { adminDzTools } from './tools/admin-dz';
import { educationDzTools } from './tools/education-dz';
import { youtubeTools } from './tools/youtube';
import { socialTools } from './tools/social';
import { emailTools } from './tools/email';
import { ecommerceTools } from './tools/ecommerce';
import { businessTools } from './tools/business';
import { designTools } from './tools/design';

// Aggregated Tools List
export const allTools: AITool[] = [
    ...blogTools,
    ...seoTools,
    ...adminDzTools,
    ...educationDzTools,
    ...youtubeTools,
    ...socialTools,
    ...emailTools,
    ...ecommerceTools,
    ...businessTools,
    ...designTools
];

export class ToolsRegistry {
    private tools: Map<string, AITool>;

    constructor() {
        this.tools = new Map(allTools.map(tool => [tool.id, tool]));
    }

    getTool(id: string): AITool | undefined {
        return this.tools.get(id);
    }

    getTools(filter?: { category?: ToolCategory; subcategory?: string }): AITool[] {
        if (!filter) return allTools;
        return allTools.filter(tool => {
            if (filter.category && tool.category !== filter.category) return false;
            if (filter.subcategory && tool.subcategory !== filter.subcategory) return false;
            return true;
        });
    }

    buildPrompt(tool: AITool, inputs: Record<string, any>): string {
        let prompt = tool.promptTemplate;
        for (const [key, value] of Object.entries(inputs)) {
            // eslint-disable-next-line
            prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), String(value));
        }
        return prompt;
    }
}

export const toolsRegistry = new ToolsRegistry();
export { adminDzTools } from './tools/admin-dz';
export { blogTools } from './tools/blog';
export { businessTools } from './tools/business';
export { designTools } from './tools/design';
export { ecommerceTools } from './tools/ecommerce';
export { educationDzTools } from './tools/education-dz';
export { emailTools } from './tools/email';
export { seoTools } from './tools/seo';
export { socialTools } from './tools/social';
export { youtubeTools } from './tools/youtube';
export * from './types';
