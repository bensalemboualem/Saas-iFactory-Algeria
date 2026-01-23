'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Play, Sparkles, Copy, Check, Loader2, Youtube, Video, FileText, Hash, Lightbulb, MessageCircle, TrendingUp, Users, DollarSign, BarChart } from 'lucide-react';
import { youtubeTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

// Configuration des formulaires par outil YouTube
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {
  // ===== BATCH 1 - CRITIQUE (10 outils) =====
  'youtube-title-generator': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Comment gagner de l\'argent sur YouTube en 2026' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé cible', required: true, placeholder: 'Ex: gagner argent YouTube' },
      { name: 'style', type: 'select', label: 'Style de titre', options: ['Clickbait léger', 'Éducatif', 'Listicle (chiffres)', 'Question', 'How-to', 'Révélation/Secret', 'Comparaison vs', 'Challenge'] },
      { name: 'emotion', type: 'select', label: 'Émotion ciblée', options: ['Curiosité', 'Urgence', 'Excitation', 'Peur de rater', 'Surprise', 'Inspiration'] },
      { name: 'variants', type: 'number', label: 'Nombre de titres', placeholder: '10' },
    ],
    promptTemplate: `Tu es un expert YouTube avec 10M+ d'abonnés, spécialisé dans l'optimisation des titres.

SUJET DE LA VIDÉO : {{video_topic}}
MOT-CLÉ CIBLE : {{target_keyword}}
STYLE : {{style}}
ÉMOTION : {{emotion}}

## 🎬 Génère {{variants}} Titres YouTube Ultra-Optimisés

**Règles à suivre :**
- Chiffres impairs (7, 9, 11) convertissent mieux
- Power words : Secret, Incroyable, Choquant, Gratuit, Révélé
- Crochets : [2026], [TUTO], [VLOG], [DÉFI]
- 60 caractères max (idéal : 45-55)
- Mot-clé au début si possible
- Majuscules stratégiques (1-2 mots max)

**Formules gagnantes :**
1. [Chiffre] + [Adjectif] + [Sujet] + [Bénéfice]
2. Comment [Action] + [Résultat] + [Timeframe]
3. J'ai testé [X] pendant [Durée] - [Résultat]
4. [Question provocante] ?
5. [X] vs [Y] : La vérité sur [Sujet]

Pour chaque titre, indique :
- Score CTR estimé (1-10)
- Pourquoi ce titre fonctionne
- Emoji recommandé (optionnel)`
  },

  'youtube-description-generator': {
    fields: [
      { name: 'video_title', type: 'text', label: 'Titre de la vidéo', required: true, placeholder: 'Ex: 10 Astuces YouTube que PERSONNE ne connaît' },
      { name: 'video_summary', type: 'textarea', label: 'Résumé du contenu', required: true, placeholder: 'Décrivez les points principaux de votre vidéo...' },
      { name: 'target_keywords', type: 'text', label: 'Mots-clés (séparés par virgules)', required: true, placeholder: 'youtube, astuces, croissance, algorithme' },
      { name: 'timestamps', type: 'textarea', label: 'Chapitres/Timestamps', placeholder: '0:00 Intro\n1:30 Astuce 1\n...' },
      { name: 'cta_type', type: 'select', label: 'Call-to-action principal', options: ['Abonnement', 'Like + Commentaire', 'Lien dans la bio', 'Playlist', 'Autre vidéo', 'Produit/Service'] },
      { name: 'links', type: 'textarea', label: 'Liens à inclure', placeholder: 'Réseaux sociaux, site web, affiliés...' },
    ],
    promptTemplate: `Tu es expert SEO YouTube avec des millions de vues générées.

TITRE : {{video_title}}
RÉSUMÉ : {{video_summary}}
MOTS-CLÉS : {{target_keywords}}
TIMESTAMPS : {{timestamps}}
CTA : {{cta_type}}
LIENS : {{links}}

## 📝 Description YouTube Optimisée SEO

**Structure professionnelle :**

### Ligne 1-2 (CRITIQUE - visible avant "plus")
Hook accrocheur + mot-clé principal + emoji

### Paragraphe principal (200-300 mots)
- Résumé engageant du contenu
- Intégration naturelle des mots-clés (3-5 fois)
- Valeur promise au viewer
- Questions pour l'engagement

### Chapitres (Timestamps)
Formate les timestamps fournis avec emojis

### Call-to-Action
{{cta_type}} avec formulation persuasive

### Liens & Ressources
Section organisée avec emojis

### Hashtags (3-5 max)
#youtube #[mot-clé] #[niche]

**Optimisation SEO :**
- 2000-5000 caractères
- Mots-clés dans les 200 premiers caractères
- Liens trackables
- Emojis stratégiques (pas trop)`
  },

  'youtube-tags-generator': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Recette couscous algérien traditionnel' },
      { name: 'main_keyword', type: 'text', label: 'Mot-clé principal', required: true, placeholder: 'Ex: couscous algérien' },
      { name: 'niche', type: 'select', label: 'Niche/Catégorie', options: ['Tech', 'Gaming', 'Cuisine', 'Lifestyle', 'Business', 'Éducation', 'Divertissement', 'Sport', 'Voyage', 'Beauté', 'Musique', 'Autre'] },
      { name: 'language', type: 'select', label: 'Langue principale', options: ['Français', 'Arabe', 'Anglais', 'Darija', 'Multilingue'] },
      { name: 'competitor_channel', type: 'text', label: 'Chaîne concurrente (optionnel)', placeholder: 'Ex: Cuisine DZ' },
    ],
    promptTemplate: `Tu es expert en SEO YouTube et optimisation des tags.

SUJET : {{video_topic}}
MOT-CLÉ PRINCIPAL : {{main_keyword}}
NICHE : {{niche}}
LANGUE : {{language}}
CONCURRENT : {{competitor_channel}}

## 🏷️ Génération de Tags YouTube Optimisés

**Stratégie de tags (500 caractères max au total) :**

### Tags Exacts (Priorité haute)
- Mot-clé exact
- Variations proches
- Avec/sans accents

### Tags Larges (Découvrabilité)
- Catégorie générale
- Termes de niche populaires

### Tags Long-tail (Faible concurrence)
- Questions fréquentes
- "Comment + [action]"
- "[Sujet] pour débutants"

### Tags Tendance
- Événements actuels liés
- Termes viraux de la niche

### Tags Locaux (si applicable)
- Géolocalisation
- Termes régionaux

**Format de sortie :**
Liste de 30-40 tags, triés par importance
Estimation du volume de recherche (Élevé/Moyen/Faible)
Tags à éviter (trop génériques ou spam)`
  },

  'youtube-script-writer': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Les 5 erreurs des débutants sur YouTube' },
      { name: 'video_length', type: 'select', label: 'Durée cible', options: ['Court (3-5 min)', 'Moyen (8-12 min)', 'Long (15-20 min)', 'Très long (25+ min)'] },
      { name: 'tone', type: 'select', label: 'Ton du script', options: ['Énergique & Dynamique', 'Calme & Éducatif', 'Humoristique', 'Storytelling', 'Direct & Professionnel', 'Inspirant'] },
      { name: 'target_audience', type: 'text', label: 'Audience cible', placeholder: 'Ex: Créateurs YouTube débutants 18-35 ans' },
      { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir', required: true, placeholder: 'Point 1: ...\nPoint 2: ...\nPoint 3: ...' },
      { name: 'cta', type: 'text', label: 'Call-to-action final', placeholder: 'Ex: Abonnez-vous et activez la cloche' },
    ],
    promptTemplate: `Tu es un scriptwriter YouTube professionnel qui a écrit pour des chaînes à millions d'abonnés.

SUJET : {{video_topic}}
DURÉE : {{video_length}}
TON : {{tone}}
AUDIENCE : {{target_audience}}
POINTS CLÉS : {{key_points}}
CTA : {{cta}}

## 🎬 Script YouTube Complet

### HOOK (0:00 - 0:30)
**[ACCROCHE CHOC]**
- Pattern interrupt (phrase surprenante)
- Promesse de valeur
- Preview du meilleur moment

**[Transition vers intro]**

### INTRO (0:30 - 1:30)
**[PRÉSENTATION]**
- Qui tu es (crédibilité)
- Ce qu'ils vont apprendre
- Pourquoi c'est important MAINTENANT

**[CTA précoce - Abonnement]**

### CORPS DU CONTENU
Pour chaque point clé :

**[POINT X - Timestamp]**
- Transition fluide
- Explication claire
- Exemple concret
- B-roll suggéré
- Note pour le montage

### RÉCAPITULATIF
- Résumé des points clés
- Valeur délivrée

### OUTRO
**[CTA FINAL]**
- {{cta}}
- Teaser prochaine vidéo
- Écran de fin

---
**Notes techniques :**
- [B-ROLL] suggestions visuelles
- [TEXTE À L'ÉCRAN] éléments graphiques
- [MUSIQUE] ambiance suggérée
- [PAUSE] moments de respiration`
  },

  'youtube-shorts-script': {
    fields: [
      { name: 'topic', type: 'text', label: 'Sujet du Short', required: true, placeholder: 'Ex: 3 astuces pour gagner des abonnés' },
      { name: 'hook_style', type: 'select', label: 'Style d\'accroche', options: ['Question choc', 'Fait surprenant', 'Promesse rapide', 'Controverse légère', 'Défi', 'POV'] },
      { name: 'format', type: 'select', label: 'Format', options: ['Tips/Astuces', 'Story time', 'Tutoriel rapide', 'Réaction', 'Avant/Après', 'Comparaison', 'Top 3'] },
      { name: 'duration', type: 'select', label: 'Durée', options: ['15 secondes', '30 secondes', '45 secondes', '60 secondes'] },
      { name: 'trend', type: 'text', label: 'Tendance/Son à utiliser (optionnel)', placeholder: 'Ex: Son viral TikTok...' },
    ],
    promptTemplate: `Tu es expert en contenu vertical viral (Shorts, Reels, TikTok).

SUJET : {{topic}}
ACCROCHE : {{hook_style}}
FORMAT : {{format}}
DURÉE : {{duration}}
TENDANCE : {{trend}}

## 📱 Script YouTube Short Viral

### STRUCTURE {{duration}}

**SECONDE 1-3 : HOOK**
[{{hook_style}}]
"[Phrase d'accroche qui STOPPE le scroll]"

**SECONDE 4-X : CONTENU**
[Rythme rapide, pas de temps mort]
- Point 1 (X sec)
- Point 2 (X sec)
- Point 3 (X sec)

**DERNIÈRES SECONDES : PAYOFF**
[Résolution + Loop potentiel]

---

### VERSION COMPLÈTE DU SCRIPT

**[À L'ÉCRAN]** Instructions visuelles
**[VOIX]** Ce que tu dis
**[TEXTE]** Texte superposé
**[ACTION]** Gestes/Mouvements

---

### OPTIMISATIONS SHORTS

**Hashtags suggérés :**
#shorts #youtube #[niche]

**Caption :**
[Texte court et engageant pour la description]

**Conseil loop :**
[Comment faire revenir au début]

**Meilleur moment pour poster :**
[Suggestion horaire]`
  },

  'youtube-thumbnail-ideas': {
    fields: [
      { name: 'video_title', type: 'text', label: 'Titre de la vidéo', required: true, placeholder: 'Ex: J\'ai testé le régime de CR7 pendant 30 jours' },
      { name: 'video_topic', type: 'textarea', label: 'Description du contenu', required: true, placeholder: 'Décrivez votre vidéo pour des idées de miniatures pertinentes...' },
      { name: 'style', type: 'select', label: 'Style de miniature', options: ['Face + Émotion', 'Avant/Après', 'Texte gros', 'Mystère/Flou', 'Split screen', 'Minimaliste', 'Coloré/Pop', 'Réaliste'] },
      { name: 'colors', type: 'select', label: 'Palette de couleurs', options: ['Rouge/Jaune (énergie)', 'Bleu/Blanc (confiance)', 'Vert/Noir (argent)', 'Rose/Violet (créatif)', 'Orange/Noir (urgence)', 'Personnalisée'] },
      { name: 'competitor_style', type: 'text', label: 'Style de concurrent à analyser', placeholder: 'Ex: MrBeast, Squeezie...' },
    ],
    promptTemplate: `Tu es designer de miniatures YouTube avec un taux de clic moyen de 12%+.

TITRE : {{video_title}}
CONTENU : {{video_topic}}
STYLE : {{style}}
COULEURS : {{colors}}
RÉFÉRENCE : {{competitor_style}}

## 🖼️ 5 Concepts de Miniatures YouTube

Pour chaque concept :

### Concept [X] : [Nom du concept]

**Composition visuelle :**
- Élément principal (60% de l'image)
- Élément secondaire
- Arrière-plan

**Texte sur miniature :**
- Maximum 3-4 mots
- Police suggérée
- Placement

**Expression faciale (si applicable) :**
- Émotion à exprimer
- Direction du regard

**Palette exacte :**
- Couleur principale : #XXXXXX
- Couleur accent : #XXXXXX
- Couleur texte : #XXXXXX

**Éléments graphiques :**
- Flèches, cercles, emojis
- Effets (glow, ombre)

**Score CTR prévu : X/10**

---

### Conseils techniques :
- Résolution : 1280x720 minimum
- Contraste élevé pour mobile
- Test de lisibilité à petite taille
- Éviter : trop de texte, visages coupés, couleurs ternes`
  },

  'youtube-hook-generator': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Comment j\'ai gagné 10K€ en dropshipping' },
      { name: 'hook_type', type: 'select', label: 'Type de hook', options: ['Question rhétorique', 'Statistique choc', 'Histoire personnelle', 'Controverse', 'Promesse directe', 'Pattern interrupt', 'Teaser du meilleur moment', 'Défi au viewer'] },
      { name: 'duration', type: 'select', label: 'Durée du hook', options: ['5 secondes', '10 secondes', '15 secondes', '30 secondes'] },
      { name: 'energy', type: 'select', label: 'Niveau d\'énergie', options: ['Explosif', 'Intrigant/Mystérieux', 'Calme mais captivant', 'Humoristique'] },
      { name: 'variants', type: 'number', label: 'Nombre de hooks', placeholder: '5' },
    ],
    promptTemplate: `Tu es expert en rétention YouTube, spécialisé dans les 30 premières secondes.

SUJET : {{video_topic}}
TYPE : {{hook_type}}
DURÉE : {{duration}}
ÉNERGIE : {{energy}}

## 🪝 {{variants}} Hooks YouTube Ultra-Captivants

**Objectif : 0% de drop dans les {{duration}} premières secondes**

Pour chaque hook :

### Hook [X] - [Style]

**Script exact :**
"[Le texte mot pour mot à dire]"

**Instructions de delivery :**
- Ton de voix
- Rythme
- Pauses stratégiques

**Visuel suggéré :**
- Ce qui apparaît à l'écran
- B-roll recommandé

**Pourquoi ça fonctionne :**
- Principe psychologique utilisé
- Score de rétention estimé

---

### Formules de hooks éprouvées :

1. **Le choc** : "Ce que je vais vous montrer a changé ma vie..."
2. **La question** : "Pourquoi 99% des gens échouent à...?"
3. **Le teaser** : "À la fin de cette vidéo, vous saurez..."
4. **L'anti-intro** : "[Meilleur moment] Mais d'abord..."
5. **Le défi** : "Je parie que vous ne saviez pas que..."`
  },

  'youtube-seo-optimizer': {
    fields: [
      { name: 'video_title', type: 'text', label: 'Titre actuel', required: true, placeholder: 'Votre titre YouTube actuel' },
      { name: 'video_description', type: 'textarea', label: 'Description actuelle', required: true, placeholder: 'Copiez votre description actuelle...' },
      { name: 'current_tags', type: 'textarea', label: 'Tags actuels', placeholder: 'tag1, tag2, tag3...' },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé principal visé', required: true, placeholder: 'Ex: apprendre le piano' },
      { name: 'competitors', type: 'textarea', label: 'URLs vidéos concurrentes', placeholder: 'https://youtube.com/watch?v=... (une par ligne)' },
    ],
    promptTemplate: `Tu es consultant SEO YouTube avec 500M+ de vues générées pour tes clients.

TITRE ACTUEL : {{video_title}}
DESCRIPTION : {{video_description}}
TAGS : {{current_tags}}
MOT-CLÉ CIBLE : {{target_keyword}}
CONCURRENTS : {{competitors}}

## 🔍 Audit SEO YouTube Complet

### 1. ANALYSE DU TITRE
**Score actuel : X/10**

❌ Problèmes détectés :
- [Liste des problèmes]

✅ Points positifs :
- [Ce qui fonctionne]

**Titre optimisé proposé :**
"[Nouveau titre]"

### 2. ANALYSE DE LA DESCRIPTION
**Score actuel : X/10**

❌ Problèmes :
- Densité mot-clé : X%
- Structure : [analyse]
- CTA : [présent/absent]

**Description optimisée :**
[Nouvelle description complète]

### 3. ANALYSE DES TAGS
**Score actuel : X/10**

❌ Tags à retirer :
- [tags inefficaces]

✅ Tags à ajouter :
- [nouveaux tags suggérés]

**Set de tags optimisé :**
[Liste complète]

### 4. RECOMMANDATIONS AVANCÉES
- Nom de fichier vidéo suggéré
- Sous-titres/CC
- Cards et écrans de fin
- Playlists pertinentes
- Meilleur moment de publication

### 5. SCORE SEO GLOBAL
**Avant : X/100 → Après : X/100**`
  },

  'youtube-content-ideas': {
    fields: [
      { name: 'channel_niche', type: 'text', label: 'Niche de votre chaîne', required: true, placeholder: 'Ex: Fitness, Tech, Cuisine algérienne...' },
      { name: 'target_audience', type: 'text', label: 'Audience cible', required: true, placeholder: 'Ex: Hommes 25-40 ans intéressés par la musculation' },
      { name: 'content_type', type: 'select', label: 'Type de contenu préféré', options: ['Tutoriels', 'Vlogs', 'Reviews', 'Listes/Top', 'Storytelling', 'Challenges', 'Interviews', 'Réactions', 'Mixte'] },
      { name: 'posting_frequency', type: 'select', label: 'Fréquence de publication', options: ['Quotidien', '3x/semaine', '2x/semaine', '1x/semaine', '2x/mois'] },
      { name: 'trending_topics', type: 'text', label: 'Sujets tendance à explorer', placeholder: 'Ex: IA, Ramadan, CAN 2026...' },
      { name: 'ideas_count', type: 'number', label: 'Nombre d\'idées', placeholder: '20' },
    ],
    promptTemplate: `Tu es stratège de contenu YouTube ayant aidé 100+ créateurs à atteindre 100K abonnés.

NICHE : {{channel_niche}}
AUDIENCE : {{target_audience}}
TYPE DE CONTENU : {{content_type}}
FRÉQUENCE : {{posting_frequency}}
TENDANCES : {{trending_topics}}

## 💡 {{ideas_count}} Idées de Vidéos YouTube

### Catégorie 1 : Contenu Evergreen (toujours pertinent)
| # | Titre suggéré | Format | Difficulté | Potentiel vues |
|---|---------------|--------|------------|----------------|
| 1 | ... | ... | ... | ... |

### Catégorie 2 : Tendances actuelles
| # | Titre suggéré | Pourquoi maintenant | Urgence |
|---|---------------|---------------------|---------|
| 1 | ... | ... | ... |

### Catégorie 3 : Contenu viral potentiel
| # | Titre suggéré | Hook | Élément viral |
|---|---------------|------|---------------|
| 1 | ... | ... | ... |

### Catégorie 4 : Séries récurrentes
| # | Nom de la série | Concept | Fréquence suggérée |
|---|-----------------|---------|-------------------|
| 1 | ... | ... | ... |

---

### Calendrier de contenu suggéré (1 mois)
**Semaine 1 :** [3-4 idées]
**Semaine 2 :** [3-4 idées]
**Semaine 3 :** [3-4 idées]
**Semaine 4 :** [3-4 idées]

### Bonus : Idées de Shorts
[5 idées de Shorts liées aux vidéos longues]`
  },

  'youtube-intro-outro-script': {
    fields: [
      { name: 'channel_name', type: 'text', label: 'Nom de la chaîne', required: true, placeholder: 'Ex: Tech DZ, Cuisine Mama...' },
      { name: 'channel_niche', type: 'text', label: 'Niche', required: true, placeholder: 'Ex: Tutoriels tech, Recettes algériennes...' },
      { name: 'personality', type: 'select', label: 'Personnalité de la chaîne', options: ['Énergique & Fun', 'Professionnel & Expert', 'Chaleureux & Accessible', 'Mystérieux & Intrigant', 'Humoristique', 'Inspirant'] },
      { name: 'intro_duration', type: 'select', label: 'Durée intro', options: ['5 secondes', '10 secondes', '15 secondes'] },
      { name: 'outro_duration', type: 'select', label: 'Durée outro', options: ['15 secondes', '20 secondes', '30 secondes'] },
      { name: 'catchphrase', type: 'text', label: 'Catchphrase existante (optionnel)', placeholder: 'Ex: "Salut la famille !"' },
    ],
    promptTemplate: `Tu es branding expert YouTube spécialisé dans les intros/outros mémorables.

CHAÎNE : {{channel_name}}
NICHE : {{channel_niche}}
PERSONNALITÉ : {{personality}}
DURÉE INTRO : {{intro_duration}}
DURÉE OUTRO : {{outro_duration}}
CATCHPHRASE : {{catchphrase}}

## 🎬 Pack Intro/Outro Professionnel

### INTRO ({{intro_duration}})

**Version 1 - Classique**
[Script + timing exact]
- 0:00 - [Action/Visuel]
- 0:0X - "[Texte à dire]"
- ...

**Version 2 - Dynamique**
[Variante plus énergique]

**Version 3 - Minimaliste**
[Variante courte et efficace]

**Éléments visuels suggérés :**
- Animation logo
- Transition
- Musique/Son (style)

---

### OUTRO ({{outro_duration}})

**Script complet :**

"[Récap rapide de la valeur]"

"[CTA Abonnement]"
→ Animation : bouton s'abonner + cloche

"[CTA Engagement]"
→ "Dis-moi en commentaire..."

"[Teaser prochaine vidéo]"
→ "La semaine prochaine, on parle de..."

"[Signature/Catchphrase de fin]"
→ {{catchphrase}} ou suggestion

**Écran de fin (20 sec) :**
- Placement vidéo suggérée
- Placement playlist
- Bouton d'abonnement

---

### MUSIQUE/SOUND DESIGN
- Style musical recommandé
- BPM suggéré
- Ressources libres de droits`
  },

  // ===== BATCH 2 - HIGH PRIORITY (10 outils) =====
  'youtube-video-outline': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Guide complet du montage vidéo pour débutants' },
      { name: 'video_length', type: 'select', label: 'Durée cible', options: ['5-8 minutes', '10-15 minutes', '20-30 minutes', '45+ minutes'] },
      { name: 'video_style', type: 'select', label: 'Style de vidéo', options: ['Tutoriel', 'Vlog', 'Essai/Opinion', 'Review', 'Documentaire', 'Entertainment'] },
      { name: 'key_takeaways', type: 'textarea', label: 'Points clés à transmettre', required: true, placeholder: 'Ce que le viewer doit retenir...' },
      { name: 'research_notes', type: 'textarea', label: 'Notes de recherche', placeholder: 'Infos, stats, sources à inclure...' },
    ],
    promptTemplate: `Tu es producteur YouTube expérimenté spécialisé dans la structure de contenu.

SUJET : {{video_topic}}
DURÉE : {{video_length}}
STYLE : {{video_style}}
POINTS CLÉS : {{key_takeaways}}
RECHERCHE : {{research_notes}}

## 📋 Plan de Vidéo YouTube Détaillé

### STRUCTURE GLOBALE

**Durée totale estimée : {{video_length}}**

| Section | Durée | % du total |
|---------|-------|------------|
| Hook | 30s | 5% |
| Intro | 1min | 10% |
| Corps | Xmin | 70% |
| Récap | 1min | 10% |
| Outro | 30s | 5% |

---

### PLAN DÉTAILLÉ

**[0:00-0:30] HOOK**
- Accroche suggérée
- Élément visuel

**[0:30-1:30] INTRO**
- Présentation du sujet
- Promesse de valeur
- CTA précoce

**[1:30-X:XX] SECTION 1 : [Titre]**
- Point principal
- Exemple/Démonstration
- Transition vers section 2
- [B-roll suggéré]

**[X:XX-X:XX] SECTION 2 : [Titre]**
...

**[X:XX-X:XX] RÉCAPITULATIF**
- Points clés résumés
- Valeur délivrée

**[X:XX-FIN] OUTRO**
- CTA final
- Teaser

---

### NOTES DE PRODUCTION
- Équipement suggéré
- Lieux de tournage
- Graphiques nécessaires
- Musique d'ambiance`
  },

  'youtube-comment-reply': {
    fields: [
      { name: 'comment', type: 'textarea', label: 'Commentaire à répondre', required: true, placeholder: 'Copiez le commentaire YouTube ici...' },
      { name: 'comment_type', type: 'select', label: 'Type de commentaire', options: ['Question', 'Compliment', 'Critique constructive', 'Hater/Négatif', 'Suggestion', 'Témoignage', 'Demande de contenu'] },
      { name: 'tone', type: 'select', label: 'Ton de réponse', options: ['Amical & Chaleureux', 'Professionnel', 'Humoristique', 'Reconnaissant', 'Éducatif'] },
      { name: 'include_cta', type: 'checkbox', label: 'Inclure un call-to-action' },
      { name: 'channel_personality', type: 'text', label: 'Personnalité de la chaîne', placeholder: 'Ex: Fun et accessible, Expert sérieux...' },
    ],
    promptTemplate: `Tu es community manager YouTube expert en engagement.

COMMENTAIRE : {{comment}}
TYPE : {{comment_type}}
TON : {{tone}}
CTA : {{include_cta}}
PERSONNALITÉ : {{channel_personality}}

## 💬 Réponses au Commentaire

### Réponse 1 - Standard
[Réponse appropriée au type de commentaire]

### Réponse 2 - Avec engagement
[Version qui encourage plus d'interaction]

### Réponse 3 - Avec CTA (si applicable)
[Version avec appel à l'action subtil]

---

### Conseils pour ce type de commentaire :
- Temps de réponse idéal
- Éléments à inclure/éviter
- Comment transformer en opportunité

### Réponses types à éviter :
- [Exemples de mauvaises réponses]

### Si le commentaire est négatif :
- Technique de désescalade
- Quand ignorer vs répondre
- Comment tourner en positif`
  },

  'youtube-community-post': {
    fields: [
      { name: 'post_type', type: 'select', label: 'Type de post', required: true, options: ['Sondage', 'Question ouverte', 'Annonce', 'Behind the scenes', 'Teaser vidéo', 'Quiz', 'Partage d\'image', 'Milestone'] },
      { name: 'topic', type: 'text', label: 'Sujet du post', required: true, placeholder: 'Ex: Quelle vidéo voulez-vous voir?' },
      { name: 'goal', type: 'select', label: 'Objectif', options: ['Engagement (commentaires)', 'Feedback audience', 'Hype pour nouvelle vidéo', 'Connexion communauté', 'Promotion'] },
      { name: 'include_image', type: 'checkbox', label: 'Post avec image' },
      { name: 'channel_niche', type: 'text', label: 'Niche de la chaîne', placeholder: 'Ex: Gaming, Cuisine...' },
    ],
    promptTemplate: `Tu es expert en engagement communauté YouTube.

TYPE : {{post_type}}
SUJET : {{topic}}
OBJECTIF : {{goal}}
IMAGE : {{include_image}}
NICHE : {{channel_niche}}

## 📢 Post Communauté YouTube

### Post Principal

**Texte du post :**
[Texte optimisé pour l'engagement, max 500 caractères]

**Si sondage - Options :**
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]

**Si image - Description :**
[Ce que l'image devrait montrer]

---

### Variantes

**Version A - Plus casual**
[Texte alternatif]

**Version B - Plus engageante**
[Texte avec question directe]

---

### Timing optimal
- Meilleur jour : [jour]
- Meilleure heure : [heure]
- Pourquoi : [explication]

### Conseils d'engagement
- Comment répondre aux premiers commentaires
- Hashtags recommandés (si applicable)
- Fréquence de posts suggérée`
  },

  'youtube-playlist-optimizer': {
    fields: [
      { name: 'playlist_theme', type: 'text', label: 'Thème de la playlist', required: true, placeholder: 'Ex: Tutoriels Python pour débutants' },
      { name: 'current_videos', type: 'textarea', label: 'Vidéos actuelles (titres)', required: true, placeholder: 'Vidéo 1\nVidéo 2\nVidéo 3...' },
      { name: 'target_audience', type: 'text', label: 'Audience cible', placeholder: 'Ex: Développeurs débutants' },
      { name: 'playlist_goal', type: 'select', label: 'Objectif de la playlist', options: ['Watch time max', 'Conversion abonnés', 'Éducation progressive', 'Showcase portfolio', 'SEO'] },
    ],
    promptTemplate: `Tu es expert en optimisation de playlists YouTube pour maximiser le watch time.

THÈME : {{playlist_theme}}
VIDÉOS : {{current_videos}}
AUDIENCE : {{target_audience}}
OBJECTIF : {{playlist_goal}}

## 📁 Optimisation Playlist YouTube

### 1. TITRE DE PLAYLIST OPTIMISÉ

**Titre actuel analysé :** [analyse]

**Nouveaux titres suggérés :**
1. [Titre SEO-friendly]
2. [Titre accrocheur]
3. [Titre descriptif]

### 2. DESCRIPTION DE PLAYLIST

[Description optimisée 200-500 mots avec mots-clés]

### 3. ORDRE OPTIMAL DES VIDÉOS

| Position | Vidéo | Raison du placement |
|----------|-------|---------------------|
| 1 | [Meilleur hook] | Capturer l'attention |
| 2 | [Vidéo populaire] | Maintenir l'intérêt |
| ... | ... | ... |

### 4. VIDÉOS MANQUANTES

Suggestions de vidéos à créer pour compléter :
1. [Idée 1] - Pourquoi
2. [Idée 2] - Pourquoi

### 5. OPTIMISATIONS AVANCÉES
- Miniature de playlist
- Cards inter-playlist
- Promotion croisée`
  },

  'youtube-channel-audit': {
    fields: [
      { name: 'channel_name', type: 'text', label: 'Nom de la chaîne', required: true, placeholder: 'Votre chaîne YouTube' },
      { name: 'channel_url', type: 'text', label: 'URL de la chaîne', placeholder: 'https://youtube.com/@...' },
      { name: 'subscriber_count', type: 'text', label: 'Nombre d\'abonnés', placeholder: 'Ex: 15K' },
      { name: 'monthly_views', type: 'text', label: 'Vues mensuelles moyennes', placeholder: 'Ex: 50K' },
      { name: 'content_frequency', type: 'select', label: 'Fréquence de publication', options: ['Quotidien', '3-4x/semaine', '1-2x/semaine', '2-3x/mois', 'Irrégulier'] },
      { name: 'main_issues', type: 'textarea', label: 'Problèmes perçus', placeholder: 'Ex: Vues en baisse, peu de commentaires...' },
    ],
    promptTemplate: `Tu es consultant YouTube ayant audité 500+ chaînes et généré des millions de vues.

CHAÎNE : {{channel_name}}
URL : {{channel_url}}
ABONNÉS : {{subscriber_count}}
VUES/MOIS : {{monthly_views}}
FRÉQUENCE : {{content_frequency}}
PROBLÈMES : {{main_issues}}

## 🔍 Audit Complet de Chaîne YouTube

### 1. SCORE GLOBAL : X/100

| Critère | Score | Priorité |
|---------|-------|----------|
| Branding | X/10 | 🔴/🟡/🟢 |
| SEO | X/10 | ... |
| Contenu | X/10 | ... |
| Engagement | X/10 | ... |
| Croissance | X/10 | ... |

---

### 2. ANALYSE DU BRANDING
**Logo & Bannière :**
- [Analyse]
- [Recommandations]

**À propos :**
- [Analyse]
- [Optimisations]

### 3. ANALYSE SEO
**Titres :**
- Pattern actuel
- Améliorations

**Descriptions :**
- [Analyse]

**Tags & Mots-clés :**
- [Analyse]

### 4. ANALYSE DU CONTENU
**Points forts :**
- [Liste]

**Points faibles :**
- [Liste]

**Opportunités manquées :**
- [Liste]

### 5. PLAN D'ACTION 30 JOURS
**Semaine 1 :** [Actions prioritaires]
**Semaine 2 :** [Actions secondaires]
**Semaine 3 :** [Optimisations]
**Semaine 4 :** [Consolidation]

### 6. OBJECTIFS RÉALISTES
- 30 jours : [objectif]
- 90 jours : [objectif]
- 6 mois : [objectif]`
  },

  'youtube-monetization-tips': {
    fields: [
      { name: 'subscriber_count', type: 'text', label: 'Nombre d\'abonnés', required: true, placeholder: 'Ex: 5K, 50K, 500K' },
      { name: 'niche', type: 'text', label: 'Niche de la chaîne', required: true, placeholder: 'Ex: Tech, Gaming, Lifestyle...' },
      { name: 'current_revenue', type: 'select', label: 'Revenus actuels', options: ['Pas encore monétisé', 'AdSense uniquement', 'AdSense + Sponsors', 'Revenus diversifiés', 'Full-time YouTuber'] },
      { name: 'goals', type: 'select', label: 'Objectif financier', options: ['Premiers 100€/mois', '1000€/mois', '5000€/mois', '10000€+/mois', 'Remplacer salaire'] },
      { name: 'audience_location', type: 'select', label: 'Localisation audience', options: ['France', 'Algérie', 'Maghreb', 'Monde arabe', 'International', 'Mixte'] },
    ],
    promptTemplate: `Tu es coach monétisation YouTube ayant aidé des créateurs à générer 6 chiffres/an.

ABONNÉS : {{subscriber_count}}
NICHE : {{niche}}
REVENUS ACTUELS : {{current_revenue}}
OBJECTIF : {{goals}}
AUDIENCE : {{audience_location}}

## 💰 Stratégie de Monétisation YouTube

### 1. ANALYSE DE VOTRE SITUATION

**Potentiel estimé :**
- CPM moyen de votre niche : X€
- Revenu AdSense potentiel : X€/mois
- Potentiel total : X€/mois

### 2. SOURCES DE REVENUS RECOMMANDÉES

| Source | Potentiel | Difficulté | Priorité |
|--------|-----------|------------|----------|
| AdSense | €€ | Facile | ⭐⭐⭐ |
| Sponsors | €€€ | Moyen | ... |
| Affiliation | €€ | Facile | ... |
| Produits | €€€€ | Difficile | ... |
| Membres | €€ | Moyen | ... |

### 3. PLAN D'ACTION PAR ÉTAPE

**Étape 1 : Atteindre les prérequis**
- 1000 abonnés : [stratégie]
- 4000h watch time : [stratégie]

**Étape 2 : Optimiser AdSense**
- Meilleurs formats de vidéos
- Durée optimale (8-15 min)
- Placement mid-rolls

**Étape 3 : Sponsors**
- Comment les contacter
- Tarifs suggérés pour {{subscriber_count}}
- Template de pitch

**Étape 4 : Diversification**
- Produits digitaux adaptés à {{niche}}
- Affiliation recommandée
- Super Thanks & Membres

### 4. REVENUS ESTIMÉS À 12 MOIS
[Projection réaliste basée sur votre situation]`
  },

  'youtube-collab-pitch': {
    fields: [
      { name: 'your_channel', type: 'text', label: 'Votre chaîne', required: true, placeholder: 'Nom et niche de votre chaîne' },
      { name: 'your_stats', type: 'text', label: 'Vos stats', required: true, placeholder: 'Ex: 25K abonnés, 100K vues/mois' },
      { name: 'target_creator', type: 'text', label: 'Créateur ciblé', required: true, placeholder: 'Nom de la chaîne à contacter' },
      { name: 'collab_idea', type: 'textarea', label: 'Idée de collaboration', required: true, placeholder: 'Décrivez votre idée de vidéo commune...' },
      { name: 'mutual_benefit', type: 'textarea', label: 'Bénéfices mutuels', placeholder: 'Ce que chacun y gagne...' },
    ],
    promptTemplate: `Tu es expert en networking YouTube et partenariats entre créateurs.

VOTRE CHAÎNE : {{your_channel}}
VOS STATS : {{your_stats}}
CRÉATEUR CIBLÉ : {{target_creator}}
IDÉE : {{collab_idea}}
BÉNÉFICES : {{mutual_benefit}}

## 🤝 Pitch de Collaboration YouTube

### EMAIL DE CONTACT

**Objet :** [3 options d'objets accrocheurs]

---

**Corps du message :**

Salut [Prénom],

[Accroche personnalisée - montrer que vous connaissez son contenu]

[Présentation rapide - 2 phrases max]

[Proposition de valeur - ce que VOUS apportez]

[Idée de collab concrète]

[Call-to-action clair]

[Signature]

---

### VERSION DM (Instagram/Twitter)

[Version courte 280 caractères]

### VERSION COMMENTAIRE YOUTUBE

[Version ultra-courte pour initier le contact]

---

### CONSEILS POUR MAXIMISER LES CHANCES

**Avant de pitcher :**
- [ ] Suivre et engager depuis 2+ semaines
- [ ] Commenter ses vidéos
- [ ] Partager son contenu

**Timing optimal :**
- Meilleur moment pour envoyer
- Délai de relance

**Red flags à éviter :**
- [Liste des erreurs courantes]

### IDÉES DE FORMATS DE COLLAB
1. [Format 1] - Pourquoi ça marche
2. [Format 2] - Pourquoi ça marche
3. [Format 3] - Pourquoi ça marche`
  },

  'youtube-brand-deal-email': {
    fields: [
      { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true, placeholder: 'Ex: Samsung, Nike, startup locale...' },
      { name: 'your_channel', type: 'text', label: 'Votre chaîne', required: true, placeholder: 'Nom et niche' },
      { name: 'your_stats', type: 'textarea', label: 'Vos statistiques', required: true, placeholder: 'Abonnés, vues moyennes, démo audience...' },
      { name: 'partnership_type', type: 'select', label: 'Type de partenariat', options: ['Vidéo sponsorisée', 'Intégration produit', 'Ambassadeur', 'Affiliation', 'Événement', 'Long terme'] },
      { name: 'previous_collabs', type: 'textarea', label: 'Collaborations précédentes', placeholder: 'Marques avec lesquelles vous avez travaillé...' },
    ],
    promptTemplate: `Tu es agent de talents YouTube spécialisé dans les deals marques.

MARQUE : {{brand_name}}
CHAÎNE : {{your_channel}}
STATS : {{your_stats}}
TYPE : {{partnership_type}}
HISTORIQUE : {{previous_collabs}}

## 📧 Email Professionnel Brand Deal

### VERSION 1 - OUTREACH INITIAL

**Objet :** Proposition de partenariat - {{your_channel}} x {{brand_name}}

---

[Email complet professionnel]

---

### VERSION 2 - RÉPONSE À BRIEF

**Objet :** Re: Opportunité de collaboration

---

[Email de réponse professionnelle]

---

### MEDIA KIT À JOINDRE (structure)

**Page 1 - Présentation**
- Bio courte
- Proposition de valeur unique

**Page 2 - Statistiques**
- Abonnés
- Vues moyennes
- Engagement rate
- Démographie audience

**Page 3 - Offres & Tarifs**
| Format | Description | Tarif |
|--------|-------------|-------|
| ... | ... | ... |

**Page 4 - Témoignages**
- Collaborations passées
- Résultats obtenus

---

### NÉGOCIATION - TARIFS SUGGÉRÉS

Pour {{your_stats}} :
- Vidéo dédiée : X€
- Intégration 60s : X€
- Mention : X€
- Pack 3 vidéos : X€

### RED FLAGS CONTRATS
- [Points à vérifier]
- [Clauses à négocier]`
  },

  'youtube-end-screen-cta': {
    fields: [
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'Ex: Comment créer un site web' },
      { name: 'next_video', type: 'text', label: 'Prochaine vidéo suggérée', placeholder: 'Titre de la vidéo à promouvoir' },
      { name: 'playlist', type: 'text', label: 'Playlist liée', placeholder: 'Nom de la playlist (optionnel)' },
      { name: 'cta_goal', type: 'select', label: 'Objectif principal', options: ['Abonnement', 'Autre vidéo', 'Playlist', 'Site externe', 'Membership'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Enthousiaste', 'Décontracté', 'Professionnel', 'Urgence légère'] },
    ],
    promptTemplate: `Tu es expert en rétention et conversion YouTube.

VIDÉO : {{video_topic}}
PROCHAINE VIDÉO : {{next_video}}
PLAYLIST : {{playlist}}
OBJECTIF : {{cta_goal}}
TON : {{tone}}

## 🔚 Scripts d'Écran de Fin

### SCRIPT 1 - Classique (20 sec)

**[Timestamp : -20s]**

"[Transition du contenu]"

"[CTA Abonnement]"
→ Pointer vers bouton

"[CTA Vidéo suivante]"
→ Pointer vers vidéo

"[Signature]"

---

### SCRIPT 2 - Teaser (20 sec)

"[Teaser mystérieux de la prochaine vidéo]"

"[CTA urgent]"

"[Signature courte]"

---

### SCRIPT 3 - Récap + CTA (20 sec)

"[Récap valeur de cette vidéo]"

"[Promesse prochaine vidéo]"

"[Double CTA]"

---

### OPTIMISATION ÉCRAN DE FIN

**Placement optimal des éléments :**
- Position vidéo suggérée : [gauche/droite]
- Position abonnement : [position]
- Zone de texte safe : [dimensions]

**Timing :**
- Durée recommandée : 20 secondes
- Ne pas parler pendant : dernières 5 sec

**A/B Test suggéré :**
- Variante A : [description]
- Variante B : [description]`
  },

  'youtube-poll-ideas': {
    fields: [
      { name: 'channel_niche', type: 'text', label: 'Niche de votre chaîne', required: true, placeholder: 'Ex: Tech, Fitness, Cuisine...' },
      { name: 'poll_goal', type: 'select', label: 'Objectif du sondage', options: ['Décider prochain contenu', 'Connaître l\'audience', 'Engagement fun', 'Feedback produit', 'Débat/Opinion'] },
      { name: 'audience_type', type: 'select', label: 'Type d\'audience', options: ['Débutants', 'Intermédiaires', 'Experts', 'Mixte', 'Jeunes (13-18)', 'Adultes (25-40)'] },
      { name: 'current_topic', type: 'text', label: 'Sujet actuel sur la chaîne', placeholder: 'De quoi parlez-vous en ce moment?' },
      { name: 'polls_count', type: 'number', label: 'Nombre de sondages', placeholder: '5' },
    ],
    promptTemplate: `Tu es expert en engagement communautaire YouTube.

NICHE : {{channel_niche}}
OBJECTIF : {{poll_goal}}
AUDIENCE : {{audience_type}}
SUJET ACTUEL : {{current_topic}}

## 📊 {{polls_count}} Idées de Sondages YouTube

### Sondage 1 : [Type]

**Question :**
"[Question engageante]"

**Options :**
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]

**Pourquoi ça fonctionne :**
[Explication]

**Meilleur moment pour poster :**
[Timing]

---

### Sondage 2 : [Type]
[Même structure...]

---

[Répéter pour tous les sondages]

---

### TYPES DE SONDAGES QUI MARCHENT

| Type | Engagement | Quand utiliser |
|------|------------|----------------|
| This or That | ⭐⭐⭐⭐⭐ | Toujours |
| Opinion | ⭐⭐⭐⭐ | Débats |
| Quiz | ⭐⭐⭐ | Éducation |
| Décision contenu | ⭐⭐⭐⭐ | Avant vidéo |

### CONSEILS SONDAGES
- Fréquence optimale : X/semaine
- Durée du sondage : 24-48h
- Comment exploiter les résultats`
  },

  // ===== BATCH 3 - MEDIUM PRIORITY (5 outils) =====
  'voiceover-script': {
    fields: [
      { name: 'video_type', type: 'select', label: 'Type de vidéo', required: true, options: ['Documentaire', 'Tutoriel', 'Explainer', 'Narration histoire', 'Product review', 'News/Actualité'] },
      { name: 'topic', type: 'text', label: 'Sujet', required: true, placeholder: 'Ex: L\'histoire de SpaceX' },
      { name: 'duration', type: 'select', label: 'Durée cible', options: ['2-3 minutes', '5-7 minutes', '10-15 minutes', '20+ minutes'] },
      { name: 'tone', type: 'select', label: 'Ton de la voix off', options: ['Narrateur documentaire', 'Énergique YouTube', 'Calme ASMR', 'Professionnel corporate', 'Storytelling dramatique'] },
      { name: 'key_points', type: 'textarea', label: 'Points clés à couvrir', required: true, placeholder: 'Les informations essentielles à transmettre...' },
    ],
    promptTemplate: `Tu es scriptwriter voix off professionnel pour chaînes YouTube documentaires.

TYPE : {{video_type}}
SUJET : {{topic}}
DURÉE : {{duration}}
TON : {{tone}}
POINTS CLÉS : {{key_points}}

## 🎙️ Script Voix Off Complet

### INFORMATIONS TECHNIQUES
- Durée estimée : {{duration}}
- Mots : ~XXX (150 mots/minute)
- Ton : {{tone}}

---

### SCRIPT

**[INTRO - 0:00]**
[Accroche narrative]

---

**[SECTION 1 - Timestamp]**
[Narration avec indications de pause]

*[Note B-roll : suggestion visuelle]*

---

**[SECTION 2 - Timestamp]**
[Suite de la narration]

*[Note musique : changement d'ambiance]*

---

[Continuer pour toutes les sections]

---

**[CONCLUSION - Timestamp]**

[Conclusion mémorable]

---

### NOTES DE PRODUCTION

**Rythme :**
- Pauses suggérées : [indications]
- Moments d'emphase : [indications]

**Musique suggérée :**
- Intro : [style]
- Corps : [style]
- Climax : [style]
- Outro : [style]

**Effets sonores :**
- [Suggestions SFX]`
  },

  'youtube-analytics-interpreter': {
    fields: [
      { name: 'metric_type', type: 'select', label: 'Métrique à analyser', required: true, options: ['Views & Watch Time', 'CTR & Impressions', 'Audience Retention', 'Traffic Sources', 'Demographics', 'Revenue', 'Subscribers'] },
      { name: 'current_value', type: 'text', label: 'Valeur actuelle', required: true, placeholder: 'Ex: CTR 4.5%, Retention 45%...' },
      { name: 'trend', type: 'select', label: 'Tendance', options: ['En hausse', 'Stable', 'En baisse', 'Volatile'] },
      { name: 'comparison_period', type: 'select', label: 'Période de comparaison', options: ['7 derniers jours', '28 derniers jours', '90 derniers jours', 'Année'] },
      { name: 'channel_size', type: 'select', label: 'Taille de la chaîne', options: ['< 1K', '1K-10K', '10K-100K', '100K-1M', '1M+'] },
    ],
    promptTemplate: `Tu es data analyst YouTube certifié avec accès aux benchmarks de l'industrie.

MÉTRIQUE : {{metric_type}}
VALEUR : {{current_value}}
TENDANCE : {{trend}}
PÉRIODE : {{comparison_period}}
TAILLE CHAÎNE : {{channel_size}}

## 📈 Analyse de Métrique YouTube

### 1. INTERPRÉTATION DE VOS DONNÉES

**Métrique analysée :** {{metric_type}}
**Votre valeur :** {{current_value}}

**Benchmark industrie (chaînes {{channel_size}}) :**
- Excellent : X%
- Bon : X%
- Moyen : X%
- À améliorer : X%

**Votre position :** [Évaluation]

---

### 2. DIAGNOSTIC

**Pourquoi cette valeur ?**
- Facteur 1 : [explication]
- Facteur 2 : [explication]
- Facteur 3 : [explication]

**Tendance {{trend}} expliquée :**
[Analyse de la tendance]

---

### 3. IMPACT SUR VOTRE CHAÎNE

**Si vous ne changez rien :**
- Court terme : [projection]
- Long terme : [projection]

**Vidéos les plus impactées :**
- [Type de vidéo 1]
- [Type de vidéo 2]

---

### 4. PLAN D'AMÉLIORATION

**Actions immédiates (cette semaine) :**
1. [Action 1]
2. [Action 2]

**Actions moyen terme (ce mois) :**
1. [Action 1]
2. [Action 2]

**Objectif réaliste :**
- Dans 30 jours : {{metric_type}} = X
- Dans 90 jours : {{metric_type}} = X

---

### 5. MÉTRIQUES LIÉES À SURVEILLER
| Métrique | Corrélation | Pourquoi |
|----------|-------------|----------|
| ... | ... | ... |`
  },

  'youtube-ab-test-titles': {
    fields: [
      { name: 'original_title', type: 'text', label: 'Titre original', required: true, placeholder: 'Votre titre actuel' },
      { name: 'video_topic', type: 'text', label: 'Sujet de la vidéo', required: true, placeholder: 'De quoi parle la vidéo' },
      { name: 'current_ctr', type: 'text', label: 'CTR actuel (%)', placeholder: 'Ex: 4.5%' },
      { name: 'target_audience', type: 'text', label: 'Audience cible', placeholder: 'Qui regarde vos vidéos' },
      { name: 'test_variants', type: 'number', label: 'Nombre de variantes', placeholder: '5' },
    ],
    promptTemplate: `Tu es growth hacker YouTube spécialisé en optimisation de CTR.

TITRE ORIGINAL : {{original_title}}
SUJET : {{video_topic}}
CTR ACTUEL : {{current_ctr}}
AUDIENCE : {{target_audience}}

## 🧪 A/B Test de Titres YouTube

### ANALYSE DU TITRE ACTUEL

**Titre :** "{{original_title}}"

**Score actuel : X/10**

| Critère | Score | Commentaire |
|---------|-------|-------------|
| Clarté | X/10 | ... |
| Curiosité | X/10 | ... |
| Mots-clés | X/10 | ... |
| Longueur | X/10 | ... |
| Power words | X/10 | ... |

**Problèmes identifiés :**
1. [Problème 1]
2. [Problème 2]

---

### {{test_variants}} VARIANTES À TESTER

**Variante A - [Stratégie]**
"[Nouveau titre]"
- Changement : [ce qui change]
- CTR prévu : +X%
- Score : X/10

**Variante B - [Stratégie]**
"[Nouveau titre]"
- Changement : [ce qui change]
- CTR prévu : +X%
- Score : X/10

[Répéter pour toutes les variantes]

---

### PROTOCOLE DE TEST

**Durée recommandée :** 48-72h par variante

**Métriques à suivre :**
- CTR (impressions → clics)
- AVD (durée moyenne de visionnage)
- Retention début (30 premières secondes)

**Quand garder un titre :**
- CTR > X% ET AVD stable

**Outils suggérés :**
- TubeBuddy A/B Test
- VidIQ
- Changement manuel + suivi

---

### RECOMMANDATION FINALE
**Meilleur titre prédit :** Variante [X]
**Raison :** [Explication]`
  },

  'youtube-niche-finder': {
    fields: [
      { name: 'interests', type: 'textarea', label: 'Vos centres d\'intérêt', required: true, placeholder: 'Tech, cuisine, voyage, gaming, fitness...' },
      { name: 'skills', type: 'textarea', label: 'Vos compétences', required: true, placeholder: 'Montage vidéo, parler en public, expertise dans...' },
      { name: 'target_audience', type: 'select', label: 'Audience souhaitée', options: ['Francophone', 'Anglophone', 'Arabophone', 'Algérie/Maghreb', 'International'] },
      { name: 'competition_preference', type: 'select', label: 'Niveau de compétition accepté', options: ['Très faible (micro-niche)', 'Faible', 'Moyen', 'Élevé (grosse niche)'] },
      { name: 'monetization_goal', type: 'select', label: 'Objectif de monétisation', options: ['AdSense uniquement', 'Sponsors', 'Produits digitaux', 'Services', 'Tout'] },
    ],
    promptTemplate: `Tu es stratège YouTube ayant lancé 50+ chaînes rentables dans différentes niches.

INTÉRÊTS : {{interests}}
COMPÉTENCES : {{skills}}
AUDIENCE : {{target_audience}}
COMPÉTITION : {{competition_preference}}
MONÉTISATION : {{monetization_goal}}

## 🎯 Analyse de Niches YouTube

### NICHES RECOMMANDÉES POUR VOUS

#### Niche 1 : [Nom de la niche]

**Adéquation avec votre profil : X/10**

| Critère | Score |
|---------|-------|
| Passion | ⭐⭐⭐⭐⭐ |
| Compétence | ⭐⭐⭐⭐ |
| Demande | ⭐⭐⭐⭐ |
| Compétition | ⭐⭐⭐ |
| Monétisation | ⭐⭐⭐⭐⭐ |

**Analyse du marché :**
- Volume de recherche : X/mois
- Chaînes leaders : [exemples]
- Gap à exploiter : [opportunité]

**Sous-niches recommandées :**
1. [Sous-niche 1]
2. [Sous-niche 2]
3. [Sous-niche 3]

**Potentiel de revenus :**
- CPM moyen : X€
- Sponsors potentiels : [types]
- Produits possibles : [idées]

**10 premières vidéos suggérées :**
1. [Titre 1]
2. [Titre 2]
...

---

#### Niche 2 : [Nom de la niche]
[Même structure...]

---

#### Niche 3 : [Nom de la niche]
[Même structure...]

---

### MATRICE DE DÉCISION

| Niche | Passion | Potentiel | Difficulté | Score final |
|-------|---------|-----------|------------|-------------|
| 1 | ... | ... | ... | X/30 |
| 2 | ... | ... | ... | X/30 |
| 3 | ... | ... | ... | X/30 |

### MA RECOMMANDATION
**Meilleure niche pour vous :** [Niche X]
**Pourquoi :** [Explication]
**Premier pas :** [Action concrète]`
  },

  'youtube-upload-checklist': {
    fields: [
      { name: 'video_title', type: 'text', label: 'Titre de la vidéo', required: true, placeholder: 'Titre de votre vidéo' },
      { name: 'video_type', type: 'select', label: 'Type de vidéo', options: ['Standard (8-20 min)', 'Long format (20+ min)', 'Short', 'Première/Live', 'Série'] },
      { name: 'target_keyword', type: 'text', label: 'Mot-clé principal', required: true, placeholder: 'Ex: apprendre python' },
      { name: 'publishing_time', type: 'text', label: 'Heure de publication prévue', placeholder: 'Ex: Samedi 14h' },
      { name: 'promotion_channels', type: 'select', label: 'Canaux de promotion', options: ['YouTube uniquement', 'YouTube + Instagram', 'YouTube + TikTok', 'Tous les réseaux', 'Newsletter aussi'] },
    ],
    promptTemplate: `Tu es YouTuber professionnel avec un process de publication rodé.

TITRE : {{video_title}}
TYPE : {{video_type}}
MOT-CLÉ : {{target_keyword}}
PUBLICATION : {{publishing_time}}
PROMOTION : {{promotion_channels}}

## ✅ Checklist Publication YouTube Complète

### PRÉ-UPLOAD (24h avant)

**Vidéo :**
- [ ] Export final vérifié (pas de bug audio/vidéo)
- [ ] Résolution : 1080p minimum (4K si possible)
- [ ] Nom de fichier : {{target_keyword}}.mp4
- [ ] Durée vérifiée : [X minutes]

**Miniature :**
- [ ] 1280x720 pixels
- [ ] < 2MB
- [ ] Test de lisibilité mobile
- [ ] A/B variantes prêtes

**Textes préparés :**
- [ ] Titre optimisé (< 60 caractères)
- [ ] Description (2000+ caractères)
- [ ] Tags (500 caractères max)

---

### PENDANT L'UPLOAD

**Métadonnées YouTube Studio :**
- [ ] Titre : "{{video_title}}"
- [ ] Description : [coller]
- [ ] Miniature : [uploader]
- [ ] Playlist : [sélectionner]
- [ ] Catégorie : [choisir]
- [ ] Tags : [ajouter]
- [ ] Langue : [sélectionner]
- [ ] Licence : YouTube standard
- [ ] Sous-titres : [uploader si disponibles]

**Visibilité :**
- [ ] Programmer pour : {{publishing_time}}
- [ ] Première activée : [Oui/Non]
- [ ] Notify subscribers : [Oui]

**Écran de fin :**
- [ ] Vidéo suggérée ajoutée
- [ ] Bouton abonnement placé
- [ ] Playlist liée (optionnel)

**Cards :**
- [ ] Card vidéo liée à [timestamp]
- [ ] Card playlist (optionnel)

---

### POST-PUBLICATION (dans l'heure)

**Engagement initial :**
- [ ] Commenter en premier (épingler)
- [ ] Répondre aux 10 premiers commentaires
- [ ] Liker les commentaires pertinents

**Promotion ({{promotion_channels}}) :**
- [ ] Story Instagram avec lien
- [ ] Post communauté YouTube
- [ ] Tweet/Thread Twitter
- [ ] TikTok teaser (si applicable)
- [ ] Newsletter (si applicable)

---

### SUIVI (24-48h après)

**Métriques à vérifier :**
- [ ] CTR (> 4% = bon)
- [ ] AVD (> 50% = excellent)
- [ ] Commentaires (répondre)
- [ ] Impressions

**Ajustements si nécessaire :**
- [ ] Changer miniature si CTR < 3%
- [ ] Modifier titre si impressions faibles
- [ ] Ajouter cards si rétention chute

---

### NOTES SPÉCIFIQUES À CETTE VIDÉO
[Espace pour notes personnelles]`
  },
};

// Config par défaut pour les outils sans config spécifique
const defaultFormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez générer...' },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Décontracté', 'Énergique', 'Éducatif'] },
    { name: 'language', type: 'select', label: 'Langue', options: ['Français', 'Arabe', 'Anglais', 'Darija'] },
  ],
  promptTemplate: `Génère du contenu YouTube basé sur cette demande...`
};

export default function YouTubeToolPage({ params }: PageProps) {
  const tool = youtubeTools.find(t => t.slug === params.toolSlug);
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
          <Link href="/tools/youtube" className="text-red-600 hover:underline">
            Retour aux outils YouTube
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

    // Simulation API - En production, appeler le gateway
    setTimeout(() => {
      const mockResult = `# Résultat généré par ${tool.name.fr}

## Contenu Généré

Voici le contenu généré basé sur vos paramètres:

${Object.entries(formData).map(([key, value]) => `**${key}**: ${value}`).join('\n')}

---

### Résultat Principal

Ce contenu a été généré par l'IA d'IAFactory Algeria pour optimiser votre présence YouTube.

### Points Clés

1. **Optimisation SEO** : Contenu optimisé pour l'algorithme YouTube
2. **Engagement** : Formulations conçues pour maximiser l'interaction
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/youtube" className="text-gray-400 hover:text-gray-600">
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
                <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <Youtube className="w-6 h-6 text-red-600" />
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
            <div className="bg-red-50 text-red-700 px-4 py-2 rounded-lg font-semibold text-lg">
              {tool.credits} crédits
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-red-600" />
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
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 transition resize-none"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      name={field.name}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 transition"
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
                        className="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                        checked={formData[field.name] === 'true'}
                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.checked ? 'true' : 'false' })}
                      />
                      <span className="text-sm text-gray-600">{field.label}</span>
                    </label>
                  ) : field.type === 'number' ? (
                    <input
                      type="number"
                      name={field.name}
                      placeholder={field.placeholder}
                      min={field.min}
                      max={field.max}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  ) : (
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      required={field.required}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 transition"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    />
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-red-600 transition px-3 py-1 rounded-lg hover:bg-gray-50"
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
                    <Loader2 className="w-8 h-8 text-red-600 animate-spin mx-auto mb-2" />
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
                    <Youtube className="w-12 h-12 mx-auto mb-2 opacity-30" />
                    <p>Le résultat apparaîtra ici</p>
                    <p className="text-sm mt-1">Remplissez le formulaire et cliquez sur Générer</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-6 bg-red-50 rounded-xl p-6 border border-red-100">
          <h3 className="font-semibold text-red-900 mb-2">Conseils pour de meilleurs résultats</h3>
          <ul className="text-sm text-red-800 space-y-1">
            <li>• Soyez précis dans la description de votre contenu vidéo</li>
            <li>• Utilisez des mots-clés pertinents pour votre niche YouTube</li>
            <li>• Testez différentes formulations pour trouver ce qui engage le plus</li>
            <li>• Adaptez toujours le résultat à votre style et votre audience</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
