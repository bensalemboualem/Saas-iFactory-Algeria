import { AITool } from '../../types';

export const humanWrittenBlog: AITool = {
    id: 'human-written-blog',
    slug: 'human-written-blog',
    name: {
        fr: 'Article Blog 100% Humain',
        ar: 'مقال مدونة بشري 100٪',
        en: 'Human Written Blog (Undetectable)',
    },
    description: {
        fr: 'Créez du contenu indétectable par les outils IA. Style naturel, imparfait et humain.',
        ar: 'أنشئ محتوى لا يمكن اكتشافه بواسطة أدوات الذكاء الاصطناعي. أسلوب طبيعي وغير كامل وبشري.',
        en: 'Create content undetectable by AI tools. Natural, imperfect and human style.',
    },
    category: 'blog',
    subcategory: 'writing',
    icon: 'UserCheck', // Lucide icon
    credits: 60,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'topic',
            type: 'text',
            label: 'Sujet',
            required: true
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
        { type: 'markdown', name: 'content' }
    ],
    promptTemplate: `Tu es un rédacteur humain professionnel. Ton objectif est d'écrire un article qui :
- Semble 100% écrit par un humain
- Passe tous les détecteurs IA (GPTZero, Originality.ai, etc.)

SUJET : {{topic}}
LANGUE : {{language}}

TECHNIQUES ANTI-DÉTECTION À APPLIQUER :
1. Varie la longueur des phrases (courtes ET longues)
2. Utilise des expressions idiomatiques et familières
3. Ajoute des opinions personnelles et anecdotes
4. Fais des transitions naturelles (pas "De plus", "En outre")
5. Inclus des imperfections mineures (sans fautes)
6. Utilise "je", "vous", "on" de manière naturelle
7. Ajoute des questions rhétoriques
8. Varie le rythme : paragraphes courts puis longs
9. Utilise des métaphores et comparaisons originales
10. Évite les structures trop parfaites

INTERDITS :
- Phrases qui commencent par "Il est important de noter"
- "Dans cet article, nous allons..."
- Structures trop prévisibles
- Vocabulaire trop soutenu partout
- Transitions robotiques

Écris comme si tu racontais à un ami passionné par le sujet.`,
    model: 'claude',
    estimatedTime: '60s',
    examples: []
};
