import { AITool } from '../../types';

export const paraphrasingTool: AITool = {
    id: 'paraphrasing-tool',
    slug: 'paraphrasing-tool',
    name: {
        fr: 'Outil de Paraphrase',
        ar: 'أداة إعادة الصياغة',
        en: 'Paraphrasing Tool',
    },
    description: {
        fr: 'Reformulez des phrases ou paragraphes pour améliorer la clarté ou éviter la répétition.',
        ar: 'أعد صياغة الجمل أو الفقرات لتحسين الوضوح أو تجنب التكرار.',
        en: 'Rephrase sentences or paragraphs to improve clarity or avoid repetition.',
    },
    category: 'blog',
    subcategory: 'rewriting',
    icon: 'Repeat',
    credits: 5,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        {
            name: 'text',
            type: 'textarea',
            label: 'Texte à paraphraser',
            required: true
        },
        {
            name: 'tone',
            type: 'select',
            label: 'Ton souhaité',
            options: ['Standard', 'Fluide', 'Formel', 'Simple', 'Créatif'],
            default: 'Standard'
        }
    ],
    outputs: [
        { type: 'markdown', name: 'variations' }
    ],
    promptTemplate: `Propose 5 variations paraphrasées du texte suivant :
  
  "{{text}}"
  
  Ton : {{tone}}
  
  Format de sortie :
  1. [Variation 1]
  2. [Variation 2]
  ...
  
  Assure-toi que chaque variation a une structure différente mais garde le même sens.`,
    model: 'gpt4',
    estimatedTime: '10s',
    examples: []
};
