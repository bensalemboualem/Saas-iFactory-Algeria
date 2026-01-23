import { AITool } from '../../types';

export const proposalGenerator: AITool = {
  id: 'proposal-generator',
  slug: 'proposal-generator',
  name: { fr: 'Générateur de Proposition Commerciale', ar: 'مولد الاقتراحات التجارية', en: 'Sales Proposal Generator' },
  description: {
    fr: 'Créez des propositions commerciales structurées et convaincantes',
    ar: 'أنشئ مقترحات تجارية منظمة ومقنعة',
    en: 'Create structured and persuasive sales proposals'
  },
  category: 'business',
  subcategory: 'documents',
  icon: 'FileText',
  credits: 20,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'client_name', type: 'text', label: 'Nom du client', required: true },
    { name: 'project_name', type: 'text', label: 'Nom du projet', required: true },
    { name: 'client_needs', type: 'textarea', label: 'Besoins du client', required: true },
    { name: 'proposed_solution', type: 'textarea', label: 'Solution proposée', required: true },
    { name: 'pricing_model', type: 'text', label: 'Modèle de tarification (ex: Forfait, TJM)' },
    { name: 'timeline', type: 'text', label: 'Durée estimée' }
  ],
  outputs: [{ type: 'markdown', name: 'proposal' }],
  promptTemplate: `Tu es un expert en vente et rédaction commerciale.

CLIENT : {{client_name}}
PROJET : {{project_name}}
BESOINS : {{client_needs}}
SOLUTION : {{proposed_solution}}
PRIX : {{pricing_model}}
DURÉE : {{timeline}}

## 📄 PROPOSITION COMMERCIALE

---

# PROPOSITION : {{project_name}}
**Pour :** {{client_name}}
**Date :** [Date]

---

## 1. CONTEXTE & COMPRÉHENSION DU BESOIN

Nous avons bien compris que {{client_name}} cherche à :
- Répondre à : {{client_needs}}
- Atteindre les objectifs suivants : [Objectifs implicites basés sur les besoins]

## 2. NOTRE SOLUTION

Pour répondre à ces enjeux, nous proposons :

**{{proposed_solution}}**

**Approche détaillée :**
1. **Phase d'analyse :** [Détail]
2. **Phase de mise en œuvre :** [Détail]
3. **Phase de validation :** [Détail]

## 3. POURQUOI NOUS CHOISIR ?

- ✅ Expertise éprouvée sur [Domaine]
- ✅ Approche sur-mesure pour {{client_name}}
- ✅ Respect des délais et qualité garantie

## 4. BUDGET & PLANNING

**Investissement :**
{{pricing_model}}

**Planning prévisionnel :**
Durée estimée : {{timeline}}

| Phase | Durée | Livrable |
|-------|-------|----------|
| 1. Lancement | [Durée] | [Livrable] |
| 2. Exécution | [Durée] | [Livrable] |
| 3. Finalisation | [Durée] | [Livrable] |

## 5. PROCHAINES ÉTAPES

1. Validation de la proposition
2. Signature du devis
3. Réunion de lancement (Kick-off)

---

**Signature**
[Votre Nom/Entreprise]
`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const invoiceGenerator: AITool = {
  id: 'invoice-generator',
  slug: 'invoice-generator',
  name: { fr: 'Générateur de Facture (Modèle)', ar: 'مولد نماذج الفواتير', en: 'Invoice Template Generator' },
  description: {
    fr: 'Générez la structure et le contenu d\'une facture professionnelle',
    ar: 'قم بإنشاء هيكل ومحتوى فاتورة احترافية',
    en: 'Generate the structure and content of a professional invoice'
  },
  category: 'business',
  subcategory: 'documents',
  icon: 'FileText',
  credits: 5,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'my_company', type: 'text', label: 'Votre entreprise', required: true },
    { name: 'client_info', type: 'textarea', label: 'Infos client (Nom, Adresse)', required: true },
    { name: 'invoice_number', type: 'text', label: 'Numéro de facture' },
    { name: 'items', type: 'textarea', label: 'Prestations/Produits (liste avec prix)', required: true },
    { name: 'tax_rate', type: 'text', label: 'Taux TVA (%)', defaultValue: '19' },
    { name: 'due_date', type: 'text', label: 'Date d\'échéance' }
  ],
  outputs: [{ type: 'markdown', name: 'invoice' }],
  promptTemplate: `Tu es un assistant administratif. Génère une facture au format Markdown propre.

VOTRE ENTREPRISE : {{my_company}}
CLIENT : {{client_info}}
NUMÉRO : {{invoice_number}}
ITEMS : {{items}}
TVA : {{tax_rate}}%
ÉCHÉANCE : {{due_date}}

## 🧾 FACTURE

---

# FACTURE N° {{invoice_number}}

**Date :** [Date du jour]
**Échéance :** {{due_date}}

| ÉMETTEUR | DESTINATAIRE |
|----------|--------------|
| **{{my_company}}** | **{{client_info}}** |
| [Adresse] | |
| [SIRET/NIF] | |
| [Email] | |

---

## DÉTAIL DES PRESTATIONS

| Description | Qté | Prix Unitaire | Total HT |
|-------------|:---:|--------------:|---------:|
| [Item 1 issu de : {{items}}] | 1 | [Prix] | [Prix] |
| [Item 2 issu de : {{items}}] | 1 | [Prix] | [Prix] |

---

| | Montant |
|---|---:|
| **Total HT** | [Calculer Total] |
| TVA ({{tax_rate}}%) | [Calculer TVA] |
| **TOTAL TTC** | **[Calculer TTC]** |

---

**Conditions de paiement :**
Paiement à réception ou avant le {{due_date}}.
Mode de règlement : Virement bancaire / Chèque.

**Coordonnées bancaires (RIB) :**
Banque : [Nom Banque]
IBAN : [FR76 XXXX ...]
BIC : [XXXX]

*En cas de retard de paiement, une pénalité de 3 fois le taux d'intérêt légal sera appliquée.*
`,
  model: 'gpt3.5',
  estimatedTime: '15s'
};

export const contractTemplateGenerator: AITool = {
  id: 'contract-template-generator',
  slug: 'contract-template-generator',
  name: { fr: 'Générateur de Contrat Type', ar: 'مولد العقود النموذجية', en: 'Contract Template Generator' },
  description: {
    fr: 'Créez une base solide pour vos contrats (Prestation, Confidentialité, etc.)',
    ar: 'أنشئ أساسًا متينًا لعقودك',
    en: 'Create a solid foundation for your contracts'
  },
  category: 'business',
  subcategory: 'documents',
  icon: 'FileText',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'contract_type', type: 'select', label: 'Type de contrat', options: ['Prestation de Service', 'NDA (Confidentialité)', 'Contrat de Travail', 'Partenariat'] },
    { name: 'party_a', type: 'text', label: 'Partie A (Vous)', required: true },
    { name: 'party_b', type: 'text', label: 'Partie B (L\'autre)', required: true },
    { name: 'scope', type: 'textarea', label: 'Objet du contrat / Périmètre' },
    { name: 'duration', type: 'text', label: 'Durée' },
    { name: 'jurisdiction', type: 'text', label: 'Juridiction (Ville/Pays)', defaultValue: 'Algérie' }
  ],
  outputs: [{ type: 'markdown', name: 'contract' }],
  promptTemplate: `Tu es un assistant juridique. Rédige un MODÈLE de contrat.
DISCLAIMER : Ce document est un modèle à titre informatif et doit être validé par un juriste.

TYPE : {{contract_type}}
ENTRE LES PARTIES : {{party_a}} ET {{party_b}}
OBJET : {{scope}}
DURÉE : {{duration}}
JURIDICTION : {{jurisdiction}}

## ⚖️ CONTRAT DE {{contract_type | uppercase}}

**ENTRE LES SOUSSIGNÉS :**

1. **{{party_a}}**, ci-après dénommé(e) "La Partie A".
2. **{{party_b}}**, ci-après dénommé(e) "La Partie B".

Il a été convenu ce qui suit :

### ARTICLE 1 : OBJET DU CONTRAT
Le présent contrat a pour objet : {{scope}}.

### ARTICLE 2 : DURÉE
Ce contrat est conclu pour une durée de {{duration}}, commençant le [Date de début].

### ARTICLE 3 : OBLIGATIONS DES PARTIES

**Obligations de La Partie A :**
- [Lister obligations standards selon le type]
- [Obligation spécifique liée à {{scope}}]

**Obligations de La Partie B :**
- [Lister obligations standards]
- Procéder au paiement (le cas échéant) selon les conditions définies.

### ARTICLE 4 : CONFIDENTIALITÉ
Les parties s'engagent à conserver confidentielles toutes les informations échangées durant l'exécution du présent contrat.

### ARTICLE 5 : RÉSILIATION
Chaque partie peut mettre fin au contrat moyennant un préavis de [X] jours/mois, par lettre recommandée.

### ARTICLE 6 : LITIGES
Tout litige relatif à l'interprétation et à l'exécution des présentes sera soumis au droit applicable à {{jurisdiction}}. À défaut de résolution amiable, les tribunaux compétents de {{jurisdiction}} seront seuls saisis.

---

Fait à {{jurisdiction}}, le [Date].

En deux exemplaires originaux.

**Pour {{party_a}}**                **Pour {{party_b}}**
[Signature]                     [Signature]
`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const okrGenerator: AITool = {
  id: 'okr-generator',
  slug: 'okr-generator',
  name: { fr: 'Générateur d\'OKRs', ar: 'مولد الأهداف والنتائج الرئيسية', en: 'OKR Generator' },
  description: {
    fr: 'Définissez des objectifs ambitieux et mesurables (Objectives & Key Results)',
    ar: 'حدد أهدافًا طموحة وقابلة للقياس',
    en: 'Define ambitious and measurable objectives (Objectives & Key Results)'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'Target',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'objective_theme', type: 'text', label: 'Thème de l\'objectif (ex: Croissance, Produit)', required: true },
    { name: 'timeframe', type: 'select', label: 'Période', options: ['Trimestre(Q1/Q2...)', 'Année', 'Mois'] },
    { name: 'current_challenges', type: 'textarea', label: 'Défis actuels' }
  ],
  outputs: [{ type: 'markdown', name: 'okrs' }],
  promptTemplate: `Tu es un coach en management agile spécialisé dans la méthode OKR (Objectives and Key Results).

THÈME : {{objective_theme}}
PÉRIODE : {{timeframe}}
DÉFIS : {{current_challenges}}

## 🎯 PROPOSITION D'OKRs

Voici 3 propositions d'Objectifs avec leurs Résultats Clés associés pour la période : {{timeframe}}.

### OPTION 1 : Ambitieuse
**Objectif (O) :** [Formulation inspirante liée à {{objective_theme}}]

**Résultats Clés (KRs) :**
1. 📈 **KR1 :** Atteindre [Chiffre précis] sur [Métrique].
2. 🚀 **KR2 :** Lancer [Fonctionnalité/Projet] avant [Date].
3. 👥 **KR3 :** Augmenter [Métrique satisfaction/qualité] de X% à Y%.

---

### OPTION 2 : Pragmatique / Focus Résolution
**Objectif (O) :** [Formulation orientée résolution des défis : {{current_challenges}}]

**Résultats Clés (KRs) :**
1. 📉 **KR1 :** Réduire [Problème] de X%.
2. ✅ **KR2 :** Valider [Étape clé] avec 100% de succès.
3. 🔄 **KR3 :** Automatiser [Processus] pour gagner X heures/semaine.

---

### OPTION 3 : Exploratoire / Innovation
**Objectif (O) :** Transformer l'approche de {{objective_theme}} grâce à l'innovation.

**Résultats Clés (KRs) :**
1. 🧪 **KR1 :** Tester [Hypothèse] auprès de X utilisateurs.
2. 🤝 **KR2 :** Signer [Nombre] nouveaux partenariats stratégiques.
3. 📊 **KR3 :** Obtenir un taux de conversion de X% sur le nouveau canal.

**Conseil d'expert :** Choisissez l'option qui correspond le mieux à votre priorité actuelle. Assurez-vous que chaque KR est mesurable (chiffre, %, binaire).
`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const kpiDashboardGenerator: AITool = {
  id: 'kpi-dashboard-generator',
  slug: 'kpi-dashboard-generator',
  name: { fr: 'Générateur de KPIs', ar: 'مولد مؤشرات الأداء', en: 'KPI Dashboard Generator' },
  description: {
    fr: 'Identifiez les indicateurs clés de performance essentiels pour votre activité',
    ar: 'حدد مؤشرات الأداء الرئيسية لنشاطك',
    en: 'Identify essential Key Performance Indicators for your business'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'TrendingUp',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_activity', type: 'text', label: 'Activité (ex: E-commerce, SaaS, Agence)', required: true },
    { name: 'stage', type: 'select', label: 'Stade de développement', options: ['Lancement', 'Croissance', 'Maturité', 'Pivot'] },
    { name: 'department', type: 'select', label: 'Département concerné', options: ['Global (CEO)', 'Marketing', 'Ventes', 'Produit', 'Service Client'] }
  ],
  outputs: [{ type: 'markdown', name: 'kpis' }],
  promptTemplate: `Tu es un analyste de données business.

ACTIVITÉ : {{business_activity}}
STADE : {{stage}}
DÉPARTEMENT : {{department}}

## 📊 TABLEAU DE BORD KPI SUGGÉRÉ

Pour une activité **{{business_activity}}** en phase de **{{stage}}**, voici les indicateurs (KPIs) essentiels pour le département **{{department}}**.

### 1. INDICATEURS "NORTH STAR" (Les plus critiques)
Ce sont les indicateurs qui définissent le succès global.

| KPI | Définition | Pourquoi le suivre ? | Fréquence |
|-----|------------|----------------------|-----------|
| **[Nom KPI 1]** | [Formule/Définition] | [Impact direct sur le business] | Hebdo |
| **[Nom KPI 2]** | [Formule/Définition] | [Impact] | Hebdo |

### 2. INDICATEURS DE PERFORMANCE (Santé du business)

- **[KPI 3]** : [Explication contextuelle liée à {{business_activity}}]. Cible suggérée : [X].
- **[KPI 4]** : [Explication]. Cible suggérée : [X].
- **[KPI 5]** : [Explication].

### 3. INDICATEURS D'ALERTE (Risques)
À surveiller pour éviter les problèmes.

- ⚠️ **[KPI Risque 1]** (ex: Churn, Burn rate...)
- ⚠️ **[KPI Risque 2]**

---

### 💡 CONSEILS D'IMPLÉMENTATION
1. Ne suivez pas plus de 5-7 KPIs clés par semaine.
2. Pour {{department}}, concentrez-vous sur [Conseil spécifique].
3. Utilisez des outils comme [Outil suggéré 1] ou [Outil suggéré 2] pour visualiser ces données.
`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const projectBriefGenerator: AITool = {
  id: 'project-brief-generator',
  slug: 'project-brief-generator',
  name: { fr: 'Générateur de Brief Projet', ar: 'مولد ملخص المشروع', en: 'Project Brief Generator' },
  description: {
    fr: 'Créez des briefs de projet clairs pour aligner toutes les parties prenantes',
    ar: 'أنشئ ملخصات مشروع واضحة لتوافق جميع الأطراف المعنية',
    en: 'Create clear project briefs to align all stakeholders'
  },
  category: 'business',
  subcategory: 'planning',
  icon: 'ClipboardList',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'project_name', type: 'text', label: 'Nom du projet', required: true },
    { name: 'goal', type: 'textarea', label: 'Objectif principal', required: true },
    { name: 'stakeholders', type: 'text', label: 'Parties prenantes (Équipe, Client...)' },
    { name: 'deadlines', type: 'text', label: 'Dates clés / Deadline' },
    { name: 'deliverables', type: 'textarea', label: 'Livrables attendus' }
  ],
  outputs: [{ type: 'markdown', name: 'brief' }],
  promptTemplate: `Tu es un chef de projet senior.

PROJET : {{project_name}}
OBJECTIF : {{goal}}
PARTIES PRENANTES : {{stakeholders}}
DATES : {{deadlines}}
LIVRABLES : {{deliverables}}

## 📋 BRIEF PROJET : {{project_name}}

### 1. LA VUE D'ENSEMBLE
**Pourquoi ce projet ?**
{{goal}}

Ce projet vise à répondre à [Problème/Opportunité] et s'inscrit dans la stratégie globale.

### 2. OBJECTIFS SMART
- **S**pécifique : [Détail]
- **M**esurable : [Critère de succès]
- **A**tteignable : [Faisabilité]
- **R**éaliste : [Ressources]
- **T**emporel : {{deadlines}}

### 3. PÉRIMÈTRE (SCOPE)
**✅ Inclus (In-Scope) :**
- {{deliverables}}
- [Autre élément implicite]

**❌ Exclu (Out-of-Scope) :**
- [Ce qu'on ne fait pas pour ce projet]

### 4. PARTIES PRENANTES (RÔLES)
- **Chef de projet :** [À définir]
- **Équipe :** {{stakeholders}}
- **Sponsors/Clients :** [À définir]

### 5. GRANDES ÉTAPES (TIMELINE)
📅 **Deadline finale :** {{deadlines}}

1. **Lancement :** [Date]
2. **Jalon intermédiaire :** [Date]
3. **Livraison :** {{deadlines}}

### 6. RISQUES & CONTRAINTES
- [Risque potentiel 1]
- [Risque potentiel 2]

---
*Ce brief sert de référence pour toute l'équipe. Merci de le valider avant le démarrage.*
`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const companyDescriptionGenerator: AITool = {
  id: 'company-description-generator',
  slug: 'company-description-generator',
  name: { fr: 'Description d\'Entreprise', ar: 'وصف الشركة', en: 'Company Description Generator' },
  description: {
    fr: 'Générez des descriptions professionnelles pour votre site, LinkedIn et plaquettes',
    ar: 'أنشئ أوصافًا احترافية لموقعك والمواد التسويقية',
    en: 'Generate professional descriptions for your website, LinkedIn, and brochures'
  },
  category: 'business',
  subcategory: 'marketing',
  icon: 'Building',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'activity', type: 'textarea', label: 'Activité / Ce que vous faites', required: true },
    { name: 'target_audience', type: 'text', label: 'Clients cibles' },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Innovant', 'Sympathique', 'Prestigieux'] },
    { name: 'usp', type: 'text', label: 'Point fort unique (USP)' }
  ],
  outputs: [{ type: 'markdown', name: 'descriptions' }],
  promptTemplate: `Tu es un copywriter spécialisé en branding.

ENTREPRISE : {{company_name}}
ACTIVITÉ : {{activity}}
CIBLE : {{target_audience}}
TON : {{tone}}
USP : {{usp}}

## 🏢 DESCRIPTIONS D'ENTREPRISE

Voici plusieurs versions adaptées à différents supports.

### 1. PITCH "ONE-LINER" (Slogan / Bio Instagram)
*Court et impactant.*

> "{{company_name}} : [Phrase d'accroche résumant l'activité et l'USP]."

### 2. VERSION "À PROPOS" (Site Web / Plaquette) - ~100 mots
*Inspirante et descriptive.*

"Chez **{{company_name}}**, nous croyons que [Vision]. C'est pourquoi nous accompagnons {{target_audience}} en proposant {{activity}}.

Notre force ? {{usp}}.
Grâce à une approche {{tone}}, nous transformons [Problème client] en [Solution/Résultat]. Rejoignez les nombreux clients qui nous font confiance pour [Bénéfice principal]."

### 3. VERSION LINKEDIN (Page Entreprise)
*Professionnelle et orientée recrutement/business.*

"Bienvenue chez {{company_name}} ! 👋

Nous sommes spécialisés dans **{{activity}}** à destination de **{{target_audience}}**.

🚀 **Notre Mission :** Aider nos clients à [Objectif principal] grâce à {{usp}}.

Nos expertises :
- [Expertise 1]
- [Expertise 2]
- [Expertise 3]

Suivez-nous pour découvrir nos actualités, nos coulisses et nos offres d'emploi.

📍 [Localisation] | 🌐 [Site Web]"

### 4. VERSION "BOILERPLATE" (Bas de communiqué de presse)
*Factuelle et journalistique.*

"À propos de {{company_name}} :
Fondée en [Année], {{company_name}} est une entreprise leader dans {{activity}}. Basée à [Lieu], elle s'adresse principalement à {{target_audience}} avec une proposition de valeur unique : {{usp}}. Pour plus d'informations, visitez [Site Web]."
`,
  model: 'gpt3.5',
  estimatedTime: '20s'
};

export const missionVisionGenerator: AITool = {
  id: 'mission-vision-generator',
  slug: 'mission-vision-generator',
  name: { fr: 'Générateur Mission & Vision', ar: 'مولد المهمة والرؤية', en: 'Mission & Vision Generator' },
  description: {
    fr: 'Définissez l\'ADN de votre entreprise : Mission, Vision et Valeurs',
    ar: 'حدد هوية شركتك: المهمة، الرؤية والقيم',
    en: 'Define your company DNA: Mission, Vision, and Values'
  },
  category: 'business',
  subcategory: 'strategy',
  icon: 'Compass',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'industry', type: 'text', label: 'Industrie / Secteur' },
    { name: 'impact', type: 'textarea', label: 'Quel impact voulez-vous avoir ?' },
    { name: 'core_values', type: 'text', label: 'Mots-clés de vos valeurs (ex: Transparence, Innovation)' }
  ],
  outputs: [{ type: 'markdown', name: 'mission_vision' }],
  promptTemplate: `Tu es un stratège de marque.

ENTREPRISE : {{company_name}}
SECTEUR : {{industry}}
IMPACT SOUHAITÉ : {{impact}}
VALEURS CLÉS : {{core_values}}

## 🧭 ADN DE MARQUE : {{company_name}}

Voici 3 options pour structurer votre identité stratégique.

---

### OPTION 1 : L'INSPIRANTE
*Ton : Élevé, visionnaire, orienté vers le futur.*

👁️ **VISION (Où allons-nous ?) :**
"Créer un monde où {{impact}} est la norme, en redéfinissant les standards de {{industry}}."

🚀 **MISSION (Que faisons-nous chaque jour ?) :**
"Donner le pouvoir à chacun de [Action] grâce à des solutions [Adjectif], propulsées par l'innovation."

💎 **VALEURS :**
- **{{core_values}}** : [Explication courte]
- **[Valeur suggérée 2]** : [Explication]

---

### OPTION 2 : LA PRAGMATIQUE
*Ton : Direct, concret, orienté client.*

👁️ **VISION :**
"Devenir le partenaire de référence en {{industry}} pour [Cible/Marché]."

🚀 **MISSION :**
"Fournir les meilleures solutions de {{industry}} pour permettre à nos clients de réaliser {{impact}} simplement et efficacement."

💎 **VALEURS :**
- **Fiabilité**
- **{{core_values}}**

---

### OPTION 3 : LA DISRUPTIVE
*Ton : Audacieux, challengeur.*

👁️ **VISION :**
"Révolutionner {{industry}} en brisant les barrières de [Problème actuel]."

🚀 **MISSION :**
"Nous existons pour {{impact}}, quoi qu'il en coûte. Nous ne suivons pas les règles, nous les réécrivons."

💎 **VALEURS :**
- **Audace**
- **{{core_values}}**

---

**Conseil :** La Vision est votre étoile du Nord (l'objectif ultime). La Mission est votre véhicule (ce que vous faites pour y aller). Les Valeurs sont votre carburant (comment vous vous comportez).
`,
  model: 'gpt4',
  estimatedTime: '30s'
};
