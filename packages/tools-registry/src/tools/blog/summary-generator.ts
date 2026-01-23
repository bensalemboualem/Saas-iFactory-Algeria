import { AITool } from '../../types';

export const summaryGenerator: AITool = {
    id: 'summary-generator',
    slug: 'summary-generator',
    name: {
        fr: 'Générateur de Résumés',
        ar: 'مولد الملخصات',
        en: 'Summary Generator',
    },
    description: {
        fr: 'Résumez n\'importe quel texte en points clés essentiels.',
        ar: 'لخص أي نص إلى نقاط رئيسية أساسية.',
        en: 'Summarize any text into essential key points.',
    },
    category: 'blog',
    subcategory: 'summary',
    icon: 'FileMinus',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'text',
            type: 'textarea',
            label: 'Texte à résumer',
            placeholder: 'Collez votre texte long ici...',
            required: true
        },
        {
            name: 'length',
            type: 'select',
            label: 'Longueur du résumé',
            options: ['Court (1 phrase)', 'Moyen (1 paragraphe)', 'Détaillé (Liste à puces)'],
            default: 'Moyen'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'summary' }
    ],
    promptTemplate: `Résume le texte suivant :

  {{text}}
  
  FORMAT CIBLE : {{length}}
  
  Instructions :
  - Capture l'idée principale
  - Ignore les détails superflus
  - Utilise un langage clair et concis
  - Si "Détaillé", utilise des listes à puces.`,
    model: 'claude',
    estimatedTime: '15s',
    examples: []
};
