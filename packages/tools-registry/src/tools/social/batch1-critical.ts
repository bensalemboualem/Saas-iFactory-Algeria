import { AITool } from '../../types';

export const instagramCaptionGenerator: AITool = {
  category: 'social',
  credits: 8,
  description: {
    ar: 'أنشئ تعليقات انستغرام جذابة تزيد التفاعل',
    en: 'Create engaging Instagram captions that boost engagement',
    fr: 'Créez des légendes Instagram engageantes qui boostent vos interactions'
  },
  icon: 'Instagram',
  id: 'instagram-caption-generator',
  inputs: [
    { label: 'Sujet du post', name: 'post_topic', required: true, type: 'text' },
    { label: 'Type de post', name: 'post_type', options: ['Photo', 'Carrousel', 'Reel', 'Story'], type: 'select' },
    { label: 'Ton', name: 'tone', options: ['Inspirant', 'Humoristique', 'Informatif', 'Personnel', 'Promotionnel'], type: 'select' },
    { label: 'Appel à l\'action', name: 'include_cta', options: ['Like', 'Comment', 'Save', 'Share', 'Link bio', 'None'], type: 'select' },
    { default: true, label: 'Générer les hashtags', name: 'include_hashtags', type: 'boolean' },
    { label: 'Niche/Secteur', name: 'niche', type: 'text' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد تعليقات انستغرام', fr: 'Générateur de Légendes Instagram', en: 'Instagram Caption Generator' },
  outputs: [{ name: 'captions', type: 'markdown' }],
  slug: 'instagram-caption-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert Instagram avec 1M+ followers.

SUJET : {{post_topic}}
TYPE : {{post_type}}
TON : {{tone}}
CTA : {{include_cta}}
NICHE : {{niche}}

## 📸 5 LÉGENDES INSTAGRAM

### Version 1 : Accroche + Valeur
"[Première ligne ACCROCHEUSE - visible avant 'plus']

[Corps du texte - 2-3 paragraphes avec espaces]

{{#if include_cta === 'Comment'}}
💬 Et vous, [question engageante] ? Dites-moi en commentaire ⬇️
{{/if}}

{{#if include_hashtags}}
.
.
.
#hashtag1 #hashtag2 #hashtag3..."
{{/if}}

### Version 2 : Storytelling
[Histoire personnelle + leçon]

### Version 3 : Liste/Tips
[Format liste avec emojis]

### Version 4 : Question d'engagement
[Débute par une question]

### Version 5 : Minimaliste
[Court et percutant - 1-2 lignes]

---

## 🏷️ HASHTAGS RECOMMANDÉS (30)

**Populaires (10)** - Portée large
#[hashtag] (X millions de posts)
...

**Moyens (10)** - Équilibre
#[hashtag] (100K-1M posts)
...

**Niche (10)** - Ciblés
#[hashtag] (<100K posts)
...

**Stratégie :** Mix de 20-25 hashtags par post`,
  subcategory: 'instagram'
};

export const instagramHashtagGenerator: AITool = {
  category: 'social',
  credits: 8,
  description: {
    ar: 'اعثر على الهاشتاجات الأكثر ملاءمة لمجالك',
    en: 'Find the most relevant hashtags for your niche',
    fr: 'Trouvez les hashtags les plus pertinents pour votre niche'
  },
  icon: 'Hash',
  id: 'instagram-hashtag-generator',
  inputs: [
    { label: 'Sujet/Niche', name: 'topic', required: true, type: 'text' },
    { label: 'Localisation (optionnel)', name: 'location', placeholder: 'Algérie, Paris...', type: 'text' },
    { label: 'Nombre de hashtags', name: 'hashtag_count', options: ['10', '20', '30'], type: 'select' },
    { name: 'language', options: ['fr', 'ar', 'en', 'mix'], type: 'select' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد الهاشتاغ', fr: 'Générateur de Hashtags', en: 'Hashtag Generator' },
  outputs: [{ name: 'hashtags', type: 'markdown' }],
  slug: 'instagram-hashtag-generator',
  priority: 'critical',
  promptTemplate: `Génère {{hashtag_count}} hashtags Instagram optimisés.

SUJET : {{topic}}
LOCALISATION : {{location}}
LANGUE : {{language}}

## 🏷️ HASHTAGS STRATÉGIQUES

### 🔥 Haute compétition (5) - Visibilité
[Hashtags 1M+ posts - pour la découverte]

### ⚡ Moyenne compétition (10) - Équilibre
[Hashtags 100K-1M - meilleur ratio]

### 🎯 Niche (10) - Engagement
[Hashtags <100K - communauté ciblée]

### 📍 Locaux {{location}} (5)
[Hashtags géographiques]

---

**SET PRÊT À COPIER :**
\`\`\`
#hashtag1 #hashtag2 #hashtag3...
\`\`\`

**Conseils :**
- Placer en commentaire ou après des points
- Varier les sets entre les posts
- Éviter les hashtags bannis`,
  subcategory: 'instagram'
};

export const tiktokCaptionGenerator: AITool = {
  category: 'social',
  credits: 8,
  description: {
    ar: 'تعليقات قصيرة ومؤثرة لتيك توك وريلز',
    en: 'Short and punchy captions for TikTok and Reels',
    fr: 'Légendes courtes et percutantes pour TikTok et Reels'
  },
  icon: 'Music',
  id: 'tiktok-caption-generator',
  inputs: [
    { label: 'Sujet de la vidéo', name: 'video_topic', required: true, type: 'text' },
    { label: 'Style', name: 'video_style', options: ['Trend', 'Educational', 'Storytime', 'Comedy', 'Lifestyle', 'Business'], type: 'select' },
    { label: 'Audience', name: 'target_audience', options: ['Gen Z', 'Millennials', 'All'], type: 'select' },
    { default: true, label: 'Inclure sons/trends actuels', name: 'include_trending', type: 'boolean' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'تعليقات تيك توك', fr: 'Légendes TikTok', en: 'TikTok Caption Generator' },
  outputs: [{ name: 'captions', type: 'markdown' }],
  slug: 'tiktok-caption-generator',
  priority: 'critical',
  promptTemplate: `Tu es un créateur TikTok viral.

SUJET : {{video_topic}}
STYLE : {{video_style}}
AUDIENCE : {{target_audience}}

## 🎵 5 LÉGENDES TIKTOK

**Règles TikTok :**
- 150 caractères max (visible sans cliquer)
- Hook immédiat
- Hashtags pertinents (4-5 max)
- Emoji stratégiques

### Version 1 : Mystère
"Personne ne parle de ça... 🤫 #fyp #pourtoi #[niche]"

### Version 2 : POV
"POV: [situation relatable] #relatable #fyp"

### Version 3 : Défi/Question
"Est-ce que quelqu'un peut m'expliquer [X] ?? 😭 #help #[niche]"

### Version 4 : Éducatif
"3 choses que j'aurais aimé savoir sur [X] 📚 #tips #[niche]"

### Version 5 : Trend
"Utilisant [TREND ACTUEL] pour [SUJET] 🔥 #trend #viral"

---

**Hashtags TikTok 2025 :**
#fyp #foryou #pourtoi #viral #trending
+ 2-3 hashtags niche`,
  subcategory: 'tiktok'
};

export const linkedinPostGenerator: AITool = {
  category: 'social',
  credits: 12,
  description: {
    ar: 'منشورات لينكدإن احترافية محسنة للوصول والمشاركة',
    en: 'Professional LinkedIn posts optimized for reach and engagement',
    fr: 'Posts LinkedIn professionnels optimisés pour la portée et l\'engagement'
  },
  icon: 'Linkedin',
  id: 'linkedin-post-generator',
  inputs: [
    { label: 'Sujet du post', name: 'topic', required: true, type: 'text' },
    { label: 'Type de post', name: 'post_type', options: [
      'Storytelling personnel',
      'Conseils/Tips',
      'Opinion/Hot take',
      'Réalisation/Milestone',
      'Question à la communauté',
      'Carrousel (texte pour slides)'
    ], type: 'select'},
    { label: 'Ton', name: 'tone', options: ['Professionnel', 'Inspirant', 'Authentique', 'Provocateur', 'Éducatif'], type: 'select' },
    { label: 'Secteur d\'activité', name: 'industry', type: 'text' },
    { label: 'Call-to-action', name: 'cta', options: ['Comment', 'Share', 'Follow', 'DM', 'Link', 'None'], type: 'select' }
  ],
  estimatedTime: '45s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد منشورات لينكدإن', fr: 'Générateur de Posts LinkedIn', en: 'LinkedIn Post Generator' },
  outputs: [{ name: 'posts', type: 'markdown' }],
  slug: 'linkedin-post-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert LinkedIn avec des posts à 100K+ vues.

SUJET : {{topic}}
TYPE : {{post_type}}
TON : {{tone}}
SECTEUR : {{industry}}

## 💼 3 POSTS LINKEDIN OPTIMISÉS

### Post 1 : Format Storytelling

[Accroche choc sur 1 ligne]

[Espace]

[Histoire personnelle en 3-4 paragraphes courts]
[Utiliser des retours à la ligne fréquents]
[Une idée par ligne]

[Espace]

[Leçon/Takeaway]

[Espace]

[CTA : Question ou appel à l'action]

---

### Post 2 : Format Liste

[Accroche avec chiffre]

Voici [X] leçons que j'ai apprises :

1️⃣ [Point 1]
↳ [Explication courte]

2️⃣ [Point 2]
↳ [Explication courte]

3️⃣ [Point 3]
↳ [Explication courte]

[CTA]

♻️ Repostez si ça vous parle

---

### Post 3 : Format Opinion/Hot Take

[Affirmation controversée]

[Espace]

Voici pourquoi :

[Argument 1]
[Argument 2]
[Argument 3]

[Espace]

D'accord ou pas d'accord ?

---

**Bonnes pratiques LinkedIn :**
✅ Hook puissant (3 premières lignes)
✅ Espaces entre paragraphes
✅ Une idée = une ligne
✅ Pas de liens dans le post (en commentaire)
✅ Emoji avec modération
✅ 1200-1500 caractères optimal`,
  subcategory: 'linkedin'
};

export const twitterThreadGenerator: AITool = {
  category: 'social',
  credits: 15,
  description: {
    ar: 'حول موضوعًا إلى ثريد تويتر جذاب',
    en: 'Transform a topic into a captivating Twitter thread',
    fr: 'Transformez un sujet en thread Twitter captivant'
  },
  icon: 'Twitter',
  id: 'twitter-thread-generator',
  inputs: [
    { label: 'Sujet du thread', name: 'topic', required: true, type: 'text' },
    { label: 'Longueur', name: 'thread_length', options: ['5 tweets', '10 tweets', '15 tweets', '20 tweets'], type: 'select' },
    { label: 'Type', name: 'thread_type', options: ['Educational', 'Story', 'Tips', 'Analysis', 'Controversial'], type: 'select' },
    { default: true, label: 'Inclure CTA final', name: 'include_cta', type: 'boolean' }
  ],
  estimatedTime: '40s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد ثريدات تويتر', fr: 'Générateur de Threads Twitter/X', en: 'Twitter Thread Generator' },
  outputs: [{ name: 'thread', type: 'markdown' }],
  slug: 'twitter-thread-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert Twitter/X avec des threads viraux.

SUJET : {{topic}}
LONGUEUR : {{thread_length}}
TYPE : {{thread_type}}

## 🧵 THREAD TWITTER/X

### Tweet 1 (HOOK) 🪝
"[Accroche percutante]

[Promesse de valeur]

🧵 Thread :"

---

### Tweet 2
"1/ [Premier point]

[Développement]"

### Tweet 3
"2/ [Deuxième point]

[Développement]"

[... continuer selon {{thread_length}}]

---

### Tweet Final (CTA)
"[X]/ Récap :

- [Point 1]
- [Point 2]
- [Point 3]

Si ce thread vous a aidé :
→ RT le premier tweet
→ Follow @[compte] pour plus

[Emoji]"

---

**Bonnes pratiques :**
✅ Hook tweet 1 = succès du thread
✅ Un concept par tweet
✅ Numéroter (1/, 2/, 3/...)
✅ Images/screenshots augmentent l'engagement
✅ Poster entre 8h-9h ou 17h-18h`,
  subcategory: 'twitter'
};

export const facebookPostGenerator: AITool = {
  category: 'social',
  credits: 10,
  description: {
    ar: 'أنشئ منشورات فيسبوك جذابة لصفحتك أو مجموعتك',
    en: 'Create engaging Facebook posts for your page or group',
    fr: 'Créez des posts Facebook engageants pour votre page ou groupe'
  },
  icon: 'Facebook',
  id: 'facebook-post-generator',
  inputs: [
    { label: 'Sujet', name: 'topic', required: true, type: 'text' },
    { label: 'Type', name: 'post_type', options: ['Page business', 'Groupe', 'Personnel', 'Événement', 'Pub'], type: 'select' },
    { label: 'Objectif', name: 'objective', options: ['Engagement', 'Trafic', 'Ventes', 'Notoriété', 'Communauté'], type: 'select' },
    { name: 'tone', options: ['Professionnel', 'Amical', 'Humoristique', 'Informatif'], type: 'select' },
    { default: true, name: 'include_emoji', type: 'boolean' }
  ],
  estimatedTime: '25s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد منشورات فيسبوك', fr: 'Générateur de Posts Facebook', en: 'Facebook Post Generator' },
  outputs: [{ name: 'posts', type: 'markdown' }],
  slug: 'facebook-post-generator',
  priority: 'critical',
  promptTemplate: `Génère un post Facebook optimisé pour l'engagement.

SUJET : {{topic}}
TYPE : {{post_type}}
OBJECTIF : {{objective}}
TON : {{tone}}

## 📘 3 POSTS FACEBOOK

### Version 1 : Engagement
"[Question ou affirmation engageante]

[Corps du texte avec histoire ou valeur]

{{#if include_emoji}}👇{{/if}} [CTA clair]"

### Version 2 : Informatif
[Format avec valeur éducative]

### Version 3 : Personnel/Authentique
[Format storytelling]

---

**Optimisations Facebook :**
- Longueur idéale : 100-250 caractères
- Les questions génèrent 2x plus de commentaires
- Les images natives > liens externes
- Heures optimales : 13h-16h`,
  subcategory: 'facebook'
};

export const socialMediaCalendar: AITool = {
  category: 'social',
  credits: 20,
  description: {
    ar: 'أنشئ خطة محتوى كاملة عبر منصات متعددة',
    en: 'Generate a complete content plan across multiple platforms',
    fr: 'Générez un plan de contenu complet sur multi-plateformes'
  },
  icon: 'Calendar',
  id: 'social-media-calendar',
  inputs: [
    { label: 'Type d\'activité', name: 'business_type', required: true, type: 'text' },
    { label: 'Plateformes (ex: Instagram, TikTok)', name: 'platforms', required: true, type: 'text' },
    { label: 'Fréquence par plateforme', name: 'posting_frequency', options: ['Daily', '3/week', 'Weekly'], type: 'select' },
    { label: 'Piliers de contenu (3-5 thèmes)', name: 'content_pillars', type: 'text' },
    { label: 'Durée du calendrier', name: 'duration', options: ['1 semaine', '2 semaines', '1 mois'], type: 'select' }
  ],
  estimatedTime: '60s',
  isAlgeriaExclusive: false,
  model: 'gpt4',
  name: { ar: 'تقويم وسائل التواصل', fr: 'Calendrier Réseaux Sociaux', en: 'Social Media Calendar' },
  outputs: [{ name: 'calendar', type: 'markdown' }],
  slug: 'social-media-calendar',
  priority: 'critical',
  promptTemplate: `Tu es un social media manager expert.

ACTIVITÉ : {{business_type}}
PLATEFORMES : {{platforms}}
FRÉQUENCE : {{posting_frequency}}
PILIERS : {{content_pillars}}
DURÉE : {{duration}}

## 📅 CALENDRIER ÉDITORIAL

### SEMAINE 1

| Jour | Plateforme | Type | Sujet | Heure |
|------|------------|------|-------|-------|
| Lun | Instagram | Carrousel | [Sujet] | 12h |
| Lun | LinkedIn | Post texte | [Sujet] | 9h |
| Mar | TikTok | Reel | [Sujet] | 19h |
| Mer | Instagram | Story | [Sujet] | 18h |
| Jeu | Twitter | Thread | [Sujet] | 8h |
| Ven | Instagram | Reel | [Sujet] | 12h |
| Sam | Facebook | Post | [Sujet] | 10h |
| Dim | Instagram | Photo | [Sujet] | 11h |

[Répéter pour chaque semaine]

---

## 📊 RÉPARTITION PAR PILIER

| Pilier | % du contenu | Types suggérés |
|--------|--------------|----------------|
| Pilier 1 | 30% | Carrousels, Threads |
| Pilier 2 | 25% | Reels, Stories |
| Pilier 3 | 25% | Posts, Photos |
| Pilier 4 | 20% | Behind scenes, Personnel |

---

## 🎯 THÈMES HEBDOMADAIRES

- **Lundi** : Motivation / Mindset
- **Mardi** : Tips / Éducatif
- **Mercredi** : Behind the scenes
- **Jeudi** : Témoignage / Résultats
- **Vendredi** : Fun / Tendances
- **Weekend** : Personnel / Communauté

---

## 📝 IDÉES DE CONTENU (30)

### Pilier 1
1. [Idée]
2. [Idée]
...

[Répéter pour chaque pilier]`,
  subcategory: 'strategy'
};

export const instagramBioGenerator: AITool = {
  category: 'social',
  credits: 8,
  description: {
    ar: 'أنشئ السيرة الذاتية المثالية لتحويل الزوار إلى متابعين',
    en: 'Create the perfect bio to convert visitors into followers',
    fr: 'Créez la bio parfaite pour convertir les visiteurs en abonnés'
  },
  icon: 'User',
  id: 'instagram-bio-generator',
  inputs: [
    { label: 'Nom ou marque', name: 'name_or_brand', required: true, type: 'text' },
    { label: 'Niche/Secteur', name: 'niche', required: true, type: 'text' },
    { label: 'Ce qui vous différencie', name: 'unique_value', type: 'text' },
    { label: 'Appel à l\'action', name: 'cta', options: ['Website', 'DM', 'Email', 'Shop', 'Youtube', 'Linktree'], type: 'select' },
    { label: 'Style', name: 'style', options: ['Professionnel', 'Fun', 'Minimaliste', 'Emoji rich'], type: 'select' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد بايو انستغرام', fr: 'Générateur de Bio Instagram', en: 'Instagram Bio Generator' },
  outputs: [{ name: 'bios', type: 'markdown' }],
  slug: 'instagram-bio-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert en personal branding Instagram.

NOM : {{name_or_brand}}
NICHE : {{niche}}
USP : {{unique_value}}
CTA : {{cta}}
STYLE : {{style}}

## 📱 10 BIOS INSTAGRAM (150 caractères max)

### Style Professionnel
1. "{{niche}} Expert 🎯
Helping [audience] achieve [résultat]
📩 DM for collabs
⬇️ [CTA]"

2. "[Titre] | [Spécialité]
[Résultat que vous apportez]
[CTA emoji] [lien]"

### Style Fun/Créatif
3. "[Emoji] [Phrase d'accroche fun]
[Ce que vous faites] sans [problème courant]
[CTA avec emoji]"

### Style Minimaliste
4. "[Niche]. [Valeur]. [CTA]."

### Style avec Chiffres
5. "[X]+ [réalisation] | [X]K followers sur [autre plateforme]
[Ce que vous faites]
[CTA]"

[... 5 autres versions]

---

**Structure optimale :**
Ligne 1 : Qui vous êtes (titre/niche)
Ligne 2 : Ce que vous apportez (valeur)
Ligne 3 : Preuve sociale (optionnel)
Ligne 4 : CTA clair

**Caractères spéciaux tendance :**
- ➜ ★ ✦ ◆ ▪ ♡ ✿ ⚡`,
  subcategory: 'instagram'
};

export const socialMediaAdCopy: AITool = {
  category: 'social',
  credits: 15,
  description: {
    ar: 'نصوص إعلانية عالية التحويل لفيسبوك وانستغرام وتيك توك',
    en: 'High-converting ad copy for Facebook, Instagram, TikTok',
    fr: 'Textes publicitaires à haute conversion pour Facebook, Instagram, TikTok'
  },
  icon: 'Megaphone',
  id: 'social-media-ad-copy',
  inputs: [
    { label: 'Plateforme', name: 'platform', options: ['Facebook/Instagram', 'TikTok', 'LinkedIn', 'Twitter'], required: true, type: 'select' },
    { label: 'Produit/Service', name: 'product_service', required: true, type: 'text' },
    { label: 'Audience cible', name: 'target_audience', type: 'textarea' },
    { label: 'Offre/Promotion', name: 'offer', placeholder: '-20%, Essai gratuit...', type: 'text' },
    { label: 'Objectif', name: 'objective', options: ['Conversions', 'Trafic', 'Leads', 'App install', 'Awareness'], type: 'select' },
    { label: 'Format', name: 'ad_format', options: ['Image', 'Video', 'Carousel', 'Story'], type: 'select' }
  ],
  estimatedTime: '40s',
  isAlgeriaExclusive: false,
  model: 'gpt4',
  name: { ar: 'نص إعلاني للسوشيال ميديا', fr: 'Copy Publicitaire Réseaux Sociaux', en: 'Social Media Ad Copy' },
  outputs: [{ name: 'adCopy', type: 'markdown' }],
  slug: 'social-media-ad-copy',
  priority: 'critical',
  promptTemplate: `Tu es un expert en publicité sociale avec des ROAS de 5x+.

PLATEFORME : {{platform}}
PRODUIT : {{product_service}}
AUDIENCE : {{target_audience}}
OFFRE : {{offer}}
OBJECTIF : {{objective}}
FORMAT : {{ad_format}}

## 📣 COPIES PUBLICITAIRES

### Version 1 : Pain Point
**Headline :** "[Problème] ? Voici la solution."
**Primary Text :**
"[Question sur le problème]

[Présentation solution]

[Bénéfice principal]

{{offer}}

[CTA]"
**CTA Button :** [Acheter maintenant / En savoir plus / S'inscrire]

---

### Version 2 : Bénéfice Direct
**Headline :** "[Bénéfice principal] en [temps]"
**Primary Text :**
"[Résultat que le client veut]

✅ [Avantage 1]
✅ [Avantage 2]
✅ [Avantage 3]

{{offer}}

[CTA urgent]"

---

### Version 3 : Social Proof
**Headline :** "Pourquoi [X]+ personnes ont choisi [Produit]"
**Primary Text :**
"[Témoignage ou statistique]

[Liste de bénéfices]

{{offer}} - Offre limitée

[CTA]"

---

### Version 4 : FOMO
**Headline :** "⚠️ Plus que [X] disponibles"
[Version avec urgence]

---

**Specs par plateforme :**
{{#if platform.includes('Facebook')}}
- Primary text : 125 caractères visibles (600 max)
- Headline : 40 caractères
- Description : 30 caractères
{{/if}}`,
  subcategory: 'advertising'
};

export const reelsScriptGenerator: AITool = {
  category: 'social',
  credits: 12,
  description: {
    ar: 'نصوص فيديو قصيرة فيروسية لـ Instagram Reels و TikTok',
    en: 'Short viral video scripts for Instagram Reels and TikTok',
    fr: 'Scripts vidéo courts viraux pour Instagram Reels et TikTok'
  },
  icon: 'Video',
  id: 'reels-script-generator',
  inputs: [
    { label: 'Sujet', name: 'topic', required: true, type: 'text' },
    { label: 'Type de Reel', name: 'reel_type', options: [
      'Talking head', 'Trend', 'Tutorial', 'Before/After', 'Day in life', 'Tips quick', 'Storytime', 'Transition'
    ], type: 'select'},
    { label: 'Durée', name: 'duration', options: ['15s', '30s', '60s', '90s'], type: 'select' },
    { name: 'hook_style', options: ['Question', 'Statement', 'Action', 'Text screen'], type: 'select' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'سيناريو ريلز', fr: 'Script Reels/TikTok', en: 'Reels Script Generator' },
  outputs: [{ name: 'reelScript', type: 'markdown' }],
  slug: 'reels-script-generator',
  priority: 'critical',
  promptTemplate: `Tu es un créateur de Reels viraux.

SUJET : {{topic}}
TYPE : {{reel_type}}
DURÉE : {{duration}}
HOOK : {{hook_style}}

## 🎬 SCRIPT REEL ({{duration}})

### HOOK (0-3 sec) ⚡
**[STOPPER LE SCROLL]**
{{#if hook_style === 'Question'}}
Texte à l'écran : "Est-ce que tu fais cette erreur ?"
Audio : "[Question choc]"
{{/if}}

### CONTENU (3-X sec)
**Scène 1 :**
- Action : [Description]
- Texte écran : "[Texte]"
- Audio/Voix : "[Script]"

**Scène 2 :**
[Idem]

### CTA (dernières 3 sec)
- Texte : "Follow pour plus !"
- Action : [Pointer vers le bouton follow]

---

**Notes techniques :**
- Format : 9:16 vertical
- Musique suggérée : [Trending sound]
- Transitions : [Type]
- Texte : Police bold, centré

**Hashtags :**
#reels #reelsinstagram #viral #[niche]`,
  subcategory: 'instagram'
};

export const pinterestPinGenerator: AITool = {
  category: 'social',
  credits: 10,
  description: {
    ar: 'أوصاف وعناوين محسنة للسيو لبينتريست',
    en: 'SEO optimized descriptions and titles for Pinterest',
    fr: 'Descriptions et titres optimisés SEO pour Pinterest'
  },
  icon: 'Image',
  id: 'pinterest-pin-generator',
  inputs: [
    { label: 'Sujet du Pin', name: 'pin_topic', required: true, type: 'text' },
    { label: 'Type', name: 'pin_type', options: ['Standard', 'Idea pin', 'Video pin', 'Product'], type: 'select' },
    { label: 'Mot-clé SEO', name: 'target_keyword', type: 'text' },
    { label: 'Tableau cible', name: 'board_name', type: 'text' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مولد بينات بينتريست', fr: 'Générateur de Pins Pinterest', en: 'Pinterest Pin Generator' },
  outputs: [{ name: 'pins', type: 'markdown' }],
  slug: 'pinterest-pin-generator',
  priority: 'critical',
  promptTemplate: `Tu es un expert Pinterest Marketing.

SUJET : {{pin_topic}}
TYPE : {{pin_type}}
MOT-CLÉ : {{target_keyword}}

## 📌 PIN PINTEREST OPTIMISÉ

### TITRE (100 caractères max)
"[Titre accrocheur avec mot-clé]"

### DESCRIPTION (500 caractères)
"[Description SEO-friendly avec :
- Mot-clé dans les 50 premiers caractères
- Bénéfices clairs
- Call-to-action
- 3-5 hashtags pertinents]"

### TEXTE SUR L'IMAGE
"[Titre court et lisible
- Police : Bold/Sans-serif
- Contraste élevé
- 2-4 lignes max]"

### ALT TEXT (SEO)
"[Description pour accessibilité avec mot-clé]"

---

**Specs Pinterest :**
- Ratio idéal : 2:3 (1000x1500 px)
- Couleurs vives = plus de saves
- Visage humain = +23% engagement`,
  subcategory: 'pinterest'
};

export const socialMediaAudit: AITool = {
  category: 'social',
  credits: 25,
  description: {
    ar: 'تحليل كامل لوجودك الاجتماعي وتوصيات',
    en: 'Complete analysis of your social presence and recommendations',
    fr: 'Analyse complète de votre présence sociale et recommandations'
  },
  icon: 'ClipboardCheck',
  id: 'social-media-audit',
  inputs: [
    { label: 'Nom de la marque/compte', name: 'brand_name', required: true, type: 'text' },
    { label: 'Plateformes à auditer', name: 'platforms', type: 'text' },
    { label: 'Followers par plateforme', name: 'followers_per_platform', type: 'textarea' },
    { label: 'Fréquence actuelle de publication', name: 'posting_frequency', type: 'text' },
    { label: 'Défis principaux', name: 'main_challenges', type: 'textarea' },
    { label: 'Concurrents (optionnel)', name: 'competitors', type: 'textarea' }
  ],
  estimatedTime: '60s',
  isAlgeriaExclusive: false,
  model: 'gpt4',
  name: { ar: 'تدقيق وسائل التواصل', fr: 'Audit Réseaux Sociaux', en: 'Social Media Audit' },
  outputs: [{ name: 'audit', type: 'markdown' }],
  slug: 'social-media-audit',
  priority: 'critical',
  promptTemplate: `Tu es un consultant social media senior.

MARQUE : {{brand_name}}
PLATEFORMES : {{platforms}}
FOLLOWERS : {{followers_per_platform}}
FRÉQUENCE : {{posting_frequency}}
DÉFIS : {{main_challenges}}

## 📊 AUDIT RÉSEAUX SOCIAUX COMPLET

### 1. SCORE GLOBAL : X/100

| Critère | Score | Statut |
|---------|-------|--------|
| Cohérence branding | X/20 | ✅/⚠️/❌ |
| Qualité contenu | X/20 | ✅/⚠️/❌ |
| Engagement rate | X/20 | ✅/⚠️/❌ |
| Fréquence | X/20 | ✅/⚠️/❌ |
| Croissance | X/20 | ✅/⚠️/❌ |

### 2. ANALYSE PAR PLATEFORME

#### Instagram
**Points forts :**
- [Force 1]
**À améliorer :**
- [Faiblesse 1] → [Solution]

[Répéter pour chaque plateforme]

### 3. BENCHMARK CONCURRENCE

[Analyse comparative]

### 4. PLAN D'ACTION (90 jours)

**Mois 1 :** [Actions prioritaires]
**Mois 2 :** [Développement]
**Mois 3 :** [Optimisation]

### 5. KPIs À SUIVRE

[Métriques clés par plateforme]`,
  subcategory: 'strategy'
};
