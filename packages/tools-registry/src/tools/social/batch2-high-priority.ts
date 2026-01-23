import { AITool } from '../../types';

export const linkedinHeadlineGenerator: AITool = {
  id: 'linkedin-headline-generator',
  slug: 'linkedin-headline-generator',
  name: { fr: 'Générateur de Titre LinkedIn', ar: 'مولد عناوين لينكدإن', en: 'LinkedIn Headline Generator' },
  description: {
    fr: 'Créez des titres LinkedIn percutants qui attirent les recruteurs et clients',
    ar: 'أنشئ عناوين لينكدإن مؤثرة تجذب المجندين',
    en: 'Create impactful LinkedIn headlines that attract recruiters and clients'
  },
  category: 'social',
  subcategory: 'linkedin',
  icon: 'Linkedin',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'current_role', type: 'text', label: 'Poste actuel', required: true },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité', required: true },
    { name: 'target_audience', type: 'select', label: 'Audience cible', options: [
      'Recruteurs',
      'Clients potentiels',
      'Réseau professionnel',
      'Investisseurs'
    ]},
    { name: 'unique_value', type: 'text', label: 'Votre valeur unique' },
    { name: 'keywords', type: 'text', label: 'Mots-clés SEO à inclure' },
    { name: 'style', type: 'select', label: 'Style', options: ['Classique', 'Créatif', 'Résultats', 'Mission'] }
  ],
  outputs: [{ type: 'markdown', name: 'headlines' }],
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
[Qui vous êtes] | [Ce que vous faites] | [Pour qui/Résultat]`,
  model: 'claude',
  estimatedTime: '20s'
};

export const linkedinSummaryGenerator: AITool = {
  id: 'linkedin-summary-generator',
  slug: 'linkedin-summary-generator',
  name: { fr: 'Générateur de Résumé LinkedIn', ar: 'مولد ملخص لينكدإن', en: 'LinkedIn Summary Generator' },
  description: {
    fr: 'Rédigez un "À propos" LinkedIn captivant qui convertit les visiteurs',
    ar: 'اكتب قسم "حول" جذاب يحول الزوار',
    en: 'Write a captivating LinkedIn About section that converts visitors'
  },
  category: 'social',
  subcategory: 'linkedin',
  icon: 'FileText',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'current_role', type: 'text', label: 'Poste actuel', required: true },
    { name: 'years_experience', type: 'number', label: 'Années d\'expérience' },
    { name: 'key_achievements', type: 'textarea', label: 'Réalisations clés (3-5)' },
    { name: 'skills', type: 'text', label: 'Compétences principales' },
    { name: 'target_audience', type: 'text', label: 'Qui voulez-vous attirer ?' },
    { name: 'personality', type: 'textarea', label: 'Quelque chose de personnel (passion, valeurs...)' },
    { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Contact', 'Connect', 'Visit website', 'Schedule call', 'Download'] },
    { name: 'tone', type: 'select', options: ['Professionnel', 'Storytelling', 'Conversationnel', 'Inspirant'] }
  ],
  outputs: [{ type: 'markdown', name: 'summary' }],
  promptTemplate: `Tu es un expert en personal branding LinkedIn.

POSTE : {{current_role}}
EXPÉRIENCE : {{years_experience}} ans
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
✅ CTA en fin de section`,
  model: 'claude',
  estimatedTime: '45s'
};

export const twitterBioGenerator: AITool = {
  id: 'twitter-bio-generator',
  slug: 'twitter-bio-generator',
  name: { fr: 'Générateur de Bio Twitter/X', ar: 'مولد بايو تويتر', en: 'Twitter/X Bio Generator' },
  description: {
    fr: 'Créez une bio Twitter percutante en 160 caractères',
    ar: 'أنشئ بايو تويتر مؤثر في 160 حرف',
    en: 'Create a punchy Twitter bio in 160 characters'
  },
  category: 'social',
  subcategory: 'twitter',
  icon: 'Twitter',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'name', type: 'text', label: 'Nom/Pseudo', required: true },
    { name: 'occupation', type: 'text', label: 'Ce que vous faites', required: true },
    { name: 'interests', type: 'text', label: 'Centres d\'intérêt (tweets sur...)' },
    { name: 'personality', type: 'select', label: 'Personnalité', options: ['Sérieux', 'Humoristique', 'Provocateur', 'Minimaliste', 'Inspirant'] },
    { name: 'include_location', type: 'text', label: 'Localisation (optionnel)' },
    { name: 'include_link', type: 'text', label: 'Lien à promouvoir' }
  ],
  outputs: [{ type: 'markdown', name: 'bios' }],
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
✅ CTA vers link in bio si pertinent`,
  model: 'claude',
  estimatedTime: '20s'
};

export const tiktokHashtagGenerator: AITool = {
  id: 'tiktok-hashtag-generator',
  slug: 'tiktok-hashtag-generator',
  name: { fr: 'Hashtags TikTok Viraux', ar: 'هاشتاغات تيك توك فيروسية', en: 'Viral TikTok Hashtags' },
  description: {
    fr: 'Générez les meilleurs hashtags TikTok pour maximiser votre portée',
    ar: 'أنشئ أفضل هاشتاغات تيك توك لزيادة الوصول',
    en: 'Generate the best TikTok hashtags to maximize reach'
  },
  category: 'social',
  subcategory: 'tiktok',
  icon: 'Hash',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true },
    { name: 'niche', type: 'text', label: 'Niche/Catégorie', required: true },
    { name: 'video_style', type: 'select', label: 'Style de vidéo', options: ['Trend', 'Educational', 'Comedy', 'Lifestyle', 'Business', 'Beauty', 'Fitness'] },
    { name: 'target_country', type: 'select', label: 'Pays cible', options: ['France', 'Algerie', 'Maroc', 'Belgique', 'Canada', 'International'] }
  ],
  outputs: [{ type: 'markdown', name: 'hashtags' }],
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
{{#if target_country === 'Algerie'}}
#algerie #dz #alger #tikokdz
{{/if}}
{{#if target_country === 'France'}}
#france #tiktokfrance #french
{{/if}}

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
❌ #follow4follow #like4like #spam...`,
  model: 'claude',
  estimatedTime: '20s'
};

export const instagramStoryIdeas: AITool = {
  id: 'instagram-story-ideas',
  slug: 'instagram-story-ideas',
  name: { fr: 'Idées de Stories Instagram', ar: 'أفكار ستوري انستغرام', en: 'Instagram Story Ideas' },
  description: {
    fr: 'Générez des idées de Stories engageantes pour booster vos interactions',
    ar: 'أنشئ أفكار ستوري جذابة لزيادة التفاعل',
    en: 'Generate engaging Story ideas to boost interactions'
  },
  category: 'social',
  subcategory: 'instagram',
  icon: 'Circle',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'niche', type: 'text', label: 'Niche/Secteur', required: true },
    { name: 'goal', type: 'select', label: 'Objectif', options: [
      'Engagement (réponses, réactions)',
      'Trafic (lien)',
      'Ventes',
      'Croissance (nouveaux followers)',
      'Connexion (personnel)'
    ]},
    { name: 'story_count', type: 'select', label: 'Nombre d\'idées', options: ['7', '14', '30'] },
    { name: 'include_interactive', type: 'boolean', label: 'Inclure stickers interactifs', default: true }
  ],
  outputs: [{ type: 'markdown', name: 'stories' }],
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

{{#if goal.includes('Engagement')}}
**Top Stories pour l'engagement :**
1. Question box + réponses
2. Sondages "Ceci ou cela"
3. Quiz avec résultats
4. Slider emoji "À quel point vous êtes d'accord ?"
5. "Envoyez-moi un 🔥 si..."
{{/if}}

{{#if goal.includes('Ventes')}}
**Top Stories pour les ventes :**
1. Témoignage client + lien
2. Unboxing/Démo produit
3. FAQ produit
4. Countdown promo
5. "DM pour [offre]"
{{/if}}

---

### 🛠️ STICKERS INTERACTIFS

| Sticker | Usage | Engagement |
|---------|-------|------------|
| 📊 Sondage | Choix binaire | ⭐⭐⭐⭐⭐ |
| ❓ Question | Q&A, feedback | ⭐⭐⭐⭐⭐ |
| 📏 Slider | Opinions graduées | ⭐⭐⭐⭐ |
| 🎯 Quiz | Éducatif/fun | ⭐⭐⭐⭐ |
| ⏰ Countdown | Events, lancements | ⭐⭐⭐ |
| 🔗 Lien | Trafic externe | ⭐⭐⭐ |`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const socialProofGenerator: AITool = {
  id: 'social-proof-generator',
  slug: 'social-proof-generator',
  name: { fr: 'Générateur de Témoignages', ar: 'مولد الشهادات', en: 'Social Proof Generator' },
  description: {
    fr: 'Transformez les retours clients en témoignages persuasifs pour vos réseaux',
    ar: 'حول تعليقات العملاء إلى شهادات مقنعة',
    en: 'Transform customer feedback into persuasive testimonials'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'Star',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'raw_feedback', type: 'textarea', label: 'Retour client brut (copier-coller)', required: true },
    { name: 'product_service', type: 'text', label: 'Produit/Service concerné' },
    { name: 'platform', type: 'select', label: 'Plateforme de publication', options: ['Instagram', 'LinkedIn', 'Website', 'Facebook', 'All'] },
    { name: 'format', type: 'select', label: 'Format souhaité', options: [
      'Citation courte',
      'Mini-histoire',
      'Avec chiffres',
      'Avant/Après'
    ]}
  ],
  outputs: [{ type: 'markdown', name: 'testimonials' }],
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
4. Que diriez-vous à quelqu'un qui hésite ?`,
  model: 'gpt4',
  estimatedTime: '25s'
};

export const ugcBriefGenerator: AITool = {
  id: 'ugc-brief-generator',
  slug: 'ugc-brief-generator',
  name: { fr: 'Brief Créateur UGC', ar: 'موجز منشئ UGC', en: 'UGC Creator Brief' },
  description: {
    fr: 'Créez des briefs professionnels pour vos collaborations UGC',
    ar: 'أنشئ موجزات احترافية لتعاونات UGC',
    en: 'Create professional briefs for UGC collaborations'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'FileText',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true },
    { name: 'product', type: 'text', label: 'Produit/Service', required: true },
    { name: 'content_type', type: 'select', label: 'Type de contenu', options: ['Unboxing', 'Review', 'Tutorial', 'Lifestyle', 'Testimonial', 'Trend'] },
    { name: 'platform', type: 'text', label: 'Plateformes (TikTok, Reels...)' },
    { name: 'key_messages', type: 'textarea', label: 'Messages clés à transmettre' },
    { name: 'budget', type: 'text', label: 'Budget (optionnel)' },
    { name: 'deadline', type: 'text', label: 'Deadline' }
  ],
  outputs: [{ type: 'markdown', name: 'brief' }],
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
[Nom] - [Email] - [Téléphone]`,
  model: 'claude',
  estimatedTime: '40s'
};

export const influencerOutreachEmail: AITool = {
  id: 'influencer-outreach-email',
  slug: 'influencer-outreach-email',
  name: { fr: 'Email Outreach Influenceurs', ar: 'بريد التواصل مع المؤثرين', en: 'Influencer Outreach Email' },
  description: {
    fr: 'Rédigez des emails de prospection efficaces pour contacter des influenceurs',
    ar: 'اكتب رسائل بريد فعالة للتواصل مع المؤثرين',
    en: 'Write effective outreach emails to contact influencers'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'Mail',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'influencer_name', type: 'text', label: 'Nom de l\'influenceur', required: true },
    { name: 'influencer_niche', type: 'text', label: 'Niche de l\'influenceur' },
    { name: 'brand_name', type: 'text', label: 'Votre marque', required: true },
    { name: 'product_service', type: 'text', label: 'Produit/Service à promouvoir' },
    { name: 'collab_type', type: 'select', label: 'Type de collaboration', options: ['Gifting', 'Paid', 'Affiliate', 'Ambassador', 'Event'] },
    { name: 'budget', type: 'text', label: 'Budget (si paid)' },
    { name: 'specific_content', type: 'text', label: 'Contenu spécifique souhaité (optionnel)' }
  ],
  outputs: [{ type: 'markdown', name: 'email' }],
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
✅ Pas de pièces jointes (1er contact)`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const socialMediaReport: AITool = {
  id: 'social-media-report',
  slug: 'social-media-report',
  name: { fr: 'Rapport Réseaux Sociaux', ar: 'تقرير وسائل التواصل', en: 'Social Media Report' },
  description: {
    fr: 'Générez des rapports de performance professionnels pour vos clients',
    ar: 'أنشئ تقارير أداء احترافية لعملائك',
    en: 'Generate professional performance reports for clients'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'BarChart',
  credits: 20,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'brand_name', type: 'text', label: 'Nom du client/marque', required: true },
    { name: 'period', type: 'select', label: 'Période', options: ['Weekly', 'Monthly', 'Quarterly'] },
    { name: 'platforms', type: 'text', label: 'Plateformes (Instagram, TikTok...)' },
    { name: 'metrics', type: 'textarea', label: 'Métriques clés (collez vos données)' },
    { name: 'highlights', type: 'textarea', label: 'Faits marquants de la période' },
    { name: 'goals_next_period', type: 'textarea', label: 'Objectifs période suivante' }
  ],
  outputs: [{ type: 'markdown', name: 'report' }],
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

*Rapport généré le [Date]*`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const contentRepurposePlanner: AITool = {
  id: 'content-repurpose-planner',
  slug: 'content-repurpose-planner',
  name: { fr: 'Planificateur de Réutilisation', ar: 'مخطط إعادة استخدام المحتوى', en: 'Content Repurpose Planner' },
  description: {
    fr: 'Transformez un contenu en 10+ formats pour toutes les plateformes',
    ar: 'حول محتوى واحد إلى 10+ صيغ لكل المنصات',
    en: 'Transform one piece of content into 10+ formats for all platforms'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'Repeat',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'original_content', type: 'select', label: 'Type de contenu original', required: true, options: [
      'Article de blog',
      'Vidéo YouTube',
      'Podcast',
      'Webinaire',
      'E-book'
    ]},
    { name: 'content_summary', type: 'textarea', label: 'Résumé du contenu', required: true },
    { name: 'key_points', type: 'textarea', label: 'Points clés (5-7)' },
    { name: 'target_platforms', type: 'text', label: 'Plateformes cibles' }
  ],
  outputs: [{ type: 'markdown', name: 'plan' }],
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

**Règle d'or :** 1 contenu original = 3 semaines de contenu recyclé`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const viralHookGenerator: AITool = {
  id: 'viral-hook-generator',
  slug: 'viral-hook-generator',
  name: { fr: 'Générateur de Hooks Viraux', ar: 'مولد الخطافات الفيروسية', en: 'Viral Hook Generator' },
  description: {
    fr: 'Créez des accroches irrésistibles pour toutes les plateformes',
    ar: 'أنشئ خطافات لا تقاوم لكل المنصات',
    en: 'Create irresistible hooks for all platforms'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'Anchor',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'topic', type: 'text', label: 'Sujet du contenu', required: true },
    { name: 'platform', type: 'select', label: 'Plateforme principale', options: ['TikTok', 'Instagram', 'YouTube', 'LinkedIn', 'Twitter', 'All'] },
    { name: 'hook_type', type: 'select', label: 'Type de hook', options: [
      'Curiosity', 'Controversy', 'Story', 'Statistic', 'Question', 'Promise', 'Fear', 'Mistake'
    ]},
    { name: 'target_emotion', type: 'select', label: 'Émotion cible', options: ['Curiosité', 'Surprise', 'FOMO', 'Identification', 'Inspiration'] }
  ],
  outputs: [{ type: 'markdown', name: 'hooks' }],
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
✅ Parler directement au viewer (tu/vous)`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const engagementResponseTemplates: AITool = {
  id: 'engagement-response-templates',
  slug: 'engagement-response-templates',
  name: { fr: 'Templates de Réponses', ar: 'قوالب الردود', en: 'Response Templates' },
  description: {
    fr: 'Bibliothèque de réponses pour gérer votre communauté efficacement',
    ar: 'مكتبة ردود لإدارة مجتمعك بكفاءة',
    en: 'Response library to manage your community efficiently'
  },
  category: 'social',
  subcategory: 'strategy',
  icon: 'MessageSquare',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'brand_voice', type: 'select', label: 'Ton de la marque', options: ['Professionnel', 'Amical', 'Humoristique', 'Premium', 'Jeune'] },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité' },
    { name: 'common_situations', type: 'text', label: 'Situations à couvrir (Compliment, Question, Réclamation...)' }
  ],
  outputs: [{ type: 'markdown', name: 'templates' }],
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
✅ Remercier même les critiques`,
  model: 'gpt4',
  estimatedTime: '30s'
};
