import { AITool } from '../../types';

export const articleRewriter: AITool = {
    id: 'article-rewriter',
    slug: 'article-rewriter',
    name: {
        fr: 'Réécrivain d\'Article Intelligent',
        ar: 'معيد كتابة المقالات الذكي',
        en: 'Smart Article Rewriter',
    },
    description: {
        fr: 'Réécrivez des articles entiers pour les rendre uniques tout en gardant le sens.',
        ar: 'أعد كتابة مقالات كاملة لجعلها فريدة مع الحفاظ على المعنى.',
        en: 'Rewrite entire articles to make them unique while keeping the meaning.',
    },
    category: 'blog',
    subcategory: 'rewriting',
    icon: 'RefreshCw',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'content',
            type: 'textarea',
            label: 'Article original',
            required: true
        },
        {
            name: 'mode',
            type: 'select',
            label: 'Mode de réécriture',
            options: ['Standard (Synonymes)', 'Créatif (Reformulation)', 'Simplifié (Vulgarisation)', 'Formel (Professionnel)'],
            default: 'Créatif'
        },
        {
            name: 'language',
            type: 'select',
            label: 'Langue de sortie',
            options: ['Français', 'Arabe', 'Anglais'],
            default: 'Français'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'rewrittenContent' }
    ],
    promptTemplate: `Tu es un expert en réécriture de contenu.

TEXTE ORIGINAL :
{{content}}

MODE : {{mode}}
LANGUE CIBLE : {{language}}

TÂCHE : Réécris ce texte intégralement.

CONTRAINTES :
1. Le sens doit rester identique
2. Utilise un vocabulaire différent (synonymes pertinents)
3. Change la structure des phrases (voix passive/active)
4. Passe le test de plagiat (100% unique)
5. Adapte le ton selon le mode choisi : {{mode}}

Rends uniquement le texte réécrit.`,
    model: 'claude',
    estimatedTime: '45s',
    examples: []
};
