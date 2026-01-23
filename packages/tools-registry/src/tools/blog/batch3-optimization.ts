import { AITool } from '../../types';

export const blogMetaDescription: AITool = {
    id: 'blog-meta-description',
    slug: 'blog-meta-description',
    name: { fr: 'Meta Description Blog', ar: 'وصف الميتا للمدونة', en: 'Blog Meta Description' },
    description: { fr: 'Créez des méta-descriptions optimisées pour le CTR et le SEO.', ar: 'أنشئ أوصاف تعريفية محسنة.', en: 'Create optimized meta descriptions.' },
    category: 'blog',
    subcategory: 'optimization',
    icon: 'Tag',
    credits: 5,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'title', type: 'text', label: 'Titre de l\'article', required: true },
        { name: 'summary', type: 'textarea', label: 'Résumé du contenu (2-3 phrases)' },
        { name: 'keyword', type: 'text', label: 'Mot-clé principal', required: true },
        { name: 'cta_style', type: 'select', label: 'Style de CTA', options: ['Découvrez', 'Apprenez', 'Lisez', 'Téléchargez', 'Aucun'], default: 'Découvrez' }
    ],
    outputs: [{ type: 'markdown', name: 'metaDescriptions' }],
    promptTemplate: `Crée une meta description SEO optimale.

TITRE : {{title}}
RÉSUMÉ : {{summary}}
MOT-CLÉ : {{keyword}}
STYLE CTA : {{cta_style}}

RÈGLES STRICTES :
- Exactement 150-155 caractères (CRITIQUE pour SEO)
- Inclure le mot-clé naturellement
- Créer de la curiosité ou promettre une valeur
- Terminer par un CTA subtil si demandé
- Éviter les guillemets et caractères spéciaux

Génère 3 versions :
1. [XX caractères] : [meta description]
2. [XX caractères] : [meta description]  
3. [XX caractères] : [meta description]

Indique la meilleure avec ⭐`,
    model: 'gpt4',
    estimatedTime: '10s'
};

export const grammarChecker: AITool = {
    id: 'grammar-checker',
    slug: 'grammar-checker',
    name: { fr: 'Correcteur Grammatical', ar: 'مدقق نحوي', en: 'Grammar Checker' },
    description: { fr: 'Corrigez la grammaire, l\'orthographe et le style de vos textes.', ar: 'صحح قواعد اللغة والإملاء والأسلوب.', en: 'Correct grammar, spelling, and style.' },
    category: 'blog',
    subcategory: 'optimization',
    icon: 'CheckCheck',
    credits: 5,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'text', type: 'textarea', label: 'Texte à corriger', required: true },
        { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais'], default: 'Français' },
        { name: 'strictness', type: 'select', label: 'Niveau de correction', options: ['Erreurs uniquement', 'Style aussi', 'Perfectionniste'], default: 'Style aussi' },
        { name: 'explain', type: 'boolean', label: 'Expliquer les corrections', default: true }
    ],
    outputs: [{ type: 'markdown', name: 'correction' }],
    promptTemplate: `Corrige ce texte selon le niveau demandé.

TEXTE :
{{text}}

LANGUE : {{language}}
NIVEAU : {{strictness}}
EXPLICATIONS : {{explain}}

FORMAT DE RÉPONSE :

**TEXTE CORRIGÉ :**
[texte corrigé complet]

{{#if explain}}
**CORRECTIONS EFFECTUÉES :**
1. "[erreur]" → "[correction]" - Raison : ...
2. ...
{{/if}}

**STATISTIQUES :**
- Erreurs grammaticales : X
- Erreurs orthographe : X
- Améliorations style : X
- Score global : X/10`,
    model: 'gpt4',
    estimatedTime: '30s'
};

export const keywordExtractor: AITool = {
    id: 'keyword-extractor',
    slug: 'keyword-extractor',
    name: { fr: 'Extracteur de Mots-clés', ar: 'مستخرج الكلمات المفتاحية', en: 'Keyword Extractor' },
    description: { fr: 'Extrayez les mots-clés et sujets principaux de n\'importe quel texte.', ar: 'استخرج الكلمات المفتاحية والمواضيع الرئيسية.', en: 'Extract keywords and main topics.' },
    category: 'blog',
    subcategory: 'optimization',
    icon: 'Key',
    credits: 8,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Contenu à analyser', required: true },
        { name: 'keyword_count', type: 'number', label: 'Nombre de mots-clés', default: 15 },
        { name: 'include_longtail', type: 'boolean', label: 'Inclure longue traîne', default: true },
        { name: 'categorize', type: 'boolean', label: 'Catégoriser par type', default: true }
    ],
    outputs: [{ type: 'markdown', name: 'keywords' }],
    promptTemplate: `Analyse ce contenu et extrais les mots-clés SEO pertinents.

CONTENU :
{{content}}

NOMBRE : {{keyword_count}}
LONGUE TRAÎNE : {{include_longtail}}
CATÉGORISER : {{categorize}}

{{#if categorize}}
**🎯 Mot-clé principal :**
- [mot-clé] (volume estimé : X)

**📌 Mots-clés secondaires :**
1. [mot-clé] - Pertinence : ⭐⭐⭐
2. ...

**🔗 Longue traîne :**
1. [expression 3-5 mots]
2. ...

**🏷️ Entités/Noms propres :**
- ...
{{else}}
1. [mot-clé] - Type : [principal/secondaire/longtail]
2. ...
{{/if}}

**💡 Suggestions de mots-clés manquants :**
- ...`,
    model: 'gpt4',
    estimatedTime: '20s'
};
