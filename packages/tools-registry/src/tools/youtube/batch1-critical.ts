import { AITool } from '../../types';

export const youtubeTitleGenerator: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'أنشئ عناوين يوتيوب جذابة تزيد النقرات',
    en: 'Create catchy YouTube titles that maximize clicks',
    fr: 'Créez des titres YouTube accrocheurs qui maximisent les clics et le CTR'
  },
  icon: 'Type',
  id: 'youtube-title-generator',
  inputs: [
    { label: 'Sujet de la vidéo', name: 'video_topic', required: true, type: 'text' },
    { label: 'Mot-clé cible', name: 'target_keyword', type: 'text' },
    { label: 'Style', name: 'style', options: ['Curiosity', 'Listicle', 'Tutorial', 'Shocking', 'Emotional', 'Versus'], type: 'select' },
    { default: true, label: 'Inclure [CROCHETS]', name: 'include_brackets', type: 'boolean' },
    { label: 'Langue', name: 'language', options: ['fr', 'ar', 'en', 'darija'], type: 'select' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد عناوين يوتيوب', fr: 'Générateur de Titres YouTube', en: 'YouTube Title Generator' },
  outputs: [{ name: 'titles', type: 'markdown' }],
  slug: 'youtube-title-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert YouTube avec 10M+ d'abonnés.

SUJET : {{video_topic}}
MOT-CLÉ : {{target_keyword}}
STYLE : {{style}}
LANGUE : {{language}}

## 🎬 10 Titres YouTube Optimisés

**Formules gagnantes :**
- Chiffres impairs (7, 9, 11)
- Power words : Secret, Incroyable, Choquant, Gratuit
- Crochets : [2025], [TUTO], [VLOG]
- 60 caractères max (idéal : 50)

Pour chaque titre :
- Caractères : X/60
- Score CTR estimé : ⭐⭐⭐⭐⭐
- Pourquoi ça marche`,
  subcategory: 'optimization'
};

export const youtubeDescriptionGenerator: AITool = {
  category: 'youtube',
  credits: 12,
  description: {
    ar: 'قم بإنشاء أوصاف محسنة لمحركات البحث مع فصول وروابط',
    en: 'Generate SEO-optimized descriptions with chapters and links',
    fr: 'Générez des descriptions optimisées pour le SEO avec chapitres et liens'
  },
  icon: 'FileText',
  id: 'youtube-description-generator',
  inputs: [
    { label: 'Titre', name: 'video_title', required: true, type: 'text' },
    { label: 'Résumé du contenu', name: 'video_summary', required: true, type: 'textarea' },
    { label: 'Chapitres (optionnel)', name: 'timestamps', type: 'textarea' },
    { label: 'Liens à inclure', name: 'links', type: 'textarea' },
    { label: 'Mots-clés SEO', name: 'keywords', type: 'text' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'وصف يوتيوب', fr: 'Description YouTube', en: 'YouTube Description' },
  outputs: [{ name: 'description', type: 'markdown' }],
  slug: 'youtube-description-generator',
  priority: 'critical',
  promptTemplate: `Génère une description YouTube optimisée SEO (5000 car. max).

TITRE : {{video_title}}
RÉSUMÉ : {{video_summary}}
MOTS-CLÉS : {{keywords}}
LIENS : {{links}}
TIMESTAMPS : {{timestamps}}

Structure :
1. Accroche (2-3 lignes visibles avant "Plus")
2. Résumé avec mots-clés
3. Chapitres/Timestamps
4. Liens réseaux
5. CTA abonnement
6. Hashtags (3-5)`,
  subcategory: 'optimization'
};

export const youtubeTagsGenerator: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'قم بإنشاء أفضل العلامات للإشارة إلى الفيديو الخاص بك',
    en: 'Generate the best tags to rank your video',
    fr: 'Générez les meilleurs tags pour référencer votre vidéo'
  },
  icon: 'Tags',
  id: 'youtube-tags-generator',
  inputs: [
    { label: 'Sujet de la vidéo', name: 'video_topic', required: true, type: 'text' },
    { label: 'Mot-clé principal', name: 'main_keyword', required: true, type: 'text' },
    { label: 'Niche (ex: Gaming, Tech)', name: 'niche', type: 'text' },
    { label: 'Langue', name: 'language', options: ['fr', 'ar', 'en'], type: 'select' }
  ],
  estimatedTime: '15s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد الوسوم', fr: 'Générateur de Tags', en: 'Tags Generator' },
  outputs: [{ name: 'tags', type: 'markdown' }],
  slug: 'youtube-tags-generator',
  priority: 'critical',
  promptTemplate: `Génère 20 tags YouTube optimisés (500 car. max total).

SUJET : {{video_topic}}
MOT-CLÉ : {{main_keyword}}
NICHE : {{niche}}
LANGUE : {{language}}

Stratégie :
1. Tag principal en premier
2. Variations longue traîne
3. Tags de niche
4. Tags trending
5. Tag chaîne (branding)

Fournis la liste prête à copier-coller (séparée par des virgules).`,
  subcategory: 'optimization'
};

export const youtubeScriptWriter: AITool = {
  category: 'youtube',
  credits: 40,
  description: {
    ar: 'قم بإنشاء نصوص جذابة مع خطاف وجسم ودعوة للعمل',
    en: 'Create captivating scripts with hook, body and call to action',
    fr: 'Créez des scripts captivants avec hook, corps et appel à l\'action'
  },
  icon: 'ScrollText',
  id: 'youtube-script-writer',
  inputs: [
    { label: 'Sujet', name: 'video_topic', required: true, type: 'text' },
    { label: 'Durée visée', name: 'video_length', options: ['Court (3min)', 'Moyen (10min)', 'Long (20min)'], type: 'select' },
    { label: 'Style', name: 'style', options: ['Éducatif', 'Divertissant', 'Storytelling', 'Tutoriel'], type: 'select' },
    { label: 'Ton', name: 'tone', options: ['Professionnel', 'Décontracté', 'Humoristique', 'Dramatique'], type: 'select' },
    { label: 'Points clés à aborder', name: 'key_points', type: 'textarea' }
  ],
  estimatedTime: '90s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'كاتب السيناريو', fr: 'Rédacteur de Script', en: 'Script Writer' },
  outputs: [{ name: 'script', type: 'markdown' }],
  slug: 'youtube-script-writer',
  priority: 'critical',
  promptTemplate: `Écris un script YouTube complet.

SUJET : {{video_topic}}
DURÉE : {{video_length}}
STYLE : {{style}}
TON : {{tone}}
POINTS CLÉS : {{key_points}}

Structure :
🎯 HOOK (0:00-0:15) - Accroche choc
📺 INTRO (0:15-0:45) - Présentation + teaser
📖 CORPS - Parties numérotées avec transitions
🔄 RÉCAP - Résumé des points clés
📢 CTA - Appel à l'action + engagement
🎞️ OUTRO - Écran de fin

Inclus :
- Indications de montage [B-roll]
- Suggestions musique
- Durée estimée par section`,
  subcategory: 'content'
};

export const youtubeShortsScript: AITool = {
  category: 'youtube',
  credits: 15,
  description: {
    ar: 'نصوص ديناميكية للشورتس والريلز وتيك توك',
    en: 'Dynamic scripts for Shorts, Reels and TikTok',
    fr: 'Scripts dynamiques pour Shorts, Reels et TikTok'
  },
  icon: 'Smartphone',
  id: 'youtube-shorts-script',
  inputs: [
    { label: 'Sujet', name: 'topic', required: true, type: 'text' },
    { label: 'Style d\'accroche', name: 'hook_style', options: ['Question', 'Affirmation choc', 'Défi', 'Secret'], type: 'select' },
    { label: 'Durée', name: 'duration', options: ['15s', '30s', '45s', '60s'], type: 'select' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'سيناريو شورتس', fr: 'Script Shorts/Reels', en: 'Shorts Script' },
  outputs: [{ name: 'shortScript', type: 'markdown' }],
  slug: 'youtube-shorts-script',
  priority: 'critical',
  promptTemplate: `Script pour Short viral.

SUJET : {{topic}}
HOOK : {{hook_style}}
DURÉE : {{duration}}

Structure :
⚡ HOOK (0-3 sec) - STOPPER LE SCROLL
📱 CONTENU (3-50 sec) - Direct, phrases courtes
🔄 CTA + LOOP (fin) - Transition vers le début

Checklist :
✅ Hook immédiat
✅ Texte à l'écran
✅ Pas de temps mort
✅ Format 9:16
✅ Hashtags suggérés`,
  subcategory: 'content'
};

export const youtubeThumbnailIdeas: AITool = {
  category: 'youtube',
  credits: 10,
  description: {
    ar: 'مفاهيم مرئية لزيادة معدل النقر',
    en: 'Visual concepts to increase your click-through rate',
    fr: 'Concepts visuels pour augmenter votre taux de clic'
  },
  icon: 'Image',
  id: 'youtube-thumbnail-ideas',
  inputs: [
    { label: 'Titre de la vidéo', name: 'video_title', required: true, type: 'text' },
    { label: 'Émotion cible', name: 'emotion', options: ['Surprise', 'Curiosité', 'Excitation', 'Choc'], type: 'select' },
    { label: 'Style visuel', name: 'style', options: ['Face reaction', 'Before/After', 'Versus', 'Text bold', 'Minimal'], type: 'select' }
  ],
  estimatedTime: '25s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'أفكار الصور المصغرة', fr: 'Idées de Miniatures', en: 'Thumbnail Ideas' },
  outputs: [{ name: 'thumbnails', type: 'markdown' }],
  slug: 'youtube-thumbnail-ideas',
  priority: 'critical',
  promptTemplate: `Génère 5 concepts de miniatures YouTube.

TITRE : {{video_title}}
ÉMOTION : {{emotion}}
STYLE : {{style}}

Pour chaque concept :
- Composition (arrière-plan, premier plan)
- Texte (3-4 MOTS MAX)
- Expression du visage
- Couleurs recommandées
- Éléments graphiques (flèches, émojis)

Règles :
- Lisible en petit (mobile)
- Contraste élevé
- Éviter le vert (interface YT)`,
  subcategory: 'optimization'
};

export const youtubeHookGenerator: AITool = {
  category: 'youtube',
  credits: 10,
  description: {
    ar: 'اعثر على الخطاف المثالي لجذب الانتباه منذ الثواني الأولى',
    en: 'Find the perfect hook to captivate from the first seconds',
    fr: 'Trouvez l\'accroche parfaite pour captiver dès les premières secondes'
  },
  icon: 'Anchor',
  id: 'youtube-hook-generator',
  inputs: [
    { label: 'Sujet', name: 'video_topic', required: true, type: 'text' },
    { label: 'Type de hook', name: 'hook_type', options: ['Question', 'Statistic', 'Story', 'Controversy', 'Promise', 'Secret'], type: 'select' },
    { label: 'Émotion', name: 'target_emotion', options: ['Curiosité', 'Peur de rater (FOMO)', 'Surprise'], type: 'select' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد الخطافات', fr: 'Générateur de Hooks', en: 'Hook Generator' },
  outputs: [{ name: 'hooks', type: 'markdown' }],
  slug: 'youtube-hook-generator',
  priority: 'critical',
  promptTemplate: `Génère 15 hooks pour capturer l'attention.

SUJET : {{video_topic}}
TYPE : {{hook_type}}
ÉMOTION : {{target_emotion}}

Types :
- QUESTION (curiosité)
- STATISTIQUE (crédibilité)
- HISTOIRE (connexion)
- PROMESSE (valeur)
- CONTROVERSE (engagement)
- SECRET (exclusivité)

Les 5 premières secondes = 50% de la rétention !`,
  subcategory: 'content'
};

export const youtubeSeoOptimizer: AITool = {
  category: 'youtube',
  credits: 20,
  description: {
    ar: 'تدقيق وتحسين محركات البحث لمقاطع الفيديو الخاصة بك',
    en: 'Audit and improve your video ranking',
    fr: 'Auditez et améliorez le référencement de vos vidéos'
  },
  icon: 'Search',
  id: 'youtube-seo-optimizer',
  inputs: [
    { label: 'Titre actuel', name: 'video_title', required: true, type: 'text' },
    { label: 'Description actuelle', name: 'video_description', type: 'textarea' },
    { label: 'Tags actuels', name: 'video_tags', type: 'text' },
    { label: 'Mot-clé cible', name: 'target_keyword', required: true, type: 'text' }
  ],
  estimatedTime: '45s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'محسن SEO يوتيوب', fr: 'Optimiseur SEO YouTube', en: 'YouTube SEO Optimizer' },
  outputs: [{ name: 'audit', type: 'markdown' }],
  slug: 'youtube-seo-optimizer',
  priority: 'critical',
  promptTemplate: `Audit SEO YouTube complet.

TITRE : {{video_title}}
DESC : {{video_description}}
TAGS : {{video_tags}}
KEYWORD : {{target_keyword}}

Analyse :
1. TITRE - Score X/10
2. DESCRIPTION - Score X/10
3. TAGS - Score X/10

Score global : X/100

Plan d'action prioritaire avec versions optimisées.`,
  subcategory: 'optimization'
};

export const youtubeContentIdeas: AITool = {
  category: 'youtube',
  credits: 15,
  description: {
    ar: 'لا تنفد أفكار الفيديو مرة أخرى',
    en: 'Never run out of video ideas again',
    fr: 'Ne soyez plus jamais à court d\'idées de vidéos'
  },
  icon: 'Lightbulb',
  id: 'youtube-content-ideas',
  inputs: [
    { label: 'Niche de la chaîne', name: 'channel_niche', required: true, type: 'text' },
    { label: 'Audience cible', name: 'target_audience', type: 'text' },
    { label: 'Type de contenu', name: 'content_type', options: ['Tutorial', 'Listicle', 'Review', 'Vlog', 'Reaction'], type: 'select' },
    { label: 'Inclure tendances', name: 'trending', type: 'boolean' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'أفكار المحتوى', fr: 'Idées de Contenu', en: 'Content Ideas' },
  outputs: [{ name: 'ideas', type: 'markdown' }],
  slug: 'youtube-content-ideas',
  priority: 'critical',
  promptTemplate: `Génère 30 idées de vidéos :

NICHE : {{channel_niche}}
AUDIENCE : {{target_audience}}
TYPE : {{content_type}}

🔥 VIRAL (10) - Fort potentiel
📚 EVERGREEN (10) - SEO long terme
🎯 NICHE (5) - Audience fidèle
📈 TENDANCES (5) - Actualités

+ Calendrier éditorial 4 semaines`,
  subcategory: 'ideation'
};

export const youtubeIntroOutroScript: AITool = {
  category: 'youtube',
  credits: 12,
  description: {
    ar: 'قم بإنشاء مقدمات قوية وخواتم تحويلية',
    en: 'Create impactful intros and outros that convert',
    fr: 'Créez des intros percutantes et des outros qui convertissent'
  },
  icon: 'Play',
  id: 'youtube-intro-outro-script',
  inputs: [
    { label: 'Nom de la chaîne', name: 'channel_name', required: true, type: 'text' },
    { label: 'Niche', name: 'channel_niche', type: 'text' },
    { label: 'Style Intro', name: 'intro_style', options: ['Direct', 'Branding', 'Teaser', 'Minimal'], type: 'select' },
    { label: 'CTAs (ex: like, abonnement, cloche)', name: 'cta_types', type: 'text' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مقدمة وخاتمة', fr: 'Script Intro/Outro', en: 'Intro/Outro Script' },
  outputs: [{ name: 'introOutro', type: 'markdown' }],
  slug: 'youtube-intro-outro-script',
  priority: 'critical',
  promptTemplate: `Génère 3 versions d'intro (15-25 sec) et 2 versions d'outro.

CHAÎNE : {{channel_name}}
NICHE : {{channel_niche}}
STYLE : {{intro_style}}
CTA : {{cta_types}}

Inclus :
- Script mot à mot
- Timing précis
- Instructions écran de fin`,
  subcategory: 'content'
};
