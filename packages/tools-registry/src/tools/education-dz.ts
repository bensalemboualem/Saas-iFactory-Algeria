import { AITool } from '../types';

export const educationDzTools: AITool[] = [
    {
        id: 'bac-dz-revision',
        slug: 'revision-bac-algerie',
        name: {
            fr: 'Coach Bac Algérie',
            ar: 'مدرب البكالوريا الجزائرية',
            en: 'Algeria Bac Coach'
        },
        description: {
            fr: 'Générez des fiches de révision et exercices conformes au programme du Bac algérien.',
            ar: 'أنشئ بطاقات مراجعة وتمارين متوافقة مع برنامج البكالوريا الجزائري.',
            en: 'Generate revision sheets and exercises compliant with the Algerian Bac program.'
        },
        category: 'education-dz',
        credits: 25,
        priority: 'critical',
        isAlgeriaExclusive: true,
        icon: 'GraduationCap',
        inputs: [
            { name: 'filiere', type: 'select', label: 'Filière', options: ['Sciences Expérimentales', 'Mathématiques', 'Technique Math', 'Gestion & Économie', 'Lettres & Philo', 'Langues Étrangères'] },
            { name: 'matiere', type: 'select', label: 'Matière', options: ['Mathématiques', 'Physique', 'Sciences (SNV)', 'Arabe', 'Français', 'Anglais', 'Histoire-Géo', 'Philosophie'] },
            { name: 'chapitre', type: 'text', label: 'Chapitre / Leçon', required: true },
            { name: 'type_contenu', type: 'select', label: 'Je veux...', options: ['Fiche de révision', 'Série d\'exercices', 'QCM', 'Sujet type Bac', 'Conseils méthodologiques'] }
        ],
        outputs: [{ type: 'markdown', name: 'content' }],
        promptTemplate: `Tu es un professeur algérien expert préparant les élèves au Baccalauréat.
    
    Filière : {{filiere}}
    Matière : {{matiere}}
    Chapitre : {{chapitre}}
    Type de contenu souhaité : {{type_contenu}}
    
    Génère du contenu pédagogique de haute qualité, strictement conforme au programme officiel du Ministère de l'Éducation Nationale algérien.
    Utilise la terminologie exacte (français ou arabe selon la matière).
    Si exercice, fournis le corrigé détaillé à la fin.`,
        model: 'gpt4' // Better reasoning for education
    }
];
