import { AITool } from '../../types';

export const permisConduireAssistant: AITool = {
  id: 'permis-conduire-assistant',
  slug: 'permis-conduire-assistant',
  name: { 
    fr: 'Assistant Permis de Conduire', 
    ar: 'مساعد رخصة السياقة', 
    en: 'Driving License Assistant'
  },
  description: {
    fr: 'Inscription, examen code et conduite, renouvellement, duplicata, permis international',
    ar: 'التسجيل، امتحان السياقة، التجديد، رخصة دولية',
    en: 'Registration, driving test, renewal, international license'
  },
  category: 'admin-dz',
  subcategory: 'documents-identite',
  icon: 'Car',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
      'Nouvelle demande (inscription auto-école)',
      'Préparation examen du code',
      'Préparation examen de conduite',
      'Renouvellement permis',
      'Duplicata (perte/vol)',
      'Permis international',
      'Conversion permis étranger',
      'Consultation points'
    ]},
    { name: 'categorie', type: 'select', label: 'Catégorie de permis', options: ['A', 'B', 'C', 'D', 'E'] },
    { name: 'wilaya', type: 'select', label: 'Wilaya', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
    { name: 'question', type: 'textarea', label: 'Votre question' }
  ],
  outputs: [{ type: 'markdown', name: 'licenseHelp' }],
  promptTemplate: `Tu es un expert du permis de conduire en Algérie.

TYPE DE DEMANDE : {{type_demande}}
CATÉGORIE : {{categorie}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🚗 Assistant Permis de Conduire

### Procédure pour {{type_demande}}

{{#if type_demande.includes('Nouvelle')}}
**Étapes pour obtenir le permis catégorie {{categorie}} :**

1. **Inscription auto-école agréée**
   - Documents requis :
     - [ ] Extrait de naissance
     - [ ] Certificat de résidence
     - [ ] Photos d'identité (6)
     - [ ] Certificat médical (médecin agréé)
     - [ ] Timbre fiscal

2. **Formation théorique (Code)**
   - Durée : 20-30 heures
   - Examen : 40 questions, 32 bonnes réponses minimum

3. **Formation pratique**
   - Durée : 20 heures minimum
   - Examen : Parcours en circulation

4. **Coûts estimés**
   - Auto-école : 25 000 - 40 000 DZD
   - Timbre permis : 2 000 DZD
   - Visite médicale : 1 000 - 2 000 DZD
{{/if}}

{{#if type_demande.includes('code')}}
**Préparation examen du code :**

📚 **Thèmes à maîtriser :**
1. Signalisation routière (panneaux, marquage)
2. Règles de priorité
3. Distances de sécurité
4. Limitations de vitesse
5. Alcool et conduite
6. Premiers secours

**Astuces :**
- Utilisez les apps de code (Code Route Algérie)
- 32/40 minimum pour réussir
- Délai entre tentatives : 15 jours
{{/if}}

{{#if type_demande.includes('international')}}
**Permis international :**
- Validité : 3 ans
- Documents : Permis national + photos + timbre
- Délai : 48-72h
- Où : Daïra de résidence
{{/if}}

### Contacts utiles
- Direction des transports de wilaya
- Site : permisdeconduire.interieur.gov.dz`,
  model: 'claude',
  estimatedTime: '20s'
};

export const carteGriseAssistant: AITool = {
  id: 'carte-grise-assistant',
  slug: 'carte-grise-assistant',
  name: { 
    fr: 'Assistant Carte Grise', 
    ar: 'مساعد البطاقة الرمادية', 
    en: 'Vehicle Registration Assistant'
  },
  description: {
    fr: 'Immatriculation véhicule, changement de propriétaire, duplicata, mutation',
    ar: 'تسجيل المركبات، تغيير الملكية، التكرار',
    en: 'Vehicle registration, ownership transfer, duplicate'
  },
  category: 'admin-dz',
  subcategory: 'documents-identite',
  icon: 'FileText',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_demande', type: 'select', label: 'Type de demande', required: true, options: [
      'Nouvelle immatriculation (véhicule neuf)',
      'Mutation (changement propriétaire)',
      'Duplicata (perte/vol/détérioration)',
      'Modification (changement caractéristiques)',
      'Radiation (casse/export)'
    ]},
    { name: 'type_vehicule', type: 'select', label: 'Type de véhicule', options: ['Voiture', 'Moto', 'Camion', 'Utilitaire', 'Remorque'] },
    { name: 'wilaya', type: 'select', label: 'Wilaya d\'immatriculation', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
    { name: 'details', type: 'textarea', label: 'Précisions sur votre situation' }
  ],
  outputs: [{ type: 'markdown', name: 'registrationHelp' }],
  promptTemplate: `Tu es un expert en immatriculation de véhicules en Algérie.

## 📋 Procédure {{type_demande}}

{{#if type_demande.includes('Mutation')}}
**Changement de propriétaire :**

1. **Documents vendeur :**
   - [ ] Carte grise originale
   - [ ] CNI
   - [ ] Certificat de non-gage (daïra)
   - [ ] Contrôle technique valide

2. **Documents acheteur :**
   - [ ] CNI
   - [ ] Certificat de résidence
   - [ ] Contrat de vente (légalisé)
   - [ ] Attestation d'assurance

3. **Frais :**
   - Timbre mutation : selon puissance fiscale
   - Droits d'enregistrement : 4% du prix

4. **Délai :** 7-15 jours

⚠️ **Important :** La mutation doit être faite dans les 30 jours suivant la vente.
{{/if}}

### Contacts
- Daïra de {{wilaya}}
- Direction des transports de wilaya`,
  model: 'claude',
  estimatedTime: '20s'
};

export const etatCivilAssistant: AITool = {
  id: 'etat-civil-assistant',
  slug: 'etat-civil-assistant',
  name: { 
    fr: 'Assistant État Civil', 
    ar: 'مساعد الحالة المدنية', 
    en: 'Civil Status Assistant'
  },
  description: {
    fr: 'Extraits de naissance, actes de mariage, livret de famille, légalisation, apostille',
    ar: 'شهادات الميلاد، عقود الزواج، دفتر العائلة',
    en: 'Birth certificates, marriage acts, family book, legalization'
  },
  category: 'admin-dz',
  subcategory: 'documents-identite',
  icon: 'Users',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'document', type: 'select', label: 'Document demandé', required: true, options: [
      'Extrait de naissance (S12)',
      'Extrait de naissance intégral',
      'Acte de mariage',
      'Acte de décès',
      'Livret de famille',
      'Fiche familiale d\'état civil',
      'Légalisation de signature',
      'Apostille (usage étranger)'
    ]},
    { name: 'commune_naissance', type: 'text', label: 'Commune de naissance/événement' },
    { name: 'annee', type: 'number', label: 'Année de l\'acte' },
    { name: 'urgence', type: 'boolean', label: 'Demande urgente' }
  ],
  outputs: [{ type: 'markdown', name: 'civilStatusHelp' }],
  promptTemplate: `Tu es un officier d'état civil expert en Algérie.

## 📜 Obtenir {{document}}

### Procédure standard
1. **Lieu de demande :** APC de {{commune_naissance}}
2. **Documents requis :**
   - [ ] Pièce d'identité
   - [ ] Ancien document (si renouvellement)
   
3. **Délai :** 
   - Sur place : Immédiat à 24h
   - En ligne : 3-7 jours

### Demande en ligne 🌐
Site : etatcivil.interieur.gov.dz
- Création compte
- Téléversement pièces
- Retrait APC ou envoi postal

### Coût
- Extrait de naissance : Gratuit
- Légalisation : 20 DZD/signature

{{#if document === 'Apostille (usage étranger)'}}
### Apostille (Convention de La Haye)
L'Algérie n'étant PAS partie à la Convention, il faut :
1. Légalisation au ministère des Affaires étrangères
2. Légalisation au consulat du pays de destination
{{/if}}`,
  model: 'claude',
  estimatedTime: '15s'
};

export const casierJudiciaireAssistant: AITool = {
  id: 'casier-judiciaire-assistant',
  slug: 'casier-judiciaire-assistant',
  name: { 
    fr: 'Assistant Casier Judiciaire', 
    ar: 'مساعد صحيفة السوابق', 
    en: 'Criminal Record Assistant'
  },
  description: {
    fr: 'Demande de casier judiciaire (Bulletin n°3), procédure en ligne et sur place',
    ar: 'طلب صحيفة السوابق العدلية',
    en: 'Criminal record request (Bulletin #3)'
  },
  category: 'admin-dz',
  subcategory: 'documents-identite',
  icon: 'FileSearch',
  credits: 8,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_bulletin', type: 'select', label: 'Type de bulletin', options: ['B3', 'B2'] },
    { name: 'motif', type: 'select', label: 'Motif de la demande', options: ['Emploi', 'Visa', 'Commerce', 'Concours', 'Autre'] },
    { name: 'urgence', type: 'boolean', label: 'Procédure express' },
    { name: 'lieu_naissance', type: 'text', label: 'Lieu de naissance (wilaya)' }
  ],
  outputs: [{ type: 'markdown', name: 'criminalRecordHelp' }],
  promptTemplate: `## 📋 Casier Judiciaire - Bulletin {{type_bulletin}}

### Demande en ligne (recommandé) 🌐
**Site :** casier-judiciaire.mjustice.dz

1. Créer un compte
2. Remplir le formulaire
3. Payer en ligne (BaridiMob/CIB)
4. Recevoir par email (PDF sécurisé)

**Délai :** 24-72h
**Coût :** 200 DZD

### Demande sur place
**Lieu :** Tribunal de {{lieu_naissance}} (lieu de naissance)

**Documents :**
- [ ] Extrait de naissance S12
- [ ] Photocopie CNI
- [ ] Timbre fiscal 200 DZD

**Délai :** 24-48h

### Validité
- Durée : 3 mois
- Renouvelable à chaque demande

### Pour les Algériens à l'étranger
Demande via le consulat ou en ligne`,
  model: 'claude',
  estimatedTime: '20s'
};

export const serviceNationalAssistant: AITool = {
  id: 'service-national-assistant',
  slug: 'service-national-assistant',
  name: { 
    fr: 'Assistant Service National', 
    ar: 'مساعد الخدمة الوطنية', 
    en: 'National Service Assistant'
  },
  description: {
    fr: 'Recensement, exemption, report, carte de service national, attestation',
    ar: 'الإحصاء، الإعفاء، التأجيل، بطاقة الخدمة الوطنية',
    en: 'Census, exemption, deferral, national service card'
  },
  category: 'admin-dz',
  subcategory: 'documents-identite',
  icon: 'Shield',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'demande', type: 'select', label: 'Type de demande', required: true, options: [
      'Recensement (19 ans)',
      'Report pour études',
      'Demande d\'exemption',
      'Attestation de position',
      'Carte de service national',
      'Dispense (soutien de famille, santé)'
    ]},
    { name: 'situation', type: 'textarea', label: 'Décrivez votre situation', required: true },
    { name: 'age', type: 'number', label: 'Votre âge' },
    { name: 'etudiant', type: 'boolean', label: 'Êtes-vous étudiant ?' }
  ],
  outputs: [{ type: 'markdown', name: 'nationalServiceHelp' }],
  promptTemplate: `Tu es un expert du service national algérien.

## 🎖️ Service National - {{demande}}

### Règles générales
- Âge de recensement : 19 ans
- Durée du service : 12 mois
- Service civil possible (certains cas)

{{#if demande.includes('Report')}}
### Report pour études

**Conditions :**
- Être inscrit dans un établissement reconnu
- Report jusqu'à 27 ans (études supérieures)
- Report jusqu'à 30 ans (doctorat)

**Documents :**
- Certificat de scolarité
- Attestation de position
- Demande manuscrite

**Où :** Bureau de la conscription (moquataa militaire)
{{/if}}

{{#if demande.includes('exemption')}}
### Cas d'exemption
- Fils unique de chahid
- Soutien de famille unique
- Inaptitude médicale (commission)
- +30 ans (sous conditions)
{{/if}}

### Contacts
- Site : www.mdn.dz
- Bureau de conscription de votre commune`,
  model: 'claude',
  estimatedTime: '25s'
};

export const banquePubliqueAssistant: AITool = {
  id: 'banque-publique-assistant',
  slug: 'banque-publique-assistant',
  name: { 
    fr: 'Assistant Banques Publiques', 
    ar: 'مساعد البنوك العمومية', 
    en: 'Public Banks Assistant'
  },
  description: {
    fr: 'CPA, BNA, BDL, CNEP, BADR : ouverture compte, crédit, épargne, services',
    ar: 'فتح حساب، قروض، ادخار، خدمات بنكية',
    en: 'Account opening, loans, savings, banking services'
  },
  category: 'admin-dz',
  subcategory: 'services-publics',
  icon: 'Landmark',
  credits: 12,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'banque', type: 'select', label: 'Banque', required: true, options: [
      'CPA (Crédit Populaire d\'Algérie)',
      'BNA (Banque Nationale d\'Algérie)',
      'BDL (Banque de Développement Local)',
      'CNEP-Banque',
      'BADR (Banque Agriculture et Développement Rural)'
    ]},
    { name: 'service', type: 'select', label: 'Service recherché', options: [
      'Ouverture compte', 'Crédit immobilier', 'Crédit consommation', 'Crédit auto', 
      'Épargne', 'Carte CIB', 'E-banking', 'Crédit entreprise'
    ]},
    { name: 'details', type: 'textarea', label: 'Précisions', required: true }
  ],
  outputs: [{ type: 'markdown', name: 'bankingHelp' }],
  promptTemplate: `Tu es un conseiller bancaire expert des banques publiques algériennes.

## 🏦 {{banque}} - {{service}}

{{#if service === 'Ouverture compte'}}
### Ouverture de compte

**Documents requis :**
- [ ] CNI + copie
- [ ] Extrait de naissance
- [ ] Justificatif de domicile
- [ ] Photo d'identité
- [ ] Versement initial : 1 000 - 5 000 DZD

**Types de comptes :**
- Compte courant
- Compte épargne (taux ~3%)
- Compte devises
{{/if}}

{{#if service === 'Crédit immobilier'}}
### Crédit immobilier {{banque}}

**Conditions générales :**
- Âge : 21-70 ans (fin de crédit)
- Ancienneté emploi : 1-2 ans
- Apport personnel : 10-20%
- Durée : jusqu'à 30-40 ans

**Taux indicatif :** 5-7% (bonifié avec épargne préalable)

**Simulation :**
Pour un crédit de X DZD sur Y ans :
- Mensualité estimée : ~Z DZD
{{/if}}

### Contacts {{banque}}
{{#if banque.includes('CNEP')}}
- Site : www.cnepbanque.dz
- Tél : 021 XX XX XX
- Agences : 200+ en Algérie
{{/if}}`,
  model: 'claude',
  estimatedTime: '40s'
};

export const nisNifAssistant: AITool = {
  id: 'nis-nif-assistant',
  slug: 'nis-nif-assistant',
  name: { 
    fr: 'Assistant NIS/NIF', 
    ar: 'مساعد NIS/NIF', 
    en: 'NIS/NIF Tax Numbers Assistant'
  },
  description: {
    fr: 'Obtention du NIS (Numéro d\'Identification Statistique) et NIF (Numéro d\'Identification Fiscale)',
    ar: 'الحصول على رقم التعريف الإحصائي والجبائي',
    en: 'Obtain NIS and NIF identification numbers'
  },
  category: 'admin-dz',
  subcategory: 'entreprise',
  icon: 'Hash',
  credits: 12,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'numero', type: 'select', label: 'Numéro demandé', required: true, options: [
      'NIF (Numéro d\'Identification Fiscale)',
      'NIS (Numéro d\'Identification Statistique)',
      'NIF + NIS'
    ]},
    { name: 'type_entite', type: 'select', label: 'Type d\'entité', options: ['Personne physique', 'EURL', 'SARL', 'SPA', 'Association'] },
    { name: 'situation', type: 'select', label: 'Situation', options: ['Nouvelle activité', 'Régularisation', 'Mise à jour', 'Vérification'] }
  ],
  outputs: [{ type: 'markdown', name: 'taxIdHelp' }],
  promptTemplate: `Tu es un expert des formalités administratives d'entreprise en Algérie.

## 🔢 Obtention {{numero}}

### NIF (Numéro d'Identification Fiscale)
**Obligatoire pour :** Toute activité commerciale, professionnelle ou artisanale

**Où l'obtenir :** Direction des Impôts (Centre des Impôts)

**Documents requis :**
- [ ] Registre du commerce
- [ ] Statuts (pour sociétés)
- [ ] CNI du gérant
- [ ] Contrat de location du local

**Délai :** 48h-7 jours
**Coût :** Gratuit

### NIS (Numéro d'Identification Statistique)
**Délivré par :** ONS (Office National des Statistiques)

**Documents :**
- [ ] NIF
- [ ] Registre du commerce
- [ ] Formulaire NIS

**Délai :** 7-15 jours

### Vérification en ligne
- NIF : jibayatic.mf.gov.dz
- NIS : ons.dz`,
  model: 'claude',
  estimatedTime: '20s'
};

export const administrationLocaleGuide: AITool = {
  id: 'administration-locale-guide',
  slug: 'administration-locale-guide',
  name: { 
    fr: 'Guide Administration Locale', 
    ar: 'دليل الإدارة المحلية', 
    en: 'Local Administration Guide'
  },
  description: {
    fr: 'Toutes les démarches Wilaya, Daïra, APC : attestations, autorisations, légalisations',
    ar: 'جميع الإجراءات: الولاية، الدائرة، البلدية',
    en: 'All procedures: Wilaya, Daïra, APC'
  },
  category: 'admin-dz',
  subcategory: 'services-publics',
  icon: 'Building',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'administration', type: 'select', label: 'Administration', required: true, options: [
      'APC (Mairie/Commune)',
      'Daïra',
      'Wilaya'
    ]},
    { name: 'document', type: 'select', label: 'Document/Service demandé', options: [
      'Certificat de résidence', 'Légalisation', 'Attestation de non emploi', 'Autorisation de construire',
      'Attestation de non propriété', 'Certificat de vie', 'Certificat de célibat', 'Autorisation de commerce'
    ]},
    { name: 'wilaya', type: 'select', label: 'Votre wilaya', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
    { name: 'commune', type: 'text', label: 'Votre commune' }
  ],
  outputs: [{ type: 'markdown', name: 'adminGuide' }],
  promptTemplate: `Tu es un expert de l'administration locale algérienne.

## 🏛️ {{administration}} - {{document}}

### Documents délivrés par l'APC (Mairie)
- Certificat de résidence
- Légalisation de signature/documents
- Extrait de naissance
- Certificat de vie
- Attestation de célibat

### Documents délivrés par la Daïra
- Certificat de non-gage (véhicules)
- Permis de conduire
- Carte grise
- Autorisations diverses

### Documents délivrés par la Wilaya
- Permis de construire (grands projets)
- Autorisations spéciales
- Recours administratifs

### Procédure pour {{document}}
{{#if document === 'Certificat de résidence'}}
**Lieu :** APC de résidence
**Documents :**
- CNI
- Justificatif domicile (facture Sonelgaz/SEAAL)
**Délai :** Immédiat à 24h
**Coût :** Gratuit
{{/if}}`,
  model: 'claude',
  estimatedTime: '20s'
};

export const recoursAdministratifAssistant: AITool = {
  id: 'recours-administratif-assistant',
  slug: 'recours-administratif-assistant',
  name: { 
    fr: 'Assistant Recours Administratif', 
    ar: 'مساعد الطعن الإداري', 
    en: 'Administrative Appeal Assistant'
  },
  description: {
    fr: 'Rédiger et déposer un recours gracieux, hiérarchique ou contentieux contre l\'administration',
    ar: 'تقديم طعن إداري ضد قرار إداري',
    en: 'Draft and file administrative appeals'
  },
  category: 'admin-dz',
  subcategory: 'juridique',
  icon: 'FileWarning',
  credits: 20,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_recours', type: 'select', label: 'Type de recours', required: true, options: [
      'Recours gracieux (même autorité)',
      'Recours hiérarchique (autorité supérieure)',
      'Recours contentieux (tribunal administratif)'
    ]},
    { name: 'administration', type: 'text', label: 'Administration concernée', required: true },
    { name: 'decision_contestee', type: 'textarea', label: 'Décision contestée (résumé)', required: true },
    { name: 'motifs', type: 'textarea', label: 'Motifs de contestation', required: true },
    { name: 'demandeur', type: 'text', label: 'Votre nom complet' }
  ],
  outputs: [{ type: 'markdown', name: 'appealDraft' }],
  promptTemplate: `Tu es un expert en contentieux administratif algérien.

## ⚖️ {{type_recours}} contre {{administration}}

### Modèle de recours

---

**[Lieu], le [Date]**

**De :** {{demandeur}}
**À :** Autorité compétente

**Objet :** {{type_recours}} contre [décision/refus] du [date]

**Madame, Monsieur,**

J'ai l'honneur de porter à votre attention le recours suivant contre la décision [référence] du [date] par laquelle [résumé de la décision].

**EXPOSÉ DES FAITS :**
{{decision_contestee}}

**MOTIFS DU RECOURS :**
{{motifs}}

**EN DROIT :**
- Conformément à la loi n°08-09 du 25 février 2008 portant code de procédure civile et administrative
- [Articles de loi pertinents]

**PAR CES MOTIFS :**
Je sollicite de votre haute bienveillance :
1. L'annulation de la décision contestée
2. [Demande spécifique]

Dans l'attente d'une suite favorable, veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

**[Signature]**

---

### Délais à respecter
- Recours gracieux/hiérarchique : 2 mois après notification
- Recours contentieux : 4 mois après notification (ou 2 mois après rejet du recours gracieux)

### Juridiction compétente
Tribunal administratif de la wilaya`,
  model: 'claude',
  estimatedTime: '60s'
};

export const calculateurSalaireNet: AITool = {
  id: 'calculateur-salaire-net',
  slug: 'calculateur-salaire-net',
  name: { 
    fr: 'Calculateur Salaire Net Algérie', 
    ar: 'حاسبة الراتب الصافي', 
    en: 'Net Salary Calculator Algeria'
  },
  description: {
    fr: 'Calculez votre salaire net à partir du brut : IRG, cotisations CNAS, primes',
    ar: 'احسب راتبك الصافي من الإجمالي',
    en: 'Calculate net salary from gross: IRG, CNAS contributions'
  },
  category: 'admin-dz',
  subcategory: 'emploi',
  icon: 'Calculator',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'salaire_base', type: 'number', label: 'Salaire de base (DZD)', required: true },
    { name: 'primes', type: 'number', label: 'Primes imposables (DZD)', default: 0 },
    { name: 'indemnites_non_imposables', type: 'number', label: 'Indemnités non imposables (transport...)', default: 0 },
    { name: 'situation_familiale', type: 'select', label: 'Situation familiale', options: ['Célibataire', 'Marié 0 enfant', 'Marié 1 enfant', 'Marié 2 enfants', 'Marié 3 enfants et plus'] },
    { name: 'secteur', type: 'select', label: 'Secteur', options: ['Privé', 'Public', 'Fonction publique'] }
  ],
  outputs: [{ type: 'markdown', name: 'salaryCalculation' }],
  promptTemplate: `Tu es un expert en paie algérienne.

## 💰 Calcul du Salaire Net

### Données saisies
- Salaire de base : {{salaire_base}} DZD
- Primes imposables : {{primes}} DZD
- Indemnités non imposables : {{indemnites_non_imposables}} DZD
- Situation : {{situation_familiale}}

### Calcul détaillé

| Élément | Montant |
|---------|---------|
| **Salaire de base** | {{salaire_base}} DZD |
| **+ Primes imposables** | {{primes}} DZD |
| **= SALAIRE BRUT IMPOSABLE** | **X DZD** |

#### Cotisations sociales (part salariale)
| Cotisation | Taux | Montant |
|------------|------|---------|
| Sécurité sociale (CNAS) | 9% | X DZD |
| **Total cotisations** | **9%** | **X DZD** |

#### Impôt sur le Revenu Global (IRG)
| Étape | Calcul |
|-------|--------|
| Salaire imposable | X DZD |
| Abattement 40% | -X DZD (min 1000, max 1500/mois) |
| Base IRG | X DZD |
| IRG barème | X DZD |

**Barème IRG 2024 :**
- 0 - 20 000 DZD : 0%
- 20 001 - 40 000 DZD : 23%
- 40 001 - 80 000 DZD : 27%
- 80 001 - 160 000 DZD : 30%
- 160 001 - 320 000 DZD : 33%
- > 320 000 DZD : 35%

### RÉSULTAT

| | Montant |
|---|---------|
| Salaire brut | X DZD |
| - Cotisations CNAS | -X DZD |
| - IRG | -X DZD |
| + Indemnités non imposables | +{{indemnites_non_imposables}} DZD |
| **= SALAIRE NET** | **X DZD** |

### Charges employeur (pour info)
- Cotisations patronales : 26% du brut = X DZD
- **Coût total employeur** : X DZD`,
  model: 'claude',
  estimatedTime: '15s'
};
