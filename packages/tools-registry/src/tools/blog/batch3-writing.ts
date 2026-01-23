import { AITool } from '../../types';

export const blogIntroHook: AITool = {
    id: 'blog-intro-hook',
    slug: 'blog-intro-hook',
    name: { fr: 'Accroche d\'Introduction', ar: 'خطاف المقدمة', en: 'Blog Intro Hook' },
    description: { fr: 'Générez des accroches percutantes pour captiver vos lecteurs dès la première phrase.', ar: 'أنشئ خطافات قوية لجذب انتباه القراء.', en: 'Generate powerful hooks to captivate your readers.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Anchor',
    credits: 5,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet de l\'article', required: true },
        {
            name: 'hook_type', type: 'select', label: 'Type d\'accroche', required: true, options: [
                'Question choc', 'Statistique surprenante', 'Anecdote', 'Citation',
                'Problème/Douleur', 'Promesse bénéfice', 'Contre-intuitive', 'Histoire'
            ], default: 'Question choc'
        },
        { name: 'audience', type: 'text', label: 'Public cible' }
    ],
    outputs: [{ type: 'markdown', name: 'hook' }],
    promptTemplate: `Crée une accroche d'introduction percutante (1-2 phrases max).

SUJET : {{topic}}
TYPE D'ACCROCHE : {{hook_type}}
PUBLIC : {{audience}}

L'accroche doit :
- Capturer l'attention en 3 secondes
- Créer une tension ou curiosité
- Donner envie de lire la suite
- Être mémorable

Génère 5 accroches différentes du type demandé :
1. ...
2. ...
3. ...
4. ...
5. ...

Indique la plus impactante avec 🔥`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const textCompleter: AITool = {
    id: 'text-completer',
    slug: 'text-completer',
    name: { fr: 'Compléteur de Texte', ar: 'مكمل النص', en: 'Text Completer' },
    description: { fr: 'Complétez automatiquement vos phrases ou paragraphes en panne d\'inspiration.', ar: 'أكمل جملك أو فقراتك تلقائيًا.', en: 'Automatically complete your sentences or paragraphs.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'PenLine',
    credits: 8,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'text_start', type: 'textarea', label: 'Début du texte', required: true },
        { name: 'direction', type: 'textarea', label: 'Direction souhaitée (optionnel)', placeholder: 'Parle ensuite de...' },
        { name: 'length', type: 'select', label: 'Longueur à ajouter', options: ['1 phrase', '1 paragraphe', '2 paragraphes', '3 paragraphes'], default: '1 paragraphe' },
        { name: 'style', type: 'select', options: ['Même style', 'Plus formel', 'Plus casual'], default: 'Même style' }
    ],
    outputs: [{ type: 'markdown', name: 'completedText' }],
    promptTemplate: `Continue ce texte de manière naturelle et cohérente.

TEXTE EXISTANT :
{{text_start}}

DIRECTION : {{direction}}
LONGUEUR À AJOUTER : {{length}}
STYLE : {{style}}

Instructions :
- Maintiens le même ton et style (sauf si demandé autrement)
- Assure une transition fluide
- Reste cohérent avec le contexte
- Ne répète pas les idées déjà présentes

[Suite du texte...]`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const bulletPointGenerator: AITool = {
    id: 'bullet-point-generator',
    slug: 'bullet-point-generator',
    name: { fr: 'Générateur de Puces', ar: 'مولد النقاط', en: 'Bullet Point Generator' },
    description: { fr: 'Transformez vos paragraphes en listes à puces claires et lisibles.', ar: 'حول فقراتك إلى قوائم نقطية واضحة.', en: 'Turn your paragraphs into clear bullet lists.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'List',
    credits: 5,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Contenu à transformer', required: true },
        { name: 'bullet_count', type: 'number', label: 'Nombre de puces', default: 5 },
        { name: 'style', type: 'select', label: 'Style', options: ['Concis', 'Détaillé', 'Actionnable', 'Bénéfices'], default: 'Concis' },
        { name: 'format', type: 'select', options: ['Puces simples', 'Puces titrées', 'Numérotées'], default: 'Puces simples' }
    ],
    outputs: [{ type: 'markdown', name: 'bullets' }],
    promptTemplate: `Transforme ce contenu en liste à puces claire et impactante.

CONTENU :
{{content}}

NOMBRE DE PUCES : {{bullet_count}}
STYLE : {{style}}
FORMAT : {{format}}

Règles :
- Extrais les points essentiels
- Une idée par puce
- Commence par un verbe d'action si style "actionnable"
- Parallélisme grammatical entre les puces
- Ordre logique (importance ou chronologie)

[Liste générée...]`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const prosConsGenerator: AITool = {
    id: 'pros-cons-generator',
    slug: 'pros-cons-generator',
    name: { fr: 'Générateur Pour/Contre', ar: 'مولد الإيجابيات والسلبيات', en: 'Pros & Cons Generator' },
    description: { fr: 'Générez une analyse des avantages et inconvénients pour n\'importe quel sujet.', ar: 'أنشئ تحليلًا للمزايا والعيوب.', en: 'Generate a pros and cons analysis.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Scale',
    credits: 10,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'subject', type: 'text', label: 'Sujet à analyser', required: true },
        { name: 'context', type: 'textarea', label: 'Contexte (pour qui, quel usage...)' },
        { name: 'count', type: 'number', label: 'Nombre de points par côté', default: 5 },
        { name: 'format', type: 'select', options: ['Liste simple', 'Tableau', 'Détaillé'], default: 'Tableau' }
    ],
    outputs: [{ type: 'markdown', name: 'prosCons' }],
    promptTemplate: `Génère une analyse Pour/Contre équilibrée et honnête.

SUJET : {{subject}}
CONTEXTE : {{context}}
POINTS PAR CÔTÉ : {{count}}

{{#if format === 'tableau'}}
| ✅ Avantages | ❌ Inconvénients |
|-------------|-----------------|
| ... | ... |
{{else}}
**✅ AVANTAGES :**
1. [Point] - [Explication courte]
...

**❌ INCONVÉNIENTS :**
1. [Point] - [Explication courte]
...
{{/if}}

**VERDICT :**
[Pour qui c'est recommandé / Pour qui ça ne l'est pas]

Sois objectif et honnête, pas promotionnel.`,
    model: 'gpt4',
    estimatedTime: '30s'
};

export const faqAnswers: AITool = {
    id: 'faq-answers',
    slug: 'faq-answers',
    name: { fr: 'Réponses FAQ', ar: 'إجابات الأسئلة الشائعة', en: 'FAQ Answers' },
    description: { fr: 'Obtenez des réponses précises et optimisées pour vos questions FAQ.', ar: 'احصل على إجابات دقيقة ومحسنة.', en: 'Get precise and optimized answers for your FAQ questions.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'MessageCircleQuestion',
    credits: 8,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'questions', type: 'textarea', label: 'Questions (une par ligne)', required: true },
        { name: 'topic_context', type: 'text', label: 'Contexte/Sujet général' },
        { name: 'answer_length', type: 'select', label: 'Longueur réponses', options: ['Courte (30 mots)', 'Moyenne (60 mots)', 'Détaillée (100 mots)'], default: 'Courte (30 mots)' },
        { name: 'include_schema', type: 'boolean', label: 'Générer Schema JSON-LD', default: false }
    ],
    outputs: [{ type: 'markdown', name: 'faqAnswers' }],
    promptTemplate: `Réponds à ces questions FAQ de manière claire et utile.

QUESTIONS :
{{questions}}

CONTEXTE : {{topic_context}}
LONGUEUR : {{answer_length}}

Pour chaque question :
**Q : [Question]**
**R :** [Réponse directe et complète]

Règles :
- Réponds directement (pas de "Bonne question!")
- Sois factuel et précis
- Inclus un exemple si utile
- Optimise pour les featured snippets Google

{{#if include_schema}}
---
**Schema FAQ JSON-LD :**
\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}
\`\`\`
{{/if}}`,
    model: 'gpt4',
    estimatedTime: '30s'
};
