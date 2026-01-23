import { AITool } from '../../types';

export const aiBlogWriter: AITool = {
    id: 'blog-writer',
    slug: 'ai-blog-writer',
    name: {
        fr: 'Rédacteur de Blog IA',
        ar: 'كاتب المدونات بالذكاء الاصطناعي',
        en: 'AI Blog Writer',
    },
    description: {
        fr: 'Générez des articles de blog complets, optimisés SEO et bien structurés.',
        ar: 'أنشئ مقالات مدونة كاملة ومحسنة لمحركات البحث ومنظمة بشكل جيد.',
        en: 'Generate full, SEO-optimized, and well-structured blog articles.',
    },
    category: 'blog',
    subcategory: 'writing',
    icon: 'FileText',
    credits: 50,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'topic',
            type: 'text',
            label: 'Sujet de l\'article',
            placeholder: 'Ex: Les bienfaits du jeûne intermittent',
            required: true
        },
        {
            name: 'keywords',
            type: 'tags',
            label: 'Mots-clés cibles',
            placeholder: 'santé, nutrition, perte de poids',
            required: false
        },
        {
            name: 'tone',
            type: 'select',
            label: 'Ton',
            options: ['Professionnel', 'Amical', 'Académique', 'Inspirant', 'Humoristique'],
            default: 'Professionnel'
        },
        {
            name: 'wordCount',
            type: 'number',
            label: 'Nombre de mots cible',
            default: 1500,
            required: true
        },
        {
            name: 'language',
            type: 'select',
            label: 'Langue',
            options: ['Français', 'Arabe', 'Anglais', 'Darija'],
            default: 'Français'
        },
        {
            name: 'audience',
            type: 'text',
            label: 'Public cible',
            placeholder: 'Ex: Débutants en fitness'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'content' }
    ],
    promptTemplate: `Tu es un rédacteur SEO expert francophone avec 10 ans d'expérience.

SUJET : {{topic}}
MOTS-CLÉS : {{keywords}}
TON : {{tone}}
LONGUEUR : {{wordCount}} mots
LANGUE : {{language}}
PUBLIC CIBLE : {{audience}}

INSTRUCTIONS :
1. Rédige un article complet et approfondi
2. Structure avec H1, H2, H3 logiques
3. Inclus les mots-clés naturellement (densité 1-2%)
4. Ajoute des listes à puces quand pertinent
5. Utilise des exemples concrets
6. Inclus des statistiques si possible
7. Termine par une conclusion avec CTA

FORMAT DE SORTIE :
- Titre H1 accrocheur (60 caractères max)
- Meta description (155 caractères)
- Article complet structuré
- 3 suggestions de titres alternatifs

Écris de manière naturelle, engageante, comme un humain expert.`,
    model: 'claude',
    estimatedTime: '60s',
    examples: []
};
