import { AITool } from '../../types';

export const facebookGroupPost: AITool = {
  id: 'facebook-group-post',
  slug: 'facebook-group-post',
  name: { fr: 'Post Groupe Facebook', ar: 'منشور مجموعة فيسبوك', en: 'Facebook Group Post' },
  description: {
    fr: 'Créez des posts engageants pour animer vos groupes Facebook',
    ar: 'أنشئ منشورات جذابة لتنشيط مجموعات فيسبوك',
    en: 'Create engaging posts to animate your Facebook groups'
  },
  category: 'social',
  subcategory: 'facebook',
  icon: 'Users',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'group_topic', type: 'text', label: 'Thème du groupe', required: true },
    { name: 'post_type', type: 'select', label: 'Type de post', options: [
      'Lancer une discussion',
      'Poser une question',
      'Sondage',
      'Accueil nouveaux membres',
      'Rappel des règles',
      'Promotion (subtile)',
      'Annonce événement',
      'Célébration/Victoires'
    ]},
    { name: 'goal', type: 'select', label: 'Objectif', options: ['Engagement', 'Ventes', 'Communauté', 'Feedback'] },
    { name: 'group_size', type: 'select', label: 'Taille du groupe', options: ['Small (<500)', 'Medium (500-5000)', 'Large (>5000)'] }
  ],
  outputs: [{ type: 'markdown', name: 'posts' }],
  promptTemplate: `Tu es un community manager expert en groupes Facebook.

THÈME : {{group_topic}}
TYPE : {{post_type}}
OBJECTIF : {{goal}}
TAILLE : {{group_size}}

## 👥 3 POSTS GROUPE FACEBOOK

{{#if post_type.includes('discussion')}}
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
{{/if}}

{{#if post_type.includes('Accueil')}}
### Post d'accueil hebdomadaire

👋 **BIENVENUE aux nouveaux membres !**

Cette semaine, on accueille [X] nouvelles personnes dans notre communauté [nom du groupe] ! 🎉

Pour bien démarrer :
1️⃣ Présentez-vous en commentaire (prénom, ville, pourquoi vous êtes là)
2️⃣ Lisez les règles épinglées
3️⃣ N'hésitez pas à poser vos questions !

**Anciens membres** : prenez 2 secondes pour souhaiter la bienvenue 🤗

On est [X] membres maintenant, merci d'être là ! 💪
{{/if}}

{{#if post_type.includes('Promotion')}}
### Post promotionnel (subtil)

💡 **[Problème que rencontrent les membres]**

[Contexte et identification]

Personnellement, voici comment j'ai résolu ça : [solution]

J'ai d'ailleurs créé [produit/service] pour ceux qui veulent aller plus loin.

👉 [Lien] (supprimez si ce n'est pas autorisé, admins !)

**Qui d'autre galère avec [problème] ?**
{{/if}}

---

**Bonnes pratiques Groupes FB :**
✅ Poster aux heures actives (12h-14h, 19h-21h)
✅ Répondre à TOUS les commentaires
✅ Taguer les membres actifs
✅ Éviter les liens dans le post principal
✅ Utiliser les sondages natifs FB`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const linkedinArticleOutline: AITool = {
  id: 'linkedin-article-outline',
  slug: 'linkedin-article-outline',
  name: { fr: 'Plan d\'Article LinkedIn', ar: 'مخطط مقال لينكدإن', en: 'LinkedIn Article Outline' },
  description: {
    fr: 'Structurez des articles LinkedIn longs qui établissent votre autorité',
    ar: 'هيكل مقالات لينكدإن الطويلة لبناء سلطتك',
    en: 'Structure long LinkedIn articles that establish your authority'
  },
  category: 'social',
  subcategory: 'linkedin',
  icon: 'FileText',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'article_topic', type: 'text', label: 'Sujet de l\'article', required: true },
    { name: 'target_audience', type: 'text', label: 'Audience cible' },
    { name: 'article_goal', type: 'select', label: 'Objectif', options: [
      'Thought Leadership',
      'How-to / Guide',
      'Analyse sectorielle',
      'Conseils carrière',
      'Étude de cas'
    ]},
    { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir' },
    { name: 'word_count', type: 'select', label: 'Longueur cible', options: ['800', '1200', '1500', '2000'] }
  ],
  outputs: [{ type: 'markdown', name: 'outline' }],
  promptTemplate: `Tu es un expert LinkedIn avec des articles à 100K+ vues.

SUJET : {{article_topic}}
AUDIENCE : {{target_audience}}
OBJECTIF : {{article_goal}}
LONGUEUR : {{word_count}} mots

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
✅ CTA en fin d'article`,
  model: 'claude',
  estimatedTime: '45s'
};

export const socialContestGenerator: AITool = {
  id: 'social-contest-generator',
  slug: 'social-contest-generator',
  name: { fr: 'Générateur de Concours', ar: 'مولد المسابقات', en: 'Contest Generator' },
  description: {
    fr: 'Créez des concours et giveaways qui font exploser votre croissance',
    ar: 'أنشئ مسابقات وهدايا تفجر نموك',
    en: 'Create contests and giveaways that explode your growth'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'Gift',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'prize', type: 'text', label: 'Lot à gagner', required: true },
    { name: 'prize_value', type: 'text', label: 'Valeur du lot' },
    { name: 'platform', type: 'select', label: 'Plateforme principale', options: ['Instagram', 'TikTok', 'Facebook', 'Twitter', 'Multi'] },
    { name: 'goal', type: 'select', label: 'Objectif principal', options: [
      'Gagner des followers',
      'Maximiser l\'engagement',
      'Générer du UGC',
      'Collecter des emails',
      'Notoriété'
    ]},
    { name: 'duration', type: 'select', label: 'Durée', options: ['3 jours', '1 semaine', '2 semaines', '1 mois'] },
    { name: 'brand_name', type: 'text', label: 'Nom de la marque' }
  ],
  outputs: [{ type: 'markdown', name: 'contest' }],
  promptTemplate: `Tu es un expert en growth hacking et concours viraux.

LOT : {{prize}} ({{prize_value}})
PLATEFORME : {{platform}}
OBJECTIF : {{goal}}
DURÉE : {{duration}}
MARQUE : {{brand_name}}

## 🎁 CONCOURS VIRAL

### 📣 ANNONCE DU CONCOURS

**Version Instagram :**

🎉 **CONCOURS** 🎉

On vous offre [{{prize}}] ! 🎁

Pour participer, c'est simple :
1️⃣ Follow @{{brand_name}}
2️⃣ Like ce post ❤️
3️⃣ Tag 2 amis en commentaire 👇
{{#if goal.includes('UGC')}}
4️⃣ Partage en story avec @{{brand_name}} (+1 chance)
{{/if}}

⏰ Tirage au sort le [DATE]
🏆 1 gagnant annoncé en story

Bonne chance ! 🍀

---

### 📋 RÈGLEMENT (à poster en commentaire ou lien)

**RÈGLEMENT DU JEU-CONCOURS "{{prize}}"**

**Article 1 - Organisation**
Le présent jeu-concours est organisé par {{brand_name}}.

**Article 2 - Conditions de participation**
- Être majeur ou avoir l'autorisation parentale
- Résider en [pays]
- Avoir un compte [plateforme] public

**Article 3 - Modalités**
[Détails des actions à effectuer]

**Article 4 - Durée**
Du [DATE DÉBUT] au [DATE FIN] à 23h59.

**Article 5 - Désignation du gagnant**
Tirage au sort aléatoire parmi les participants éligibles.

**Article 6 - Lots**
1 x {{prize}} (valeur : {{prize_value}})

**Article 7 - Remise du lot**
Le gagnant sera contacté par DM sous 48h.

---

### 📅 CALENDRIER

| Jour | Action |
|------|--------|
| J-3 | Teaser en story |
| J | Lancement concours |
| J+2 | Rappel #1 |
| J+5 | Rappel #2 + compteur |
| J+7 | Clôture + tirage |
| J+8 | Annonce gagnant |

---

### 📊 MÉTRIQUES À SUIVRE

- Nouveaux followers
- Commentaires/participations
- Reach du post
- Taux d'engagement
- Coût par follower acquis

---

### 💡 ASTUCES POUR MAXIMISER

✅ Poster à heure de pointe
✅ Relancer en story tous les 2 jours
✅ Répondre à TOUS les commentaires
✅ Collaborer avec d'autres comptes
✅ Faire un "last call" 24h avant la fin`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const whatsappBroadcastMessage: AITool = {
  id: 'whatsapp-broadcast-message',
  slug: 'whatsapp-broadcast-message',
  name: { fr: 'Message Broadcast WhatsApp', ar: 'رسالة بث واتساب', en: 'WhatsApp Broadcast Message' },
  description: {
    fr: 'Rédigez des messages WhatsApp Business efficaces pour vos campagnes',
    ar: 'اكتب رسائل واتساب بيزنس فعالة لحملاتك',
    en: 'Write effective WhatsApp Business messages for your campaigns'
  },
  category: 'social',
  subcategory: 'messaging',
  icon: 'MessageCircle',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'message_type', type: 'select', label: 'Type de message', required: true, options: [
      'Promotion/Offre',
      'Nouveau produit',
      'Rappel/Relance',
      'Invitation événement',
      'Mise à jour/Info',
      'Remerciement'
    ]},
    { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'offer_details', type: 'textarea', label: 'Détails de l\'offre/message' },
    { name: 'cta', type: 'select', label: 'Action souhaitée', options: ['Répondre', 'Appeler', 'Visiter boutique', 'Cliquer lien', 'Commander'] },
    { name: 'urgency', type: 'boolean', label: 'Ajouter de l\'urgence' }
  ],
  outputs: [{ type: 'markdown', name: 'whatsapp' }],
  promptTemplate: `Tu es un expert en WhatsApp Marketing.

TYPE : {{message_type}}
ENTREPRISE : {{business_name}}
DÉTAILS : {{offer_details}}
CTA : {{cta}}
URGENCE : {{urgency}}

## 📱 3 MESSAGES WHATSAPP

### Message 1 : Direct et efficace

Salam ! 👋

[Message principal court]

{{#if message_type.includes('Promotion')}}
🎁 **OFFRE SPÉCIALE** : {{offer_details}}

{{#if urgency}}⚠️ Valable jusqu'au [DATE] seulement !{{/if}}
{{/if}}

👉 [CTA clair]

{{business_name}}

---

### Message 2 : Avec personnalisation

Bonjour [Prénom] ! 😊

[Message personnalisé selon l'historique client]

[Offre/Info]

Répondez "OUI" pour [action] !

À bientôt,
L'équipe {{business_name}}

---

### Message 3 : Format liste

✨ **{{business_name}}** ✨

[Intro courte]

Ce qu'on vous propose :
✅ [Avantage 1]
✅ [Avantage 2]
✅ [Avantage 3]

📞 [Numéro] pour commander
🔗 [Lien]

---

**Règles WhatsApp Business :**
✅ Max 1024 caractères
✅ Personnaliser quand possible
✅ 1 message/semaine max (éviter le spam)
✅ Inclure option de désinscription
✅ Respecter les templates approuvés
✅ Éviter les mots spam (GRATUIT, URGENT...)`,
  model: 'gpt4',
  estimatedTime: '25s'
};

export const telegramChannelPost: AITool = {
  id: 'telegram-channel-post',
  slug: 'telegram-channel-post',
  name: { fr: 'Post Canal Telegram', ar: 'منشور قناة تيليغرام', en: 'Telegram Channel Post' },
  description: {
    fr: 'Créez des posts engageants pour votre canal Telegram',
    ar: 'أنشئ منشورات جذابة لقناتك على تيليغرام',
    en: 'Create engaging posts for your Telegram channel'
  },
  category: 'social',
  subcategory: 'messaging',
  icon: 'Send',
  credits: 8,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'channel_niche', type: 'text', label: 'Niche du canal', required: true },
    { name: 'post_type', type: 'select', label: 'Type de post', options: [
      'News/Actualité',
      'Tips/Conseils',
      'Ressource/Lien',
      'Discussion (avec groupe lié)',
      'Sondage',
      'Contenu exclusif'
    ]},
    { name: 'content_topic', type: 'text', label: 'Sujet du post', required: true },
    { name: 'include_media', type: 'select', label: 'Média', options: ['None', 'Image', 'Video', 'Document'] }
  ],
  outputs: [{ type: 'markdown', name: 'post' }],
  promptTemplate: `Tu es un expert en communautés Telegram.

NICHE : {{channel_niche}}
TYPE : {{post_type}}
SUJET : {{content_topic}}

## 📢 3 POSTS TELEGRAM

### Post 1 : Format News

📰 **[TITRE ACCROCHEUR]**

[Contenu principal - 2-3 paragraphes]

🔗 Source : [lien]

💬 Vos réactions ? Rejoignez le groupe de discussion : [lien groupe]

#{{hashtag1}} #{{hashtag2}}

---

### Post 2 : Format Tips

💡 **[X] conseils pour [sujet]**

1️⃣ [Conseil 1]
→ [Explication courte]

2️⃣ [Conseil 2]
→ [Explication]

3️⃣ [Conseil 3]
→ [Explication]

📌 Sauvegardez ce post pour plus tard !

🔔 Activez les notifs pour ne rien rater

---

### Post 3 : Format Ressource

📚 **RESSOURCE GRATUITE**

[Description de ce qu'on partage]

👇 **Télécharger ici :**
[Fichier joint ou lien]

♻️ Partagez à quelqu'un qui en a besoin !

---

**Bonnes pratiques Telegram :**
✅ Utiliser les formatages (gras, italique, code)
✅ Ajouter des émojis pour la lisibilité
✅ Inclure des hashtags pour la recherche
✅ Poster régulièrement (1-3x/jour selon niche)
✅ Utiliser les sondages pour l'engagement
✅ Épingler les posts importants`,
  model: 'gpt4',
  estimatedTime: '25s'
};

export const discordAnnouncement: AITool = {
  id: 'discord-announcement',
  slug: 'discord-announcement',
  name: { fr: 'Annonce Discord', ar: 'إعلان ديسكورد', en: 'Discord Announcement' },
  description: {
    fr: 'Rédigez des annonces Discord percutantes pour votre serveur',
    ar: 'اكتب إعلانات ديسكورد مؤثرة لخادمك',
    en: 'Write impactful Discord announcements for your server'
  },
  category: 'social',
  subcategory: 'community',
  icon: 'MessageSquare',
  credits: 8,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'server_type', type: 'select', label: 'Type de serveur', options: [
      'Gaming', 'Crypto/NFT', 'Tech/Dev', 'Créateur de contenu', 'Marque/Entreprise', 'Éducation'
    ]},
    { name: 'announcement_type', type: 'select', label: 'Type d\'annonce', options: [
      'Mise à jour', 'Événement', 'Giveaway', 'Règles', 'Bienvenue', 'Partenariat'
    ]},
    { name: 'announcement_content', type: 'textarea', label: 'Contenu de l\'annonce', required: true },
    { name: 'mention', type: 'select', label: 'Mention', options: ['None', 'Everyone', 'Here', 'Role'] }
  ],
  outputs: [{ type: 'markdown', name: 'announcement' }],
  promptTemplate: `Tu es un community manager Discord expert.

SERVEUR : {{server_type}}
TYPE : {{announcement_type}}
CONTENU : {{announcement_content}}
MENTION : {{mention}}

## 🎮 ANNONCE DISCORD

### Format Standard

{{#if mention === 'Everyone'}}@everyone{{/if}}
{{#if mention === 'Here'}}@here{{/if}}

───────────────────
{{#if announcement_type.includes('Mise à jour')}}📢 **MISE À JOUR**{{/if}}
{{#if announcement_type.includes('Événement')}}🎉 **ÉVÉNEMENT**{{/if}}
{{#if announcement_type.includes('Giveaway')}}🎁 **GIVEAWAY**{{/if}}
───────────────────

[Contenu principal avec formatage Discord]

**📌 Points importants :**
- [Point 1]
- [Point 2]
- [Point 3]

{{#if announcement_type.includes('Événement')}}
📅 **Date :** [Date]
⏰ **Heure :** [Heure]
📍 **Où :** [Canal/Lien]
{{/if}}

{{#if announcement_type.includes('Giveaway')}}
🎁 **Lot :** [Description]
⏰ **Fin :** [Date/Heure]
✅ **Pour participer :** Réagissez avec 🎉
{{/if}}

───────────────────

👇 **Réagissez si vous avez lu !**
❓ Questions ? → #support

---

### Format Embed (description pour bot)

**Titre :** [Titre]
**Couleur :** [Hex - #FF5733]
**Description :** [Contenu]
**Fields :**
- Nom: [X] | Valeur: [Y]
**Footer :** [Texte footer]
**Thumbnail :** [URL image]

---

**Formatage Discord :**
\`\`\`
**gras**
*italique*
__souligné__
~~barré~~
> citation
\`code\`
\`\`\`bloc code\`\`\`
[texte](lien)
\`\`\`

**Emojis serveur suggérés :**
:check: :cross: :warning: :info: :fire:`,
  model: 'gpt4',
  estimatedTime: '30s'
};
