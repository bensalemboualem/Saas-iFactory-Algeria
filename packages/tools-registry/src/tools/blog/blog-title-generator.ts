import { AITool } from '../../types';

export const blogTitleGenerator: AITool = {
    id: 'blog-title-generator',
    slug: 'blog-title-generator',
    name: {
        fr: 'Générateur de Titres Blog',
        ar: 'مولد عناوين المدونة',
        en: 'Blog Title Generator',
    },
    description: {
        fr: 'Créez des titres accrocheurs et optimisés pour le clic (CTR) et le SEO.',
        ar: 'أنشئ عناوين جذابة ومحسنة للنقر (CTR) ومحركات البحث (SEO).',
        en: 'Create catchy, CTR and SEO optimized titles.',
    },
    category: 'blog',
    subcategory: 'ideation',
    icon: 'Heading',
    credits: 5,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'topic',
            type: 'text',
            label: 'Sujet de l\'article',
            required: true
        },
        {
            name: 'keyword',
            type: 'text',
            label: 'Mot-clé principal',
            required: true
        },
        {
            name: 'style',
            type: 'select',
            label: 'Style de titre',
            options: ['Clickbait', 'Professionnel', 'Question', 'Guide / How-to', 'Liste (Top 10)'],
            default: 'Clickbait'
        },
        {
            name: 'emotion',
            type: 'select',
            label: 'Émotion cible',
            options: ['Curiosité', 'Urgence', 'Bénéfice immédiat', 'Peur / Erreur à éviter', 'Surprise'],
            default: 'Curiosité'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'titles' }
    ],
    promptTemplate: `Tu es un expert en copywriting et SEO.

SUJET : {{topic}}
MOT-CLÉ PRINCIPAL : {{keyword}}
STYLE : {{style}}
ÉMOTION : {{emotion}}

Génère 10 titres uniques pour un article de blog :

RÈGLES :
1. Maximum 60 caractères (SEO optimal)
2. Inclure le mot-clé naturellement
3. Créer de la curiosité ou promettre une valeur
4. Éviter les titres génériques
5. Utiliser des chiffres quand pertinent
6. Varier les formules

FORMAT :
1. [Titre] - [Pourquoi ça marche]
2. ...

Bonus : Suggère le meilleur titre avec explication.`,
    model: 'gpt4',
    estimatedTime: '15s',
    examples: []
};
