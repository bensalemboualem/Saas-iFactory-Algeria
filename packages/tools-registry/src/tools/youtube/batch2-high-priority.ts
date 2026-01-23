import { AITool } from '../../types';

export const youtubeVideoOutline: AITool = {
  category: 'youtube',
  credits: 15,
  description: {
    ar: 'أنشئ مخططًا تفصيليًا لهيكلة الفيديو',
    en: 'Create a detailed outline to structure your video',
    fr: 'Créez un plan détaillé pour structurer votre vidéo avant le tournage'
  },
  icon: 'ListTree',
  id: 'youtube-video-outline',
  inputs: [
    { label: 'Sujet de la vidéo', name: 'video_topic', required: true, type: 'text' },
    { label: 'Durée cible', name: 'target_length', options: ['5min', '10min', '15min', '20min', '30min'], type: 'select' },
    { label: 'Objectif principal', name: 'video_goal', options: ['Eduquer', 'Divertir', 'Vendre', 'Inspirer', 'Informer'], type: 'select' },
    { label: 'Points clés à couvrir', name: 'key_points', type: 'textarea' },
    { label: 'Niveau audience', name: 'audience_level', options: ['Debutant', 'Intermediaire', 'Avance'], type: 'select' }
  ],
  estimatedTime: '45s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'مخطط الفيديو', fr: 'Plan de Vidéo Structuré', en: 'Video Outline' },
  outputs: [{ name: 'outline', type: 'markdown' }],
  slug: 'youtube-video-outline',
  priority: 'high',
  promptTemplate: `Tu es un producteur YouTube professionnel.

SUJET : {{video_topic}}
DURÉE : {{target_length}}
OBJECTIF : {{video_goal}}
POINTS CLÉS : {{key_points}}

## 📋 PLAN DE VIDÉO STRUCTURÉ

### 🎯 HOOK (0:00 - 0:15)
**Objectif :** Capturer l'attention immédiatement
- Phrase d'accroche : "[suggestion]"
- Visuel suggéré : [description]

### 📺 INTRO (0:15 - 1:00)
**Objectif :** Présenter et promettre
- Présentation rapide
- Ce que le viewer va apprendre
- Pourquoi rester jusqu'à la fin

### 📖 PARTIE 1 : [TITRE] (1:00 - X:XX)
**Durée estimée :** X min
**Points à couvrir :**
- Point A
- Point B
- Exemple/illustration
**Transition vers Partie 2 :** "[phrase]"

### 📖 PARTIE 2 : [TITRE] (X:XX - X:XX)
[Structure similaire]

### 📖 PARTIE 3 : [TITRE] (X:XX - X:XX)
[Structure similaire]

### 🎁 BONUS (optionnel)
**Valeur ajoutée :** [suggestion]

### 🔄 RÉCAP (X:XX - X:XX)
**Résumé en 3 points :**
1. [Point clé 1]
2. [Point clé 2]
3. [Point clé 3]

### 📢 CTA + OUTRO (X:XX - fin)
- Appel à l'action principal
- Question engagement commentaires
- Teaser prochaine vidéo

---

## 📝 NOTES DE PRODUCTION

**B-roll suggéré :**
- [Moment 1] : [type de visuel]
- [Moment 2] : [type de visuel]

**Ressources à préparer :**
- [ ] [Ressource 1]
- [ ] [Ressource 2]

**Timestamps prêts à copier :**
0:00 Intro
X:XX [Partie 1]
X:XX [Partie 2]
...`,
  subcategory: 'content'
};

export const youtubeCommentReply: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'أنشئ ردودًا جذابة على تعليقات يوتيوب',
    en: 'Generate engaging replies to YouTube comments',
    fr: 'Générez des réponses engageantes pour vos commentaires YouTube'
  },
  icon: 'MessageCircle',
  id: 'youtube-comment-reply',
  inputs: [
    { label: 'Commentaire reçu', name: 'comment', required: true, type: 'textarea' },
    { label: 'Type de commentaire', name: 'comment_type', options: [
      'Positif / Compliment',
      'Question',
      'Négatif / Critique',
      'Suggestion',
      'Spam / Hors sujet'
    ], type: 'select'},
    { label: 'Ton souhaité', name: 'tone', options: ['Amical', 'Professionnel', 'Humoristique', 'Reconnaissant'], type: 'select' },
    { label: 'Inclure un appel à l\'action', name: 'include_cta', type: 'boolean' },
    { label: 'Nom de la chaîne (pour personnalisation)', name: 'channel_name', type: 'text' }
  ],
  estimatedTime: '20s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'الرد على التعليقات', fr: 'Réponses aux Commentaires', en: 'Comment Reply Generator' },
  outputs: [{ name: 'replies', type: 'markdown' }],
  slug: 'youtube-comment-reply',
  priority: 'high',
  promptTemplate: `Tu gères la communauté d'une chaîne YouTube populaire.

COMMENTAIRE : "{{comment}}"
TYPE : {{comment_type}}
TON : {{tone}}

## 💬 3 Réponses Suggérées

{{#if comment_type.includes('Positif')}}
### Réponse 1 (Reconnaissance)
"[Remercier sincèrement + personnalisation]"

### Réponse 2 (Engagement)
"[Remercier + poser une question]"

### Réponse 3 (CTA subtil)
"[Remercier + inviter à voir une autre vidéo]"
{{/if}}

{{#if comment_type === 'Question'}}
### Réponse 1 (Directe)
"[Répondre clairement à la question]"

### Réponse 2 (Développée)
"[Réponse + contexte supplémentaire]"

### Réponse 3 (Renvoi)
"[Réponse courte + lien vers vidéo qui approfondit]"
{{/if}}

{{#if comment_type.includes('Négatif')}}
### Réponse 1 (Professionnelle)
"[Reconnaître le feedback + explication]"

### Réponse 2 (Ouverte au dialogue)
"[Demander plus de détails + amélioration]"

### Réponse 3 (Redirection positive)
"[Accepter la critique + mentionner ce qui vient]"

⚠️ **Ne jamais :**
- Être défensif ou agressif
- Ignorer une critique constructive
- Supprimer sans raison valable
{{/if}}

---

**Bonnes pratiques :**
✅ Répondre dans les 24h (algorithme favorise)
✅ Mentionner le prénom si visible
✅ Poser une question pour relancer
✅ Épingler les meilleurs commentaires`,
  subcategory: 'engagement'
};

export const youtubeCommunityPost: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'أنشئ منشورات جذابة لتبويب المجتمع',
    en: 'Create engaging posts for your Community tab',
    fr: 'Créez des posts engageants pour l\'onglet Communauté de votre chaîne'
  },
  icon: 'Users',
  id: 'youtube-community-post',
  inputs: [
    { label: 'Type de post', name: 'post_type', options: [
      'Sondage',
      'Teaser prochaine vidéo',
      'Behind the scenes',
      'Question à la communauté',
      'Célébration / Milestone',
      'Throwback / Ancienne vidéo',
      'Annonce'
    ], required: true, type: 'select'},
    { label: 'Contexte / Détails', name: 'context', required: true, type: 'textarea' },
    { label: 'Niche de la chaîne', name: 'channel_niche', type: 'text' },
    { label: 'Inclure suggestion d\'image', name: 'include_image', type: 'boolean' }
  ],
  estimatedTime: '25s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'منشور مجتمع يوتيوب', fr: 'Post Communauté YouTube', en: 'Community Post Generator' },
  outputs: [{ name: 'posts', type: 'markdown' }],
  slug: 'youtube-community-post',
  priority: 'high',
  promptTemplate: `Tu es un community manager YouTube expert.

TYPE : {{post_type}}
CONTEXTE : {{context}}
NICHE : {{channel_niche}}

## 📱 3 Posts Communauté

{{#if post_type === 'Sondage'}}
### Post 1 : Sondage Engagement
"[Question engageante]"

Options :
- 🔵 [Option A]
- 🔴 [Option B]
- 🟢 [Option C]
- 🟡 [Option D]

### Post 2 : Sondage Décision
"Aidez-moi à choisir le sujet de ma prochaine vidéo ! 👇"

Options :
- [Sujet A]
- [Sujet B]
- Autre (commentez !)
{{/if}}

{{#if post_type.includes('Teaser')}}
### Post 1 : Mystère
"🔜 Quelque chose d'ÉNORME arrive dimanche...

Indice : [emoji cryptique]

Qui a deviné ? 👀"

### Post 2 : Aperçu
"[Screenshot ou behind the scenes]

La prochaine vidéo est FOLLE 🔥
Dites-moi ce que vous pensez qu'il va se passer ⬇️"
{{/if}}

{{#if post_type.includes('Question')}}
### Post 1 : Opinion
"Question du jour 🤔

[Question ouverte liée à la niche]

Je lis TOUS vos commentaires ⬇️"

### Post 2 : Conseil
"J'ai besoin de VOTRE aide !

[Situation/dilemme]

Qu'est-ce que vous feriez ? 💭"
{{/if}}

---

**Meilleurs moments pour poster :**
- Mardi-Jeudi : 14h-16h
- Samedi : 10h-12h

**Fréquence recommandée :**
- 2-3 posts/semaine entre les vidéos`,
  subcategory: 'engagement'
};

export const youtubePlaylistOptimizer: AITool = {
  category: 'youtube',
  credits: 10,
  description: {
    ar: 'حسّن قوائم التشغيل للسيو والاحتفاظ بالمشاهدين',
    en: 'Optimize playlists for SEO and viewer retention',
    fr: 'Optimisez vos playlists pour le SEO et la rétention'
  },
  icon: 'ListMusic',
  id: 'youtube-playlist-optimizer',
  inputs: [
    { label: 'Thème de la playlist', name: 'playlist_topic', required: true, type: 'text' },
    { label: 'Mot-clé cible', name: 'target_keyword', type: 'text' },
    { default: 10, label: 'Nombre de vidéos', name: 'video_count', type: 'number' },
    { label: 'Titre actuel (si modification)', name: 'current_title', type: 'text' }
  ],
  estimatedTime: '30s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'محسن قوائم التشغيل', fr: 'Optimiseur de Playlists', en: 'Playlist Optimizer' },
  outputs: [{ name: 'optimizedPlaylist', type: 'markdown' }],
  slug: 'youtube-playlist-optimizer',
  priority: 'high',
  promptTemplate: `Tu es un expert SEO YouTube.

THÈME : {{playlist_topic}}
MOT-CLÉ : {{target_keyword}}
VIDÉOS : {{video_count}}

## 🎵 Optimisation Playlist

### 1. TITRE OPTIMISÉ (5 suggestions)
**Règles :**
- Mot-clé au début
- 60 caractères max
- Inclure le bénéfice

1. "[Mot-clé] : Guide Complet pour [Audience]"
2. "Apprendre [Mot-clé] de A à Z | Série Complète"
3. "[Nombre] Vidéos pour Maîtriser [Mot-clé]"
4. "[Mot-clé] pour Débutants → Avancés"
5. "Tout sur [Mot-clé] | Formation Gratuite"

### 2. DESCRIPTION OPTIMISÉE
"[Description 200-300 mots avec mots-clés]"

**Structure :**
- Ligne 1 : Accroche + mot-clé
- Ce que contient la playlist
- Pour qui c'est fait
- CTA abonnement
- Hashtags

### 3. ORDRE DES VIDÉOS
**Stratégie de rétention :**
1. 🎯 **Vidéo 1** : La plus populaire (hook)
2. 📚 **Vidéos 2-4** : Fondamentaux
3. 🔥 **Vidéos 5-7** : Contenu avancé
4. ⭐ **Vidéos 8-9** : Best-of / Populaires
5. 🎁 **Vidéo finale** : Bonus + CTA

### 4. MINIATURE DE PLAYLIST
- Utiliser la miniature de la meilleure vidéo
- Ou créer une miniature dédiée "SÉRIE COMPLÈTE"

### 5. CHECKLIST
✅ Titre avec mot-clé
✅ Description complète
✅ Ordre stratégique
✅ Vidéos cohérentes (même thème)
✅ Pas de vidéos "mortes" (faible rétention)`,
  subcategory: 'optimization'
};

export const youtubeChannelAudit: AITool = {
  category: 'youtube',
  credits: 25,
  description: {
    ar: 'حلل قناتك واحصل على توصيات للتحسين',
    en: 'Analyze your channel and get improvement recommendations',
    fr: 'Analysez votre chaîne et obtenez des recommandations d\'amélioration'
  },
  icon: 'ClipboardCheck',
  id: 'youtube-channel-audit',
  inputs: [
    { label: 'Nom de la chaîne', name: 'channel_name', required: true, type: 'text' },
    { label: 'Niche', name: 'channel_niche', required: true, type: 'text' },
    { label: 'Nombre d\'abonnés', name: 'subscriber_count', type: 'number' },
    { label: 'Nombre de vidéos', name: 'video_count', type: 'number' },
    { label: 'Vues moyennes par vidéo', name: 'avg_views', type: 'number' },
    { label: 'Fréquence publication', name: 'upload_frequency', options: ['daily', 'weekly', '2_per_week', 'monthly', 'irregular'], type: 'select' },
    { label: 'Description actuelle de la chaîne', name: 'channel_description', type: 'textarea' },
    { label: 'Problèmes rencontrés', name: 'main_issues', type: 'textarea' }
  ],
  estimatedTime: '60s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'تدقيق قناة يوتيوب', fr: 'Audit de Chaîne YouTube', en: 'Channel Audit' },
  outputs: [{ name: 'audit', type: 'markdown' }],
  slug: 'youtube-channel-audit',
  priority: 'high',
  promptTemplate: `Tu es un consultant YouTube avec 10 ans d'expérience.

CHAÎNE : {{channel_name}}
NICHE : {{channel_niche}}
ABONNÉS : {{subscriber_count}}
VIDÉOS : {{video_count}}
VUES MOYENNES : {{avg_views}}
FRÉQUENCE : {{upload_frequency}}

## 📊 AUDIT COMPLET DE CHAÎNE

### 1. MÉTRIQUES CLÉS

| Métrique | Valeur | Benchmark niche | Statut |
|----------|--------|-----------------|--------|
| Ratio vues/abonnés | X% | 10-30% | ✅/⚠️/❌ |
| Engagement estimé | X% | 3-5% | ✅/⚠️/❌ |
| Fréquence | {{upload_frequency}} | Weekly | ✅/⚠️/❌ |

### 2. ANALYSE BRANDING

**Nom de chaîne :** {{channel_name}}
- ✅/❌ Mémorable
- ✅/❌ Facile à épeler
- ✅/❌ Reflète la niche

**Description :**
- ✅/❌ Proposition de valeur claire
- ✅/❌ Mots-clés présents
- ✅/❌ CTA abonnement

**Bannière & Logo :**
[Recommandations visuelles]

### 3. ANALYSE CONTENU

**Points forts identifiés :**
- [Force 1]
- [Force 2]

**Axes d'amélioration :**
- [Faiblesse 1] → Solution
- [Faiblesse 2] → Solution

### 4. ANALYSE SEO

**Optimisations recommandées :**
- Titres : [Recommandation]
- Descriptions : [Recommandation]
- Tags : [Recommandation]
- Miniatures : [Recommandation]

### 5. STRATÉGIE DE CROISSANCE

**Objectif 3 mois :** [X abonnés]
**Objectif 6 mois :** [X abonnés]
**Objectif 12 mois :** [X abonnés]

**Actions prioritaires :**
1. 🔴 **URGENT** : [Action 1]
2. 🟠 **IMPORTANT** : [Action 2]
3. 🟡 **RECOMMANDÉ** : [Action 3]

### 6. PLAN D'ACTION (30 jours)

| Semaine | Action | Impact attendu |
|---------|--------|----------------|
| S1 | [Action] | [Impact] |
| S2 | [Action] | [Impact] |
| S3 | [Action] | [Impact] |
| S4 | [Action] | [Impact] |

### 7. SCORE GLOBAL : X/100

**Répartition :**
- Branding : X/20
- SEO : X/20
- Contenu : X/20
- Engagement : X/20
- Stratégie : X/20`,
  subcategory: 'strategy'
};

export const youtubeMonetizationTips: AITool = {
  category: 'youtube',
  credits: 15,
  description: {
    ar: 'استراتيجيات لتحقيق الدخل من قناتك',
    en: 'Strategies to monetize your YouTube channel beyond AdSense',
    fr: 'Stratégies pour monétiser votre chaîne YouTube au-delà de AdSense'
  },
  icon: 'DollarSign',
  id: 'youtube-monetization-tips',
  inputs: [
    { label: 'Abonnés actuels', name: 'subscriber_count', required: true, type: 'number' },
    { label: 'Vues mensuelles', name: 'monthly_views', type: 'number' },
    { label: 'Niche', name: 'niche', required: true, type: 'text' },
    { label: 'Revenus actuels', name: 'current_revenue', options: ['0', '1-100', '100-500', '500-1000', '1000-5000', '5000+'], type: 'select' },
    { label: 'Objectifs (ex: adsense, sponsoring, affiliation)', name: 'monetization_goals', type: 'text' }
  ],
  estimatedTime: '40s',
  isAlgeriaExclusive: false,
  model: 'claude',
  name: { ar: 'نصائح تحقيق الدخل', fr: 'Conseils Monétisation', en: 'Monetization Tips' },
  outputs: [{ name: 'tips', type: 'markdown' }],
  slug: 'youtube-monetization-tips',
  priority: 'high',
  promptTemplate: `Tu es un expert en monétisation YouTube.

ABONNÉS : {{subscriber_count}}
VUES/MOIS : {{monthly_views}}
NICHE : {{niche}}
REVENUS ACTUELS : {{current_revenue}}

## 💰 STRATÉGIES DE MONÉTISATION

### 1. VOTRE POTENTIEL ACTUEL

**Estimation revenus AdSense :**
- CPM estimé ({{niche}}) : $X - $X
- Revenus mensuels potentiels : $X - $X

**Éligibilité Programme Partenaire :**
{{#if subscriber_count >= 1000}}
✅ 1000 abonnés atteints
{{else}}
❌ 1000 abonnés requis (il vous manque X)
{{/if}}

### 2. SOURCES DE REVENUS RECOMMANDÉES

#### 🎯 Niveau 1 : 0-10K abonnés
1. **Affiliation** (Revenus potentiels : $100-500/mois)
   - Programmes recommandés pour {{niche}}
   - Comment intégrer naturellement

2. **Services/Coaching** ($500-2000/mois)
   - [Idées de services pour votre niche]

#### 🎯 Niveau 2 : 10K-100K abonnés
3. **Sponsoring** ($500-5000/vidéo)
   - Comment pitcher les marques
   - Tarifs recommandés

4. **Produits numériques** ($500-5000/mois)
   - E-book, formation, templates

#### 🎯 Niveau 3 : 100K+ abonnés
5. **Memberships YouTube** ($1000-10000/mois)
6. **Merchandising** (Variable)
7. **Licensing** (Variable)

### 3. PLAN D'ACTION PERSONNALISÉ

**Cette semaine :**
- [ ] [Action immédiate]

**Ce mois :**
- [ ] [Action 1]
- [ ] [Action 2]

**Ce trimestre :**
- [ ] [Action 1]
- [ ] [Action 2]

### 4. ERREURS À ÉVITER
❌ [Erreur 1]
❌ [Erreur 2]
❌ [Erreur 3]`,
  subcategory: 'strategy'
};

export const youtubeCollabPitch: AITool = {
  category: 'youtube',
  credits: 12,
  description: {
    ar: 'أنشئ رسائل مؤثرة لاقتراح التعاون',
    en: 'Create impactful messages to propose collaborations',
    fr: 'Créez des messages percutants pour proposer des collaborations'
  },
  icon: 'Handshake',
  id: 'youtube-collab-pitch',
  inputs: [
    { label: 'Votre chaîne', name: 'your_channel', required: true, type: 'text' },
    { label: 'Vos abonnés', name: 'your_subscribers', type: 'number' },
    { label: 'Chaîne cible', name: 'target_channel', required: true, type: 'text' },
    { label: 'Idée de collaboration', name: 'collab_idea', required: true, type: 'textarea' },
    { label: 'Bénéfice mutuel', name: 'mutual_benefit', type: 'textarea' }
  ],
  estimatedTime: '25s',
  model: 'claude',
  name: { ar: 'عرض التعاون', en: 'Collab Pitch Generator', fr: 'Pitch de Collaboration' },
  outputs: [{ name: 'pitch', type: 'markdown' }],
  priority: 'high',
  slug: 'youtube-collab-pitch',
  promptTemplate: `Tu es un expert en networking YouTube.

VOTRE CHAÎNE : {{your_channel}} ({{your_subscribers}} abonnés)
CIBLE : {{target_channel}}
IDÉE : {{collab_idea}}

## 🤝 3 VERSIONS DE PITCH

### Version 1 : DM Court (Instagram/Twitter)
"[Message de 2-3 lignes max, direct et intrigant]"

### Version 2 : Email Professionnel
**Objet :** Idée de collab {{your_channel}} x {{target_channel}} 🎬

"Salut [Prénom],

[Paragraphe 1 : Compliment sincère et spécifique]

[Paragraphe 2 : Qui je suis en 1-2 phrases]

[Paragraphe 3 : L'idée de collab + bénéfice pour EUX]

[Paragraphe 4 : CTA simple]

[Signature]"

### Version 3 : Message Communauté/Commentaire
"[Version très courte pour attirer l'attention]"

---

**Checklist avant d'envoyer :**
✅ Personnalisé (pas de copier-coller évident)
✅ Bénéfice pour EUX mis en avant
✅ Pas de demande, mais une proposition
✅ CTA clair et simple
✅ Pas de fautes

**Où contacter :**
1. Email professionnel (meilleur)
2. Instagram DM
3. Twitter
4. Discord (si communauté)

**Timing :**
- Éviter le lundi matin et vendredi soir
- Idéal : Mardi-Jeudi, 10h-14h`,
  subcategory: 'strategy'
};

export const youtubeBrandDealEmail: AITool = {
  category: 'youtube',
  credits: 12,
  description: {
    ar: 'اكتب رسائل بريد احترافية للحصول على رعاية',
    en: 'Write professional emails to land sponsorships',
    fr: 'Rédigez des emails professionnels pour décrocher des sponsorings'
  },
  icon: 'Mail',
  id: 'youtube-brand-deal-email',
  inputs: [
    { label: 'Type d\'email', name: 'email_type', options: [
      'Prospection (vous contactez la marque)',
      'Réponse (la marque vous a contacté)',
      'Négociation tarifaire',
      'Relance'
    ], required: true, type: 'select'},
    { label: 'Nom de la marque', name: 'brand_name', required: true, type: 'text' },
    { label: 'Votre chaîne', name: 'your_channel', type: 'text' },
    { label: 'Vos statistiques clés', name: 'your_stats', type: 'textarea' },
    { label: 'Tarif proposé (optionnel)', name: 'proposed_rate', type: 'text' },
    { label: 'Idée de campagne', name: 'campaign_idea', type: 'textarea' }
  ],
  estimatedTime: '30s',
  model: 'claude',
  name: { ar: 'بريد صفقة العلامة', en: 'Brand Deal Email', fr: 'Email Partenariat Marque' },
  outputs: [{ name: 'email', type: 'markdown' }],
  priority: 'high',
  slug: 'youtube-brand-deal-email',
  promptTemplate: `Tu es un créateur YouTube professionnel qui négocie des sponsorings.

TYPE : {{email_type}}
MARQUE : {{brand_name}}
CHAÎNE : {{your_channel}}
STATS : {{your_stats}}

## 📧 EMAIL {{email_type}}

{{#if email_type.includes('Prospection')}}
**Objet :** Partenariat {{your_channel}} x {{brand_name}} - Proposition

Bonjour [Prénom/Équipe Marketing],

Je suis [Prénom], créateur de la chaîne {{your_channel}} où je [proposition de valeur en 1 ligne].

**Pourquoi {{brand_name}} ?**
[1-2 phrases montrant que vous connaissez et utilisez la marque]

**Ma communauté :**
{{your_stats}}

**Idée de contenu :**
{{campaign_idea}}

Je serais ravi d'en discuter. Êtes-vous disponible pour un appel de 15 minutes cette semaine ?

Bien cordialement,
[Signature avec liens]
{{/if}}

{{#if email_type.includes('Négociation')}}
**Objet :** RE: Proposition de partenariat

Bonjour [Prénom],

Merci pour votre proposition !

Après analyse, voici ma contre-proposition :

**Livrables :**
- [Détail des livrables]

**Tarif :** {{proposed_rate}}

Ce tarif reflète [justification : audience, engagement, exclusivité, droits...].

Je reste ouvert à la discussion. Qu'en pensez-vous ?

[Signature]
{{/if}}

---

**Media Kit à joindre :**
- Statistiques chaîne
- Démographie audience
- Exemples de collaborations passées
- Tarifs (optionnel)`,
  subcategory: 'strategy'
};

export const youtubeEndScreenCta: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'نصوص واستراتيجيات لشاشات نهاية يوتيوب',
    en: 'Scripts and strategies for YouTube end screens',
    fr: 'Scripts et stratégies pour vos écrans de fin YouTube'
  },
  icon: 'Monitor',
  id: 'youtube-end-screen-cta',
  inputs: [
    { label: 'Sujet de la vidéo actuelle', name: 'video_topic', required: true, type: 'text' },
    { label: 'Sujet de la vidéo recommandée', name: 'next_video_topic', type: 'text' },
    { label: 'Objectif principal', name: 'cta_goal', options: ['Subscribe', 'Watch next', 'Playlist', 'Both'], type: 'select' },
    { label: 'Style', name: 'style', options: ['Direct', 'Teaser', 'Urgence', 'Humour'], type: 'select' }
  ],
  estimatedTime: '20s',
  model: 'claude',
  name: { ar: 'دعوة شاشة النهاية', en: 'End Screen CTA Generator', fr: 'CTA Écran de Fin' },
  outputs: [{ name: 'cta', type: 'markdown' }],
  priority: 'high',
  slug: 'youtube-end-screen-cta',
  promptTemplate: `Tu es un expert en rétention YouTube.

VIDÉO ACTUELLE : {{video_topic}}
VIDÉO SUIVANTE : {{next_video_topic}}
OBJECTIF : {{cta_goal}}

## 🖥️ SCRIPTS ÉCRAN DE FIN (20 secondes)

### Version 1 : Direct
"Si cette vidéo vous a plu, vous allez ADORER celle-ci [pointer] où je vous montre [teaser].
Et si ce n'est pas déjà fait, abonnez-vous [pointer] pour ne rien manquer !
À très vite !"

### Version 2 : Teaser Mystère
"Mais attendez... dans la prochaine vidéo, je vous révèle [teaser intrigant].
Cliquez ici [pointer] avant qu'il ne soit trop tard !
Et abonnez-vous [pointer] !"

### Version 3 : Social Proof
"Rejoignez les [X] personnes qui ont déjà vu cette vidéo [pointer].
Ils ont découvert [bénéfice] et vous pouvez aussi !
Abonnez-vous [pointer] pour faire partie de la communauté !"

---

**Configuration écran de fin :**
- Durée : 20 secondes obligatoire
- Élément 1 : Vidéo/Playlist (gauche)
- Élément 2 : Abonnement (droite)
- Animation : Pointer avec la main ou graphique

**Timing optimal :**
- Commencer le CTA vocal à T-25 secondes
- Éléments cliquables : T-20 à T-0`,
  subcategory: 'engagement'
};

export const youtubePollIdeas: AITool = {
  category: 'youtube',
  credits: 8,
  description: {
    ar: 'أنشئ استطلاعات جذابة لتبويب المجتمع',
    en: 'Generate engaging polls for your Community tab',
    fr: 'Générez des sondages engageants pour votre onglet Communauté'
  },
  icon: 'BarChart',
  id: 'youtube-poll-ideas',
  inputs: [
    { label: 'Niche de la chaîne', name: 'channel_niche', required: true, type: 'text' },
    { label: 'Objectif du sondage', name: 'poll_goal', options: [
      'Engagement',
      'Feedback',
      'Idées de contenu',
      'Divertissement'
    ], type: 'select'},
    { label: 'Dernière vidéo publiée (optionnel)', name: 'recent_video', type: 'text' }
  ],
  estimatedTime: '20s',
  model: 'claude',
  name: { ar: 'أفكار استطلاعات', en: 'Poll Ideas Generator', fr: 'Idées de Sondages' },
  outputs: [{ name: 'polls', type: 'markdown' }],
  priority: 'high',
  slug: 'youtube-poll-ideas',
  promptTemplate: `Tu es un community manager YouTube expert.

NICHE : {{channel_niche}}
OBJECTIF : {{poll_goal}}

## 📊 10 IDÉES DE SONDAGES

### Sondages Engagement (viraux)
1. "Le débat qui divise : [Option A] ou [Option B] ?"
   - 🔵 [Option A]
   - 🔴 [Option B]
   - 🟡 Les deux !
   - ⚫ Aucun...

2. "Unpopular opinion : [Affirmation controversée dans la niche]"
   - 💯 Totalement d'accord
   - 🤔 Ça dépend
   - ❌ Pas du tout
   - 😅 C'est quoi le sujet ?

### Sondages Feedback
3. "Quelle vidéo voulez-vous voir en premier ?"
   - [Sujet A]
   - [Sujet B]
   - [Sujet C]
   - Autre (commentez !)

4. "Comment vous avez trouvé [dernière vidéo] ?"
   - 🔥 Incroyable
   - 👍 Bien
   - 😐 Moyen
   - 👎 Décevant

### Sondages Fun/Personnels
5. "Depuis combien de temps vous suivez la chaîne ?"
   - 📅 Moins d'un mois
   - 📆 1-6 mois
   - 🗓️ 6 mois - 1 an
   - 🏆 OG (+ d'un an)

---

**Bonnes pratiques :**
✅ 4 options maximum
✅ Une option "fun" ou "autre"
✅ Répondre aux commentaires
✅ Partager les résultats après`,
  subcategory: 'engagement'
};
