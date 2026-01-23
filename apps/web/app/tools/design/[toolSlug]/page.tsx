'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Palette, Sparkles } from 'lucide-react';
import { getToolBySlug } from '@/lib/tools-data';

// Types
interface FormField {
  name: string;
  label: string;
  type: 'text' | 'textarea' | 'select' | 'number' | 'checkbox' | 'tags' | 'multiselect';
  placeholder?: string;
  options?: { value: string; label: string }[];
  required?: boolean;
  rows?: number;
}

interface ToolConfig {
  fields: FormField[];
  promptTemplate: string;
}

// ========================================
// CONFIGURATIONS DES 15 OUTILS DESIGN
// ========================================
const toolConfigs: Record<string, ToolConfig> = {
  // ===== BATCH 1 - CRITIQUE (8) =====

  'midjourney-prompt-generator': {
    fields: [
      { name: 'subject', label: 'Sujet principal', type: 'text', placeholder: 'Ex: Un dragon majestueux sur une montagne', required: true },
      { name: 'style', label: 'Style artistique', type: 'select', options: [
        { value: 'photorealistic', label: 'Photorealiste' },
        { value: 'digital_art', label: 'Art digital' },
        { value: 'oil_painting', label: 'Peinture a l\'huile' },
        { value: 'watercolor', label: 'Aquarelle' },
        { value: 'anime', label: 'Anime/Manga' },
        { value: '3d_render', label: 'Rendu 3D' },
        { value: 'concept_art', label: 'Concept art' },
        { value: 'vintage', label: 'Vintage/Retro' },
        { value: 'minimalist', label: 'Minimaliste' },
        { value: 'surrealist', label: 'Surrealiste' },
      ], required: true },
      { name: 'mood', label: 'Ambiance', type: 'select', options: [
        { value: 'epic', label: 'Epique' },
        { value: 'peaceful', label: 'Paisible' },
        { value: 'dark', label: 'Sombre' },
        { value: 'bright', label: 'Lumineux' },
        { value: 'mysterious', label: 'Mysterieux' },
        { value: 'romantic', label: 'Romantique' },
        { value: 'dramatic', label: 'Dramatique' },
        { value: 'whimsical', label: 'Fantasque' },
      ] },
      { name: 'lighting', label: 'Eclairage', type: 'select', options: [
        { value: 'golden_hour', label: 'Golden hour' },
        { value: 'dramatic', label: 'Dramatique' },
        { value: 'soft', label: 'Doux/Diffus' },
        { value: 'neon', label: 'Neon' },
        { value: 'studio', label: 'Studio' },
        { value: 'natural', label: 'Naturel' },
        { value: 'cinematic', label: 'Cinematique' },
      ] },
      { name: 'aspectRatio', label: 'Format', type: 'select', options: [
        { value: '1:1', label: 'Carre (1:1)' },
        { value: '16:9', label: 'Paysage (16:9)' },
        { value: '9:16', label: 'Portrait (9:16)' },
        { value: '4:3', label: 'Standard (4:3)' },
        { value: '3:2', label: 'Photo (3:2)' },
      ] },
      { name: 'additionalDetails', label: 'Details supplementaires', type: 'textarea', placeholder: 'Couleurs, textures, elements specifiques...', rows: 3 },
      { name: 'negativePrompt', label: 'Elements a eviter', type: 'text', placeholder: 'Ex: flou, basse qualite, texte' },
    ],
    promptTemplate: `Tu es un expert en generation de prompts Midjourney. Cree un prompt optimise et detaille.

**SUJET:** {{subject}}
**STYLE:** {{style}}
{{#if mood}}**AMBIANCE:** {{mood}}{{/if}}
{{#if lighting}}**ECLAIRAGE:** {{lighting}}{{/if}}
{{#if aspectRatio}}**FORMAT:** {{aspectRatio}}{{/if}}
{{#if additionalDetails}}**DETAILS:** {{additionalDetails}}{{/if}}
{{#if negativePrompt}}**A EVITER:** {{negativePrompt}}{{/if}}

---

Genere:

## PROMPT MIDJOURNEY PRINCIPAL
Un prompt complet en anglais, optimise pour Midjourney v6, incluant:
- Description detaillee du sujet
- Style artistique avec references d'artistes si pertinent
- Qualificateurs de qualite (8k, highly detailed, masterpiece, etc.)
- Parametres recommandes (--ar, --style, --chaos, --stylize)

## VARIATIONS
3 variations du prompt avec des approches differentes:
1. Version plus minimaliste
2. Version plus detaillee
3. Version avec style artistique alternatif

## PARAMETRES RECOMMANDES
- --ar (aspect ratio)
- --style (raw, cute, scenic, etc.)
- --stylize (0-1000)
- --chaos (0-100)
- --quality

## CONSEILS D'OPTIMISATION
- Mots-cles les plus impactants
- Ordre optimal des elements
- Erreurs courantes a eviter`
  },

  'dalle-prompt-generator': {
    fields: [
      { name: 'subject', label: 'Sujet principal', type: 'text', placeholder: 'Ex: Un chat astronaute sur la lune', required: true },
      { name: 'style', label: 'Style visuel', type: 'select', options: [
        { value: 'photorealistic', label: 'Photorealiste' },
        { value: 'digital_art', label: 'Art digital' },
        { value: 'illustration', label: 'Illustration' },
        { value: 'cartoon', label: 'Cartoon' },
        { value: 'oil_painting', label: 'Peinture a l\'huile' },
        { value: 'watercolor', label: 'Aquarelle' },
        { value: 'pencil_sketch', label: 'Croquis crayon' },
        { value: 'pixel_art', label: 'Pixel art' },
        { value: '3d_render', label: 'Rendu 3D' },
        { value: 'vintage_poster', label: 'Affiche vintage' },
      ], required: true },
      { name: 'mood', label: 'Ton/Ambiance', type: 'select', options: [
        { value: 'playful', label: 'Ludique' },
        { value: 'serious', label: 'Serieux' },
        { value: 'dreamy', label: 'Onirique' },
        { value: 'energetic', label: 'Energique' },
        { value: 'calm', label: 'Calme' },
        { value: 'mysterious', label: 'Mysterieux' },
        { value: 'nostalgic', label: 'Nostalgique' },
      ] },
      { name: 'colorPalette', label: 'Palette de couleurs', type: 'text', placeholder: 'Ex: bleu pastel, rose, blanc' },
      { name: 'additionalElements', label: 'Elements additionnels', type: 'textarea', placeholder: 'Arriere-plan, objets, personnages...', rows: 3 },
      { name: 'size', label: 'Taille', type: 'select', options: [
        { value: '1024x1024', label: 'Carre (1024x1024)' },
        { value: '1792x1024', label: 'Paysage (1792x1024)' },
        { value: '1024x1792', label: 'Portrait (1024x1792)' },
      ] },
    ],
    promptTemplate: `Tu es un expert en prompts DALL-E 3. Cree des prompts optimises pour OpenAI.

**SUJET:** {{subject}}
**STYLE:** {{style}}
{{#if mood}}**AMBIANCE:** {{mood}}{{/if}}
{{#if colorPalette}}**COULEURS:** {{colorPalette}}{{/if}}
{{#if additionalElements}}**ELEMENTS:** {{additionalElements}}{{/if}}
{{#if size}}**TAILLE:** {{size}}{{/if}}

---

Genere:

## PROMPT DALL-E 3 PRINCIPAL
Un prompt descriptif en anglais, clair et structure:
- Description naturelle et fluide (DALL-E prefere les phrases completes)
- Style artistique explicite
- Details sur la composition et l'eclairage
- Eviter les termes techniques complexes

## PROMPT ALTERNATIF (PLUS SIMPLE)
Version condensee gardant l'essentiel

## PROMPT ALTERNATIF (PLUS DETAILLE)
Version enrichie avec plus de details visuels

## CONSEILS DALL-E 3
- DALL-E comprend mieux les descriptions naturelles que les listes de mots-cles
- Specifier clairement le style au debut du prompt
- Eviter les references a des personnes reelles
- Les emotions et ambiances sont bien interpretes

## EXEMPLE D'UTILISATION API
\`\`\`python
response = client.images.generate(
  model="dall-e-3",
  prompt="[VOTRE PROMPT ICI]",
  size="{{size}}",
  quality="hd",
  n=1
)
\`\`\``
  },

  'stable-diffusion-prompt-generator': {
    fields: [
      { name: 'subject', label: 'Sujet principal', type: 'text', placeholder: 'Ex: Portrait d\'une femme cyberpunk', required: true },
      { name: 'checkpoint', label: 'Modele/Checkpoint', type: 'select', options: [
        { value: 'sd_xl', label: 'Stable Diffusion XL' },
        { value: 'sd_15', label: 'Stable Diffusion 1.5' },
        { value: 'realistic_vision', label: 'Realistic Vision' },
        { value: 'dreamshaper', label: 'DreamShaper' },
        { value: 'deliberate', label: 'Deliberate' },
        { value: 'anime', label: 'Anime (specialise)' },
      ], required: true },
      { name: 'style', label: 'Style artistique', type: 'text', placeholder: 'Ex: hyperrealistic, cinematic, anime' },
      { name: 'qualityTags', label: 'Tags de qualite', type: 'multiselect', options: [
        { value: 'masterpiece', label: 'masterpiece' },
        { value: 'best_quality', label: 'best quality' },
        { value: 'highly_detailed', label: 'highly detailed' },
        { value: '8k', label: '8k resolution' },
        { value: 'professional', label: 'professional' },
        { value: 'sharp_focus', label: 'sharp focus' },
      ] },
      { name: 'lighting', label: 'Eclairage', type: 'text', placeholder: 'Ex: volumetric lighting, rim light, studio lighting' },
      { name: 'camera', label: 'Parametres camera', type: 'text', placeholder: 'Ex: 85mm lens, f/1.4, bokeh, depth of field' },
      { name: 'negativePrompt', label: 'Negative prompt', type: 'textarea', placeholder: 'Elements a eviter...', rows: 3 },
    ],
    promptTemplate: `Tu es un expert Stable Diffusion avec une maitrise des prompts techniques. Genere un prompt optimise.

**SUJET:** {{subject}}
**MODELE:** {{checkpoint}}
{{#if style}}**STYLE:** {{style}}{{/if}}
{{#if qualityTags}}**QUALITE:** {{qualityTags}}{{/if}}
{{#if lighting}}**ECLAIRAGE:** {{lighting}}{{/if}}
{{#if camera}}**CAMERA:** {{camera}}{{/if}}
{{#if negativePrompt}}**NEGATIVE:** {{negativePrompt}}{{/if}}

---

Genere:

## POSITIVE PROMPT
Un prompt structure avec:
- Tags de qualite en premier (masterpiece, best quality, etc.)
- Description du sujet
- Style artistique
- Eclairage et atmosphere
- Details techniques (camera, resolution)

## NEGATIVE PROMPT
Un negative prompt complet pour eviter les artefacts courants:
- Problemes anatomiques
- Qualite basse
- Artefacts visuels
- Elements non desires

## PARAMETRES RECOMMANDES
\`\`\`
Steps: 25-35
CFG Scale: 7-9
Sampler: DPM++ 2M Karras ou Euler a
Size: 768x1024 (portrait) / 1024x768 (paysage)
{{#if checkpoint}}Checkpoint: {{checkpoint}}{{/if}}
\`\`\`

## LORAS SUGGERES
Recommandations de LoRAs complementaires pour ce style

## VARIATIONS
3 variations du prompt avec des emphases differentes

## WORKFLOW COMFYUI (OPTIONNEL)
Structure de nodes recommandee pour ce type d'image`
  },

  'image-alt-text-generator': {
    fields: [
      { name: 'imageDescription', label: 'Description de l\'image', type: 'textarea', placeholder: 'Decrivez l\'image en detail: sujet, couleurs, contexte...', required: true, rows: 4 },
      { name: 'pageContext', label: 'Contexte de la page', type: 'text', placeholder: 'Ex: Page produit e-commerce, article de blog voyage' },
      { name: 'targetKeyword', label: 'Mot-cle cible (SEO)', type: 'text', placeholder: 'Ex: chaussures running homme' },
      { name: 'imageType', label: 'Type d\'image', type: 'select', options: [
        { value: 'product', label: 'Photo produit' },
        { value: 'infographic', label: 'Infographie' },
        { value: 'illustration', label: 'Illustration' },
        { value: 'photo', label: 'Photographie' },
        { value: 'screenshot', label: 'Capture d\'ecran' },
        { value: 'logo', label: 'Logo' },
        { value: 'banner', label: 'Banniere' },
        { value: 'graph', label: 'Graphique/Diagramme' },
      ] },
      { name: 'brand', label: 'Marque (optionnel)', type: 'text', placeholder: 'Nom de la marque si pertinent' },
    ],
    promptTemplate: `Tu es un expert SEO specialise dans l'optimisation des images. Genere des textes alternatifs optimises.

**DESCRIPTION IMAGE:** {{imageDescription}}
{{#if pageContext}}**CONTEXTE PAGE:** {{pageContext}}{{/if}}
{{#if targetKeyword}}**MOT-CLE CIBLE:** {{targetKeyword}}{{/if}}
{{#if imageType}}**TYPE:** {{imageType}}{{/if}}
{{#if brand}}**MARQUE:** {{brand}}{{/if}}

---

Genere:

## TEXTE ALT PRINCIPAL (Recommande)
Un texte alt de 100-125 caracteres max:
- Descriptif et naturel
- Inclut le mot-cle cible naturellement
- Accessible pour les lecteurs d'ecran
- SEO-friendly

## VERSION COURTE (< 60 caracteres)
Pour les contextes ou la brievete est requise

## VERSION LONGUE (Title attribute)
Description plus detaillee pour l'attribut title

## ANALYSE SEO
- Densite du mot-cle
- Pertinence contextuelle
- Accessibilite
- Score d'optimisation

## BONNES PRATIQUES RAPPELEES
- Ne pas commencer par "Image de..."
- Eviter le keyword stuffing
- Decrire le contenu, pas la fonction
- Inclure les infos textuelles presentes dans l'image

## EXEMPLES D'IMPLEMENTATION
\`\`\`html
<img src="image.jpg" alt="[TEXTE ALT]" title="[VERSION LONGUE]">
\`\`\`

## AUTRES IMAGES SUGGERES
Si pertinent, suggestions pour les images complementaires de la page`
  },

  'social-media-image-ideas': {
    fields: [
      { name: 'brand', label: 'Marque/Business', type: 'text', placeholder: 'Nom de votre marque', required: true },
      { name: 'industry', label: 'Secteur', type: 'select', options: [
        { value: 'tech', label: 'Tech/Startup' },
        { value: 'fashion', label: 'Mode/Beaute' },
        { value: 'food', label: 'Food/Restaurant' },
        { value: 'fitness', label: 'Fitness/Bien-etre' },
        { value: 'travel', label: 'Voyage/Tourisme' },
        { value: 'education', label: 'Education' },
        { value: 'finance', label: 'Finance/Business' },
        { value: 'art', label: 'Art/Creative' },
        { value: 'ecommerce', label: 'E-commerce' },
        { value: 'other', label: 'Autre' },
      ], required: true },
      { name: 'platform', label: 'Plateforme', type: 'select', options: [
        { value: 'instagram', label: 'Instagram' },
        { value: 'facebook', label: 'Facebook' },
        { value: 'linkedin', label: 'LinkedIn' },
        { value: 'twitter', label: 'Twitter/X' },
        { value: 'pinterest', label: 'Pinterest' },
        { value: 'tiktok', label: 'TikTok' },
        { value: 'all', label: 'Multi-plateforme' },
      ], required: true },
      { name: 'contentTheme', label: 'Theme du contenu', type: 'text', placeholder: 'Ex: Lancement produit, Behind the scenes, Tips...' },
      { name: 'brandColors', label: 'Couleurs de marque', type: 'text', placeholder: 'Ex: Bleu #0066CC, Orange #FF6600' },
      { name: 'quantity', label: 'Nombre d\'idees', type: 'select', options: [
        { value: '5', label: '5 idees' },
        { value: '10', label: '10 idees' },
        { value: '15', label: '15 idees' },
        { value: '30', label: '30 idees (calendrier mensuel)' },
      ] },
    ],
    promptTemplate: `Tu es un directeur artistique social media expert. Genere des idees d'images creatives.

**MARQUE:** {{brand}}
**SECTEUR:** {{industry}}
**PLATEFORME:** {{platform}}
{{#if contentTheme}}**THEME:** {{contentTheme}}{{/if}}
{{#if brandColors}}**COULEURS:** {{brandColors}}{{/if}}
**QUANTITE:** {{quantity}} idees

---

Genere {{quantity}} idees d'images avec pour chacune:

## IDEES D'IMAGES VISUELLES

Pour chaque idee, fournis:

### Idee #X: [TITRE ACCROCHEUR]
- **Concept:** Description visuelle detaillee
- **Composition:** Disposition des elements
- **Style:** Photographique/Illustre/Graphique
- **Couleurs:** Palette recommandee
- **Texte overlay:** Si applicable
- **CTA:** Appel a l'action suggere
- **Format:** {{platform}} optimal (carre, portrait, story, etc.)
- **Prompt IA:** Prompt pour generer cette image avec Midjourney/DALL-E

---

## CALENDRIER DE PUBLICATION
Suggestion d'organisation sur la semaine/mois

## CONSEILS DE STYLE
- Coherence visuelle
- Best practices {{platform}}
- Tendances actuelles

## OUTILS RECOMMANDES
- Apps de creation (Canva, Figma, etc.)
- Banques d'images
- Filtres et presets`
  },

  'logo-concept-generator': {
    fields: [
      { name: 'brandName', label: 'Nom de la marque', type: 'text', placeholder: 'Nom de votre entreprise/marque', required: true },
      { name: 'industry', label: 'Secteur d\'activite', type: 'text', placeholder: 'Ex: Tech, Mode, Restauration, Finance...', required: true },
      { name: 'brandValues', label: 'Valeurs de la marque', type: 'textarea', placeholder: 'Ex: Innovation, Confiance, Durabilite, Elegance...', rows: 2 },
      { name: 'targetAudience', label: 'Public cible', type: 'text', placeholder: 'Ex: Jeunes professionnels 25-35 ans' },
      { name: 'competitors', label: 'Concurrents (logos a eviter)', type: 'text', placeholder: 'Marques dont vous voulez vous differencier' },
      { name: 'preferences', label: 'Preferences de style', type: 'multiselect', options: [
        { value: 'minimalist', label: 'Minimaliste' },
        { value: 'modern', label: 'Moderne' },
        { value: 'classic', label: 'Classique' },
        { value: 'playful', label: 'Ludique' },
        { value: 'luxury', label: 'Luxe' },
        { value: 'geometric', label: 'Geometrique' },
        { value: 'organic', label: 'Organique' },
        { value: 'bold', label: 'Bold/Impactant' },
      ] },
      { name: 'colorPreferences', label: 'Preferences de couleurs', type: 'text', placeholder: 'Couleurs souhaitees ou a eviter' },
    ],
    promptTemplate: `Tu es un directeur artistique senior specialise en branding. Cree des concepts de logo.

**MARQUE:** {{brandName}}
**SECTEUR:** {{industry}}
{{#if brandValues}}**VALEURS:** {{brandValues}}{{/if}}
{{#if targetAudience}}**CIBLE:** {{targetAudience}}{{/if}}
{{#if competitors}}**DIFFERENCIATION:** {{competitors}}{{/if}}
{{#if preferences}}**STYLE:** {{preferences}}{{/if}}
{{#if colorPreferences}}**COULEURS:** {{colorPreferences}}{{/if}}

---

Genere un brief creatif complet:

## ANALYSE STRATEGIQUE
- Positionnement de la marque
- Message a communiquer
- Emotions a evoquer
- Differenciation concurrentielle

## CONCEPTS DE LOGO (5 directions)

### Concept 1: [NOM DU CONCEPT]
- **Type:** Wordmark / Lettermark / Symbole / Combinaison
- **Description visuelle:** Detail du design
- **Symbolisme:** Signification des elements
- **Typographie:** Police suggere
- **Couleurs:** Palette avec codes hex
- **Prompt Midjourney:** Pour generer une inspiration visuelle

### Concept 2-5: [Meme structure]

## GUIDE DE COULEURS
Pour chaque concept:
- Couleur primaire + code hex
- Couleur secondaire + code hex
- Couleurs d'accent

## TYPOGRAPHIES RECOMMANDEES
- Polices principales (Google Fonts gratuites)
- Polices premium alternatives
- Hierarchie typographique

## VARIATIONS A PREVOIR
- Logo principal
- Version horizontale
- Version verticale
- Favicon/App icon
- Version monochrome
- Version sur fond sombre

## BRIEF POUR DESIGNER
Resume pret a envoyer a un graphiste professionnel`
  },

  'color-palette-generator': {
    fields: [
      { name: 'brandName', label: 'Nom de la marque', type: 'text', placeholder: 'Votre marque', required: true },
      { name: 'industry', label: 'Secteur', type: 'text', placeholder: 'Ex: Tech, Mode, Sante...', required: true },
      { name: 'mood', label: 'Ambiance souhaitee', type: 'multiselect', options: [
        { value: 'professional', label: 'Professionnel' },
        { value: 'playful', label: 'Ludique' },
        { value: 'luxurious', label: 'Luxueux' },
        { value: 'natural', label: 'Naturel' },
        { value: 'energetic', label: 'Energique' },
        { value: 'calm', label: 'Calme' },
        { value: 'modern', label: 'Moderne' },
        { value: 'traditional', label: 'Traditionnel' },
      ], required: true },
      { name: 'baseColor', label: 'Couleur de base (optionnel)', type: 'text', placeholder: 'Ex: #0066CC ou "bleu"' },
      { name: 'avoidColors', label: 'Couleurs a eviter', type: 'text', placeholder: 'Couleurs de concurrents ou non souhaitees' },
      { name: 'useCase', label: 'Usage principal', type: 'select', options: [
        { value: 'web', label: 'Site web/App' },
        { value: 'print', label: 'Print/Impression' },
        { value: 'both', label: 'Web + Print' },
        { value: 'social', label: 'Reseaux sociaux' },
      ] },
    ],
    promptTemplate: `Tu es un expert en theorie des couleurs et branding. Cree une palette de couleurs harmonieuse.

**MARQUE:** {{brandName}}
**SECTEUR:** {{industry}}
**AMBIANCE:** {{mood}}
{{#if baseColor}}**BASE:** {{baseColor}}{{/if}}
{{#if avoidColors}}**A EVITER:** {{avoidColors}}{{/if}}
{{#if useCase}}**USAGE:** {{useCase}}{{/if}}

---

Genere une palette complete:

## PALETTE PRINCIPALE

### Couleur Primaire
- Nom: [Nom evocateur]
- HEX: #XXXXXX
- RGB: rgb(X, X, X)
- HSL: hsl(X, X%, X%)
- Signification: Pourquoi cette couleur

### Couleur Secondaire
[Meme format]

### Couleur d'Accent
[Meme format]

### Couleurs Neutres (3-4)
- Blanc/Clair
- Gris moyen
- Gris fonce
- Noir/Sombre

## PALETTE ETENDUE
- 5-7 teintes additionnelles pour les variations

## HARMONIES COULEUR
- Visualisation des combinaisons
- Contrastes recommandes
- Ratios d'accessibilite (WCAG)

## UTILISATION RECOMMANDEE
| Element | Couleur | Ratio |
|---------|---------|-------|
| Arriere-plan principal | ... | 60% |
| Elements secondaires | ... | 30% |
| CTA / Accents | ... | 10% |

## VARIANTES MODE SOMBRE
Adaptation de la palette pour le dark mode

## PSYCHOLOGIE DES COULEURS
Justification des choix selon:
- Emotions evoquees
- Associations culturelles
- Impact sur la conversion

## EXPORT
- Variables CSS
- Variables Tailwind
- Palette Figma/Sketch

\`\`\`css
:root {
  --color-primary: #XXXXXX;
  --color-secondary: #XXXXXX;
  --color-accent: #XXXXXX;
}
\`\`\``
  },

  'ui-component-ideas': {
    fields: [
      { name: 'componentType', label: 'Type de composant', type: 'select', options: [
        { value: 'button', label: 'Boutons' },
        { value: 'form', label: 'Formulaires' },
        { value: 'card', label: 'Cards' },
        { value: 'navigation', label: 'Navigation' },
        { value: 'modal', label: 'Modales/Popups' },
        { value: 'table', label: 'Tables/Listes' },
        { value: 'dashboard', label: 'Dashboard widgets' },
        { value: 'hero', label: 'Hero sections' },
        { value: 'footer', label: 'Footer' },
        { value: 'pricing', label: 'Pricing tables' },
      ], required: true },
      { name: 'platform', label: 'Plateforme', type: 'select', options: [
        { value: 'web', label: 'Web (Desktop)' },
        { value: 'mobile', label: 'Mobile app' },
        { value: 'responsive', label: 'Responsive (tous)' },
        { value: 'desktop_app', label: 'Desktop app' },
      ], required: true },
      { name: 'style', label: 'Style UI', type: 'select', options: [
        { value: 'minimal', label: 'Minimaliste' },
        { value: 'glassmorphism', label: 'Glassmorphism' },
        { value: 'neumorphism', label: 'Neumorphism' },
        { value: 'material', label: 'Material Design' },
        { value: 'flat', label: 'Flat design' },
        { value: 'brutalist', label: 'Brutalist' },
        { value: 'skeuomorphic', label: 'Skeuomorphic' },
      ] },
      { name: 'functionality', label: 'Fonctionnalite principale', type: 'text', placeholder: 'Ex: Checkout, User profile, Analytics...' },
      { name: 'framework', label: 'Framework/Tech', type: 'select', options: [
        { value: 'react', label: 'React' },
        { value: 'vue', label: 'Vue.js' },
        { value: 'tailwind', label: 'Tailwind CSS' },
        { value: 'css', label: 'CSS pur' },
        { value: 'flutter', label: 'Flutter' },
        { value: 'swift', label: 'SwiftUI' },
      ] },
      { name: 'accessibilityLevel', label: 'Niveau d\'accessibilite', type: 'select', options: [
        { value: 'aa', label: 'WCAG AA' },
        { value: 'aaa', label: 'WCAG AAA' },
        { value: 'basic', label: 'Basique' },
      ] },
    ],
    promptTemplate: `Tu es un UI/UX designer senior. Genere des idees et specs pour des composants d'interface.

**TYPE:** {{componentType}}
**PLATEFORME:** {{platform}}
{{#if style}}**STYLE:** {{style}}{{/if}}
{{#if functionality}}**FONCTION:** {{functionality}}{{/if}}
{{#if framework}}**TECH:** {{framework}}{{/if}}
{{#if accessibilityLevel}}**ACCESSIBILITE:** {{accessibilityLevel}}{{/if}}

---

Genere des specs completes:

## ANALYSE DU BESOIN
- Objectif principal du composant
- Cas d'usage
- User flow concerne

## VARIANTES DU COMPOSANT (3-5)

### Variante 1: [NOM]
**Description visuelle:**
- Dimensions recommandees
- Spacing/Padding
- Border radius
- Shadows
- Couleurs

**Etats:**
- Default
- Hover
- Active/Pressed
- Focus
- Disabled
- Loading
- Error/Success

**Animation:**
- Transitions
- Micro-interactions

### Variante 2-5: [Meme structure]

## SPECIFICATIONS TECHNIQUES

### Props/Parametres
\`\`\`typescript
interface {{componentType}}Props {
  // Definir les props
}
\`\`\`

### Tokens de Design
\`\`\`css
/* Spacing */
--component-padding: Xpx;
--component-gap: Xpx;

/* Colors */
--component-bg: #XXX;
--component-text: #XXX;
\`\`\`

## CODE EXEMPLE ({{framework}})
\`\`\`jsx
// Exemple d'implementation
\`\`\`

## ACCESSIBILITE
- Attributs ARIA requis
- Navigation clavier
- Contraste minimum
- Screen reader friendly

## RESPONSIVE
- Breakpoints
- Adaptations mobile

## PROMPT MIDJOURNEY
Pour generer une inspiration visuelle du composant`
  },

  // ===== BATCH 2 - HIGH PRIORITY (7) =====

  'thumbnail-idea-generator': {
    fields: [
      { name: 'videoTitle', label: 'Titre de la video', type: 'text', placeholder: 'Le titre exact de votre video YouTube', required: true },
      { name: 'videoTopic', label: 'Sujet/Niche', type: 'select', options: [
        { value: 'tech', label: 'Tech/Gaming' },
        { value: 'tutorial', label: 'Tutoriel/How-to' },
        { value: 'vlog', label: 'Vlog/Lifestyle' },
        { value: 'business', label: 'Business/Finance' },
        { value: 'education', label: 'Education' },
        { value: 'entertainment', label: 'Entertainment' },
        { value: 'fitness', label: 'Fitness/Sante' },
        { value: 'food', label: 'Cuisine/Food' },
        { value: 'travel', label: 'Voyage' },
        { value: 'news', label: 'News/Actualite' },
      ], required: true },
      { name: 'emotion', label: 'Emotion a transmettre', type: 'select', options: [
        { value: 'excitement', label: 'Excitation/Hype' },
        { value: 'curiosity', label: 'Curiosite' },
        { value: 'shock', label: 'Choc/Surprise' },
        { value: 'trust', label: 'Confiance' },
        { value: 'urgency', label: 'Urgence' },
        { value: 'fun', label: 'Fun/Humour' },
        { value: 'inspiration', label: 'Inspiration' },
      ] },
      { name: 'style', label: 'Style visuel', type: 'select', options: [
        { value: 'face_reaction', label: 'Visage + Reaction' },
        { value: 'text_heavy', label: 'Texte fort' },
        { value: 'before_after', label: 'Avant/Apres' },
        { value: 'comparison', label: 'Comparaison' },
        { value: 'minimal', label: 'Minimaliste' },
        { value: 'collage', label: 'Collage' },
        { value: 'screenshot', label: 'Screenshot + Texte' },
      ] },
      { name: 'brandColors', label: 'Couleurs de votre chaine', type: 'text', placeholder: 'Ex: Rouge, Noir, Blanc' },
      { name: 'competitors', label: 'Chaines concurrentes (inspiration)', type: 'text', placeholder: 'Chaines dont vous aimez les miniatures' },
    ],
    promptTemplate: `Tu es un expert YouTube specialise dans les miniatures a fort taux de clic. Genere des concepts de miniatures.

**VIDEO:** {{videoTitle}}
**NICHE:** {{videoTopic}}
**EMOTION:** {{emotion}}
**STYLE:** {{style}}
{{#if brandColors}}**COULEURS:** {{brandColors}}{{/if}}
{{#if competitors}}**INSPIRATION:** {{competitors}}{{/if}}

---

Genere 5 concepts de miniatures:

## CONCEPT 1: [NOM ACCROCHEUR]

### Composition visuelle
- **Premier plan:** Element principal (visage, produit, texte)
- **Arriere-plan:** Contexte, couleur, pattern
- **Texte overlay:** 2-4 mots maximum
- **Elements graphiques:** Fleches, cercles, emojis

### Palette de couleurs
- Couleur dominante: [Choix + justification]
- Couleur de contraste: [Pour le texte/elements]
- Couleur d'accent: [Pour attirer l'oeil]

### Psychologie du clic
- Pourquoi ca fonctionne
- Emotion declenchee
- Pattern de lecture (ou l'oeil va en premier)

### Prompt Midjourney/DALL-E
\`\`\`
[Prompt optimise pour generer cette miniature]
\`\`\`

### Specifications techniques
- Taille: 1280x720px
- Police recommandee: [Nom]
- Taille du texte: X% de l'image

## CONCEPTS 2-5: [Meme structure detaillee]

---

## ANALYSE COMPARATIVE
Tableau comparant les 5 concepts:
| Concept | CTR estime | Difficulte creation | Best pour |

## CONSEILS D'OPTIMISATION
- A/B testing recommande
- Mots a fort impact
- Couleurs qui performent dans votre niche
- Erreurs courantes a eviter

## OUTILS RECOMMANDES
- Canva (templates)
- Photoshop
- TubeBuddy (A/B test)
- Thumbs Up (analyse)`
  },

  'infographic-outline-generator': {
    fields: [
      { name: 'topic', label: 'Sujet de l\'infographie', type: 'text', placeholder: 'Ex: Les etapes pour lancer une startup', required: true },
      { name: 'dataPoints', label: 'Donnees/Stats a inclure', type: 'textarea', placeholder: 'Listez les chiffres, statistiques ou faits a visualiser', rows: 4, required: true },
      { name: 'type', label: 'Type d\'infographie', type: 'select', options: [
        { value: 'process', label: 'Processus/Etapes' },
        { value: 'comparison', label: 'Comparaison' },
        { value: 'timeline', label: 'Timeline' },
        { value: 'statistical', label: 'Statistiques' },
        { value: 'geographic', label: 'Geographique/Carte' },
        { value: 'hierarchical', label: 'Hierarchique' },
        { value: 'list', label: 'Liste/Top X' },
        { value: 'how_to', label: 'How-to/Guide' },
      ], required: true },
      { name: 'audience', label: 'Public cible', type: 'text', placeholder: 'Ex: Entrepreneurs, Etudiants, Professionnels RH...' },
      { name: 'brandColors', label: 'Couleurs de marque', type: 'text', placeholder: 'Vos couleurs ou preferences' },
      { name: 'platform', label: 'Plateforme de diffusion', type: 'select', options: [
        { value: 'pinterest', label: 'Pinterest' },
        { value: 'linkedin', label: 'LinkedIn' },
        { value: 'blog', label: 'Blog/Site web' },
        { value: 'instagram', label: 'Instagram' },
        { value: 'print', label: 'Impression' },
        { value: 'presentation', label: 'Presentation' },
      ] },
    ],
    promptTemplate: `Tu es un designer d'information expert en infographies virales. Cree un plan detaille.

**SUJET:** {{topic}}
**DONNEES:** {{dataPoints}}
**TYPE:** {{type}}
{{#if audience}}**AUDIENCE:** {{audience}}{{/if}}
{{#if brandColors}}**COULEURS:** {{brandColors}}{{/if}}
{{#if platform}}**PLATEFORME:** {{platform}}{{/if}}

---

## STRUCTURE DE L'INFOGRAPHIE

### En-tete (Header)
- **Titre accrocheur:** [Proposition]
- **Sous-titre:** [Contexte/Hook]
- **Visuel header:** [Description]

### Corps - Sections principales

#### Section 1: [TITRE]
- **Donnee cle:** [Stat/Fait]
- **Visualisation:** [Type de graphique/icone]
- **Texte d'accompagnement:** [2-3 phrases]
- **Icone/Illustration:** [Description]

#### Section 2-X: [Meme structure]

### Pied (Footer)
- **Call-to-action:** [Action souhaitee]
- **Sources:** [Format]
- **Branding:** [Logo, site, social]

## SPECIFICATIONS DESIGN

### Dimensions
- Format: {{platform}} optimise
- Ratio recommande: [X:Y]
- Resolution: [px]

### Hierarchie visuelle
1. [Element principal]
2. [Elements secondaires]
3. [Details]

### Typographie
- Titre: [Police, taille, poids]
- Sous-titres: [Police, taille]
- Corps: [Police, taille]
- Donnees/Stats: [Police, taille, couleur]

### Palette de couleurs
- Primaire: [HEX]
- Secondaire: [HEX]
- Accent: [HEX]
- Fond: [HEX]

### Icones et illustrations
- Style: [Flat, outline, filled, etc.]
- Source recommandee: [Flaticon, Noun Project, etc.]

## FLOW VISUEL
Description du parcours de l'oeil a travers l'infographie

## TEXTES COMPLETS
Tous les textes prets a copier-coller

## PROMPT POUR CREATION
Prompt Canva/Figma ou instructions detaillees pour un designer

## ALTERNATIVES
2 variations de structure pour A/B testing`
  },

  'banner-ad-concept': {
    fields: [
      { name: 'product', label: 'Produit/Service', type: 'text', placeholder: 'Ce que vous promouvez', required: true },
      { name: 'offer', label: 'Offre/Promotion', type: 'text', placeholder: 'Ex: -50%, Essai gratuit, Livraison offerte', required: true },
      { name: 'platform', label: 'Plateforme publicitaire', type: 'select', options: [
        { value: 'google_display', label: 'Google Display Network' },
        { value: 'facebook', label: 'Facebook/Instagram Ads' },
        { value: 'linkedin', label: 'LinkedIn Ads' },
        { value: 'programmatic', label: 'Programmatique' },
        { value: 'website', label: 'Banniere site web' },
      ], required: true },
      { name: 'sizes', label: 'Formats requis', type: 'multiselect', options: [
        { value: '300x250', label: 'Medium Rectangle (300x250)' },
        { value: '728x90', label: 'Leaderboard (728x90)' },
        { value: '160x600', label: 'Skyscraper (160x600)' },
        { value: '320x50', label: 'Mobile Banner (320x50)' },
        { value: '300x600', label: 'Half Page (300x600)' },
        { value: '970x250', label: 'Billboard (970x250)' },
      ] },
      { name: 'targetAudience', label: 'Audience cible', type: 'text', placeholder: 'Qui voulez-vous cibler?' },
      { name: 'cta', label: 'Call-to-action', type: 'text', placeholder: 'Ex: Decouvrir, Acheter, S\'inscrire' },
      { name: 'brandGuidelines', label: 'Contraintes de marque', type: 'textarea', placeholder: 'Couleurs, police, logo, ton...', rows: 2 },
    ],
    promptTemplate: `Tu es un directeur de creation publicitaire. Genere des concepts de bannieres display.

**PRODUIT:** {{product}}
**OFFRE:** {{offer}}
**PLATEFORME:** {{platform}}
**FORMATS:** {{sizes}}
{{#if targetAudience}}**CIBLE:** {{targetAudience}}{{/if}}
{{#if cta}}**CTA:** {{cta}}{{/if}}
{{#if brandGuidelines}}**GUIDELINES:** {{brandGuidelines}}{{/if}}

---

## STRATEGIE CREATIVE

### Message principal
- Hook: [Phrase d'accroche]
- Proposition de valeur: [Benefice cle]
- Urgence: [Element de FOMO]

### Approche visuelle
- Concept: [Description]
- Ton: [Serieux, fun, urgence, etc.]
- Style: [Photo, illustration, graphique]

## CONCEPTS DE BANNIERES (3 versions)

### Concept A: [NOM - ex: "L'offre irresistible"]

Pour chaque format ({{sizes}}):

#### 300x250 (Medium Rectangle)
- **Layout:** [Description de la composition]
- **Texte ligne 1:** [X caracteres max]
- **Texte ligne 2:** [X caracteres max]
- **CTA:** [Bouton]
- **Image/Visual:** [Description]
- **Animation:** [Si applicable - 15s max]

[Repeter pour chaque format]

### Concept B & C: [Meme structure]

## COPY VARIATIONS
Pour A/B testing:
- Headline v1: "..."
- Headline v2: "..."
- Headline v3: "..."

- CTA v1: "..."
- CTA v2: "..."
- CTA v3: "..."

## SPECIFICATIONS TECHNIQUES
- Poids max: 150KB
- Format: JPG/PNG/GIF/HTML5
- Animation: Max 15 secondes, 3 loops
- Texte: Max 20% de l'image (Facebook)

## BRIEF DESIGNER
Instructions completes pour creation

## PROMPTS GENERATION IA
Pour creer les visuels avec Midjourney/DALL-E

## METRIQUES A SUIVRE
- CTR attendu
- Elements a A/B tester
- Criteres de succes`
  },

  'product-mockup-ideas': {
    fields: [
      { name: 'productType', label: 'Type de produit', type: 'select', options: [
        { value: 'physical', label: 'Produit physique' },
        { value: 'digital', label: 'Produit digital (app, site)' },
        { value: 'packaging', label: 'Packaging' },
        { value: 'apparel', label: 'Vetements/Textile' },
        { value: 'print', label: 'Print (livre, carte, flyer)' },
        { value: 'device', label: 'Device (phone, laptop)' },
      ], required: true },
      { name: 'productName', label: 'Nom du produit', type: 'text', placeholder: 'Nom de votre produit', required: true },
      { name: 'productDescription', label: 'Description du produit', type: 'textarea', placeholder: 'Decrivez votre produit en detail', rows: 3, required: true },
      { name: 'useCase', label: 'Usage du mockup', type: 'select', options: [
        { value: 'ecommerce', label: 'Fiche produit e-commerce' },
        { value: 'social', label: 'Reseaux sociaux' },
        { value: 'presentation', label: 'Presentation/Pitch' },
        { value: 'advertising', label: 'Publicite' },
        { value: 'portfolio', label: 'Portfolio' },
      ] },
      { name: 'mood', label: 'Ambiance souhaitee', type: 'select', options: [
        { value: 'premium', label: 'Premium/Luxe' },
        { value: 'minimal', label: 'Minimaliste' },
        { value: 'lifestyle', label: 'Lifestyle' },
        { value: 'professional', label: 'Professionnel' },
        { value: 'playful', label: 'Fun/Colore' },
        { value: 'natural', label: 'Naturel/Eco' },
      ] },
      { name: 'quantity', label: 'Nombre d\'idees', type: 'select', options: [
        { value: '5', label: '5 mockups' },
        { value: '10', label: '10 mockups' },
      ] },
    ],
    promptTemplate: `Tu es un photographe produit et directeur artistique. Genere des idees de mockups creatifs.

**TYPE:** {{productType}}
**PRODUIT:** {{productName}}
**DESCRIPTION:** {{productDescription}}
**USAGE:** {{useCase}}
**AMBIANCE:** {{mood}}
**QUANTITE:** {{quantity}}

---

Genere {{quantity}} idees de mockups:

## MOCKUP 1: [NOM EVOCATEUR]

### Description visuelle complete
- **Angle de vue:** [Front, 3/4, flat lay, etc.]
- **Composition:** [Disposition des elements]
- **Arriere-plan:** [Couleur, texture, environnement]
- **Eclairage:** [Type, direction, intensite]
- **Props/Accessoires:** [Elements de decoration]

### Contexte et storytelling
- Scene suggeree
- Emotion transmise
- Public vise

### Specifications techniques
- Ratio recommande: [16:9, 1:1, 4:5]
- Resolution minimum: [px]
- Format fichier: [PNG, JPG, PSD]

### Prompt Midjourney
\`\`\`
[Prompt detaille pour generer ce mockup]
\`\`\`

### Sources de mockups gratuits
- [Liens vers templates similaires sur Mockup World, Freepik, etc.]

## MOCKUPS 2-{{quantity}}: [Meme structure]

---

## SERIE COHERENTE
Comment utiliser ces mockups ensemble pour:
- Une fiche produit complete
- Un carrousel Instagram
- Une page de vente

## CONSEILS PHOTO
- Equipement recommande
- Parametres appareil
- Post-production

## RESSOURCES
- Templates PSD/Figma gratuits
- Sites de mockups premium
- Banques d'images pour props`
  },

  'icon-description-generator': {
    fields: [
      { name: 'iconPurpose', label: 'Fonction de l\'icone', type: 'text', placeholder: 'Ex: Bouton parametres, Navigation menu, Action supprimer', required: true },
      { name: 'context', label: 'Contexte d\'utilisation', type: 'text', placeholder: 'Ex: App mobile bancaire, Site e-commerce, Dashboard admin' },
      { name: 'style', label: 'Style d\'icone', type: 'select', options: [
        { value: 'outline', label: 'Outline/Ligne' },
        { value: 'filled', label: 'Filled/Plein' },
        { value: 'duotone', label: 'Duotone' },
        { value: 'flat', label: 'Flat' },
        { value: 'hand_drawn', label: 'Hand drawn' },
        { value: '3d', label: '3D' },
        { value: 'gradient', label: 'Gradient' },
      ], required: true },
      { name: 'size', label: 'Taille d\'utilisation', type: 'select', options: [
        { value: '16', label: 'Petite (16-20px)' },
        { value: '24', label: 'Moyenne (24-32px)' },
        { value: '48', label: 'Grande (48-64px)' },
        { value: 'multiple', label: 'Multiple tailles' },
      ] },
      { name: 'existingIcons', label: 'Set d\'icones existant', type: 'select', options: [
        { value: 'none', label: 'Nouveau set' },
        { value: 'heroicons', label: 'Heroicons' },
        { value: 'phosphor', label: 'Phosphor' },
        { value: 'lucide', label: 'Lucide' },
        { value: 'material', label: 'Material Icons' },
        { value: 'feather', label: 'Feather' },
        { value: 'fontawesome', label: 'Font Awesome' },
      ] },
      { name: 'quantity', label: 'Nombre d\'icones', type: 'select', options: [
        { value: '1', label: '1 icone' },
        { value: '5', label: 'Set de 5 icones' },
        { value: '10', label: 'Set de 10 icones' },
      ] },
    ],
    promptTemplate: `Tu es un icon designer professionnel. Cree des descriptions et briefs pour la conception d'icones.

**FONCTION:** {{iconPurpose}}
{{#if context}}**CONTEXTE:** {{context}}{{/if}}
**STYLE:** {{style}}
**TAILLE:** {{size}}px
{{#if existingIcons}}**SET EXISTANT:** {{existingIcons}}{{/if}}
**QUANTITE:** {{quantity}}

---

## BRIEF ICONE(S)

### Icone 1: {{iconPurpose}}

#### Description visuelle detaillee
- **Forme principale:** [Geometrie de base]
- **Elements:** [Composants de l'icone]
- **Details:** [Petits elements distinctifs]
- **Epaisseur de trait:** [Si outline - Xpx]
- **Coins:** [Arrondis, carres, etc.]

#### Metaphore visuelle
- Concept represente
- Association mentale
- Reference universelle

#### Grille et proportions
- Grille de base: [24x24, 32x32, etc.]
- Zone de securite: [X px]
- Alignement: [Optique vs mathematique]

#### Specifications techniques
\`\`\`
Taille: {{size}}px
Style: {{style}}
Stroke width: X px (si outline)
Corner radius: X px
Format: SVG
\`\`\`

{{#if existingIcons}}
#### Coherence avec {{existingIcons}}
- Epaisseur de trait identique
- Angles coherents
- Style de coins uniforme
{{/if}}

### Icones 2-{{quantity}}: [Si applicable, meme structure]

---

## PROMPT MIDJOURNEY
Pour generer une inspiration/reference:
\`\`\`
icon design, [description], {{style}} style, minimal, vector, white background, centered --ar 1:1
\`\`\`

## ICONES SIMILAIRES EXISTANTES
Liens vers des icones similaires sur:
- {{existingIcons}} (si applicable)
- Iconify
- The Noun Project

## GUIDE D'EXPORTATION
- Formats: SVG (vector), PNG (raster)
- Tailles: 16, 24, 32, 48, 64px
- Couleurs: Couleur actuelle + blanc + noir

## CODE D'IMPLEMENTATION
\`\`\`jsx
// React avec Lucide/Heroicons
import { IconName } from 'lucide-react';
<IconName size={{size}} strokeWidth={1.5} />
\`\`\`

## ACCESSIBILITE
- aria-label suggere
- Contraste minimum
- Taille minimum tactile (48px)`
  },

  'brand-style-guide-generator': {
    fields: [
      { name: 'brandName', label: 'Nom de la marque', type: 'text', placeholder: 'Nom de votre entreprise', required: true },
      { name: 'industry', label: 'Secteur d\'activite', type: 'text', placeholder: 'Ex: Fintech, Mode, Food...', required: true },
      { name: 'brandValues', label: 'Valeurs de la marque', type: 'textarea', placeholder: 'Les valeurs fondamentales de votre marque', rows: 3, required: true },
      { name: 'targetAudience', label: 'Public cible', type: 'text', placeholder: 'Votre audience principale' },
      { name: 'existingAssets', label: 'Elements existants', type: 'multiselect', options: [
        { value: 'logo', label: 'Logo' },
        { value: 'colors', label: 'Couleurs definies' },
        { value: 'fonts', label: 'Typographies' },
        { value: 'website', label: 'Site web' },
        { value: 'nothing', label: 'Rien encore' },
      ] },
      { name: 'tone', label: 'Ton de communication', type: 'multiselect', options: [
        { value: 'professional', label: 'Professionnel' },
        { value: 'friendly', label: 'Amical' },
        { value: 'playful', label: 'Ludique' },
        { value: 'authoritative', label: 'Expert/Autorite' },
        { value: 'inspirational', label: 'Inspirant' },
        { value: 'minimalist', label: 'Minimaliste' },
      ] },
      { name: 'competitors', label: 'Concurrents', type: 'text', placeholder: 'Marques concurrentes pour differenciation' },
    ],
    promptTemplate: `Tu es un directeur de marque senior. Cree un guide de style complet.

**MARQUE:** {{brandName}}
**SECTEUR:** {{industry}}
**VALEURS:** {{brandValues}}
{{#if targetAudience}}**AUDIENCE:** {{targetAudience}}{{/if}}
{{#if existingAssets}}**EXISTANT:** {{existingAssets}}{{/if}}
{{#if tone}}**TON:** {{tone}}{{/if}}
{{#if competitors}}**CONCURRENTS:** {{competitors}}{{/if}}

---

# GUIDE DE STYLE {{brandName}}

## 1. IDENTITE DE MARQUE

### Mission
[Enonce de mission en 1-2 phrases]

### Vision
[Ou vous voulez amener la marque]

### Valeurs fondamentales
Pour chaque valeur:
- **[Valeur]:** Definition + Comment elle se manifeste visuellement

### Personnalite de marque
- Archetype: [Sage, Hero, Creator, etc.]
- Traits de personnalite: [3-5 adjectifs]
- Si {{brandName}} etait une personne: [Description]

---

## 2. LOGO

### Logo principal
- Description
- Zone de protection (clear space)
- Taille minimum

### Variations
- Logo horizontal
- Logo vertical
- Logo simplifie (favicon)
- Logo monochrome

### Utilisations incorrectes
Liste des choses a NE PAS faire

---

## 3. PALETTE DE COULEURS

### Couleurs primaires
| Nom | HEX | RGB | Utilisation |
|-----|-----|-----|-------------|
| [Nom] | #XXXXXX | rgb(X,X,X) | [Usage] |

### Couleurs secondaires
[Meme format]

### Couleurs d'accent
[Meme format]

### Ratios d'utilisation
- Primaire: 60%
- Secondaire: 30%
- Accent: 10%

### Mode sombre
Adaptations pour dark mode

---

## 4. TYPOGRAPHIE

### Police principale (Titres)
- Nom: [Police]
- Source: [Google Fonts / Adobe / etc.]
- Poids utilises: [Bold, Medium, etc.]
- Cas d'usage: [Titres, Headlines]

### Police secondaire (Corps)
[Meme format]

### Police accent (Optionnel)
[Meme format]

### Hierarchie typographique
| Element | Police | Taille | Poids | Line Height |
|---------|--------|--------|-------|-------------|
| H1 | ... | ... | ... | ... |
| H2 | ... | ... | ... | ... |
| Body | ... | ... | ... | ... |

---

## 5. IMAGERIE

### Style photographique
- Ton: [Lumineux, sombre, naturel, etc.]
- Sujets: [Personnes, produits, abstraits]
- Traitement: [Filtres, couleurs]

### Illustrations
- Style: [Flat, line art, 3D, etc.]
- Palette: [Coherente avec marque]

### Icones
- Style: [Outline, filled, etc.]
- Set recommande: [Heroicons, Phosphor, etc.]

---

## 6. VOIX ET TON

### Personnalite editoriale
- Nous sommes: [3 adjectifs]
- Nous ne sommes pas: [3 adjectifs]

### Exemples de formulations
| Au lieu de | Dites |
|------------|-------|
| ... | ... |

### Ton par canal
- Site web: [Formel/Casual]
- Reseaux sociaux: [Ton]
- Emails: [Ton]
- Support client: [Ton]

---

## 7. APPLICATIONS

### Cartes de visite
[Specifications]

### Presentations
[Template et guidelines]

### Social media
[Formats et templates]

### Email signatures
[Format standard]

---

## 8. DO's AND DON'Ts

### A FAIRE
- [Liste des bonnes pratiques]

### A NE PAS FAIRE
- [Liste des erreurs a eviter]

---

## TELECHARGEMENTS
- [ ] Kit logo (tous formats)
- [ ] Palette couleurs (ASE, CSS)
- [ ] Polices
- [ ] Templates (Figma, Canva)
- [ ] Icones
- [ ] Photos stock approuvees`
  },

  'image-caption-generator': {
    fields: [
      { name: 'imageDescription', label: 'Description de l\'image', type: 'textarea', placeholder: 'Decrivez l\'image en detail: sujet, couleurs, action, contexte...', required: true, rows: 4 },
      { name: 'platform', label: 'Plateforme', type: 'select', options: [
        { value: 'instagram', label: 'Instagram' },
        { value: 'facebook', label: 'Facebook' },
        { value: 'linkedin', label: 'LinkedIn' },
        { value: 'twitter', label: 'Twitter/X' },
        { value: 'pinterest', label: 'Pinterest' },
        { value: 'tiktok', label: 'TikTok' },
        { value: 'all', label: 'Multi-plateforme' },
      ], required: true },
      { name: 'tone', label: 'Ton souhaite', type: 'select', options: [
        { value: 'professional', label: 'Professionnel' },
        { value: 'casual', label: 'Decontracte' },
        { value: 'inspirational', label: 'Inspirant' },
        { value: 'humorous', label: 'Humoristique' },
        { value: 'educational', label: 'Educatif' },
        { value: 'emotional', label: 'Emotionnel' },
        { value: 'promotional', label: 'Promotionnel' },
      ], required: true },
      { name: 'brand', label: 'Marque/Business', type: 'text', placeholder: 'Nom de votre marque (optionnel)' },
      { name: 'hashtags', label: 'Inclure des hashtags', type: 'checkbox' },
      { name: 'cta', label: 'Call-to-action souhaite', type: 'text', placeholder: 'Ex: Visiter le lien en bio, Commenter, Partager...' },
      { name: 'quantity', label: 'Nombre de legendes', type: 'select', options: [
        { value: '3', label: '3 legendes' },
        { value: '5', label: '5 legendes' },
        { value: '10', label: '10 legendes' },
      ] },
    ],
    promptTemplate: `Tu es un expert en copywriting social media. Genere des legendes engageantes pour cette image.

**IMAGE:** {{imageDescription}}
**PLATEFORME:** {{platform}}
**TON:** {{tone}}
{{#if brand}}**MARQUE:** {{brand}}{{/if}}
{{#if hashtags}}**HASHTAGS:** Oui{{/if}}
{{#if cta}}**CTA:** {{cta}}{{/if}}
**QUANTITE:** {{quantity}}

---

## LEGENDES POUR {{platform}}

{{#if platform === 'instagram'}}
Limites: 2200 caracteres max, 30 hashtags max
{{/if}}
{{#if platform === 'twitter'}}
Limites: 280 caracteres max
{{/if}}
{{#if platform === 'linkedin'}}
Limites: 3000 caracteres, ton professionnel
{{/if}}

### Legende 1: [TYPE - ex: "Storytelling"]

**Texte:**
[Legende complete prete a copier]

{{#if hashtags}}
**Hashtags:**
#hashtag1 #hashtag2 #hashtag3...
{{/if}}

**Pourquoi ca marche:**
- Hook utilise
- Emotion declenchee
- Engagement attendu

---

### Legendes 2-{{quantity}}: [Meme structure avec variations]

- Version courte (accroche)
- Version longue (storytelling)
- Version question (engagement)
- Version emotionnelle
- Version educative

---

## ANALYSE DES LEGENDES

| # | Type | Longueur | Engagement prevu | Meilleur pour |
|---|------|----------|------------------|---------------|
| 1 | ... | ... | ... | ... |

## CONSEILS D'OPTIMISATION {{platform}}

### Meilleur moment pour poster
- Jour: [Recommandation]
- Heure: [Recommandation]

### Structure ideale
- Hook en premiere ligne
- Corps avec valeur
- CTA a la fin
- Hashtags places correctement

### Emojis recommandes
[Liste d'emojis pertinents]

## A/B TEST SUGGERE
Tester:
- Legende 1 vs Legende 3
- Avec hashtags vs Sans
- Avec emoji vs Sans

## HASHTAGS RECHERCHES
{{#if hashtags}}
- Populaires (500k+): #xxx #xxx
- Moyens (50-500k): #xxx #xxx
- Niche (<50k): #xxx #xxx
{{/if}}`
  },
};

export default function DesignToolPage() {
  const params = useParams();
  const toolSlug = params.toolSlug as string;

  const tool = getToolBySlug('design', toolSlug);
  const config = toolConfigs[toolSlug];

  if (!tool || !config) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Outil non trouve</h1>
          <Link href="/tools/design" className="text-fuchsia-600 hover:underline">
            Retour aux outils Design
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/design" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Credits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-fuchsia-100 rounded-xl flex items-center justify-center">
              <Palette className="w-6 h-6 text-fuchsia-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
              <p className="text-gray-600">{tool.description.fr}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="bg-fuchsia-100 text-fuchsia-700 px-3 py-1 rounded-full text-sm font-medium">
              {tool.credits} credits
            </span>
            {tool.priority === 'critical' && (
              <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                <Sparkles className="w-4 h-4" /> Populaire
              </span>
            )}
          </div>
        </div>

        {/* Form */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <form className="space-y-6">
            {config.fields.map((field) => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {field.label}
                  {field.required && <span className="text-red-500 ml-1">*</span>}
                </label>

                {field.type === 'text' && (
                  <input
                    type="text"
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fuchsia-500 focus:border-fuchsia-500"
                  />
                )}

                {field.type === 'textarea' && (
                  <textarea
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    rows={field.rows || 4}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fuchsia-500 focus:border-fuchsia-500"
                  />
                )}

                {field.type === 'select' && (
                  <select
                    name={field.name}
                    required={field.required}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fuchsia-500 focus:border-fuchsia-500"
                  >
                    <option value="">Selectionner...</option>
                    {field.options?.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                )}

                {field.type === 'multiselect' && (
                  <div className="flex flex-wrap gap-2">
                    {field.options?.map((option) => (
                      <label
                        key={option.value}
                        className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50"
                      >
                        <input type="checkbox" name={field.name} value={option.value} className="rounded text-fuchsia-600" />
                        <span className="text-sm">{option.label}</span>
                      </label>
                    ))}
                  </div>
                )}

                {field.type === 'number' && (
                  <input
                    type="number"
                    name={field.name}
                    placeholder={field.placeholder}
                    required={field.required}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fuchsia-500 focus:border-fuchsia-500"
                  />
                )}

                {field.type === 'checkbox' && (
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" name={field.name} className="rounded text-fuchsia-600" />
                    <span className="text-sm text-gray-600">{field.placeholder || 'Oui'}</span>
                  </label>
                )}
              </div>
            ))}

            <button
              type="submit"
              className="w-full bg-fuchsia-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-fuchsia-700 transition flex items-center justify-center gap-2"
            >
              <Sparkles className="w-5 h-5" />
              Generer ({tool.credits} credits)
            </button>
          </form>
        </div>

        {/* Result Placeholder */}
        <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Resultat</h3>
          <div className="bg-gray-50 rounded-lg p-4 min-h-[200px] flex items-center justify-center text-gray-400">
            Le resultat apparaitra ici apres generation...
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Concu en Algerie
          </p>
        </div>
      </footer>
    </div>
  );
}
