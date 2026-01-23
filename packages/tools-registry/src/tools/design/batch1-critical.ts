import { AITool } from '../../types';

export const midjourneyPromptGenerator: AITool = {
  id: 'midjourney-prompt-generator',
  slug: 'midjourney-prompt-generator',
  name: { fr: 'Générateur de Prompts Midjourney', ar: 'مولد مطالبات Midjourney', en: 'Midjourney Prompt Generator' },
  description: {
    fr: 'Générez des prompts détaillés et optimisés pour Midjourney v6',
    ar: 'قم بإنشاء مطالبات مفصلة ومحسنة لـ Midjourney v6',
    en: 'Generate detailed and optimized prompts for Midjourney v6'
  },
  category: 'design',
  subcategory: 'prompts',
  icon: 'Zap',
  credits: 5,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'subject', type: 'text', label: 'Sujet principal', required: true },
    { name: 'art_style', type: 'select', label: 'Style artistique', options: ['Photorealistic', 'Cinematic', 'Anime', 'Digital Art', 'Oil Painting', 'Cyberpunk', 'Minimalist'] },
    { name: 'lighting', type: 'select', label: 'Éclairage', options: ['Cinematic Lighting', 'Natural Light', 'Studio Lighting', 'Neon Lights', 'Golden Hour'] },
    { name: 'aspect_ratio', type: 'select', label: 'Format (Aspect Ratio)', options: ['--ar 16:9', '--ar 9:16', '--ar 1:1', '--ar 4:5', '--ar 3:2'] }
  ],
  outputs: [{ type: 'text', name: 'prompt' }],
  promptTemplate: `Act as a prompt engineer for Midjourney v6.
Generate 5 detailed prompts for the following subject: {{subject}}
Style: {{art_style}}
Lighting: {{lighting}}
Aspect Ratio: {{aspect_ratio}}

Structure your response as a list of copiable commands like this:
/imagine prompt: [detailed description], [style keywords], [lighting keywords], [camera settings], --v 6 {{aspect_ratio}}

Provide variety in composition and mood.`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const dallePromptGenerator: AITool = {
  id: 'dalle-prompt-generator',
  slug: 'dalle-prompt-generator',
  name: { fr: 'Générateur de Prompts DALL-E 3', ar: 'مولد مطالبات DALL-E 3', en: 'DALL-E 3 Prompt Generator' },
  description: {
    fr: 'Créez des descriptions précises pour obtenir exactement ce que vous voulez avec DALL-E 3',
    ar: 'أنشئ أوصافًا دقيقة للحصول على ما تريده تمامًا باستخدام DALL-E 3',
    en: 'Create precise descriptions to get exactly what you want with DALL-E 3'
  },
  category: 'design',
  subcategory: 'prompts',
  icon: 'Zap',
  credits: 5,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'concept', type: 'textarea', label: 'Concept ou Idée', required: true },
    { name: 'style', type: 'text', label: 'Style visuel (ex: 3D render, Photo, Dessin)' },
    { name: 'mood', type: 'text', label: 'Ambiance' }
  ],
  outputs: [{ type: 'text', name: 'prompt' }],
  promptTemplate: `You are an expert at prompting DALL-E 3.
Create a detailed, descriptive prompt based on this concept: {{concept}}
Style: {{style}}
Mood: {{mood}}

DALL-E 3 prefers natural language descriptions over keyword lists. Write a cohesive paragraph describing the scene, the subject, the action, the lighting, and the artistic style in vivid detail.`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const stableDiffusionPromptGenerator: AITool = {
  id: 'stable-diffusion-prompt-generator',
  slug: 'stable-diffusion-prompt-generator',
  name: { fr: 'Générateur Stable Diffusion', ar: 'مولد Stable Diffusion', en: 'Stable Diffusion Prompt Generator' },
  description: {
    fr: 'Optimisez vos prompts pour Stable Diffusion XL (SDXL) avec les bons mots-clés',
    ar: 'قم بتحسين مطالباتك لـ Stable Diffusion XL باستخدام الكلمات الرئيسية الصحيحة',
    en: 'Optimize your prompts for Stable Diffusion XL (SDXL) with the right keywords'
  },
  category: 'design',
  subcategory: 'prompts',
  icon: 'Zap',
  credits: 5,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'topic', type: 'text', label: 'Sujet', required: true },
    { name: 'style_ref', type: 'text', label: 'Référence de style (Artiste ou Mouvement)' },
    { name: 'negative_prompt', type: 'boolean', label: 'Inclure Negative Prompt suggéré ?' }
  ],
  outputs: [{ type: 'markdown', name: 'prompts' }],
  promptTemplate: `Generate 3 high-quality prompts for Stable Diffusion XL regarding: {{topic}}
Style reference: {{style_ref}}

Format:
**Positive Prompt:** (Subject), (Action), (Context), (Art Style), (Tags: "4k", "detailed", "trending on artstation", etc.)
{{#if negative_prompt}}
**Negative Prompt:** (List of things to avoid like "ugly", "deformed", "blurry", etc.)
{{/if}}`,
  model: 'gpt3.5',
  estimatedTime: '15s'
};

export const imageAltTextGenerator: AITool = {
  id: 'image-alt-text-generator',
  slug: 'image-alt-text-generator',
  name: { fr: 'Générateur de Texte Alternatif (Alt Text)', ar: 'مولد النص البديل للصورة', en: 'Image Alt Text Generator' },
  description: {
    fr: 'Améliorez votre SEO et l\'accessibilité avec des balises Alt optimisées',
    ar: 'حسن تحسين محركات البحث وإمكانية الوصول باستخدام نص بديل محسن',
    en: 'Improve your SEO and accessibility with optimized Alt tags'
  },
  category: 'design',
  subcategory: 'seo',
  icon: 'Sliders',
  credits: 3,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'image_description', type: 'textarea', label: 'Décrivez l\'image brièvement', required: true },
    { name: 'keywords', type: 'text', label: 'Mots-clés SEO cibles' },
    { name: 'context', type: 'text', label: 'Contexte d\'utilisation (ex: Article de blog, E-commerce)' }
  ],
  outputs: [{ type: 'text', name: 'alt_text' }],
  promptTemplate: `Generate 3 options for Image Alt Text based on this description: {{image_description}}
SEO Keywords to include if natural: {{keywords}}
Context: {{context}}

Rules:
1. Describe the image content accurately.
2. Keep it under 125 characters if possible.
3. Don't start with "Image of..." or "Picture of...".
4. Make it descriptive but concise.

Output format:
Option 1: [Alt text]
Option 2: [Alt text]
Option 3: [Alt text]`,
  model: 'gpt3.5',
  estimatedTime: '10s'
};

export const socialMediaImageIdeas: AITool = {
  id: 'social-media-image-ideas',
  slug: 'social-media-image-ideas',
  name: { fr: 'Idées de Visuels Social Media', ar: 'أفكار صور وسائل التواصل', en: 'Social Media Image Ideas' },
  description: {
    fr: 'Trouvez des idées créatives de visuels pour vos posts Instagram, LinkedIn, etc.',
    ar: 'اعثر على أفكار بصرية إبداعية لمنشوراتك',
    en: 'Find creative visual ideas for your social media posts'
  },
  category: 'design',
  subcategory: 'social',
  icon: 'Instagram',
  credits: 5,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'post_topic', type: 'text', label: 'Sujet du post', required: true },
    { name: 'platform', type: 'select', label: 'Plateforme', options: ['Instagram', 'LinkedIn', 'Twitter', 'Facebook', 'Pinterest'] },
    { name: 'brand_vibe', type: 'text', label: 'Vibe de la marque (ex: Fun, Pro, Luxe)' }
  ],
  outputs: [{ type: 'markdown', name: 'ideas' }],
  promptTemplate: `Suggest 5 creative visual ideas for a {{platform}} post about: {{post_topic}}
Brand Vibe: {{brand_vibe}}

For each idea, describe:
1. The Image/Graphic Concept (Composition, Colors, Elements).
2. Text overlay suggestions (if any).
3. Why it stops the scroll.`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const logoConceptGenerator: AITool = {
  id: 'logo-concept-generator',
  slug: 'logo-concept-generator',
  name: { fr: 'Générateur de Concepts de Logo', ar: 'مولد مفاهيم الشعار', en: 'Logo Concept Generator' },
  description: {
    fr: 'Brainstormez des idées de logos originaux pour votre marque',
    ar: 'عصف ذهني لأفكار شعار أصلية لعلامتك التجارية',
    en: 'Brainstorm original logo ideas for your brand'
  },
  category: 'design',
  subcategory: 'branding',
  icon: 'Palette',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité', required: true },
    { name: 'values', type: 'text', label: 'Valeurs (ex: Trust, Speed, Innovation)' },
    { name: 'style_preference', type: 'select', label: 'Préférence de style', options: ['Minimalist', 'Vintage', 'Abstract', 'Mascot', 'Typography-based'] }
  ],
  outputs: [{ type: 'markdown', name: 'concepts' }],
  promptTemplate: `Generate 5 unique logo design concepts for:
Brand Name: {{brand_name}}
Industry: {{industry}}
Values: {{values}}
Style: {{style_preference}}

For each concept provide:
1. **Visual Symbol:** What is the icon/symbol? What does it represent?
2. **Typography:** Suggested font style (Serif, Sans-serif, Script, Bold, etc.).
3. **Color Palette:** 2-3 colors with hex codes or names.
4. **Vibe:** How it feels to the viewer.
`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const colorPaletteGenerator: AITool = {
  id: 'color-palette-generator',
  slug: 'color-palette-generator',
  name: { fr: 'Générateur de Palette de Couleurs', ar: 'مولد لوحة الألوان', en: 'Color Palette Generator' },
  description: {
    fr: 'Créez des palettes de couleurs harmonieuses pour vos projets',
    ar: 'أنشئ لوحات ألوان متناغمة لمشاريعك',
    en: 'Create harmonious color palettes for your projects'
  },
  category: 'design',
  subcategory: 'branding',
  icon: 'Palette',
  credits: 5,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'project_description', type: 'text', label: 'Description du projet', required: true },
    { name: 'base_color', type: 'text', label: 'Couleur de base (Optionnel - Nom ou Hex)' },
    { name: 'emotion', type: 'text', label: 'Émotion souhaitée (ex: Calme, Énergie, Confiance)' }
  ],
  outputs: [{ type: 'markdown', name: 'palettes' }],
  promptTemplate: `Generate 3 distinct color palettes for a project described as: {{project_description}}
Base color (if any): {{base_color}}
Desired emotion: {{emotion}}

For each palette, provide:
- A creative name for the palette.
- 5 colors (Hex codes).
- The rationale behind the combination.
- Use cases (Background, Accent, Text, etc.).`,
  model: 'gpt3.5',
  estimatedTime: '15s'
};

export const uiComponentIdeas: AITool = {
  id: 'ui-component-ideas',
  slug: 'ui-component-ideas',
  name: { fr: 'Idées de Composants UI', ar: 'أفكار مكونات واجهة المستخدم', en: 'UI Component Ideas' },
  description: {
    fr: 'Obtenez des spécifications et idées pour des composants d\'interface modernes',
    ar: 'احصل على مواصفات وأفكار لمكونات واجهة المستخدم الحديثة',
    en: 'Get specifications and ideas for modern UI components'
  },
  category: 'design',
  subcategory: 'ui_ux',
  icon: 'Layout',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'component_name', type: 'text', label: 'Nom du composant (ex: Card, Navbar, Modal)', required: true },
    { name: 'app_style', type: 'text', label: 'Style de l\'app (ex: Modern SaaS, Dark Mode, Corporate)' },
    { name: 'functionality', type: 'text', label: 'Fonctionnalité principale' }
  ],
  outputs: [{ type: 'markdown', name: 'ideas' }],
  promptTemplate: `You are a UI/UX expert. Provide 3 design variations for a {{component_name}} component.
App Style: {{app_style}}
Functionality: {{functionality}}

For each variation:
1. **Name:** Descriptive name of the variant.
2. **Layout/Structure:** How elements are arranged.
3. **Visual Details:** Shadows, borders, rounded corners, typography.
4. **Interactions:** Hover states, click effects.
5. **Pros:** Why choose this one?`,
  model: 'gpt4',
  estimatedTime: '30s'
};
