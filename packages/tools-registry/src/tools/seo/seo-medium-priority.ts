import { AITool } from '../../types';

export const readabilityScoreAnalyzer: AITool = {
    id: 'readability-score-analyzer',
    slug: 'readability-score-analyzer',
    name: { fr: 'Analyseur de Lisibilité', ar: 'محلل سهولة القراءة', en: 'Readability Analyzer' },
    description: { fr: 'Analysez la lisibilité de votre texte (Flesch, Gunning Fog) pour maximiser l\'engagement.', ar: 'حلل سهولة قراءة النص.', en: 'Analyze text readability.' },
    category: 'seo',
    subcategory: 'optimization',
    icon: 'BookOpen',
    credits: 10,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Texte à analyser', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'readabilityReport' }],
    promptTemplate: `Analyse la lisibilité de ce texte.

TEXTE : {{content}}

ANALYSE :
- Score Flesch Reading Ease
- Niveau scolaire estimé
- Complexité des phrases
- Mots complexes utilisés

RECOMMANDATIONS :
- Phrases à simplifier
- Mots à remplacer
- Structure à aérer`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const keywordDensityChecker: AITool = {
    id: 'keyword-density-checker',
    slug: 'keyword-density-checker',
    name: { fr: 'Vérificateur de Densité', ar: 'مدقق كثافة الكلمات', en: 'Keyword Density Checker' },
    description: { fr: 'Vérifiez si vous n\'optimisez pas trop (ou pas assez) vos mots-clés.', ar: 'تحقق من كثافة الكلمات المفتاحية.', en: 'Check keyword density.' },
    category: 'seo',
    subcategory: 'optimization',
    icon: 'Percent',
    credits: 8,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'content', type: 'textarea', label: 'Texte à analyser', required: true },
        { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'densityAnalysis' }],
    promptTemplate: `Analyse la densité des mots-clés.

TEXTE : {{content}}
MOT-CLÉ : {{target_keyword}}

RÉSULTATS :
- Occurrences : X
- Densité : X%
- Verdict : [Faible / Optimal / Bourrage]

CONSEILS :
- [Conseils d'ajustement]`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const anchorTextOptimizer: AITool = {
    id: 'anchor-text-optimizer',
    slug: 'anchor-text-optimizer',
    name: { fr: 'Optimiseur de Texte d\'Ancre', ar: 'محسن نص الرابط', en: 'Anchor Text Optimizer' },
    description: { fr: 'Générez des variations de textes d\'ancre pour éviter les pénalités.', ar: 'أنشئ نصوص روابط متنوعة.', en: 'Generate varied anchor texts.' },
    category: 'seo',
    subcategory: 'optimization',
    icon: 'Anchor',
    credits: 8,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'target_url', type: 'text', label: 'URL cible', required: true },
        { name: 'keyword', type: 'text', label: 'Mot-clé principal', required: true },
        { name: 'source_context', type: 'text', label: 'Contexte de la page source' }
    ],
    outputs: [{ type: 'markdown', name: 'anchorSuggestions' }],
    promptTemplate: `Suggère des textes d'ancre variés.

URL : {{target_url}}
MOT-CLÉ : {{keyword}}
CONTEXTE : {{source_context}}

SUGGESTIONS :
1. Exact Match (max 20%) : [mot-clé]
2. Partial Match : [variation]
3. Branded : [marque]
4. Generic : [cliquez ici...]
5. Naked URL : [url]

RECOMMANDATION :
Lequel utiliser dans ce contexte précis ?`,
    model: 'gpt4',
    estimatedTime: '15s'
};

export const robotsTxtGenerator: AITool = {
    id: 'robots-txt-generator',
    slug: 'robots-txt-generator',
    name: { fr: 'Générateur Robots.txt', ar: 'مولد Robots.txt', en: 'Robots.txt Generator' },
    description: { fr: 'Créez un fichier robots.txt correct pour guider les moteurs de recherche.', ar: 'أنشئ ملف robots.txt صحيح.', en: 'Create a correct robots.txt file.' },
    category: 'seo',
    subcategory: 'technical',
    icon: 'Bot',
    credits: 10,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'user_agents', type: 'select', label: 'User Agents', options: ['Tous (*)', 'Googlebot', 'Bingbot'], default: 'Tous (*)' },
        { name: 'allowed_paths', type: 'textarea', label: 'Chemins autorisés (un par ligne)' },
        { name: 'disallowed_paths', type: 'textarea', label: 'Chemins interdits (un par ligne)' },
        { name: 'sitemap_url', type: 'text', label: 'URL du Sitemap' }
    ],
    outputs: [{ type: 'markdown', name: 'robotsTxt' }],
    promptTemplate: `Génère le fichier robots.txt.

USER AGENT : {{user_agents}}
ALLOWED : {{allowed_paths}}
DISALLOWED : {{disallowed_paths}}
SITEMAP : {{sitemap_url}}

CODE ROBOTS.TXT :
\`\`\`
User-agent: ...
Disallow: ...
Allow: ...

Sitemap: ...
\`\`\`

VALIDATION :
- Vérifie la syntaxe
- Avertit si danger de bloquer tout le site`,
    model: 'gpt4',
    estimatedTime: '10s'
};

export const sitemapGenerator: AITool = {
    id: 'sitemap-generator',
    slug: 'sitemap-generator',
    name: { fr: 'Générateur de Sitemap', ar: 'مولد خريطة الموقع', en: 'Sitemap Generator' },
    description: { fr: 'Générez la structure XML de votre sitemap pour l\'indexation.', ar: 'أنشئ خريطة الموقع XML.', en: 'Generate XML sitemap structure.' },
    category: 'seo',
    subcategory: 'technical',
    icon: 'Map',
    credits: 10,
    priority: 'medium',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'urls', type: 'textarea', label: 'Liste des URLs (une par ligne)', required: true },
        { name: 'frequency', type: 'select', label: 'Fréquence de mise à jour', options: ['daily', 'weekly', 'monthly', 'yearly'], default: 'weekly' },
        { name: 'priority', type: 'number', label: 'Priorité par défaut (0.0 - 1.0)', default: 0.5 }
    ],
    outputs: [{ type: 'markdown', name: 'sitemapXml' }],
    promptTemplate: `Génère un sitemap.xml valide.

URLS : {{urls}}
FREQ : {{frequency}}
PRIO : {{priority}}

CODE SITEMAP XML :
\`\`\`xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ...
</urlset>
\`\`\``,
    model: 'gpt4',
    estimatedTime: '20s'
};
