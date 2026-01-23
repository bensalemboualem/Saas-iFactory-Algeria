import { AITool } from '../../types';

export const thumbnailIdeaGenerator: AITool = {
  id: 'thumbnail-idea-generator',
  slug: 'thumbnail-idea-generator',
  name: { fr: 'Générateur d\'Idées de Miniatures', ar: 'مولد أفكار الصور المصغرة', en: 'Thumbnail Idea Generator' },
  description: {
    fr: 'Créez des concepts de miniatures YouTube qui maximisent les clics',
    ar: 'أنشئ أفكار صور مصغرة يوتيوب تزيد النقرات',
    en: 'Create YouTube thumbnail concepts that maximize clicks'
  },
  category: 'design',
  subcategory: 'social',
  icon: 'Play',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'video_title', type: 'text', label: 'Titre de la vidéo', required: true },
    { name: 'video_topic', type: 'textarea', label: 'Sujet de la vidéo' },
    { name: 'channel_niche', type: 'select', label: 'Niche de la chaîne', options: [
      'Tech/Tutoriels', 'Gaming', 'Lifestyle', 'Business', 'Éducation', 'Divertissement', 'Fitness', 'Cuisine'
    ]},
    { name: 'thumbnail_style', type: 'select', label: 'Style préféré', options: [
      'Face reaction', 'Before/After', 'Text-heavy', 'Minimalist', 'Clickbait', 'Professional'
    ]},
    { name: 'brand_colors', type: 'text', label: 'Couleurs de marque' }
  ],
  outputs: [{ type: 'markdown', name: 'thumbnail_concepts' }],
  promptTemplate: `Tu es un expert en optimisation YouTube avec +1M de vues.

TITRE : {{video_title}}
SUJET : {{video_topic}}
NICHE : {{channel_niche}}
STYLE : {{thumbnail_style}}
COULEURS : {{brand_colors}}

## 🎬 CONCEPTS DE MINIATURES YOUTUBE

### SPECS TECHNIQUES

| Paramètre | Valeur |
|-----------|--------|
| Dimensions | 1280 x 720 px |
| Ratio | 16:9 |
| Taille max | 2 MB |
| Format | JPG, PNG, GIF |

---

### CONCEPT 1 : [Nom du concept]

**🖼️ Description visuelle :**
[Description détaillée de la miniature - composition, éléments, couleurs]

**📝 Texte sur l'image :**
"[Texte court et impactant - max 3-4 mots]"

**🎨 Éléments clés :**
- Arrière-plan : [Description]
- Sujet principal : [Description]
- Éléments graphiques : [Flèches, cercles, emojis...]
- Expression faciale : [Si applicable]

**🎯 Pourquoi ça marche :**
- [Raison psychologique 1]
- [Raison psychologique 2]

**Prompt Midjourney :**
\`\`\`
youtube thumbnail, {{video_topic}}, [description], bright colors, high contrast, professional, 16:9 --ar 16:9 --v 6
\`\`\`

---

### CONCEPT 2 : Style Avant/Après

**🖼️ Description visuelle :**
Split screen avec transformation visuelle

**📝 Texte :**
Gauche : "AVANT" / Droite : "APRÈS"

**🎨 Éléments :**
- Flèche de progression
- Contraste de couleurs (gris → vibrant)
- Émoji 🤯 ou ➡️

---

### CONCEPT 3 : Réaction Faciale

**🖼️ Description visuelle :**
Visage en gros plan avec expression forte (surprise, excitation)

**📝 Texte :**
"[MOT-CLÉ CHOC]" en gros caractères

**🎨 Éléments :**
- Fond contrasté (rouge, jaune)
- Ombre portée sur le texte
- Cercle ou flèche pointant vers un élément

---

### CONCEPT 4 : Minimaliste Pro

**🖼️ Description visuelle :**
Design épuré, focus sur un élément central

**📝 Texte :**
[1-2 mots maximum]

**🎨 Éléments :**
- Fond uni ou dégradé subtil
- Typographie bold
- Un seul élément visuel fort

---

### CONCEPT 5 : Clickbait Éthique

**🖼️ Description visuelle :**
Élément intrigant partiellement caché ou flouté

**📝 Texte :**
"[Question ou teaser]"

**🎨 Éléments :**
- Zone floue/censurée
- Point d'interrogation
- Expression de curiosité

---

## ✅ CHECKLIST MINIATURE PARFAITE

- [ ] Lisible sur mobile (petit écran)
- [ ] Contraste élevé
- [ ] Max 3-4 mots de texte
- [ ] Visage visible (si applicable)
- [ ] Cohérent avec la marque
- [ ] Émotion claire
- [ ] Pas de clickbait mensonger

---

## 🎨 PALETTE RECOMMANDÉE

**Couleurs qui performent :**
- 🔴 Rouge : Urgence, énergie
- 🟡 Jaune : Attention, optimisme
- 🔵 Bleu : Confiance, pro
- 🟢 Vert : Succès, argent
- ⚫ Noir : Premium, mystère

**Combinaisons gagnantes :**
- Rouge + Jaune + Blanc
- Bleu + Orange
- Noir + Jaune

---

## 🛠️ OUTILS

| Outil | Usage | Prix |
|-------|-------|------|
| Canva | Templates faciles | Freemium |
| Photoshop | Pro | Payant |
| TubeBuddy | A/B testing | Freemium |
| VidIQ | Analyse concurrence | Freemium |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const infographicOutlineGenerator: AITool = {
  id: 'infographic-outline-generator',
  slug: 'infographic-outline-generator',
  name: { fr: 'Générateur de Plans d\'Infographie', ar: 'مولد مخططات الإنفوغرافيك', en: 'Infographic Outline Generator' },
  description: {
    fr: 'Créez des plans structurés pour des infographies impactantes',
    ar: 'أنشئ مخططات منظمة لإنفوغرافيك مؤثر',
    en: 'Create structured outlines for impactful infographics'
  },
  category: 'design',
  subcategory: 'marketing',
  icon: 'BarChart2',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'infographic_topic', type: 'text', label: 'Sujet de l\'infographie', required: true },
    { name: 'infographic_type', type: 'select', label: 'Type d\'infographie', options: [
      'Statistique', 'Processus/Étapes', 'Comparaison', 'Chronologie', 'Géographique', 'Hiérarchique', 'Liste'
    ]},
    { name: 'target_audience', type: 'text', label: 'Audience cible' },
    { name: 'key_data', type: 'textarea', label: 'Données clés à inclure' },
    { name: 'brand_style', type: 'select', label: 'Style visuel', options: ['Corporate', 'Playful', 'Minimalist', 'Bold', 'Tech'] }
  ],
  outputs: [{ type: 'markdown', name: 'outline' }],
  promptTemplate: `Tu es un designer d'information spécialisé en infographies virales.

SUJET : {{infographic_topic}}
TYPE : {{infographic_type}}
AUDIENCE : {{target_audience}}
DONNÉES : {{key_data}}
STYLE : {{brand_style}}

## 📊 PLAN D'INFOGRAPHIE

### INFORMATIONS GÉNÉRALES

**Titre :** "[Titre accrocheur]"
**Sous-titre :** "[Contexte ou hook]"
**Dimensions recommandées :** 800 x 2000 px (Pinterest-friendly)
**Type :** {{infographic_type}}

---

### STRUCTURE VISUELLE

\`\`\`
┌─────────────────────────────────┐
│         🎯 HEADER               │
│  Titre + Sous-titre + Logo      │
├─────────────────────────────────┤
│         📌 INTRO                │
│  Contexte / Stat choc           │
├─────────────────────────────────┤
│         📊 SECTION 1            │
│  [Contenu principal]            │
├─────────────────────────────────┤
│         📈 SECTION 2            │
│  [Données/Graphiques]           │
├─────────────────────────────────┤
│         💡 SECTION 3            │
│  [Insights/Conseils]            │
├─────────────────────────────────┤
│         🎯 CONCLUSION           │
│  Key takeaway + CTA             │
├─────────────────────────────────┤
│         📋 FOOTER               │
│  Sources + Logo + URL           │
└─────────────────────────────────┘
\`\`\`

---

### SECTION 1 : [TITRE]

**Contenu :**
- [Point 1 avec donnée]
- [Point 2 avec donnée]
- [Point 3 avec donnée]

**Visualisation suggérée :**
{{#if infographic_type === 'Statistique'}}
- Graphique en barres / Camembert
- Icônes avec pourcentages
- Pictogrammes
{{/if}}
{{#if infographic_type.includes('Processus')}}
- Flèches numérotées
- Timeline verticale
- Étapes connectées
{{/if}}
{{#if infographic_type === 'Comparaison'}}
- Tableau côte à côte
- VS au centre
- Couleurs contrastées
{{/if}}

**Icônes à utiliser :**
- [Icône 1] pour [concept]
- [Icône 2] pour [concept]

---

### SECTION 2 : [TITRE]

**Contenu :**
[Détails...]

**Visualisation suggérée :**
[Type de graphique/visuel]

---

### SECTION 3 : [TITRE]

**Contenu :**
[Détails...]

**Visualisation suggérée :**
[Type de graphique/visuel]

---

### DONNÉES CLÉS À METTRE EN AVANT

| Donnée | Valeur | Visualisation |
|--------|--------|---------------|
| [Stat 1] | [Chiffre] | [Type] |
| [Stat 2] | [Chiffre] | [Type] |
| [Stat 3] | [Chiffre] | [Type] |

---

### PALETTE DE COULEURS

**Style {{brand_style}} :**
- Couleur principale : #[HEX]
- Couleur secondaire : #[HEX]
- Couleur d'accent : #[HEX]
- Couleur de fond : #[HEX]
- Couleur de texte : #[HEX]

---

### TYPOGRAPHIE

- **Titres :** [Police Bold] - [Taille]
- **Sous-titres :** [Police Medium] - [Taille]
- **Corps :** [Police Regular] - [Taille]
- **Données :** [Police Bold] - Grande taille

---

### ÉLÉMENTS GRAPHIQUES

- [ ] Icônes cohérentes (même style)
- [ ] Lignes de connexion
- [ ] Formes géométriques
- [ ] Illustrations simples
- [ ] Pictogrammes

---

### CALL-TO-ACTION FINAL

**Texte :** "[CTA]"
**URL :** [Votre site]
**Hashtags :** #[hashtag1] #[hashtag2]

---

### SOURCES

1. [Source 1] - [Année]
2. [Source 2] - [Année]
3. [Source 3] - [Année]

---

## 🛠️ OUTILS RECOMMANDÉS

| Outil | Niveau | Prix |
|-------|--------|------|
| Canva | Débutant | Freemium |
| Piktochart | Intermédiaire | Freemium |
| Venngage | Intermédiaire | Freemium |
| Adobe Illustrator | Avancé | Payant |
| Figma | Avancé | Freemium |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const bannerAdConcept: AITool = {
  id: 'banner-ad-concept',
  slug: 'banner-ad-concept',
  name: { fr: 'Concepts de Bannières Publicitaires', ar: 'أفكار لافتات إعلانية', en: 'Banner Ad Concepts' },
  description: {
    fr: 'Créez des concepts de bannières publicitaires pour vos campagnes display',
    ar: 'أنشئ أفكار لافتات إعلانية لحملاتك',
    en: 'Create banner ad concepts for your display campaigns'
  },
  category: 'design',
  subcategory: 'marketing',
  icon: 'Image',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_service', type: 'text', label: 'Produit/Service', required: true },
    { name: 'campaign_objective', type: 'select', label: 'Objectif', options: [
      'Notoriété', 'Trafic', 'Conversion', 'Retargeting'
    ]},
    { name: 'offer', type: 'text', label: 'Offre/Promotion', placeholder: '-20%, Essai gratuit...' },
    { name: 'target_audience', type: 'text', label: 'Audience cible' },
    { name: 'brand_colors', type: 'text', label: 'Couleurs de marque' },
    { name: 'banner_sizes', type: 'text', label: 'Formats (ex: 300x250, 728x90)' }
  ],
  outputs: [{ type: 'markdown', name: 'concepts' }],
  promptTemplate: `Tu es un directeur artistique spécialisé en publicité display.

PRODUIT : {{product_service}}
OBJECTIF : {{campaign_objective}}
OFFRE : {{offer}}
AUDIENCE : {{target_audience}}
COULEURS : {{brand_colors}}
FORMATS : {{banner_sizes}}

## 🎯 CONCEPTS DE BANNIÈRES PUBLICITAIRES

### FORMATS STANDARDS

| Format | Nom | Usage |
|--------|-----|-------|
| 300x250 | Medium Rectangle | Le plus populaire |
| 728x90 | Leaderboard | En-tête de page |
| 160x600 | Wide Skyscraper | Sidebar |
| 320x50 | Mobile Banner | Mobile |
| 300x600 | Half Page | Fort impact |
| 970x250 | Billboard | Premium |

---

### CONCEPT 1 : [Nom du concept]

**🎨 Direction artistique :**
[Description du style visuel global]

**📐 Layout (300x250) :**
\`\`\`
┌─────────────────────────────┐
│  [LOGO]           [Image]   │
│                             │
│  [HEADLINE]                 │
│  [Sous-titre/Offre]         │
│                             │
│     [CTA BUTTON]            │
└─────────────────────────────┘
\`\`\`

**📝 Textes :**
- Headline : "[Texte accrocheur - max 5 mots]"
- Sous-titre : "[Bénéfice ou offre]"
- CTA : "[Verbe d'action]"

**🖼️ Visuels :**
- Image principale : [Description]
- Style : [Photo/Illustration/Flat]

**🎨 Couleurs :**
- Fond : {{brand_colors}} ou #[HEX]
- CTA : [Couleur contrastée]
- Texte : [Couleur lisible]

---

### CONCEPT 2 : Minimaliste

**📐 Layout :**
Design épuré avec focus sur le message

**📝 Textes :**
- Headline : "[Message direct]"
- CTA : "[Action]"

**🎨 Style :**
- Beaucoup d'espace blanc
- Typographie forte
- Un seul visuel

---

### CONCEPT 3 : Offre Urgente

**📐 Layout :**
Mise en avant de l'offre/promotion

**📝 Textes :**
- Badge : "{{offer}}"
- Headline : "[Bénéfice]"
- Urgence : "Offre limitée !"
- CTA : "[Action maintenant]"

**🎨 Style :**
- Couleurs vives (rouge/orange)
- Badge promotionnel
- Timer visuel (optionnel)

---

### CONCEPT 4 : Storytelling

**📐 Layout :**
Séquence narrative en plusieurs frames

**📝 Textes :**
- Frame 1 : "[Problème]"
- Frame 2 : "[Solution]"
- Frame 3 : "[CTA]"

**🎨 Style :**
- Animation subtile
- Progression visuelle

---

## 📋 DÉCLINAISONS PAR FORMAT

### 728x90 (Leaderboard)
\`\`\`
[Logo] | [Headline] | [Offre] | [CTA]
\`\`\`

### 160x600 (Skyscraper)
\`\`\`
[Logo]
─────
[Image]
─────
[Headline]
[Sous-titre]
─────
[CTA]
\`\`\`

### 320x50 (Mobile)
\`\`\`
[Logo] [Headline court] [CTA]
\`\`\`

---

## ✅ CHECKLIST BANNIÈRE

- [ ] Message clair en < 3 secondes
- [ ] CTA visible et contrasté
- [ ] Logo présent
- [ ] Taille fichier < 150 KB
- [ ] Texte lisible (min 10px)
- [ ] Animation < 15 secondes (si animé)
- [ ] Pas plus de 3 couleurs

---

## 📊 SPECS TECHNIQUES

| Paramètre | Valeur |
|-----------|--------|
| Format | JPG, PNG, GIF, HTML5 |
| Poids max | 150 KB |
| Animation max | 15 sec, 3 loops |
| Police min | 10px |

---

## 🎯 A/B TESTS SUGGÉRÉS

| Variable | Version A | Version B |
|----------|-----------|-----------|
| CTA | "[Option 1]" | "[Option 2]" |
| Headline | "[Version 1]" | "[Version 2]" |
| Couleur CTA | [Couleur 1] | [Couleur 2] |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const productMockupIdeas: AITool = {
  id: 'product-mockup-ideas',
  slug: 'product-mockup-ideas',
  name: { fr: 'Idées de Mockups Produit', ar: 'أفكار نماذج المنتجات', en: 'Product Mockup Ideas' },
  description: {
    fr: 'Générez des idées de mockups créatifs pour présenter vos produits',
    ar: 'أنشئ أفكار نماذج إبداعية لعرض منتجاتك',
    en: 'Generate creative mockup ideas to showcase your products'
  },
  category: 'design',
  subcategory: 'marketing',
  icon: 'Box',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_type', type: 'select', label: 'Type de produit', required: true, options: [
      'Application mobile', 'Site web', 'Produit physique', 'Packaging', 'Livre/Ebook', 'Vêtement', 'Papeterie'
    ]},
    { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
    { name: 'target_use', type: 'select', label: 'Utilisation', options: [
      'Social Media', 'Website', 'Presentation', 'App Store', 'Print', 'Portfolio'
    ]},
    { name: 'style', type: 'select', label: 'Style', options: [
      'Minimalist', 'Lifestyle', 'Professional', 'Playful', 'Premium'
    ]}
  ],
  outputs: [{ type: 'markdown', name: 'mockup_ideas' }],
  promptTemplate: `Tu es un directeur artistique spécialisé en présentation de produits.

PRODUIT : {{product_type}}
NOM : {{product_name}}
UTILISATION : {{target_use}}
STYLE : {{style}}

## 🎨 IDÉES DE MOCKUPS

### MOCKUP 1 : [Nom descriptif]

**📸 Description de la scène :**
[Description détaillée de la mise en scène]

**🎯 Usage idéal :**
{{target_use}}

**📐 Angles suggérés :**
- Vue frontale
- Vue 3/4
- Vue de dessus (flat lay)
- Vue en situation

**🌈 Ambiance :**
- Éclairage : [Type d'éclairage]
- Couleurs de fond : [Palette]
- Props/Accessoires : [Liste]

**Prompt IA pour génération :**
\`\`\`
{{product_type}} mockup, {{product_name}}, {{style}} style, [détails de la scène], professional photography, high quality, studio lighting --ar 4:3
\`\`\`

---

{{#if product_type.includes('App')}}
### MOCKUPS APPLICATION MOBILE

**Mockup 2 : iPhone en main**
- Main tenant l'iPhone avec l'app affichée
- Fond flou lifestyle
- Éclairage naturel

**Mockup 3 : Multi-devices**
- iPhone + iPad + MacBook
- Disposition isométrique
- Fond gradient ou uni

**Mockup 4 : App Store style**
- Écrans côte à côte
- Fond coloré
- Badges et annotations

**Mockup 5 : Flat lay tech**
- iPhone posé sur bureau
- Accessoires autour (casque, café, plante)
- Vue de dessus
{{/if}}

{{#if product_type.includes('Physique')}}
### MOCKUPS PRODUIT PHYSIQUE

**Mockup 2 : Lifestyle**
- Produit en situation d'utilisation
- Environnement réaliste
- Modèle humain (optionnel)

**Mockup 3 : Studio**
- Fond blanc/gris infini
- Éclairage studio pro
- Ombres douces

**Mockup 4 : Flatlay**
- Vue de dessus
- Arrangement esthétique
- Props complémentaires

**Mockup 5 : Packaging**
- Boîte + produit
- Unboxing experience
- Détails de finition
{{/if}}

{{#if product_type.includes('Livre')}}
### MOCKUPS LIVRE/EBOOK

**Mockup 2 : 3D Cover**
- Livre debout en 3D
- Ombre portée réaliste
- Fond simple

**Mockup 3 : Opened book**
- Livre ouvert montrant l'intérieur
- Pages visibles
- Mise en contexte

**Mockup 4 : Stack**
- Pile de livres
- Différents angles
- Variation de couleurs

**Mockup 5 : E-reader**
- Sur Kindle/iPad
- Version digitale mise en avant
- Multi-formats
{{/if}}

---

## 🛠️ OUTILS & RESSOURCES

**Générateurs de mockups :**
| Outil | Type | Prix |
|-------|------|------|
| Smartmockups | Web | Freemium |
| Placeit | Web | Payant |
| Mockup World | Templates | Gratuit |
| Figma plugins | Design | Freemium |
| Midjourney | IA | Payant |

**Sites de mockups gratuits :**
- [Mockup World](https://mockupworld.co)
- [Graphic Burger](https://graphicburger.com)
- [Pixeden](https://pixeden.com)
- [FreePik](https://freepik.com)

---

## ✅ CHECKLIST MOCKUP PARFAIT

- [ ] Haute résolution (min 300 DPI print, 72 DPI web)
- [ ] Éclairage cohérent
- [ ] Ombres réalistes
- [ ] Produit bien visible
- [ ] Contexte approprié
- [ ] Pas de distractions
- [ ] Format adapté à l'usage`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const iconDescriptionGenerator: AITool = {
  id: 'icon-description-generator',
  slug: 'icon-description-generator',
  name: { fr: 'Générateur de Descriptions d\'Icônes', ar: 'مولد أوصاف الأيقونات', en: 'Icon Description Generator' },
  description: {
    fr: 'Créez des descriptions et briefs pour la conception d\'icônes',
    ar: 'أنشئ أوصاف وموجزات لتصميم الأيقونات',
    en: 'Create descriptions and briefs for icon design'
  },
  category: 'design',
  subcategory: 'ui_ux',
  icon: 'Shapes',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'icon_concept', type: 'text', label: 'Concept/Action à représenter', required: true },
    { name: 'icon_style', type: 'select', label: 'Style d\'icône', options: [
      'Line (trait)', 'Filled (plein)', 'Duotone', 'Flat', 'Glyph', '3D'
    ]},
    { name: 'use_context', type: 'select', label: 'Contexte d\'utilisation', options: [
      'App UI', 'Website', 'Presentation', 'Infographic', 'Logo'
    ]},
    { name: 'icon_size', type: 'select', label: 'Taille cible', options: ['16px', '24px', '32px', '48px', '64px', '128px'] }
  ],
  outputs: [{ type: 'markdown', name: 'icon_brief' }],
  promptTemplate: `Tu es un icon designer expert.

CONCEPT : {{icon_concept}}
STYLE : {{icon_style}}
CONTEXTE : {{use_context}}
TAILLE : {{icon_size}}

## 🔷 BRIEF ICÔNE

### CONCEPT : {{icon_concept}}

---

### DESCRIPTION VISUELLE

**Forme principale :**
[Description de la forme géométrique de base]

**Éléments constitutifs :**
1. [Élément 1] - [Description]
2. [Élément 2] - [Description]
3. [Élément 3] - [Description]

**Métaphore visuelle :**
[Explication de la symbolique]

---

### VARIANTES PROPOSÉES

**Variante 1 : [Nom]**
[Description de l'approche visuelle]

**Variante 2 : [Nom]**
[Description alternative]

**Variante 3 : [Nom]**
[Description créative]

---

### SPÉCIFICATIONS TECHNIQUES

| Paramètre | Valeur |
|-----------|--------|
| Style | {{icon_style}} |
| Taille de base | {{icon_size}} |
| Grille | [X] x [X] px |
| Épaisseur trait | [X] px |
| Coins | [Arrondis X px / Carrés] |
| Espace optique | [X] px |

---

### PROMPTS IA

**Pour Midjourney :**
\`\`\`
simple {{icon_style}} icon of {{icon_concept}}, minimal, flat design, single color, white background, vector style --v 6
\`\`\`

**Pour DALL-E :**
\`\`\`
A clean, simple {{icon_style}} icon representing {{icon_concept}}. Minimalist design, single flat color, suitable for UI. Professional, modern style.
\`\`\`

---

### VARIATIONS À CRÉER

| État | Description |
|------|-------------|
| Default | État normal |
| Hover | Légèrement plus épais ou coloré |
| Active | Rempli ou accentué |
| Disabled | Grisé, 50% opacité |

---

### ICÔNES SIMILAIRES (RÉFÉRENCE)

Rechercher dans :
- [Lucide Icons](https://lucide.dev)
- [Heroicons](https://heroicons.com)
- [Phosphor Icons](https://phosphoricons.com)
- [Feather Icons](https://feathericons.com)

---

### CHECKLIST ICÔNE

- [ ] Reconnaissable en {{icon_size}}
- [ ] Cohérent avec le set existant
- [ ] Fonctionne en une seule couleur
- [ ] Équilibre optique correct
- [ ] Pas trop de détails
- [ ] Métaphore claire`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const brandStyleGuideGenerator: AITool = {
  id: 'brand-style-guide-generator',
  slug: 'brand-style-guide-generator',
  name: { fr: 'Générateur de Guide de Style', ar: 'مولد دليل الهوية البصرية', en: 'Brand Style Guide Generator' },
  description: {
    fr: 'Créez un guide de style de marque complet pour assurer la cohérence visuelle',
    ar: 'أنشئ دليل هوية بصرية شامل لضمان الاتساق',
    en: 'Create a complete brand style guide to ensure visual consistency'
  },
  category: 'design',
  subcategory: 'branding',
  icon: 'BookOpen',
  credits: 20,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true },
    { name: 'brand_description', type: 'textarea', label: 'Description de la marque' },
    { name: 'primary_color', type: 'text', label: 'Couleur principale', placeholder: '#3B82F6' },
    { name: 'secondary_colors', type: 'text', label: 'Couleurs secondaires' },
    { name: 'brand_personality', type: 'textarea', label: 'Personnalité de marque (adjectifs)' },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité' }
  ],
  outputs: [{ type: 'markdown', name: 'style_guide' }],
  promptTemplate: `Tu es un brand strategist et directeur artistique.

MARQUE : {{brand_name}}
DESCRIPTION : {{brand_description}}
COULEUR PRINCIPALE : {{primary_color}}
COULEURS SECONDAIRES : {{secondary_colors}}
PERSONNALITÉ : {{brand_personality}}
SECTEUR : {{industry}}

## 📘 GUIDE DE STYLE - {{brand_name}}

---

# BRAND STYLE GUIDE
## {{brand_name}}

**Version :** 1.0
**Date :** [Date]

---

## 1. INTRODUCTION

### 1.1 À propos de ce guide
Ce guide définit les standards visuels de {{brand_name}} pour assurer une cohérence sur tous les supports de communication.

### 1.2 Notre marque
{{brand_description}}

### 1.3 Personnalité de marque
{{brand_personality}}

**Mots-clés :**
- [Adjectif 1]
- [Adjectif 2]
- [Adjectif 3]

---

## 2. LOGO

### 2.1 Logo principal
[Description du logo principal]

### 2.2 Versions du logo

| Version | Usage |
|---------|-------|
| Logo couleur | Usage principal |
| Logo monochrome | Fond coloré |
| Logo blanc | Fond sombre |
| Logo noir | Impression N&B |
| Icône/Favicon | Petits formats |

### 2.3 Zones de protection
[Espace minimum autour du logo = X fois la hauteur du symbole]

### 2.4 Tailles minimales
- Print : [X] mm
- Digital : [X] px

### 2.5 Usages interdits ❌
- Ne pas déformer
- Ne pas changer les couleurs
- Ne pas ajouter d'effets
- Ne pas utiliser sur fond chargé

---

## 3. COULEURS

### 3.1 Palette principale

| Nom | Hex | RGB | CMYK | Pantone |
|-----|-----|-----|------|---------|
| **Primary** | {{primary_color}} | rgb(X,X,X) | C:X M:X Y:X K:X | [Pantone] |
| **Secondary** | #[HEX] | rgb(X,X,X) | C:X M:X Y:X K:X | [Pantone] |

### 3.2 Palette secondaire/accent
{{secondary_colors}}

### 3.3 Couleurs neutres

| Nom | Hex | Usage |
|-----|-----|-------|
| Noir | #1A1A1A | Texte principal |
| Gris foncé | #4A4A4A | Texte secondaire |
| Gris clair | #E5E5E5 | Bordures, séparateurs |
| Blanc | #FFFFFF | Fonds |

### 3.4 Ratios d'utilisation
\`\`\`
████████████████████████ 60% Neutres
████████████ 30% Couleur principale
████ 10% Accent
\`\`\`

### 3.5 Accessibilité
[Contraste minimum WCAG AA : 4.5:1]

---

## 4. TYPOGRAPHIE

### 4.1 Police principale

**[Nom de la police]**
- Usage : Titres, headlines
- Téléchargement : [Lien Google Fonts / Adobe Fonts]

### 4.2 Police secondaire

**[Nom de la police]**
- Usage : Corps de texte, paragraphes

### 4.3 Hiérarchie typographique

| Élément | Police | Taille | Poids | Interligne |
|---------|--------|--------|-------|------------|
| H1 | [Police] | 48px | Bold | 1.2 |
| H2 | [Police] | 36px | Bold | 1.3 |
| H3 | [Police] | 24px | SemiBold | 1.4 |
| Body | [Police] | 16px | Regular | 1.6 |
| Caption | [Police] | 14px | Regular | 1.5 |

### 4.4 Polices de substitution
- Web : [Arial / Helvetica]
- Email : [Arial / Verdana]

---

## 5. ICONOGRAPHIE

### 5.1 Style d'icônes
- Type : [Line / Filled / Duotone]
- Épaisseur : [X] px
- Coins : [Arrondis / Carrés]

### 5.2 Librairie recommandée
[Lucide / Heroicons / Custom]

---

## 6. IMAGERIE

### 6.1 Style photographique
- Éclairage : [Naturel / Studio]
- Ton : [Chaleureux / Froid]
- Sujets : [Description]

### 6.2 Filtres/Traitements
- [Description des retouches standard]

### 6.3 Illustrations
- Style : [Flat / Isométrique / Dessiné]
- Palette : [Couleurs de marque]

---

## 7. ÉLÉMENTS GRAPHIQUES

### 7.1 Formes
[Formes géométriques associées à la marque]

### 7.2 Patterns
[Motifs récurrents]

### 7.3 Dégradés
[Si applicable - couleurs et angles]

---

## 8. VOIX & TON

### 8.1 Personnalité éditoriale
- [Caractéristique 1]
- [Caractéristique 2]
- [Caractéristique 3]

### 8.2 Ce qu'on dit / Ce qu'on ne dit pas

| ✅ On dit | ❌ On ne dit pas |
|-----------|------------------|
| [Exemple] | [Exemple] |
| [Exemple] | [Exemple] |

---

## 9. APPLICATIONS

### 9.1 Cartes de visite
[Spécifications]

### 9.2 Papier à en-tête
[Spécifications]

### 9.3 Signature email
[Template]

### 9.4 Social Media
[Templates et formats]

---

## 10. RESSOURCES

### 10.1 Téléchargements
- Logo pack : [Lien]
- Polices : [Lien]
- Templates : [Lien]

### 10.2 Contacts
Brand Manager : [Email]`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const imageCaptionGenerator: AITool = {
  id: 'image-caption-generator',
  slug: 'image-caption-generator',
  name: { fr: 'Générateur de Légendes d\'Images', ar: 'مولد تعليقات الصور', en: 'Image Caption Generator' },
  description: {
    fr: 'Créez des légendes engageantes pour vos images sur différentes plateformes',
    ar: 'أنشئ تعليقات جذابة لصورك على مختلف المنصات',
    en: 'Create engaging captions for your images across different platforms'
  },
  category: 'design',
  subcategory: 'social',
  icon: 'MessageSquare',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'image_description', type: 'textarea', label: 'Décrivez l\'image', required: true },
    { name: 'platform', type: 'select', label: 'Plateforme', options: [
      'Instagram', 'LinkedIn', 'Twitter/X', 'Facebook', 'Pinterest'
    ]},
    { name: 'tone', type: 'select', label: 'Ton', options: [
      'Professional', 'Casual', 'Funny', 'Inspirational', 'Educational', 'Promotional'
    ]},
    { name: 'include_cta', type: 'boolean', label: 'Inclure un call-to-action' },
    { name: 'include_hashtags', type: 'boolean', label: 'Inclure des hashtags' }
  ],
  outputs: [{ type: 'markdown', name: 'captions' }],
  promptTemplate: `Tu es un community manager expert en engagement.

IMAGE : {{image_description}}
PLATEFORME : {{platform}}
TON : {{tone}}
CTA : {{include_cta}}
HASHTAGS : {{include_hashtags}}

## 📝 LÉGENDES D'IMAGE

### PLATEFORME : {{platform | uppercase}}

---

### LÉGENDE 1 : Hook + Storytelling

"[Accroche qui arrête le scroll]

[Paragraphe de storytelling ou contexte]

[Message clé ou insight]

{{#if include_cta}}
👉 [Call-to-action clair]
{{/if}}

{{#if include_hashtags}}
.
.
.
#[hashtag1] #[hashtag2] #[hashtag3] #[hashtag4] #[hashtag5]
{{/if}}"

---

### LÉGENDE 2 : Question + Engagement

"[Question intrigante liée à l'image] 🤔

[Contexte court]

[Votre perspective]

{{#if include_cta}}
💬 [Invitation à commenter]
{{/if}}

{{#if include_hashtags}}
#[hashtags pertinents]
{{/if}}"

---

### LÉGENDE 3 : Directe et impactante

"[Statement fort et direct] ✨

{{#if include_cta}}
[CTA simple]
{{/if}}

{{#if include_hashtags}}
#[hashtags]
{{/if}}"

---

### LÉGENDE 4 : Éducative/Valeur

"💡 [Tip ou fait intéressant]

Voici ce que vous devez savoir :

→ [Point 1]
→ [Point 2]
→ [Point 3]

{{#if include_cta}}
📌 [CTA : Sauvegardez/Partagez]
{{/if}}

{{#if include_hashtags}}
#[hashtags]
{{/if}}"

---

### LÉGENDE 5 : Émotionnelle

"[Expression émotionnelle] 💭

[Réflexion personnelle ou moment capturé]

[Message inspirant]

{{#if include_hashtags}}
#[hashtags inspirants]
{{/if}}"

---

## 📊 SPECS PAR PLATEFORME

{{#if platform === 'Instagram'}}
| Paramètre | Recommandation |
|-----------|----------------|
| Longueur | 150-300 caractères (optimal) |
| Max | 2,200 caractères |
| Hashtags | 5-15 (en commentaire ou fin) |
| Emojis | Oui, modérément |
| Line breaks | Utiliser le "." pour l'espacement |
{{/if}}

{{#if platform === 'LinkedIn'}}
| Paramètre | Recommandation |
|-----------|----------------|
| Longueur | 150-300 mots |
| Hook | 2-3 premières lignes cruciales |
| Hashtags | 3-5 pertinents |
| Ton | Professionnel mais humain |
| CTA | Question ou invitation à discuter |
{{/if}}

{{#if platform === 'Twitter/X'}}
| Paramètre | Recommandation |
|-----------|----------------|
| Max | 280 caractères |
| Optimal | 100-150 caractères |
| Hashtags | 1-2 maximum |
| Style | Concis, percutant |
{{/if}}

---

## 🏷️ HASHTAGS SUGGÉRÉS

**Hashtags populaires :**
#[hashtag1] #[hashtag2] #[hashtag3]

**Hashtags de niche :**
#[hashtag4] #[hashtag5] #[hashtag6]

**Hashtags de marque :**
#[votrehashtag]

---

## ✅ CHECKLIST LÉGENDE

- [ ] Hook dans les premières lignes
- [ ] Ton cohérent avec la marque
- [ ] Valeur ajoutée pour le lecteur
- [ ] CTA clair (si applicable)
- [ ] Hashtags pertinents (pas de spam)
- [ ] Pas de fautes d'orthographe
- [ ] Emojis appropriés`,
  model: 'gpt4',
  estimatedTime: '30s'
};
