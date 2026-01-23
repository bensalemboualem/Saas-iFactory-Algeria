'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Briefcase, Sparkles, Zap, Star, FileText, Target, Users, DollarSign, ClipboardList, BarChart3, FileCheck, Megaphone } from 'lucide-react';
import { useState } from 'react';
import { businessTools, getToolBySlug } from '@/lib/tools-data';

// Configuration des formulaires pour chaque outil
const formConfigs: Record<string, {
  fields: Array<{
    name: string;
    label: string;
    type: 'text' | 'textarea' | 'select' | 'number' | 'checkbox' | 'tags' | 'multiselect';
    placeholder?: string;
    options?: { value: string; label: string }[];
    required?: boolean;
    rows?: number;
  }>;
  promptTemplate: string;
}> = {
  // ===== BATCH 1 - CRITIQUE (8 outils) =====

  'business-plan-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'industry', label: 'Secteur d\'activité', type: 'select', required: true, options: [
        { value: 'tech', label: '💻 Tech / SaaS' },
        { value: 'ecommerce', label: '🛒 E-commerce' },
        { value: 'food', label: '🍽️ Food & Restauration' },
        { value: 'health', label: '🏥 Santé' },
        { value: 'education', label: '📚 Éducation' },
        { value: 'finance', label: '💰 Finance / Fintech' },
        { value: 'logistics', label: '🚛 Logistique' },
        { value: 'manufacturing', label: '🏭 Industrie' },
        { value: 'services', label: '🤝 Services' },
        { value: 'other', label: '📋 Autre' }
      ]},
      { name: 'businessModel', label: 'Modèle économique', type: 'select', required: true, options: [
        { value: 'b2b', label: '🏢 B2B' },
        { value: 'b2c', label: '👥 B2C' },
        { value: 'b2b2c', label: '🔄 B2B2C' },
        { value: 'marketplace', label: '🏪 Marketplace' },
        { value: 'subscription', label: '📆 Abonnement' },
        { value: 'freemium', label: '🆓 Freemium' }
      ]},
      { name: 'problemSolved', label: 'Problème résolu', type: 'textarea', placeholder: 'Décrivez le problème que votre produit/service résout...', required: true, rows: 3 },
      { name: 'solution', label: 'Votre solution', type: 'textarea', placeholder: 'Décrivez votre produit/service et comment il résout le problème...', required: true, rows: 3 },
      { name: 'targetMarket', label: 'Marché cible', type: 'textarea', placeholder: 'Ex: PME algériennes, 500-5000 entreprises potentielles', required: true, rows: 2 },
      { name: 'competitors', label: 'Concurrents principaux', type: 'text', placeholder: 'Ex: Concurrent A, Concurrent B, solutions alternatives' },
      { name: 'uniqueAdvantage', label: 'Avantage concurrentiel', type: 'textarea', placeholder: 'Qu\'est-ce qui vous différencie de la concurrence?', rows: 2 },
      { name: 'revenueStreams', label: 'Sources de revenus', type: 'text', placeholder: 'Ex: Abonnements, commissions, licences' },
      { name: 'fundingNeeded', label: 'Financement recherché', type: 'text', placeholder: 'Ex: 50M DZD pour 18 mois' },
      { name: 'teamSize', label: 'Taille de l\'équipe actuelle', type: 'select', options: [
        { value: 'solo', label: '👤 Solo founder' },
        { value: '2-5', label: '👥 2-5 personnes' },
        { value: '6-10', label: '👨‍👩‍👧‍👦 6-10 personnes' },
        { value: '11-25', label: '🏢 11-25 personnes' },
        { value: '25+', label: '🏛️ 25+ personnes' }
      ]},
      { name: 'stage', label: 'Stade de développement', type: 'select', options: [
        { value: 'idea', label: '💡 Idée' },
        { value: 'mvp', label: '🔧 MVP en développement' },
        { value: 'launched', label: '🚀 Produit lancé' },
        { value: 'traction', label: '📈 Traction / Premiers clients' },
        { value: 'scaling', label: '⚡ Croissance / Scaling' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en stratégie d'entreprise et en rédaction de business plans professionnels. Génère un business plan complet et structuré.

INFORMATIONS DE L'ENTREPRISE:
- Nom: {{companyName}}
- Secteur: {{industry}}
- Modèle économique: {{businessModel}}
- Stade: {{stage}}
- Équipe: {{teamSize}}

PROBLÈME & SOLUTION:
- Problème résolu: {{problemSolved}}
- Solution proposée: {{solution}}

MARCHÉ:
- Marché cible: {{targetMarket}}
- Concurrents: {{competitors}}
- Avantage concurrentiel: {{uniqueAdvantage}}

FINANCES:
- Sources de revenus: {{revenueStreams}}
- Financement recherché: {{fundingNeeded}}

Génère un business plan professionnel en {{language}} avec les sections suivantes:

## 1. RÉSUMÉ EXÉCUTIF (Executive Summary)
- Pitch de l'entreprise en 3-4 phrases percutantes
- Problème/Solution en bref
- Opportunité de marché
- Demande de financement et utilisation

## 2. PRÉSENTATION DE L'ENTREPRISE
- Vision et mission
- Valeurs
- Historique et étapes clés
- Structure juridique recommandée

## 3. ANALYSE DU MARCHÉ
- Taille du marché (TAM, SAM, SOM)
- Tendances du secteur
- Analyse des segments cibles
- Comportement d'achat

## 4. ANALYSE CONCURRENTIELLE
- Mapping des concurrents
- Forces et faiblesses
- Positionnement différenciant
- Barrières à l'entrée

## 5. PRODUIT / SERVICE
- Description détaillée
- Fonctionnalités clés
- Roadmap produit
- Propriété intellectuelle

## 6. STRATÉGIE COMMERCIALE
- Canaux de distribution
- Stratégie pricing
- Plan marketing
- Partenariats stratégiques

## 7. MODÈLE ÉCONOMIQUE
- Sources de revenus détaillées
- Structure de coûts
- Marges prévisionnelles
- Point mort

## 8. PLAN OPÉRATIONNEL
- Organisation de l'équipe
- Processus clés
- Ressources nécessaires
- Jalons à 12-24 mois

## 9. PROJECTIONS FINANCIÈRES
- Prévisions de revenus (3 ans)
- Budget d'exploitation
- Cash flow prévisionnel
- Métriques clés (CAC, LTV, MRR)

## 10. DEMANDE DE FINANCEMENT
- Montant et valorisation
- Utilisation des fonds
- Retour attendu
- Exit strategy

Utilise des données réalistes pour le marché algérien. Sois professionnel, précis et convaincant.`
  },

  'pitch-deck-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'tagline', label: 'Tagline / Slogan', type: 'text', placeholder: 'Ex: L\'IA au service des PME algériennes', required: true },
      { name: 'problem', label: 'Le problème', type: 'textarea', placeholder: 'Décrivez le problème que vous résolvez...', required: true, rows: 3 },
      { name: 'solution', label: 'Votre solution', type: 'textarea', placeholder: 'Comment votre produit résout ce problème?', required: true, rows: 3 },
      { name: 'marketSize', label: 'Taille du marché', type: 'text', placeholder: 'Ex: 500M$ marché algérien, 5B$ Afrique du Nord' },
      { name: 'businessModel', label: 'Modèle de revenus', type: 'textarea', placeholder: 'Comment gagnez-vous de l\'argent?', rows: 2 },
      { name: 'traction', label: 'Traction / Métriques', type: 'textarea', placeholder: 'Ex: 500 utilisateurs, 10M DZD ARR, 30% croissance mensuelle', rows: 2 },
      { name: 'competition', label: 'Concurrence', type: 'textarea', placeholder: 'Qui sont vos concurrents et pourquoi êtes-vous meilleur?', rows: 2 },
      { name: 'team', label: 'Équipe fondatrice', type: 'textarea', placeholder: 'Présentez les fondateurs et leurs expertises', rows: 2 },
      { name: 'askAmount', label: 'Montant recherché', type: 'text', placeholder: 'Ex: 100M DZD / 500K€' },
      { name: 'useOfFunds', label: 'Utilisation des fonds', type: 'textarea', placeholder: 'Comment allez-vous utiliser cet investissement?', rows: 2 },
      { name: 'deckStyle', label: 'Style du pitch', type: 'select', options: [
        { value: 'investor', label: '💰 Pour investisseurs (VC/Angels)' },
        { value: 'accelerator', label: '🚀 Pour accélérateur/incubateur' },
        { value: 'competition', label: '🏆 Pour compétition startup' },
        { value: 'corporate', label: '🏢 Pour partenaire corporate' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en pitch deck et en levée de fonds. Crée un pitch deck percutant et professionnel.

ENTREPRISE:
- Nom: {{companyName}}
- Tagline: {{tagline}}
- Style: {{deckStyle}}

CONTENU:
- Problème: {{problem}}
- Solution: {{solution}}
- Marché: {{marketSize}}
- Modèle: {{businessModel}}
- Traction: {{traction}}
- Concurrence: {{competition}}
- Équipe: {{team}}
- Ask: {{askAmount}}
- Utilisation: {{useOfFunds}}

Génère un pitch deck professionnel en {{language}} avec le contenu textuel de chaque slide:

## SLIDE 1: TITRE
- Logo/Nom: {{companyName}}
- Tagline percutante
- Contact fondateur

## SLIDE 2: LE PROBLÈME
- Problème en 3 points maximum
- Données chiffrées si disponibles
- Impact émotionnel

## SLIDE 3: LA SOLUTION
- Votre solution en une phrase
- 3 bénéfices clés
- Screenshot/Demo si applicable

## SLIDE 4: PRODUIT
- Fonctionnalités principales
- Différenciateurs techniques
- Demo ou captures d'écran

## SLIDE 5: MARCHÉ
- TAM / SAM / SOM
- Croissance du marché
- Opportunité timing

## SLIDE 6: MODÈLE ÉCONOMIQUE
- Sources de revenus
- Pricing
- Unit economics (CAC, LTV)

## SLIDE 7: TRACTION
- Métriques clés
- Croissance
- Témoignages/logos clients

## SLIDE 8: CONCURRENCE
- Matrice comparative
- Votre positionnement unique
- Avantages défendables

## SLIDE 9: ÉQUIPE
- Fondateurs avec photos
- Expériences pertinentes
- Advisors si applicable

## SLIDE 10: ROADMAP
- Jalons passés
- Objectifs 12-18 mois
- Vision long terme

## SLIDE 11: FINANCIALS
- Projections 3 ans
- Métriques clés
- Path to profitability

## SLIDE 12: THE ASK
- Montant demandé
- Utilisation des fonds (graphique)
- Prochaines étapes

## SLIDE 13: CONTACT
- Coordonnées
- Call to action

Chaque slide doit être concise (max 6 points), visuelle et mémorable. Adapte le ton au type de pitch ({{deckStyle}}).`
  },

  'swot-analysis-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise/projet', type: 'text', placeholder: 'Ex: Ma Startup', required: true },
      { name: 'industry', label: 'Secteur d\'activité', type: 'text', placeholder: 'Ex: E-commerce alimentaire', required: true },
      { name: 'description', label: 'Description de l\'activité', type: 'textarea', placeholder: 'Décrivez votre entreprise, produits/services...', required: true, rows: 3 },
      { name: 'currentSituation', label: 'Situation actuelle', type: 'textarea', placeholder: 'Où en êtes-vous? Chiffre d\'affaires, équipe, clients...', rows: 3 },
      { name: 'competitors', label: 'Concurrents principaux', type: 'textarea', placeholder: 'Listez vos concurrents directs et indirects', rows: 2 },
      { name: 'resources', label: 'Ressources disponibles', type: 'textarea', placeholder: 'Budget, équipe, technologie, partenariats...', rows: 2 },
      { name: 'marketContext', label: 'Contexte marché', type: 'textarea', placeholder: 'Tendances, réglementations, évolutions...', rows: 2 },
      { name: 'objectives', label: 'Objectifs à atteindre', type: 'textarea', placeholder: 'Que voulez-vous accomplir?', rows: 2 },
      { name: 'analysisDepth', label: 'Profondeur d\'analyse', type: 'select', options: [
        { value: 'quick', label: '⚡ Rapide (5-10 points par catégorie)' },
        { value: 'detailed', label: '📊 Détaillée (10-15 points par catégorie)' },
        { value: 'comprehensive', label: '📈 Exhaustive (15+ points avec recommandations)' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un consultant stratégique expert en analyse SWOT. Réalise une analyse complète et actionnable.

ENTREPRISE:
- Nom: {{companyName}}
- Secteur: {{industry}}
- Description: {{description}}
- Situation: {{currentSituation}}
- Concurrents: {{competitors}}
- Ressources: {{resources}}
- Contexte: {{marketContext}}
- Objectifs: {{objectives}}
- Profondeur: {{analysisDepth}}

Génère une analyse SWOT professionnelle en {{language}}:

## RÉSUMÉ EXÉCUTIF
Synthèse en 3-4 phrases de la position stratégique de l'entreprise.

## FORCES (Strengths) - Facteurs internes positifs
Pour chaque force:
- [Force] : Description
- Impact: Fort/Moyen/Faible
- Comment l'exploiter

{{#if analysisDepth === 'comprehensive'}}
Analyse approfondie de chaque force avec exemples concrets.
{{/if}}

## FAIBLESSES (Weaknesses) - Facteurs internes négatifs
Pour chaque faiblesse:
- [Faiblesse] : Description
- Urgence: Critique/Importante/Mineure
- Plan d'amélioration

{{#if analysisDepth === 'comprehensive'}}
Analyse des causes profondes et solutions détaillées.
{{/if}}

## OPPORTUNITÉS (Opportunities) - Facteurs externes positifs
Pour chaque opportunité:
- [Opportunité] : Description
- Potentiel: Élevé/Moyen/Faible
- Comment la saisir

{{#if analysisDepth === 'comprehensive'}}
Timeline et ressources nécessaires pour chaque opportunité.
{{/if}}

## MENACES (Threats) - Facteurs externes négatifs
Pour chaque menace:
- [Menace] : Description
- Probabilité: Haute/Moyenne/Basse
- Stratégie de mitigation

{{#if analysisDepth === 'comprehensive'}}
Scénarios de crise et plans de contingence.
{{/if}}

## MATRICE SWOT CROISÉE
- Stratégies SO (Forces + Opportunités)
- Stratégies WO (Faiblesses + Opportunités)
- Stratégies ST (Forces + Menaces)
- Stratégies WT (Faiblesses + Menaces)

## RECOMMANDATIONS STRATÉGIQUES
1. Actions prioritaires (0-3 mois)
2. Actions moyen terme (3-12 mois)
3. Actions long terme (12+ mois)

## INDICATEURS DE SUIVI
KPIs recommandés pour mesurer l'exécution de la stratégie.

Sois spécifique au contexte algérien si pertinent. Fournis des recommandations actionnables.`
  },

  'buyer-persona-generator': {
    fields: [
      { name: 'productService', label: 'Produit/Service vendu', type: 'textarea', placeholder: 'Décrivez ce que vous vendez...', required: true, rows: 2 },
      { name: 'industry', label: 'Secteur d\'activité', type: 'text', placeholder: 'Ex: SaaS B2B, E-commerce mode', required: true },
      { name: 'priceRange', label: 'Gamme de prix', type: 'text', placeholder: 'Ex: 5000-20000 DZD/mois' },
      { name: 'currentCustomers', label: 'Clients actuels (si existants)', type: 'textarea', placeholder: 'Décrivez vos clients actuels: qui sont-ils?', rows: 2 },
      { name: 'targetMarket', label: 'Marché cible', type: 'select', options: [
        { value: 'b2b', label: '🏢 B2B (Entreprises)' },
        { value: 'b2c', label: '👥 B2C (Particuliers)' },
        { value: 'both', label: '🔄 Les deux' }
      ]},
      { name: 'geography', label: 'Zone géographique', type: 'select', options: [
        { value: 'algeria', label: '🇩🇿 Algérie uniquement' },
        { value: 'maghreb', label: '🌍 Maghreb' },
        { value: 'francophone', label: '🇫🇷 Afrique francophone' },
        { value: 'mena', label: '🌙 MENA' },
        { value: 'global', label: '🌐 International' }
      ]},
      { name: 'personaCount', label: 'Nombre de personas', type: 'select', options: [
        { value: '1', label: '1️⃣ Un persona principal' },
        { value: '2', label: '2️⃣ Deux personas' },
        { value: '3', label: '3️⃣ Trois personas' }
      ]},
      { name: 'painPoints', label: 'Problèmes que vous résolvez', type: 'textarea', placeholder: 'Quels problèmes votre solution résout?', rows: 2 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en marketing et en création de buyer personas. Crée des personas détaillés et actionnables.

PRODUIT/SERVICE:
- Description: {{productService}}
- Secteur: {{industry}}
- Prix: {{priceRange}}
- Clients actuels: {{currentCustomers}}
- Marché: {{targetMarket}}
- Zone: {{geography}}
- Problèmes résolus: {{painPoints}}

Génère {{personaCount}} buyer persona(s) détaillé(s) en {{language}}:

{{#each personas}}
## PERSONA {{index}}: [Prénom fictif]

### PROFIL DÉMOGRAPHIQUE
- Prénom: [Prénom typique]
- Âge: [Tranche d'âge]
- Genre: [Si pertinent]
- Localisation: [Ville/Région]
- Situation familiale: [Célibataire/Marié/Enfants]
- Niveau d'éducation: [Diplôme]
- Revenus: [Tranche en DZD]

### PROFIL PROFESSIONNEL
- Poste: [Titre exact]
- Entreprise type: [Taille, secteur]
- Ancienneté: [Années d'expérience]
- Responsabilités: [3-4 responsabilités clés]
- Objectifs professionnels: [Ce qu'il/elle veut accomplir]
- Défis quotidiens: [Frustrations au travail]

### COMPORTEMENT D'ACHAT
- Processus de décision: [Comment il/elle achète]
- Critères de choix: [Top 5 critères]
- Budget typique: [Montant]
- Cycle d'achat: [Durée]
- Influenceurs: [Qui influence sa décision]
- Objections courantes: [Freins à l'achat]

### CANAUX & MÉDIAS
- Réseaux sociaux: [Lesquels, fréquence]
- Sources d'information: [Sites, blogs, podcasts]
- Événements: [Salons, conférences]
- Communautés: [Groupes, forums]

### POINTS DE DOULEUR (Pain Points)
1. [Problème majeur 1]
2. [Problème majeur 2]
3. [Problème majeur 3]
4. [Problème majeur 4]

### MOTIVATIONS
- Ce qui le/la motive à acheter
- Résultats recherchés
- Émotions associées

### OBJECTIONS TYPIQUES
1. "[Objection 1]" → Réponse suggérée
2. "[Objection 2]" → Réponse suggérée
3. "[Objection 3]" → Réponse suggérée

### MESSAGE CLÉ
La phrase qui résonne le plus avec ce persona.

### CITATION TYPIQUE
"[Une phrase que ce persona dirait]"
{{/each}}

## SYNTHÈSE MARKETING
- Comment atteindre ces personas
- Messages clés par persona
- Canaux prioritaires
- Contenu recommandé

Adapte les personas au contexte {{geography}} et au marché {{targetMarket}}.`
  },

  'value-proposition-generator': {
    fields: [
      { name: 'productService', label: 'Produit/Service', type: 'textarea', placeholder: 'Décrivez votre produit ou service...', required: true, rows: 3 },
      { name: 'targetCustomer', label: 'Client cible', type: 'textarea', placeholder: 'Qui est votre client idéal?', required: true, rows: 2 },
      { name: 'mainProblem', label: 'Problème principal résolu', type: 'textarea', placeholder: 'Quel problème résolvez-vous?', required: true, rows: 2 },
      { name: 'keyBenefits', label: 'Bénéfices clés', type: 'textarea', placeholder: 'Listez 3-5 bénéfices principaux', rows: 2 },
      { name: 'competitors', label: 'Alternatives/Concurrents', type: 'textarea', placeholder: 'Que font les clients actuellement?', rows: 2 },
      { name: 'uniqueFeatures', label: 'Ce qui vous rend unique', type: 'textarea', placeholder: 'Votre différenciateur principal', rows: 2 },
      { name: 'proofPoints', label: 'Preuves/Résultats', type: 'textarea', placeholder: 'Ex: +50% productivité, 1000 clients satisfaits', rows: 2 },
      { name: 'tone', label: 'Ton souhaité', type: 'select', options: [
        { value: 'professional', label: '👔 Professionnel' },
        { value: 'friendly', label: '😊 Amical' },
        { value: 'bold', label: '🔥 Audacieux' },
        { value: 'technical', label: '⚙️ Technique' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en positionnement marketing et en création de propositions de valeur percutantes.

PRODUIT/SERVICE: {{productService}}
CLIENT CIBLE: {{targetCustomer}}
PROBLÈME: {{mainProblem}}
BÉNÉFICES: {{keyBenefits}}
CONCURRENCE: {{competitors}}
DIFFÉRENCIATEUR: {{uniqueFeatures}}
PREUVES: {{proofPoints}}
TON: {{tone}}

Génère une proposition de valeur complète en {{language}}:

## 1. VALUE PROPOSITION CANVAS

### Profil Client
- Jobs to be done (tâches à accomplir):
  1. [Job fonctionnel]
  2. [Job émotionnel]
  3. [Job social]

- Pains (douleurs):
  1. [Douleur 1]
  2. [Douleur 2]
  3. [Douleur 3]

- Gains (gains recherchés):
  1. [Gain 1]
  2. [Gain 2]
  3. [Gain 3]

### Carte de Valeur
- Products & Services:
  [Liste des éléments de votre offre]

- Pain Relievers:
  [Comment vous soulagez chaque douleur]

- Gain Creators:
  [Comment vous créez chaque gain]

## 2. FORMULES DE PROPOSITION DE VALEUR

### Format classique
"Pour [client cible] qui [problème/besoin], [produit] est [catégorie] qui [bénéfice principal]. Contrairement à [alternative], notre solution [différenciateur unique]."

### Format XYZ
"Nous aidons [X] à [Y] grâce à [Z]."

### Format "Avant/Après"
- AVANT: [Situation sans votre solution]
- APRÈS: [Situation avec votre solution]

### Format problème-solution
"[Problème] ? [Solution en une phrase]."

## 3. VARIATIONS PAR CONTEXTE

### Pour la page d'accueil
[Titre accrocheur]
[Sous-titre explicatif]
[CTA]

### Pour un pitch de 30 secondes
[Version orale concise]

### Pour les réseaux sociaux
[Version courte et percutante]

### Pour l'email marketing
[Version avec bénéfices]

## 4. MESSAGES DE SOUTIEN

### Bénéfice 1: [Titre]
[Explication + preuve]

### Bénéfice 2: [Titre]
[Explication + preuve]

### Bénéfice 3: [Titre]
[Explication + preuve]

## 5. OBJECTIONS & RÉPONSES

| Objection | Réponse |
|-----------|---------|
| [Objection 1] | [Réponse] |
| [Objection 2] | [Réponse] |
| [Objection 3] | [Réponse] |

## 6. TAGLINES SUGGÉRÉES
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]
5. [Option 5]

Assure-toi que chaque formulation est claire, mémorable et différenciante. Ton: {{tone}}.`
  },

  'competitive-analysis-generator': {
    fields: [
      { name: 'companyName', label: 'Votre entreprise', type: 'text', placeholder: 'Ex: Ma Startup', required: true },
      { name: 'industry', label: 'Secteur d\'activité', type: 'text', placeholder: 'Ex: Livraison de repas', required: true },
      { name: 'yourOffering', label: 'Votre offre', type: 'textarea', placeholder: 'Décrivez votre produit/service...', required: true, rows: 3 },
      { name: 'competitors', label: 'Concurrents à analyser', type: 'textarea', placeholder: 'Listez 3-5 concurrents avec une brève description de chacun', required: true, rows: 4 },
      { name: 'comparisonCriteria', label: 'Critères de comparaison', type: 'textarea', placeholder: 'Ex: Prix, fonctionnalités, qualité, service client...', rows: 2 },
      { name: 'yourStrengths', label: 'Vos forces', type: 'textarea', placeholder: 'Ce que vous faites mieux que les autres', rows: 2 },
      { name: 'analysisGoal', label: 'Objectif de l\'analyse', type: 'select', options: [
        { value: 'positioning', label: '🎯 Définir mon positionnement' },
        { value: 'pricing', label: '💰 Définir ma stratégie prix' },
        { value: 'features', label: '⚙️ Prioriser mes fonctionnalités' },
        { value: 'marketing', label: '📢 Améliorer mon marketing' },
        { value: 'complete', label: '📊 Analyse complète' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un analyste stratégique expert en veille concurrentielle. Réalise une analyse concurrentielle approfondie.

VOTRE ENTREPRISE:
- Nom: {{companyName}}
- Secteur: {{industry}}
- Offre: {{yourOffering}}
- Forces: {{yourStrengths}}

CONCURRENTS:
{{competitors}}

CRITÈRES: {{comparisonCriteria}}
OBJECTIF: {{analysisGoal}}

Génère une analyse concurrentielle complète en {{language}}:

## RÉSUMÉ EXÉCUTIF
Synthèse de la position concurrentielle et recommandations clés.

## 1. PANORAMA DU MARCHÉ
- Taille et croissance du marché
- Tendances majeures
- Facteurs clés de succès
- Barrières à l'entrée

## 2. PROFILS DES CONCURRENTS

{{#each competitor}}
### [Nom du concurrent]

**Aperçu**
- Fondation/Historique
- Taille estimée (employés, CA)
- Positionnement

**Offre**
- Produits/Services principaux
- Pricing
- Modèle économique

**Forces**
- [Force 1]
- [Force 2]
- [Force 3]

**Faiblesses**
- [Faiblesse 1]
- [Faiblesse 2]
- [Faiblesse 3]

**Stratégie**
- Approche marketing
- Canaux de distribution
- Cibles prioritaires

**Menace pour vous**: Faible / Moyenne / Élevée
{{/each}}

## 3. MATRICE COMPARATIVE

| Critère | {{companyName}} | Concurrent 1 | Concurrent 2 | Concurrent 3 |
|---------|-----------------|--------------|--------------|--------------|
| Prix | | | | |
| Qualité | | | | |
| Innovation | | | | |
| Service | | | | |
| [Autres critères] | | | | |

Légende: ⭐⭐⭐ Excellent | ⭐⭐ Bon | ⭐ Faible

## 4. ANALYSE DES PRIX
- Grille tarifaire comparative
- Positionnement prix
- Stratégie recommandée

## 5. CARTE DE POSITIONNEMENT
Description d'une matrice de positionnement 2x2 avec les axes pertinents.

## 6. OPPORTUNITÉS DE DIFFÉRENCIATION
1. [Opportunité 1]: Comment l'exploiter
2. [Opportunité 2]: Comment l'exploiter
3. [Opportunité 3]: Comment l'exploiter

## 7. MENACES À SURVEILLER
1. [Menace 1]: Comment se préparer
2. [Menace 2]: Comment se préparer
3. [Menace 3]: Comment se préparer

## 8. RECOMMANDATIONS STRATÉGIQUES

### Court terme (0-3 mois)
- [Action 1]
- [Action 2]

### Moyen terme (3-12 mois)
- [Action 1]
- [Action 2]

### Long terme (12+ mois)
- [Action 1]
- [Action 2]

## 9. VEILLE CONCURRENTIELLE
- Sources à surveiller
- Fréquence de mise à jour
- Indicateurs à tracker

Sois factuel et objectif. Base ton analyse sur les informations fournies et les tendances du secteur {{industry}}.`
  },

  'executive-summary-generator': {
    fields: [
      { name: 'documentType', label: 'Type de document', type: 'select', required: true, options: [
        { value: 'business-plan', label: '📋 Business Plan' },
        { value: 'proposal', label: '📝 Proposition commerciale' },
        { value: 'report', label: '📊 Rapport d\'activité' },
        { value: 'project', label: '🎯 Projet' },
        { value: 'investment', label: '💰 Dossier d\'investissement' },
        { value: 'strategy', label: '🧭 Plan stratégique' }
      ]},
      { name: 'companyName', label: 'Entreprise/Projet', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'keyPoints', label: 'Points clés à inclure', type: 'textarea', placeholder: 'Listez les éléments essentiels du document...', required: true, rows: 5 },
      { name: 'objective', label: 'Objectif du document', type: 'textarea', placeholder: 'Que cherchez-vous à obtenir? (financement, approbation, vente...)', required: true, rows: 2 },
      { name: 'audience', label: 'Audience cible', type: 'select', options: [
        { value: 'investors', label: '💰 Investisseurs' },
        { value: 'executives', label: '👔 Direction/Comité' },
        { value: 'clients', label: '🤝 Clients/Prospects' },
        { value: 'partners', label: '🤝 Partenaires' },
        { value: 'board', label: '📋 Conseil d\'administration' }
      ]},
      { name: 'keyMetrics', label: 'Chiffres clés', type: 'textarea', placeholder: 'Ex: CA, croissance, marché, économies...', rows: 2 },
      { name: 'summaryLength', label: 'Longueur souhaitée', type: 'select', options: [
        { value: 'short', label: '📄 Court (1/2 page)' },
        { value: 'medium', label: '📃 Moyen (1 page)' },
        { value: 'detailed', label: '📑 Détaillé (1-2 pages)' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un rédacteur professionnel expert en communication exécutive. Rédige un résumé exécutif percutant.

DOCUMENT:
- Type: {{documentType}}
- Entreprise: {{companyName}}
- Objectif: {{objective}}
- Audience: {{audience}}
- Longueur: {{summaryLength}}

CONTENU À SYNTHÉTISER:
{{keyPoints}}

MÉTRIQUES CLÉS:
{{keyMetrics}}

Génère un résumé exécutif professionnel en {{language}}:

## RÉSUMÉ EXÉCUTIF

{{#if documentType === 'business-plan'}}
### L'Opportunité
[Problème de marché et opportunité en 2-3 phrases]

### Notre Solution
[Description de la solution et différenciateur]

### Le Marché
[Taille et potentiel]

### Notre Avantage
[Pourquoi nous allons réussir]

### Traction
[Résultats actuels et validation]

### L'Équipe
[Pourquoi cette équipe peut exécuter]

### La Demande
[Ce que nous cherchons et pourquoi]

### Projection
[Objectifs et retour attendu]
{{/if}}

{{#if documentType === 'proposal'}}
### Contexte
[Situation actuelle et besoin identifié]

### Notre Proposition
[Solution proposée en synthèse]

### Bénéfices Clés
- [Bénéfice 1 avec chiffre]
- [Bénéfice 2 avec chiffre]
- [Bénéfice 3 avec chiffre]

### Investissement
[Coût et ROI attendu]

### Prochaines Étapes
[Call to action clair]
{{/if}}

{{#if documentType === 'report'}}
### Période & Périmètre
[Contexte du rapport]

### Faits Saillants
- [Point clé 1]
- [Point clé 2]
- [Point clé 3]

### Performance
[Résultats vs objectifs]

### Défis & Solutions
[Problèmes rencontrés et résolutions]

### Perspectives
[Outlook et prochaines étapes]
{{/if}}

{{#if documentType === 'project'}}
### Le Projet en Bref
[Objectif et périmètre]

### Justification
[Pourquoi ce projet maintenant]

### Livrables Clés
- [Livrable 1]
- [Livrable 2]
- [Livrable 3]

### Ressources
[Budget, équipe, timeline]

### Risques & Mitigation
[Principaux risques et plans]

### Demande d'Approbation
[Ce qui est demandé]
{{/if}}

{{#if documentType === 'investment'}}
### Opportunité d'Investissement
[Hook accrocheur]

### Le Marché
[Taille et croissance]

### Notre Position
[Traction et différenciation]

### Financials
[Métriques clés et projections]

### L'Investissement
[Montant, valorisation, utilisation]

### Retour Attendu
[Scénarios de sortie]
{{/if}}

{{#if documentType === 'strategy'}}
### Vision
[Où nous allons]

### Diagnostic
[Situation actuelle]

### Axes Stratégiques
1. [Axe 1]: [Objectif]
2. [Axe 2]: [Objectif]
3. [Axe 3]: [Objectif]

### Ressources Clés
[Ce dont nous avons besoin]

### Jalons
[Timeline des accomplissements]
{{/if}}

---

**Point d'attention**: [Élément critique à retenir]

**Action requise**: [Ce que le lecteur doit faire]

Le résumé doit être autonome (compréhensible sans lire le document complet), orienté action, et adapté à {{audience}}. Longueur: {{summaryLength}}.`
  },

  'meeting-agenda-generator': {
    fields: [
      { name: 'meetingType', label: 'Type de réunion', type: 'select', required: true, options: [
        { value: 'team', label: '👥 Réunion d\'équipe' },
        { value: 'client', label: '🤝 Réunion client' },
        { value: 'board', label: '📋 Conseil d\'administration' },
        { value: 'project', label: '🎯 Revue de projet' },
        { value: 'brainstorm', label: '💡 Brainstorming' },
        { value: 'sales', label: '💼 Réunion commerciale' },
        { value: 'oneonone', label: '👤 One-on-One' },
        { value: 'kickoff', label: '🚀 Kickoff projet' }
      ]},
      { name: 'meetingTitle', label: 'Titre de la réunion', type: 'text', placeholder: 'Ex: Revue mensuelle Q1 2026', required: true },
      { name: 'objectives', label: 'Objectifs de la réunion', type: 'textarea', placeholder: 'Que devez-vous accomplir à la fin de cette réunion?', required: true, rows: 3 },
      { name: 'participants', label: 'Participants', type: 'textarea', placeholder: 'Listez les participants et leurs rôles', required: true, rows: 2 },
      { name: 'duration', label: 'Durée prévue', type: 'select', options: [
        { value: '30', label: '⏱️ 30 minutes' },
        { value: '45', label: '⏱️ 45 minutes' },
        { value: '60', label: '⏱️ 1 heure' },
        { value: '90', label: '⏱️ 1h30' },
        { value: '120', label: '⏱️ 2 heures' }
      ]},
      { name: 'topics', label: 'Sujets à aborder', type: 'textarea', placeholder: 'Listez les sujets principaux à couvrir', rows: 4 },
      { name: 'prework', label: 'Préparation requise', type: 'textarea', placeholder: 'Documents à lire, données à préparer...', rows: 2 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un facilitateur professionnel expert en organisation de réunions productives. Crée un ordre du jour structuré et efficace.

RÉUNION:
- Type: {{meetingType}}
- Titre: {{meetingTitle}}
- Durée: {{duration}} minutes
- Participants: {{participants}}

OBJECTIFS:
{{objectives}}

SUJETS:
{{topics}}

PRÉPARATION:
{{prework}}

Génère un ordre du jour professionnel en {{language}}:

# ORDRE DU JOUR

## {{meetingTitle}}
📅 Date: [À compléter]
⏰ Heure: [À compléter]
⏱️ Durée: {{duration}} minutes
📍 Lieu: [À compléter]

---

### 👥 PARTICIPANTS
{{participants}}

---

### 🎯 OBJECTIFS DE LA RÉUNION
{{#each objectives}}
- {{this}}
{{/each}}

---

### 📋 PRÉPARATION REQUISE
{{#if prework}}
{{prework}}
{{else}}
- Revoir les documents ci-joints
- Préparer vos questions/commentaires
{{/if}}

---

### 📝 DÉROULÉ

| Heure | Durée | Sujet | Responsable | Type |
|-------|-------|-------|-------------|------|
| 00:00 | 5 min | Accueil & Introduction | [Animateur] | Info |
{{#each topics}}
| [Heure] | [X] min | {{sujet}} | [Resp] | [Type] |
{{/each}}
| [Fin-5] | 5 min | Actions & Clôture | [Animateur] | Action |

**Types**: 📢 Info | 💬 Discussion | ✅ Décision | 💡 Brainstorm | 📊 Review

---

### 📌 DÉTAIL DES SUJETS

{{#each topics}}
#### {{index}}. {{titre}} ({{durée}} min)
**Objectif**: {{objectif}}
**Points à couvrir**:
- {{point1}}
- {{point2}}
**Questions clés**:
- {{question1}}
**Décision attendue**: {{decision}}
{{/each}}

---

### ✅ ACTIONS À DÉFINIR
| Action | Responsable | Échéance |
|--------|-------------|----------|
| [À définir en réunion] | | |

---

### 📎 DOCUMENTS JOINTS
- [Document 1]
- [Document 2]

---

### 💡 RÈGLES DE LA RÉUNION
- Téléphones en silencieux
- Une conversation à la fois
- Respecter les temps de parole
- Rester focalisé sur les objectifs

---

**Animateur**: [Nom]
**Compte-rendu par**: [Nom]

Adapte le niveau de formalité au type de réunion ({{meetingType}}).`
  },

  // ===== BATCH 2 - HIGH PRIORITY (8 outils) =====

  'proposal-generator': {
    fields: [
      { name: 'clientName', label: 'Nom du client', type: 'text', placeholder: 'Ex: Entreprise ABC', required: true },
      { name: 'projectTitle', label: 'Titre du projet', type: 'text', placeholder: 'Ex: Refonte du site web', required: true },
      { name: 'projectDescription', label: 'Description du projet', type: 'textarea', placeholder: 'Décrivez le projet en détail...', required: true, rows: 4 },
      { name: 'deliverables', label: 'Livrables prévus', type: 'textarea', placeholder: 'Listez les livrables...', rows: 3 },
      { name: 'timeline', label: 'Délai proposé', type: 'text', placeholder: 'Ex: 3 mois' },
      { name: 'budget', label: 'Budget proposé', type: 'text', placeholder: 'Ex: 500 000 DZD' },
      { name: 'yourCompany', label: 'Votre entreprise', type: 'text', placeholder: 'Ex: Ma Société SARL' },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en rédaction de propositions commerciales. Génère une proposition professionnelle et convaincante.

CLIENT: {{clientName}}
PROJET: {{projectTitle}}
DESCRIPTION: {{projectDescription}}
LIVRABLES: {{deliverables}}
DÉLAI: {{timeline}}
BUDGET: {{budget}}
VOTRE ENTREPRISE: {{yourCompany}}

Génère une proposition commerciale complète en {{language}} avec:
1. Page de garde professionnelle
2. Résumé exécutif
3. Compréhension des besoins client
4. Notre approche et méthodologie
5. Périmètre et livrables détaillés
6. Planning et jalons
7. Équipe proposée
8. Budget détaillé
9. Conditions et garanties
10. Prochaines étapes
11. Annexes (références, portfolio)`
  },

  'invoice-generator': {
    fields: [
      { name: 'clientName', label: 'Nom du client', type: 'text', placeholder: 'Ex: Entreprise ABC SARL', required: true },
      { name: 'clientAddress', label: 'Adresse du client', type: 'textarea', placeholder: 'Adresse complète...', rows: 2 },
      { name: 'items', label: 'Lignes de facturation', type: 'textarea', placeholder: 'Ex:\n- Service A: 50 000 DZD\n- Service B: 30 000 DZD', required: true, rows: 5 },
      { name: 'invoiceNumber', label: 'Numéro de facture', type: 'text', placeholder: 'Ex: FAC-2026-001' },
      { name: 'paymentTerms', label: 'Conditions de paiement', type: 'select', options: [
        { value: 'immediate', label: 'Paiement immédiat' },
        { value: '15days', label: '15 jours' },
        { value: '30days', label: '30 jours' },
        { value: '60days', label: '60 jours' }
      ]},
      { name: 'yourCompany', label: 'Votre entreprise', type: 'text', placeholder: 'Votre raison sociale' },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' }
      ]}
    ],
    promptTemplate: `Tu es un comptable expert. Génère une facture professionnelle conforme aux normes algériennes.

CLIENT: {{clientName}}
ADRESSE: {{clientAddress}}
PRESTATIONS: {{items}}
N° FACTURE: {{invoiceNumber}}
CONDITIONS: {{paymentTerms}}
ÉMETTEUR: {{yourCompany}}

Génère une facture professionnelle en {{language}} incluant:
1. En-tête avec coordonnées émetteur
2. Informations client
3. Date et numéro de facture
4. Tableau des prestations (description, quantité, prix unitaire HT, montant HT)
5. Total HT
6. TVA (19%)
7. Total TTC
8. Conditions de paiement
9. Coordonnées bancaires
10. Mentions légales obligatoires (NIF, RC, Art.)`
  },

  'contract-template-generator': {
    fields: [
      { name: 'contractType', label: 'Type de contrat', type: 'select', required: true, options: [
        { value: 'service', label: '🤝 Contrat de prestation de service' },
        { value: 'sale', label: '🛒 Contrat de vente' },
        { value: 'partnership', label: '🤝 Contrat de partenariat' },
        { value: 'nda', label: '🔒 Accord de confidentialité (NDA)' },
        { value: 'employment', label: '👔 Contrat de travail' },
        { value: 'freelance', label: '💼 Contrat freelance' }
      ]},
      { name: 'parties', label: 'Parties au contrat', type: 'textarea', placeholder: 'Décrivez les parties (noms, adresses, qualités)...', required: true, rows: 3 },
      { name: 'object', label: 'Objet du contrat', type: 'textarea', placeholder: 'Décrivez l\'objet précis du contrat...', required: true, rows: 3 },
      { name: 'duration', label: 'Durée du contrat', type: 'text', placeholder: 'Ex: 12 mois, CDI, mission ponctuelle' },
      { name: 'price', label: 'Prix / Rémunération', type: 'text', placeholder: 'Ex: 100 000 DZD' },
      { name: 'specificClauses', label: 'Clauses spécifiques', type: 'textarea', placeholder: 'Clauses particulières à inclure...', rows: 3 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' }
      ]}
    ],
    promptTemplate: `Tu es un juriste expert en droit des affaires algérien. Génère un modèle de contrat professionnel.

TYPE: {{contractType}}
PARTIES: {{parties}}
OBJET: {{object}}
DURÉE: {{duration}}
PRIX: {{price}}
CLAUSES SPÉCIFIQUES: {{specificClauses}}

Génère un contrat professionnel en {{language}} conforme au droit algérien incluant:
1. Identification des parties
2. Préambule
3. Article 1: Objet du contrat
4. Article 2: Durée
5. Article 3: Obligations des parties
6. Article 4: Prix et modalités de paiement
7. Article 5: Confidentialité
8. Article 6: Propriété intellectuelle (si applicable)
9. Article 7: Responsabilité et garanties
10. Article 8: Résiliation
11. Article 9: Force majeure
12. Article 10: Règlement des litiges
13. Article 11: Dispositions diverses
14. Signatures

Note: Ce modèle est fourni à titre indicatif. Consultez un avocat pour validation.`
  },

  'okr-generator': {
    fields: [
      { name: 'companyName', label: 'Entreprise / Équipe', type: 'text', placeholder: 'Ex: Équipe Marketing', required: true },
      { name: 'period', label: 'Période', type: 'select', options: [
        { value: 'q1', label: 'Q1 (Jan-Mars)' },
        { value: 'q2', label: 'Q2 (Avr-Juin)' },
        { value: 'q3', label: 'Q3 (Juil-Sept)' },
        { value: 'q4', label: 'Q4 (Oct-Déc)' },
        { value: 'annual', label: 'Annuel' }
      ]},
      { name: 'strategicGoals', label: 'Objectifs stratégiques', type: 'textarea', placeholder: 'Quels sont vos grands objectifs?', required: true, rows: 4 },
      { name: 'currentChallenges', label: 'Défis actuels', type: 'textarea', placeholder: 'Quels problèmes devez-vous résoudre?', rows: 3 },
      { name: 'resources', label: 'Ressources disponibles', type: 'textarea', placeholder: 'Budget, équipe, outils...', rows: 2 },
      { name: 'okrCount', label: 'Nombre d\'objectifs', type: 'select', options: [
        { value: '3', label: '3 Objectifs' },
        { value: '4', label: '4 Objectifs' },
        { value: '5', label: '5 Objectifs' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en management et en définition d'OKRs (Objectives & Key Results). Génère des OKRs SMART et ambitieux.

ÉQUIPE: {{companyName}}
PÉRIODE: {{period}}
OBJECTIFS STRATÉGIQUES: {{strategicGoals}}
DÉFIS: {{currentChallenges}}
RESSOURCES: {{resources}}

Génère {{okrCount}} OKRs en {{language}} avec:

Pour chaque Objectif:
- Énoncé inspirant et ambitieux
- 3-5 Key Results mesurables
- Initiatives clés pour atteindre chaque KR
- Indicateurs de suivi
- Responsable suggéré

Format:
## Objectif 1: [Énoncé inspirant]
- KR1: [Métrique de X à Y]
- KR2: [Métrique de X à Y]
- KR3: [Métrique de X à Y]

Initiatives:
- [Initiative 1]
- [Initiative 2]

Assure-toi que les KRs sont:
- Spécifiques et mesurables
- Ambitieux mais atteignables (70% de probabilité)
- Limités dans le temps
- Alignés avec la stratégie globale`
  },

  'kpi-dashboard-generator': {
    fields: [
      { name: 'businessType', label: 'Type d\'activité', type: 'select', required: true, options: [
        { value: 'saas', label: '💻 SaaS / Tech' },
        { value: 'ecommerce', label: '🛒 E-commerce' },
        { value: 'services', label: '🤝 Services' },
        { value: 'retail', label: '🏪 Retail' },
        { value: 'manufacturing', label: '🏭 Production' },
        { value: 'agency', label: '🎨 Agence' }
      ]},
      { name: 'department', label: 'Département', type: 'select', options: [
        { value: 'executive', label: '👔 Direction générale' },
        { value: 'sales', label: '💼 Commercial' },
        { value: 'marketing', label: '📢 Marketing' },
        { value: 'product', label: '⚙️ Produit' },
        { value: 'finance', label: '💰 Finance' },
        { value: 'hr', label: '👥 RH' },
        { value: 'operations', label: '🔧 Opérations' }
      ]},
      { name: 'objectives', label: 'Objectifs principaux', type: 'textarea', placeholder: 'Quels sont vos objectifs business?', required: true, rows: 3 },
      { name: 'currentMetrics', label: 'Métriques actuelles', type: 'textarea', placeholder: 'Quelles métriques suivez-vous déjà?', rows: 2 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en business intelligence et en définition de KPIs. Génère un dashboard de KPIs pertinent.

TYPE: {{businessType}}
DÉPARTEMENT: {{department}}
OBJECTIFS: {{objectives}}
MÉTRIQUES ACTUELLES: {{currentMetrics}}

Génère un dashboard de KPIs en {{language}} incluant:

## DASHBOARD {{department}} - {{businessType}}

### KPIs PRIMAIRES (5-7 indicateurs clés)
Pour chaque KPI:
- Nom du KPI
- Définition et formule
- Fréquence de mesure
- Objectif/Benchmark
- Seuils (vert/orange/rouge)
- Source de données

### KPIs SECONDAIRES (5-10 indicateurs de support)
[Même format]

### VISUALISATIONS RECOMMANDÉES
- Type de graphique pour chaque KPI
- Layout suggéré du dashboard
- Drill-down recommandés

### ALERTES & ACTIONS
- Quand déclencher une alerte
- Actions correctives suggérées

### OUTILS RECOMMANDÉS
- Excel/Google Sheets
- Power BI / Tableau
- Metabase / Looker
- Solutions spécifiques au secteur`
  },

  'project-brief-generator': {
    fields: [
      { name: 'projectName', label: 'Nom du projet', type: 'text', placeholder: 'Ex: Lancement App Mobile', required: true },
      { name: 'projectType', label: 'Type de projet', type: 'select', options: [
        { value: 'product', label: '📦 Lancement produit' },
        { value: 'marketing', label: '📢 Campagne marketing' },
        { value: 'tech', label: '💻 Projet technique' },
        { value: 'event', label: '🎉 Événement' },
        { value: 'internal', label: '🏢 Projet interne' }
      ]},
      { name: 'background', label: 'Contexte', type: 'textarea', placeholder: 'Pourquoi ce projet?', required: true, rows: 3 },
      { name: 'objectives', label: 'Objectifs', type: 'textarea', placeholder: 'Que devez-vous accomplir?', required: true, rows: 3 },
      { name: 'scope', label: 'Périmètre', type: 'textarea', placeholder: 'Ce qui est inclus / exclu', rows: 3 },
      { name: 'stakeholders', label: 'Parties prenantes', type: 'textarea', placeholder: 'Qui est impliqué?', rows: 2 },
      { name: 'budget', label: 'Budget', type: 'text', placeholder: 'Ex: 1M DZD' },
      { name: 'deadline', label: 'Date de livraison', type: 'text', placeholder: 'Ex: 30 Mars 2026' },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un chef de projet expert. Génère un brief de projet complet et professionnel.

PROJET: {{projectName}}
TYPE: {{projectType}}
CONTEXTE: {{background}}
OBJECTIFS: {{objectives}}
PÉRIMÈTRE: {{scope}}
PARTIES PRENANTES: {{stakeholders}}
BUDGET: {{budget}}
DEADLINE: {{deadline}}

Génère un brief de projet en {{language}} incluant:

## PROJECT BRIEF: {{projectName}}

### 1. RÉSUMÉ
[Synthèse en 3-4 phrases]

### 2. CONTEXTE & JUSTIFICATION
- Situation actuelle
- Problème/Opportunité
- Pourquoi maintenant

### 3. OBJECTIFS
- Objectifs SMART
- Critères de succès
- KPIs de mesure

### 4. PÉRIMÈTRE
#### Inclus
[Liste]
#### Exclu
[Liste]
#### Hypothèses
[Liste]

### 5. LIVRABLES
[Liste des livrables avec description]

### 6. PARTIES PRENANTES
| Rôle | Nom | Responsabilités |
|------|-----|-----------------|
[Tableau]

### 7. PLANNING PRÉVISIONNEL
| Phase | Dates | Jalons |
|-------|-------|--------|
[Tableau]

### 8. BUDGET
[Répartition budget]

### 9. RISQUES
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
[Tableau]

### 10. GOUVERNANCE
- Réunions prévues
- Reporting
- Processus de décision

### 11. PROCHAINES ÉTAPES
[Actions immédiates]

**Date**: [Date]
**Version**: 1.0
**Sponsor**: [Nom]
**Chef de projet**: [Nom]`
  },

  'company-description-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'industry', label: 'Secteur d\'activité', type: 'text', placeholder: 'Ex: FinTech, E-commerce', required: true },
      { name: 'productsServices', label: 'Produits/Services', type: 'textarea', placeholder: 'Décrivez ce que vous proposez...', required: true, rows: 3 },
      { name: 'targetMarket', label: 'Marché cible', type: 'textarea', placeholder: 'Qui sont vos clients?', rows: 2 },
      { name: 'uniqueValue', label: 'Valeur unique', type: 'textarea', placeholder: 'Ce qui vous différencie...', rows: 2 },
      { name: 'achievements', label: 'Réalisations clés', type: 'textarea', placeholder: 'Chiffres, clients, prix...', rows: 2 },
      { name: 'tone', label: 'Ton souhaité', type: 'select', options: [
        { value: 'professional', label: '👔 Professionnel/Corporate' },
        { value: 'startup', label: '🚀 Startup/Dynamique' },
        { value: 'friendly', label: '😊 Accessible/Humain' },
        { value: 'expert', label: '🎓 Expert/Technique' }
      ]},
      { name: 'length', label: 'Longueur', type: 'select', options: [
        { value: 'short', label: '📝 Court (50 mots)' },
        { value: 'medium', label: '📄 Moyen (100-150 mots)' },
        { value: 'long', label: '📃 Long (200-300 mots)' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en copywriting corporate. Génère une description d'entreprise engageante.

ENTREPRISE: {{companyName}}
SECTEUR: {{industry}}
PRODUITS/SERVICES: {{productsServices}}
MARCHÉ: {{targetMarket}}
VALEUR UNIQUE: {{uniqueValue}}
RÉALISATIONS: {{achievements}}
TON: {{tone}}
LONGUEUR: {{length}}

Génère des descriptions d'entreprise en {{language}}:

## VERSION COURTE (1 phrase)
[Pitch en une phrase percutante]

## VERSION RÉSEAUX SOCIAUX (Bio)
### LinkedIn
[160 caractères]
### Twitter/X
[160 caractères]
### Instagram
[150 caractères + hashtags]

## VERSION {{length}}
[Description principale adaptée à la longueur demandée]

## VERSION PAGE À PROPOS
[Description complète pour site web avec:
- Qui nous sommes
- Ce que nous faisons
- Pourquoi nous le faisons
- Ce qui nous rend uniques
- Call to action]

## VERSION SIGNATURE EMAIL
[2-3 lignes pour signature]

## VERSION COMMUNIQUÉ DE PRESSE
[Paragraphe boilerplate pour fin de communiqué]

Assure-toi que le ton ({{tone}}) est cohérent dans toutes les versions.`
  },

  'mission-vision-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'industry', label: 'Secteur d\'activité', type: 'text', placeholder: 'Ex: EdTech', required: true },
      { name: 'coreActivity', label: 'Activité principale', type: 'textarea', placeholder: 'Que fait votre entreprise?', required: true, rows: 2 },
      { name: 'targetBeneficiaries', label: 'Qui bénéficie de votre activité?', type: 'textarea', placeholder: 'Clients, utilisateurs, société...', rows: 2 },
      { name: 'longTermGoal', label: 'Objectif à long terme', type: 'textarea', placeholder: 'Quel impact voulez-vous avoir dans 10 ans?', rows: 2 },
      { name: 'coreValues', label: 'Valeurs fondamentales', type: 'textarea', placeholder: 'Listez 3-5 valeurs importantes pour vous', rows: 2 },
      { name: 'differentiator', label: 'Ce qui vous rend unique', type: 'textarea', placeholder: 'Votre approche distinctive', rows: 2 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en stratégie d'entreprise et en communication corporate. Génère des énoncés de mission, vision et valeurs percutants.

ENTREPRISE: {{companyName}}
SECTEUR: {{industry}}
ACTIVITÉ: {{coreActivity}}
BÉNÉFICIAIRES: {{targetBeneficiaries}}
OBJECTIF LT: {{longTermGoal}}
VALEURS: {{coreValues}}
DIFFÉRENCIATEUR: {{differentiator}}

Génère les éléments fondamentaux en {{language}}:

## MISSION
[Pourquoi l'entreprise existe - Ce qu'elle fait aujourd'hui]

### Version longue (2-3 phrases)
[Description complète de la raison d'être]

### Version courte (1 phrase)
[Énoncé concis et mémorable]

## VISION
[Où l'entreprise veut aller - L'avenir qu'elle construit]

### Version longue
[Description de l'impact futur souhaité]

### Version courte
[Énoncé inspirant en une phrase]

## VALEURS (5 valeurs)

### 1. [Valeur 1]
**Définition**: [Ce que ça signifie pour vous]
**En action**: [Comment ça se manifeste au quotidien]

### 2. [Valeur 2]
[Même format]

### 3. [Valeur 3]
[Même format]

### 4. [Valeur 4]
[Même format]

### 5. [Valeur 5]
[Même format]

## PROMESSE DE MARQUE
[Engagement envers les clients en une phrase]

## POSITIONNEMENT
[Ce qui vous différencie de la concurrence]

## CULTURE D'ENTREPRISE
[3-4 phrases sur l'environnement de travail et l'esprit d'équipe]

Les énoncés doivent être:
- Authentiques et spécifiques à {{companyName}}
- Inspirants mais réalistes
- Mémorables et faciles à communiquer
- Alignés avec {{coreValues}}`
  },

  // ===== BATCH 3 - MEDIUM PRIORITY (4 outils) =====

  'partnership-proposal': {
    fields: [
      { name: 'yourCompany', label: 'Votre entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'partnerCompany', label: 'Entreprise partenaire visée', type: 'text', placeholder: 'Ex: Grande Entreprise SA', required: true },
      { name: 'partnershipType', label: 'Type de partenariat', type: 'select', options: [
        { value: 'commercial', label: '🤝 Commercial (co-selling)' },
        { value: 'marketing', label: '📣 Marketing (co-marketing)' },
        { value: 'technology', label: '⚙️ Technologique (intégration)' },
        { value: 'distribution', label: '📦 Distribution' },
        { value: 'strategic', label: '🎯 Stratégique' },
        { value: 'affiliate', label: '💰 Affiliation' }
      ]},
      { name: 'valueForPartner', label: 'Valeur pour le partenaire', type: 'textarea', placeholder: 'Ce qu\'ils gagnent à travailler avec vous', required: true, rows: 3 },
      { name: 'valueForYou', label: 'Valeur pour vous', type: 'textarea', placeholder: 'Ce que vous gagnez de ce partenariat', required: true, rows: 3 },
      { name: 'proposedActivities', label: 'Activités proposées', type: 'textarea', placeholder: 'Webinars conjoints, co-promotion, intégration...', rows: 3 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en développement de partenariats stratégiques.

VOTRE ENTREPRISE : {{yourCompany}}
PARTENAIRE VISÉ : {{partnerCompany}}
TYPE : {{partnershipType}}
VALEUR PARTENAIRE : {{valueForPartner}}
VALEUR POUR VOUS : {{valueForYou}}
ACTIVITÉS : {{proposedActivities}}

Génère une proposition de partenariat professionnelle en {{language}}:

## 🤝 PROPOSITION DE PARTENARIAT

---

# PROPOSITION DE PARTENARIAT
## {{yourCompany}} × {{partnerCompany}}

**Date :** [Date]
**Préparée par :** [Nom], [Titre]
**Contact :** [Email] | [Téléphone]

---

## RÉSUMÉ EXÉCUTIF

[2-3 phrases résumant l'opportunité de partenariat et les bénéfices mutuels]

---

## 1. QUI SOMMES-NOUS ?

### {{yourCompany}}

**En bref :**
[Description courte de votre entreprise]

**Chiffres clés :**
- 📊 [Métrique 1 : clients, CA, croissance...]
- 👥 [Métrique 2 : audience, utilisateurs...]
- 🏆 [Réalisation notable]

**Notre expertise :**
- [Compétence 1]
- [Compétence 2]
- [Compétence 3]

---

## 2. POURQUOI {{partnerCompany}} ?

Nous avons identifié {{partnerCompany}} comme partenaire idéal car :

✅ **Complémentarité :** [Explication]
✅ **Audience commune :** [Explication]
✅ **Valeurs alignées :** [Explication]
✅ **Synergies potentielles :** [Explication]

---

## 3. L'OPPORTUNITÉ

### Le constat
[Problème ou opportunité du marché]

### La solution : un partenariat {{partnershipType}}
[Comment le partenariat répond à cette opportunité]

---

## 4. CE QUE NOUS PROPOSONS

### 4.1 Activités du partenariat

{{#if partnershipType === 'marketing'}}
**Co-Marketing :**
- 📝 Co-création de contenus (webinars, articles, études)
- 📧 Cross-promotion email
- 📱 Campagnes social media conjointes
- 🎤 Events co-brandés
{{/if}}

{{#if partnershipType === 'commercial'}}
**Co-Selling :**
- 🤝 Référencement mutuel de clients
- 📦 Offres bundlées
- 💰 Commission sur ventes référées
- 🎯 Leads partagés
{{/if}}

{{#if partnershipType === 'technology'}}
**Intégration Technologique :**
- 🔗 Intégration API
- 📲 Connecteur natif
- 🛠️ Développement conjoint
- 📚 Documentation commune
{{/if}}

### 4.2 Engagements mutuels

| {{yourCompany}} s'engage à | {{partnerCompany}} s'engage à |
|-----------------------------|--------------------------------|
| [Engagement 1] | [Engagement attendu 1] |
| [Engagement 2] | [Engagement attendu 2] |
| [Engagement 3] | [Engagement attendu 3] |

---

## 5. BÉNÉFICES POUR {{partnerCompany}}

🎯 **Pour vous :**

1. **[Bénéfice 1]**
   → [Détail et quantification]

2. **[Bénéfice 2]**
   → [Détail et quantification]

3. **[Bénéfice 3]**
   → [Détail et quantification]

**ROI estimé :** [Estimation]

---

## 6. MODÈLE ÉCONOMIQUE

### Option A : [Nom du modèle]
- [Description]
- Partage : [X/X]

### Option B : [Nom du modèle]
- [Description]
- Commission : [X%]

---

## 7. ROADMAP PROPOSÉE

| Phase | Durée | Actions | Objectifs |
|-------|-------|---------|-----------|
| Pilote | 3 mois | [Actions] | [KPIs] |
| Déploiement | 6 mois | [Actions] | [KPIs] |
| Optimisation | Ongoing | [Actions] | [KPIs] |

---

## 8. PROCHAINES ÉTAPES

1. 📞 Call de découverte (30 min)
2. 🤝 Rencontre équipes
3. 📝 Définition du scope
4. ✍️ Signature accord
5. 🚀 Lancement pilote

**Disponibilité :** [Dates proposées]

---

## 9. RÉFÉRENCES

### Partenariats existants
- [Partenaire 1] - [Type] - [Résultat]
- [Partenaire 2] - [Type] - [Résultat]

### Témoignage
> "[Citation d'un partenaire actuel]"
> — [Nom], [Titre], [Entreprise]

---

**CONTACT**

[Nom]
[Titre]
{{yourCompany}}

📧 [Email]
📱 [Téléphone]
🔗 [LinkedIn]

---

*Nous sommes convaincus que ce partenariat créera une valeur significative pour nos deux entreprises. Au plaisir d'en discuter !*`
  },

  'press-release-generator': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'announcementType', label: 'Type d\'annonce', type: 'select', required: true, options: [
        { value: 'product_launch', label: '🚀 Lancement produit' },
        { value: 'funding', label: '💰 Levée de fonds' },
        { value: 'partnership', label: '🤝 Partenariat' },
        { value: 'acquisition', label: '🏢 Acquisition' },
        { value: 'milestone', label: '🏆 Milestone/Record' },
        { value: 'event', label: '📅 Événement' },
        { value: 'executive', label: '👔 Nomination' },
        { value: 'expansion', label: '🌍 Expansion' }
      ]},
      { name: 'headline', label: 'Titre principal', type: 'text', placeholder: 'L\'annonce en une phrase percutante', required: true },
      { name: 'keyFacts', label: 'Faits clés à communiquer', type: 'textarea', placeholder: 'Tous les détails importants...', required: true, rows: 5 },
      { name: 'quotePerson', label: 'Personne citée (Nom, Titre)', type: 'text', placeholder: 'Ex: Mohamed Ali, CEO' },
      { name: 'quoteContent', label: 'Citation', type: 'textarea', placeholder: 'La citation à inclure dans le communiqué', rows: 2 },
      { name: 'releaseDate', label: 'Date de publication', type: 'text', placeholder: 'Ex: immediate, ou 15 janvier 2026' },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en relations presse et communication corporate.

ENTREPRISE : {{companyName}}
TYPE : {{announcementType}}
TITRE : {{headline}}
FAITS : {{keyFacts}}
CITATION PAR : {{quotePerson}}
CITATION : {{quoteContent}}
DATE : {{releaseDate}}

Génère un communiqué de presse professionnel en {{language}}:

## 📰 COMMUNIQUÉ DE PRESSE

---

**COMMUNIQUÉ DE PRESSE**
{{#if releaseDate === 'immediate'}}
**Pour diffusion immédiate**
{{else}}
**Embargo jusqu'au {{releaseDate}}**
{{/if}}

---

# {{headline}}

**[Sous-titre accrocheur résumant l'annonce]**

---

**[Ville], le [Date]** — {{companyName}} [verbe d'action] [annonce principale en une phrase percutante].

[Paragraphe 1 : Développement de l'annonce - Quoi, Qui, Quand, Où, Pourquoi]

[Paragraphe 2 : Contexte et importance de l'annonce]

{{#if announcementType === 'funding'}}
Cette levée de fonds de [montant] a été menée par [investisseur lead], avec la participation de [autres investisseurs]. Les fonds seront utilisés pour [objectifs : recrutement, R&D, expansion...].
{{/if}}

{{#if announcementType === 'product_launch'}}
[Nom du produit] permet à [audience cible] de [bénéfice principal]. Parmi les fonctionnalités clés : [liste des features principales].
{{/if}}

---

{{#if quoteContent}}
**« {{quoteContent}} »** déclare {{quotePerson}}.
{{/if}}

---

[Paragraphe 3 : Détails supplémentaires, chiffres, impact]

[Paragraphe 4 : Prochaines étapes ou disponibilité]

---

### À PROPOS DE {{companyName}}

{{companyName}} est [description factuelle de l'entreprise en 2-3 phrases]. Fondée en [année], l'entreprise [activité principale]. [Chiffre clé ou fait notable].

Pour plus d'informations : [site web]

---

### CONTACT PRESSE

**[Nom du contact]**
[Titre]
📧 [Email presse]
📱 [Téléphone]

---

### RESSOURCES

- 🖼️ Kit presse : [Lien]
- 📸 Photos HD : [Lien]
- 🎥 Vidéo : [Lien si applicable]

---

**###**

*[Note aux rédacteurs si nécessaire]*

---

## VERSIONS ALTERNATIVES

### Version courte (100 mots)
*Pour : Dépêches, réseaux sociaux*

"{{companyName}} annonce [annonce] [date]. [Détail principal]. [Citation courte]. [Call-to-action]."

### Version email pitch journaliste

**Objet :** [Accroche journalistique] - {{companyName}}

"Bonjour [Prénom],

[1 phrase d'accroche personnalisée]

{{companyName}} vient de [annonce] et je pense que cela pourrait intéresser vos lecteurs car [angle éditorial].

**En bref :**
- [Fait 1]
- [Fait 2]
- [Fait 3]

Je serais ravi de vous envoyer le communiqué complet ou d'organiser une interview avec [porte-parole].

Cordialement,
[Signature]"`
  },

  'job-description-generator': {
    fields: [
      { name: 'jobTitle', label: 'Intitulé du poste', type: 'text', placeholder: 'Ex: Développeur Full Stack Senior', required: true },
      { name: 'department', label: 'Département/Équipe', type: 'text', placeholder: 'Ex: Tech, Marketing, Commercial' },
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'location', label: 'Localisation', type: 'text', placeholder: 'Ex: Alger, Hydra / Remote possible' },
      { name: 'contractType', label: 'Type de contrat', type: 'select', options: [
        { value: 'cdi', label: '📋 CDI' },
        { value: 'cdd', label: '📄 CDD' },
        { value: 'freelance', label: '💼 Freelance' },
        { value: 'stage', label: '🎓 Stage' },
        { value: 'alternance', label: '📚 Alternance' }
      ]},
      { name: 'experienceLevel', label: 'Niveau d\'expérience', type: 'select', options: [
        { value: 'junior', label: '🌱 Junior (0-2 ans)' },
        { value: 'confirmed', label: '💼 Confirmé (2-5 ans)' },
        { value: 'senior', label: '⭐ Senior (5-8 ans)' },
        { value: 'lead', label: '🎯 Lead (8+ ans)' },
        { value: 'executive', label: '👔 Executive' }
      ]},
      { name: 'responsibilities', label: 'Missions principales', type: 'textarea', placeholder: 'Décrivez les responsabilités...', required: true, rows: 4 },
      { name: 'requirements', label: 'Compétences requises', type: 'textarea', placeholder: 'Compétences, expérience, formation...', required: true, rows: 4 },
      { name: 'salaryRange', label: 'Fourchette de salaire (optionnel)', type: 'text', placeholder: 'Ex: 150 000 - 200 000 DZD/mois' },
      { name: 'benefits', label: 'Avantages', type: 'textarea', placeholder: 'Avantages, culture, équipe...', rows: 3 },
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'ar', label: '🇩🇿 Arabe' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert en recrutement et marque employeur.

POSTE : {{jobTitle}}
DÉPARTEMENT : {{department}}
ENTREPRISE : {{companyName}}
LIEU : {{location}}
CONTRAT : {{contractType}}
NIVEAU : {{experienceLevel}}
MISSIONS : {{responsibilities}}
COMPÉTENCES : {{requirements}}
SALAIRE : {{salaryRange}}
AVANTAGES : {{benefits}}

Génère une offre d'emploi attractive en {{language}}:

## 👔 OFFRE D'EMPLOI

---

# {{jobTitle}}
## {{companyName}} | {{location}}

**Type :** {{contractType}}
**Expérience :** {{experienceLevel}}
**Département :** {{department}}
{{#if salaryRange}}**Rémunération :** {{salaryRange}}{{/if}}

---

### 🚀 REJOIGNEZ L'AVENTURE {{companyName}} !

[Accroche engageante sur l'entreprise et le contexte du recrutement]

---

### 🎯 VOTRE MISSION

En tant que {{jobTitle}}, vous serez responsable de :

**Responsabilités principales :**
- [Mission 1 - avec impact attendu]
- [Mission 2 - avec impact attendu]
- [Mission 3 - avec impact attendu]
- [Mission 4 - avec impact attendu]
- [Mission 5 - avec impact attendu]

**Au quotidien, vous allez :**
- [Activité quotidienne 1]
- [Activité quotidienne 2]
- [Activité quotidienne 3]

---

### 👤 VOTRE PROFIL

**Indispensable :**
- ✅ [Compétence requise 1]
- ✅ [Compétence requise 2]
- ✅ [Compétence requise 3]
- ✅ [X] années d'expérience en [domaine]

**Un plus :**
- ➕ [Compétence bonus 1]
- ➕ [Compétence bonus 2]
- ➕ [Compétence bonus 3]

**Soft skills :**
- 💡 [Qualité 1]
- 🤝 [Qualité 2]
- 📈 [Qualité 3]

---

### 🎁 CE QUE NOUS OFFRONS

{{#if salaryRange}}
💰 **Rémunération :** {{salaryRange}}
{{/if}}

**Avantages :**
- [Avantage 1 : Télétravail, RTT...]
- [Avantage 2 : Tickets resto, mutuelle...]
- [Avantage 3 : Formation, évolution...]
- [Avantage 4 : Équipe, culture...]
- [Avantage 5 : Équipement, bureaux...]

---

### 🏢 POURQUOI {{companyName}} ?

**Notre culture :**
[Description de la culture d'entreprise]

**Nos valeurs :**
- [Valeur 1]
- [Valeur 2]
- [Valeur 3]

**Témoignage équipe :**
> "[Citation d'un membre de l'équipe]"
> — [Prénom], [Poste]

---

### 📝 PROCESSUS DE RECRUTEMENT

1. 📞 Échange téléphonique (15 min)
2. 💻 Entretien visio RH (45 min)
3. 🎯 Entretien technique/métier (1h)
4. 🤝 Rencontre équipe (30 min)
5. ✅ Offre

**Délai moyen :** [X] semaines

---

### 📩 POSTULER

Envoyez votre CV et lettre de motivation à : [email]

Ou postulez directement sur : [lien]

---

*{{companyName}} s'engage en faveur de la diversité et de l'égalité des chances. Tous nos postes sont ouverts aux personnes en situation de handicap.*

---

## VERSION LINKEDIN

**[Version optimisée pour LinkedIn Jobs - 2000 caractères]**

## VERSION INDEED

**[Version optimisée pour Indeed - avec mots-clés]**`
  },

  'onboarding-checklist': {
    fields: [
      { name: 'companyName', label: 'Nom de l\'entreprise', type: 'text', placeholder: 'Ex: TechStart Algeria', required: true },
      { name: 'department', label: 'Département', type: 'text', placeholder: 'Ex: Tech, Marketing, Commercial' },
      { name: 'role', label: 'Poste du nouvel employé', type: 'text', placeholder: 'Ex: Développeur Frontend', required: true },
      { name: 'startDate', label: 'Date de début', type: 'text', placeholder: 'Ex: 1er Février 2026' },
      { name: 'manager', label: 'Manager direct', type: 'text', placeholder: 'Nom du responsable' },
      { name: 'tools', label: 'Outils utilisés', type: 'textarea', placeholder: 'Ex: Slack, Jira, Figma, GitHub...', rows: 2 },
      { name: 'teamSize', label: 'Taille de l\'équipe', type: 'select', options: [
        { value: 'small', label: '👥 Petite (2-5)' },
        { value: 'medium', label: '👨‍👩‍👧‍👦 Moyenne (6-15)' },
        { value: 'large', label: '🏢 Grande (15+)' }
      ]},
      { name: 'workMode', label: 'Mode de travail', type: 'select', options: [
        { value: 'onsite', label: '🏢 Présentiel' },
        { value: 'remote', label: '🏠 Full remote' },
        { value: 'hybrid', label: '🔄 Hybride' }
      ]},
      { name: 'language', label: 'Langue', type: 'select', options: [
        { value: 'fr', label: '🇫🇷 Français' },
        { value: 'en', label: '🇬🇧 Anglais' }
      ]}
    ],
    promptTemplate: `Tu es un expert RH en intégration des nouveaux employés. Génère une checklist d'onboarding complète.

ENTREPRISE: {{companyName}}
DÉPARTEMENT: {{department}}
POSTE: {{role}}
DATE DÉBUT: {{startDate}}
MANAGER: {{manager}}
OUTILS: {{tools}}
ÉQUIPE: {{teamSize}}
MODE: {{workMode}}

Génère une checklist d'onboarding en {{language}}:

# CHECKLIST D'INTÉGRATION
## {{role}} - {{department}}
### {{companyName}}

---

## AVANT L'ARRIVÉE (Jour J-7 à J-1)

### Administration RH
- [ ] Contrat de travail signé
- [ ] Documents administratifs collectés
- [ ] Compte bancaire pour salaire
- [ ] Assurance/mutuelle activée
- [ ] Badge d'accès commandé
- [ ] Place de parking (si applicable)

### Préparation technique
- [ ] Ordinateur configuré
- [ ] Écran(s) / périphériques
- [ ] Email professionnel créé
- [ ] Accès outils: {{tools}}
- [ ] Licences logiciels activées
- [ ] VPN configuré (si remote)

### Communication
- [ ] Annonce à l'équipe
- [ ] Buddy/Mentor assigné
- [ ] Planning première semaine
- [ ] Réservation salle pour accueil

---

## JOUR 1 - L'ACCUEIL

### Matin
- [ ] Accueil par {{manager}} ou RH
- [ ] Tour des locaux
- [ ] Présentation à l'équipe
- [ ] Remise du matériel
- [ ] Configuration des accès

### Après-midi
- [ ] Présentation de l'entreprise (vision, valeurs, organisation)
- [ ] Lecture du handbook/wiki
- [ ] Installation des outils
- [ ] Premier 1:1 avec manager

---

## SEMAINE 1 - LA DÉCOUVERTE

### Jour 2
- [ ] Formation outils internes
- [ ] Accès documentation
- [ ] Premier déjeuner d'équipe
- [ ] Introduction aux process

### Jour 3
- [ ] Shadow d'un collègue
- [ ] Premier projet/tâche simple
- [ ] Point avec buddy

### Jour 4
- [ ] Formation spécifique au rôle
- [ ] Participation première réunion d'équipe
- [ ] Revue des objectifs de la période d'essai

### Jour 5
- [ ] Point de fin de semaine avec manager
- [ ] Feedback sur l'accueil
- [ ] Planning semaine 2

---

## SEMAINE 2-4 - L'INTÉGRATION

### Semaine 2
- [ ] Premiers livrables autonomes
- [ ] Rencontres cross-team
- [ ] Approfondissement technique
- [ ] Point hebdo manager

### Semaine 3
- [ ] Responsabilités accrues
- [ ] Contribution aux rituels d'équipe
- [ ] Formation continue
- [ ] Feedback 360

### Semaine 4
- [ ] Bilan du premier mois
- [ ] Ajustement des objectifs
- [ ] Plan de développement
- [ ] Célébration milestone

---

## MOIS 2-3 - L'AUTONOMIE

### Mois 2
- [ ] Projets en autonomie
- [ ] Mentorat si applicable
- [ ] Participation aux décisions
- [ ] Mid-review période d'essai

### Mois 3
- [ ] Pleine autonomie
- [ ] Contributions significatives
- [ ] Validation période d'essai
- [ ] Plan de carrière initial

---

## RESSOURCES

### Contacts clés
| Rôle | Nom | Contact |
|------|-----|---------|
| Manager | {{manager}} | |
| RH | | |
| IT Support | | |
| Buddy | | |

### Documents importants
- [ ] Handbook employé
- [ ] Organigramme
- [ ] Politique remote (si {{workMode}})
- [ ] Avantages & congés

### Outils à maîtriser
{{tools}}

---

**Responsable onboarding**: [Nom]
**Date création**: [Date]`
  }
};

// Icônes par subcategory
const subcategoryIcons: Record<string, any> = {
  planning: ClipboardList,
  strategy: Target,
  fundraising: DollarSign,
  marketing: Megaphone,
  documents: FileCheck,
  productivity: BarChart3,
  hr: Users,
};

export default function BusinessToolPage() {
  const params = useParams();
  const toolSlug = params.toolSlug as string;

  const tool = getToolBySlug('business', toolSlug);
  const formConfig = formConfigs[toolSlug];

  const [formData, setFormData] = useState<Record<string, string>>({});
  const [generatedContent, setGeneratedContent] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);

  if (!tool) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Outil non trouvé</h1>
          <Link href="/tools/business" className="text-indigo-600 hover:underline">
            Retour aux outils Business
          </Link>
        </div>
      </div>
    );
  }

  const SubcategoryIcon = subcategoryIcons[tool.subcategory || 'planning'] || Briefcase;

  const handleInputChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulation de génération
    setTimeout(() => {
      let prompt = formConfig?.promptTemplate || '';
      Object.entries(formData).forEach(([key, value]) => {
        prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), value);
      });
      setGeneratedContent(`# Résultat généré\n\n${prompt.substring(0, 500)}...\n\n[Contenu complet généré par l'IA]`);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/business" className="text-gray-400 hover:text-gray-600">
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

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-8">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-indigo-100 rounded-xl flex items-center justify-center">
              <SubcategoryIcon className="w-8 h-8 text-indigo-600" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
                {tool.priority === 'critical' && (
                  <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-medium flex items-center gap-1">
                    <Zap className="w-3 h-3" /> Essentiel
                  </span>
                )}
              </div>
              <p className="text-gray-600">{tool.description.fr}</p>
              <div className="flex items-center gap-4 mt-3">
                <span className="text-sm text-gray-500">
                  <Star className="w-4 h-4 inline mr-1 text-yellow-500" />
                  {tool.credits} crédits
                </span>
                <span className="text-sm text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                  {tool.subcategory}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Formulaire */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-indigo-600" />
              Paramètres
            </h2>

            {formConfig ? (
              <div className="space-y-4">
                {formConfig.fields.map((field) => (
                  <div key={field.name}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {field.label}
                      {field.required && <span className="text-red-500 ml-1">*</span>}
                    </label>

                    {field.type === 'text' && (
                      <input
                        type="text"
                        placeholder={field.placeholder}
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    )}

                    {field.type === 'textarea' && (
                      <textarea
                        placeholder={field.placeholder}
                        rows={field.rows || 3}
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    )}

                    {field.type === 'select' && (
                      <select
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value="">Sélectionner...</option>
                        {field.options?.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    )}

                    {field.type === 'number' && (
                      <input
                        type="number"
                        placeholder={field.placeholder}
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    )}
                  </div>
                ))}

                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="w-full mt-6 bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Génération en cours...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Générer ({tool.credits} crédits)
                    </>
                  )}
                </button>
              </div>
            ) : (
              <p className="text-gray-500">Configuration du formulaire en cours de développement.</p>
            )}
          </div>

          {/* Résultat */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              Résultat
            </h2>

            {generatedContent ? (
              <div className="prose prose-sm max-w-none">
                <div className="bg-gray-50 rounded-lg p-4 whitespace-pre-wrap font-mono text-sm">
                  {generatedContent}
                </div>
                <div className="flex gap-2 mt-4">
                  <button className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200">
                    Copier
                  </button>
                  <button className="flex-1 bg-indigo-100 text-indigo-700 py-2 px-4 rounded-lg hover:bg-indigo-200">
                    Télécharger
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <Briefcase className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Le résultat apparaîtra ici</p>
              </div>
            )}
          </div>
        </div>

        {/* Related Tools */}
        <div className="mt-12">
          <h2 className="text-xl font-semibold mb-4">Outils similaires</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {businessTools
              .filter(t => t.subcategory === tool.subcategory && t.id !== tool.id)
              .slice(0, 4)
              .map(relatedTool => (
                <Link
                  key={relatedTool.id}
                  href={`/tools/business/${relatedTool.slug}`}
                  className="bg-white rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <h3 className="font-medium text-gray-900 text-sm">{relatedTool.name.fr}</h3>
                  <p className="text-xs text-gray-500 mt-1">{relatedTool.credits} crédits</p>
                </Link>
              ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria - Conçu en Algérie
          </p>
        </div>
      </footer>
    </div>
  );
}
