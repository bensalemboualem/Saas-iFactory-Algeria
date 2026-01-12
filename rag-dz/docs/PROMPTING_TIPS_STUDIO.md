# 💡 Guide de Prompting - Studio Créatif IA Factory

> **Conseils et astuces pour une utilisation optimale du Studio Créatif**

Basé sur les bonnes pratiques Abacus.AI, adapté pour IA Factory Algeria.

---

## 🎯 Principes Généraux

### 1. Soyez Clair et Spécifique

Plus votre demande est détaillée, meilleure sera la réponse.

**❌ Mauvais:**
```
"Créer une vidéo"
```

**✅ Bon:**
```
"Créer une vidéo de 30 secondes sur le tourisme dans le Sahara algérien au coucher du soleil,
style cinématique, format vertical 9:16 pour TikTok"
```

### 2. Utilisez un Langage Simple

Évitez les formulations trop complexes. Restez direct.

**❌ Mauvais:**
```
"Générer une représentation visuelle sophistiquée incorporant des éléments de design moderne"
```

**✅ Bon:**
```
"Créer un logo moderne pour une startup tech"
```

### 3. Fournissez du Contexte

Donnez suffisamment de contexte pour aider l'IA à générer des réponses précises.

**❌ Mauvais:**
```
"Écrire un email"
```

**✅ Bon:**
```
"Écrire un email marketing pour une nouvelle application de fitness
ciblant les jeunes professionnels algériens, ton enthousiaste et motivant"
```

### 4. Itérez et Affinez

Si la réponse n'est pas celle attendue, affinez votre question ou ajoutez des détails.

**Première tentative:**
```
"Résumer les avantages de l'énergie renouvelable"
```

**Raffinement:**
```
"Résumer les avantages de l'énergie renouvelable en Algérie.
Focus sur l'énergie solaire dans le sud et l'éolien dans les Hauts Plateaux"
```

### 5. Demandez des Exemples

En cas de doute, demandez à l'IA de fournir des exemples.

```
"Donne-moi 3 exemples de posts LinkedIn engageants pour promouvoir un hackathon à Alger"
```

### 6. Décomposez les Tâches Complexes

Pour des demandes complexes, divisez-les en étapes gérables.

**Étape 1:**
```
"Génère un plan pour une présentation sur l'IA en Algérie (5 slides)"
```

**Étape 2:**
```
"Maintenant, rédige le contenu de la slide 1 : Introduction"
```

---

## 🎨 Prompting par Outil

### 🎬 Video-Gen

**Structure Recommandée:**
```
[Type de vidéo] + [Sujet] + [Style] + [Durée] + [Format] + [Destination]
```

**Exemples:**

```
"Vidéo promotionnelle sur les startups algériennes, style moderne et dynamique,
30 secondes, format vertical, pour Instagram Reels"
```

```
"Clip animé expliquant la blockchain en arabe algérien (darija),
style pédagogique avec icônes, 60 secondes, 16:9, pour YouTube"
```

```
"Time-lapse du coucher de soleil à Tipaza, style cinématique 4K,
15 secondes, horizontal, pour campagne touristique"
```

**Mots-clés de détection:**
- `vidéo`, `video`, `clip`, `film`, `montage`, `animation`

---

### 🖼️ Image Generation

**Structure Recommandée:**
```
[Type d'image] + [Sujet] + [Style artistique] + [Couleurs] + [Ambiance] + [Ratio]
```

**Exemples:**

```
"Logo minimaliste pour une entreprise de cybersécurité algérienne,
couleurs bleu et vert, moderne et professionnel, fond transparent"
```

```
"Illustration d'un marché traditionnel algérien, style aquarelle,
couleurs chaudes (rouge, orange, jaune), ambiance vivante, ratio 16:9"
```

```
"Photo-réaliste d'un plat de couscous algérien, éclairage naturel,
fond bois rustique, style food photography, haute résolution"
```

**Mots-clés de détection:**
- Par défaut si aucun autre type détecté
- `image`, `photo`, `illustration`, `logo`, `design`

---

### 📊 Powerpoint Generation

**Structure Recommandée:**
```
[Sujet] + [Nombre de slides] + [Public cible] + [Ton] + [Structure]
```

**Exemples:**

```
"Présentation sur l'Intelligence Artificielle en Algérie,
10 slides, pour investisseurs, ton professionnel,
structure: Introduction > État des lieux > Opportunités > Conclusion"
```

```
"Pitch deck pour startup fintech algérienne, 8 slides, pour incubateurs,
ton dynamique, inclure: Problème > Solution > Marché > Business Model > Équipe"
```

```
"Formation sur la cybersécurité, 15 slides, pour PME algériennes,
ton pédagogique, avec exemples concrets et bonnes pratiques"
```

**Mots-clés de détection:**
- `présentation`, `powerpoint`, `slides`, `ppt`, `pitch deck`, `diapo`

---

### 💻 Code Generation

**Structure Recommandée:**
```
[Action] + [Langage] + [Fonctionnalité] + [Contexte] + [Bonnes pratiques]
```

**Exemples:**

```
"Créer une fonction Python pour analyser des logs système,
extraire les erreurs et les sauvegarder en JSON,
avec gestion d'exceptions et commentaires"
```

```
"Écrire un script JavaScript pour valider un formulaire de contact,
vérifier email et téléphone algérien (+213),
utiliser regex et retourner messages d'erreur en français"
```

```
"Générer une API REST FastAPI pour gérer des utilisateurs (CRUD),
avec authentification JWT, validation Pydantic,
et documentation Swagger automatique"
```

**Mots-clés de détection:**
- `code`, `fonction`, `script`, `programme`, `API`, `class`

---

### 🔬 Deep Research

**Structure Recommandée:**
```
[Sujet de recherche] + [Profondeur] + [Sources] + [Format de sortie]
```

**Exemples:**

```
"Recherche approfondie sur l'écosystème des startups tech en Algérie,
analyser les 5 dernières années, sources: rapports officiels + presse locale,
format: rapport structuré avec graphiques"
```

```
"Analyser les opportunités d'IA dans le secteur agricole algérien,
focus sur le sud, inclure études de cas internationales adaptables,
synthèse exécutive + recommandations"
```

```
"Explorer les tendances du e-commerce en Algérie post-COVID,
comparer avec les pays du Maghreb,
rapport avec données chiffrées et prévisions 2025"
```

**Mots-clés de détection:**
- `recherche`, `analyser`, `explorer`, `étudier`, `investigation`

---

### 🎤 Text-to-Speech

**Structure Recommandée:**
```
[Texte] + [Langue] + [Voix] + [Émotion] + [Vitesse]
```

**Exemples:**

```
"Convertir ce texte en audio: 'Bienvenue sur IA Factory Algeria',
en français avec accent algérien, voix féminine professionnelle,
ton chaleureux, vitesse normale"
```

```
"Générer voix-off pour vidéo promotionnelle (script joint),
en arabe standard, voix masculine dynamique,
ton enthousiaste et motivant, légèrement rapide"
```

```
"Créer narration pour podcast tech (texte de 500 mots),
en français, voix neutre professionnelle,
ton informatif et posé, vitesse moyenne"
```

**Mots-clés de détection:**
- `audio`, `voix`, `parler`, `narration`, `voice-over`, `TTS`

---

### 📄 Doc-Gen

**Structure Recommandée:**
```
[Type de document] + [Contenu] + [Format] + [Ton] + [Sections]
```

**Exemples:**

```
"Générer un rapport d'activité annuel, pour entreprise IT,
format PDF professionnel, ton formel,
sections: Chiffres clés > Projets > Équipe > Perspectives"
```

```
"Créer une proposition commerciale pour service cloud,
destinée aux PME algériennes, format Word,
ton convaincant mais accessible, 10 pages max"
```

```
"Rédiger un guide utilisateur pour application mobile,
en français simplifié avec captures d'écran,
format PDF interactif, ton pédagogique"
```

---

### 🌐 Scrape URL

**Structure Recommandée:**
```
[URL] + [Type de données] + [Format sortie]
```

**Exemples:**

```
"Extraire tous les articles de https://example.com/blog,
récupérer titres + dates + premiers paragraphes,
format JSON structuré"
```

```
"Scraper les prix des produits sur https://shop.dz/electronics,
comparer avec prix de la semaine dernière,
tableau Excel comparatif"
```

```
"Analyser la structure de navigation de https://competitor.dz,
extraire menu principal + sous-menus,
diagramme hiérarchique"
```

---

### ⭕ Humanize

**Tons Disponibles:**

#### 💼 Professionnel
```
"Humaniser ce texte IA en ton professionnel:
'L'intelligence artificielle révolutionne le secteur bancaire...'
(garder les faits, adoucir le style robot)"
```

#### 😄 Humoristique
```
"Convertir ce texte technique en version humoristique mais informative:
'Le cloud computing permet de...'
(ajouter analogies drôles, garder précision)"
```

#### 💝 Caring (Empathique)
```
"Réécrire ce message client en ton empathique et rassurant:
'Votre demande a été traitée...'
(personnaliser, montrer compréhension)"
```

---

## 🎯 Exemples Avancés par Cas d'Usage

### 📱 Campagne Social Media Complète

**Prompt Multi-étapes:**

```
1. "Créer 3 visuels Instagram pour lancement d'app mobile algérienne,
   style moderne coloré, format carré, thème: innovation locale"

2. "Rédiger 3 captions en français pour ces visuels,
   ton enthousiaste, avec emojis, call-to-action téléchargement"

3. "Générer vidéo teaser 15s pour TikTok,
   montrer features app en motion design, musique dynamique"

4. "Planifier calendrier publication 2 semaines,
   meilleurs créneaux pour audience algérienne 18-35 ans"
```

### 🏢 Pitch Startup Complet

```
1. "Générer pitch deck 10 slides pour startup edtech algérienne,
   focus: apprentissage personnalisé IA,
   public: investisseurs VCs africains"

2. "Créer script de pitch 3 minutes basé sur ce deck,
   ton confiant et data-driven,
   inclure: hook > problème > solution > traction > demande"

3. "Générer démo vidéo produit 60s,
   montrer interface utilisateur, style tutoriel rapide"

4. "Rédiger one-pager exécutif (1 page A4),
   résumer l'essentiel, design attractif"
```

### 📰 Article de Blog SEO-Optimisé

```
1. "Rechercher tendances actuelles sur 'IA et éducation en Algérie',
   analyser 10 articles récents,
   identifier mots-clés principaux"

2. "Rédiger article 1500 mots: 'Comment l'IA Transforme l'Éducation en Algérie',
   structure: intro > 5 sections > conclusion,
   ton informatif et accessible,
   inclure stats locales et exemples concrets"

3. "Générer 3 images d'illustration pour l'article,
   style moderne éducatif, couleurs Algérie (vert/blanc/rouge touches)"

4. "Créer meta description SEO (160 caractères),
   5 tags pertinents,
   3 suggestions de titres alternatifs"
```

---

## 🚀 Optimisations Spéciales

### Pour la Génération Vidéo (Sora 2, Veo 3)

**Ajoutez ces détails:**
- **Mouvement caméra**: "travelling avant", "plan fixe", "drone vue aérienne"
- **Lighting**: "golden hour", "éclairage studio", "lumière naturelle"
- **Style**: "cinématique", "documentaire", "publicitaire", "minimaliste"
- **Transitions**: "cut rapide", "fondu", "wipe"

**Exemple complet:**
```
"Vidéo promotionnelle startup algérienne,
bureaux modernes à Alger, équipe collaborative multiculturelle,
travelling latéral fluide, éclairage naturel fenêtre,
style cinématique corporate, transitions fondus,
musique inspirante background, 30s, 4K, 16:9"
```

### Pour la Génération Image (FLUX Pro, DALL-E)

**Ajoutez ces détails:**
- **Perspective**: "vue frontale", "angle bas", "isométrique", "bird's eye view"
- **Texture**: "détaillé", "lisse", "texturé", "minimaliste"
- **Profondeur**: "bokeh background", "tout net", "profondeur de champ"
- **Post-processing**: "HDR", "contraste élevé", "couleurs saturées"

**Exemple complet:**
```
"Logo startup fintech algérienne 'DinarPay',
symbole fusion croissant islamique + graphique montant,
style minimaliste moderne, couleurs vert émeraude + or,
géométrie sacrée subtile, fond transparent,
vectoriel haute résolution, adaptable noir/blanc"
```

---

## ⚡ Raccourcis & Templates

### Templates Prêts à l'Emploi

#### 1. Template Marketing
```
TYPE: [Email/Post/Vidéo]
PRODUIT: [Nom + description courte]
CIBLE: [Persona détaillée]
TON: [Professionnel/Décontracté/Urgent]
CTA: [Action souhaitée]
FORMAT: [Longueur/Durée]
```

#### 2. Template Technique
```
OBJECTIF: [Que doit faire le code]
LANGAGE: [Python/JS/etc.]
INPUTS: [Type et format]
OUTPUTS: [Type et format attendu]
CONTRAINTES: [Performance/Sécurité/etc.]
STYLE: [Commenté/Clean/Optimisé]
```

#### 3. Template Contenu
```
SUJET: [Thème précis]
ANGLE: [Perspective unique]
FORMAT: [Article/Vidéo/Présentation]
LONGUEUR: [Mots/Minutes/Slides]
SOURCES: [Données à inclure]
TON: [Style d'écriture]
```

---

## 🎓 Bonnes Pratiques Avancées

### 1. Utiliser le Contexte Local Algérien

**✅ À faire:**
- Mentionner "Algérie", "algérien", "DZ"
- Utiliser exemples locaux (villes, entreprises connues)
- Préciser langues (FR, AR, Darija, Tamazight)
- Adapter aux fuseaux horaires (UTC+1)

**Exemple:**
```
"Créer calendrier contenu Ramadan 2025 pour e-commerce algérien,
adapter horaires publication au jeûne,
ton respectueux traditions + moderne,
mix français et arabe selon type contenu"
```

### 2. Combiner Plusieurs Outils

**Workflow type:**
```
1. Deep Research → Trouver insights
2. Doc-Gen → Structurer rapport
3. Image Gen → Créer visuels
4. Powerpoint → Assembler présentation
5. Video-Gen → Créer teaser
6. Publication → Diffuser multi-canal
```

### 3. Itération Progressive

**Première génération (large):**
```
"Créer campagne lancement produit"
```

**Raffinement 1:**
```
"Campagne lancement app mobile livraison Alger, cible jeunes 20-35 ans"
```

**Raffinement 2:**
```
"Campagne lancement app livraison rapide Alger,
cible urbains actifs 20-35 ans,
différenciation: livraison sous 30min garantie,
canaux: Instagram + TikTok + Facebook,
budget limité,
durée: 2 semaines pré-lancement + 1 mois post"
```

---

## 📊 Checklist de Qualité

Avant de soumettre votre prompt, vérifiez:

- [ ] **Objectif clair**: Je sais exactement ce que je veux
- [ ] **Contexte fourni**: J'ai donné les infos nécessaires
- [ ] **Format précisé**: Durée/Longueur/Dimensions indiquées
- [ ] **Public défini**: Je connais ma cible
- [ ] **Ton spécifié**: Style d'écriture/voix claire
- [ ] **Exemples donnés**: (Si applicable) J'ai fourni des références
- [ ] **Contraintes listées**: Limitations techniques/budgétaires mentionnées

---

## 🆘 Troubleshooting

### Problème: Résultat pas assez spécifique

**Solution:** Ajoutez 3-5 détails supplémentaires

**Avant:**
```
"Créer une vidéo de présentation"
```

**Après:**
```
"Créer vidéo présentation entreprise IT algérienne,
montrer bureaux + équipe + réalisations,
style corporate moderne,
musique instrumentale légère,
sous-titres français,
45 secondes,
format LinkedIn (carré)"
```

### Problème: Mauvaise détection d'outil

**Solution:** Utilisez les mots-clés de détection explicitement

**Au lieu de:**
```
"Je veux quelque chose sur le tourisme"
```

**Utilisez:**
```
"Créer une VIDÉO promotionnelle sur le tourisme saharien" (→ Video-Gen)
"Générer une IMAGE affiche tourisme Sahara" (→ Image)
"Rédiger PRÉSENTATION PowerPoint tourisme algérien" (→ Powerpoint)
```

### Problème: Résultat trop générique

**Solution:** Ajoutez des contraintes uniques

**Exemple:**
```
"Logo pour restaurant,
MAIS: fusion cuisine algérienne-japonaise,
symboliser pont culturel,
éviter clichés (pas de tour Eiffel, pas de drapeau),
inspiration: calligraphie arabe + minimalisme japonais,
couleurs: bleu nuit + cuivre"
```

---

## 🎯 Exemples par Secteur

### 🏦 Fintech
```
"Créer infographie explicative sur le paiement mobile en Algérie,
comparer 3 solutions (CIB, Baridi Mob, Flexy),
style moderne et pédagogique,
données 2024,
format vertical Instagram"
```

### 🎓 Education
```
"Générer cours interactif sur la programmation Python,
niveau débutant lycéen algérien,
10 modules progressifs,
exemples contextualisés (DZ),
mix vidéos courtes + exercices,
français simplifié"
```

### 🏥 Santé
```
"Créer campagne sensibilisation diabète pour Algérie,
focus prévention et dépistage,
ton empathique non culpabilisant,
visuels inclusifs familles algériennes,
adaptation Ramadan,
multi-format (affiches + vidéos + posts)"
```

### 🛍️ E-commerce
```
"Générer descriptions produits optimisées SEO,
pour boutique mode algérienne en ligne,
ton moderne et local,
inclure: caractéristiques + bénéfices + sizing local,
français et darija mixé naturellement,
CTA adapté marché DZ"
```

---

## 🚀 Pro Tips

1. **Soyez spécifique sur les langues**
   - "Français standard" vs "Français avec expressions algériennes"
   - "Arabe littéraire" vs "Darija algéroise"

2. **Précisez toujours le format final**
   - Vertical (9:16) ≠ Horizontal (16:9) ≠ Carré (1:1)

3. **Mentionnez la plateforme de destination**
   - Instagram (esthétique) ≠ LinkedIn (pro) ≠ TikTok (viral)

4. **Donnez des références si possible**
   - "Style similaire à [marque/créateur connu]"

5. **Itérez sans hésiter**
   - Première version = base
   - Raffinements successifs = excellence

---

## 📚 Ressources Complémentaires

- **Guide Complet Studio**: `./STUDIO_CREATIF_GUIDE.md`
- **Quick Start**: `../STUDIO_README.md`
- **Documentation MCP**: `./MCP_SERVERS_GUIDE.md` (TODO)
- **Exemples Avancés**: `./ADVANCED_EXAMPLES.md` (TODO)

---

**Dernière mise à jour**: 2025-01-18
**Version**: 1.0.0

🇩🇿 **IA Factory Algeria - Prompting Intelligent pour Création de Qualité**

