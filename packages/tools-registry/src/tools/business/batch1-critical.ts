import { AITool } from '../../types';

export const businessPlanGenerator: AITool = {
  id: 'business-plan-generator',
  slug: 'business-plan-generator',
  name: { fr: 'Générateur de Business Plan', ar: 'مولد خطة العمل', en: 'Business Plan Generator' },
  description: {
    fr: 'Créez un business plan professionnel et complet en quelques minutes',
    ar: 'أنشئ خطة عمل احترافية وشاملة في دقائق',
    en: 'Create a professional and complete business plan in minutes'
  },
  category: 'business',
  subcategory: 'planning',
  icon: 'FileText',
  credits: 40,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'business_type', type: 'select', label: 'Type d\'activité', options: [
      'Produit physique',
      'Service',
      'SaaS/Digital',
      'E-commerce',
      'Restauration',
      'Commerce de détail'
    ]},
    { name: 'business_idea', type: 'textarea', label: 'Décrivez votre idée', required: true },
    { name: 'target_market', type: 'text', label: 'Marché cible' },
    { name: 'initial_investment', type: 'text', label: 'Investissement initial estimé' },
    { name: 'country', type: 'select', label: 'Pays', options: ['Algérie', 'France', 'Suisse', 'Maroc', 'Autre'] },
    { name: 'plan_purpose', type: 'select', label: 'Objectif du plan', options: ['Banque', 'Investisseurs', 'ANSEJ/CNAC', 'Interne', 'Partenaires'] }
  ],
  outputs: [{ type: 'markdown', name: 'business_plan' }],
  promptTemplate: `Tu es un consultant en stratégie d'entreprise avec 20 ans d'expérience.

ENTREPRISE : {{business_name}}
TYPE : {{business_type}}
IDÉE : {{business_idea}}
MARCHÉ : {{target_market}}
INVESTISSEMENT : {{initial_investment}}
PAYS : {{country}}
OBJECTIF : {{plan_purpose}}

## 📋 BUSINESS PLAN COMPLET

---

# BUSINESS PLAN
## {{business_name}}

**Date :** [Date]
**Porteur de projet :** [Nom]
**Contact :** [Email/Téléphone]

---

## TABLE DES MATIÈRES

1. Résumé Exécutif
2. Présentation du Projet
3. Étude de Marché
4. Stratégie Commerciale
5. Plan Opérationnel
6. Équipe & Organisation
7. Plan Financier
8. Annexes

---

## 1. RÉSUMÉ EXÉCUTIF

**L'entreprise :**
{{business_name}} est [description en 2-3 lignes].

**Le problème :**
[Problème identifié sur le marché]

**La solution :**
[Votre solution unique]

**Le marché :**
[Taille du marché, opportunité]

**Le modèle économique :**
[Comment vous gagnez de l'argent]

**Les besoins :**
- Investissement recherché : {{initial_investment}}
- Utilisation des fonds : [Répartition]

**Les projections :**
| Année | CA | Résultat |
|-------|-----|----------|
| N+1 | [X] | [X] |
| N+2 | [X] | [X] |
| N+3 | [X] | [X] |

---

## 2. PRÉSENTATION DU PROJET

### 2.1 L'idée
[Description détaillée]

### 2.2 Genèse du projet
[Origine de l'idée, motivation]

### 2.3 Vision & Mission
**Vision :** [Où voulez-vous aller]
**Mission :** [Comment y arriver]

### 2.4 Valeurs
- [Valeur 1]
- [Valeur 2]
- [Valeur 3]

### 2.5 Objectifs
**Court terme (1 an) :**
- [Objectif 1]
- [Objectif 2]

**Moyen terme (3 ans) :**
- [Objectif 1]
- [Objectif 2]

---

## 3. ÉTUDE DE MARCHÉ

### 3.1 Le marché
**Taille :** [TAM/SAM/SOM]
**Tendances :** [Évolutions]
**Croissance :** [% annuel]

### 3.2 La clientèle cible
**Segment principal :**
- Profil : [Description]
- Besoins : [Liste]
- Budget : [Fourchette]

**Persona type :**
[Description du client idéal]

### 3.3 La concurrence
| Concurrent | Forces | Faiblesses | Prix |
|------------|--------|------------|------|
| [Concurrent 1] | [+] | [-] | [€] |
| [Concurrent 2] | [+] | [-] | [€] |

### 3.4 Avantage concurrentiel
[Ce qui vous différencie]

### 3.5 Analyse SWOT
| Forces | Faiblesses |
|--------|------------|
| [+] | [-] |

| Opportunités | Menaces |
|--------------|---------|
| [+] | [-] |

---

## 4. STRATÉGIE COMMERCIALE

### 4.1 Offre produit/service
[Description de l'offre]

### 4.2 Politique de prix
[Stratégie de pricing]

### 4.3 Distribution
[Canaux de vente]

### 4.4 Communication
[Plan marketing]

### 4.5 Objectifs commerciaux
[KPIs et objectifs chiffrés]

---

## 5. PLAN OPÉRATIONNEL

### 5.1 Processus
[Description des opérations]

### 5.2 Moyens nécessaires
**Locaux :** [Besoins]
**Équipements :** [Liste]
**Logiciels :** [Outils]

### 5.3 Planning de lancement
| Phase | Action | Deadline |
|-------|--------|----------|
| 1 | [Action] | [Date] |
| 2 | [Action] | [Date] |

---

## 6. ÉQUIPE & ORGANISATION

### 6.1 Porteur de projet
[CV résumé]

### 6.2 Équipe
[Organigramme]

### 6.3 Besoins en recrutement
[Postes à pourvoir]

---

## 7. PLAN FINANCIER

### 7.1 Investissements initiaux
| Poste | Montant |
|-------|---------|
| [Poste 1] | [€] |
| Total | {{initial_investment}} |

### 7.2 Plan de financement
| Source | Montant |
|--------|---------|
| Apport personnel | [€] |
| Emprunt | [€] |
{{#if country.includes('Algérie')}}
| ANSEJ/CNAC | [€] |
{{/if}}

### 7.3 Compte de résultat prévisionnel
[Tableau N+1 à N+3]

### 7.4 Plan de trésorerie
[Tableau mensuel année 1]

### 7.5 Seuil de rentabilité
[Calcul du point mort]

---

## 8. ANNEXES

- CV détaillés
- Études de marché
- Devis fournisseurs
- Contrats types

{{#if country.includes('Algérie')}}
---
**Spécificités Algérie :**
- Forme juridique recommandée : EURL/SARL
- Démarches CNRC
- Éligibilité ANSEJ/CNAC
- Fiscalité applicable
{{/if}}`,
  model: 'gpt4',
  estimatedTime: '120s'
};

export const pitchDeckGenerator: AITool = {
  id: 'pitch-deck-generator',
  slug: 'pitch-deck-generator',
  name: { fr: 'Générateur de Pitch Deck', ar: 'مولد عرض المشروع', en: 'Pitch Deck Generator' },
  description: {
    fr: 'Créez un pitch deck percutant pour convaincre investisseurs et partenaires',
    ar: 'أنشئ عرض تقديمي مقنع للمستثمرين والشركاء',
    en: 'Create a compelling pitch deck to convince investors and partners'
  },
  category: 'business',
  subcategory: 'fundraising',
  icon: 'Presentation',
  credits: 35,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'startup_name', type: 'text', label: 'Nom de la startup', required: true },
    { name: 'one_liner', type: 'text', label: 'One-liner (1 phrase)', required: true },
    { name: 'problem', type: 'textarea', label: 'Problème que vous résolvez' },
    { name: 'solution', type: 'textarea', label: 'Votre solution' },
    { name: 'traction', type: 'textarea', label: 'Traction actuelle (chiffres)' },
    { name: 'business_model', type: 'text', label: 'Modèle économique' },
    { name: 'funding_ask', type: 'text', label: 'Montant recherché' },
    { name: 'team', type: 'textarea', label: 'Équipe fondatrice' }
  ],
  outputs: [{ type: 'markdown', name: 'pitch_deck' }],
  promptTemplate: `Tu es un expert en levée de fonds avec 50+ deals réussis.

STARTUP : {{startup_name}}
ONE-LINER : {{one_liner}}
PROBLÈME : {{problem}}
SOLUTION : {{solution}}
TRACTION : {{traction}}
BUSINESS MODEL : {{business_model}}
DEMANDE : {{funding_ask}}
ÉQUIPE : {{team}}

## 🎤 PITCH DECK (12 SLIDES)

### SLIDE 1 : COVER
**{{startup_name}}**
*{{one_liner}}*

[Logo]
[Contact]

---

### SLIDE 2 : PROBLÈME
**"[Stat choc ou citation]"**

Le problème :
- [Point douloureux 1]
- [Point douloureux 2]
- [Point douloureux 3]

💰 Coût du problème : [Chiffre]

---

### SLIDE 3 : SOLUTION
**{{startup_name}} : [Tagline solution]**

[Description claire en 3 bullets]

✅ Avant : [Situation douloureuse]
✅ Après : [Situation idéale avec votre solution]

[Screenshot/Démo visuelle]

---

### SLIDE 4 : PRODUIT
**Comment ça marche**

1️⃣ [Étape 1]
2️⃣ [Étape 2]
3️⃣ [Étape 3]

[Capture d'écran ou schéma]

---

### SLIDE 5 : MARCHÉ (TAM/SAM/SOM)
**Une opportunité de [X] milliards**

🌍 TAM : [Marché total] - $[X]B
🎯 SAM : [Marché adressable] - $[X]B
📍 SOM : [Marché ciblé] - $[X]M

Croissance : +[X]% /an

---

### SLIDE 6 : BUSINESS MODEL
**Comment nous gagnons de l'argent**

| Offre | Prix | Marge |
|-------|------|-------|
| [Offre 1] | [€] | [%] |
| [Offre 2] | [€] | [%] |

**LTV :** [€]
**CAC :** [€]
**Ratio LTV/CAC :** [X]

---

### SLIDE 7 : TRACTION
**Les preuves que ça marche**

📈 [Métrique 1] : [Chiffre]
👥 [Métrique 2] : [Chiffre]
💰 [Métrique 3] : [Chiffre]

[Graphique croissance]

**Clients notables :**
[Logos clients]

---

### SLIDE 8 : CONCURRENCE
**Notre positionnement**

[Matrice 2x2 ou tableau comparatif]

| | Nous | Concurrent A | Concurrent B |
|---|---|---|---|
| [Critère 1] | ✅ | ❌ | ✅ |
| [Critère 2] | ✅ | ✅ | ❌ |

**Notre avantage unfair :** [Moat]

---

### SLIDE 9 : GO-TO-MARKET
**Notre stratégie d'acquisition**

**Canal 1 :** [Description] → [Coût] → [Résultat]
**Canal 2 :** [Description] → [Coût] → [Résultat]

**Prochaines étapes :**
- [Milestone 1]
- [Milestone 2]

---

### SLIDE 10 : ÉQUIPE
**Les bâtisseurs**

👤 **[Nom]** - CEO
[Expérience clé]

👤 **[Nom]** - CTO
[Expérience clé]

👤 **[Nom]** - [Rôle]
[Expérience clé]

**Advisors :** [Noms si applicable]

---

### SLIDE 11 : FINANCIALS
**Projections**

| | 2024 | 2025 | 2026 |
|---|---|---|---|
| ARR | [€] | [€] | [€] |
| Clients | [X] | [X] | [X] |
| Équipe | [X] | [X] | [X] |

---

### SLIDE 12 : THE ASK
**Ce que nous recherchons**

💰 **Levée :** {{funding_ask}}

**Utilisation des fonds :**
- [X]% Produit
- [X]% Sales & Marketing
- [X]% Opérations

**Objectifs 18 mois :**
- [Milestone 1]
- [Milestone 2]
- [Milestone 3]

📧 **Contact :** [Email]

---

**TIPS PITCH :**
✅ Max 20 mots par slide
✅ 1 idée = 1 slide
✅ Graphs > Tableaux > Texte
✅ Pratiquer le pitch en 3 min`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const swotAnalysisGenerator: AITool = {
  id: 'swot-analysis-generator',
  slug: 'swot-analysis-generator',
  name: { fr: 'Analyse SWOT', ar: 'تحليل SWOT', en: 'SWOT Analysis' },
  description: {
    fr: 'Générez une analyse SWOT complète pour votre entreprise ou projet',
    ar: 'أنشئ تحليل SWOT شامل لمشروعك',
    en: 'Generate a complete SWOT analysis for your business or project'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'Grid',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise/projet', required: true },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité', required: true },
    { name: 'business_description', type: 'textarea', label: 'Description de l\'activité' },
    { name: 'competitors', type: 'textarea', label: 'Principaux concurrents' },
    { name: 'current_situation', type: 'textarea', label: 'Situation actuelle' }
  ],
  outputs: [{ type: 'markdown', name: 'swot_analysis' }],
  promptTemplate: `Tu es un consultant en stratégie d'entreprise.

ENTREPRISE : {{business_name}}
SECTEUR : {{industry}}
DESCRIPTION : {{business_description}}
CONCURRENTS : {{competitors}}
SITUATION : {{current_situation}}

## 📊 ANALYSE SWOT - {{business_name}}

### MATRICE SWOT

|  | **Positif** | **Négatif** |
|---|---|---|
| **Interne** | **FORCES** | **FAIBLESSES** |
| **Externe** | **OPPORTUNITÉS** | **MENACES** |

---

### 💪 FORCES (Strengths)

**Ressources & Compétences :**
1. **[Force 1]**
   → Impact : [Explication]
   
2. **[Force 2]**
   → Impact : [Explication]

3. **[Force 3]**
   → Impact : [Explication]

4. **[Force 4]**
   → Impact : [Explication]

5. **[Force 5]**
   → Impact : [Explication]

**Score forces : X/10**

---

### 😓 FAIBLESSES (Weaknesses)

**Points à améliorer :**
1. **[Faiblesse 1]**
   → Risque : [Explication]
   → Action corrective : [Suggestion]

2. **[Faiblesse 2]**
   → Risque : [Explication]
   → Action corrective : [Suggestion]

3. **[Faiblesse 3]**
   → Risque : [Explication]
   → Action corrective : [Suggestion]

4. **[Faiblesse 4]**
   → Risque : [Explication]
   → Action corrective : [Suggestion]

5. **[Faiblesse 5]**
   → Risque : [Explication]
   → Action corrective : [Suggestion]

**Score faiblesses : X/10** (plus c'est bas, mieux c'est)

---

### 🚀 OPPORTUNITÉS (Opportunities)

**Facteurs externes favorables :**
1. **[Opportunité 1]**
   → Potentiel : [Estimation]
   → Comment en profiter : [Action]

2. **[Opportunité 2]**
   → Potentiel : [Estimation]
   → Comment en profiter : [Action]

3. **[Opportunité 3]**
   → Potentiel : [Estimation]
   → Comment en profiter : [Action]

4. **[Opportunité 4]**
   → Potentiel : [Estimation]

5. **[Opportunité 5]**
   → Potentiel : [Estimation]

---

### ⚠️ MENACES (Threats)

**Facteurs externes défavorables :**
1. **[Menace 1]**
   → Probabilité : [Haute/Moyenne/Basse]
   → Impact : [Fort/Moyen/Faible]
   → Mitigation : [Action]

2. **[Menace 2]**
   → Probabilité : [X]
   → Impact : [X]
   → Mitigation : [Action]

3. **[Menace 3]**
   → Probabilité : [X]
   → Impact : [X]
   → Mitigation : [Action]

4. **[Menace 4]**

5. **[Menace 5]**

---

### 🎯 STRATÉGIES CROISÉES

**SO (Forces × Opportunités) - Stratégie offensive :**
→ Utiliser [Force] pour saisir [Opportunité]

**WO (Faiblesses × Opportunités) - Stratégie de développement :**
→ Corriger [Faiblesse] pour profiter de [Opportunité]

**ST (Forces × Menaces) - Stratégie défensive :**
→ Utiliser [Force] pour contrer [Menace]

**WT (Faiblesses × Menaces) - Stratégie de survie :**
→ Minimiser [Faiblesse] face à [Menace]

---

### 📋 PLAN D'ACTION PRIORITAIRE

| Priorité | Action | Responsable | Deadline |
|----------|--------|-------------|----------|
| 🔴 | [Action 1] | [Qui] | [Quand] |
| 🟠 | [Action 2] | [Qui] | [Quand] |
| 🟡 | [Action 3] | [Qui] | [Quand] |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const buyerPersonaGenerator: AITool = {
  id: 'buyer-persona-generator',
  slug: 'buyer-persona-generator',
  name: { fr: 'Générateur de Persona', ar: 'مولد شخصية المشتري', en: 'Buyer Persona Generator' },
  description: {
    fr: 'Créez des personas détaillés pour mieux comprendre vos clients',
    ar: 'أنشئ شخصيات مفصلة لفهم عملائك بشكل أفضل',
    en: 'Create detailed personas to better understand your customers'
  },
  category: 'business',
  subcategory: 'marketing',
  icon: 'User',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_service', type: 'text', label: 'Produit/Service', required: true },
    { name: 'industry', type: 'text', label: 'Secteur' },
    { name: 'target_market', type: 'select', label: 'Marché', options: ['B2C', 'B2B', 'Both'] },
    { name: 'existing_customers', type: 'textarea', label: 'Description de vos clients actuels (si applicable)' },
    { name: 'persona_count', type: 'select', label: 'Nombre de personas', options: ['1', '2', '3'] }
  ],
  outputs: [{ type: 'markdown', name: 'personas' }],
  promptTemplate: `Tu es un expert en marketing et comportement consommateur.

PRODUIT : {{product_service}}
SECTEUR : {{industry}}
MARCHÉ : {{target_market}}
CLIENTS EXISTANTS : {{existing_customers}}

## 👤 BUYER PERSONA

---

### PERSONA 1 : "[Prénom type]"

**📸 Photo type :** [Description visuelle]

---

#### DÉMOGRAPHIE

| Attribut | Valeur |
|----------|--------|
| Prénom | [Prénom] |
| Âge | [X] ans |
| Genre | [H/F] |
| Localisation | [Ville/Région] |
| Situation familiale | [Statut] |
| Revenus | [Fourchette] |
| Éducation | [Niveau] |
| Profession | [Métier] |

---

#### PSYCHOGRAPHIE

**🎯 Objectifs & Aspirations :**
- [Objectif 1]
- [Objectif 2]
- [Objectif 3]

**😤 Frustrations & Points de douleur :**
- [Frustration 1]
- [Frustration 2]
- [Frustration 3]

**💭 Valeurs :**
- [Valeur 1]
- [Valeur 2]

**😨 Peurs :**
- [Peur 1]
- [Peur 2]

---

#### COMPORTEMENT D'ACHAT

**🔍 Processus de décision :**
1. [Étape 1 - Découverte]
2. [Étape 2 - Recherche]
3. [Étape 3 - Comparaison]
4. [Étape 4 - Décision]

**📱 Canaux préférés :**
- [Canal 1] - [Usage]
- [Canal 2] - [Usage]
- [Canal 3] - [Usage]

**🛒 Déclencheurs d'achat :**
- [Trigger 1]
- [Trigger 2]

**🚫 Objections courantes :**
- "[Objection 1]" → Réponse : [Comment y répondre]
- "[Objection 2]" → Réponse : [Comment y répondre]

---

#### CITATION TYPIQUE

> "[Citation qui résume ce persona]"

---

#### COMMENT L'ATTEINDRE

**Messages clés :**
- [Message 1]
- [Message 2]

**Canaux marketing :**
- [Canal] : [Type de contenu]

**Ton de communication :**
[Description du ton]

---

### PERSONA 2 : "[Prénom type]"
[Même structure...]

---

### PERSONA 3 : "[Prénom type]"
[Même structure...]

---

### TABLEAU COMPARATIF

| | Persona 1 | Persona 2 | Persona 3 |
|---|---|---|---|
| Âge | X | X | X |
| Revenu | X | X | X |
| Motivation principale | X | X | X |
| Canal préféré | X | X | X |
| Priorité business | 🔴 | 🟠 | 🟡 |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const valuePropositionGenerator: AITool = {
  id: 'value-proposition-generator',
  slug: 'value-proposition-generator',
  name: { fr: 'Générateur de Proposition de Valeur', ar: 'مولد عرض القيمة', en: 'Value Proposition Generator' },
  description: {
    fr: 'Créez une proposition de valeur claire et différenciante',
    ar: 'أنشئ عرض قيمة واضح ومميز',
    en: 'Create a clear and differentiating value proposition'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'Gem',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_service', type: 'text', label: 'Produit/Service', required: true },
    { name: 'target_customer', type: 'text', label: 'Client cible', required: true },
    { name: 'main_benefit', type: 'text', label: 'Bénéfice principal' },
    { name: 'competitors', type: 'textarea', label: 'Ce que font les concurrents' },
    { name: 'unique_features', type: 'textarea', label: 'Ce qui vous rend unique' }
  ],
  outputs: [{ type: 'markdown', name: 'value_proposition' }],
  promptTemplate: `Tu es un expert en positionnement stratégique.

PRODUIT : {{product_service}}
CLIENT : {{target_customer}}
BÉNÉFICE : {{main_benefit}}
CONCURRENTS : {{competitors}}
UNICITÉ : {{unique_features}}

## 💎 PROPOSITION DE VALEUR

### VALUE PROPOSITION CANVAS

**PROFIL CLIENT :**

| Jobs to be done | Douleurs | Gains recherchés |
|-----------------|----------|------------------|
| [Job 1] | [Pain 1] | [Gain 1] |
| [Job 2] | [Pain 2] | [Gain 2] |
| [Job 3] | [Pain 3] | [Gain 3] |

**CARTE DE VALEUR :**

| Produits/Services | Pain relievers | Gain creators |
|-------------------|----------------|---------------|
| [Feature 1] | [Soulage pain 1] | [Crée gain 1] |
| [Feature 2] | [Soulage pain 2] | [Crée gain 2] |

---

### FORMULATIONS

**Format classique :**
"Pour [{{target_customer}}] qui [problème/besoin], {{product_service}} est [catégorie] qui [bénéfice principal]. Contrairement à [alternatives], nous [différenciateur unique]."

---

**Version 1 - Orientée bénéfice :**
"[Bénéfice principal] pour [audience] grâce à [méthode unique]"

**Version 2 - Orientée problème :**
"[Résoudre problème] sans [inconvénient habituel]"

**Version 3 - Orientée résultat :**
"Obtenez [résultat mesurable] en [temps] avec [produit]"

---

### ONE-LINERS (10 versions)

1. "[Version courte et percutante]"
2. "[Version avec chiffre]"
3. "[Version question]"
4. "[Version comparaison]"
5. "[Version émotionnelle]"
6. "[Version rationnelle]"
7. "[Version pour les sceptiques]"
8. "[Version technique]"
9. "[Version simple]"
10. "[Version storytelling]"

---

### ELEVATOR PITCH (30 secondes)

"Vous savez comment [problème courant] ?

Eh bien, {{product_service}} [solution].

En fait, [preuve/résultat].

Ce qui signifie que [bénéfice pour eux].

Voulez-vous [CTA] ?"

---

### POSITIONNEMENT VS CONCURRENCE

|  | Vous | Concurrent A | Concurrent B |
|--|------|--------------|--------------|
| [Critère 1] | ✅ | ❌ | ✅ |
| [Critère 2] | ✅ | ✅ | ❌ |
| **Proposition unique** | [Votre truc] | [Leur truc] | [Leur truc] |`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const competitiveAnalysisGenerator: AITool = {
  id: 'competitive-analysis-generator',
  slug: 'competitive-analysis-generator',
  name: { fr: 'Analyse Concurrentielle', ar: 'تحليل المنافسين', en: 'Competitive Analysis' },
  description: {
    fr: 'Analysez vos concurrents et identifiez vos opportunités',
    ar: 'حلل منافسيك وحدد فرصك',
    en: 'Analyze your competitors and identify your opportunities'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'Users',
  credits: 20,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'your_business', type: 'text', label: 'Votre entreprise', required: true },
    { name: 'competitors', type: 'textarea', label: 'Liste des concurrents (un par ligne)', required: true },
    { name: 'industry', type: 'text', label: 'Secteur d\'activité' },
    { name: 'analysis_focus', type: 'text', label: 'Points à analyser', placeholder: 'pricing, features, marketing, positioning, strengths_weaknesses' }
  ],
  outputs: [{ type: 'markdown', name: 'competitor_analysis' }],
  promptTemplate: `Tu es un analyste stratégique spécialisé en intelligence concurrentielle.

VOTRE ENTREPRISE : {{your_business}}
CONCURRENTS : {{competitors}}
SECTEUR : {{industry}}
FOCUS : {{analysis_focus}}

## 🔍 ANALYSE CONCURRENTIELLE

### VUE D'ENSEMBLE

| Concurrent | Part de marché | Positionnement | Force principale |
|------------|----------------|----------------|------------------|
| {{your_business}} | [X%] | [Position] | [Force] |
| [Concurrent 1] | [X%] | [Position] | [Force] |
| [Concurrent 2] | [X%] | [Position] | [Force] |
| [Concurrent 3] | [X%] | [Position] | [Force] |

---

### ANALYSE DÉTAILLÉE PAR CONCURRENT

#### 🏢 [CONCURRENT 1]

**Informations générales :**
- Site web : [URL]
- Fondation : [Année]
- Taille : [Employés]
- Financement : [Montant si startup]

**Offre :**
- Produits/Services : [Liste]
- Prix : [Grille tarifaire]
- Positionnement : [Description]

**Forces :**
- ✅ [Force 1]
- ✅ [Force 2]
- ✅ [Force 3]

**Faiblesses :**
- ❌ [Faiblesse 1]
- ❌ [Faiblesse 2]
- ❌ [Faiblesse 3]

**Stratégie marketing :**
- Canaux : [Liste]
- Messages clés : [Thèmes]
- Ton : [Description]

**Avis clients :**
- Note moyenne : [X/5]
- Points positifs récurrents : [Liste]
- Plaintes récurrentes : [Liste]

---

#### 🏢 [CONCURRENT 2]
[Même structure...]

---

### COMPARATIF FONCTIONNALITÉS

| Fonctionnalité | Vous | Conc. 1 | Conc. 2 | Conc. 3 |
|----------------|------|---------|---------|---------|
| [Feature 1] | ✅ | ✅ | ❌ | ✅ |
| [Feature 2] | ✅ | ❌ | ✅ | ❌ |
| [Feature 3] | ❌ | ✅ | ✅ | ✅ |

---

### COMPARATIF PRIX

| Offre | Vous | Conc. 1 | Conc. 2 | Conc. 3 |
|-------|------|---------|---------|---------|
| Entrée | [€] | [€] | [€] | [€] |
| Pro | [€] | [€] | [€] | [€] |
| Enterprise | [€] | [€] | [€] | [€] |

---

### CARTE DE POSITIONNEMENT

[Matrice 2x2 avec axes pertinents]

Axe X : [Prix] ← → [Premium]
Axe Y : [Simple] ← → [Complet]

---

### OPPORTUNITÉS IDENTIFIÉES

🎯 **Gaps à exploiter :**
1. [Opportunité 1] - [Pourquoi]
2. [Opportunité 2] - [Pourquoi]
3. [Opportunité 3] - [Pourquoi]

⚠️ **Menaces à surveiller :**
1. [Menace 1] - [Action recommandée]
2. [Menace 2] - [Action recommandée]

---

### RECOMMANDATIONS STRATÉGIQUES

1. **Différenciation :** [Stratégie]
2. **Prix :** [Stratégie]
3. **Marketing :** [Stratégie]
4. **Produit :** [Fonctionnalités à ajouter]`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const executiveSummaryGenerator: AITool = {
  id: 'executive-summary-generator',
  slug: 'executive-summary-generator',
  name: { fr: 'Résumé Exécutif', ar: 'ملخص تنفيذي', en: 'Executive Summary' },
  description: {
    fr: 'Rédigez un résumé exécutif percutant pour vos documents business',
    ar: 'اكتب ملخص تنفيذي مؤثر لوثائقك التجارية',
    en: 'Write a compelling executive summary for your business documents'
  },
  category: 'business',
  subcategory: 'documents',
  icon: 'FileText',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'document_type', type: 'select', label: 'Type de document', options: [
      'Business Plan',
      'Proposal',
      'Report',
      'Strategy',
      'Investment Memo'
    ]},
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'key_points', type: 'textarea', label: 'Points clés à inclure', required: true },
    { name: 'target_reader', type: 'text', label: 'Lecteur cible' },
    { name: 'desired_action', type: 'text', label: 'Action souhaitée du lecteur' }
  ],
  outputs: [{ type: 'markdown', name: 'executive_summary' }],
  promptTemplate: `Tu es un rédacteur business senior.

TYPE : {{document_type}}
ENTREPRISE : {{company_name}}
POINTS CLÉS : {{key_points}}
LECTEUR : {{target_reader}}
ACTION SOUHAITÉE : {{desired_action}}

## 📄 RÉSUMÉ EXÉCUTIF

---

**[TITRE DU DOCUMENT]**
*Résumé Exécutif*

---

### L'ESSENTIEL

[Paragraphe d'accroche - 2-3 phrases qui captent l'attention et résument le message principal]

---

### LE CONTEXTE

[2-3 phrases sur la situation actuelle/le problème/l'opportunité]

---

### LA PROPOSITION

**{{company_name}}** [description de la solution/proposition en 2-3 phrases]

**Points clés :**
- [Point 1]
- [Point 2]
- [Point 3]

---

### LES CHIFFRES CLÉS

| Indicateur | Valeur |
|------------|--------|
| [Métrique 1] | [Chiffre] |
| [Métrique 2] | [Chiffre] |
| [Métrique 3] | [Chiffre] |

---

### LES BÉNÉFICES

Pour {{target_reader}} :
1. [Bénéfice 1]
2. [Bénéfice 2]
3. [Bénéfice 3]

---

### LA DEMANDE

[Ce que vous demandez au lecteur - 1-2 phrases claires]

---

### PROCHAINES ÉTAPES

1. [Étape 1]
2. [Étape 2]
3. [Étape 3]

---

**Contact :**
[Nom] | [Téléphone] | [Email]

---

**Règles d'un bon résumé exécutif :**
✅ Max 1-2 pages
✅ Peut être lu en 5 minutes
✅ Autonome (compréhensible seul)
✅ Chiffres concrets
✅ Call-to-action clair`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const meetingAgendaGenerator: AITool = {
  id: 'meeting-agenda-generator',
  slug: 'meeting-agenda-generator',
  name: { fr: 'Ordre du Jour de Réunion', ar: 'جدول أعمال الاجتماع', en: 'Meeting Agenda Generator' },
  description: {
    fr: 'Créez des ordres du jour professionnels pour des réunions efficaces',
    ar: 'أنشئ جداول أعمال احترافية لاجتماعات فعالة',
    en: 'Create professional agendas for effective meetings'
  },
  category: 'business',
  subcategory: 'productivity',
  icon: 'Calendar',
  credits: 8,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'meeting_type', type: 'select', label: 'Type de réunion', options: [
      'Team Weekly', 'Project Kickoff', 'Client Meeting', 'Board Meeting', 'Brainstorming', 'One-on-One', 'Sales Meeting', 'Review'
    ]},
    { name: 'meeting_topic', type: 'text', label: 'Sujet de la réunion', required: true },
    { name: 'duration', type: 'select', label: 'Durée', options: ['30min', '45min', '1h', '1h30', '2h'] },
    { name: 'participants', type: 'textarea', label: 'Participants' },
    { name: 'objectives', type: 'textarea', label: 'Objectifs de la réunion' }
  ],
  outputs: [{ type: 'markdown', name: 'agenda' }],
  promptTemplate: `Tu es un expert en facilitation et gestion de réunions.

TYPE : {{meeting_type}}
SUJET : {{meeting_topic}}
DURÉE : {{duration}}
PARTICIPANTS : {{participants}}
OBJECTIFS : {{objectives}}

## 📋 ORDRE DU JOUR

---

**RÉUNION : {{meeting_topic}}**

📅 Date : [À compléter]
⏰ Heure : [À compléter]
⏱️ Durée : {{duration}}
📍 Lieu : [Présentiel/Visio]
👥 Participants : {{participants}}

---

### 🎯 OBJECTIFS

À l'issue de cette réunion, nous aurons :
- [ ] [Objectif 1]
- [ ] [Objectif 2]
- [ ] [Objectif 3]

---

### 📝 AGENDA

| Heure | Durée | Sujet | Responsable | Type |
|-------|-------|-------|-------------|------|
| 00:00 | 5 min | Accueil & Contexte | [Nom] | 📣 Info |
| 00:05 | X min | [Point 1] | [Nom] | 💬 Discussion |
| XX:XX | X min | [Point 2] | [Nom] | ✅ Décision |
| XX:XX | X min | [Point 3] | [Nom] | 🧠 Brainstorm |
| XX:XX | 5 min | Actions & Prochaines étapes | [Nom] | 📋 Récap |

**Légende :**
📣 Information | 💬 Discussion | ✅ Décision | 🧠 Brainstorming | 📋 Récapitulatif

---

### 📚 DOCUMENTS À PRÉPARER

- [ ] [Document 1] - Responsable : [Nom]
- [ ] [Document 2] - Responsable : [Nom]

---

### 📌 RÈGLES DE LA RÉUNION

- ⏰ Commencer et finir à l'heure
- 📵 Téléphones en silencieux
- ✋ Une personne parle à la fois
- 📝 Prendre des notes

---

### ✅ TEMPLATE COMPTE-RENDU

**Décisions prises :**
1. [Décision]

**Actions :**
| Action | Responsable | Deadline |
|--------|-------------|----------|
| [Action] | [Nom] | [Date] |

**Prochaine réunion :** [Date/Heure]`,
  model: 'gpt4',
  estimatedTime: '20s'
};
