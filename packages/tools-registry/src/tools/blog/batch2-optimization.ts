import { AITool } from '../../types';

export const paragraphGenerator: AITool = {
    id: 'paragraph-generator',
    slug: 'paragraph-generator',
    name: { fr: 'Générateur de Paragraphe', ar: 'مولد الفقرات', en: 'Paragraph Generator' },
    description: { fr: 'Rédigez des paragraphes parfaits pour enrichir vos articles.', ar: 'اكتب فقرات مثالية لإثراء مقالاتك.', en: 'Write perfect paragraphs to enrich your articles.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'AlignLeft',
    credits: 8,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet du paragraphe', required: true },
        { name: 'context', type: 'textarea', label: 'Contexte (paragraphe précédent...)' },
        { name: 'length', type: 'select', options: ['Court (50 mots)', 'Moyen (100 mots)', 'Long (200 mots)'], default: 'Moyen (100 mots)' },
        { name: 'purpose', type: 'select', options: ['Informer', 'Convaincre', 'Expliquer', 'Illustrer'], default: 'Informer' }
    ],
    outputs: [{ type: 'markdown', name: 'paragraph' }],
    promptTemplate: `Génère un paragraphe de qualité.

SUJET : {{topic}}
CONTEXTE : {{context}}
LONGUEUR : {{length}}
OBJECTIF : {{purpose}}

Le paragraphe doit :
- S'intégrer naturellement au contexte
- Avoir une phrase d'accroche
- Développer une idée principale
- Conclure avec transition

Écris de manière fluide et engageante.`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const contentExpander: AITool = {
    id: 'content-expander',
    slug: 'content-expander',
    name: { fr: 'Expandeur de Contenu', ar: 'موسع المحتوى', en: 'Content Expander' },
    description: { fr: 'Développez une phrase ou un paragraphe court en un contenu riche et détaillé.', ar: 'قم بتوسيع جملة أو فقرة قصيرة إلى محتوى غني ومفصل.', en: 'Expand a sentence or short paragraph into rich, detailed content.' },
    category: 'blog',
    subcategory: 'optimization',
    icon: 'Maximize',
    credits: 15,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Contenu à développer', required: true },
        { name: 'expansion_factor', type: 'select', label: 'Facteur d\'expansion', options: ['x2', 'x3', 'x4'], default: 'x2' },
        { name: 'add_elements', type: 'tags', label: 'Éléments à ajouter (exemples, stats, citations...)' }
    ],
    outputs: [{ type: 'markdown', name: 'expandedContent' }],
    promptTemplate: `Développe ce contenu en le rendant plus riche et détaillé.

CONTENU ORIGINAL :
{{content}}

EXPANSION : {{expansion_factor}}
ÉLÉMENTS À AJOUTER : {{add_elements}}

Instructions :
- Garde le message principal intact
- Ajoute de la profondeur, pas du remplissage
- Intègre les éléments demandés naturellement
- Améliore la clarté et l'engagement
- Varie les structures de phrases

Retourne le contenu développé uniquement.`,
    model: 'gpt4',
    estimatedTime: '30s'
};

export const blogSectionWriter: AITool = {
    id: 'blog-section-writer',
    slug: 'blog-section-writer',
    name: { fr: 'Rédacteur de Section', ar: 'كاتب القسم', en: 'Blog Section Writer' },
    description: { fr: 'Rédigez une section spécifique (H2/H3) de votre article.', ar: 'اكتب قسمًا محددًا (H2/H3) من مقالك.', en: 'Write a specific section (H2/H3) of your article.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'LayoutList',
    credits: 20,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'section_title', type: 'text', label: 'Titre H2/H3', required: true },
        { name: 'main_topic', type: 'text', label: 'Sujet principal de l\'article' },
        { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir' },
        { name: 'word_count', type: 'number', label: 'Nombre de mots', default: 300 }
    ],
    outputs: [{ type: 'markdown', name: 'section' }],
    promptTemplate: `Rédige une section complète pour un article de blog.

TITRE DE SECTION : {{section_title}}
ARTICLE PRINCIPAL : {{main_topic}}
POINTS À COUVRIR : {{key_points}}
LONGUEUR : {{word_count}} mots

Structure :
1. Phrase d'introduction de la section
2. Développement des points clés
3. Exemple ou illustration
4. Transition vers la section suivante

Écris de manière fluide, comme partie d'un article cohérent.`,
    model: 'gpt4',
    estimatedTime: '40s'
};

export const contentBriefGenerator: AITool = {
    id: 'content-brief-generator',
    slug: 'content-brief-generator',
    name: { fr: 'Brief de Contenu', ar: 'ملخص المحتوى', en: 'Content Brief Generator' },
    description: { fr: 'Générez des briefs détaillés pour vos rédacteurs.', ar: 'أنشئ ملخصات مفصلة وكتابك.', en: 'Generate detailed briefs for your writers.' },
    category: 'blog',
    subcategory: 'ideation',
    icon: 'FileText',
    credits: 25,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet', required: true },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible' },
        { name: 'competitors', type: 'textarea', label: 'URLs concurrents (optionnel)' },
        { name: 'brand_voice', type: 'select', options: ['Corporate', 'Startup', 'Expert', 'Amical'], default: 'Expert' }
    ],
    outputs: [{ type: 'markdown', name: 'brief' }],
    promptTemplate: `Crée un brief de contenu détaillé pour un rédacteur.

SUJET : {{topic}}
MOT-CLÉ : {{target_keyword}}
CONCURRENTS : {{competitors}}
VOIX : {{brand_voice}}

BRIEF À GÉNÉRER :
1. Objectif de l'article
2. Persona cible
3. Intention de recherche
4. Mot-clé principal + secondaires (10)
5. Questions à répondre (People Also Ask)
6. Structure recommandée (H1, H2, H3)
7. Points obligatoires à couvrir
8. Points à éviter
9. Ton et style
10. CTA suggéré
11. Liens internes à inclure
12. Sources recommandées
13. Longueur cible

Ce brief doit permettre à n'importe quel rédacteur de produire un excellent article.`,
    model: 'gpt4',
    estimatedTime: '45s'
};

export const pillarContent: AITool = {
    id: 'pillar-content',
    slug: 'pillar-content',
    name: { fr: 'Contenu Pilier', ar: 'محتوى أساسي', en: 'Pillar Content' },
    description: { fr: 'Créez des articles piliers massifs (3000m+) pour dominer une thématique.', ar: 'أنشئ مقالات أساسية ضخمة للسيطرة على موضوع ما.', en: 'Create massive pillar articles to dominate a topic.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Building2',
    credits: 80,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'main_topic', type: 'text', label: 'Sujet principal', required: true },
        { name: 'subtopics', type: 'tags', label: 'Sous-sujets à couvrir' },
        { name: 'word_count', type: 'number', default: 5000 },
        { name: 'cluster_articles', type: 'textarea', label: 'Articles du cluster à lier' }
    ],
    outputs: [{ type: 'markdown', name: 'pillarArticle' }],
    promptTemplate: `Crée un article pilier exhaustif (cornerstone content).

SUJET PRINCIPAL : {{main_topic}}
SOUS-SUJETS : {{subtopics}}
LONGUEUR : {{word_count}} mots
ARTICLES DU CLUSTER : {{cluster_articles}}

C'est un article de référence qui doit :
1. Couvrir le sujet de A à Z
2. Être la ressource #1 sur ce sujet
3. Lier vers tous les articles du cluster
4. Attirer des backlinks naturellement

STRUCTURE :
1. Titre définitif : "Le Guide Ultime de {{main_topic}} [2025]"
2. Table des matières cliquable
3. Introduction complète (qu'est-ce que, pourquoi important)
4. Section pour chaque sous-sujet avec :
   - Explication approfondie
   - Lien vers l'article cluster dédié
5. FAQ exhaustive
6. Conclusion + ressources
7. Schema markup suggéré

Qualité encyclopédique + optimisation SEO parfaite.`,
    model: 'claude',
    estimatedTime: '180s'
};

export const newsArticleWriter: AITool = {
    id: 'news-article-writer',
    slug: 'news-article-writer',
    name: { fr: 'Article d\'Actualité', ar: 'مقال إخباري', en: 'News Article Writer' },
    description: { fr: 'Transformez un fait ou une dépêche en article d\'actualité journalistique.', ar: 'حول حقيقة أو برقية إلى مقال إخباري صحفي.', en: 'Turn a fact or wire into a journalistic news article.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Newspaper',
    credits: 30,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'headline', type: 'text', label: 'Titre/Fait principal', required: true },
        { name: 'details', type: 'textarea', label: 'Détails connus', required: true },
        { name: 'sources', type: 'textarea', label: 'Sources (citations...)' },
        { name: 'angle', type: 'select', options: ['Factuel', 'Analyse', 'Opinion', 'Investigation'], default: 'Factuel' }
    ],
    outputs: [{ type: 'markdown', name: 'newsArticle' }],
    promptTemplate: `Rédige un article d'actualité professionnel.

FAIT PRINCIPAL : {{headline}}
DÉTAILS : {{details}}
SOURCES : {{sources}}
ANGLE : {{angle}}

STRUCTURE PYRAMIDE INVERSÉE :
1. Titre accrocheur
2. Chapô (qui, quoi, où, quand, pourquoi - 2 phrases)
3. Développement par ordre d'importance décroissante
4. Contexte et background
5. Réactions et citations
6. Perspectives et suite
7. Encadré "À retenir" (bullet points)

Style journalistique : phrases courtes, faits vérifiés, objectivité.`,
    model: 'gpt4',
    estimatedTime: '60s'
};

export const blogIdeasFromUrl: AITool = {
    id: 'blog-ideas-from-url',
    slug: 'blog-ideas-from-url',
    name: { fr: 'Idées depuis URL', ar: 'أفكار من رابط', en: 'Blog Ideas from URL' },
    description: { fr: 'Analysez une page web existante pour générer de nouvelles idées de contenu.', ar: 'حلل صفحة ويب موجودة لتوليد أفكار محتوى جديدة.', en: 'Analyze an existing web page to generate new content ideas.' },
    category: 'blog',
    subcategory: 'ideation',
    icon: 'Link',
    credits: 15,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'url_content', type: 'textarea', label: 'Colle le contenu de l\'URL', required: true },
        { name: 'ideas_count', type: 'number', label: 'Nombre d\'idées', default: 10 },
        { name: 'content_type', type: 'text', label: 'Types souhaités (Article, Guide...)' } // Simpler than multiselect for now
    ],
    outputs: [{ type: 'markdown', name: 'ideas' }],
    promptTemplate: `Analyse ce contenu et génère des idées d'articles connexes.

CONTENU SOURCE :
{{url_content}}

NOMBRE D'IDÉES : {{ideas_count}}
TYPES SOUHAITÉS : {{content_type}}

Pour chaque idée, fournis :
1. Titre optimisé SEO
2. Type de contenu
3. Angle unique (comment se différencier)
4. Mots-clés cibles
5. Intention de recherche
6. Potentiel (1-5 étoiles)

Propose des angles originaux, pas des copies.`,
    model: 'gpt4',
    estimatedTime: '30s'
};
