import { AITool } from '../../types';

export const metaTagGenerator: AITool = {
    id: 'meta-tag-generator',
    slug: 'meta-tag-generator',
    name: { fr: 'Générateur de Meta Tags', ar: 'مولد الوسوم الوصفية', en: 'Meta Tag Generator' },
    description: { fr: 'Générez des balises meta optimisées pour améliorer votre classement.', ar: 'أنشئ وسوم تعريفية محسنة.', en: 'Generate optimized meta tags.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Code',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'page_title', type: 'text', label: 'Titre de la page', required: true },
        { name: 'page_content', type: 'textarea', label: 'Contenu/Description de la page', required: true },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé principal', required: true },
        { name: 'secondary_keywords', type: 'tags', label: 'Mots-clés secondaires' },
        { name: 'page_type', type: 'select', options: ['Homepage', 'Article', 'Product', 'Category', 'Service', 'Landing'], default: 'Article' }
    ],
    outputs: [{ type: 'markdown', name: 'metaTags' }],
    promptTemplate: `Génère des meta tags SEO optimisés.

PAGE : {{page_title}}
CONTENU : {{page_content}}
MOT-CLÉ PRINCIPAL : {{target_keyword}}
MOTS-CLÉS SECONDAIRES : {{secondary_keywords}}
TYPE : {{page_type}}

GÉNÈRE :

1. META TITLE (60 caractères max)
   - Inclure le mot-clé au début
   - Ajouter un élément accrocheur
   - Format : [Mot-clé] - [Bénéfice] | [Marque]

2. META DESCRIPTION (155 caractères max)
   - Inclure le mot-clé naturellement
   - Ajouter un CTA
   - Créer de la curiosité

3. OG TAGS (Open Graph)
   - og:title
   - og:description
   - og:type

4. TWITTER CARDS
   - twitter:title
   - twitter:description

5. BALISES SUPPLÉMENTAIRES
   - canonical suggéré
   - robots (index/noindex)

Fournis le code HTML complet prêt à copier.`,
    model: 'gpt4',
    estimatedTime: '30s'
};

export const keywordGenerator: AITool = {
    id: 'keyword-generator',
    slug: 'keyword-generator',
    name: { fr: 'Générateur de Mots-clés', ar: 'مولد الكلمات المفتاحية', en: 'Keyword Generator' },
    description: { fr: 'Trouvez les meilleurs mots-clés pour votre niche (volume, difficulté).', ar: 'اعثر على أفضل الكلمات المفتاحية.', en: 'Find best keywords for your niche.' },
    category: 'seo',
    subcategory: 'research',
    icon: 'Search',
    credits: 15,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'seed_keyword', type: 'text', label: 'Mot-clé de base', required: true },
        { name: 'industry', type: 'text', label: 'Secteur d\'activité' },
        { name: 'location', type: 'text', label: 'Localisation', default: 'Algérie' },
        { name: 'language', type: 'select', options: ['Français', 'Arabe', 'Anglais', 'Darija'], default: 'Français' },
        { name: 'intent', type: 'tags', label: 'Intentions (info, transac...)' }
    ],
    outputs: [{ type: 'markdown', name: 'keywords' }],
    promptTemplate: `Génère une liste complète de mots-clés SEO.

MOT-CLÉ DE BASE : {{seed_keyword}}
SECTEUR : {{industry}}
LOCALISATION : {{location}}
LANGUE : {{language}}
INTENTIONS : {{intent}}

GÉNÈRE 50 MOTS-CLÉS organisés par :

1. MOTS-CLÉS PRINCIPAUX (5)
   - Volume estimé : Élevé
   - Difficulté : Haute
   - Format : [mot-clé] | [intention] | [difficulté]

2. MOTS-CLÉS LONGUE TRAÎNE (20)
   - Questions (comment, pourquoi, quand...)
   - Comparaisons (vs, ou, meilleur)
   - Locaux ({{location}})

3. MOTS-CLÉS LSI/SÉMANTIQUES (15)
   - Termes associés
   - Synonymes
   - Concepts liés

4. MOTS-CLÉS COMMERCIAUX (10)
   - "acheter", "prix", "pas cher"
   - "meilleur", "avis", "comparatif"

Pour chaque mot-clé, indique :
- Intention de recherche
- Difficulté estimée (1-10)
- Priorité recommandée`,
    model: 'gpt4',
    estimatedTime: '60s'
};

export const longtailKeywordGenerator: AITool = {
    id: 'longtail-keyword-generator',
    slug: 'longtail-keyword-generator',
    name: { fr: 'Mots-clés Longue Traîne', ar: 'كلمات مفتاحية طويلة', en: 'Long-tail Keywords' },
    description: { fr: 'Ciblez des mots-clés moins concurrentiels et plus précis.', ar: 'استهدف كلمات مفتاحية أقل تنافسية.', en: 'Target less competitive keywords.' },
    category: 'seo',
    subcategory: 'research',
    icon: 'TrendingUp',
    credits: 12,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'main_keyword', type: 'text', label: 'Mot-clé principal', required: true },
        { name: 'count', type: 'number', label: 'Nombre de suggestions', default: 30 },
        { name: 'include_questions', type: 'boolean', label: 'Inclure les questions', default: true },
        { name: 'include_local', type: 'boolean', label: 'Inclure variantes locales (Algérie)', default: false }
    ],
    outputs: [{ type: 'markdown', name: 'longtailKeywords' }],
    promptTemplate: `Génère des mots-clés longue traîne à faible concurrence.

MOT-CLÉ : {{main_keyword}}
NOMBRE : {{count}}
QUESTIONS : {{include_questions}}
LOCAL ALGÉRIE : {{include_local}}

CATÉGORIES À COUVRIR :

1. QUESTIONS ({{#if include_questions}}15{{else}}0{{/if}})
   - Comment [mot-clé]...
   - Pourquoi [mot-clé]...
   - Quand [mot-clé]...
   - Où [mot-clé]...
   - Quel/Quelle [mot-clé]...

2. COMPARAISONS (5)
   - [mot-clé] vs [alternative]
   - [mot-clé] ou [alternative]
   - différence entre [mot-clé] et...

3. SPÉCIFIQUES (5)
   - [mot-clé] pour [audience spécifique]
   - [mot-clé] [année]
   - [mot-clé] gratuit/pas cher

4. LOCAUX ALGÉRIE ({{#if include_local}}5{{else}}0{{/if}})
   - [mot-clé] Algérie
   - [mot-clé] Alger/Oran/Constantine
   - [mot-clé] en DZD

Format tableau :
| Mot-clé | Volume estimé | Difficulté | Intention |`,
    model: 'gpt4',
    estimatedTime: '45s'
};

export const metaDescriptionGenerator: AITool = {
    id: 'meta-description-generator',
    slug: 'meta-description-generator',
    name: { fr: 'Générateur de Meta Description', ar: 'مولد الوصف الميتا', en: 'Meta Description Generator' },
    description: { fr: 'Augmentez votre CTR avec des descriptions irrésistibles.', ar: 'زد معدل النقر مع أوصاف لا تقاوم.', en: 'Increase CTR with irresistible descriptions.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'FileText',
    credits: 8,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'page_title', type: 'text', label: 'Titre de la page', required: true },
        { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true },
        { name: 'page_type', type: 'select', options: ['Article', 'Produit', 'Service', 'Accueil', 'Catégorie'], default: 'Article' },
        { name: 'usp', type: 'text', label: 'Argument clé / USP' },
        { name: 'cta', type: 'select', label: 'Type de CTA', options: ['Découvrir', 'Acheter', 'Apprendre', 'Télécharger', 'Contacter'], default: 'Découvrir' }
    ],
    outputs: [{ type: 'markdown', name: 'metaDescriptions' }],
    promptTemplate: `Génère 5 meta descriptions optimisées pour le CTR.

PAGE : {{page_title}}
MOT-CLÉ : {{keyword}}
TYPE : {{page_type}}
USP : {{usp}}
CTA : {{cta}}

RÈGLES :
- 150-155 caractères exactement
- Mot-clé dans les 70 premiers caractères
- Inclure un bénéfice clair
- Terminer par un CTA
- Utiliser des power words (découvrez, gratuit, exclusif...)
- Créer de l'urgence ou curiosité

GÉNÈRE 5 VERSIONS :

1. [Version bénéfice] - Focus sur ce que l'utilisateur gagne
2. [Version curiosité] - Crée l'envie de cliquer
3. [Version urgence] - Sentiment d'opportunité
4. [Version sociale] - Preuve sociale si pertinent
5. [Version directe] - Droit au but

Pour chaque version :
- Meta description
- Nombre de caractères
- Score CTR estimé (1-10)`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const seoContentOptimizer: AITool = {
    id: 'seo-content-optimizer',
    slug: 'seo-content-optimizer',
    name: { fr: 'Optimiseur de Contenu SEO', ar: 'محسن محتوى SEO', en: 'SEO Content Optimizer' },
    description: { fr: 'Analysez et optimisez votre contenu pour le référencement naturel.', ar: 'حلل وحسن المحتوى الخاص بك لمحركات البحث.', en: 'Analyze and optimize content for SEO.' },
    category: 'seo',
    subcategory: 'optimization',
    icon: 'Gauge',
    credits: 25,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Contenu à optimiser', required: true },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true },
        { name: 'secondary_keywords', type: 'tags', label: 'Mots-clés secondaires' },
        { name: 'competitor_url', type: 'text', label: 'URL concurrent (optionnel)' }
    ],
    outputs: [{ type: 'markdown', name: 'optimizationReport' }],
    promptTemplate: `Analyse et optimise ce contenu pour le SEO.

CONTENU :
{{content}}

MOT-CLÉ PRINCIPAL : {{target_keyword}}
MOTS-CLÉS SECONDAIRES : {{secondary_keywords}}

ANALYSE ET RECOMMANDATIONS :

1. SCORE SEO ACTUEL : X/100

2. DENSITÉ DES MOTS-CLÉS
   - {{target_keyword}} : X% (optimal : 1-2%)
   - Recommandation : [ajouter/réduire]

3. STRUCTURE
   - ✅/❌ Mot-clé dans le H1
   - ✅/❌ Mot-clé dans le premier paragraphe
   - ✅/❌ Mot-clé dans au moins 1 H2
   - ✅/❌ Mot-clé dans la conclusion

4. LISIBILITÉ
   - Score Flesch : X
   - Longueur moyenne des phrases
   - Recommandations

5. ÉLÉMENTS MANQUANTS
   - [ ] Mots-clés LSI à ajouter
   - [ ] Questions à inclure (PAA)
   - [ ] Liens internes suggérés

6. VERSION OPTIMISÉE
   [Contenu réécrit avec optimisations]

7. CHECKLIST FINALE
   □ Title tag optimisé
   □ Meta description
   □ URL slug
   □ Alt text images`,
    model: 'claude',
    estimatedTime: '120s'
};

export const competitorKeywordAnalyzer: AITool = {
    id: 'competitor-keyword-analyzer',
    slug: 'competitor-keyword-analyzer',
    name: { fr: 'Analyseur de Concurrents', ar: 'محلل المنافسين', en: 'Competitor Analyzer' },
    description: { fr: 'Espionnez les mots-clés et stratégies de vos concurrents.', ar: 'تجسس على كلمات واستراتيجيات منافسيك.', en: 'Spy on competitor keywords and strategies.' },
    category: 'seo',
    subcategory: 'research',
    icon: 'Users',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'competitor_content', type: 'textarea', label: 'Contenu du concurrent (copier-coller)', required: true },
        { name: 'competitor_url', type: 'text', label: 'URL du concurrent' },
        { name: 'your_keyword', type: 'text', label: 'Votre mot-clé cible' }
    ],
    outputs: [{ type: 'markdown', name: 'competitorAnalysis' }],
    promptTemplate: `Analyse le contenu concurrent et trouve des opportunités.

CONTENU CONCURRENT :
{{competitor_content}}

URL : {{competitor_url}}
VOTRE MOT-CLÉ : {{your_keyword}}

ANALYSE :

1. MOTS-CLÉS UTILISÉS
   - Principal détecté : [X]
   - Secondaires : [liste]
   - Densité : X%

2. STRUCTURE DU CONTENU
   - Nombre de mots : X
   - Nombre de H2 : X
   - Nombre de H3 : X
   - Images : X
   - Liens externes : X

3. POINTS FORTS À COPIER
   - [ce qu'ils font bien]

4. FAIBLESSES À EXPLOITER
   - [ce qui manque chez eux]

5. OPPORTUNITÉS DE CONTENU
   - Sujets non couverts
   - Questions sans réponse
   - Angles uniques possibles

6. STRATÉGIE RECOMMANDÉE
   Pour les battre sur "{{your_keyword}}" :
   - Longueur cible : X mots
   - Sections à inclure
   - Éléments différenciants`,
    model: 'gpt4',
    estimatedTime: '60s'
};

export const schemaMarkupGenerator: AITool = {
    id: 'schema-markup-generator',
    slug: 'schema-markup-generator',
    name: { fr: 'Générateur de Schema Markup', ar: 'مولد Schema', en: 'Schema Markup Generator' },
    description: { fr: 'Générez facilement des données structurées pour les Rich Snippets.', ar: 'أنشئ بيانات منظمة بسهولة.', en: 'Easily generate structured data for Rich Snippets.' },
    category: 'seo',
    subcategory: 'technical',
    icon: 'Braces',
    credits: 15,
    priority: 'critical',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'schema_type', type: 'select', label: 'Type de Schema', required: true, options: ['Article', 'Product', 'LocalBusiness', 'FAQ', 'HowTo', 'Recipe', 'Event', 'Organization', 'Person', 'Review'], default: 'Article' },
        { name: 'content_data', type: 'textarea', label: 'Informations à structurer', required: true },
        { name: 'website_name', type: 'text', label: 'Nom du site' },
        { name: 'website_url', type: 'text', label: 'URL du site' }
    ],
    outputs: [{ type: 'markdown', name: 'schemaMarkup' }],
    promptTemplate: `Génère le Schema Markup JSON-LD.

TYPE : {{schema_type}}
DONNÉES : {{content_data}}
SITE : {{website_name}}
URL : {{website_url}}

GÉNÈRE :

1. CODE JSON-LD COMPLET
\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "{{schema_type}}",
  // ... propriétés complètes
}
\`\`\`

2. INSTRUCTIONS D'IMPLÉMENTATION
   - Où placer le code
   - Comment tester (Rich Results Test)

3. PROPRIÉTÉS RECOMMANDÉES
   - Obligatoires : ✅
   - Optionnelles recommandées : ⭐
   - Bonus pour rich snippets : 🎯

4. VALIDATION
   - Erreurs potentielles
   - Avertissements à éviter

Le code doit passer le test Google Rich Results.`,
    model: 'gpt4',
    estimatedTime: '30s'
};
