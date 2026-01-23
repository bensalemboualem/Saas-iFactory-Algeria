export type ToolCategory =
    | 'blog'
    | 'seo'
    | 'social'
    | 'youtube'
    | 'email'
    | 'ecommerce'
    | 'business'
    | 'ads'
    | 'images'
    | 'video'
    | 'education-dz'
    | 'admin-dz'
    | 'compliance-dz'
    | 'finance-dz'
    | 'hr'
    | 'support'
    | 'design';

export interface ToolInput {
    default?: any;
    label?: string;
    name: string;
    options?: string[];
    placeholder?: string;
    required?: boolean;
    type: 'text' | 'textarea' | 'number' | 'select' | 'tags' | 'boolean'; // For select type
}

export interface ToolOutput {
    name: string;
    type: 'text' | 'markdown' | 'json' | 'image' | 'video';
}

export interface AITool {
    category: ToolCategory;
    // Icon name (lucide-react)
    credits: number;
    description: {
        ar: string;
        en: string;
        fr: string;
    };
    estimatedTime?: string;
    examples?: {
        avgTime: string;
        outputSample?: string;
    }[];
    icon: string;
    id: string;
    inputs: ToolInput[];
    isAlgeriaExclusive: boolean;
    model: 'claude' | 'gpt4' | 'mistral' | 'image' | 'video';
    name: {
        ar: string;
        darija?: string;
        en: string;
        fr: string;
    };
    outputs: ToolOutput[];
    priority: 'critical' | 'high' | 'medium' | 'low';
    promptTemplate: string;
    slug: string;
    subcategory?: string;
}
