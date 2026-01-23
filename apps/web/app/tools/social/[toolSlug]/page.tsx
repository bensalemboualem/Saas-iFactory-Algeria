'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Play, Sparkles, Copy, Check, Loader2, Share2, Instagram, Linkedin, Twitter, Facebook, Hash, Music } from 'lucide-react';
import { socialTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

// Configuration des formulaires par outil Social Media
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {
  // ===== BATCH 1 - CRITIQUE (12 outils) =====
  'instagram-caption-generator': {
    fields: [
      { name: 'post_topic', type: 'text', label: 'Sujet du post', required: true, placeholder: 'Ex: Lancement de notre nouvelle collection' },
      { name: 'post_type', type: 'select', label: 'Type de post', options: ['Photo', 'Carrousel', 'Reel', 'Story'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Inspirant', 'Humoristique', 'Informatif', 'Personnel', 'Promotionnel'] },
      { name: 'include_cta', type: 'select', label: 'Appel à l\'action', options: ['Like', 'Commentaire', 'Save', 'Partage', 'Lien bio', 'Aucun'] },
      { name: 'niche', type: 'text', label: 'Niche/Secteur', placeholder: 'Ex: Mode, Fitness, Tech...' },
      { name: 'hashtag_count', type: 'select', label: 'Nombre de hashtags', options: ['10', '20', '30'] },
    ],
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

💬 Et vous, [question engageante] ? Dites-moi en commentaire ⬇️

.
.
.
#hashtag1 #hashtag2 #hashtag3..."

### Version 2 : Storytelling
[Histoire personnelle + leçon]

### Version 3 : Liste/Tips
[Format liste avec emojis]

### Version 4 : Question d'engagement
[Débute par une question]

### Version 5 : Minimaliste
[Court et percutant - 1-2 lignes]

---

## 🏷️ {{hashtag_count}} HASHTAGS RECOMMANDÉS

**Populaires** - Portée large
#[hashtag] ...

**Moyens** - Équilibre
#[hashtag] ...

**Niche** - Ciblés
#[hashtag] ...`
  },

  'instagram-hashtag-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet/Niche', required: true, placeholder: 'Ex: Fitness, Mode, Cuisine...' },
      { name: 'location', type: 'text', label: 'Localisation (optionnel)', placeholder: 'Algérie, Paris, Oran...' },
      { name: 'hashtag_count', type: 'select', label: 'Nombre de hashtags', options: ['10', '20', '30'] },
      { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais', 'Mix'] },
      { name: 'audience', type: 'select', label: 'Type d\'audience', options: ['Grand public', 'Professionnels', 'Jeunes', 'Niche spécifique'] },
    ],
    promptTemplate: `Tu es expert en SEO Instagram et hashtags viraux.

SUJET : {{topic}}
LOCALISATION : {{location}}
LANGUE : {{language}}
AUDIENCE : {{audience}}

## 🏷️ {{hashtag_count}} HASHTAGS STRATÉGIQUES

### 🔥 Haute compétition (1M+ posts) - Visibilité
[Hashtags très populaires pour la découverte]

### ⚡ Moyenne compétition (100K-1M) - Équilibre
[Meilleur ratio portée/concurrence]

### 🎯 Niche (<100K) - Engagement ciblé
[Hashtags de communauté spécifique]

### 📍 Locaux ({{location}})
[Hashtags géographiques]

---

**SET PRÊT À COPIER :**
\`\`\`
#hashtag1 #hashtag2 #hashtag3 ...
\`\`\`

**Conseils :**
- Placer en premier commentaire ou après 5 points
- Varier les sets entre les posts
- Éviter les hashtags bannis`
  },

  'tiktok-caption-generator': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: 3 astuces pour gagner du temps' },
      { name: 'video_style', type: 'select', label: 'Style', options: ['Trend', 'Éducatif', 'Storytime', 'Comedy', 'Lifestyle', 'Business'] },
      { name: 'target_audience', type: 'select', label: 'Audience', options: ['Gen Z', 'Millennials', 'Tous'] },
      { name: 'hook_type', type: 'select', label: 'Type d\'accroche', options: ['Question', 'Affirmation choc', 'POV', 'Défi', 'Mystère'] },
    ],
    promptTemplate: `Tu es un créateur TikTok viral avec des millions de vues.

SUJET : {{video_topic}}
STYLE : {{video_style}}
AUDIENCE : {{target_audience}}
HOOK : {{hook_type}}

## 🎵 5 LÉGENDES TIKTOK (150 caractères max)

**Règles TikTok :**
- 150 caractères max (visible sans cliquer)
- Hook immédiat
- 4-5 hashtags max
- Emojis stratégiques

### Version 1 : Mystère
"Personne ne parle de ça... 🤫 #fyp #pourtoi #[niche]"

### Version 2 : POV
"POV: [situation relatable] #relatable #fyp"

### Version 3 : Défi/Question
"Est-ce que quelqu'un peut m'expliquer [X] ?? 😭 #help #[niche]"

### Version 4 : Éducatif
"3 choses que j'aurais aimé savoir sur [X] 📚 #tips #[niche]"

### Version 5 : Trend
"Utilisant [TREND] pour [SUJET] 🔥 #trend #viral"

---

**Hashtags TikTok 2026 :**
#fyp #foryou #pourtoi #viral #trending
+ 2-3 hashtags niche`
  },

  'linkedin-post-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet du post', required: true, placeholder: 'Ex: Leçons de mon échec entrepreneurial' },
      { name: 'post_type', type: 'select', label: 'Type de post', options: ['Storytelling personnel', 'Conseils/Tips', 'Opinion/Hot take', 'Réalisation/Milestone', 'Question communauté', 'Carrousel (texte slides)'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Inspirant', 'Authentique', 'Provocateur', 'Éducatif'] },
      { name: 'industry', type: 'text', label: 'Secteur d\'activité', placeholder: 'Ex: Tech, Marketing, RH...' },
      { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Commentaire', 'Partage', 'Follow', 'DM', 'Lien', 'Aucun'] },
    ],
    promptTemplate: `Tu es un expert LinkedIn avec des posts à 100K+ vues.

SUJET : {{topic}}
TYPE : {{post_type}}
TON : {{tone}}
SECTEUR : {{industry}}
CTA : {{cta}}

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

### Post 3 : Format Opinion

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
✅ Pas de liens dans le post (en commentaire)
✅ 1200-1500 caractères optimal`
  },

  'twitter-thread-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet du thread', required: true, placeholder: 'Ex: Comment j\'ai construit une audience de 100K' },
      { name: 'thread_length', type: 'select', label: 'Longueur', options: ['5 tweets', '10 tweets', '15 tweets', '20 tweets'] },
      { name: 'thread_type', type: 'select', label: 'Type', options: ['Éducatif', 'Story', 'Tips', 'Analyse', 'Controversé'] },
      { name: 'include_visuals', type: 'checkbox', label: 'Suggestions d\'images/screenshots' },
    ],
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

[Développement court]"

### Tweet 3
"2/ [Deuxième point]

[Développement]"

[... continuer selon la longueur]

---

### Tweet Final (CTA)
"[X]/ Récap :

• [Point 1]
• [Point 2]
• [Point 3]

Si ce thread vous a aidé :
→ RT le premier tweet
→ Follow pour plus

🔥"

---

**Bonnes pratiques :**
✅ Hook tweet 1 = succès du thread
✅ Un concept par tweet
✅ Numéroter (1/, 2/, 3/...)
✅ Images augmentent l'engagement
✅ Poster entre 8h-9h ou 17h-18h`
  },

  'facebook-post-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet', required: true, placeholder: 'Ex: Annonce d\'un nouveau service' },
      { name: 'post_type', type: 'select', label: 'Type', options: ['Page Business', 'Groupe', 'Personnel', 'Événement', 'Pub'] },
      { name: 'objective', type: 'select', label: 'Objectif', options: ['Engagement', 'Trafic', 'Ventes', 'Notoriété', 'Communauté'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Amical', 'Humoristique', 'Informatif'] },
      { name: 'include_emoji', type: 'checkbox', label: 'Inclure des emojis' },
    ],
    promptTemplate: `Tu es expert en engagement Facebook.

SUJET : {{topic}}
TYPE : {{post_type}}
OBJECTIF : {{objective}}
TON : {{tone}}

## 📘 3 POSTS FACEBOOK

### Version 1 : Engagement
"[Question ou affirmation engageante]

[Corps du texte avec histoire ou valeur]

👇 [CTA clair]"

### Version 2 : Informatif
[Format avec valeur éducative]

### Version 3 : Personnel/Authentique
[Format storytelling]

---

**Optimisations Facebook :**
- Longueur idéale : 100-250 caractères
- Les questions = 2x plus de commentaires
- Images natives > liens externes
- Heures optimales : 13h-16h`
  },

  'social-media-calendar': {
    fields: [
      { name: 'business_type', type: 'text', label: 'Type d\'activité', required: true, placeholder: 'Ex: Restaurant, Coach fitness, Boutique mode...' },
      { name: 'platforms', type: 'select', label: 'Plateformes', options: ['Instagram seul', 'Instagram + TikTok', 'LinkedIn seul', 'Multi-plateformes'] },
      { name: 'posting_frequency', type: 'select', label: 'Fréquence', options: ['Quotidien', '3x/semaine', '2x/semaine', '1x/semaine'] },
      { name: 'content_pillars', type: 'textarea', label: 'Piliers de contenu (3-5 thèmes)', placeholder: 'Ex: Éducatif, Behind the scenes, Produits, Témoignages...' },
      { name: 'duration', type: 'select', label: 'Durée du calendrier', options: ['1 semaine', '2 semaines', '1 mois'] },
    ],
    promptTemplate: `Tu es un social media manager expert.

ACTIVITÉ : {{business_type}}
PLATEFORMES : {{platforms}}
FRÉQUENCE : {{posting_frequency}}
PILIERS : {{content_pillars}}
DURÉE : {{duration}}

## 📅 CALENDRIER ÉDITORIAL ({{duration}})

### SEMAINE 1

| Jour | Plateforme | Type | Sujet | Heure |
|------|------------|------|-------|-------|
| Lun | Instagram | Carrousel | [Sujet] | 12h |
| Mar | TikTok | Reel | [Sujet] | 19h |
| Mer | Instagram | Story | [Sujet] | 18h |
| Jeu | LinkedIn | Post texte | [Sujet] | 9h |
| Ven | Instagram | Reel | [Sujet] | 12h |
| Sam | Facebook | Post | [Sujet] | 10h |
| Dim | Instagram | Photo | [Sujet] | 11h |

[Répéter pour chaque semaine]

---

## 🎯 THÈMES HEBDOMADAIRES

- **Lundi** : Motivation / Mindset
- **Mardi** : Tips / Éducatif
- **Mercredi** : Behind the scenes
- **Jeudi** : Témoignage / Résultats
- **Vendredi** : Fun / Tendances
- **Weekend** : Personnel / Communauté

---

## 📝 30 IDÉES DE CONTENU

[Liste de 30 idées adaptées à {{business_type}}]`
  },

  'instagram-bio-generator': {
    fields: [
      { name: 'name_or_brand', type: 'text', label: 'Nom ou marque', required: true, placeholder: 'Votre nom ou nom de marque' },
      { name: 'niche', type: 'text', label: 'Niche/Secteur', required: true, placeholder: 'Ex: Coach fitness, Designer, Entrepreneur...' },
      { name: 'unique_value', type: 'text', label: 'Ce qui vous différencie', placeholder: 'Votre proposition de valeur unique' },
      { name: 'cta', type: 'select', label: 'Appel à l\'action', options: ['Site web', 'DM', 'Email', 'Shop', 'YouTube', 'Linktree'] },
      { name: 'style', type: 'select', label: 'Style', options: ['Professionnel', 'Fun', 'Minimaliste', 'Rich en emojis'] },
    ],
    promptTemplate: `Tu es expert en personal branding Instagram.

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
Ligne 1 : Qui vous êtes
Ligne 2 : Ce que vous apportez
Ligne 3 : Preuve sociale (optionnel)
Ligne 4 : CTA clair`
  },

  'social-media-ad-copy': {
    fields: [
      { name: 'platform', type: 'select', label: 'Plateforme', required: true, options: ['Facebook/Instagram Ads', 'TikTok Ads', 'LinkedIn Ads', 'Twitter Ads'] },
      { name: 'product_service', type: 'text', label: 'Produit/Service', required: true, placeholder: 'Ex: Formation en ligne, Produit physique...' },
      { name: 'target_audience', type: 'textarea', label: 'Audience cible', placeholder: 'Décrivez votre audience idéale...' },
      { name: 'offer', type: 'text', label: 'Offre/Promotion', placeholder: '-20%, Essai gratuit, Livraison offerte...' },
      { name: 'objective', type: 'select', label: 'Objectif', options: ['Conversions', 'Trafic', 'Leads', 'App install', 'Notoriété'] },
      { name: 'ad_format', type: 'select', label: 'Format', options: ['Image', 'Vidéo', 'Carrousel', 'Story'] },
    ],
    promptTemplate: `Tu es un expert en publicité sociale avec des ROAS de 5x+.

PLATEFORME : {{platform}}
PRODUIT : {{product_service}}
AUDIENCE : {{target_audience}}
OFFRE : {{offer}}
OBJECTIF : {{objective}}
FORMAT : {{ad_format}}

## 📣 3 COPIES PUBLICITAIRES

### Version 1 : Pain Point
**Headline :** "[Problème] ? Voici la solution."
**Primary Text :**
"[Question sur le problème]

[Présentation solution]

[Bénéfice principal]

{{offer}}

[CTA]"
**CTA Button :** [Acheter maintenant / En savoir plus]

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

**Specs {{platform}} :**
- Primary text : 125 caractères visibles
- Headline : 40 caractères
- Image : 1080x1080 ou 1080x1920`
  },

  'reels-script-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet', required: true, placeholder: 'Ex: 3 erreurs à éviter en cuisine' },
      { name: 'reel_type', type: 'select', label: 'Type de Reel', options: ['Talking head', 'Trend', 'Tutorial', 'Before/After', 'Day in life', 'Tips rapides', 'Storytime', 'Transition'] },
      { name: 'duration', type: 'select', label: 'Durée', options: ['15 secondes', '30 secondes', '60 secondes', '90 secondes'] },
      { name: 'hook_style', type: 'select', label: 'Style de hook', options: ['Question', 'Affirmation', 'Action', 'Texte à l\'écran'] },
    ],
    promptTemplate: `Tu es un créateur de Reels viraux.

SUJET : {{topic}}
TYPE : {{reel_type}}
DURÉE : {{duration}}
HOOK : {{hook_style}}

## 🎬 SCRIPT REEL ({{duration}})

### HOOK (0-3 sec) ⚡
**[STOPPER LE SCROLL]**
Texte à l'écran : "[Accroche visuelle]"
Audio : "[Ce que vous dites]"

### CONTENU (3-X sec)
**Scène 1 :**
- Action : [Description]
- Texte écran : "[Texte]"
- Audio : "[Script]"

**Scène 2 :**
[Idem]

**Scène 3 :**
[Idem]

### CTA (dernières 3 sec)
- Texte : "Follow pour plus !"
- Action : [Pointer vers le bouton follow]

---

**Notes techniques :**
- Format : 9:16 vertical
- Musique suggérée : [Trending sound]
- Transitions : [Type recommandé]

**Hashtags :**
#reels #reelsinstagram #viral #fyp #[niche]`
  },

  'pinterest-pin-generator': {
    fields: [
      { name: 'pin_topic', type: 'text', label: 'Sujet du Pin', required: true, placeholder: 'Ex: 10 idées de décoration salon' },
      { name: 'pin_type', type: 'select', label: 'Type', options: ['Standard', 'Idea Pin', 'Video Pin', 'Product'] },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé SEO', placeholder: 'Ex: décoration intérieure' },
      { name: 'board_name', type: 'text', label: 'Tableau cible', placeholder: 'Nom du tableau Pinterest' },
    ],
    promptTemplate: `Tu es expert Pinterest Marketing.

SUJET : {{pin_topic}}
TYPE : {{pin_type}}
MOT-CLÉ : {{target_keyword}}
TABLEAU : {{board_name}}

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
- Visage humain = +23% engagement`
  },

  'social-media-audit': {
    fields: [
      { name: 'brand_name', type: 'text', label: 'Nom de la marque/compte', required: true, placeholder: 'Votre marque ou @username' },
      { name: 'platforms', type: 'select', label: 'Plateformes à auditer', options: ['Instagram', 'TikTok', 'LinkedIn', 'Multi-plateformes'] },
      { name: 'followers', type: 'text', label: 'Nombre de followers', placeholder: 'Ex: 5K, 50K...' },
      { name: 'posting_frequency', type: 'text', label: 'Fréquence actuelle', placeholder: 'Ex: 3 posts/semaine' },
      { name: 'main_challenges', type: 'textarea', label: 'Défis principaux', placeholder: 'Ex: Faible engagement, peu de croissance...' },
    ],
    promptTemplate: `Tu es un consultant social media senior.

MARQUE : {{brand_name}}
PLATEFORMES : {{platforms}}
FOLLOWERS : {{followers}}
FRÉQUENCE : {{posting_frequency}}
DÉFIS : {{main_challenges}}

## 📊 AUDIT RÉSEAUX SOCIAUX

### 1. SCORE GLOBAL : X/100

| Critère | Score | Statut |
|---------|-------|--------|
| Cohérence branding | X/20 | ✅/⚠️/❌ |
| Qualité contenu | X/20 | ... |
| Engagement rate | X/20 | ... |
| Fréquence | X/20 | ... |
| Croissance | X/20 | ... |

### 2. ANALYSE DÉTAILLÉE

**Points forts :**
- [Force 1]
- [Force 2]

**À améliorer :**
- [Faiblesse 1] → [Solution]
- [Faiblesse 2] → [Solution]

### 3. BENCHMARK

[Comparaison avec standards du secteur]

### 4. PLAN D'ACTION (90 jours)

**Mois 1 :** [Actions prioritaires]
**Mois 2 :** [Développement]
**Mois 3 :** [Optimisation]

### 5. KPIs À SUIVRE

[Métriques clés recommandées]`
  },

  // ===== BATCH 2 - HAUTE PRIORITÉ (12 outils) =====
  'linkedin-headline-generator': {
    fields: [
      { name: 'current_role', type: 'text', label: 'Poste actuel', required: true, placeholder: 'Ex: Directeur Marketing' },
      { name: 'industry', type: 'text', label: 'Secteur d\'activité', required: true, placeholder: 'Ex: Tech, Finance, Marketing...' },
      { name: 'target_audience', type: 'select', label: 'Audience cible', options: ['Recruteurs', 'Clients potentiels', 'Réseau professionnel', 'Investisseurs'] },
      { name: 'unique_value', type: 'text', label: 'Votre valeur unique', placeholder: 'Ce qui vous différencie des autres' },
      { name: 'keywords', type: 'text', label: 'Mots-clés SEO à inclure', placeholder: 'Ex: Growth, Data, Leadership...' },
      { name: 'style', type: 'select', label: 'Style', options: ['Classique', 'Créatif', 'Résultats', 'Mission'] },
    ],
    promptTemplate: `Tu es un expert LinkedIn avec un profil optimisé à 100%.

POSTE : {{current_role}}
SECTEUR : {{industry}}
AUDIENCE : {{target_audience}}
VALEUR : {{unique_value}}
MOTS-CLÉS : {{keywords}}

## 💼 10 TITRES LINKEDIN (220 caractères max)

### Style Classique (Poste + Entreprise)
1. "{{current_role}} | [Spécialité] | [Entreprise]"
2. "[Titre] chez [Entreprise] | Expert en [domaine]"

### Style Créatif (Accroche + Valeur)
3. "J'aide [audience] à [résultat] grâce à [méthode] | {{current_role}}"
4. "[Passion] + [Expertise] = [Résultat] | {{current_role}}"

### Style Résultats (Chiffres)
5. "[X]+ [réalisations] | [X] ans d'expérience en [domaine] | {{current_role}}"
6. "De [situation A] à [situation B] | J'accompagne [audience]"

### Style Mission
7. "En mission pour [objectif] | {{current_role}} | [Entreprise]"
8. "Passionné par [domaine] | [Ce que vous apportez]"

### Style Recherche d'emploi
9. "{{current_role}} | En recherche active | Expert [compétences] | Open to work"
10. "[X] ans en [domaine] | Disponible pour [type de poste]"

---

**Bonnes pratiques :**
✅ Inclure le poste exact (SEO recruteurs)
✅ Ajouter 2-3 mots-clés de votre secteur
✅ Montrer la valeur, pas juste le titre
✅ Utiliser | ou • comme séparateurs
✅ Éviter les émojis (sauf si secteur créatif)

**Formule gagnante :**
[Qui vous êtes] | [Ce que vous faites] | [Pour qui/Résultat]`
  },

  'linkedin-summary-generator': {
    fields: [
      { name: 'current_role', type: 'text', label: 'Poste actuel', required: true, placeholder: 'Ex: Directeur Marketing' },
      { name: 'years_experience', type: 'select', label: 'Années d\'expérience', options: ['1-3 ans', '3-5 ans', '5-10 ans', '10-15 ans', '15+ ans'] },
      { name: 'key_achievements', type: 'textarea', label: 'Réalisations clés (3-5)', required: true, placeholder: 'Vos plus grandes réussites avec chiffres...' },
      { name: 'skills', type: 'text', label: 'Compétences principales', placeholder: 'Ex: Leadership, Data Analysis, Growth...' },
      { name: 'target_audience', type: 'text', label: 'Qui voulez-vous attirer?', placeholder: 'Recruteurs, Clients, Investisseurs...' },
      { name: 'personality', type: 'textarea', label: 'Quelque chose de personnel', placeholder: 'Passion, valeurs, hobby...' },
      { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Me contacter', 'Se connecter', 'Visiter mon site', 'Planifier un appel', 'Télécharger'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Storytelling', 'Conversationnel', 'Inspirant'] },
    ],
    promptTemplate: `Tu es un expert en personal branding LinkedIn.

POSTE : {{current_role}}
EXPÉRIENCE : {{years_experience}}
RÉALISATIONS : {{key_achievements}}
COMPÉTENCES : {{skills}}
AUDIENCE : {{target_audience}}
PERSONNALITÉ : {{personality}}
CTA : {{cta}}
TON : {{tone}}

## 📝 RÉSUMÉ LINKEDIN (2600 caractères max)

### Version 1 : Storytelling

[Hook accrocheur - 1ère ligne visible]

---

[Paragraphe 1 : Histoire personnelle - Pourquoi vous faites ce métier]

[Paragraphe 2 : Ce que vous faites et pour qui]

[Paragraphe 3 : Vos réalisations avec chiffres]
✅ [Réalisation 1]
✅ [Réalisation 2]
✅ [Réalisation 3]

[Paragraphe 4 : Votre approche unique / Valeurs]

[Paragraphe 5 : Ce que vous cherchez actuellement]

---

🎯 [CTA clair]

📧 [Contact]
🔗 [Lien]

---

### Version 2 : Direct et Structuré

**QUI JE SUIS**
[1-2 phrases]

**CE QUE JE FAIS**
[Description claire]

**MES RÉSULTATS**
→ [Chiffre 1]
→ [Chiffre 2]
→ [Chiffre 3]

**MES COMPÉTENCES**
[Liste]

**CONTACTEZ-MOI SI**
[Cas d'usage]

---

**Optimisations :**
✅ Hook dans les 3 premières lignes (visibles)
✅ Mots-clés secteur pour le SEO
✅ Chiffres et résultats concrets
✅ Paragraphes courts (3-4 lignes)
✅ CTA en fin de section`
  },

  'twitter-bio-generator': {
    fields: [
      { name: 'name', type: 'text', label: 'Nom/Pseudo', required: true, placeholder: 'Votre nom ou pseudo' },
      { name: 'occupation', type: 'text', label: 'Ce que vous faites', required: true, placeholder: 'Votre activité principale' },
      { name: 'interests', type: 'text', label: 'Centres d\'intérêt (tweets sur...)', placeholder: 'Tech, Business, Crypto...' },
      { name: 'personality', type: 'select', label: 'Personnalité', options: ['Sérieux', 'Humoristique', 'Provocateur', 'Minimaliste', 'Inspirant'] },
      { name: 'include_location', type: 'text', label: 'Localisation (optionnel)', placeholder: 'Alger, Paris...' },
      { name: 'include_link', type: 'text', label: 'Lien à promouvoir', placeholder: 'URL de votre site/newsletter' },
    ],
    promptTemplate: `Tu es un expert Twitter/X avec 100K+ followers.

NOM : {{name}}
ACTIVITÉ : {{occupation}}
INTÉRÊTS : {{interests}}
PERSONNALITÉ : {{personality}}

## 🐦 10 BIOS TWITTER (160 caractères max)

### Style Professionnel
1. "[Occupation] | Tweets sur [sujets] | [Credential] | [CTA]"
   → X caractères

2. "[Titre] @[entreprise] | [Ce que vous partagez] | 📍[Location]"
   → X caractères

### Style Humoristique
3. "[Occupation] le jour, [passion] la nuit | Opinions personnelles | ☕️ addict"
   → X caractères

4. "Je tweete sur [sujet] pour que vous n'ayez pas à faire les erreurs que j'ai faites"
   → X caractères

### Style Minimaliste
5. "[Occupation]. [Intérêt]. [Intérêt]."
   → X caractères

6. "Building [projet] | Prev @[entreprise]"
   → X caractères

### Style Créateur
7. "[X]K sur [autre plateforme] | Je partage [contenu] | Newsletter ⬇️"
   → X caractères

### Style Provocateur
8. "[Opinion controversée sur le secteur] | [Occupation]"
   → X caractères

### Style Inspirant
9. "Helping [audience] [résultat] | [X] [réalisations] | DMs ouverts"
   → X caractères

10. "From [situation A] to [situation B] | Now sharing the journey"
    → X caractères

---

**Astuces Twitter Bio :**
✅ 160 caractères max
✅ Les 50 premiers caractères = les plus importants
✅ Utiliser des | ou • comme séparateurs
✅ Un emoji max (sauf si compte fun)
✅ CTA vers link in bio si pertinent`
  },

  'tiktok-hashtag-generator': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'De quoi parle votre vidéo?' },
      { name: 'niche', type: 'text', label: 'Niche/Catégorie', required: true, placeholder: 'Ex: Fitness, Cuisine, Mode...' },
      { name: 'video_style', type: 'select', label: 'Style de vidéo', options: ['Trend', 'Éducatif', 'Comedy', 'Lifestyle', 'Business', 'Beauty', 'Fitness'] },
      { name: 'target_country', type: 'select', label: 'Pays cible', options: ['France', 'Algérie', 'Maroc', 'Belgique', 'Canada', 'International'] },
    ],
    promptTemplate: `Tu es un expert TikTok avec des vidéos à millions de vues.

SUJET : {{video_topic}}
NICHE : {{niche}}
STYLE : {{video_style}}
PAYS : {{target_country}}

## 🎵 HASHTAGS TIKTOK OPTIMISÉS

### 🔥 Hashtags Obligatoires (FYP)
#fyp #foryou #pourtoi #foryoupage #viral #trending
→ À TOUJOURS inclure (portée maximale)

### 🎯 Hashtags Niche (5-7)
#[niche1] #[niche2] #[niche3]...
→ Votre communauté cible

### 📈 Hashtags Tendance (3-5)
#[trend2025] #[trending_sound] #[challenge]
→ Surfer sur les trends actuels

### 📍 Hashtags Locaux {{target_country}} (2-3)
#algerie #dz #alger #tiktokdz (si Algérie)
#france #tiktokfrance #french (si France)

---

**SET COMPLET (copier-coller) :**
\`\`\`
#fyp #foryou #pourtoi #viral #[niche1] #[niche2] #[niche3] #[trend1] #[local1]
\`\`\`

**Règles TikTok 2025 :**
✅ 4-6 hashtags = optimal (pas plus !)
✅ #fyp et #foryou toujours
✅ 2-3 hashtags niche
✅ 1 hashtag trend si pertinent
✅ Éviter les hashtags bannis
✅ Pas de hashtags dans le texte, juste à la fin

**Hashtags à éviter (shadowban) :**
❌ #follow4follow #like4like #spam...`
  },

  'instagram-story-ideas': {
    fields: [
      { name: 'niche', type: 'text', label: 'Niche/Secteur', required: true, placeholder: 'Ex: Fitness, Mode, Food...' },
      { name: 'goal', type: 'select', label: 'Objectif', required: true, options: ['Engagement (réponses, réactions)', 'Trafic (lien)', 'Ventes', 'Croissance (nouveaux followers)', 'Connexion (personnel)'] },
      { name: 'story_count', type: 'select', label: 'Nombre d\'idées', options: ['7', '14', '30'] },
      { name: 'include_interactive', type: 'checkbox', label: 'Inclure stickers interactifs' },
    ],
    promptTemplate: `Tu es un expert Instagram avec un taux d'engagement Stories de 15%+.

NICHE : {{niche}}
OBJECTIF : {{goal}}
NOMBRE : {{story_count}} idées

## 📱 IDÉES DE STORIES INSTAGRAM

### 🗓️ STORIES QUOTIDIENNES (7 jours)

**LUNDI - Behind the Scenes**
📸 Story 1 : "Ma routine du lundi matin" + musique
📸 Story 2 : Bureau/workspace setup
📸 Story 3 : Sondage "Votre mood du lundi ?" (😴/💪/☕)

**MARDI - Éducatif**
📸 Story 1 : "Tip du jour sur [niche]"
📸 Story 2 : Carrousel mini-tuto (3 slides)
📸 Story 3 : Quiz "Vrai ou Faux ?" sur [sujet]

**MERCREDI - Engagement**
📸 Story 1 : Question box "Posez vos questions sur [niche]"
📸 Story 2 : "Ceci ou cela ?" (2 options liées à la niche)
📸 Story 3 : Réponses aux questions (UGC)

**JEUDI - Valeur**
📸 Story 1 : "3 erreurs que je vois souvent en [niche]"
📸 Story 2 : Swipe up/Lien vers contenu
📸 Story 3 : Témoignage client + slider "C'est possible pour vous aussi"

**VENDREDI - Fun/Personnel**
📸 Story 1 : "Confession du vendredi" (personnel)
📸 Story 2 : Musique du weekend + countdown
📸 Story 3 : "Vos plans ce weekend ?" + sondage

**SAMEDI - Inspiration**
📸 Story 1 : Citation motivante
📸 Story 2 : Avant/Après ou transformation
📸 Story 3 : "Ce qui m'inspire en ce moment"

**DIMANCHE - Connexion**
📸 Story 1 : "Sunday reset" + routine
📸 Story 2 : Recommandation (livre, podcast, série)
📸 Story 3 : Preview de la semaine à venir + sondage

---

### 🎯 STORIES PAR OBJECTIF

**Pour l'engagement :**
1. Question box + réponses
2. Sondages "Ceci ou cela"
3. Quiz avec résultats
4. Slider emoji "À quel point vous êtes d'accord ?"
5. "Envoyez-moi un 🔥 si..."

**Pour les ventes :**
1. Témoignage client + lien
2. Unboxing/Démo produit
3. FAQ produit
4. Countdown promo
5. "DM pour [offre]"

---

### 🛠️ STICKERS INTERACTIFS

| Sticker | Usage | Engagement |
|---------|-------|------------|
| 📊 Sondage | Choix binaire | ⭐⭐⭐⭐⭐ |
| ❓ Question | Q&A, feedback | ⭐⭐⭐⭐⭐ |
| 📏 Slider | Opinions graduées | ⭐⭐⭐⭐ |
| 🎯 Quiz | Éducatif/fun | ⭐⭐⭐⭐ |
| ⏰ Countdown | Events, lancements | ⭐⭐⭐ |
| 🔗 Lien | Trafic externe | ⭐⭐⭐ |`
  },

  'social-proof-generator': {
    fields: [
      { name: 'raw_feedback', type: 'textarea', label: 'Retour client brut (copier-coller)', required: true, placeholder: 'Collez le témoignage ou feedback de votre client...' },
      { name: 'product_service', type: 'text', label: 'Produit/Service concerné', required: true, placeholder: 'Nom de votre offre' },
      { name: 'platform', type: 'select', label: 'Plateforme de publication', options: ['Instagram', 'LinkedIn', 'Site web', 'Facebook', 'Toutes'] },
      { name: 'format', type: 'select', label: 'Format souhaité', options: ['Citation courte', 'Mini-histoire', 'Avec chiffres', 'Avant/Après'] },
    ],
    promptTemplate: `Tu es un expert en copywriting et social proof.

FEEDBACK BRUT : "{{raw_feedback}}"
PRODUIT/SERVICE : {{product_service}}
PLATEFORME : {{platform}}
FORMAT : {{format}}

## ⭐ TÉMOIGNAGES OPTIMISÉS

### Version 1 : Citation Impactante
"[Phrase la plus percutante du témoignage]"

— [Prénom], [Titre/Contexte]

### Version 2 : Format Storytelling
**Avant :** [Situation problématique]
**Solution :** [Votre produit/service]
**Après :** [Transformation/Résultat]

"[Citation du client]"

### Version 3 : Avec Chiffres
"Grâce à [produit], j'ai [résultat chiffré] en [temps]."

📈 [Stat 1]
📈 [Stat 2]
📈 [Stat 3]

### Version 4 : Pour Instagram
[Visuel suggéré]

"[Témoignage adapté format Instagram]

✨ [Hashtags pertinents]"

---

### 📱 ADAPTATIONS PAR PLATEFORME

**Instagram :**
- Carrousel avant/après
- Story avec screenshot avis
- Reel témoignage vidéo

**LinkedIn :**
- Post avec photo client (si autorisation)
- Article case study

**Site web :**
- Section dédiée
- Pop-up avis
- Page témoignages

---

**Questions pour obtenir de meilleurs témoignages :**
1. Quel était votre plus gros problème avant ?
2. Qu'est-ce qui vous a fait hésiter ?
3. Quel résultat avez-vous obtenu ?
4. Que diriez-vous à quelqu'un qui hésite ?`
  },

  'ugc-brief-generator': {
    fields: [
      { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true, placeholder: 'Votre marque' },
      { name: 'product', type: 'text', label: 'Produit/Service', required: true, placeholder: 'Produit à promouvoir' },
      { name: 'content_type', type: 'select', label: 'Type de contenu', options: ['Unboxing', 'Review', 'Tutorial', 'Lifestyle', 'Testimonial', 'Trend'] },
      { name: 'platform', type: 'select', label: 'Plateforme cible', options: ['TikTok', 'Instagram Reels', 'Instagram Story', 'YouTube Shorts', 'Multi-plateforme'] },
      { name: 'key_messages', type: 'textarea', label: 'Messages clés à transmettre', required: true, placeholder: 'Points essentiels à mentionner...' },
      { name: 'budget', type: 'text', label: 'Budget (optionnel)', placeholder: 'Ex: 200€ + produit' },
      { name: 'deadline', type: 'text', label: 'Deadline', placeholder: 'Ex: 15 janvier 2026' },
    ],
    promptTemplate: `Tu es un directeur marketing expert en UGC.

MARQUE : {{brand_name}}
PRODUIT : {{product}}
TYPE : {{content_type}}
PLATEFORMES : {{platform}}
MESSAGES : {{key_messages}}

## 📋 BRIEF UGC PROFESSIONNEL

---

### 🏢 INFORMATIONS MARQUE

**Marque :** {{brand_name}}
**Produit :** {{product}}
**Site web :** [À compléter]
**Réseaux :** @[handles]

---

### 🎯 OBJECTIF DE LA CAMPAGNE

[Objectif principal : awareness, conversions, engagement...]

**KPIs visés :**
- [KPI 1]
- [KPI 2]

---

### 📱 LIVRABLES ATTENDUS

| Livrable | Format | Plateforme | Durée |
|----------|--------|------------|-------|
| Vidéo 1 | Vertical 9:16 | TikTok | 30-60s |
| Vidéo 2 | Vertical 9:16 | Instagram Reel | 30-60s |
| Photos | 1080x1350 | Instagram Feed | - |

---

### 📝 SCRIPT/STRUCTURE SUGGÉRÉE

**Hook (0-3s) :**
"[Suggestion d'accroche]"

**Corps (3-25s) :**
- Point 1 : [Message clé]
- Point 2 : [Bénéfice produit]
- Point 3 : [Démonstration]

**CTA (25-30s) :**
"[Call-to-action]"

---

### ✅ DO'S (À faire)

- [Instruction 1]
- [Instruction 2]
- [Instruction 3]
- Mentionner @{{brand_name}}
- Utiliser le hashtag #[hashtag]

### ❌ DON'TS (À éviter)

- [Interdit 1]
- [Interdit 2]
- Mentionner les concurrents
- Faire des claims non vérifiés

---

### 🎨 GUIDELINES VISUELLES

**Ton :** [Authentique, fun, premium...]
**Musique :** [Trending sounds OK / Musique fournie]
**Éclairage :** Naturel préféré
**Lieu :** [Intérieur, extérieur, studio...]

---

### 📅 TIMELINE

| Étape | Date |
|-------|------|
| Réception produit | [Date] |
| Premier draft | [Date] |
| Révisions | [Date] |
| Livraison finale | {{deadline}} |
| Publication | [Date] |

---

### 💰 RÉMUNÉRATION

[Montant et conditions]

### 📄 DROITS D'UTILISATION

[Droits cédés : réseaux organiques, paid ads, site web...]
[Durée des droits]

---

**Contact :**
[Nom] - [Email] - [Téléphone]`
  },

  'influencer-outreach-email': {
    fields: [
      { name: 'influencer_name', type: 'text', label: 'Nom de l\'influenceur', required: true, placeholder: 'Nom ou pseudo' },
      { name: 'influencer_niche', type: 'text', label: 'Niche de l\'influenceur', placeholder: 'Beauty, Fitness, Tech...' },
      { name: 'brand_name', type: 'text', label: 'Votre marque', required: true, placeholder: 'Nom de votre marque' },
      { name: 'product_service', type: 'text', label: 'Produit/Service à promouvoir', required: true },
      { name: 'collab_type', type: 'select', label: 'Type de collaboration', options: ['Gifting (produit gratuit)', 'Partenariat payé', 'Affiliation', 'Ambassadeur long terme', 'Event/Lancement'] },
      { name: 'budget', type: 'text', label: 'Budget (si payé)', placeholder: 'Ex: 500€ + produits' },
      { name: 'specific_content', type: 'text', label: 'Contenu spécifique souhaité (optionnel)', placeholder: 'Ex: Reel unboxing' },
    ],
    promptTemplate: `Tu es un expert en influencer marketing.

INFLUENCEUR : {{influencer_name}}
NICHE : {{influencer_niche}}
MARQUE : {{brand_name}}
PRODUIT : {{product_service}}
TYPE COLLAB : {{collab_type}}

## 📧 3 EMAILS D'APPROCHE

### Email 1 : Approche Personnalisée

**Objet :** Collab {{brand_name}} x {{influencer_name}} ? 🎁

---

Salut {{influencer_name}} !

[Paragraphe 1 : Compliment sincère et SPÉCIFIQUE sur son contenu]
→ Mentionner une vidéo/post précis qu'on a aimé

[Paragraphe 2 : Présentation courte de la marque]
→ En 2 phrases max, ce qu'on fait

[Paragraphe 3 : La proposition]
→ Type de collab + ce qu'on offre

[Paragraphe 4 : CTA simple]
→ "Ça te dit d'en discuter ?"

À très vite,
[Signature]

---

### Email 2 : Approche Directe/Pro

**Objet :** Partenariat {{brand_name}} - [Montant/Gifting]

---

Bonjour {{influencer_name}},

[Version plus formelle et directe]
[Inclure les détails concrets : budget, livrables, timeline]

---

### Email 3 : Relance (J+5)

**Objet :** RE: Collab {{brand_name}} x {{influencer_name}} ? 🎁

---

Hey {{influencer_name}} !

Je me permets de revenir vers toi concernant mon message de la semaine dernière.

[Rappel court de la proposition]

[Nouvelle accroche ou info supplémentaire]

Pas de pression, dis-moi juste si ça t'intéresse ou non 😊

[Signature]

---

**Checklist avant envoi :**
✅ Objet court et intrigant
✅ Personnalisation visible
✅ Pas de copier-coller évident
✅ CTA clair et simple
✅ Signature avec liens
✅ Pas de pièces jointes (1er contact)`
  },

  'social-media-report': {
    fields: [
      { name: 'brand_name', type: 'text', label: 'Nom du client/marque', required: true, placeholder: 'Nom du client' },
      { name: 'period', type: 'select', label: 'Période', options: ['Hebdomadaire', 'Mensuel', 'Trimestriel'] },
      { name: 'platforms', type: 'select', label: 'Plateformes', options: ['Instagram', 'TikTok', 'LinkedIn', 'Twitter', 'Facebook', 'Multi-plateformes'] },
      { name: 'metrics', type: 'textarea', label: 'Métriques clés (collez vos données)', required: true, placeholder: 'Followers: X, Engagement: X%, Reach: X...' },
      { name: 'highlights', type: 'textarea', label: 'Faits marquants de la période', placeholder: 'Post viral, nouveau partenariat, milestone...' },
      { name: 'goals_next_period', type: 'textarea', label: 'Objectifs période suivante', placeholder: 'Ce que vous visez pour la prochaine période' },
    ],
    promptTemplate: `Tu es un social media manager senior présentant un rapport client.

CLIENT : {{brand_name}}
PÉRIODE : {{period}}
PLATEFORMES : {{platforms}}
MÉTRIQUES : {{metrics}}
HIGHLIGHTS : {{highlights}}

## 📊 RAPPORT SOCIAL MEDIA

### {{brand_name}} | Rapport {{period}}
**Période :** [Dates]
**Préparé par :** [Nom]

---

### 📈 RÉSUMÉ EXÉCUTIF

[3-4 phrases résumant la performance globale]

**Score de performance :** X/10

---

### 🎯 KPIs PRINCIPAUX

| Métrique | Ce mois | Mois précédent | Évolution |
|----------|---------|----------------|-----------|
| Followers | X | X | +X% ✅ |
| Engagement Rate | X% | X% | +X% ✅ |
| Reach | X | X | -X% ⚠️ |
| Impressions | X | X | +X% ✅ |

---

### 📱 PERFORMANCE PAR PLATEFORME

#### Instagram
- Followers : X (+X%)
- Engagement : X%
- Top post : [Description]
- Reach : X

[Répéter pour chaque plateforme]

---

### 🏆 TOP CONTENUS DU MOIS

| # | Contenu | Plateforme | Engagement | Reach |
|---|---------|------------|------------|-------|
| 1 | [Titre] | Instagram | X | X |
| 2 | [Titre] | TikTok | X | X |
| 3 | [Titre] | LinkedIn | X | X |

**Analyse :** [Pourquoi ces contenus ont performé]

---

### 📉 CONTENUS À AMÉLIORER

[Analyse des contenus moins performants]

---

### 💡 INSIGHTS & RECOMMANDATIONS

1. **[Insight 1]**
   → Action recommandée

2. **[Insight 2]**
   → Action recommandée

3. **[Insight 3]**
   → Action recommandée

---

### 🎯 OBJECTIFS PÉRIODE SUIVANTE

1. [Objectif SMART 1]
2. [Objectif SMART 2]
3. [Objectif SMART 3]

---

### 📅 PLAN D'ACTION

| Action | Responsable | Deadline |
|--------|-------------|----------|
| [Action 1] | [Nom] | [Date] |
| [Action 2] | [Nom] | [Date] |

---

*Rapport généré le [Date]*`
  },

  'content-repurpose-planner': {
    fields: [
      { name: 'original_content', type: 'select', label: 'Type de contenu original', required: true, options: ['Article de blog', 'Vidéo YouTube', 'Podcast', 'Webinaire', 'E-book'] },
      { name: 'content_summary', type: 'textarea', label: 'Résumé du contenu', required: true, placeholder: 'De quoi parle ce contenu...' },
      { name: 'key_points', type: 'textarea', label: 'Points clés (5-7)', required: true, placeholder: '1. Premier point\n2. Deuxième point...' },
      { name: 'target_platforms', type: 'select', label: 'Plateformes cibles', options: ['Toutes', 'Instagram + TikTok', 'LinkedIn + Twitter', 'YouTube + Email'] },
    ],
    promptTemplate: `Tu es un expert en content marketing et repurposing.

CONTENU ORIGINAL : {{original_content}}
RÉSUMÉ : {{content_summary}}
POINTS CLÉS : {{key_points}}
PLATEFORMES : {{target_platforms}}

## ♻️ PLAN DE RÉUTILISATION

### 📊 TRANSFORMATION MAP

Un {{original_content}} → 15+ contenus :

---

### 📸 INSTAGRAM (5 contenus)

1. **Carrousel éducatif**
   - 10 slides avec les points clés
   - Design suggéré : [Description]

2. **Reel "Tips rapides"**
   - 30s avec les 3 meilleurs conseils
   - Hook : "[Suggestion]"

3. **Story série (5 stories)**
   - Story 1 : Question d'intro
   - Stories 2-4 : Points clés
   - Story 5 : CTA vers le contenu complet

4. **Citation visuelle**
   - La phrase la plus impactante du contenu

5. **Behind the scenes**
   - Le process de création

---

### 🎵 TIKTOK (3 contenus)

1. **Version condensée (60s)**
   - Les points essentiels en format rapide

2. **POV/Storytelling**
   - Angle personnel sur le sujet

3. **Trend adaptation**
   - Adapter à un format trending

---

### 💼 LINKEDIN (3 contenus)

1. **Post long-form**
   - Storytelling + leçons

2. **Carrousel PDF**
   - Version slides du contenu

3. **Article LinkedIn**
   - Version adaptée du blog

---

### 🐦 TWITTER (3 contenus)

1. **Thread (10 tweets)**
   - Chaque point clé = 1 tweet

2. **Tweet unique accrocheur**
   - Le message principal

3. **Thread "Ce que j'ai appris"**
   - Angle personnel

---

### 📧 EMAIL (2 contenus)

1. **Newsletter digest**
   - Résumé + lien

2. **Email séquence**
   - Série de 3 emails sur le sujet

---

### 📌 PINTEREST (2 contenus)

1. **Infographie**
   - Les stats/points clés visuels

2. **Pin article**
   - Image + lien vers le blog

---

## 📅 CALENDRIER DE PUBLICATION

| Jour | Plateforme | Contenu |
|------|------------|---------|
| J+0 | Blog/YouTube | Original |
| J+1 | LinkedIn | Post long |
| J+2 | Instagram | Carrousel |
| J+3 | Twitter | Thread |
| J+4 | TikTok | Reel |
| J+5 | Email | Newsletter |
| J+7 | Instagram | Reel |

**Règle d'or :** 1 contenu original = 3 semaines de contenu recyclé`
  },

  'viral-hook-generator': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet du contenu', required: true, placeholder: 'De quoi parle votre contenu?' },
      { name: 'platform', type: 'select', label: 'Plateforme principale', options: ['TikTok', 'Instagram', 'YouTube', 'LinkedIn', 'Twitter', 'Toutes'] },
      { name: 'hook_type', type: 'select', label: 'Type de hook', options: ['Curiosité', 'Controverse', 'Story', 'Statistique', 'Question', 'Promesse', 'Peur', 'Erreur'] },
      { name: 'target_emotion', type: 'select', label: 'Émotion cible', options: ['Curiosité', 'Surprise', 'FOMO', 'Identification', 'Inspiration'] },
    ],
    promptTemplate: `Tu es un expert en viralité avec des contenus à millions de vues.

SUJET : {{topic}}
PLATEFORME : {{platform}}
TYPE : {{hook_type}}
ÉMOTION : {{target_emotion}}

## 🪝 25 HOOKS VIRAUX

### 🤔 CURIOSITÉ (5)
1. "Personne ne parle de ça, mais..."
2. "Ce que [experts] ne veulent pas que tu saches sur [sujet]"
3. "J'ai découvert pourquoi [situation commune] et c'est choquant"
4. "La vraie raison derrière [phénomène]..."
5. "Ouvrez pas cette vidéo si vous voulez continuer à [croyance]"

### 🔥 CONTROVERSE (5)
6. "[Opinion impopulaire] et voici pourquoi..."
7. "Je vais me faire détester mais [vérité]"
8. "Arrêtez de [conseil commun], voici ce qui marche vraiment"
9. "[X] est une arnaque. Voici la preuve."
10. "Tout le monde fait [erreur] et personne n'en parle"

### 📖 STORYTELLING (5)
11. "Il y a [temps], j'étais [situation], maintenant [résultat]"
12. "L'histoire de comment j'ai [réalisation] en partant de [rien]"
13. "Ce jour-là, tout a changé quand [événement]"
14. "J'ai failli abandonner [chose], et puis [tournant]"
15. "Mon plus gros échec m'a appris [leçon]"

### 📊 STATISTIQUE (5)
16. "[X]% des gens font cette erreur avec [sujet]"
17. "Seulement [X]% des gens savent que [fait]"
18. "[Chiffre choc] - et voici ce que ça signifie pour vous"
19. "J'ai analysé [X] [choses] et voici ce que j'ai trouvé"
20. "Les [X] qui [réussissent] font tous [chose]"

### ❓ QUESTION (5)
21. "Est-ce que tu fais aussi cette erreur avec [sujet] ?"
22. "Pourquoi est-ce que [situation frustrante] ?"
23. "Tu savais que [fait surprenant] ?"
24. "Et si tout ce qu'on t'a dit sur [sujet] était faux ?"
25. "Qui d'autre en a marre de [problème] ?"

---

**Règles d'or des hooks :**
✅ 3 secondes max pour capturer
✅ Créer un "pattern interrupt"
✅ Promettre une valeur claire
✅ Créer une tension/curiosité
✅ Parler directement au viewer (tu/vous)`
  },

  'engagement-response-templates': {
    fields: [
      { name: 'brand_voice', type: 'select', label: 'Ton de la marque', required: true, options: ['Professionnel', 'Amical', 'Humoristique', 'Premium', 'Jeune'] },
      { name: 'industry', type: 'text', label: 'Secteur d\'activité', required: true, placeholder: 'Ex: Fitness, Tech, Mode...' },
      { name: 'common_situations', type: 'select', label: 'Situations à couvrir', options: ['Toutes', 'Compliments', 'Questions produit', 'Réclamations', 'Demande prix', 'Demande collab'] },
    ],
    promptTemplate: `Tu es un community manager expert.

TON : {{brand_voice}}
SECTEUR : {{industry}}
SITUATIONS : {{common_situations}}

## 💬 BIBLIOTHÈQUE DE RÉPONSES

### ✨ COMPLIMENTS / AVIS POSITIFS

**Template 1 - Court :**
"Merci beaucoup [Prénom] ! 🙏 Ça fait vraiment plaisir !"

**Template 2 - Engagement :**
"[Prénom], ton message nous fait trop plaisir ! 😊 Qu'est-ce que tu as préféré ?"

**Template 3 - Partage :**
"Wow merci ! 🥰 Si tu as 2 secondes, un petit avis sur [plateforme] nous aiderait énormément !"

---

### ❓ QUESTIONS PRODUIT/SERVICE

**Template 1 - Réponse directe :**
"Hello [Prénom] ! [Réponse]. N'hésite pas si tu as d'autres questions 😊"

**Template 2 - Renvoi :**
"Bonne question ! Tu trouveras tous les détails ici : [lien]. Sinon DM nous !"

**Template 3 - Complexe :**
"Hey ! Pour te répondre au mieux, envoie-nous un DM avec [infos nécessaires] 📩"

---

### 😤 RÉCLAMATIONS / PROBLÈMES

**Template 1 - Empathie :**
"[Prénom], je suis vraiment désolé que tu aies vécu ça 😔 Envoie-nous un DM avec ta commande, on règle ça tout de suite."

**Template 2 - Solution :**
"On comprend ta frustration et on prend ça très au sérieux. Voici ce qu'on peut faire : [solution]"

**Template 3 - Escalade :**
"Merci de nous avoir alertés. Notre équipe te contacte en privé dans l'heure pour résoudre ça."

---

### 💰 DEMANDES DE PRIX

**Template 1 - Public :**
"Hello ! Nos tarifs commencent à [X]. Tous les détails sur [lien] 😊"

**Template 2 - Privé :**
"Hey [Prénom] ! Envoie-nous un DM pour qu'on te fasse une offre adaptée à tes besoins 📩"

---

### 🤝 DEMANDES DE COLLABORATION

**Template 1 - Intéressé :**
"Hello ! On adore ton profil 👀 Envoie-nous un email à [email] avec ton media kit !"

**Template 2 - Pas intéressé (poli) :**
"Merci pour ton message ! On ne recherche pas de collabs en ce moment mais on garde ton profil en tête 🙏"

---

### 🚫 SPAM / TROLLS

**Template 1 - Ignorer avec humour :**
"[Réponse humoristique qui désamorce]"

**Template 2 - Rediriger :**
"On préfère garder un espace positif ici 😊 Bonne journée !"

**Action :** Masquer/Supprimer si nécessaire

---

### 💡 SUGGESTIONS

**Template :**
"Super idée [Prénom] ! 💡 On note et on transmet à l'équipe. Merci de nous aider à nous améliorer !"

---

**Règles de réponse :**
✅ Répondre en < 1h si possible
✅ Toujours personnaliser (prénom)
✅ Ne jamais être défensif
✅ Déplacer en DM si sensible
✅ Remercier même les critiques`
  },

  // ===== BATCH 3 - MOYENNE PRIORITÉ (6 outils) =====
  'facebook-group-post': {
    fields: [
      { name: 'group_topic', type: 'text', label: 'Thème du groupe', required: true, placeholder: 'Ex: Entrepreneurs DZ, Fitness, Marketing...' },
      { name: 'post_type', type: 'select', label: 'Type de post', required: true, options: ['Lancer une discussion', 'Poser une question', 'Sondage', 'Accueil nouveaux membres', 'Rappel des règles', 'Promotion (subtile)', 'Annonce événement', 'Célébration/Victoires'] },
      { name: 'goal', type: 'select', label: 'Objectif', options: ['Engagement', 'Ventes', 'Communauté', 'Feedback'] },
      { name: 'group_size', type: 'select', label: 'Taille du groupe', options: ['Petit (<500)', 'Moyen (500-5000)', 'Grand (5000+)'] },
    ],
    promptTemplate: `Tu es un community manager expert en groupes Facebook.

THÈME : {{group_topic}}
TYPE : {{post_type}}
OBJECTIF : {{goal}}
TAILLE : {{group_size}}

## 👥 3 POSTS GROUPE FACEBOOK

### Post 1 : Discussion ouverte

🔥 **[Question provocatrice ou débat]**

Je vois souvent [observation dans le groupe] et ça me fait réfléchir...

[Votre opinion ou expérience]

👇 **Et vous, qu'en pensez-vous ?**

Option A : [...]
Option B : [...]
Option C : Autre chose (commentez !)

---

### Post 2 : Partage d'expérience

📖 **Petit retour d'expérience sur [sujet]...**

[Histoire personnelle ou cas concret]

Ce que j'en retiens :
✅ [Leçon 1]
✅ [Leçon 2]
✅ [Leçon 3]

**Qui a vécu quelque chose de similaire ?** 👇

---

### Post 3 : Accueil/Communauté

👋 **BIENVENUE aux nouveaux membres !**

Cette semaine, on accueille [X] nouvelles personnes dans notre communauté ! 🎉

Pour bien démarrer :
1️⃣ Présentez-vous en commentaire (prénom, ville, pourquoi vous êtes là)
2️⃣ Lisez les règles épinglées
3️⃣ N'hésitez pas à poser vos questions !

**Anciens membres** : prenez 2 secondes pour souhaiter la bienvenue 🤗

---

**Bonnes pratiques Groupes FB :**
✅ Poster aux heures actives (12h-14h, 19h-21h)
✅ Répondre à TOUS les commentaires
✅ Taguer les membres actifs
✅ Éviter les liens dans le post principal
✅ Utiliser les sondages natifs FB`
  },

  'linkedin-article-outline': {
    fields: [
      { name: 'article_topic', type: 'text', label: 'Sujet de l\'article', required: true, placeholder: 'Ex: L\'avenir du travail hybride' },
      { name: 'target_audience', type: 'text', label: 'Audience cible', placeholder: 'Ex: RH, Managers, Entrepreneurs...' },
      { name: 'article_goal', type: 'select', label: 'Objectif', required: true, options: ['Thought Leadership', 'How-to / Guide', 'Analyse sectorielle', 'Conseils carrière', 'Étude de cas'] },
      { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir', placeholder: 'Les idées principales que vous voulez développer...' },
      { name: 'word_count', type: 'select', label: 'Longueur cible', options: ['800 mots', '1200 mots', '1500 mots', '2000 mots'] },
    ],
    promptTemplate: `Tu es un expert LinkedIn avec des articles à 100K+ vues.

SUJET : {{article_topic}}
AUDIENCE : {{target_audience}}
OBJECTIF : {{article_goal}}
LONGUEUR : {{word_count}}

## 📝 PLAN D'ARTICLE LINKEDIN

### TITRE (3 options)

1. "[Titre accrocheur avec bénéfice]"
2. "[Titre question]"
3. "[Titre avec chiffre]"

---

### STRUCTURE COMPLÈTE

**INTRODUCTION (150 mots)**
- Hook : [Accroche - stat choc, question, ou histoire]
- Contexte : [Pourquoi ce sujet maintenant]
- Promesse : [Ce que le lecteur va apprendre]
- Teaser : [Pourquoi lire jusqu'au bout]

---

**PARTIE 1 : [TITRE SECTION] (250 mots)**

H2 : [Sous-titre accrocheur]

- Point principal
- Exemple concret ou donnée
- Transition vers partie 2

---

**PARTIE 2 : [TITRE SECTION] (250 mots)**

H2 : [Sous-titre]

- Point principal
- Exemple/anecdote
- Insight actionnable

---

**PARTIE 3 : [TITRE SECTION] (250 mots)**

H2 : [Sous-titre]

- Point principal
- Cas d'étude ou preuve
- Leçon clé

---

**PARTIE 4 : CONSEILS PRATIQUES (200 mots)**

H2 : "Comment appliquer ça concrètement"

1. Action 1
2. Action 2
3. Action 3

---

**CONCLUSION (100 mots)**

- Récap des points clés
- Ouverture / réflexion
- CTA (commentaire, partage, follow)

---

### 🖼️ VISUELS SUGGÉRÉS

- Image de couverture : [Description]
- Infographie : [Si pertinent]
- Screenshots : [Si pertinent]

---

### 🏷️ TAGS LINKEDIN (5)

#[tag1] #[tag2] #[tag3] #[tag4] #[tag5]

---

**Optimisations Article LinkedIn :**
✅ Titre < 100 caractères
✅ Paragraphes courts (3-4 lignes)
✅ Sous-titres tous les 200-300 mots
✅ Bullet points pour la lisibilité
✅ Une image minimum
✅ CTA en fin d'article`
  },

  'social-contest-generator': {
    fields: [
      { name: 'platform', type: 'select', label: 'Plateforme', required: true, options: ['Instagram', 'Facebook', 'TikTok', 'Twitter', 'Multi-plateforme'] },
      { name: 'prize', type: 'text', label: 'Prix à gagner', required: true, placeholder: 'Ex: iPhone, Formation, Produit...' },
      { name: 'goal', type: 'select', label: 'Objectif principal', options: ['Followers', 'Engagement', 'UGC/Contenu', 'Email list', 'Notoriété'] },
      { name: 'duration', type: 'select', label: 'Durée', options: ['24 heures', '3 jours', '1 semaine', '2 semaines'] },
      { name: 'entry_requirements', type: 'select', label: 'Conditions de participation', options: ['Simple (like+follow)', 'Moyen (like+follow+tag)', 'Engagé (like+follow+tag+share)', 'UGC (créer du contenu)'] },
    ],
    promptTemplate: `Tu es expert en marketing viral et concours sociaux.

PLATEFORME : {{platform}}
PRIX : {{prize}}
OBJECTIF : {{goal}}
DURÉE : {{duration}}
CONDITIONS : {{entry_requirements}}

## 🎁 CONCOURS SOCIAL MEDIA

### POST D'ANNONCE

**[ACCROCHE]**
🎁 GIVEAWAY TIME ! 🎁

**Le prix :**
[Détails sur {{prize}}]

**Comment participer :**
1️⃣ [Condition 1]
2️⃣ [Condition 2]
3️⃣ [Condition 3]

**Chances bonus :**
⭐ [Action bonus]

**Fin du concours :** [Date]

Bonne chance à tous ! 🍀

#giveaway #concours #[niche]

---

### STORIES DE PROMOTION (5)

**Story 1 - Annonce :**
"GIVEAWAY 🎁 Swipe pour participer ⬇️"

**Story 2 - Le prix :**
[Visuel du prix + valeur]

**Story 3 - Comment participer :**
[Steps en format story]

**Story 4 - Rappel :**
"Plus que [X] heures pour participer ! 🏃"

**Story 5 - Winner :**
"Le gagnant est... 🥁 @[username] ! Félicitations ! 🎉"

---

### RÈGLES LÉGALES
[Mention légale simplifiée à adapter]

---

### KPIs À SUIVRE
- Nouveaux followers
- Engagement rate
- Nombre de participations
- UGC créé (si applicable)`
  },

  'whatsapp-broadcast-message': {
    fields: [
      { name: 'message_type', type: 'select', label: 'Type de message', required: true, options: ['Promotion/Offre', 'Annonce produit', 'Rappel événement', 'Newsletter', 'Message personnalisé'] },
      { name: 'business_type', type: 'text', label: 'Type de business', required: true },
      { name: 'offer_details', type: 'textarea', label: 'Détails de l\'offre/message', placeholder: 'Ce que vous voulez communiquer...' },
      { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Répondre au message', 'Cliquer sur un lien', 'Appeler', 'Venir en magasin', 'Commander'] },
    ],
    promptTemplate: `Tu es expert en WhatsApp Business Marketing.

TYPE : {{message_type}}
BUSINESS : {{business_type}}
DÉTAILS : {{offer_details}}
CTA : {{cta}}

## 📱 3 MESSAGES WHATSAPP BROADCAST

### Message 1 : Direct et efficace

Bonjour [Prénom] ! 👋

[Message principal court]

{{offer_details}}

[CTA clair]

À bientôt !
[Signature]

---

### Message 2 : Avec urgence

🔔 [Prénom], offre exclusive !

[Détail de l'offre]

⏰ Valable jusqu'à [date]

👉 [CTA]

---

### Message 3 : Personnalisé

Salut [Prénom] ! 😊

J'espère que tu vas bien !

[Message personnalisé]

[CTA souple]

---

**Bonnes pratiques WhatsApp Business :**
✅ Garder le message court (< 300 caractères)
✅ Personnaliser avec le prénom
✅ Un seul CTA clair
✅ Envoyer à des heures appropriées
✅ Ne pas spammer (1-2 messages/semaine max)
✅ Respecter le RGPD`
  },

  'telegram-channel-post': {
    fields: [
      { name: 'channel_type', type: 'select', label: 'Type de canal', required: true, options: ['Business/Marque', 'Communauté', 'News/Actualités', 'Éducatif', 'Deals/Promos'] },
      { name: 'post_topic', type: 'text', label: 'Sujet du post', required: true },
      { name: 'include_buttons', type: 'checkbox', label: 'Inclure des boutons' },
      { name: 'formatting', type: 'select', label: 'Style de formatage', options: ['Rich (gras, italique)', 'Simple', 'Avec emojis structurés'] },
    ],
    promptTemplate: `Tu es expert en marketing Telegram.

TYPE CANAL : {{channel_type}}
SUJET : {{post_topic}}
BOUTONS : {{include_buttons}}
FORMAT : {{formatting}}

## 📢 POST CANAL TELEGRAM

### Version complète

[Emoji] **[TITRE EN GRAS]**

[Corps du message avec formatage Telegram]

*[Point important en italique]*

• Point 1
• Point 2
• Point 3

📌 [Information clé]

{{#if include_buttons}}
[Bouton 1] | [Bouton 2]
{{/if}}

#hashtag1 #hashtag2

---

### Version courte

[Emoji] [Message concis]

[CTA]

---

### Version news

📰 **BREAKING/ACTUALITÉ**

[Résumé de l'info]

🔗 [Source]

💬 Votre avis ?

---

**Formatage Telegram :**
- **Gras** : \`**texte**\` ou \`<b>texte</b>\`
- *Italique* : \`*texte*\` ou \`<i>texte</i>\`
- \`Code\` : \`\`texte\`\`
- [Liens](url) : \`[texte](url)\`

**Conseils :**
✅ Structure claire avec emojis
✅ Boutons interactifs
✅ Pas trop de hashtags (2-3 max)
✅ Heures optimales : 10h, 15h, 20h`
  },

  'discord-announcement': {
    fields: [
      { name: 'server_type', type: 'select', label: 'Type de serveur', required: true, options: ['Gaming', 'Communauté créateurs', 'Business/Marque', 'Éducation', 'NFT/Crypto', 'Général'] },
      { name: 'announcement_type', type: 'select', label: 'Type d\'annonce', options: ['Mise à jour', 'Événement', 'Giveaway', 'Nouveauté', 'Règles', 'Bienvenue'] },
      { name: 'content', type: 'textarea', label: 'Contenu de l\'annonce', required: true },
      { name: 'mentions', type: 'select', label: 'Mentions', options: ['@everyone', '@here', 'Role spécifique', 'Aucune'] },
    ],
    promptTemplate: `Tu es community manager Discord expert.

SERVEUR : {{server_type}}
TYPE : {{announcement_type}}
CONTENU : {{content}}
MENTIONS : {{mentions}}

## 📢 ANNONCE DISCORD

### Format standard

{{mentions}}

**[TITRE DE L'ANNONCE]** [Emoji approprié]

━━━━━━━━━━━━━━━━━

[Corps de l'annonce]

**📌 Points importants :**
> Point 1
> Point 2
> Point 3

**🔗 Liens utiles :**
• [Lien 1]
• [Lien 2]

━━━━━━━━━━━━━━━━━

[CTA ou question d'engagement]

[Emoji de réaction suggérés]

---

### Format événement

🎉 **[NOM DE L'ÉVÉNEMENT]** 🎉

📅 **Date :** [Date et heure]
📍 **Où :** [Channel ou lieu]
🎁 **Prix :** [Si applicable]

**Comment participer :**
1. [Step 1]
2. [Step 2]

React avec [emoji] si tu participes !

---

### Format mise à jour

🔄 **MISE À JOUR - [Version/Date]**

**Nouveautés :**
✅ [Nouveauté 1]
✅ [Nouveauté 2]

**Corrections :**
🔧 [Fix 1]
🔧 [Fix 2]

Des questions ? Posez-les dans #support !

---

**Formatage Discord :**
- **Gras** : \`**texte**\`
- *Italique* : \`*texte*\`
- __Souligné__ : \`__texte__\`
- ~~Barré~~ : \`~~texte~~\`
- > Citation
- \`\`\`Code block\`\`\``
  },
};

// Config par défaut
const defaultFormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez générer...' },
    { name: 'platform', type: 'select', label: 'Plateforme', options: ['Instagram', 'TikTok', 'LinkedIn', 'Twitter', 'Facebook'] },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Décontracté', 'Humoristique', 'Inspirant'] },
  ],
  promptTemplate: `Génère du contenu social media basé sur cette demande...`
};

export default function SocialToolPage({ params }: PageProps) {
  const tool = socialTools.find(t => t.slug === params.toolSlug);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [result, setResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!tool) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Outil non trouvé</h1>
          <p className="text-gray-500 mb-4">L'outil "{params.toolSlug}" n'existe pas.</p>
          <Link href="/tools/social" className="text-pink-600 hover:underline">
            Retour aux outils Social Media
          </Link>
        </div>
      </div>
    );
  }

  const formConfig = toolFormConfigs[tool.slug] || defaultFormConfig;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult('');

    setTimeout(() => {
      const mockResult = `# Résultat généré par ${tool.name.fr}

## Contenu Généré

Voici le contenu généré basé sur vos paramètres:

${Object.entries(formData).map(([key, value]) => `**${key}**: ${value}`).join('\n')}

---

### Résultat Principal

Ce contenu a été généré par l'IA d'IAFactory Algeria pour optimiser votre présence sur les réseaux sociaux.

### Points Clés

1. **Engagement optimisé** : Contenu conçu pour maximiser les interactions
2. **Algorithme-friendly** : Adapté aux dernières tendances de chaque plateforme
3. **Conversion** : Call-to-actions stratégiques inclus

### Prochaines Étapes

- Adaptez le contenu à votre style personnel
- Testez différentes variantes
- Analysez les performances

---
*Généré avec ${tool.credits} crédits • ${new Date().toLocaleDateString('fr-FR')}*`;

      setResult(mockResult);
      setIsLoading(false);
    }, 2500);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const priorityColors = {
    critical: 'bg-red-100 text-red-700',
    high: 'bg-orange-100 text-orange-700',
    medium: 'bg-yellow-100 text-yellow-700',
    low: 'bg-gray-100 text-gray-700',
  };

  const subcategoryIcons: Record<string, any> = {
    instagram: Instagram,
    tiktok: Music,
    linkedin: Linkedin,
    twitter: Twitter,
    facebook: Facebook,
  };

  const IconComponent = subcategoryIcons[tool.subcategory || ''] || Share2;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/social" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 bg-pink-100 rounded-lg flex items-center justify-center">
                  <IconComponent className="w-6 h-6 text-pink-600" />
                </div>
                <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${priorityColors[tool.priority]}`}>
                  {tool.priority}
                </span>
              </div>
              <p className="text-gray-600 mb-3">{tool.description.fr}</p>
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>Catégorie: <strong className="text-gray-700">{tool.subcategory}</strong></span>
                <span>•</span>
                <span>ID: <code className="bg-gray-100 px-1 rounded">{tool.id}</code></span>
              </div>
            </div>
            <div className="bg-pink-50 text-pink-700 px-4 py-2 rounded-lg font-semibold text-lg">
              {tool.credits} crédits
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-pink-600" />
              Paramètres
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              {formConfig.fields.map((field: any) => (
                <div key={field.name}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                    {field.required && <span className="text-red-500 ml-1">*</span>}
                  </label>
                  {field.type === 'textarea' ? (
                    <textarea
                      name={field.name}
                      placeholder={field.placeholder}
                      rows={4}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-200 transition resize-none"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      name={field.name}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    >
                      <option value="">Sélectionner...</option>
                      {field.options?.map((opt: string) => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : field.type === 'checkbox' ? (
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        name={field.name}
                        className="w-4 h-4 text-pink-600 border-gray-300 rounded focus:ring-pink-500"
                        checked={formData[field.name] === 'true'}
                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked ? 'true' : 'false' })}
                      />
                      <span className="text-sm text-gray-600">{field.label}</span>
                    </label>
                  ) : (
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-pink-600 hover:to-purple-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Générer ({tool.credits} crédits)
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Result */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Résultat</h2>
              {result && (
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-pink-600 transition px-3 py-1 rounded-lg hover:bg-gray-50"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4" />
                      Copié !
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copier
                    </>
                  )}
                </button>
              )}
            </div>
            <div className="bg-gray-50 rounded-lg p-4 min-h-[450px] max-h-[600px] overflow-y-auto">
              {isLoading ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <Loader2 className="w-8 h-8 text-pink-600 animate-spin mx-auto mb-2" />
                    <p className="text-gray-500">Génération en cours...</p>
                    <p className="text-sm text-gray-400 mt-1">Cela peut prendre quelques secondes</p>
                  </div>
                </div>
              ) : result ? (
                <div className="prose prose-sm max-w-none">
                  <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm leading-relaxed">{result}</pre>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-400">
                  <div className="text-center">
                    <Share2 className="w-12 h-12 mx-auto mb-2 opacity-30" />
                    <p>Le résultat apparaîtra ici</p>
                    <p className="text-sm mt-1">Remplissez le formulaire et cliquez sur Générer</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-6 bg-gradient-to-r from-pink-50 to-purple-50 rounded-xl p-6 border border-pink-100">
          <h3 className="font-semibold text-pink-900 mb-2">Conseils pour de meilleurs résultats</h3>
          <ul className="text-sm text-pink-800 space-y-1">
            <li>- Soyez précis sur votre audience cible et votre niche</li>
            <li>- Adaptez le ton à la plateforme (pro sur LinkedIn, fun sur TikTok)</li>
            <li>- Testez différentes variations de contenu</li>
            <li>- Personnalisez toujours le résultat avec votre touche unique</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
