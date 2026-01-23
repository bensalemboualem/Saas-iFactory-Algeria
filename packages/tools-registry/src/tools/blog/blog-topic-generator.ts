import { AITool } from '../../types';

export const blogTopicGenerator: AITool = {
    id: 'blog-topic-generator', // Note: This ID updates the existing placeholder
    slug: 'blog-topic-generator',
    name: {
        fr: 'Générateur d\'Idées de Sujets',
        ar: 'مولد أفكار الموضوعات',
        en: 'Blog Topic Generator',
    },
    description: {
        fr: 'Trouvez des idées de sujets viraux et pertinents pour votre niche.',
        ar: 'ابحث عن أفكار موضوعات فيروسية وذات صلة بمجالك.',
        en: 'Find viral and relevant topic ideas for your niche.',
    },
    category: 'blog',
    subcategory: 'ideation',
    icon: 'Lightbulb',
    credits: 5,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'niche', type: 'text', label: 'Niche / Thématique', required: true },
        { name: 'audience', type: 'text', label: 'Audience cible', required: false }
    ],
    outputs: [
        { type: 'markdown', name: 'ideas' }
    ],
    promptTemplate: `Génère 10 idées de sujets de blog viraux pour la niche : {{niche}}.
      Audience cible : {{audience}}.
      
      Pour chaque idée :
      1. Titre provisoire
      2. Pourquoi c'est intéressant (Potentiel de trafic)
      3. Angle d'attaque suggéré
      4. Difficulté estimée (Faible/Moyenne/Haute)`,
    model: 'gpt4',
    estimatedTime: '15s',
    examples: []
};
