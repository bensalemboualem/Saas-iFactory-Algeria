import { AITool } from '../../types';

export const blogOutlineGenerator: AITool = {
    id: 'blog-outline-generator',
    slug: 'blog-outline-generator',
    name: {
        fr: 'Générateur de Plan d\'Article',
        ar: 'مولد مخطط المقال',
        en: 'Blog Outline Generator',
    },
    description: {
        fr: 'Structurez vos articles avec des plans détaillés optimisés pour le SEO.',
        ar: 'قم ببناء مقالاتك بمخططات مفصلة ومحسنة لمحركات البحث.',
        en: 'Structure your articles with detailed, SEO-optimized outlines.',
    },
    category: 'blog',
    subcategory: 'planning',
    icon: 'ListTree',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet', required: true },
        { name: 'keywords', type: 'tags', label: 'Mots-clés', required: false },
        { name: 'wordCount', type: 'number', label: 'Longueur cible', default: 1500 },
        {
            name: 'articleType',
            type: 'select',
            label: 'Type d\'article',
            options: ['Article de fond', 'Liste (Listicle)', 'Guide Comment faire', 'Comparatif', 'Actualité']
        },
        {
            name: 'searchIntent',
            type: 'select',
            label: 'Intention de recherche',
            options: ['Informationnel (Savoir)', 'Transactionnel (Acheter)', 'Navigationnel (Trouver)', 'Commercial (Comparer)']
        }
    ],
    outputs: [
        { type: 'markdown', name: 'outline' }
    ],
    promptTemplate: `Tu es un stratège de contenu SEO.

SUJET : {{topic}}
MOTS-CLÉS : {{keywords}}
LONGUEUR CIBLE : {{wordCount}} mots
TYPE D'ARTICLE : {{articleType}}
INTENTION DE RECHERCHE : {{searchIntent}}

Crée un plan d'article détaillé :

STRUCTURE REQUISE :
1. Titre H1 optimisé
2. Meta description (155 car.)
3. Introduction (hook + contexte + promesse)
4. 5-8 sections H2 avec :
   - Titre H2 optimisé
   - 2-3 sous-sections H3
   - Points clés à couvrir
   - Mot-clé secondaire à inclure
5. Conclusion avec CTA
6. FAQ (3-5 questions)

OPTIMISATION SEO :
- Place le mot-clé principal dans H1, premier H2, conclusion
- Distribue les mots-clés secondaires naturellement
- Suggère les liens internes potentiels`,
    model: 'gpt4',
    estimatedTime: '20s',
    examples: []
};
