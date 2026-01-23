import { AITool } from '../../types';

export const aiHumanizer: AITool = {
    id: 'ai-humanizer',
    slug: 'ai-humanizer',
    name: {
        fr: 'Humaniseur de Texte IA',
        ar: 'أداة أنسنة النص',
        en: 'AI Text Humanizer',
    },
    description: {
        fr: 'Transformez un texte généré par IA en texte naturel indétectable.',
        ar: 'حول النص الناتج عن الذكاء الاصطناعي إلى نص طبيعي لا يمكن اكتشافه.',
        en: 'Transform AI-generated text into undetectable natural text.',
    },
    category: 'blog',
    subcategory: 'rewriting',
    icon: 'Wand2',
    credits: 15,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'inputText',
            type: 'textarea',
            label: 'Texte à humaniser',
            placeholder: 'Collez votre texte IA ici...',
            required: true
        },
        {
            name: 'level',
            type: 'select',
            label: 'Niveau d\'humanisation',
            options: ['Léger', 'Modéré', 'Intense (Réécriture complète)'],
            default: 'Modéré'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'humanizedText' }
    ],
    promptTemplate: `Tu es un expert en humanisation de texte IA.

TEXTE ORIGINAL :
{{inputText}}

NIVEAU D'HUMANISATION : {{level}}

TÂCHE : Réécris ce texte pour qu'il paraisse 100% humain.

TRANSFORMATIONS À APPLIQUER :
1. Remplace les formulations typiques IA
2. Ajoute de la personnalité et des opinions
3. Varie les structures de phrases
4. Insère des expressions naturelles
5. Ajoute des connecteurs conversationnels
6. Rends le rythme plus naturel
7. Ajoute des touches d'humour si approprié

PRÉSERVE :
- Le sens original
- Les informations clés
- Le ton général demandé
- La structure logique

Retourne le texte humanisé uniquement.`,
    model: 'claude',
    estimatedTime: '30s',
    examples: []
};
