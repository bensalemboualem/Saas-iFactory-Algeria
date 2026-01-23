import { AITool } from '../../types';

export const toneChanger: AITool = {
    id: 'tone-changer',
    slug: 'tone-changer',
    name: { fr: 'Changeur de Ton', ar: 'مغير النبرة', en: 'Tone Changer' },
    description: { fr: 'Changez le ton de votre texte (ex: Formel → Amical) en un clic.', ar: 'غير نبرة نصك.', en: 'Change the tone of your text.' },
    category: 'blog',
    subcategory: 'rewriting',
    icon: 'Palette',
    credits: 10,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Texte à transformer', required: true },
        { name: 'current_tone', type: 'select', label: 'Ton actuel', options: ['Formel', 'Casual', 'Neutre', 'Technique', 'Inconnu'], default: 'Inconnu' },
        {
            name: 'target_tone', type: 'select', label: 'Ton souhaité', required: true, options: [
                'Professionnel', 'Conversationnel', 'Académique', 'Humoristique',
                'Inspirant', 'Urgent', 'Empathique', 'Autoritaire', 'Amical'
            ], default: 'Professionnel'
        },
        { name: 'preserve_length', type: 'boolean', label: 'Garder la même longueur', default: true }
    ],
    outputs: [{ type: 'markdown', name: 'rewrittenText' }],
    promptTemplate: `Transforme ce texte vers un nouveau ton tout en préservant le message.

TEXTE ORIGINAL :
{{content}}

TON ACTUEL : {{current_tone}}
TON CIBLE : {{target_tone}}
PRÉSERVER LONGUEUR : {{preserve_length}}

RÈGLES :
- Garde le sens et les informations intactes
- Adapte le vocabulaire au nouveau ton
- Modifie la structure des phrases si nécessaire
- Le résultat doit sembler naturel, pas forcé

Retourne uniquement le texte transformé.`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const sentenceRewriter: AITool = {
    id: 'sentence-rewriter',
    slug: 'sentence-rewriter',
    name: { fr: 'Réécriveur de Phrase', ar: 'معيد كتابة الجمل', en: 'Sentence Rewriter' },
    description: { fr: 'Obtenez plusieurs variantes d\'une même phrase pour trouver la formulation parfaite.', ar: 'احصل على صيغ متعددة لنفس الجملة.', en: 'Get multiple variations of the same sentence.' },
    category: 'blog',
    subcategory: 'rewriting',
    icon: 'RefreshCw',
    credits: 3,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'sentence', type: 'textarea', label: 'Phrase(s) à réécrire', required: true },
        {
            name: 'goal', type: 'select', label: 'Objectif', options: [
                'Clarifier', 'Simplifier', 'Enrichir', 'Raccourcir', 'Allonger', 'Varier structure'
            ], default: 'Clarifier'
        },
        { name: 'variations', type: 'number', label: 'Nombre de variations', default: 5 }
    ],
    outputs: [{ type: 'markdown', name: 'variations' }],
    promptTemplate: `Réécris cette phrase de {{variations}} manières différentes.

PHRASE ORIGINALE :
{{sentence}}

OBJECTIF : {{goal}}

Pour chaque variation :
- Garde le sens exact
- Applique l'objectif demandé
- Assure une grammaire parfaite
- Propose une structure différente

Variations :
1. ...
2. ...
...

Indique la meilleure version avec ✓`,
    model: 'gpt4',
    estimatedTime: '10s'
};
