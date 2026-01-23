import { AITool } from '../../types';

export const cnasAssistant: AITool = {
    id: 'cnas-assistant',
    slug: 'cnas-assistant',
    name: {
        fr: 'Assistant CNAS',
        ar: 'مساعد الصندوق الوطني للتأمينات الاجتماعية',
        en: 'CNAS Assistant'
    },
    description: {
        fr: 'Guide complet pour toutes les démarches CNAS : remboursements, arrêts maladie, maternité, accidents de travail',
        ar: 'دليل شامل لجميع إجراءات الصندوق الوطني للتأمينات الاجتماعية',
        en: 'Complete guide for CNAS procedures'
    },
    category: 'admin-dz',
    subcategory: 'securite-sociale',
    icon: 'ShieldCheck',
    credits: 15,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande',
            type: 'select',
            label: 'Type de demande',
            required: true,
            options: [
                'Remboursement soins',
                'Arrêt maladie / Indemnités journalières',
                'Congé maternité',
                'Accident de travail',
                'Maladie professionnelle',
                'Carte Chifa',
                'Affiliation / Immatriculation',
                'Attestation d\'affiliation',
                'Déclaration ayants droit',
                'Autre question'
            ]
        },
        { name: 'situation', type: 'select', label: 'Vous êtes', options: ['Salarié', 'Employeur', 'Retraité', 'Ayant droit'] },
        { name: 'wilaya', type: 'select', label: 'Wilaya', options: ['Alger', 'Oran', 'Constantine', 'Annaba', 'Blida', 'Sétif', 'Batna', 'Tizi Ouzou', 'Béjaïa', 'Autre'] },
        { name: 'question', type: 'textarea', label: 'Décrivez votre situation ou question', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'response' }],
    promptTemplate: `Tu es un expert de la CNAS (Caisse Nationale des Assurances Sociales) en Algérie.

TYPE DE DEMANDE : {{type_demande}}
SITUATION : {{situation}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

RÉPONDS DE MANIÈRE STRUCTURÉE :

## 📋 Réponse à votre demande

### 1. Explication de vos droits
[Explique clairement les droits selon la législation algérienne]

### 2. Documents requis
- [ ] Document 1 (où l'obtenir)
- [ ] Document 2 (où l'obtenir)
- [ ] ...

### 3. Démarches à suivre
1. **Étape 1** : [Action + lieu]
2. **Étape 2** : [Action + lieu]
3. ...

### 4. Délais légaux
- Délai de traitement : X jours
- Délai de remboursement : X jours

### 5. Coordonnées utiles ({{wilaya}})
- Adresse agence CNAS : [si connue]
- Téléphone : 3030 (numéro vert CNAS)
- Site web : www.cnas.dz

### 6. Conseils pratiques
💡 [Astuces pour accélérer la procédure]

### ⚖️ Base légale
- Loi n°83-11 du 2 juillet 1983
- [Autres textes pertinents]

Sois précis, pratique et oriente vers les bonnes ressources.`,
    model: 'claude',
    estimatedTime: '45s'
};

export const casnosSimulator: AITool = {
    id: 'casnos-simulator',
    slug: 'casnos-simulator',
    name: {
        fr: 'Simulateur CASNOS',
        ar: 'محاكي كاسنوس',
        en: 'CASNOS Simulator'
    },
    description: {
        fr: 'Calculez vos cotisations CASNOS et simulez vos droits à la retraite pour non-salariés',
        ar: 'احسب اشتراكاتك في صندوق الضمان الاجتماعي لغير الأجراء',
        en: 'Calculate CASNOS contributions for self-employed'
    },
    category: 'admin-dz',
    subcategory: 'securite-sociale',
    icon: 'Calculator',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        { name: 'activite', type: 'select', label: 'Type d\'activité', options: ['Commerçant', 'Artisan', 'Profession libérale', 'Agriculteur', 'Auto-entrepreneur'] },
        { name: 'revenu_annuel', type: 'number', label: 'Revenu annuel déclaré (DZD)', required: true },
        { name: 'annees_cotisation', type: 'number', label: 'Années de cotisation', default: 0 },
        { name: 'age', type: 'number', label: 'Votre âge' },
        { name: 'simulation_type', type: 'select', label: 'Type de simulation', options: ['Cotisation annuelle', 'Retraite', 'Droits maladie'], default: 'Cotisation annuelle' }
    ],
    outputs: [{ type: 'markdown', name: 'simulationResult' }],
    promptTemplate: `Tu es un expert CASNOS (Caisse Nationale de Sécurité Sociale des Non-Salariés) en Algérie.

ACTIVITÉ : {{activite}}
REVENU ANNUEL : {{revenu_annuel}} DZD
ANNÉES DE COTISATION : {{annees_cotisation}}
ÂGE : {{age}} ans
TYPE SIMULATION : {{simulation_type}}

## 📊 Simulation CASNOS

### 1. Calcul des cotisations
Base de cotisation : {{revenu_annuel}} DZD

| Type de cotisation | Taux | Montant annuel |
|-------------------|------|----------------|
| Assurance maladie | 12% | X DZD |
| Retraite | 6% | X DZD |
| **TOTAL** | **18%** | **X DZD** |

Cotisation trimestrielle : X DZD
Cotisation mensuelle : X DZD

### 2. Échéances de paiement
- 1er trimestre : avant le 30 mars
- 2ème trimestre : avant le 30 juin
- 3ème trimestre : avant le 30 septembre
- 4ème trimestre : avant le 30 décembre

### 3. {{#if simulation_type === 'retraite'}}Simulation retraite
Avec {{annees_cotisation}} années de cotisation :
- Âge de départ : 60 ans (hommes) / 55 ans (femmes)
- Pension estimée : X DZD/mois
- Taux de remplacement : X%
{{/if}}

### 4. Vos droits actuels
- ✅ Couverture maladie : [Oui/Non]
- ✅ Allocations familiales : [Oui/Non]
- ✅ Indemnités journalières : [Oui/Non]

### 5. Comment payer
- En ligne : portail.casnos.dz
- CCP / BaridiMob
- Agence CASNOS

### ⚠️ Pénalités de retard
10% de majoration après l'échéance

Base légale : Loi 83-14, Décret 85-35`,
    model: 'claude',
    estimatedTime: '30s'
};

export const impotsDzAssistant: AITool = {
    id: 'impots-dz-assistant',
    slug: 'impots-dz-assistant',
    name: {
        fr: 'Assistant Impôts DZ',
        ar: 'مساعد الضرائب الجزائرية',
        en: 'Algeria Tax Assistant'
    },
    description: {
        fr: 'Guide fiscal algérien : IRG, IBS, TVA, TAP, déclarations G50 et bilans fiscaux',
        ar: 'دليل الضرائب الجزائرية: الضريبة على الدخل، الضريبة على أرباح الشركات',
        en: 'Algerian tax guide: IRG, IBS, VAT'
    },
    category: 'admin-dz',
    subcategory: 'fiscalite',
    icon: 'Receipt',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_impot', type: 'select', label: 'Type d\'impôt', required: true, options: [
                'IRG sur salaires',
                'IRG professions libérales',
                'IBS (Impôt sur Bénéfices des Sociétés)',
                'TVA',
                'TAP (Taxe sur Activité Professionnelle)',
                'Déclaration G50',
                'Bilan fiscal annuel'
            ]
        },
        { name: 'statut', type: 'select', label: 'Statut', options: ['Salarié', 'Auto-entrepreneur', 'EURL/SARL', 'SPA', 'Profession libérale'] },
        { name: 'montant', type: 'number', label: 'Montant concerné (DZD)' },
        { name: 'question', type: 'textarea', label: 'Votre question fiscale', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'taxResponse' }],
    promptTemplate: `Tu es un expert fiscal algérien (inspecteur des impôts expérimenté).

TYPE D'IMPÔT : {{type_impot}}
STATUT : {{statut}}
MONTANT : {{montant}} DZD
QUESTION : {{question}}

## 🧾 Réponse fiscale

### 1. Explication du régime fiscal
[Explication claire selon le Code des Impôts Directs et Taxes Assimilées]

### 2. Calcul détaillé
{{#if type_impot === 'irg_salaire'}}
**Barème IRG 2024 :**
| Tranche de revenu | Taux |
|-------------------|------|
| 0 - 240 000 DZD | 0% |
| 240 001 - 480 000 DZD | 23% |
| 480 001 - 960 000 DZD | 27% |
| 960 001 - 1 920 000 DZD | 30% |
| 1 920 001 - 3 840 000 DZD | 33% |
| > 3 840 000 DZD | 35% |

Abattement forfaitaire : 40% (min 12 000 DZD, max 18 000 DZD/mois)
{{/if}}

{{#if type_impot === 'tva'}}
**Taux TVA en Algérie :**
- Taux normal : 19%
- Taux réduit : 9%
{{/if}}

### 3. Obligations déclaratives
- Formulaire : [G50 / Série G / etc.]
- Échéance : [Date limite]
- Où déposer : Centre des Impôts de votre commune

### 4. Pièces justificatives
- [ ] Document 1
- [ ] Document 2

### 5. Pénalités en cas de retard
- Majoration : 10% le 1er mois, 3% par mois supplémentaire
- Intérêts de retard : 4% par an

### 💡 Conseils d'optimisation fiscale (légaux)
[Suggestions pour réduire légalement la charge fiscale]

### ⚖️ Références légales
- Code des Impôts Directs (CIDTA)
- Code des Taxes sur le Chiffre d'Affaires
- Loi de Finances 2024`,
    model: 'claude',
    estimatedTime: '60s'
};

export const cnrcAssistant: AITool = {
    id: 'cnrc-assistant',
    slug: 'cnrc-assistant',
    name: {
        fr: 'Assistant CNRC',
        ar: 'مساعد السجل التجاري',
        en: 'Trade Register Assistant'
    },
    description: {
        fr: 'Création d\'entreprise, registre du commerce, modifications statutaires, radiation',
        ar: 'إنشاء الشركات، السجل التجاري، التعديلات',
        en: 'Business registration and trade register'
    },
    category: 'admin-dz',
    subcategory: 'entreprise',
    icon: 'Building2',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
                'Création d\'entreprise',
                'Modification (adresse, activité, gérant...)',
                'Renouvellement registre commerce',
                'Radiation / Fermeture',
                'Extrait de registre du commerce',
                'Vérification nom commercial'
            ]
        },
        { name: 'forme_juridique', type: 'select', label: 'Forme juridique', options: ['Auto-entrepreneur', 'EURL', 'SARL', 'SPA', 'SNC', 'Personne physique'] },
        { name: 'activite', type: 'text', label: 'Activité envisagée' },
        { name: 'wilaya', type: 'select', label: 'Wilaya d\'implantation', options: ['Alger', 'Oran', 'Constantine', 'Annaba', 'Autre'] },
        { name: 'question', type: 'textarea', label: 'Votre question', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'cnrcGuide' }],
    promptTemplate: `Tu es un expert du Centre National du Registre du Commerce (CNRC) en Algérie.

TYPE DE DEMANDE : {{type_demande}}
FORME JURIDIQUE : {{forme_juridique}}
ACTIVITÉ : {{activite}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🏢 Guide CNRC

### 1. Procédure {{type_demande}}

{{#if type_demande === 'creation'}}
**Étapes de création d'entreprise ({{forme_juridique}}) :**

1. **Vérification du nom commercial**
   - Site : www.cnrc.dz
   - Coût : Gratuit en ligne

2. **Constitution du dossier**
   Documents requis :
   - [ ] Acte de naissance n°12
   - [ ] Certificat de résidence
   - [ ] Casier judiciaire (bulletin n°3)
   - [ ] Justificatif du local (contrat de location ou titre de propriété)
   - [ ] Statuts (pour EURL/SARL/SPA)
   - [ ] Attestation de dépôt de capital (pour sociétés)
   - [ ] Formulaires CNRC

3. **Dépôt du dossier**
   - Lieu : Antenne CNRC de {{wilaya}}
   - Coût : ~X DZD (selon forme juridique)

4. **Retrait du registre du commerce**
   - Délai : 24-72h
{{/if}}

### 2. Coûts estimés
| Élément | Montant |
|---------|---------|
| Immatriculation | X DZD |
| Timbres fiscaux | X DZD |
| Publication BOAL | X DZD |
| **Total estimé** | **X DZD** |

### 3. Contacts CNRC {{wilaya}}
- Adresse : [Adresse antenne locale]
- Tél : [Numéro]
- Site : www.cnrc.dz
- E-services : sidjilcom.cnrc.dz

### 4. Délais
- Traitement : 24-72h
- Validité registre : 2 ans (renouvellement obligatoire)

### ⚖️ Base légale
- Code de Commerce algérien
- Décret exécutif 97-41`,
    model: 'claude',
    estimatedTime: '45s'
};

export const sonelgazAssistant: AITool = {
    id: 'sonelgaz-assistant',
    slug: 'sonelgaz-assistant',
    name: {
        fr: 'Assistant Sonelgaz',
        ar: 'مساعد سونلغاز',
        en: 'Sonelgaz Assistant'
    },
    description: {
        fr: 'Factures, abonnements, réclamations, raccordement électricité et gaz',
        ar: 'الفواتير، الاشتراكات، الشكاوى، التوصيل بالكهرباء والغاز',
        en: 'Electricity and gas bills, subscriptions, complaints'
    },
    category: 'admin-dz',
    subcategory: 'services-publics',
    icon: 'Zap',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
                'Comprendre ma facture',
                'Nouvel abonnement',
                'Changement de nom',
                'Augmentation de puissance',
                'Réclamation / Contestation facture',
                'Coupure de courant',
                'Nouveau raccordement',
                'Modes de paiement'
            ]
        },
        { name: 'type_energie', type: 'select', label: 'Type d\'énergie', options: ['Électricité', 'Gaz', 'Les deux'], default: 'Électricité' },
        { name: 'wilaya', type: 'select', label: 'Wilaya', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
        { name: 'details', type: 'textarea', label: 'Détails de votre demande', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'sonelgazHelp' }],
    promptTemplate: `Tu es un conseiller clientèle expert Sonelgaz.

TYPE DE DEMANDE : {{type_demande}}
ÉNERGIE : {{type_energie}}
WILAYA : {{wilaya}}
DÉTAILS : {{details}}

## ⚡ Assistance Sonelgaz

{{#if type_demande === 'comprendre_facture'}}
### Comment lire votre facture Sonelgaz

**Éléments de la facture :**
1. **Référence contrat** : Numéro unique de votre abonnement
2. **Index relevé** : Ancien index → Nouvel index
3. **Consommation** : Différence en kWh (électricité) ou thermies (gaz)
4. **Tarification** :
   - Tranche 1 (0-125 kWh) : Tarif social
   - Tranche 2 (126-250 kWh) : Tarif normal
   - Tranche 3 (>250 kWh) : Tarif plein

5. **Taxes** :
   - TVA : 9% ou 19%
   - TAP : Taxe sur activité professionnelle
   - Droits fixes
{{/if}}

{{#if type_demande === 'reclamation'}}
### Procédure de réclamation

1. **Réclamation en ligne**
   - Site : www.sonelgaz.dz
   - Espace client → Réclamations

2. **En agence**
   - Munissez-vous de vos 3 dernières factures
   - Pièce d'identité

3. **Par téléphone**
   - Numéro vert : 3303

**Délai de traitement** : 15 jours ouvrables
**Si pas de réponse** : Saisir la Commission de Régulation (CREG)
{{/if}}

### Contacts utiles ({{wilaya}})
- Service client : 3303
- Urgences/Dépannage : 3303 (option 1)
- Site web : www.sonelgaz.dz
- Application mobile : Sonelgaz Mobile

### Modes de paiement
- 💳 En ligne (CIB, BaridiMob)
- 🏦 CCP
- 🏪 Points de paiement agréés
- 📱 Application Sonelgaz`,
    model: 'claude',
    estimatedTime: '20s'
};

export const seaalAssistant: AITool = {
    id: 'seaal-assistant',
    slug: 'seaal-assistant',
    name: {
        fr: 'Assistant SEAAL',
        ar: 'مساعد سيال',
        en: 'SEAAL Water Assistant'
    },
    description: {
        fr: 'Eau et assainissement Alger : factures, abonnements, fuites, qualité de l\'eau',
        ar: 'المياه والصرف الصحي بالجزائر العاصمة',
        en: 'Water and sanitation for Algiers'
    },
    category: 'admin-dz',
    subcategory: 'services-publics',
    icon: 'Droplets',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande', type: 'select', label: 'Type de demande', options: [
                'Facture', 'Nouvel abonnement', 'Fuite', 'Qualité eau', 'Coupure', 'Réclamation', 'Branchement'
            ]
        },
        { name: 'commune', type: 'text', label: 'Commune (Alger)' },
        { name: 'details', type: 'textarea', label: 'Détails', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'seaalHelp' }],
    promptTemplate: `Tu es un conseiller SEAAL (Société des Eaux et de l'Assainissement d'Alger).

TYPE DE DEMANDE : {{type_demande}}
COMMUNE : {{commune}}
DÉTAILS : {{details}}

## 💧 Assistance SEAAL

[Réponse détaillée et structurée]

Contacts :
- Numéro vert : 1594
- Site : www.seaal.dz
- Urgences fuites : 1594 (24h/24)`,
    model: 'claude',
    estimatedTime: '20s'
};

export const cnrRetraiteAssistant: AITool = {
    id: 'cnr-retraite-assistant',
    slug: 'cnr-retraite-assistant',
    name: {
        fr: 'Assistant Retraite CNR',
        ar: 'مساعد التقاعد',
        en: 'CNR Retirement Assistant'
    },
    description: {
        fr: 'Simulation retraite, demande de pension, réversion, droits des retraités CNR',
        ar: 'محاكاة التقاعد، طلب المعاش، حقوق المتقاعدين',
        en: 'Retirement simulation and pension rights'
    },
    category: 'admin-dz',
    subcategory: 'securite-sociale',
    icon: 'UserCheck',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande', type: 'select', label: 'Type de demande', options: [
                'Simulation retraite', 'Demande pension', 'Réversion', 'Attestation', 'Rachat années', 'Cumul emploi/retraite'
            ]
        },
        { name: 'annees_travail', type: 'number', label: 'Années de travail' },
        { name: 'salaire_moyen', type: 'number', label: 'Salaire moyen des 5 dernières années (DZD)' },
        { name: 'age', type: 'number', label: 'Âge actuel' },
        { name: 'sexe', type: 'select', options: ['Homme', 'Femme'] }
    ],
    outputs: [{ type: 'markdown', name: 'cnrHelp' }],
    promptTemplate: `Tu es un expert de la CNR (Caisse Nationale des Retraites) en Algérie.

## 👴 Assistant Retraite CNR

### Simulation de pension
**Vos données :**
- Années de cotisation : {{annees_travail}}
- Salaire de référence : {{salaire_moyen}} DZD
- Âge : {{age}} ans
- Sexe : {{sexe}}

**Conditions de départ :**
- Âge légal : 60 ans (H) / 55 ans (F)
- Minimum cotisation : 15 ans
- Retraite anticipée : possible avec 32 ans de cotisation

**Calcul de la pension :**
Taux = 2.5% × années de cotisation (max 80%)
Pension = Salaire de référence × Taux

Pension estimée : **X DZD/mois**

### Documents pour la demande
- [ ] Demande manuscrite
- [ ] Extrait de naissance
- [ ] Relevé de carrière CNAS
- [ ] Attestation de cessation d'activité
- [ ] RIB bancaire ou CCP

Délai de traitement : 2-3 mois`,
    model: 'claude',
    estimatedTime: '30s'
};

export const anemEmploiAssistant: AITool = {
    id: 'anem-emploi-assistant',
    slug: 'anem-emploi-assistant',
    name: {
        fr: 'Assistant ANEM Emploi',
        ar: 'مساعد الوكالة الوطنية للتشغيل',
        en: 'ANEM Employment Assistant'
    },
    description: {
        fr: 'Recherche d\'emploi, DAIP, formations, aides à l\'embauche, contrats aidés',
        ar: 'البحث عن عمل، عقود الإدماج، التكوين',
        en: 'Job search, DAIP contracts, training programs'
    },
    category: 'admin-dz',
    subcategory: 'emploi',
    icon: 'Briefcase',
    credits: 15,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        {
            name: 'type_demande', type: 'select', label: 'Type de demande', options: [
                'Inscription', 'DAIP', 'Formation', 'Offres emploi', 'Aides employeur', 'Attestation'
            ]
        },
        { name: 'diplome', type: 'select', label: 'Niveau de diplôme', options: ['Sans diplôme', 'BEM', 'Bac', 'Licence', 'Master', 'Doctorat', 'Formation pro'] },
        { name: 'experience', type: 'select', label: 'Expérience', options: ['Débutant', '1-3 ans', '3-5 ans', '> 5 ans'] },
        { name: 'wilaya', type: 'select', label: 'Wilaya' },
        { name: 'question', type: 'textarea', label: 'Votre question', required: true }
    ],
    outputs: [{ type: 'markdown', name: 'anemHelp' }],
    promptTemplate: `Tu es un conseiller de l'ANEM (Agence Nationale de l'Emploi) en Algérie.

## 💼 Assistant ANEM

### Dispositifs disponibles selon votre profil

**DAIP (Dispositif d'Aide à l'Insertion Professionnelle) :**
- CID (Contrat d'Insertion des Diplômés) : Pour Bac+
  - Salaire : 15 000 DZD/mois (État) + complément employeur
  - Durée : 12-24 mois
  
- CIP (Contrat d'Insertion Professionnelle) : Pour niveaux moyens
  - Salaire : 12 000 DZD/mois
  
- CFI (Contrat Formation-Insertion) : Formation + emploi
  - Salaire : 6 000 DZD/mois pendant formation

### Comment s'inscrire à l'ANEM
1. Se rendre à l'agence ANEM de {{wilaya}}
2. Documents requis :
   - [ ] Pièce d'identité
   - [ ] Diplômes
   - [ ] Photos d'identité
   - [ ] CV
3. Obtenir votre carte de demandeur d'emploi

### Contacts ANEM {{wilaya}}
- Site : www.anem.dz
- Portail emploi : tawdif.anem.dz`,
    model: 'claude',
    estimatedTime: '25s'
};

export const ansejCnacAssistant: AITool = {
    id: 'ansej-cnac-assistant',
    slug: 'ansej-cnac-assistant',
    name: {
        fr: 'Assistant ANSEJ/CNAC',
        ar: 'مساعد أونساج/كناك',
        en: 'ANSEJ/CNAC Startup Assistant'
    },
    description: {
        fr: 'Création d\'entreprise pour jeunes, microcrédits, financement projets ANSEJ et CNAC',
        ar: 'إنشاء المؤسسات للشباب، القروض المصغرة',
        en: 'Youth entrepreneurship, microloans, project financing'
    },
    category: 'admin-dz',
    subcategory: 'entreprise',
    icon: 'Rocket',
    credits: 20,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        { name: 'dispositif', type: 'select', label: 'Dispositif', options: ['ANSEJ (19-35 ans)', 'CNAC (30-55 ans)', 'ANGEM'] },
        { name: 'age', type: 'number', label: 'Votre âge', required: true },
        { name: 'projet', type: 'textarea', label: 'Description du projet', required: true },
        { name: 'montant_estime', type: 'number', label: 'Investissement estimé (DZD)' },
        { name: 'apport_personnel', type: 'number', label: 'Apport personnel disponible (DZD)' },
        { name: 'wilaya', type: 'select', label: 'Wilaya d\'implantation' }
    ],
    outputs: [{ type: 'markdown', name: 'startupHelp' }],
    promptTemplate: `Tu es un conseiller expert des dispositifs d'aide à la création d'entreprise en Algérie.

## 🚀 Financement de projet

### Éligibilité

**ANSEJ** (19-35 ans) :
- Âge : {{age}} ans {{#if age >= 19 && age <= 35}}✅ Éligible{{else}}❌ Non éligible (19-35 ans){{/if}}
- Avantages fiscaux : Exonération IRG/IBS (3-6 ans)
- Financement : Jusqu'à 10 millions DZD

**CNAC** (30-55 ans, chômeurs) :
- Pour les chômeurs de plus de 30 ans
- Mêmes avantages qu'ANSEJ

**ANGEM** (Micro-entreprises) :
- Prêt jusqu'à 1 million DZD
- Taux bonifié

### Structure de financement type
| Source | Pourcentage |
|--------|-------------|
| Apport personnel | 1-2% |
| Prêt non rémunéré (État) | 28-29% |
| Crédit bancaire | 70% |

### Étapes du parcours
1. Pré-inscription en ligne
2. Formation à l'entrepreneuriat
3. Étude de faisabilité
4. Validation du projet
5. Déblocage des fonds

### Documents requis
[Liste des documents selon le dispositif]`,
    model: 'claude',
    estimatedTime: '40s'
};

export const passeportCniAssistant: AITool = {
    id: 'passeport-cni-assistant',
    slug: 'passeport-cni-assistant',
    name: {
        fr: 'Assistant Passeport & CNI',
        ar: 'مساعد جواز السفر وبطاقة التعريف',
        en: 'Passport & ID Card Assistant'
    },
    description: {
        fr: 'Demande et renouvellement de passeport biométrique et carte d\'identité nationale',
        ar: 'طلب وتجديد جواز السفر البيومتري وبطاقة التعريف',
        en: 'Biometric passport and national ID card procedures'
    },
    category: 'admin-dz',
    subcategory: 'documents-identite',
    icon: 'CreditCard',
    credits: 10,
    priority: 'critical',
    isAlgeriaExclusive: true,
    inputs: [
        { name: 'document', type: 'select', label: 'Document demandé', options: ['Passeport adulte', 'Passeport mineur', 'CNI adulte', 'CNI mineur'] },
        { name: 'type_demande', type: 'select', label: 'Type de demande', options: ['Première demande', 'Renouvellement', 'Perte / Vol', 'Détérioration'] },
        { name: 'urgence', type: 'boolean', label: 'Demande urgente' },
        { name: 'commune', type: 'text', label: 'Commune de résidence' },
        { name: 'question', type: 'textarea', label: 'Question spécifique' }
    ],
    outputs: [{ type: 'markdown', name: 'passportHelp' }],
    promptTemplate: `Tu es un agent expert des documents d'identité en Algérie.

## 🛂 Procédures {{document}}

### Pré-inscription obligatoire
Site : passeport.interieur.gov.dz

### Documents requis ({{type_demande}})
- [ ] Formulaire de demande (retiré à la mairie)
- [ ] Extrait de naissance spécial (S12)
- [ ] Justificatif de domicile (moins de 3 mois)
- [ ] Photos biométriques (fond blanc)
- [ ] Timbre fiscal (6 000 DZD passeport / gratuit CNI)
- [ ] Ancien document (si renouvellement)
{{#if type_demande === 'perte_vol'}}
- [ ] Déclaration de perte/vol (commissariat)
{{/if}}

### Procédure
1. Pré-inscription en ligne → Obtenir RDV
2. Se présenter à la daïra/APC avec le dossier
3. Prise d'empreintes et photo
4. Retrait : 15-30 jours (normal) / 3-5 jours (urgent)

### Coût
- Passeport 48 pages : 6 000 DZD
- Passeport 28 pages : 4 000 DZD
- CNI : Gratuite

### Contacts
- Info : 1100
- Site : www.interieur.gov.dz`,
    model: 'claude',
    estimatedTime: '15s'
};
