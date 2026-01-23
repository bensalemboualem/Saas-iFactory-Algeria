import { AITool } from '../../types';

export const blogIntroduction: AITool = {
    id: 'blog-introduction',
    slug: 'blog-introduction',
    name: { fr: 'Introduction de Blog', ar: 'مقدمة المدونة', en: 'Blog Introduction' },
    description: { fr: 'Générez des introductions captivantes qui accrochent le lecteur dès les premières lignes.', ar: 'أنشئ مقدمات مدونة جذابة تجذب القارئ.', en: 'Generate captivating blog introductions.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Play',
    credits: 10,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'title', type: 'text', label: 'Titre de l\'article', required: true },
        { name: 'topic', type: 'textarea', label: 'Sujet principal', required: true },
        { name: 'hook_style', type: 'select', label: 'Style d\'accroche', options: ['Question', 'Statistique', 'Anecdote', 'Citation', 'Problème'], default: 'Question' },
        { name: 'tone', type: 'select', options: ['Professionnel', 'Casual', 'Académique', 'Conversationnel'], default: 'Professionnel' }
    ],
    outputs: [{ type: 'markdown', name: 'introduction' }],
    promptTemplate: `Écris une introduction captivante pour un article de blog.

TITRE : {{title}}
SUJET : {{topic}}
STYLE D'ACCROCHE : {{hook_style}}
TON : {{tone}}

STRUCTURE (150-200 mots) :
1. HOOK : Accroche percutante selon le style choisi
2. CONTEXTE : Pourquoi ce sujet est important maintenant
3. PROMESSE : Ce que le lecteur va apprendre
4. TRANSITION : Phrase de liaison vers le premier H2

Rends l'introduction irrésistible, le lecteur doit VOULOIR continuer.`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const blogConclusion: AITool = {
    id: 'blog-conclusion',
    slug: 'blog-conclusion',
    name: { fr: 'Conclusion de Blog', ar: 'خاتمة المدونة', en: 'Blog Conclusion' },
    description: { fr: 'Rédigez des conclusions mémorables avec un appel à l\'action fort.', ar: 'اكتب خاتمات لا تنسى مع دعوة قوية لاتخاذ إجراء.', en: 'Write memorable conclusions with a strong CTA.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'CheckCircle',
    credits: 10,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'article_summary', type: 'textarea', label: 'Résumé des points clés', required: true },
        { name: 'cta_type', type: 'select', label: 'Type de CTA', options: ['Newsletter', 'Commentaire', 'Partage', 'Produit', 'Article Suivant', 'Contact'], default: 'Newsletter' },
        { name: 'cta_details', type: 'text', label: 'Détails du CTA (lien, produit...)' }
    ],
    outputs: [{ type: 'markdown', name: 'conclusion' }],
    promptTemplate: `Écris une conclusion mémorable pour un article de blog.

POINTS CLÉS DE L'ARTICLE : {{article_summary}}
TYPE DE CTA : {{cta_type}}
DÉTAILS CTA : {{cta_details}}

STRUCTURE (100-150 mots) :
1. RÉCAP : Synthèse des 3 points essentiels
2. VALEUR : Rappel du bénéfice pour le lecteur  
3. CTA : Appel à l'action clair et motivant
4. OUVERTURE : Question ou réflexion finale

Le lecteur doit partir avec une impression positive ET passer à l'action.`,
    model: 'gpt4',
    estimatedTime: '20s'
};

export const listicleGenerator: AITool = {
    id: 'listicle-generator',
    slug: 'listicle-generator',
    name: { fr: 'Générateur de Listicle', ar: 'مولد قوائم المقالات', en: 'Listicle Generator' },
    description: { fr: 'Créez des articles de liste viraux (Top 10, X Façons de...).', ar: 'أنشئ مقالات قائمة فيروسية.', en: 'Create viral listicle articles.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'ListOrdered',
    credits: 40,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet de la liste', required: true },
        { name: 'list_count', type: 'number', label: 'Nombre d\'éléments', default: 10 },
        { name: 'format', type: 'select', options: ['Top X', 'Meilleures', 'Erreurs à éviter', 'Astuces', 'Raisons', 'Façons'], default: 'Top X' },
        { name: 'depth', type: 'select', label: 'Profondeur', options: ['Court (100 mots)', 'Moyen (200 mots)', 'Détaillé (400 mots)'], default: 'Moyen (200 mots)' }
    ],
    outputs: [{ type: 'markdown', name: 'listicle' }],
    promptTemplate: `Crée un article listicle complet et engageant.

SUJET : {{topic}}
NOMBRE D'ÉLÉMENTS : {{list_count}}
FORMAT : {{format}}
PROFONDEUR PAR ÉLÉMENT : {{depth}}

STRUCTURE :
1. Titre accrocheur avec chiffre
2. Introduction (pourquoi cette liste)
3. {{list_count}} éléments avec :
   - Titre numéroté percutant
   - Explication détaillée
   - Exemple concret
   - Conseil actionnable
4. Conclusion avec récap

Rends chaque élément unique et valuable. Évite le remplissage.`,
    model: 'claude',
    estimatedTime: '90s'
};

export const howToGuide: AITool = {
    id: 'how-to-guide',
    slug: 'how-to-guide',
    name: { fr: 'Guide Pratique', ar: 'دليل عملي', en: 'How-To Guide' },
    description: { fr: 'Générez des guides étape par étape faciles à suivre.', ar: 'أنشئ أدلة خطوة بخطوة سهلة المتابعة.', en: 'Generate easy-to-follow step-by-step guides.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'BookOpen',
    credits: 45,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'task', type: 'text', label: 'Tâche à accomplir', required: true, placeholder: 'Comment créer un site web...' },
        { name: 'audience_level', type: 'select', label: 'Niveau du public', options: ['Débutant', 'Intermédiaire', 'Avancé'], default: 'Débutant' },
        { name: 'include_images', type: 'boolean', label: 'Suggérer emplacements images', default: true },
        { name: 'tools_needed', type: 'text', label: 'Outils/prérequis (optionnel)' }
    ],
    outputs: [{ type: 'markdown', name: 'guide' }],
    promptTemplate: `Crée un guide pratique étape par étape.

TÂCHE : {{task}}
NIVEAU : {{audience_level}}
OUTILS REQUIS : {{tools_needed}}
SUGGESTIONS IMAGES : {{include_images}}

STRUCTURE :
1. Titre "Comment [tâche] en X étapes"
2. Introduction : Résultat final + temps estimé
3. Prérequis et matériel nécessaire
4. Étapes numérotées avec :
   - Action claire et précise
   - Explication du "pourquoi"
   - ⚠️ Erreur courante à éviter
   - 💡 Astuce de pro
   - [📸 Image suggérée] si demandé
5. Résultat attendu
6. FAQ (3 questions)
7. Prochaines étapes

Sois ultra pratique. Le lecteur doit pouvoir suivre sans aide externe.`,
    model: 'claude',
    estimatedTime: '90s'
};

export const comparisonArticle: AITool = {
    id: 'comparison-article',
    slug: 'comparison-article',
    name: { fr: 'Article Comparatif', ar: 'مقال مقارنة', en: 'Comparison Article' },
    description: { fr: 'Comparez deux produits ou services de manière objective.', ar: 'قارن بين منتجين أو خدمتين بموضوعية.', en: 'Objectively compare two products or services.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'GitCompare',
    credits: 50,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'item1', type: 'text', label: 'Élément 1', required: true },
        { name: 'item2', type: 'text', label: 'Élément 2', required: true },
        { name: 'criteria', type: 'tags', label: 'Critères de comparaison', placeholder: 'prix, qualité, facilité...' },
        { name: 'recommendation', type: 'select', label: 'Donner une recommandation ?', options: ['Oui, claire', 'Oui, nuancée', 'Non, neutre'], default: 'Oui, claire' }
    ],
    outputs: [{ type: 'markdown', name: 'comparison' }],
    promptTemplate: `Crée un article comparatif objectif et utile.

ÉLÉMENT 1 : {{item1}}
ÉLÉMENT 2 : {{item2}}
CRITÈRES : {{criteria}}
RECOMMANDATION : {{recommendation}}

STRUCTURE :
1. Titre : "{{item1}} vs {{item2}} : Le Guide Complet [2025]"
2. Intro : Contexte + pour qui est cette comparaison
3. Tableau récapitulatif (synthèse visuelle)
4. Présentation de {{item1}} (forces, faiblesses)
5. Présentation de {{item2}} (forces, faiblesses)
6. Comparaison critère par critère :
   - Analyse + Verdict
7. Verdict final selon le profil utilisateur
8. FAQ

Sois factuel et aide vraiment le lecteur à choisir.`,
    model: 'claude',
    estimatedTime: '120s'
};

export const reviewArticle: AITool = {
    id: 'review-article',
    slug: 'review-article',
    name: { fr: 'Article de Test/Avis', ar: 'مقال مراجعة', en: 'Review Article' },
    description: { fr: 'Rédigez des tests produits complets et crédibles.', ar: 'اكتب مراجعات منتجات كاملة وموثوقة.', en: 'Write complete and credible product reviews.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'Star',
    credits: 45,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'product', type: 'text', label: 'Produit/Service à tester', required: true },
        { name: 'category', type: 'text', label: 'Catégorie', placeholder: 'logiciel, téléphone, service...' },
        { name: 'rating', type: 'number', label: 'Note globale /10', default: 8 },
        { name: 'tested_duration', type: 'text', label: 'Durée du test', placeholder: '2 semaines, 3 mois...' }
    ],
    outputs: [{ type: 'markdown', name: 'review' }],
    promptTemplate: `Crée un article de test/avis complet et crédible.

PRODUIT : {{product}}
CATÉGORIE : {{category}}
NOTE : {{rating}}/10
DURÉE DU TEST : {{tested_duration}}

STRUCTURE :
1. Titre : "{{product}} : Test Complet et Avis Honnête [2025]"
2. Résumé rapide (verdict en 3 lignes + note)
3. Présentation du produit
4. Points forts (5-7 avec détails)
5. Points faibles (3-5 avec honnêteté)
6. Test en conditions réelles
7. Rapport qualité/prix
8. Alternatives à considérer
9. Pour qui est ce produit ?
10. Verdict final + Note détaillée
11. FAQ

Sois honnête et détaillé. La crédibilité d'abord.`,
    model: 'claude',
    estimatedTime: '90s'
};

export const caseStudyWriter: AITool = {
    id: 'case-study-writer',
    slug: 'case-study-writer',
    name: { fr: 'Étude de Cas', ar: 'دراسة حالة', en: 'Case Study Writer' },
    description: { fr: 'Transformez vos succès clients en études de cas convaincantes.', ar: 'حول نجاحات عملائك إلى دراسات حالة مقنعة.', en: 'Turn client successes into convincing case studies.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'FileSearch',
    credits: 55,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'client', type: 'text', label: 'Client/Entreprise', required: true },
        { name: 'challenge', type: 'textarea', label: 'Problématique initiale', required: true },
        { name: 'solution', type: 'textarea', label: 'Solution apportée', required: true },
        { name: 'results', type: 'textarea', label: 'Résultats obtenus', required: true },
        { name: 'industry', type: 'text', label: 'Secteur d\'activité' }
    ],
    outputs: [{ type: 'markdown', name: 'caseStudy' }],
    promptTemplate: `Crée une étude de cas professionnelle et convaincante.

CLIENT : {{client}}
SECTEUR : {{industry}}
DÉFI : {{challenge}}
SOLUTION : {{solution}}
RÉSULTATS : {{results}}

STRUCTURE :
1. Titre : "Comment [Client] a [Résultat clé] grâce à [Solution]"
2. Résumé exécutif (bullet points)
3. Contexte et présentation du client
4. La problématique (douleur, enjeux, urgence)
5. Notre approche et solution
6. Mise en œuvre (étapes clés)
7. Résultats (chiffres, témoignages)
8. Enseignements clés
9. CTA : Comment reproduire ce succès

Storytelling puissant + preuves concrètes.`,
    model: 'claude',
    estimatedTime: '120s'
};

export const faqArticleGenerator: AITool = {
    id: 'faq-article-generator',
    slug: 'faq-article-generator',
    name: { fr: 'Article FAQ', ar: 'مقال الأسئلة الشائعة', en: 'FAQ Article Generator' },
    description: { fr: 'Générez des pages FAQ complètes optimisées pour le SEO.', ar: 'أنشئ صفحات أسئلة شائعة كاملة ومحسنة لمحركات البحث.', en: 'Generate complete SEO-optimized FAQ pages.' },
    category: 'blog',
    subcategory: 'writing',
    icon: 'HelpCircle',
    credits: 35,
    priority: 'high',
    isAlgeriaExclusive: false,
    inputs: [
        { name: 'topic', type: 'text', label: 'Sujet principal', required: true },
        { name: 'questions_count', type: 'number', label: 'Nombre de questions', default: 15 },
        { name: 'audience', type: 'text', label: 'Public cible', placeholder: 'débutants, professionnels...' },
        { name: 'include_schema', type: 'boolean', label: 'Inclure le Schema FAQ (SEO)', default: true }
    ],
    outputs: [{ type: 'markdown', name: 'faq' }],
    promptTemplate: `Crée un article FAQ complet et optimisé SEO.

SUJET : {{topic}}
NOMBRE DE QUESTIONS : {{questions_count}}
PUBLIC : {{audience}}
SCHEMA FAQ : {{include_schema}}

STRUCTURE :
1. Titre : "{{topic}} : {{questions_count}} Questions Fréquentes"
2. Introduction courte
3. Questions organisées par thème :
   - Questions de base (c'est quoi, pourquoi...)
   - Questions pratiques (comment faire...)
   - Questions avancées (et si..., peut-on...)
   - Questions prix/coûts si pertinent
4. Conclusion avec ressources

Pour chaque question :
- Réponse concise ET complète
- Exemple si utile
- Lien interne suggéré

{{#if include_schema}}
À la fin, génère le JSON-LD Schema FAQ.
{{/if}}`,
    model: 'gpt4',
    estimatedTime: '60s'
};
