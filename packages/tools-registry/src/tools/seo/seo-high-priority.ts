import { AITool } from '../../types';

export const titleTagOptimizer: AITool = {
    id: 'title-tag-optimizer',
    slug: 'title-tag-optimizer',
    name: { fr: 'Optimiseur de Title Tag', ar: 'محسن عنوان الصفحة', en: 'Title Tag Optimizer' },
    description: { fr: 'Créez des titres de page parfaits pour le SEO et l\'engagement.', ar: 'أنشئ عناوين صفحات مثالية.', en: 'Create perfect page titles.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Type',
    credits: 8,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'current_title', type: 'text', label: 'Title actuel (optionnel)' },
        { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true },
        { name: 'brand', type: 'text', label: 'Nom de marque' },
        { name: 'page_type', type: 'select', options: ['Article', 'Produit', 'Service', 'Accueil'], default: 'Article' }
    ],
    outputs: [{ type: 'markdown', name: 'optimizedTitles' }],
    promptTemplate: `Optimise ou crée un Title Tag parfait.

TITLE ACTUEL : {{current_title}}
MOT-CLÉ : {{keyword}}
MARQUE : {{brand}}
TYPE : {{page_type}}

RÈGLES :
- 50-60 caractères (idéal : 55)
- Mot-clé au début
- Marque à la fin (si place)
- Power words pour le CTR

GÉNÈRE 5 TITLE TAGS :

1. [Format classique] : Mot-clé - Description | Marque
2. [Format question] : Comment/Pourquoi Mot-clé ?
3. [Format liste] : X Meilleurs Mot-clé [2025]
4. [Format bénéfice] : Mot-clé : Obtenez [Résultat]
5. [Format urgence] : Mot-clé : [Action] Maintenant

Pour chaque :
- Title tag
- Caractères : X/60
- Score CTR estimé`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const internalLinkingSuggester: AITool = {
    id: 'internal-linking-suggester',
    slug: 'internal-linking-suggester',
    name: { fr: 'Suggestions de Liens Internes', ar: 'اقتراحات الروابط الداخلية', en: 'Internal Linking Suggester' },
    description: { fr: 'Améliorez votre maillage interne avec des suggestions intelligentes.', ar: 'حسن الروابط الداخلية باقتراحات ذكية.', en: 'Improve internal linking with smart suggestions.' },
    category: 'seo',
    subcategory: 'optimization',
    icon: 'Link2',
    credits: 12,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'current_article', type: 'textarea', label: 'Article actuel', required: true },
        { name: 'site_pages', type: 'textarea', label: 'Liste de vos pages/articles (titre + URL)' },
        { name: 'max_links', type: 'number', label: 'Nombre max de liens', default: 5 }
    ],
    outputs: [{ type: 'markdown', name: 'internalLinks' }],
    promptTemplate: `Suggère les meilleurs liens internes à ajouter.

ARTICLE ACTUEL :
{{current_article}}

PAGES DISPONIBLES :
{{site_pages}}

MAX LIENS : {{max_links}}

ANALYSE ET SUGGESTIONS :

1. LIENS CONTEXTUELS RECOMMANDÉS
   Pour chaque suggestion :
   - Texte d'ancre recommandé
   - Phrase où insérer le lien
   - Page cible
   - Pertinence (1-10)

2. STRUCTURE DE MAILLAGE
   - Liens vers pages piliers
   - Liens vers articles connexes
   - Liens vers pages commerciales (si pertinent)

3. TEXTES D'ANCRE VARIÉS
   - Éviter la sur-optimisation
   - Varier les formulations
   - Ancres naturelles

4. CODE HTML PRÊT À COPIER
   [phrase avec <a href="url">ancre</a>]`,
    model: 'gpt4',
    estimatedTime: '45s'
};

export const urlSlugOptimizer: AITool = {
    id: 'url-slug-optimizer',
    slug: 'url-slug-optimizer',
    name: { fr: 'Optimiseur d\'URL', ar: 'محسن الرابط', en: 'URL Slug Optimizer' },
    description: { fr: 'Créez des URLs courtes, lisibles et optimisées pour le SEO.', ar: 'أنشئ روابط قصيرة ومحسنة.', en: 'Create short, readable, SEO-optimized URLs.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Link',
    credits: 5,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'page_title', type: 'text', label: 'Titre de la page', required: true },
        { name: 'keyword', type: 'text', label: 'Mot-clé cible', required: true },
        { name: 'current_url', type: 'text', label: 'URL actuelle (si modification)' }
    ],
    outputs: [{ type: 'markdown', name: 'optimizedUrl' }],
    promptTemplate: `Génère une URL SEO-friendly optimale.

TITRE : {{page_title}}
MOT-CLÉ : {{keyword}}
URL ACTUELLE : {{current_url}}

RÈGLES URL SEO :
- Court (3-5 mots max)
- Mot-clé inclus
- Pas de mots vides (le, la, de, et...)
- Tirets entre les mots
- Minuscules uniquement
- Pas de caractères spéciaux

SUGGESTIONS (5) :

1. /{{keyword-optimise}}
   - Longueur : X caractères
   - Score SEO : X/10

2-5. [Variations]

RECOMMANDATION FINALE : [meilleure option]

⚠️ Si changement d'URL existante :
- Redirection 301 nécessaire
- Impact potentiel sur le ranking`,
    model: 'gpt4',
    estimatedTime: '10s'
};

export const headingStructureAnalyzer: AITool = {
    id: 'heading-structure-analyzer',
    slug: 'heading-structure-analyzer',
    name: { fr: 'Analyseur de Structure Hn', ar: 'محلل هيكل العناوين', en: 'Heading Structure Analyzer' },
    description: { fr: 'Vérifiez et corrigez la hiérarchie de vos titres (H1, H2, H3...).', ar: 'تحقق من تسلسل العناوين وصححه.', en: 'Check and fix heading hierarchy.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Heading',
    credits: 10,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Contenu avec titres', required: true },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible' }
    ],
    outputs: [{ type: 'markdown', name: 'headingAnalysis' }],
    promptTemplate: `Analyse et optimise la structure des titres (Hn).

CONTENU :
{{content}}

MOT-CLÉ : {{target_keyword}}

ANALYSE :

1. STRUCTURE ACTUELLE
   H1: [titre]
   ├── H2: [titre]
   │   ├── H3: [titre]
   │   └── H3: [titre]
   └── H2: [titre]

2. PROBLÈMES DÉTECTÉS
   - ❌ H1 multiples ?
   - ❌ Sauts de niveau (H1 → H3) ?
   - ❌ Mot-clé absent des Hn ?
   - ❌ Titres trop longs ?

3. SCORE STRUCTURE : X/100

4. RECOMMANDATIONS
   - Titres à modifier
   - Titres à ajouter
   - Hiérarchie optimale

5. STRUCTURE OPTIMISÉE SUGGÉRÉE
   [Nouvelle structure avec mot-clé intégré]`,
    model: 'gpt4',
    estimatedTime: '30s'
};

export const imageAltGenerator: AITool = {
    id: 'image-alt-generator',
    slug: 'image-alt-generator',
    name: { fr: 'Générateur de Alt Text', ar: 'مولد النص البديل', en: 'Image Alt Text Generator' },
    description: { fr: 'Optimisez vos images pour Google Images et l\'accessibilité.', ar: 'حسن صورك لمحركات البحث.', en: 'Optimize images for SEO and accessibility.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Image',
    credits: 8,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'image_description', type: 'textarea', label: 'Description de l\'image', required: true },
        { name: 'page_keyword', type: 'text', label: 'Mot-clé de la page' },
        { name: 'image_context', type: 'text', label: 'Contexte (section de l\'article)' },
        { name: 'count', type: 'number', label: 'Nombre d\'images', default: 1 }
    ],
    outputs: [{ type: 'markdown', name: 'altText' }],
    promptTemplate: `Génère des textes alternatifs SEO pour images.

DESCRIPTION IMAGE : {{image_description}}
MOT-CLÉ PAGE : {{page_keyword}}
CONTEXTE : {{image_context}}

RÈGLES ALT TEXT SEO :
- Descriptif et naturel
- 125 caractères max
- Inclure le mot-clé SI pertinent
- Pas de "image de" ou "photo de"
- Utile pour l'accessibilité

POUR CHAQUE IMAGE :

1. ALT TEXT PRINCIPAL
   alt="[description optimisée]"

2. TITLE ATTRIBUT (optionnel)
   title="[info complémentaire]"

3. NOM DE FICHIER SUGGÉRÉ
   [mot-cle-description].jpg

4. LÉGENDE SUGGÉRÉE (si applicable)
   [Texte pour <figcaption>]`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const contentGapAnalyzer: AITool = {
    id: 'content-gap-analyzer',
    slug: 'content-gap-analyzer',
    name: { fr: 'Analyseur de Lacunes', ar: 'محلل فجوات المحتوى', en: 'Content Gap Analyzer' },
    description: { fr: 'Découvrez ce qui manque à votre contenu par rapport aux concurrents.', ar: 'اكتشف ما ينقص محتواك مقارنة بالمنافسين.', en: 'Find content gaps vs competitors.' },
    category: 'seo',
    subcategory: 'research',
    icon: 'Search',
    credits: 20,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'your_content', type: 'textarea', label: 'Votre contenu actuel', required: true },
        { name: 'competitor_content', type: 'textarea', label: 'Contenu concurrent (top 3 Google)' },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible' }
    ],
    outputs: [{ type: 'markdown', name: 'gapAnalysis' }],
    promptTemplate: `Identifie les lacunes de contenu vs la concurrence.

VOTRE CONTENU :
{{your_content}}

CONTENU CONCURRENT :
{{competitor_content}}

MOT-CLÉ : {{target_keyword}}

ANALYSE DES LACUNES :

1. SUJETS MANQUANTS
   - [sujet couvert par concurrents mais pas vous]
   - Importance : Haute/Moyenne/Basse

2. QUESTIONS SANS RÉPONSE
   - Questions PAA non traitées
   - Questions implicites du sujet

3. MOTS-CLÉS MANQUANTS
   - Termes utilisés par concurrents
   - Mots-clés LSI absents

4. ÉLÉMENTS DE FORMAT
   - ❌ Tableaux comparatifs ?
   - ❌ Listes à puces ?
   - ❌ Images/infographies ?
   - ❌ Vidéo ?
   - ❌ FAQ ?

5. PLAN D'ACTION PRIORITAIRE
   1. [Action #1 - Impact élevé]
   2. [Action #2]
   3. [Action #3]

6. CONTENU À AJOUTER (suggestions rédigées)`,
    model: 'gpt4',
    estimatedTime: '60s'
};

export const seoAuditChecklist: AITool = {
    id: 'seo-audit-checklist',
    slug: 'seo-audit-checklist',
    name: { fr: 'Checklist Audit SEO', ar: 'قائمة تدقيق SEO', en: 'SEO Audit Checklist' },
    description: { fr: 'Générez une checklist d\'audit personnalisée pour n\'importe quelle page.', ar: 'أنشئ قائمة تدقيق مخصصة لأي صفحة.', en: 'Generate a custom SEO audit checklist.' },
    category: 'seo',
    subcategory: 'technical',
    icon: 'ClipboardCheck',
    credits: 15,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'page_url', type: 'text', label: 'URL de la page', required: true },
        { name: 'page_content', type: 'textarea', label: 'Contenu de la page' },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible' }
    ],
    outputs: [{ type: 'markdown', name: 'auditChecklist' }],
    promptTemplate: `Génère une checklist d'audit SEO complète.

URL : {{page_url}}
MOT-CLÉ : {{target_keyword}}
CONTENU : {{page_content}}

CHECKLIST AUDIT SEO :

## ON-PAGE (Score: X/25)
- [ ] Title tag optimisé (60 car., mot-clé au début)
- [ ] Meta description (155 car., CTA)
- [ ] URL SEO-friendly (courte, mot-clé)
- [ ] H1 unique avec mot-clé
- [ ] Structure Hn logique
- [ ] Mot-clé dans les 100 premiers mots
- [ ] Densité mot-clé 1-2%
- [ ] Images avec alt text
- [ ] Liens internes (3-5)
- [ ] Lien externe (1-2 autorité)

## TECHNIQUE (Score: X/15)
- [ ] HTTPS actif
- [ ] Mobile-friendly
- [ ] Vitesse < 3 secondes
- [ ] Pas d'erreurs 404
- [ ] Sitemap XML
- [ ] Robots.txt correct
- [ ] Schema markup

## CONTENU (Score: X/20)
- [ ] Longueur suffisante (1500+ mots)
- [ ] Contenu unique
- [ ] Réponse à l'intention de recherche
- [ ] FAQ incluse
- [ ] Mise à jour récente

## SCORE GLOBAL : X/60

## TOP 3 ACTIONS PRIORITAIRES :
1. [Action critique]
2. [Action importante]
3. [Action recommandée]`,
    model: 'gpt4',
    estimatedTime: '45s'
};

export const serpPreview: AITool = {
    id: 'serp-preview',
    slug: 'serp-preview',
    name: { fr: 'Aperçu SERP', ar: 'معاينة نتائج البحث', en: 'SERP Preview' },
    description: { fr: 'Visualisez comment votre page apparaîtra dans les résultats Google.', ar: 'شاهد كيف ستظهر صفحتك في نتائج البحث.', en: 'Preview your page in Google results.' },
    category: 'seo',
    subcategory: 'on-page',
    icon: 'Monitor',
    credits: 5,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'title', type: 'text', label: 'Title Tag', required: true },
        { name: 'url', type: 'text', label: 'URL', required: true },
        { name: 'description', type: 'textarea', label: 'Meta Description', required: true },
        { name: 'rich_snippet', type: 'select', label: 'Rich Snippet', options: ['None', 'FAQ', 'Rating', 'Breadcrumb', 'Sitelinks'], default: 'None' }
    ],
    outputs: [{ type: 'markdown', name: 'serpPreview' }],
    promptTemplate: `Génère un aperçu SERP et analyse son efficacité.

TITLE : {{title}}
URL : {{url}}
DESCRIPTION : {{description}}
RICH SNIPPET : {{rich_snippet}}

APERÇU GOOGLE :
┌─────────────────────────────────────────────┐
│ {{title}}                                   │
│ {{url}}                                     │
│ {{description}}                             │
└─────────────────────────────────────────────┘

ANALYSE :

1. TITLE TAG
   - Longueur : X/60 caractères
   - Troncature : Oui/Non
   - Score CTR : X/10

2. URL
   - Longueur : OK/Trop longue
   - Lisibilité : X/10

3. META DESCRIPTION
   - Longueur : X/155 caractères
   - CTA présent : Oui/Non
   - Score CTR : X/10

4. OPTIMISATIONS SUGGÉRÉES
   - [Suggestion 1]
   - [Suggestion 2]

5. VERSION OPTIMISÉE
   [Nouvel aperçu amélioré]`,
    model: 'gpt4',
    estimatedTime: '15s'
};
