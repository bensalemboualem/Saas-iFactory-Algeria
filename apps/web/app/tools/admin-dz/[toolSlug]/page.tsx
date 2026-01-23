'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ArrowLeft, Sparkles, Loader2, Copy, Check, Building, ShieldCheck, Calculator, Receipt, Zap, Droplets, Briefcase, CreditCard, Scale, Package, GraduationCap, Home, Phone } from 'lucide-react';
import { adminDzTools } from '@/lib/tools-data';

// Liste des 58 wilayas d'Algérie
const WILAYAS = [
  'Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra', 'Béchar',
  'Blida', 'Bouira', 'Tamanrasset', 'Tébessa', 'Tlemcen', 'Tiaret', 'Tizi Ouzou', 'Alger',
  'Djelfa', 'Jijel', 'Sétif', 'Saïda', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 'Guelma',
  'Constantine', 'Médéa', 'Mostaganem', 'M\'Sila', 'Mascara', 'Ouargla', 'Oran', 'El Bayadh',
  'Illizi', 'Bordj Bou Arréridj', 'Boumerdès', 'El Tarf', 'Tindouf', 'Tissemsilt', 'El Oued',
  'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 'Naâma', 'Aïn Témouchent',
  'Ghardaïa', 'Relizane', 'Timimoun', 'Bordj Badji Mokhtar', 'Ouled Djellal', 'Béni Abbès',
  'In Salah', 'In Guezzam', 'Touggourt', 'Djanet', 'El M\'Ghair', 'El Meniaa'
];

// Configurations des formulaires pour chaque outil Admin DZ
const toolFormConfigs: Record<string, { fields: any[], promptTemplate: string }> = {
  // ===== BATCH 1 - CRITIQUE (10) =====

  'cnas-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Remboursement soins', 'Arrêt maladie / Indemnités journalières', 'Congé maternité',
        'Accident de travail', 'Maladie professionnelle', 'Carte Chifa',
        'Affiliation / Immatriculation', 'Attestation d\'affiliation', 'Déclaration ayants droit', 'Autre question'
      ]},
      { name: 'situation', type: 'select', label: 'Vous êtes', required: true, options: ['Salarié(e)', 'Employeur', 'Retraité(e)', 'Ayant droit'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Décrivez votre situation ou question', required: true, placeholder: 'Ex: Je souhaite me faire rembourser une consultation chez un spécialiste...' },
    ],
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
- Téléphone : 3030 (numéro vert CNAS)
- Site web : www.cnas.dz

### 6. Conseils pratiques
💡 [Astuces pour accélérer la procédure]

### ⚖️ Base légale
- Loi n°83-11 du 2 juillet 1983
- [Autres textes pertinents]`
  },

  'casnos-simulator': {
    fields: [
      { name: 'activite', type: 'select', label: 'Type d\'activité', required: true, options: [
        'Commerçant', 'Artisan', 'Profession libérale', 'Agriculteur', 'Auto-entrepreneur'
      ]},
      { name: 'revenu_annuel', type: 'number', label: 'Revenu annuel déclaré (DZD)', required: true, placeholder: 'Ex: 2000000' },
      { name: 'annees_cotisation', type: 'number', label: 'Années de cotisation déjà effectuées', placeholder: '0' },
      { name: 'age', type: 'number', label: 'Votre âge', placeholder: 'Ex: 35' },
      { name: 'simulation_type', type: 'select', label: 'Type de simulation', required: true, options: [
        'Cotisation annuelle', 'Simulation retraite', 'Droits maladie'
      ]},
    ],
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
| Assurance maladie | 12% | [Calcul] DZD |
| Retraite | 6% | [Calcul] DZD |
| **TOTAL** | **18%** | **[Total] DZD** |

Cotisation trimestrielle : [Calcul] DZD
Cotisation mensuelle : [Calcul] DZD

### 2. Échéances de paiement
- 1er trimestre : avant le 30 mars
- 2ème trimestre : avant le 30 juin
- 3ème trimestre : avant le 30 septembre
- 4ème trimestre : avant le 30 décembre

### 3. Simulation retraite (si applicable)
Avec {{annees_cotisation}} années de cotisation :
- Âge de départ légal : 60 ans (hommes) / 55 ans (femmes)
- Pension estimée : [Calcul] DZD/mois
- Taux de remplacement : [X]%

### 4. Vos droits actuels
- ✅ Couverture maladie : [Oui/Non selon cotisations]
- ✅ Allocations familiales : [Oui/Non]
- ✅ Indemnités journalières : [Oui/Non]

### 5. Comment payer
- En ligne : portail.casnos.dz
- CCP / BaridiMob
- Agence CASNOS

### ⚠️ Pénalités de retard
10% de majoration après l'échéance

Base légale : Loi 83-14, Décret 85-35`
  },

  'cnr-retraite-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Simulation retraite', 'Demande de pension', 'Pension de réversion', 'Attestation',
        'Rachat d\'années', 'Cumul emploi-retraite', 'Revalorisation pension'
      ]},
      { name: 'annees_travail', type: 'number', label: 'Années de travail', required: true, placeholder: 'Ex: 25' },
      { name: 'salaire_moyen', type: 'number', label: 'Salaire moyen des 5 dernières années (DZD)', placeholder: 'Ex: 80000' },
      { name: 'age', type: 'number', label: 'Âge actuel', required: true, placeholder: 'Ex: 58' },
      { name: 'sexe', type: 'select', label: 'Sexe', required: true, options: ['Homme', 'Femme'] },
      { name: 'question', type: 'textarea', label: 'Question spécifique (optionnel)', placeholder: 'Détails supplémentaires...' },
    ],
    promptTemplate: `Tu es un expert de la CNR (Caisse Nationale des Retraites) en Algérie.

TYPE DE DEMANDE : {{type_demande}}
ANNÉES DE TRAVAIL : {{annees_travail}}
SALAIRE MOYEN (5 dernières années) : {{salaire_moyen}} DZD
ÂGE : {{age}} ans
SEXE : {{sexe}}
QUESTION : {{question}}

## 👴 Assistant Retraite CNR

### 1. Conditions de départ à la retraite
**Âge légal :**
- Hommes : 60 ans
- Femmes : 55 ans
- Retraite anticipée : possible avec 32 ans de cotisation

**Minimum de cotisation :** 15 ans

### 2. Calcul de votre pension estimée
**Formule :**
Taux = 2.5% × années de cotisation (plafonné à 80%)
Pension = Salaire de référence × Taux

Avec {{annees_travail}} années :
- Taux de liquidation : [2.5% × {{annees_travail}}]%
- Pension brute estimée : **[Calcul] DZD/mois**
- Pension nette (après retenues) : **[Calcul] DZD/mois**

### 3. Documents pour la demande
- [ ] Demande manuscrite adressée au Directeur CNR
- [ ] Extrait de naissance (S12) - moins de 3 mois
- [ ] Relevé de carrière CNAS complet
- [ ] Attestation de cessation d'activité de l'employeur
- [ ] Copie de la CNI
- [ ] RIB bancaire ou CCP
- [ ] 2 photos d'identité

### 4. Procédure
1. Constituer le dossier complet
2. Déposer à l'agence CNR de votre wilaya
3. Délai de traitement : 2-3 mois
4. Notification de la décision par courrier

### 5. Contacts CNR
- Numéro vert : 3040
- Site : www.cnr.dz
- Email : contact@cnr.dz

### ⚖️ Base légale
- Loi 83-12 relative à la retraite
- Ordonnance 97-13`
  },

  'impots-dz-assistant': {
    fields: [
      { name: 'type_impot', type: 'select', label: 'Type d\'impôt', required: true, options: [
        'IRG sur salaires', 'IRG professions libérales', 'IBS (Impôt sur Bénéfices des Sociétés)',
        'TVA', 'TAP (Taxe sur Activité Professionnelle)', 'Déclaration G50', 'Bilan fiscal annuel'
      ]},
      { name: 'statut', type: 'select', label: 'Statut', required: true, options: [
        'Salarié', 'Auto-entrepreneur', 'EURL/SARL', 'SPA', 'Profession libérale'
      ]},
      { name: 'montant', type: 'number', label: 'Montant concerné (DZD)', placeholder: 'Ex: 500000' },
      { name: 'question', type: 'textarea', label: 'Votre question fiscale', required: true, placeholder: 'Ex: Comment calculer mon IRG mensuel ?' },
    ],
    promptTemplate: `Tu es un expert fiscal algérien (inspecteur des impôts expérimenté).

TYPE D'IMPÔT : {{type_impot}}
STATUT : {{statut}}
MONTANT : {{montant}} DZD
QUESTION : {{question}}

## 🧾 Réponse fiscale

### 1. Explication du régime fiscal
[Explication claire selon le Code des Impôts Directs et Taxes Assimilées]

### 2. Calcul détaillé

**Barème IRG 2024 (si applicable) :**
| Tranche de revenu annuel | Taux |
|--------------------------|------|
| 0 - 240 000 DZD | 0% |
| 240 001 - 480 000 DZD | 23% |
| 480 001 - 960 000 DZD | 27% |
| 960 001 - 1 920 000 DZD | 30% |
| 1 920 001 - 3 840 000 DZD | 33% |
| > 3 840 000 DZD | 35% |

Abattement forfaitaire salariés : 40% (min 12 000 DZD, max 18 000 DZD/mois)

**Taux TVA en Algérie :**
- Taux normal : 19%
- Taux réduit : 9%

**TAP :** 1% à 3% selon activité

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
- Loi de Finances 2024`
  },

  'cnrc-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Création d\'entreprise', 'Modification (adresse, activité, gérant...)', 'Renouvellement registre commerce',
        'Radiation / Fermeture', 'Extrait de registre du commerce', 'Vérification nom commercial'
      ]},
      { name: 'forme_juridique', type: 'select', label: 'Forme juridique', required: true, options: [
        'Auto-entrepreneur', 'EURL', 'SARL', 'SPA', 'SNC', 'Personne physique (commerçant)'
      ]},
      { name: 'activite', type: 'text', label: 'Activité envisagée', placeholder: 'Ex: Commerce de détail, Restaurant, Import-export...' },
      { name: 'wilaya', type: 'select', label: 'Wilaya d\'implantation', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Ex: Quels documents pour créer une SARL ?' },
    ],
    promptTemplate: `Tu es un expert du Centre National du Registre du Commerce (CNRC) en Algérie.

TYPE DE DEMANDE : {{type_demande}}
FORME JURIDIQUE : {{forme_juridique}}
ACTIVITÉ : {{activite}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🏢 Guide CNRC

### 1. Procédure {{type_demande}}

**Étapes de création d'entreprise ({{forme_juridique}}) :**

1. **Vérification du nom commercial**
   - Site : www.cnrc.dz ou sidjilcom.cnrc.dz
   - Coût : Gratuit en ligne

2. **Constitution du dossier**
   Documents requis :
   - [ ] Acte de naissance n°12 (moins de 3 mois)
   - [ ] Certificat de résidence (moins de 3 mois)
   - [ ] Casier judiciaire (bulletin n°3) - moins de 3 mois
   - [ ] Justificatif du local (contrat de location notarié ou titre de propriété)
   - [ ] Statuts (pour EURL/SARL/SPA) - 4 exemplaires
   - [ ] Attestation de dépôt de capital (pour sociétés)
   - [ ] Formulaires CNRC (téléchargeables sur cnrc.dz)
   - [ ] Copie CNI
   - [ ] 2 photos d'identité

3. **Dépôt du dossier**
   - Lieu : Antenne CNRC de {{wilaya}}
   - Horaires : 8h-16h du dimanche au jeudi

4. **Retrait du registre du commerce**
   - Délai : 24-72h

### 2. Coûts estimés ({{forme_juridique}})
| Élément | Montant |
|---------|---------|
| Immatriculation | [X] DZD |
| Timbres fiscaux | [X] DZD |
| Publication BOAL | [X] DZD |
| Frais notaire (si société) | [X] DZD |
| **Total estimé** | **[X] DZD** |

### 3. Contacts CNRC {{wilaya}}
- Site national : www.cnrc.dz
- E-services : sidjilcom.cnrc.dz
- Tél : 021 XX XX XX

### 4. Délais et validité
- Traitement : 24-72h
- Validité registre : 2 ans (renouvellement obligatoire)
- Renouvellement : 1 mois avant expiration

### ⚖️ Base légale
- Code de Commerce algérien
- Décret exécutif 97-41`
  },

  'ansej-cnac-assistant': {
    fields: [
      { name: 'dispositif', type: 'select', label: 'Dispositif', required: true, options: ['ANSEJ', 'CNAC', 'ANGEM'] },
      { name: 'age', type: 'number', label: 'Votre âge', required: true, placeholder: 'Ex: 28' },
      { name: 'projet', type: 'textarea', label: 'Description du projet', required: true, placeholder: 'Décrivez votre projet d\'entreprise...' },
      { name: 'montant_estime', type: 'number', label: 'Investissement estimé (DZD)', placeholder: 'Ex: 5000000' },
      { name: 'apport_personnel', type: 'number', label: 'Apport personnel disponible (DZD)', placeholder: 'Ex: 100000' },
      { name: 'wilaya', type: 'select', label: 'Wilaya d\'implantation', required: true, options: WILAYAS },
    ],
    promptTemplate: `Tu es un conseiller expert des dispositifs d'aide à la création d'entreprise en Algérie.

DISPOSITIF : {{dispositif}}
ÂGE : {{age}} ans
PROJET : {{projet}}
INVESTISSEMENT ESTIMÉ : {{montant_estime}} DZD
APPORT PERSONNEL : {{apport_personnel}} DZD
WILAYA : {{wilaya}}

## 🚀 Financement de projet

### 1. Éligibilité {{dispositif}}

**ANSEJ** (19-35 ans) :
- Âge : {{age}} ans - [Éligible/Non éligible]
- Avantages fiscaux : Exonération IRG/IBS (3-6 ans)
- Financement : Jusqu'à 10 millions DZD

**CNAC** (30-55 ans, chômeurs) :
- Pour les chômeurs inscrits à l'ANEM depuis +6 mois
- Mêmes avantages qu'ANSEJ

**ANGEM** (Micro-entreprises) :
- Prêt jusqu'à 1 million DZD
- Taux bonifié 0%
- Sans condition d'âge

### 2. Structure de financement type
| Source | Pourcentage |
|--------|-------------|
| Apport personnel | 1-2% |
| Prêt non rémunéré (État) | 28-29% |
| Crédit bancaire | 70% |

Pour votre projet de {{montant_estime}} DZD :
- Apport personnel requis : [Calcul] DZD
- Prêt État : [Calcul] DZD
- Crédit bancaire : [Calcul] DZD

### 3. Étapes du parcours
1. **Pré-inscription en ligne** : ansej.dz / cnac.dz
2. **Convocation** : Entretien avec conseiller
3. **Formation** : 15 jours en gestion d'entreprise
4. **Étude de faisabilité** : Accompagnement gratuit
5. **Validation PV** : Commission de validation
6. **Déblocage** : Signature contrat + déblocage fonds

### 4. Avantages fiscaux
- Exonération TVA sur équipements
- Exonération IRG/IBS (3-6 ans)
- Bonification taux d'intérêt
- Accompagnement gratuit

### 5. Documents requis
- [ ] CNI
- [ ] Extrait de naissance
- [ ] Certificat de résidence
- [ ] Diplôme ou attestation de formation
- [ ] Business plan (modèle fourni)

### 📍 Contact {{dispositif}} {{wilaya}}
- Site : www.ansej.dz / www.cnac.dz
- Tél antenne locale : [Numéro]`
  },

  'sonelgaz-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Comprendre ma facture', 'Nouvel abonnement', 'Changement de nom', 'Augmentation de puissance',
        'Réclamation / Contestation facture', 'Coupure de courant', 'Nouveau raccordement', 'Modes de paiement'
      ]},
      { name: 'type_energie', type: 'select', label: 'Type d\'énergie', required: true, options: ['Électricité', 'Gaz', 'Les deux'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'details', type: 'textarea', label: 'Détails de votre demande', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un conseiller clientèle expert Sonelgaz.

TYPE DE DEMANDE : {{type_demande}}
ÉNERGIE : {{type_energie}}
WILAYA : {{wilaya}}
DÉTAILS : {{details}}

## ⚡ Assistance Sonelgaz

### Comment lire votre facture Sonelgaz

**Éléments de la facture :**
1. **Référence contrat** : Numéro unique de votre abonnement
2. **Index relevé** : Ancien index → Nouvel index
3. **Consommation** : Différence en kWh (électricité) ou thermies (gaz)
4. **Tarification électricité** :
   - Tranche 1 (0-125 kWh) : 1,779 DZD/kWh (tarif social)
   - Tranche 2 (126-250 kWh) : 4,179 DZD/kWh
   - Tranche 3 (251-1000 kWh) : 4,812 DZD/kWh
   - Tranche 4 (>1000 kWh) : 5,480 DZD/kWh

5. **Taxes** :
   - TVA : 9% (domestique) ou 19% (professionnel)
   - Droits fixes mensuels

### Procédure {{type_demande}}

[Instructions détaillées selon le type de demande]

### Contacts utiles ({{wilaya}})
- Service client : **3303** (numéro vert 24h/24)
- Urgences/Dépannage : 3303 (option 1)
- Site web : www.sonelgaz.dz
- Application mobile : Sonelgaz Mobile (Play Store / App Store)

### Modes de paiement
- 💳 En ligne via CIB sur sonelgaz.dz
- 📱 BaridiMob / CCP
- 🏪 Points de paiement agréés (Flexy, épiceries)
- 🏦 Agences Sonelgaz

### Délais de traitement
- Réclamation : 15 jours ouvrables
- Nouveau branchement : 15-30 jours
- Changement de nom : 7 jours

### ⚠️ En cas de non-réponse
Saisir la Commission de Régulation de l'Électricité et du Gaz (CREG)
- Site : www.creg.dz`
  },

  'seaal-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Comprendre ma facture', 'Nouvel abonnement', 'Fuite d\'eau', 'Qualité de l\'eau',
        'Coupure d\'eau', 'Réclamation', 'Nouveau branchement'
      ]},
      { name: 'commune', type: 'text', label: 'Commune (Alger)', required: true, placeholder: 'Ex: Bab El Oued, Hydra, Kouba...' },
      { name: 'details', type: 'textarea', label: 'Détails', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un conseiller SEAAL (Société des Eaux et de l'Assainissement d'Alger).

TYPE DE DEMANDE : {{type_demande}}
COMMUNE : {{commune}}
DÉTAILS : {{details}}

## 💧 Assistance SEAAL

### Tarification de l'eau (2024)
| Tranche | Consommation | Prix/m³ |
|---------|--------------|---------|
| 1 | 0-25 m³/trim | 6,30 DZD |
| 2 | 26-55 m³/trim | 20,48 DZD |
| 3 | 56-82 m³/trim | 34,65 DZD |
| 4 | > 82 m³/trim | 40,95 DZD |

+ Redevance assainissement : 20% du montant eau
+ Taxes diverses

### Procédure {{type_demande}}

[Instructions détaillées selon le type de demande]

### Contacts SEAAL
- **Numéro vert : 1594** (24h/24 - 7j/7)
- Site : www.seaal.dz
- Espace client : espace-client.seaal.dz
- Urgences fuites : 1594 (option 1)

### Horaires agences
- Dimanche à Jeudi : 8h00 - 16h00

### Modes de paiement
- En ligne sur espace-client.seaal.dz
- CCP / BaridiMob
- Agences SEAAL
- Points de paiement agréés

### Délais
- Signalement fuite : intervention sous 24-48h
- Réclamation facture : réponse sous 15 jours
- Nouveau branchement : 1-3 mois`
  },

  'anem-emploi-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Inscription demandeur d\'emploi', 'Contrat DAIP (CID/CIP/CFI)', 'Formation professionnelle',
        'Recherche offres d\'emploi', 'Aides à l\'employeur', 'Attestation de chômage'
      ]},
      { name: 'diplome', type: 'select', label: 'Niveau de diplôme', required: true, options: [
        'Sans diplôme', 'BEM', 'Bac', 'Licence (Bac+3)', 'Master (Bac+5)', 'Doctorat', 'Formation professionnelle'
      ]},
      { name: 'experience', type: 'select', label: 'Expérience', required: true, options: [
        'Débutant (sans expérience)', '1-3 ans', '3-5 ans', 'Plus de 5 ans'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Ex: Comment m\'inscrire au dispositif DAIP ?' },
    ],
    promptTemplate: `Tu es un conseiller de l'ANEM (Agence Nationale de l'Emploi) en Algérie.

TYPE DE DEMANDE : {{type_demande}}
DIPLÔME : {{diplome}}
EXPÉRIENCE : {{experience}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 💼 Assistant ANEM

### Dispositifs disponibles selon votre profil

**DAIP (Dispositif d'Aide à l'Insertion Professionnelle) :**

1. **CID - Contrat d'Insertion des Diplômés** (Bac+ minimum)
   - Salaire État : 15 000 DZD/mois
   - Complément employeur obligatoire
   - Durée : 12 mois (renouvelable 1 fois)
   - Éligibilité : [Selon votre profil]

2. **CIP - Contrat d'Insertion Professionnelle** (Niveau moyen)
   - Salaire État : 12 000 DZD/mois
   - Durée : 12 mois

3. **CFI - Contrat Formation-Insertion**
   - Formation + emploi
   - Indemnité : 6 000 DZD/mois pendant formation

### Comment s'inscrire à l'ANEM

1. **En ligne** : www.anem.dz → Espace demandeur
2. **En agence** : Agence ANEM de {{wilaya}}

**Documents requis :**
- [ ] Pièce d'identité (CNI)
- [ ] Diplômes et attestations
- [ ] 2 photos d'identité
- [ ] CV à jour
- [ ] Certificat de résidence

### Recherche d'emploi
- Portail national : tawdif.anem.dz
- Offres actualisées quotidiennement
- Alertes email personnalisées

### Contacts ANEM {{wilaya}}
- Site : www.anem.dz
- Portail emploi : tawdif.anem.dz
- Tél : [Numéro agence locale]

### ⚖️ Base légale
- Décret exécutif 08-126 (DAIP)
- Loi 04-19 relative à l'emploi`
  },

  'passeport-cni-assistant': {
    fields: [
      { name: 'document', type: 'select', label: 'Document demandé', required: true, options: [
        'Passeport adulte', 'Passeport mineur', 'CNI adulte', 'CNI mineur'
      ]},
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Première demande', 'Renouvellement', 'Perte ou vol', 'Détérioration'
      ]},
      { name: 'urgence', type: 'select', label: 'Urgence', options: ['Non', 'Oui - raison médicale', 'Oui - raison professionnelle'] },
      { name: 'commune', type: 'text', label: 'Commune de résidence', required: true, placeholder: 'Ex: Hussein Dey, Bir Mourad Raïs...' },
      { name: 'question', type: 'textarea', label: 'Question spécifique', placeholder: 'Détails ou questions supplémentaires...' },
    ],
    promptTemplate: `Tu es un agent expert des documents d'identité en Algérie.

DOCUMENT : {{document}}
TYPE DE DEMANDE : {{type_demande}}
URGENCE : {{urgence}}
COMMUNE : {{commune}}
QUESTION : {{question}}

## 🛂 Procédure {{document}} - {{type_demande}}

### 1. Pré-inscription OBLIGATOIRE
**Site : passeport.interieur.gov.dz**

Étapes :
1. Créer un compte
2. Remplir le formulaire en ligne
3. Télécharger les documents
4. Obtenir un rendez-vous

### 2. Documents requis
- [ ] Formulaire de demande (téléchargé après pré-inscription)
- [ ] Extrait de naissance spécial (S12) - moins de 3 mois
- [ ] Justificatif de domicile (facture Sonelgaz/SEAAL ou certificat de résidence)
- [ ] Photos biométriques (fond blanc, format 3.5x4.5)
- [ ] Timbre fiscal
- [ ] Ancien document (si renouvellement)

**En cas de perte/vol :**
- [ ] Déclaration de perte/vol (commissariat de police)

**Pour mineur :**
- [ ] Autorisation parentale (les deux parents)
- [ ] CNI des parents

### 3. Timbres fiscaux
| Document | Prix |
|----------|------|
| Passeport 48 pages | 6 000 DZD |
| Passeport 28 pages | 4 000 DZD |
| Passeport urgent | +10 000 DZD |
| CNI | Gratuite |

### 4. Où déposer
- **APC** (mairie) de votre commune : {{commune}}
- **Daïra** pour certaines communes

### 5. Délais de délivrance
- Passeport normal : 15-30 jours
- Passeport urgent : 3-5 jours (si justificatif)
- CNI : 7-15 jours

### 6. Retrait
- Retrait personnel obligatoire
- Présenter la CNI + récépissé

### Contacts
- Info : **1100**
- Site : www.interieur.gov.dz
- Pré-inscription : passeport.interieur.gov.dz`
  },

  // ===== BATCH 2 - HAUTE PRIORITÉ =====

  'algerie-telecom-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Nouvel abonnement ADSL/Fibre', 'Panne internet', 'Réclamation facture', 'Résiliation', 'Changement offre'
      ]},
      { name: 'offre', type: 'select', label: 'Offre actuelle/souhaitée', options: ['ADSL', 'VDSL', 'Fibre FTTH', '4G LTE Fixe', 'Idoom Fibre'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'details', type: 'textarea', label: 'Détails', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un conseiller Algérie Télécom expert.

[Génère une réponse complète sur les offres, tarifs, procédures et contacts Algérie Télécom]`
  },

  'permis-conduire-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Première demande (auto-école)', 'Renouvellement', 'Duplicata (perte)', 'Conversion permis étranger', 'Points permis'
      ]},
      { name: 'categorie', type: 'select', label: 'Catégorie', options: ['B (voiture)', 'A (moto)', 'C (poids lourd)', 'D (transport personnes)', 'E (remorque)'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un expert des procédures de permis de conduire en Algérie.

[Génère une réponse complète avec documents, coûts, délais et contacts]`
  },

  'douanes-assistant': {
    fields: [
      { name: 'type_operation', type: 'select', label: 'Type d\'opération', required: true, options: [
        'Import marchandises', 'Export', 'Franchise touristique', 'Véhicule importé', 'Colis postal', 'Dédouanement'
      ]},
      { name: 'nature_marchandise', type: 'text', label: 'Nature de la marchandise', placeholder: 'Ex: Électronique, vêtements, véhicule...' },
      { name: 'valeur', type: 'number', label: 'Valeur estimée (DZD ou EUR)', placeholder: 'Ex: 50000' },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un expert en douanes algériennes.

[Génère une réponse sur les tarifs douaniers, procédures et réglementations]`
  },

  'apc-daira-assistant': {
    fields: [
      { name: 'type_document', type: 'select', label: 'Type de document', required: true, options: [
        'Acte de naissance', 'Certificat de résidence', 'Légalisation de signature', 'Fiche familiale', 'Attestation de vie', 'Casier judiciaire'
      ]},
      { name: 'commune', type: 'text', label: 'Commune', required: true, placeholder: 'Votre commune' },
      { name: 'details', type: 'textarea', label: 'Détails', required: true },
    ],
    promptTemplate: `Tu es un agent d'état civil expert en démarches administratives communales.

[Génère une réponse avec procédures, documents et délais pour la mairie/daïra]`
  },

  'cacobatph-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Cotisations employeur', 'Congés payés ouvrier', 'Attestation de congés', 'Indemnités'
      ]},
      { name: 'secteur', type: 'select', label: 'Secteur', options: ['Bâtiment', 'Travaux publics', 'Hydraulique'] },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un expert CACOBATPH.

[Génère une réponse sur les congés payés du secteur BTP]`
  },

  'cpa-banque-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Ouverture compte', 'Crédit immobilier', 'Crédit auto', 'Carte CIB', 'BaridiMob', 'Transfert international'
      ]},
      { name: 'banque', type: 'select', label: 'Banque', options: ['BNA', 'CPA', 'BEA', 'BADR', 'BDL', 'CNEP', 'AGB', 'BNP Paribas El Djazaïr', 'Société Générale', 'Autre'] },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un conseiller bancaire expert du système bancaire algérien.

[Génère une réponse sur les services bancaires en Algérie]`
  },

  'caf-allocations-assistant': {
    fields: [
      { name: 'type_allocation', type: 'select', label: 'Type d\'allocation', required: true, options: [
        'Allocations familiales', 'Prime de scolarité', 'Allocation handicapé', 'Allocation maternité'
      ]},
      { name: 'nombre_enfants', type: 'number', label: 'Nombre d\'enfants', placeholder: 'Ex: 3' },
      { name: 'situation', type: 'select', label: 'Situation', options: ['Salarié', 'Non-salarié', 'Retraité', 'Chômeur'] },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un expert des allocations familiales en Algérie.

[Génère une réponse sur les droits et montants des allocations]`
  },

  'angem-microcredit-assistant': {
    fields: [
      { name: 'type_projet', type: 'text', label: 'Type de projet', required: true, placeholder: 'Ex: Couture, pâtisserie, artisanat...' },
      { name: 'montant_demande', type: 'number', label: 'Montant demandé (DZD)', placeholder: 'Max 1 000 000 DZD' },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un conseiller ANGEM (microcrédit).

[Génère une réponse sur les conditions et procédures ANGEM]`
  },

  'notaire-assistant': {
    fields: [
      { name: 'type_acte', type: 'select', label: 'Type d\'acte', required: true, options: [
        'Vente immobilière', 'Donation', 'Succession/Héritage', 'Contrat de mariage', 'SCI/Société', 'Procuration'
      ]},
      { name: 'valeur_bien', type: 'number', label: 'Valeur du bien (DZD)', placeholder: 'Si applicable' },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un notaire expert en droit algérien.

[Génère une réponse sur les actes notariés, frais et procédures]`
  },

  'carte-grise-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Nouvelle immatriculation', 'Mutation (changement propriétaire)', 'Duplicata', 'Changement adresse', 'Véhicule importé'
      ]},
      { name: 'type_vehicule', type: 'select', label: 'Type de véhicule', options: ['Voiture', 'Moto', 'Utilitaire', 'Camion'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Question', required: true },
    ],
    promptTemplate: `Tu es un expert en immatriculation de véhicules en Algérie.

[Génère une réponse sur les procédures carte grise]`
  },

  // ===== BATCH 2 BIS - 10 nouveaux outils =====

  'avocat-virtuel-dz': {
    fields: [
      { name: 'domaine_droit', type: 'select', label: 'Domaine du droit', required: true, options: [
        'Droit du travail', 'Droit de la famille (divorce, garde, pension)', 'Droit commercial',
        'Droit pénal', 'Droit immobilier', 'Droit des successions', 'Droit administratif', 'Autre'
      ]},
      { name: 'situation', type: 'textarea', label: 'Décrivez votre situation', required: true, placeholder: 'Expliquez votre problème juridique en détail...' },
      { name: 'partie', type: 'select', label: 'Vous êtes', options: ['Demandeur (plaignant)', 'Défendeur', 'Tiers concerné', 'Simple information'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'urgence', type: 'select', label: 'Urgence', options: ['Non urgente', 'Délai en cours', 'Très urgent'] },
    ],
    promptTemplate: `Tu es un avocat virtuel expert en droit algérien. Tu fournis des conseils juridiques généraux à titre informatif.

DOMAINE : {{domaine_droit}}
SITUATION : {{situation}}
PARTIE : {{partie}}
WILAYA : {{wilaya}}
URGENCE : {{urgence}}

## ⚖️ Consultation Juridique

### 1. Analyse de votre situation
[Analyse juridique de la situation décrite]

### 2. Cadre légal applicable
**Textes de référence :**
- [Loi/Code applicable]
- [Articles pertinents]

### 3. Vos droits et obligations
[Liste des droits et obligations selon le droit algérien]

### 4. Démarches recommandées
1. **Étape 1** : [Action + délai]
2. **Étape 2** : [Action + délai]
3. ...

### 5. Juridiction compétente
- Tribunal de : [Tribunal compétent selon le domaine]
- Adresse tribunal {{wilaya}} : [Adresse]

### 6. Coûts estimés
| Élément | Montant estimé |
|---------|----------------|
| Frais de justice | [X] DZD |
| Honoraires avocat | [X] DZD |
| Huissier | [X] DZD |

### 7. Délais de prescription
⚠️ [Délais à respecter selon le type d'affaire]

### 8. Documents à préparer
- [ ] Document 1
- [ ] Document 2
- [ ] ...

### ⚠️ Avertissement
Ces informations sont fournies à titre indicatif et ne remplacent pas une consultation avec un avocat inscrit au barreau.
Pour une assistance personnalisée, contactez le Barreau de {{wilaya}}.

### 📞 Contacts utiles
- Barreau d'Algérie : www.una.dz
- Aide juridictionnelle : Tribunal de {{wilaya}}`
  },

  'douane-calculator': {
    fields: [
      { name: 'type_operation', type: 'select', label: 'Type d\'opération', required: true, options: [
        'Import marchandises commerciales', 'Import véhicule neuf', 'Import véhicule occasion (moins de 3 ans)',
        'Effets personnels (retour définitif)', 'Colis/achats en ligne', 'Export marchandises'
      ]},
      { name: 'nature_produit', type: 'text', label: 'Nature du produit', required: true, placeholder: 'Ex: Téléphone, Vêtements, Pièces auto, Véhicule...' },
      { name: 'valeur_caf', type: 'number', label: 'Valeur CAF en DZD (ou équivalent)', required: true, placeholder: 'Ex: 500000' },
      { name: 'pays_origine', type: 'text', label: 'Pays d\'origine', required: true, placeholder: 'Ex: Chine, France, Turquie...' },
      { name: 'poids_kg', type: 'number', label: 'Poids (kg)', placeholder: 'Optionnel' },
    ],
    promptTemplate: `Tu es un expert en douanes algériennes et tarification douanière.

TYPE D'OPÉRATION : {{type_operation}}
PRODUIT : {{nature_produit}}
VALEUR CAF : {{valeur_caf}} DZD
PAYS D'ORIGINE : {{pays_origine}}
POIDS : {{poids_kg}} kg

## 🛃 Calcul Droits de Douane

### 1. Classification tarifaire
**Position SH estimée :** [Code SH à 8 chiffres]
**Désignation :** {{nature_produit}}

### 2. Droits et taxes applicables

| Élément | Taux | Montant (DZD) |
|---------|------|---------------|
| Valeur CAF | - | {{valeur_caf}} |
| Droit de douane (DD) | [X]% | [Calcul] |
| TVA import | 19% | [Calcul] |
| Droit additionnel provisoire (DAP) | [0-200%] | [Calcul] |
| Taxe domiciliation bancaire | 4% | [Calcul] |
| Frais de dédouanement | Forfait | [X] |
| **TOTAL À PAYER** | - | **[TOTAL] DZD** |

### 3. Coût total importation
- Valeur CAF : {{valeur_caf}} DZD
- Total droits et taxes : [X] DZD
- **Prix de revient total : [X] DZD**
- Taux de taxation effectif : [X]%

### 4. Documents requis pour dédouanement
- [ ] Facture commerciale originale
- [ ] Connaissement (BL) ou LTA
- [ ] Certificat d'origine
- [ ] Domiciliation bancaire (si > 100 000 DZD)
- [ ] Note de colisage
- [ ] [Autres selon produit]

### 5. Procédure de dédouanement
1. Domiciliation bancaire (si applicable)
2. Dépôt déclaration en douane
3. Vérification et liquidation
4. Paiement des droits
5. Enlèvement de la marchandise

### 6. Restrictions / Interdictions
[Indiquer si le produit est soumis à licence, interdit, ou restrictions particulières]

### 📍 Contacts Douanes
- Site : www.douane.gov.dz
- Tel : 021 XX XX XX
- Bureau le plus proche : [Selon ville]

### ⚠️ Note
Tarifs indicatifs, susceptibles de variation. Consultez le tarif douanier officiel sur douane.gov.dz`
  },

  'contrat-location-dz': {
    fields: [
      { name: 'type_bien', type: 'select', label: 'Type de bien', required: true, options: [
        'Appartement (habitation)', 'Maison (habitation)', 'Local commercial', 'Bureau', 'Garage/Parking', 'Terrain'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya du bien', required: true, options: WILAYAS },
      { name: 'adresse_bien', type: 'text', label: 'Adresse du bien', required: true, placeholder: 'Adresse complète du bien loué' },
      { name: 'loyer_mensuel', type: 'number', label: 'Loyer mensuel (DZD)', required: true, placeholder: 'Ex: 40000' },
      { name: 'duree_bail', type: 'select', label: 'Durée du bail', options: ['1 an', '2 ans', '3 ans', '5 ans', 'Indéterminée'] },
      { name: 'depot_garantie', type: 'number', label: 'Dépôt de garantie (mois)', placeholder: 'Ex: 2' },
      { name: 'charges_incluses', type: 'select', label: 'Charges incluses', options: ['Aucune', 'Eau uniquement', 'Eau + Électricité', 'Toutes charges'] },
    ],
    promptTemplate: `Tu es un expert en droit immobilier algérien. Génère un contrat de location conforme au droit algérien.

TYPE DE BIEN : {{type_bien}}
WILAYA : {{wilaya}}
ADRESSE : {{adresse_bien}}
LOYER : {{loyer_mensuel}} DZD/mois
DURÉE : {{duree_bail}}
DÉPÔT GARANTIE : {{depot_garantie}} mois
CHARGES : {{charges_incluses}}

---

## 📋 CONTRAT DE LOCATION

### ENTRE LES SOUSSIGNÉS :

**LE BAILLEUR :**
Nom et prénom : _____________________
Adresse : _____________________
N° CNI : _____________________

**LE LOCATAIRE :**
Nom et prénom : _____________________
Adresse actuelle : _____________________
N° CNI : _____________________

### IL A ÉTÉ CONVENU CE QUI SUIT :

**ARTICLE 1 - OBJET DU CONTRAT**
Le bailleur loue au locataire le bien suivant :
- Nature : {{type_bien}}
- Adresse : {{adresse_bien}}, Wilaya de {{wilaya}}
- Surface : _____ m²
- Composition : _____

**ARTICLE 2 - DURÉE**
Le présent bail est consenti pour une durée de {{duree_bail}}, à compter du ___/___/_____.

**ARTICLE 3 - LOYER**
Le loyer mensuel est fixé à **{{loyer_mensuel}} DZD** (_____ dinars algériens), payable d'avance le _____ de chaque mois.

**ARTICLE 4 - DÉPÔT DE GARANTIE**
Un dépôt de garantie de {{depot_garantie}} mois de loyer, soit **[Calcul] DZD**, est versé à la signature.

**ARTICLE 5 - CHARGES**
{{charges_incluses}}

**ARTICLE 6 - OBLIGATIONS DU BAILLEUR**
- Délivrer le bien en bon état
- Assurer la jouissance paisible
- Effectuer les grosses réparations

**ARTICLE 7 - OBLIGATIONS DU LOCATAIRE**
- Payer le loyer aux termes convenus
- User du bien en bon père de famille
- Effectuer les réparations locatives
- Ne pas sous-louer sans autorisation écrite

**ARTICLE 8 - RÉSILIATION**
[Conditions de résiliation selon le type de bail]

**ARTICLE 9 - ÉLECTION DE DOMICILE**
Pour l'exécution du présent contrat, les parties élisent domicile en leurs adresses respectives.

**ARTICLE 10 - LITIGES**
Tout litige relatif au présent bail sera soumis aux juridictions compétentes de {{wilaya}}.

---

Fait à ___________, le ___/___/_____

En deux exemplaires originaux.

**Le Bailleur**                    **Le Locataire**
(Signature)                        (Signature)

---

### ⚖️ Base légale
- Code civil algérien (Articles 467 à 537)
- Loi n°07-05 du 25/04/2007

### 📌 Recommandations
1. Faire légaliser les signatures à l'APC
2. Enregistrer le contrat aux impôts
3. Joindre un état des lieux d'entrée
4. Conserver l'original en lieu sûr`
  },

  'statuts-entreprise-generator': {
    fields: [
      { name: 'forme_juridique', type: 'select', label: 'Forme juridique', required: true, options: [
        'EURL (Entreprise Unipersonnelle)', 'SARL (Société à Responsabilité Limitée)', 'SPA (Société Par Actions)', 'SNC (Société en Nom Collectif)'
      ]},
      { name: 'denomination', type: 'text', label: 'Dénomination sociale', required: true, placeholder: 'Ex: TECH ALGÉRIE' },
      { name: 'objet_social', type: 'textarea', label: 'Objet social (activités)', required: true, placeholder: 'Ex: Commerce général, import-export, services informatiques...' },
      { name: 'capital', type: 'number', label: 'Capital social (DZD)', required: true, placeholder: 'Minimum 100 000 DZD pour SARL' },
      { name: 'siege', type: 'text', label: 'Adresse du siège social', required: true, placeholder: 'Adresse complète' },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'duree', type: 'select', label: 'Durée de la société', options: ['99 ans', '50 ans', '25 ans', 'Illimitée'] },
    ],
    promptTemplate: `Tu es un expert en droit des sociétés algérien. Génère des statuts conformes au Code de Commerce algérien.

FORME : {{forme_juridique}}
DÉNOMINATION : {{denomination}}
OBJET : {{objet_social}}
CAPITAL : {{capital}} DZD
SIÈGE : {{siege}}, {{wilaya}}
DURÉE : {{duree}}

---

## 📋 STATUTS DE {{denomination}} {{forme_juridique}}

### TITRE I - FORME - OBJET - DÉNOMINATION - SIÈGE - DURÉE

**ARTICLE 1 - FORME**
Il est formé entre les associés soussignés une {{forme_juridique}} régie par les présents statuts et par la législation algérienne en vigueur.

**ARTICLE 2 - OBJET**
La société a pour objet :
{{objet_social}}

Et plus généralement, toutes opérations commerciales, industrielles, mobilières et immobilières se rattachant directement ou indirectement à l'objet social.

**ARTICLE 3 - DÉNOMINATION**
La société prend la dénomination : **{{denomination}}**
Dans tous les actes et documents, la dénomination sera suivie de la mention "{{forme_juridique}}" et du capital social.

**ARTICLE 4 - SIÈGE SOCIAL**
Le siège social est fixé à : {{siege}}, Wilaya de {{wilaya}}
Il pourra être transféré en tout autre lieu par décision de l'assemblée générale.

**ARTICLE 5 - DURÉE**
La durée de la société est fixée à {{duree}} à compter de son immatriculation au registre du commerce.

### TITRE II - CAPITAL SOCIAL - PARTS SOCIALES

**ARTICLE 6 - CAPITAL SOCIAL**
Le capital social est fixé à **{{capital}} DZD** (_____ dinars algériens).
Il est divisé en _____ parts sociales de _____ DZD chacune.

**ARTICLE 7 - APPORTS**
Les associés effectuent les apports suivants :
- [Nom associé 1] : _____ parts (soit _____ DZD)
- [Nom associé 2] : _____ parts (soit _____ DZD)

**ARTICLE 8 - PARTS SOCIALES**
Les parts sociales ne peuvent être cédées qu'avec l'agrément préalable des associés représentant au moins les 3/4 du capital social.

### TITRE III - GÉRANCE

**ARTICLE 9 - GÉRANCE**
La société est gérée par un ou plusieurs gérants, associés ou non, nommés par les associés.
Le premier gérant est : _____________________

**ARTICLE 10 - POUVOIRS DU GÉRANT**
Le gérant dispose des pouvoirs les plus étendus pour agir au nom de la société, dans la limite de l'objet social.

### TITRE IV - ASSEMBLÉES GÉNÉRALES

**ARTICLE 11 - DÉCISIONS COLLECTIVES**
Les décisions sont prises en assemblée générale ou par consultation écrite.

**ARTICLE 12 - MAJORITÉ**
- Décisions ordinaires : Majorité des parts
- Décisions extraordinaires : 3/4 des parts

### TITRE V - COMPTES SOCIAUX - BÉNÉFICES

**ARTICLE 13 - EXERCICE SOCIAL**
L'exercice social commence le 1er janvier et se termine le 31 décembre.

**ARTICLE 14 - AFFECTATION DES RÉSULTATS**
Sur le bénéfice net, il est prélevé 5% pour constituer le fonds de réserve légale (jusqu'à 10% du capital).

### TITRE VI - DISSOLUTION - LIQUIDATION

**ARTICLE 15 - DISSOLUTION**
La société est dissoute par décision des associés ou par les causes prévues par la loi.

---

Fait à {{wilaya}}, le ___/___/_____

**Les Associés :**
(Signatures)

---

### ⚖️ Base légale
- Code de Commerce algérien (Ordonnance 75-59 modifiée)
- Articles 564 à 595 (SARL)

### 📌 Prochaines étapes
1. Signature des statuts par les associés
2. Enregistrement aux impôts
3. Ouverture compte bancaire + dépôt capital
4. Publication au BOAL
5. Immatriculation au CNRC`
  },

  'attestation-travail-generator': {
    fields: [
      { name: 'type_document', type: 'select', label: 'Type de document', required: true, options: [
        'Attestation de travail', 'Certificat de travail (fin de contrat)', 'Certificat de salaire', 'Attestation de revenu', 'Attestation de stage'
      ]},
      { name: 'nom_employe', type: 'text', label: 'Nom et prénom de l\'employé', required: true, placeholder: 'Ex: BENALI Ahmed' },
      { name: 'poste', type: 'text', label: 'Poste occupé', required: true, placeholder: 'Ex: Comptable' },
      { name: 'date_embauche', type: 'text', label: 'Date d\'embauche', required: true, placeholder: 'Ex: 01/03/2020' },
      { name: 'date_fin', type: 'text', label: 'Date de fin (si applicable)', placeholder: 'Laisser vide si toujours en poste' },
      { name: 'salaire_mensuel', type: 'number', label: 'Salaire mensuel brut (DZD)', placeholder: 'Ex: 80000' },
      { name: 'nom_entreprise', type: 'text', label: 'Nom de l\'entreprise', required: true, placeholder: 'Raison sociale' },
      { name: 'adresse_entreprise', type: 'text', label: 'Adresse de l\'entreprise', required: true },
    ],
    promptTemplate: `Tu es un gestionnaire RH expert en documents administratifs algériens.

TYPE : {{type_document}}
EMPLOYÉ : {{nom_employe}}
POSTE : {{poste}}
DATE EMBAUCHE : {{date_embauche}}
DATE FIN : {{date_fin}}
SALAIRE : {{salaire_mensuel}} DZD
ENTREPRISE : {{nom_entreprise}}
ADRESSE : {{adresse_entreprise}}

---

## 📋 {{type_document | uppercase}}

---

**{{nom_entreprise}}**
{{adresse_entreprise}}
Tél : _____________________
N° RC : _____________________
NIF : _____________________

---

### ATTESTATION DE TRAVAIL
N° : _____/2024

Je soussigné(e), _____________________, agissant en qualité de _____________________ de la société **{{nom_entreprise}}**,

Atteste par la présente que :

**Monsieur/Madame : {{nom_employe}}**

Né(e) le : _____________________
Demeurant à : _____________________
N° CNI : _____________________
N° Sécurité Sociale : _____________________

**Est employé(e) au sein de notre entreprise depuis le {{date_embauche}}**

En qualité de : **{{poste}}**

Type de contrat : CDI / CDD
Salaire mensuel brut : **{{salaire_mensuel}} DZD**
Salaire mensuel net : **[Calcul] DZD**

L'intéressé(e) est à ce jour toujours en fonction dans notre entreprise.

Cette attestation est délivrée à l'intéressé(e) pour servir et valoir ce que de droit.

---

Fait à _____________________, le ___/___/_____

**Le Responsable**
(Cachet et signature)

---

### 📌 Informations complémentaires

**Documents à joindre pour validation :**
- [ ] Copie CNI de l'employé
- [ ] Copie du contrat de travail
- [ ] Dernière fiche de paie

**Utilisation courante :**
- Demande de crédit bancaire
- Location immobilière
- Demande de visa
- Dossier administratif

### ⚖️ Base légale
- Loi n°90-11 du 21/04/1990 relative aux relations de travail
- Code du travail algérien`
  },

  'lettre-motivation-dz': {
    fields: [
      { name: 'type_candidature', type: 'select', label: 'Type de candidature', required: true, options: [
        'Candidature spontanée', 'Réponse à offre d\'emploi', 'Stage', 'Formation', 'Concours fonction publique'
      ]},
      { name: 'poste_vise', type: 'text', label: 'Poste visé', required: true, placeholder: 'Ex: Ingénieur commercial' },
      { name: 'entreprise', type: 'text', label: 'Entreprise/Organisation', required: true, placeholder: 'Nom de l\'entreprise' },
      { name: 'secteur', type: 'select', label: 'Secteur d\'activité', options: [
        'Informatique/Tech', 'Banque/Finance', 'Commerce', 'Industrie', 'Santé', 'Éducation', 'Administration publique', 'BTP', 'Énergie', 'Télécom', 'Autre'
      ]},
      { name: 'diplome', type: 'text', label: 'Votre diplôme', required: true, placeholder: 'Ex: Master en Gestion' },
      { name: 'experience', type: 'textarea', label: 'Expérience professionnelle', placeholder: 'Résumez vos expériences pertinentes...' },
      { name: 'competences', type: 'textarea', label: 'Compétences clés', placeholder: 'Listez vos compétences principales...' },
      { name: 'langue', type: 'select', label: 'Langue de la lettre', options: ['Français', 'Arabe'] },
    ],
    promptTemplate: `Tu es un expert en recrutement et rédaction de candidatures pour le marché algérien.

TYPE : {{type_candidature}}
POSTE : {{poste_vise}}
ENTREPRISE : {{entreprise}}
SECTEUR : {{secteur}}
DIPLÔME : {{diplome}}
EXPÉRIENCE : {{experience}}
COMPÉTENCES : {{competences}}
LANGUE : {{langue}}

---

## 📝 LETTRE DE MOTIVATION

---

**[Votre Nom et Prénom]**
[Votre Adresse]
[Code Postal, Ville]
Tél : [Votre numéro]
Email : [Votre email]

À [Ville], le [Date]

**À l'attention du Responsable des Ressources Humaines**
**{{entreprise}}**
[Adresse de l'entreprise]

**Objet : Candidature au poste de {{poste_vise}}**

Madame, Monsieur,

[PARAGRAPHE 1 - ACCROCHE]
Diplômé(e) en {{diplome}} et passionné(e) par le secteur {{secteur}}, je me permets de vous soumettre ma candidature pour le poste de {{poste_vise}} au sein de votre entreprise {{entreprise}}.

[PARAGRAPHE 2 - EXPÉRIENCE ET COMPÉTENCES]
Fort(e) de mon parcours professionnel, j'ai développé des compétences solides en :
{{competences}}

Mon expérience me permet d'apporter :
{{experience}}

[PARAGRAPHE 3 - MOTIVATION POUR L'ENTREPRISE]
Votre entreprise {{entreprise}} se distingue par [points forts de l'entreprise]. C'est avec enthousiasme que je souhaiterais contribuer à votre développement et mettre mes compétences au service de vos projets.

[PARAGRAPHE 4 - CONCLUSION]
Disponible pour un entretien à votre convenance, je reste à votre disposition pour tout complément d'information.

Dans l'attente de votre réponse favorable, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

[Signature]
**[Votre Nom]**

---

### P.J. : Curriculum Vitae

---

### 💡 Conseils pour le marché algérien

1. **Soignez la présentation** : Police classique, mise en page aérée
2. **Adaptez au secteur** : Public = plus formel, Privé = plus dynamique
3. **Mentionnez les langues** : Arabe, Français, Anglais si applicable
4. **Références locales** : Valorisez les expériences en Algérie
5. **Disponibilité** : Précisez si vous êtes disponible immédiatement

### 📌 Erreurs à éviter
- Fautes d'orthographe (faire relire)
- Lettre trop longue (1 page max)
- Formules génériques
- Oublier les coordonnées`
  },

  'telecom-dz-comparateur': {
    fields: [
      { name: 'usage_principal', type: 'select', label: 'Usage principal', required: true, options: [
        'Internet mobile (data)', 'Appels nationaux', 'International (diaspora)', 'Mixte (data + appels)', 'Internet fixe maison'
      ]},
      { name: 'budget_mensuel', type: 'select', label: 'Budget mensuel', required: true, options: [
        'Moins de 500 DZD', '500 - 1000 DZD', '1000 - 2000 DZD', '2000 - 3000 DZD', 'Plus de 3000 DZD'
      ]},
      { name: 'data_mensuelle', type: 'select', label: 'Besoin en data/mois', options: [
        'Moins de 5 Go', '5 - 15 Go', '15 - 30 Go', '30 - 50 Go', 'Plus de 50 Go', 'Illimité'
      ]},
      { name: 'operateur_actuel', type: 'select', label: 'Opérateur actuel', options: ['Mobilis', 'Djezzy', 'Ooredoo', 'Aucun'] },
      { name: 'zone', type: 'select', label: 'Zone de résidence', options: ['Grande ville (Alger, Oran, Constantine)', 'Ville moyenne', 'Zone rurale', 'Sud du pays'] },
    ],
    promptTemplate: `Tu es un expert télécom algérien spécialisé dans la comparaison des offres Mobilis, Djezzy et Ooredoo.

USAGE : {{usage_principal}}
BUDGET : {{budget_mensuel}}
DATA SOUHAITÉE : {{data_mensuelle}}
OPÉRATEUR ACTUEL : {{operateur_actuel}}
ZONE : {{zone}}

## 📱 Comparatif Forfaits Télécom Algérie

### Selon votre profil :
- Usage : {{usage_principal}}
- Budget : {{budget_mensuel}}
- Zone : {{zone}}

### 🏆 TOP 3 Recommandations

#### 1. [MEILLEUR CHOIX] - [Opérateur] - [Nom forfait]
| Élément | Détail |
|---------|--------|
| Prix | [X] DZD/mois |
| Data | [X] Go |
| Appels | [X] min |
| SMS | [X] |
| Validité | [X] jours |
| **Score rapport qualité/prix** | ⭐⭐⭐⭐⭐ |

#### 2. [ALTERNATIVE] - [Opérateur] - [Nom forfait]
[Détails similaires]

#### 3. [ÉCONOMIQUE] - [Opérateur] - [Nom forfait]
[Détails similaires]

### 📊 Comparatif détaillé

| Critère | Mobilis | Djezzy | Ooredoo |
|---------|---------|--------|---------|
| Couverture 4G | [Score] | [Score] | [Score] |
| Prix moyen data | [X] DZD/Go | [X] DZD/Go | [X] DZD/Go |
| Qualité réseau {{zone}} | [Score] | [Score] | [Score] |
| Service client | [Score] | [Score] | [Score] |

### 💡 Offres actuelles (janvier 2024)

**MOBILIS :**
- Forfait X : [Détails]
- Code USSD : *600#

**DJEZZY :**
- Forfait Y : [Détails]
- Code USSD : *720#

**OOREDOO :**
- Forfait Z : [Détails]
- Code USSD : *888#

### 📌 Conseils
1. [Conseil 1 selon profil]
2. [Conseil 2]
3. [Conseil 3]

### 🔄 Comment changer d'opérateur (Portabilité)
1. Vérifier éligibilité
2. Demander code RIO
3. Souscrire chez le nouvel opérateur
4. Délai : 24-48h

### 📞 Contacts
- Mobilis : 666 / www.mobilis.dz
- Djezzy : 777 / www.djezzy.dz
- Ooredoo : 888 / www.ooredoo.dz`
  },

  'algerie-poste-assistant': {
    fields: [
      { name: 'type_service', type: 'select', label: 'Type de service', required: true, options: [
        'Compte CCP (Chèque Postal)', 'BaridiMob', 'Mandat postal', 'Colis/Envoi', 'Western Union', 'Réclamation', 'Autre'
      ]},
      { name: 'type_demande', type: 'select', label: 'Votre demande', required: true, options: [
        'Ouverture de compte', 'Consultation solde', 'Virement', 'Retrait', 'Activation service', 'Problème/Panne', 'Tarifs'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Détails de votre question', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert des services d'Algérie Poste.

SERVICE : {{type_service}}
DEMANDE : {{type_demande}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 📮 Assistant Algérie Poste

### Service demandé : {{type_service}} - {{type_demande}}

### 1. Procédure détaillée

[Instructions selon le service et la demande]

### 2. Services CCP

**Ouverture de compte CCP :**
Documents requis :
- [ ] CNI originale + copie
- [ ] Extrait de naissance n°12
- [ ] 2 photos d'identité
- [ ] Justificatif de domicile
- Lieu : Bureau de poste de votre commune

**Numéro de compte CCP :**
Format : XXXXXX clé XX (ex: 123456 clé 12)

### 3. BaridiMob

**Activation :**
1. Télécharger l'app BaridiMob (Play Store / App Store)
2. S'inscrire avec numéro CCP
3. Recevoir code par SMS
4. Créer code PIN

**Services disponibles :**
- Consultation solde
- Virements CCP vers CCP
- Paiement factures (Sonelgaz, SEAAL, Mobilis...)
- Recharge téléphonique
- Transfert vers carte Edahabia

### 4. Tarifs

| Service | Tarif |
|---------|-------|
| Ouverture CCP | Gratuit |
| Virement CCP | 20 DZD |
| Retrait guichet | Gratuit |
| Mandat postal | Variable selon montant |
| Colis national | À partir de 150 DZD |

### 5. Contacts Algérie Poste

- **Numéro vert : 15 15**
- Site web : www.poste.dz
- BaridiMob : www.baridimob.dz
- Email : contact@poste.dz

### 6. Bureau de poste {{wilaya}}
- Horaires : Dimanche-Jeudi 8h-16h
- Adresse : [Consulter poste.dz pour localiser]

### ⚠️ En cas de problème
1. Contacter le 15 15
2. Se rendre au bureau de poste
3. Réclamation en ligne sur poste.dz

### 💡 Conseils
- Gardez toujours votre numéro CCP + clé
- Ne communiquez jamais votre code PIN BaridiMob
- Vérifiez régulièrement votre solde`
  },

  'scolarite-dz-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Inscription scolaire (primaire/moyen/secondaire)', 'Inscription universitaire',
        'Certificat de scolarité', 'Transfert d\'établissement', 'Bourse scolaire',
        'Résultats examens (Bac/BEM)', 'Orientation post-Bac', 'Recours/Réclamation'
      ]},
      { name: 'niveau', type: 'select', label: 'Niveau scolaire', options: [
        'Primaire', 'Moyen (CEM)', 'Secondaire (Lycée)', 'Universitaire (Licence)', 'Master', 'Doctorat', 'Formation professionnelle'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Détaillez votre demande...' },
    ],
    promptTemplate: `Tu es un expert du système éducatif algérien.

TYPE DE DEMANDE : {{type_demande}}
NIVEAU : {{niveau}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🎓 Assistant Scolarité Algérie

### Demande : {{type_demande}}

### 1. Procédure détaillée

[Instructions selon le niveau et le type de demande]

### 2. Calendrier scolaire 2024-2025

| Événement | Date |
|-----------|------|
| Rentrée scolaire | Septembre 2024 |
| Vacances d'automne | [Dates] |
| Vacances d'hiver | [Dates] |
| Vacances de printemps | [Dates] |
| BEM | Juin 2025 |
| Baccalauréat | Juin 2025 |
| Fin d'année | Juillet 2025 |

### 3. Inscription scolaire

**Documents requis (primaire/moyen/secondaire) :**
- [ ] Extrait de naissance
- [ ] Certificat de scolarité de l'année précédente
- [ ] Photos d'identité
- [ ] Certificat de résidence
- [ ] Carnet de santé (vaccinations)

**Inscription universitaire :**
- [ ] Relevé de notes Bac
- [ ] Attestation de succès Bac
- [ ] Fiche de vœux (orientation-esi.dz)

### 4. Bourses et aides

**Bourse universitaire :**
- Montant : 4 000 DZD/trimestre (environ)
- Demande via la plateforme PROGRES

**Prime de scolarité :**
- 5 000 DZD pour enfants scolarisés
- Versée via CCP en septembre

### 5. Contacts utiles

**Ministère de l'Éducation Nationale :**
- Site : www.education.gov.dz
- Résultats : bem.onec.dz / bac.onec.dz

**Ministère de l'Enseignement Supérieur :**
- Site : www.mesrs.dz
- Orientation : www.orientation-esi.dz
- Bourse PROGRES : progres.mesrs.dz

### 6. Direction de l'Éducation {{wilaya}}
- Adresse : [Selon wilaya]
- Horaires : Dimanche-Jeudi 8h-16h

### 💡 Conseils
1. Anticipez les inscriptions (dates limites strictes)
2. Conservez copies de tous les documents
3. Consultez régulièrement les sites officiels
4. En cas de problème, contactez d'abord l'établissement`
  },

  'logement-dz-assistant': {
    fields: [
      { name: 'programme', type: 'select', label: 'Programme logement', required: true, options: [
        'AADL (Location-vente)', 'LPP (Logement Promotionnel Public)',
        'Logement social (OPGI)', 'Aide CNL (construction/rural)',
        'LPA (Logement Promotionnel Aidé)', 'Information générale'
      ]},
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Nouvelle inscription', 'Suivi dossier', 'Paiement tranches', 'Recours', 'Choix du site', 'Remise des clés'
      ]},
      { name: 'situation_familiale', type: 'select', label: 'Situation familiale', options: ['Célibataire', 'Marié(e) sans enfants', 'Marié(e) avec enfants', 'Divorcé(e)', 'Veuf/Veuve'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert des programmes de logement en Algérie.

PROGRAMME : {{programme}}
TYPE DEMANDE : {{type_demande}}
SITUATION FAMILIALE : {{situation_familiale}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🏠 Assistant Logement Algérie

### Programme : {{programme}}

### 1. Présentation du programme

**AADL (Location-vente) :**
- Logements subventionnés avec paiement échelonné sur 25-30 ans
- Apport initial : 25% du prix
- Site : www.aadl.com.dz

**LPP (Logement Promotionnel Public) :**
- Pour revenus moyens
- Prix subventionné
- Site : www.lpp.dz

**Logement social (OPGI) :**
- Gratuit pour revenus modestes
- Dossier via la Daïra/APC
- Barème de points

**CNL (Aide à la construction) :**
- Aide financière pour auto-construction
- Jusqu'à 700 000 DZD en zone rurale

### 2. Conditions d'éligibilité

| Critère | {{programme}} |
|---------|---------------|
| Âge minimum | [X] ans |
| Revenu mensuel | [Tranche] |
| Propriétaire actuel | Non |
| Inscription antérieure | [Conditions] |

### 3. Documents requis

- [ ] Formulaire d'inscription
- [ ] Extrait de naissance
- [ ] Fiche familiale d'état civil
- [ ] Certificat de résidence
- [ ] Attestation de travail + fiches de paie
- [ ] Attestation de non-propriété (Conservation foncière)
- [ ] CNI

### 4. Procédure {{type_demande}}

[Instructions détaillées selon le type de demande]

### 5. Tranches de paiement (AADL)

| Tranche | Pourcentage | Montant estimé |
|---------|-------------|----------------|
| Apport initial | 25% | [X] DZD |
| 1ère tranche | 20% | [X] DZD |
| 2ème tranche | 20% | [X] DZD |
| Remise des clés | 15% | [X] DZD |
| Mensualités | 20% sur 25 ans | [X] DZD/mois |

### 6. Contacts

**AADL :**
- Site : www.aadl.com.dz
- Tel : 021 XX XX XX

**CNL (Caisse Nationale du Logement) :**
- Site : www.cnl.dz
- Tel : 021 XX XX XX

**OPGI {{wilaya}} :**
- [Adresse locale]

### 💡 Conseils
1. Inscrivez-vous dès que possible (listes longues)
2. Mettez à jour votre dossier régulièrement
3. Payez les tranches à temps pour éviter la radiation
4. Consultez le site officiel pour les nouvelles souscriptions`
  },

  // ===== BATCH 3 FINAL - MOYENNE PRIORITÉ (10) =====

  'etat-civil-assistant': {
    fields: [
      { name: 'type_acte', type: 'select', label: 'Type d\'acte', required: true, options: [
        'Acte de naissance (S12)', 'Acte de naissance intégral', 'Acte de mariage',
        'Acte de décès', 'Livret de famille', 'Fiche familiale d\'état civil',
        'Certificat de célibat', 'Apostille', 'Légalisation', 'Autre'
      ]},
      { name: 'motif', type: 'select', label: 'Motif de la demande', options: [
        'Première demande', 'Renouvellement', 'Perte/Vol', 'Correction d\'erreur',
        'Procédure administrative', 'Visa/Voyage', 'Mariage', 'Autre'
      ]},
      { name: 'commune_naissance', type: 'text', label: 'Commune de naissance/mariage', required: true, placeholder: 'Ex: Hussein Dey, Alger' },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Détails supplémentaires', placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert de l'état civil en Algérie.

TYPE D'ACTE : {{type_acte}}
MOTIF : {{motif}}
COMMUNE : {{commune_naissance}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 📋 Assistant État Civil Algérie

### 1. Document demandé : {{type_acte}}

**Description :**
[Explication du document et son utilité]

### 2. Procédure d'obtention

**Option 1 : En ligne (si disponible)**
- Site : www.interieur.gov.dz / www.eci.dz
- Délai : 24-72h
- Réception : Téléchargement ou envoi par email

**Option 2 : En mairie (APC)**
- Lieu : APC de {{commune_naissance}}, {{wilaya}}
- Horaires : 8h-16h du dimanche au jeudi
- Délai : Immédiat ou 24h

### 3. Documents requis
- [ ] CNI du demandeur (original + copie)
- [ ] Procuration légalisée (si tiers)
- [ ] Ancien livret de famille (si renouvellement)
- [ ] Timbre fiscal (si applicable)
- [ ] [Autres selon le type d'acte]

### 4. Coûts
| Élément | Montant |
|---------|---------|
| Acte standard | Gratuit |
| Copie certifiée | [X] DZD |
| Timbre fiscal | [X] DZD |
| Apostille | [X] DZD |

### 5. Délais légaux
- Acte de naissance S12 : Immédiat à 24h
- Livret de famille : 3-5 jours
- Apostille : 1-2 semaines

### 6. Cas particuliers

**Correction d'erreur :**
- Requête manuscrite au Procureur de la République
- Jugement du tribunal
- Transcription par l'officier d'état civil

**Pour les Algériens nés à l'étranger :**
- Acte transcrit au Ministère des Affaires Étrangères
- Ou consulat d'Algérie

### 📍 Contacts
- APC {{commune_naissance}} : [Adresse]
- Tel : 021 XX XX XX
- Site : www.interieur.gov.dz

### ⚖️ Base légale
- Code de l'état civil (Loi 14-08)
- Ordonnance 70-20`
  },

  'casier-judiciaire-assistant': {
    fields: [
      { name: 'type_bulletin', type: 'select', label: 'Type de bulletin', required: true, options: [
        'Bulletin n°3 (personnel)', 'Bulletin n°2 (autorités)', 'Certificat de bonne vie et mœurs'
      ]},
      { name: 'motif', type: 'select', label: 'Motif de la demande', required: true, options: [
        'Emploi', 'Visa/Immigration', 'Création d\'entreprise', 'Concours administratif',
        'Adoption', 'Autre procédure'
      ]},
      { name: 'lieu_naissance', type: 'text', label: 'Lieu de naissance', required: true, placeholder: 'Commune et wilaya de naissance' },
      { name: 'wilaya_residence', type: 'select', label: 'Wilaya de résidence actuelle', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Questions spécifiques', placeholder: 'Ex: Délai urgent pour visa...' },
    ],
    promptTemplate: `Tu es un expert des procédures judiciaires administratives en Algérie.

TYPE : {{type_bulletin}}
MOTIF : {{motif}}
LIEU DE NAISSANCE : {{lieu_naissance}}
WILAYA RÉSIDENCE : {{wilaya_residence}}
QUESTION : {{question}}

## 📋 Assistant Casier Judiciaire Algérie

### 1. Bulletin demandé : {{type_bulletin}}

**Bulletin n°3 :**
- Délivré à l'intéressé lui-même
- Mentions : Condamnations non effacées
- Usage : Emploi, visa, création entreprise

**Bulletin n°2 :**
- Réservé aux autorités administratives
- Plus détaillé que le B3

### 2. Procédure d'obtention

**Option 1 : En ligne (recommandé)**
- Site : www.mjustice.dz / casier-judiciaire.mjustice.dz
- Inscription avec email + téléphone
- Délai : 24-48h
- Réception : PDF par email ou retrait

**Option 2 : Au tribunal**
- Lieu : Tribunal de {{lieu_naissance}} (lieu de naissance)
- Ou : Tribunal de {{wilaya_residence}} (résidence)
- Horaires : 8h-14h du dimanche au jeudi

### 3. Documents requis
- [ ] CNI originale (présentation)
- [ ] Copie CNI
- [ ] Extrait de naissance récent (moins de 3 mois)
- [ ] Timbre fiscal de [X] DZD
- [ ] Formulaire de demande (sur place ou téléchargeable)

### 4. Coûts
| Élément | Montant |
|---------|---------|
| Bulletin n°3 | Gratuit (en ligne) ou [X] DZD |
| Timbre fiscal | [X] DZD |
| Certification | [X] DZD |

### 5. Délais
- En ligne : 24-48h
- Au tribunal : Immédiat ou 24-72h
- **Validité : 3 mois**

### 6. Cas particuliers

**Pour les Algériens nés à l'étranger :**
- Demande au Ministère de la Justice (Alger)
- Ou via consulat d'Algérie

**En cas d'inscription au casier :**
- Réhabilitation possible après délai légal
- Demande au Procureur de la République

### 📍 Contacts
- Service en ligne : casier-judiciaire.mjustice.dz
- Ministère de la Justice : 021 XX XX XX

### ⚖️ Base légale
- Code de procédure pénale (Articles 618 à 630)
- Loi 04-04 du 23/02/2004`
  },

  'service-national-assistant': {
    fields: [
      { name: 'situation', type: 'select', label: 'Votre situation', required: true, options: [
        'Convoqué (j\'ai reçu l\'ordre d\'appel)', 'Demande de report', 'Demande d\'exemption',
        'En cours de service', 'Recherche carte service national', 'Question générale'
      ]},
      { name: 'age', type: 'number', label: 'Votre âge', required: true, placeholder: '19-30' },
      { name: 'niveau_etudes', type: 'select', label: 'Niveau d\'études', options: [
        'Sans diplôme', 'Bac', 'Licence/Master', 'Doctorat', 'Formation professionnelle'
      ]},
      { name: 'motif_report', type: 'select', label: 'Motif de report/exemption (si applicable)', options: [
        'Études en cours', 'Soutien de famille (fils unique)', 'Problème de santé',
        'Travail à l\'étranger', 'Double nationalité', 'Autre'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert du service national en Algérie.

SITUATION : {{situation}}
ÂGE : {{age}} ans
NIVEAU D'ÉTUDES : {{niveau_etudes}}
MOTIF REPORT/EXEMPTION : {{motif_report}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🎖️ Assistant Service National Algérie

### 1. Votre situation : {{situation}}

### 2. Informations générales

**Âge d'appel :**
- 19 ans (révolus)
- Limite : 30 ans

**Durée du service :**
- 12 mois (standard)
- 9 mois (bac et plus)
- 6 mois (diplômes supérieurs, selon disponibilité)

### 3. Cas de report

**Report d'études (Article 12) :**
- Étudiants régulièrement inscrits
- Jusqu'à 27 ans (licence) ou 30 ans (doctorat)
- Documents : Certificat de scolarité annuel

**Report professionnel :**
- Contrat de travail à l'étranger
- Durée limitée

### 4. Cas d'exemption

| Motif | Condition |
|-------|-----------|
| Fils unique de veuve | Justificatif état civil |
| Soutien de famille | Enquête sociale |
| Inaptitude physique | Commission médicale |
| Pères de famille | 2+ enfants |

### 5. Documents requis

**Pour convocation :**
- [ ] Ordre d'appel
- [ ] CNI
- [ ] Extrait de naissance
- [ ] Photos d'identité
- [ ] Certificat médical

**Pour report :**
- [ ] Demande manuscrite au Wali
- [ ] Certificat de scolarité / contrat travail
- [ ] Extrait de naissance
- [ ] CNI

### 6. Procédure

1. Inscription au recensement (19 ans)
2. Réception ordre d'appel
3. Visite médicale d'incorporation
4. Affectation au centre de formation
5. Formation militaire de base (3 mois)
6. Affectation définitive

### 7. Après le service

**Carte du service national :**
- Document obligatoire pour emploi public
- Délivrée après accomplissement ou exemption
- Ou "situation régulière" après 30 ans

### 📍 Contacts
- Direction régionale du service national ({{wilaya}})
- Ministère de la Défense Nationale
- Tel : 021 XX XX XX

### ⚖️ Base légale
- Loi 14-06 relative au service national
- Ordonnance 74-103`
  },

  'banque-publique-assistant': {
    fields: [
      { name: 'banque', type: 'select', label: 'Banque concernée', required: true, options: [
        'BNA (Banque Nationale d\'Algérie)', 'CPA (Crédit Populaire d\'Algérie)',
        'BEA (Banque Extérieure d\'Algérie)', 'CNEP-Banque', 'BDL (Banque de Développement Local)',
        'BADR (Banque Agriculture)', 'Information générale'
      ]},
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Ouverture de compte', 'Crédit immobilier', 'Crédit auto', 'Crédit à la consommation',
        'Épargne (livret, DAT)', 'Carte bancaire (CIB)', 'Virement international', 'Réclamation', 'Autre'
      ]},
      { name: 'statut', type: 'select', label: 'Vous êtes', options: ['Salarié', 'Fonctionnaire', 'Commerçant', 'Profession libérale', 'Retraité', 'Étudiant', 'Sans emploi'] },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre demande...' },
    ],
    promptTemplate: `Tu es un conseiller bancaire expert du système bancaire public algérien.

BANQUE : {{banque}}
TYPE DE DEMANDE : {{type_demande}}
STATUT : {{statut}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🏦 Assistant Banques Publiques Algérie

### 1. {{banque}} - {{type_demande}}

### 2. Présentation des banques publiques

| Banque | Spécialité | Site |
|--------|-----------|------|
| BNA | Généraliste, agricole | www.bna.dz |
| CPA | Particuliers, PME | www.cpa-bank.dz |
| BEA | Commerce extérieur | www.bea.dz |
| CNEP | Épargne, immobilier | www.cnepbanque.dz |
| BDL | Collectivités, PME | www.bdl.dz |
| BADR | Agriculture | www.bafrbanque.dz |

### 3. Ouverture de compte

**Documents requis (compte courant) :**
- [ ] CNI originale + copie
- [ ] Extrait de naissance
- [ ] Justificatif de domicile (< 3 mois)
- [ ] 2 photos d'identité
- [ ] Attestation de travail + fiches de paie (si salarié)
- [ ] Registre de commerce (si commerçant)

**Dépôt minimum :** Variable selon banque (500-5000 DZD)

### 4. Crédits disponibles

**Crédit immobilier (CNEP spécialiste) :**
- Taux : 5-7% (bonifié)
- Durée : Jusqu'à 30 ans
- Apport : 10-20%
- Financement : Jusqu'à 80% du prix

**Crédit auto :**
- Véhicules neufs produits localement
- Taux : 5-8%
- Durée : 5-7 ans

**Crédit consommation :**
- Plafonné selon revenus
- Taux : 7-9%

### 5. Services en ligne

- BNA : e-bna.dz
- CPA : www.cpa-bank.dz/e-banking
- CNEP : www.cnepbanque.dz/cnep-net

**Carte CIB :**
- Paiement en ligne (Algérie)
- Retrait DAB
- Gratuite ou 500-1000 DZD/an

### 6. Agences {{wilaya}}

**{{banque}} - {{wilaya}} :**
- Adresse principale : [À vérifier sur site officiel]
- Horaires : 8h30-15h30 (dim-jeu)
- Tel : [Numéro agence]

### 💡 Conseils
1. Comparez les taux entre banques
2. CNEP est spécialisée pour l'immobilier
3. Préparez un dossier complet pour accélérer le traitement
4. Les fonctionnaires ont souvent des conditions préférentielles

### ⚖️ Base légale
- Loi 90-10 relative à la monnaie et au crédit
- Règlements Banque d'Algérie`
  },

  'nis-nif-assistant': {
    fields: [
      { name: 'type_identifiant', type: 'select', label: 'Identifiant recherché', required: true, options: [
        'NIF (Numéro d\'Identification Fiscale)', 'NIS (Numéro d\'Identification Statistique)',
        'Les deux (création entreprise)', 'Vérification/Recherche numéro existant'
      ]},
      { name: 'type_entite', type: 'select', label: 'Type d\'entité', required: true, options: [
        'Personne physique (auto-entrepreneur)', 'EURL', 'SARL', 'SPA', 'Association', 'Profession libérale'
      ]},
      { name: 'situation', type: 'select', label: 'Situation', options: [
        'Nouvelle création', 'Modification (adresse, activité)', 'Perte du numéro', 'Radiation', 'Vérification'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya d\'implantation', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Question spécifique', placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert en identification fiscale et statistique des entreprises en Algérie.

TYPE D'IDENTIFIANT : {{type_identifiant}}
TYPE D'ENTITÉ : {{type_entite}}
SITUATION : {{situation}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🔢 Assistant NIS/NIF Algérie

### 1. Différence NIS et NIF

| Identifiant | Signification | Délivré par | Usage |
|-------------|---------------|-------------|-------|
| **NIS** | N° Identification Statistique | ONS | Statistiques nationales |
| **NIF** | N° Identification Fiscale | DGI (Impôts) | Obligations fiscales |

### 2. Obtention du NIF

**Procédure :**
1. Création entreprise au CNRC (registre commerce)
2. Dépôt dossier au centre des impôts
3. Attribution automatique du NIF

**Documents requis :**
- [ ] Registre du commerce (extrait)
- [ ] Statuts (pour sociétés)
- [ ] CNI du gérant
- [ ] Justificatif du local
- [ ] Formulaire G1 rempli

**Délai :** 7-15 jours

**Format NIF :** XXXXXXXXXXXXXXXX (16 chiffres)

### 3. Obtention du NIS

**Procédure :**
- Automatique lors de l'immatriculation au CNRC
- Ou demande à l'ONS (Office National des Statistiques)

**Site ONS :** www.ons.dz

**Format NIS :** XXXXXXXXXXX (11 chiffres)

### 4. Vérification d'un numéro existant

**NIF :**
- Site DGI : www.mfdgi.gov.dz
- Service en ligne de vérification

**NIS :**
- Site CNRC : sidjilcom.cnrc.dz
- Recherche par dénomination

### 5. Cas de perte/oubli

**Récupération NIF :**
1. Centre des impôts de rattachement
2. Avec CNI + registre commerce

**Récupération NIS :**
1. Extrait CNRC (le NIS y figure)
2. Ou ONS avec registre commerce

### 6. Modification

En cas de changement (adresse, activité, gérant) :
1. Modification au CNRC d'abord
2. Déclaration aux impôts (modèle G1 bis)
3. Le NIF reste identique, seules les informations changent

### 📍 Contacts
- Centre des Impôts de {{wilaya}}
- ONS : 021 77 78 54
- CNRC : www.cnrc.dz

### ⚖️ Base légale
- Code des Impôts Directs
- Décret 96-63 relatif au NIS`
  },

  'administration-locale-guide': {
    fields: [
      { name: 'institution', type: 'select', label: 'Institution', required: true, options: [
        'APC (Mairie/Commune)', 'Daïra (Sous-préfecture)', 'Wilaya (Préfecture)',
        'Conservation foncière', 'Domaines', 'Urbanisme', 'Protection civile', 'Autre'
      ]},
      { name: 'type_demarche', type: 'select', label: 'Type de démarche', required: true, options: [
        'Légalisation de signature', 'Certificat de résidence', 'Attestation d\'hébergement',
        'Permis de construire', 'Acte de propriété', 'Extrait cadastral', 'Renseignements généraux', 'Autre'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
      { name: 'commune', type: 'text', label: 'Commune', placeholder: 'Ex: Hussein Dey' },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre démarche...' },
    ],
    promptTemplate: `Tu es un guide expert de l'administration locale en Algérie.

INSTITUTION : {{institution}}
TYPE DE DÉMARCHE : {{type_demarche}}
WILAYA : {{wilaya}}
COMMUNE : {{commune}}
QUESTION : {{question}}

## 🏛️ Guide Administration Locale - {{wilaya}}

### 1. {{institution}} - {{type_demarche}}

### 2. Organisation administrative algérienne

| Niveau | Nom | Responsable | Compétences |
|--------|-----|-------------|-------------|
| 1 | Wilaya (58) | Wali | Coordination régionale |
| 2 | Daïra | Chef de daïra | Contrôle, état civil |
| 3 | Commune/APC | P/APC (Maire) | Services de proximité |

### 3. Services de l'APC ({{commune}})

**Horaires standard :**
- Dimanche à Jeudi : 8h00 - 16h00
- Ramadan : 9h00 - 15h00

**Services disponibles :**
- État civil (naissances, mariages, décès)
- Légalisation de signatures
- Certificats de résidence
- Attestations diverses
- Urbanisme (PC, conformité)

### 4. Procédure : {{type_demarche}}

**Documents requis :**
- [ ] CNI originale
- [ ] [Documents spécifiques selon démarche]
- [ ] Timbre fiscal (si applicable)

**Délai :** [Variable selon démarche]

**Coût :** [Gratuit ou montant]

### 5. Services de la Daïra

- Visa de documents
- Transcription état civil
- Recours administratifs
- Coordination inter-communale

### 6. Services de la Wilaya

- Passeports et CNI biométriques
- Permis de conduire
- Cartes grises
- Affaires sociales
- Investissement (guichet unique)

### 7. Contacts {{wilaya}}

**APC {{commune}} :**
- Adresse : [Adresse mairie]
- Tel : [Numéro]

**Daïra de {{commune}} :**
- Adresse : [Adresse daïra]
- Tel : [Numéro]

**Wilaya {{wilaya}} :**
- Adresse : Siège de la wilaya
- Site : wilaya-{{wilaya}}.dz (si disponible)
- Tel : [Numéro standard]

### 💡 Conseils pratiques
1. Arrivez tôt (files d'attente)
2. Préparez tous les documents à l'avance
3. Faites des copies de tous les documents
4. Vérifiez les horaires spéciaux (été, ramadan)
5. Utilisez les services en ligne quand disponibles

### 🌐 Services en ligne
- État civil : www.interieur.gov.dz
- Rendez-vous passeport/CNI : www.passeport.interieur.gov.dz`
  },

  'recours-administratif-assistant': {
    fields: [
      { name: 'type_recours', type: 'select', label: 'Type de recours', required: true, options: [
        'Recours gracieux (à l\'auteur de la décision)', 'Recours hiérarchique (au supérieur)',
        'Recours devant le tribunal administratif', 'Recours au Médiateur de la République'
      ]},
      { name: 'objet_decision', type: 'select', label: 'Objet de la décision contestée', required: true, options: [
        'Refus de permis de construire', 'Refus de mutation', 'Décision fiscale',
        'Refus d\'inscription (logement, concours...)', 'Sanction disciplinaire',
        'Refus de visa/passeport', 'Autre décision administrative'
      ]},
      { name: 'date_decision', type: 'text', label: 'Date de la décision contestée', required: true, placeholder: 'JJ/MM/AAAA' },
      { name: 'administration', type: 'text', label: 'Administration concernée', required: true, placeholder: 'Ex: Direction de l\'Urbanisme, Wilaya d\'Alger' },
      { name: 'motifs', type: 'textarea', label: 'Motifs de contestation', required: true, placeholder: 'Expliquez pourquoi vous contestez cette décision...' },
      { name: 'wilaya', type: 'select', label: 'Wilaya', required: true, options: WILAYAS },
    ],
    promptTemplate: `Tu es un expert en contentieux administratif algérien.

TYPE DE RECOURS : {{type_recours}}
OBJET : {{objet_decision}}
DATE DE LA DÉCISION : {{date_decision}}
ADMINISTRATION : {{administration}}
MOTIFS : {{motifs}}
WILAYA : {{wilaya}}

## ⚖️ Assistant Recours Administratif

### 1. Type de recours recommandé : {{type_recours}}

### 2. Les différents recours

**1. Recours gracieux :**
- À l'auteur même de la décision
- Délai : 2 mois après notification
- Gratuit, suspend le délai contentieux

**2. Recours hiérarchique :**
- Au supérieur de l'auteur
- Délai : 2 mois après notification
- Gratuit, suspend le délai contentieux

**3. Recours contentieux :**
- Tribunal administratif compétent
- Délai : 4 mois après décision (ou rejet recours)
- Requête motivée + pièces

### 3. Délais à respecter ⚠️

| Étape | Délai |
|-------|-------|
| Recours gracieux/hiérarchique | 2 mois après décision |
| Réponse administration | 2 mois (silence = rejet) |
| Recours contentieux | 4 mois après décision/rejet |

**ATTENTION :** Passé ces délais, le recours est irrecevable !

### 4. Modèle de recours gracieux

---

**[Vos coordonnées]**
Nom : _____
Adresse : _____
{{wilaya}}

**À l'attention de :**
{{administration}}

**Objet :** Recours gracieux contre la décision du {{date_decision}}

Madame, Monsieur,

Par la présente, j'ai l'honneur de former un recours gracieux contre votre décision du {{date_decision}} portant [objet de la décision].

**Exposé des faits :**
[Résumer la situation]

**Motifs de contestation :**
{{motifs}}

**Ma demande :**
Je vous prie de bien vouloir reconsidérer votre décision et [préciser la demande].

Dans l'attente de votre réponse, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

Fait à _____, le _____

Signature

**Pièces jointes :**
- Copie de la décision contestée
- CNI
- [Autres pièces justificatives]

---

### 5. En cas de rejet

Si votre recours est rejeté (ou silence après 2 mois) :
1. Saisir le tribunal administratif de {{wilaya}}
2. Dans les 4 mois suivant le rejet
3. Avec l'aide d'un avocat (recommandé)

### 6. Le Médiateur de la République

En cas d'échec des recours :
- Institution indépendante
- Gratuit
- mediateur-republique.dz

### 📍 Contacts
- Tribunal administratif de {{wilaya}}
- Médiateur de la République : 021 XX XX XX

### ⚖️ Base légale
- Loi 08-09 portant code de procédure civile et administrative
- Articles 830 à 954 (contentieux administratif)`
  },

  'calculateur-salaire-net': {
    fields: [
      { name: 'salaire_base', type: 'number', label: 'Salaire de base mensuel (DZD)', required: true, placeholder: 'Ex: 50000' },
      { name: 'primes', type: 'number', label: 'Primes et indemnités imposables (DZD)', placeholder: 'Ex: 10000' },
      { name: 'statut', type: 'select', label: 'Statut', required: true, options: [
        'Salarié secteur privé', 'Fonctionnaire', 'Contractuel fonction publique', 'Cadre dirigeant'
      ]},
      { name: 'situation_familiale', type: 'select', label: 'Situation familiale', options: [
        'Célibataire', 'Marié(e) sans enfants', 'Marié(e) avec 1 enfant', 'Marié(e) avec 2 enfants',
        'Marié(e) avec 3+ enfants'
      ]},
      { name: 'avantages_nature', type: 'number', label: 'Avantages en nature (DZD)', placeholder: 'Ex: logement, voiture...' },
    ],
    promptTemplate: `Tu es un expert en paie et fiscalité des salaires en Algérie.

SALAIRE DE BASE : {{salaire_base}} DZD
PRIMES : {{primes}} DZD
STATUT : {{statut}}
SITUATION FAMILIALE : {{situation_familiale}}
AVANTAGES EN NATURE : {{avantages_nature}} DZD

## 💰 Calculateur Salaire Net Algérie

### 1. Récapitulatif du salaire brut

| Élément | Montant (DZD) |
|---------|---------------|
| Salaire de base | {{salaire_base}} |
| Primes et indemnités | {{primes}} |
| Avantages en nature | {{avantages_nature}} |
| **Salaire brut total** | **[Somme]** |

### 2. Cotisations sociales (Part salarié)

| Cotisation | Taux | Montant (DZD) |
|------------|------|---------------|
| CNAS (Sécurité sociale) | 9% | [Calcul] |
| **Total cotisations** | **9%** | **[Total]** |

### 3. Calcul de l'IRG (Impôt sur le Revenu Global)

**Base imposable :**
Salaire brut - Cotisations sociales - Abattement

**Abattement forfaitaire :** 40%
(Minimum 12 000 DZD/mois, Maximum 18 000 DZD/mois)

**Barème IRG 2024 (mensuel) :**

| Tranche mensuelle | Taux |
|-------------------|------|
| 0 - 20 000 DZD | 0% |
| 20 001 - 40 000 DZD | 23% |
| 40 001 - 80 000 DZD | 27% |
| 80 001 - 160 000 DZD | 30% |
| 160 001 - 320 000 DZD | 33% |
| > 320 000 DZD | 35% |

**Calcul détaillé :**

1. Salaire brut imposable : [X] DZD
2. Cotisations sociales (9%) : -[X] DZD
3. = Revenu après cotisations : [X] DZD
4. Abattement (40%, plafonné) : -[X] DZD
5. = **Base imposable** : [X] DZD
6. IRG calculé : [X] DZD

### 4. Récapitulatif final

| Élément | Montant (DZD) |
|---------|---------------|
| Salaire brut | [X] |
| - Cotisations CNAS (9%) | -[X] |
| - IRG | -[X] |
| **= SALAIRE NET** | **[X]** |

### 5. Charges patronales (pour info)

| Cotisation | Taux | Montant |
|------------|------|---------|
| CNAS employeur | 26% | [X] DZD |
| Œuvres sociales | 0.5% | [X] DZD |
| Formation | 1% | [X] DZD |
| **Total patronal** | **27.5%** | **[X] DZD** |

**Coût total employeur :** [Brut + Charges] DZD

### 6. Allocations familiales (si applicable)

| Enfants | Allocation mensuelle |
|---------|---------------------|
| 1 | 600 DZD |
| 2 | 1200 DZD |
| 3+ | 300 DZD/enfant supp. |

### 💡 Notes
- Les primes de rendement peuvent avoir un régime fiscal différent
- Certaines indemnités sont exonérées (transport, panier...)
- Le SMIG algérien est de 20 000 DZD (2024)

### ⚖️ Base légale
- Code des Impôts Directs (CIDTA)
- Loi de Finances 2024
- Loi 83-14 relative à la sécurité sociale`
  },

  'foncier-cadastre-assistant': {
    fields: [
      { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
        'Acte de propriété (livret foncier)', 'Extrait cadastral', 'Plan de situation',
        'Bornage de terrain', 'Vérification de propriété', 'Mutation foncière',
        'Certificat de non-litige', 'Autre'
      ]},
      { name: 'type_bien', type: 'select', label: 'Type de bien', required: true, options: [
        'Terrain nu', 'Maison individuelle', 'Appartement', 'Local commercial', 'Terrain agricole'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya du bien', required: true, options: WILAYAS },
      { name: 'commune', type: 'text', label: 'Commune du bien', required: true, placeholder: 'Ex: Kouba' },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre situation...' },
    ],
    promptTemplate: `Tu es un expert du foncier et du cadastre en Algérie.

TYPE DE DEMANDE : {{type_demande}}
TYPE DE BIEN : {{type_bien}}
WILAYA : {{wilaya}}
COMMUNE : {{commune}}
QUESTION : {{question}}

## 🏗️ Assistant Foncier & Cadastre Algérie

### 1. Votre demande : {{type_demande}}

### 2. Les institutions du foncier

| Institution | Rôle | Compétence |
|-------------|------|------------|
| **Conservation foncière** | Titres de propriété | Livrets fonciers, mutations |
| **Cadastre (DGC)** | Plans parcellaires | Extraits, bornage |
| **Domaines** | Biens de l'État | Concessions, ventes |
| **Notaire** | Actes authentiques | Ventes, donations |

### 3. Procédure : {{type_demande}}

**Acte de propriété (Livret foncier) :**

Si vous n'avez pas de titre :
1. Attestation de possession du président APC
2. Enquête cadastrale
3. Procédure de régularisation (Loi 90-25)

Documents requis :
- [ ] CNI
- [ ] Acte de vente / donation / succession
- [ ] Extrait cadastral
- [ ] Certificat de non-litige
- [ ] Plan de situation

**Extrait cadastral :**
1. Direction du Cadastre de {{wilaya}}
2. Avec références parcellaires ou adresse exacte
3. Délai : 3-7 jours

### 4. Documents fonciers types

| Document | Délivré par | Usage |
|----------|-------------|-------|
| Livret foncier | Conservation | Preuve de propriété |
| Extrait cadastral | Cadastre | Identification parcelle |
| Certificat de non-litige | Conservation | Vérification situation |
| Plan de situation | Cadastre | Localisation |

### 5. Coûts estimés

| Prestation | Tarif (DZD) |
|------------|-------------|
| Extrait cadastral | [X] DZD |
| Certificat de propriété | [X] DZD |
| Bornage (par géomètre) | Variable |
| Mutation foncière | % de la valeur |

### 6. Délais de traitement

- Extrait cadastral : 3-7 jours
- Certificat de propriété : 7-15 jours
- Mutation : 1-3 mois
- Régularisation foncière : Variable (plusieurs mois)

### 7. Problèmes fréquents et solutions

**Terrain sans titre :**
- Procédure de régularisation (art. 21 Loi 90-25)
- Attestation de possession + enquête

**Litige de propriété :**
- Tribunal compétent
- Expertise judiciaire

**Indivision (héritage) :**
- Partage notarié
- Ou maintien en indivision

### 📍 Contacts {{wilaya}}

**Conservation foncière {{wilaya}} :**
- Adresse : [Adresse]
- Tel : [Numéro]

**Direction du Cadastre {{wilaya}} :**
- Adresse : [Adresse]
- Tel : [Numéro]

### ⚖️ Base légale
- Loi 90-25 relative au foncier
- Loi 07-02 relative au cadastre
- Code civil (propriété immobilière)`
  },

  'visa-consulat-assistant': {
    fields: [
      { name: 'pays_destination', type: 'select', label: 'Pays de destination', required: true, options: [
        'France', 'Espagne', 'Italie', 'Allemagne', 'Belgique', 'Canada', 'États-Unis',
        'Royaume-Uni', 'Turquie', 'Tunisie', 'Maroc', 'Émirats Arabes Unis', 'Autre Schengen', 'Autre pays'
      ]},
      { name: 'type_visa', type: 'select', label: 'Type de visa', required: true, options: [
        'Tourisme / Visite familiale', 'Affaires', 'Études', 'Travail', 'Soins médicaux',
        'Transit', 'Long séjour / Installation'
      ]},
      { name: 'situation', type: 'select', label: 'Votre situation', options: [
        'Salarié', 'Fonctionnaire', 'Commerçant', 'Étudiant', 'Retraité', 'Sans emploi'
      ]},
      { name: 'wilaya', type: 'select', label: 'Wilaya de résidence', required: true, options: WILAYAS },
      { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre situation, motif du voyage...' },
    ],
    promptTemplate: `Tu es un expert des procédures de visa et services consulaires pour les Algériens.

PAYS DE DESTINATION : {{pays_destination}}
TYPE DE VISA : {{type_visa}}
SITUATION : {{situation}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## ✈️ Assistant Visa & Consulat

### 1. Visa {{pays_destination}} - {{type_visa}}

### 2. Informations générales

**Visa Schengen (France, Espagne, Italie, etc.) :**
- Durée : Court séjour (90 jours max sur 180 jours)
- Validité : Variable (multi-entrées possible)
- Délai de traitement : 15 jours (jusqu'à 45)

**Visa Canada / USA :**
- Procédure plus longue
- Biométrie obligatoire
- Entretien possible

### 3. Documents requis ({{type_visa}})

**Dossier de base :**
- [ ] Passeport valide (6 mois après retour)
- [ ] Formulaire de demande rempli
- [ ] Photos d'identité aux normes
- [ ] Assurance voyage (30 000 €)
- [ ] Justificatif d'hébergement (hôtel ou attestation)
- [ ] Billet d'avion (ou réservation)

**Justificatifs financiers :**
- [ ] Relevés bancaires (3-6 mois)
- [ ] Attestation de travail + fiches de paie
- [ ] Avis d'imposition (pour France)
- [ ] Justificatif de revenus/patrimoine

**Selon motif :**
- Visite familiale : Attestation d'accueil
- Affaires : Lettre d'invitation de l'entreprise
- Études : Inscription + ressources
- Soins : Certificat médical + prise en charge

### 4. Procédure de demande

**Étapes :**
1. **Prise de RDV** : Via VFS Global ou TLS Contact
   - France : fr.tlscontact.com/dz
   - Espagne : blsspainvisa.com
   - Canada : cic.gc.ca

2. **Dépôt du dossier** : Centre de visa de {{wilaya}} ou Alger

3. **Biométrie** : Prise d'empreintes sur place

4. **Traitement** : 15-45 jours selon pays

5. **Retrait** : Sur place ou par courrier

### 5. Coûts

| Élément | Montant |
|---------|---------|
| Frais de visa Schengen | 80-90 € |
| Frais de service (VFS/TLS) | 30-50 € |
| Assurance voyage | 20-50 € |
| **Total estimé** | **130-190 €** |

### 6. Centres de visa pour {{wilaya}}

**France (TLS Contact) :**
- Alger, Oran, Annaba
- RDV : fr.tlscontact.com/dz

**Espagne (BLS) :**
- Alger, Oran
- RDV : blsspainvisa.com

**Canada :**
- Dépôt en ligne + biométrie à Alger
- Site : ircc.canada.ca

### 7. Conseils pour augmenter vos chances

1. **Dossier complet** : Aucun document manquant
2. **Justificatifs solides** : Emploi stable, revenus réguliers
3. **Attaches au pays** : Propriété, famille, emploi
4. **Historique voyage** : Voyages précédents respectés
5. **Lettre de motivation** : Claire et cohérente

### 8. En cas de refus

- Délai de recours : 30-60 jours selon pays
- Recours gracieux ou contentieux
- Possibilité de redéposer avec dossier renforcé

### 📍 Ambassades/Consulats à Alger

- France : 25 Chemin Abdelkader Gadouche, Hydra
- Canada : 18 Rue Mustapha Khalef, Ben Aknoun
- Espagne : 46 Bis Rue Mohamed Chabani

### ⚠️ Attention aux arnaques
- Ne jamais payer pour un "visa garanti"
- Passer uniquement par les canaux officiels`
  },
};

// Config par défaut
const defaultFormConfig = {
  fields: [
    { name: 'question', type: 'textarea', label: 'Votre question', required: true, placeholder: 'Décrivez votre situation ou question...' },
    { name: 'wilaya', type: 'select', label: 'Wilaya', options: WILAYAS },
  ],
  promptTemplate: `Tu es un assistant administratif expert pour l'Algérie.

QUESTION : {{question}}
WILAYA : {{wilaya}}

Fournis une réponse complète avec :
1. Explication claire
2. Documents requis
3. Démarches à suivre
4. Délais
5. Contacts utiles`
};

// Icônes par sous-catégorie
const subcategoryIcons: Record<string, any> = {
  'securite-sociale': ShieldCheck,
  'fiscalite': Receipt,
  'entreprise': Building,
  'services-publics': Zap,
  'emploi': Briefcase,
  'documents-identite': CreditCard,
  'telecom': Phone,
  'juridique': Scale,
  'douanes': Package,
  'education': GraduationCap,
  'logement': Home,
};

export default function AdminDzToolPage() {
  const params = useParams();
  const toolSlug = params.toolSlug as string;

  const tool = adminDzTools.find(t => t.slug === toolSlug);
  const formConfig = toolFormConfigs[toolSlug] || defaultFormConfig;

  const [formData, setFormData] = useState<Record<string, any>>({});
  const [result, setResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!tool) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Outil non trouvé</h1>
          <Link href="/tools/admin-dz" className="text-green-600 hover:underline">
            Retour aux outils Admin Algérie
          </Link>
        </div>
      </div>
    );
  }

  const IconComponent = subcategoryIcons[tool.subcategory || ''] || Building;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulation - remplacer par appel API réel
    await new Promise(resolve => setTimeout(resolve, 2000));

    let response = formConfig.promptTemplate;
    Object.entries(formData).forEach(([key, value]) => {
      response = response.replace(new RegExp(`{{${key}}}`, 'g'), String(value || ''));
    });

    setResult(response);
    setIsLoading(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderField = (field: any) => {
    const value = formData[field.name] || '';

    switch (field.type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200"
            required={field.required}
          >
            <option value="">Sélectionner...</option>
            {field.options.map((opt: string) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        );
      case 'textarea':
        return (
          <textarea
            value={value}
            onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
            placeholder={field.placeholder}
            rows={4}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200"
            required={field.required}
          />
        );
      case 'number':
        return (
          <input
            type="number"
            value={value}
            onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
            placeholder={field.placeholder}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200"
            required={field.required}
          />
        );
      default:
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
            placeholder={field.placeholder}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200"
            required={field.required}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/admin-dz" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-3">
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
              🇩🇿 Exclusif Algérie
            </span>
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-8">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
              <IconComponent className="w-8 h-8 text-white" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
                <span className="bg-gradient-to-r from-green-500 to-green-600 text-white text-xs font-bold px-2 py-1 rounded-full">
                  🇩🇿 Exclusif
                </span>
              </div>
              <p className="text-gray-600 mb-3">{tool.description.fr}</p>
              <div className="flex items-center gap-3">
                <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
                  {tool.credits} crédits
                </span>
                <span className="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-sm">
                  {tool.subcategory?.replace('-', ' ')}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-green-600" />
            Remplissez le formulaire
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {formConfig.fields.map((field: any) => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {field.label}
                  {field.required && <span className="text-red-500 ml-1">*</span>}
                </label>
                {renderField(field)}
              </div>
            ))}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-green-700 hover:to-emerald-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Génération en cours...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Générer la réponse ({tool.credits} crédits)
                </>
              )}
            </button>
          </form>
        </div>

        {/* Result */}
        {result && (
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Check className="w-5 h-5 text-green-600" />
                Réponse générée
              </h2>
              <button
                onClick={handleCopy}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 px-3 py-1.5 rounded-lg hover:bg-gray-100"
              >
                {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                {copied ? 'Copié !' : 'Copier'}
              </button>
            </div>
            <div className="prose prose-green max-w-none bg-gray-50 rounded-lg p-4 whitespace-pre-wrap">
              {result}
            </div>
          </div>
        )}

        {/* Info Box */}
        <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5" />
            Informations importantes
          </h3>
          <ul className="text-sm text-green-800 space-y-2">
            <li>• Ces informations sont fournies à titre indicatif et ne remplacent pas un conseil professionnel</li>
            <li>• Les procédures et tarifs peuvent évoluer, vérifiez toujours auprès des organismes officiels</li>
            <li>• Conservez une copie de tous vos documents et récépissés</li>
            <li>• En cas de doute, contactez directement l'organisme concerné</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
