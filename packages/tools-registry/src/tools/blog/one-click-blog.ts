import { AITool } from '../../types';

export const oneClickBlog: AITool = {
    id: 'one-click-blog',
    slug: 'one-click-blog',
    name: {
        fr: 'Article de Blog en 1 Clic',
        ar: 'مقال مدونة بنقرة واحدة',
        en: 'One Click Blog Post',
    },
    description: {
        fr: 'La méthode la plus rapide : Entrez juste un titre, l\'IA fait tout le reste (Plan, Rédaction, SEO).',
        ar: 'أسرع طريقة: فقط أدخل العنوان، وسيقوم الذكاء الاصطناعي بالباقي (المخطط، الكتابة، تحسين محركات البحث).',
        en: 'The fastest method: Just enter a title, AI does the rest (Outline, Writing, SEO).',
    },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Zap',
    credits: 60,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'title',
            type: 'text',
            label: 'Titre de votre article',
            placeholder: 'Ex: Comment débuter en jardinage urbain',
            required: true
        },
        {
            name: 'tone',
            type: 'select',
            label: 'Ton',
            options: ['Informatif', 'Inspirant', 'Opinion', 'Drôle'],
            default: 'Informatif'
        },
        {
            name: 'language',
            type: 'select',
            label: 'Langue',
            options: ['Français', 'Arabe', 'Anglais'],
            default: 'Français'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'fullArticle' }
    ],
    promptTemplate: `Génère un article de blog COMPLET à partir de ce seul titre : "{{title}}"

  Langue : {{language}}
  Ton : {{tone}}
  
  AUTO-PILOT MODE :
  1. Déduis les meilleurs mots-clés SEO pour ce titre
  2. Crée un plan logique en interne
  3. Rédige l'article complet (Introduction, Corps H2/H3, Conclusion)
  4. Optimise pour le SEO sans qu'on ait besoin de le demander
  
  Rends l'article final formaté en Markdown.`,
    model: 'claude',
    estimatedTime: '90s',
    examples: []
};
