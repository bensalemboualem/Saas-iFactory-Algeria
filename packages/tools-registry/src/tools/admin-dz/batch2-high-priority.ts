import { AITool } from '../../types';

export const avocatVirtuelDz: AITool = {
  id: 'avocat-virtuel-dz',
  slug: 'avocat-virtuel-dz',
  name: { 
    fr: 'Avocat Virtuel DZ', 
    ar: 'المحامي الافتراضي', 
    en: 'Virtual Lawyer DZ'
  },
  description: {
    fr: 'Conseil juridique algérien : droit de la famille, pénal, civil, commercial, travail',
    ar: 'استشارات قانونية جزائرية: قانون الأسرة، الجنائي، المدني',
    en: 'Algerian legal advice: family, criminal, civil, commercial law'
  },
  category: 'admin-dz',
  subcategory: 'juridique',
  icon: 'Scale',
  credits: 25,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'domaine_juridique', type: 'select', label: 'Domaine juridique', required: true, options: [
      'Droit de la famille (mariage, divorce, héritage, garde)',
      'Droit civil (contrats, responsabilité, propriété)',
      'Droit commercial (sociétés, faillite, litiges)',
      'Droit du travail (licenciement, salaires, conflits)',
      'Droit pénal (infractions, procédures)',
      'Droit immobilier (vente, location, copropriété)',
      'Droit administratif (recours, contentieux)'
    ]},
    { name: 'situation', type: 'textarea', label: 'Décrivez votre situation', required: true },
    { name: 'role', type: 'select', label: 'Vous êtes', options: ['Demandeur', 'Défendeur', 'Victime', 'Témoin', 'Conseil'] },
    { name: 'urgence', type: 'select', label: 'Niveau d\'urgence', options: ['Information', 'Procédure en cours', 'Urgent'] }
  ],
  outputs: [{ type: 'markdown', name: 'legalAdvice' }],
  promptTemplate: `Tu es un avocat algérien expérimenté spécialisé en {{domaine_juridique}}.

DOMAINE : {{domaine_juridique}}
SITUATION : {{situation}}
RÔLE : {{role}}
URGENCE : {{urgence}}

## ⚖️ Consultation Juridique

### 1. Analyse de votre situation
[Analyse juridique selon le droit algérien]

### 2. Cadre légal applicable
**Textes de référence :**
{{#if domaine_juridique.includes('famille')}}
- Code de la famille algérien (Ordonnance 05-02 du 27 février 2005)
- Articles applicables : [X, Y, Z]
{{/if}}
{{#if domaine_juridique.includes('travail')}}
- Loi 90-11 relative aux relations de travail
- Convention collective applicable
{{/if}}
{{#if domaine_juridique.includes('commercial')}}
- Code de commerce algérien
- Registre du commerce (CNRC)
{{/if}}

### 3. Vos droits et obligations
✅ Vous avez le droit de : [...]
⚠️ Vous devez : [...]

### 4. Procédures recommandées
1. **Étape 1** : [Action + délai]
2. **Étape 2** : [Action + délai]
3. **Étape 3** : [Action + délai]

### 5. Documents à préparer
- [ ] Document 1
- [ ] Document 2
- [ ] ...

### 6. Juridiction compétente
- Tribunal : [Tribunal de première instance / Cour / Conseil]
- Localisation : Selon votre wilaya

### 7. Délais légaux
- Prescription : X ans
- Délai d'appel : X jours

### 8. Estimation des frais
- Frais de justice : ~X DZD
- Honoraires avocat : Variable

### ⚠️ Avertissement
Cette consultation est à titre informatif. Pour une défense en justice, consultez un avocat agréé près la cour.

### 📞 Contacts utiles
- Ordre des avocats : [Coordonnées barreau local]
- Aide juridictionnelle : Tribunal de votre wilaya`,
  model: 'claude',
  estimatedTime: '60s'
};

export const douaneCalculator: AITool = {
  id: 'douane-calculator',
  slug: 'douane-calculator',
  name: { 
    fr: 'Calculateur Douanes DZ', 
    ar: 'حاسبة الجمارك', 
    en: 'Algeria Customs Calculator'
  },
  description: {
    fr: 'Calculez les droits de douane, TVA et taxes pour vos importations en Algérie',
    ar: 'احسب الرسوم الجمركية وضريبة القيمة المضافة للواردات',
    en: 'Calculate customs duties, VAT and taxes for imports to Algeria'
  },
  category: 'admin-dz',
  subcategory: 'douanes',
  icon: 'Package',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_produit', type: 'select', label: 'Catégorie de produit', required: true, options: [
      'Véhicule (voiture, moto)',
      'Électronique (téléphone, PC, TV)',
      'Électroménager',
      'Vêtements et textiles',
      'Produits alimentaires',
      'Cosmétiques et parfums',
      'Machines et équipements industriels',
      'Matières premières',
      'Autre'
    ]},
    { name: 'valeur_caf', type: 'number', label: 'Valeur CAF (DZD)', required: true },
    { name: 'pays_origine', type: 'text', label: 'Pays d\'origine' },
    { name: 'code_douanier', type: 'text', label: 'Code SH (si connu)', placeholder: 'Ex: 8471.30.00' },
    { name: 'usage', type: 'select', label: 'Usage', options: ['Personnel', 'Commercial', 'Industriel'] },
    { name: 'regime', type: 'select', label: 'Régime douanier', options: ['Mise à la consommation', 'Admission temporaire', 'Transit', 'Zone franche'] }
  ],
  outputs: [{ type: 'markdown', name: 'customsCalculation' }],
  promptTemplate: `Tu es un déclarant en douane expert algérien.

PRODUIT : {{type_produit}}
VALEUR CAF : {{valeur_caf}} DZD
ORIGINE : {{pays_origine}}
CODE SH : {{code_douanier}}
USAGE : {{usage}}
RÉGIME : {{regime}}

## 📦 Calcul des Droits et Taxes à l'Importation

### 1. Identification du produit
- Position tarifaire : {{code_douanier}} (à confirmer)
- Catégorie : {{type_produit}}
- Origine : {{pays_origine}}

### 2. Base de calcul
| Élément | Montant |
|---------|---------|
| Valeur CAF | {{valeur_caf}} DZD |

### 3. Droits et taxes applicables

| Taxe | Taux | Base | Montant |
|------|------|------|---------|
| **Droit de Douane (DD)** | X% | Valeur CAF | X DZD |
| **TVA** | 19% | CAF + DD | X DZD |
| **Taxe de Domiciliation** | 4% | Valeur CAF | X DZD |

{{#if type_produit.includes('Véhicule')}}
| **Taxe sur Véhicules Neufs** | Variable | - | X DZD |
| **Vignette** | Selon puissance | - | X DZD |
{{/if}}

### 4. Récapitulatif

| | Montant |
|------|---------|
| Valeur CAF | {{valeur_caf}} DZD |
| Total droits et taxes | **X DZD** |
| **COÛT TOTAL DÉBARQUÉ** | **X DZD** |

### 5. Documents requis pour le dédouanement
- [ ] Facture commerciale
- [ ] Connaissement (B/L) ou LTA
- [ ] Certificat d'origine
- [ ] Liste de colisage
- [ ] Attestation de conformité
- [ ] Domiciliation bancaire (D10)
{{#if type_produit.includes('Véhicule')}}
- [ ] Carte grise pays d'origine
- [ ] Certificat de conformité
{{/if}}

### 6. Procédure
1. Domiciliation bancaire (30-60 jours avant)
2. Dépôt de déclaration (D10)
3. Contrôle et liquidation
4. Paiement des droits
5. Bon à enlever

### ⚠️ Produits interdits/contingentés
Vérifiez que votre produit n'est pas sur la liste des produits interdits à l'importation.

### 📞 Contacts Douanes
- Info : www.douane.gov.dz
- Guichet unique : GUCE (guce.finances.gov.dz)`,
  model: 'claude',
  estimatedTime: '40s'
};

export const contratLocationDz: AITool = {
  id: 'contrat-location-dz',
  slug: 'contrat-location-dz',
  name: { 
    fr: 'Générateur Contrat de Location', 
    ar: 'مولد عقد الإيجار', 
    en: 'Rental Contract Generator DZ'
  },
  description: {
    fr: 'Génère des contrats de location conformes au droit algérien (habitation, commercial, professionnel)',
    ar: 'إنشاء عقود إيجار متوافقة مع القانون الجزائري',
    en: 'Generate rental contracts compliant with Algerian law'
  },
  category: 'admin-dz',
  subcategory: 'juridique',
  icon: 'FileSignature',
  credits: 30,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_bail', type: 'select', label: 'Type de bail', required: true, options: [
      'Location habitation',
      'Local commercial',
      'Local professionnel',
      'Location meublée',
      'Terrain nu'
    ]},
    { name: 'bailleur_nom', type: 'text', label: 'Nom du bailleur (propriétaire)', required: true },
    { name: 'bailleur_adresse', type: 'text', label: 'Adresse du bailleur' },
    { name: 'bailleur_cni', type: 'text', label: 'N° CNI du bailleur' },
    { name: 'locataire_nom', type: 'text', label: 'Nom du locataire', required: true },
    { name: 'locataire_adresse', type: 'text', label: 'Adresse du locataire' },
    { name: 'locataire_cni', type: 'text', label: 'N° CNI du locataire' },
    { name: 'bien_adresse', type: 'text', label: 'Adresse du bien loué', required: true },
    { name: 'bien_description', type: 'textarea', label: 'Description du bien (surface, pièces...)' },
    { name: 'loyer_mensuel', type: 'number', label: 'Loyer mensuel (DZD)', required: true },
    { name: 'charges', type: 'number', label: 'Charges mensuelles (DZD)', default: 0 },
    { name: 'depot_garantie', type: 'number', label: 'Dépôt de garantie (DZD)' },
    { name: 'duree_bail', type: 'select', label: 'Durée du bail', options: ['1 an', '2 ans', '3 ans', '6 ans', '9 ans'] },
    { name: 'date_debut', type: 'text', label: 'Date de début du bail (JJ/MM/AAAA)' }
  ],
  outputs: [{ type: 'markdown', name: 'rentalContract' }],
  promptTemplate: `Tu es un notaire algérien expert en droit immobilier.

Génère un CONTRAT DE LOCATION COMPLET conforme au droit algérien.

TYPE : {{type_bail}}
BAILLEUR : {{bailleur_nom}}
LOCATAIRE : {{locataire_nom}}
BIEN : {{bien_adresse}}
LOYER : {{loyer_mensuel}} DZD/mois
DURÉE : {{duree_bail}}

---

# CONTRAT DE LOCATION {{type_bail | uppercase}}

**Conformément aux dispositions du Code Civil algérien (Ordonnance n°75-58 du 26 septembre 1975 modifiée et complétée)**

## ENTRE LES SOUSSIGNÉS :

**LE BAILLEUR :**
M./Mme {{bailleur_nom}}
Demeurant à : {{bailleur_adresse}}
Titulaire de la CNI n° : {{bailleur_cni}}
Ci-après dénommé "LE BAILLEUR"

**D'une part,**

**LE LOCATAIRE :**
M./Mme {{locataire_nom}}
Demeurant à : {{locataire_adresse}}
Titulaire de la CNI n° : {{locataire_cni}}
Ci-après dénommé "LE LOCATAIRE"

**D'autre part,**

## IL A ÉTÉ CONVENU CE QUI SUIT :

### ARTICLE 1 : OBJET
Le bailleur donne en location au locataire, qui accepte, le bien immobilier suivant :
- **Adresse** : {{bien_adresse}}
- **Description** : {{bien_description}}
- **Usage** : {{type_bail}}

### ARTICLE 2 : DURÉE
Le présent bail est consenti pour une durée de **{{duree_bail}}** à compter du **{{date_debut}}**.

### ARTICLE 3 : LOYER
Le loyer mensuel est fixé à **{{loyer_mensuel}} DZD** (X dinars algériens), payable d'avance le premier de chaque mois.
Charges mensuelles : {{charges}} DZD

### ARTICLE 4 : DÉPÔT DE GARANTIE
Le locataire verse ce jour au bailleur un dépôt de garantie de **{{depot_garantie}} DZD**, soit X mois de loyer, qui sera restitué en fin de bail, déduction faite des sommes dues.

### ARTICLE 5 : OBLIGATIONS DU BAILLEUR
Le bailleur s'engage à :
- Délivrer le bien en bon état
- Assurer la jouissance paisible
- Entretenir le bien (grosses réparations)
- Remettre les quittances de loyer

### ARTICLE 6 : OBLIGATIONS DU LOCATAIRE
Le locataire s'engage à :
- Payer le loyer aux échéances convenues
- User du bien en bon père de famille
- Effectuer les réparations locatives
- Ne pas sous-louer sans autorisation écrite
- Restituer le bien en bon état

### ARTICLE 7 : CHARGES
Les charges suivantes sont à la charge du locataire :
- Électricité, gaz, eau
- Ordures ménagères
- [Autres charges]

### ARTICLE 8 : RÉSILIATION
Le présent bail pourra être résilié :
- D'un commun accord des parties
- Par le locataire avec préavis de 3 mois
- Par le bailleur pour motif légitime avec préavis de 6 mois

### ARTICLE 9 : ÉTAT DES LIEUX
Un état des lieux contradictoire sera établi à l'entrée et à la sortie.

### ARTICLE 10 : ÉLECTION DE DOMICILE
Pour l'exécution du présent contrat, les parties élisent domicile à leurs adresses respectives.

### ARTICLE 11 : LITIGES
En cas de litige, les tribunaux de la wilaya du bien loué seront compétents.

---

**Fait à** ______________, **le** ______________

**En deux (2) exemplaires originaux**

**LE BAILLEUR** (Signature précédée de "Lu et approuvé")



**LE LOCATAIRE** (Signature précédée de "Lu et approuvé")



---

⚠️ **IMPORTANT** : Ce contrat doit être enregistré auprès des services fiscaux (Direction des Impôts) dans les 30 jours suivant sa signature. Droit d'enregistrement : 2% du loyer annuel (minimum 500 DZD).`,
  model: 'claude',
  estimatedTime: '90s'
};

export const statutsEntrepriseGenerator: AITool = {
  id: 'statuts-entreprise-generator',
  slug: 'statuts-entreprise-generator',
  name: { 
    fr: 'Générateur de Statuts', 
    ar: 'مولد القانون الأساسي', 
    en: 'Company Statutes Generator'
  },
  description: {
    fr: 'Génère des statuts de société conformes au Code de Commerce algérien (EURL, SARL, SPA, SNC)',
    ar: 'إنشاء القانون الأساسي للشركات وفقاً للقانون التجاري الجزائري',
    en: 'Generate company statutes compliant with Algerian Commercial Code'
  },
  category: 'admin-dz',
  subcategory: 'entreprise',
  icon: 'ScrollText',
  credits: 40,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'forme_juridique', type: 'select', label: 'Forme juridique', required: true, options: [
      'EURL (Entreprise Unipersonnelle à Responsabilité Limitée)',
      'SARL (Société à Responsabilité Limitée)',
      'SPA (Société Par Actions)',
      'SNC (Société en Nom Collectif)'
    ]},
    { name: 'denomination', type: 'text', label: 'Dénomination sociale', required: true },
    { name: 'objet_social', type: 'textarea', label: 'Objet social (activités)', required: true },
    { name: 'siege_social', type: 'text', label: 'Adresse du siège social', required: true },
    { name: 'capital_social', type: 'number', label: 'Capital social (DZD)', required: true },
    { name: 'associes', type: 'textarea', label: 'Associés (Nom, apport, parts)', helpText: 'Ex: Ahmed BENALI - 500 000 DZD - 50%' },
    { name: 'gerant', type: 'text', label: 'Gérant (nom complet)' },
    { name: 'duree', type: 'number', label: 'Durée de la société (années)', default: 99 }
  ],
  outputs: [{ type: 'markdown', name: 'companyStatutes' }],
  promptTemplate: `Tu es un juriste d'affaires algérien spécialisé en droit des sociétés.

Génère les STATUTS COMPLETS conformes au Code de Commerce algérien.

FORME : {{forme_juridique}}
DÉNOMINATION : {{denomination}}
CAPITAL : {{capital_social}} DZD
SIÈGE : {{siege_social}}

---

# STATUTS DE {{denomination}}
## {{forme_juridique | uppercase}}

**Conformément aux dispositions du Code de Commerce algérien (Ordonnance n°75-59 du 26 septembre 1975 modifiée)**

---

## TITRE I - FORME - OBJET - DÉNOMINATION - SIÈGE - DURÉE

### ARTICLE 1 : FORME
Il est formé entre les soussignés une société commerciale sous la forme d'une **{{forme_juridique | uppercase}}**, régie par les lois et règlements en vigueur en Algérie, notamment le Code de Commerce, ainsi que par les présents statuts.

### ARTICLE 2 : DÉNOMINATION
La société prend la dénomination : **{{denomination}}**

Dans tous les actes et documents, la dénomination sociale doit être précédée ou suivie des mots "{{forme_juridique | uppercase}}" et de l'indication du capital social.

### ARTICLE 3 : OBJET SOCIAL
La société a pour objet, en Algérie et à l'étranger :
{{objet_social}}

Et plus généralement, toutes opérations commerciales, industrielles, mobilières, immobilières et financières se rattachant directement ou indirectement à l'objet social.

### ARTICLE 4 : SIÈGE SOCIAL
Le siège social est fixé à : **{{siege_social}}**

Il pourra être transféré en tout autre lieu par décision de l'assemblée générale extraordinaire.

### ARTICLE 5 : DURÉE
La durée de la société est fixée à **{{duree}} années** à compter de la date de son immatriculation au registre du commerce.

---

## TITRE II - APPORTS - CAPITAL SOCIAL

### ARTICLE 6 : CAPITAL SOCIAL
Le capital social est fixé à la somme de **{{capital_social}} DZD** (X dinars algériens), divisé en X parts sociales de X DZD chacune, numérotées de 1 à X.

### ARTICLE 7 : APPORTS
Les apports sont les suivants :

{{associes}}

{{#if forme_juridique.includes('SARL') || forme_juridique.includes('EURL')}}
**Total des apports** : {{capital_social}} DZD
{{/if}}

### ARTICLE 8 : DÉPÔT DES FONDS
Les fonds correspondant aux apports en numéraire ont été déposés à la banque [NOM BANQUE], agence de [VILLE], au crédit d'un compte bloqué ouvert au nom de la société en formation.

---

## TITRE III - PARTS SOCIALES

### ARTICLE 9 : REPRÉSENTATION DES PARTS
Les parts sociales ne peuvent être représentées par des titres négociables.

### ARTICLE 10 : CESSION DE PARTS
{{#if forme_juridique.includes('EURL')}}
L'associé unique peut céder librement ses parts à toute personne de son choix.
{{else}}
Les parts sociales sont librement cessibles entre associés. Toute cession à un tiers est soumise à l'agrément de la majorité des associés représentant au moins les trois quarts du capital social.
{{/if}}

---

## TITRE IV - GÉRANCE

### ARTICLE 11 : NOMINATION DU GÉRANT
La société est gérée par un ou plusieurs gérants, personnes physiques, associés ou non.

Est nommé gérant : **{{gerant}}**

### ARTICLE 12 : POUVOIRS DU GÉRANT
Le gérant est investi des pouvoirs les plus étendus pour agir au nom de la société et l'engager envers les tiers.

### ARTICLE 13 : RÉMUNÉRATION
La rémunération du gérant est fixée par décision collective des associés.

---

## TITRE V - DÉCISIONS COLLECTIVES

### ARTICLE 14 : ASSEMBLÉES GÉNÉRALES
Les décisions collectives sont prises en assemblée générale.
- AGO : Majorité simple
- AGE : Majorité des 3/4 du capital

---

## TITRE VI - COMPTES ANNUELS - BÉNÉFICES

### ARTICLE 15 : EXERCICE SOCIAL
L'exercice social commence le 1er janvier et se termine le 31 décembre de chaque année.

### ARTICLE 16 : AFFECTATION DES BÉNÉFICES
Les bénéfices, diminués des charges, constituent le bénéfice net sur lequel sont prélevés :
- 5% pour la réserve légale (jusqu'à 10% du capital)
- Le solde est distribué ou reporté

---

## TITRE VII - DISSOLUTION - LIQUIDATION

### ARTICLE 17 : DISSOLUTION
La société est dissoute par l'arrivée du terme, décision des associés, ou toute autre cause légale.

---

## TITRE VIII - DISPOSITIONS DIVERSES

### ARTICLE 18 : CONTESTATIONS
Tout litige sera soumis aux tribunaux compétents du siège social.

### ARTICLE 19 : FORMALITÉS
Tous pouvoirs sont donnés au gérant pour effectuer les formalités légales.

---

**Fait à** ______________, **le** ______________

**LES ASSOCIÉS :**

{{associes}} (Signatures)

---

📋 **FORMALITÉS À ACCOMPLIR :**
1. [ ] Dépôt du capital à la banque
2. [ ] Enregistrement aux impôts
3. [ ] Publication au BOAL
4. [ ] Inscription au CNRC
5. [ ] Déclaration à la CNAS/CASNOS`,
  model: 'claude',
  estimatedTime: '120s'
};

export const attestationTravailGenerator: AITool = {
  id: 'attestation-travail-generator',
  slug: 'attestation-travail-generator',
  name: { 
    fr: 'Générateur Attestation de Travail', 
    ar: 'مولد شهادة العمل', 
    en: 'Work Certificate Generator'
  },
  description: {
    fr: 'Génère des attestations de travail, certificats de salaire et documents RH conformes',
    ar: 'إنشاء شهادات العمل ووثائق الموارد البشرية',
    en: 'Generate work certificates and HR documents'
  },
  category: 'admin-dz',
  subcategory: 'emploi',
  icon: 'FileCheck',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_document', type: 'select', label: 'Type de document', required: true, options: [
      'Attestation de travail',
      'Certificat de salaire',
      'Attestation de congé',
      'Certificat d\'expérience'
    ]},
    { name: 'entreprise_nom', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'entreprise_adresse', type: 'text', label: 'Adresse de l\'entreprise' },
    { name: 'entreprise_rc', type: 'text', label: 'N° Registre de Commerce' },
    { name: 'employe_nom', type: 'text', label: 'Nom complet de l\'employé', required: true },
    { name: 'employe_fonction', type: 'text', label: 'Fonction/Poste', required: true },
    { name: 'date_embauche', type: 'text', label: 'Date d\'embauche (JJ/MM/AAAA)', required: true },
    { name: 'date_fin', type: 'text', label: 'Date de fin (si applicable)' },
    { name: 'salaire', type: 'number', label: 'Salaire mensuel (DZD)' },
    { name: 'motif', type: 'text', label: 'Motif de l\'attestation', placeholder: 'Ex: Pour servir et valoir ce que de droit' }
  ],
  outputs: [{ type: 'markdown', name: 'hrDocument' }],
  promptTemplate: `Génère un document RH officiel conforme aux normes algériennes.

TYPE : {{type_document}}
ENTREPRISE : {{entreprise_nom}}
EMPLOYÉ : {{employe_nom}}
FONCTION : {{employe_fonction}}

---

{{#if type_document === 'Attestation de travail'}}
# ATTESTATION DE TRAVAIL

**{{entreprise_nom}}**
{{entreprise_adresse}}
RC : {{entreprise_rc}}

---

**ATTESTATION DE TRAVAIL**

Je soussigné(e), [Nom du responsable], agissant en qualité de [Directeur/Gérant] de la société **{{entreprise_nom}}**, atteste par la présente que :

**M./Mme {{employe_nom}}**

Est employé(e) au sein de notre entreprise depuis le **{{date_embauche}}** en qualité de :

**{{employe_fonction}}**

{{#if date_fin}}
jusqu'au **{{date_fin}}**.
{{else}}
et est toujours en fonction à ce jour.
{{/if}}

Cette attestation est délivrée à l'intéressé(e) à sa demande pour servir et valoir ce que de droit.

**Fait à** ______________, **le** ______________

**Le Directeur / Gérant**
(Signature et cachet)

---
{{/if}}

{{#if type_document === 'Certificat de salaire'}}
# CERTIFICAT DE SALAIRE

**{{entreprise_nom}}**
{{entreprise_adresse}}
RC : {{entreprise_rc}}

---

**CERTIFICAT DE SALAIRE**

Nous soussignés, certifions que **M./Mme {{employe_nom}}**, employé(e) de notre société en qualité de **{{employe_fonction}}**, perçoit une rémunération mensuelle de :

| Élément | Montant |
|---------|---------|
| Salaire de base | X DZD |
| Prime de rendement | X DZD |
| Indemnités | X DZD |
| **SALAIRE BRUT** | **{{salaire}} DZD** |

Retenues :
- IRG : X DZD
- Cotisation SS : X DZD

**SALAIRE NET** : **X DZD**

**Fait à** ______________, **le** ______________

**Le Service des Ressources Humaines**
(Signature et cachet)
{{/if}}`,
  model: 'claude',
  estimatedTime: '30s'
};

export const lettreMotivationDz: AITool = {
  id: 'lettre-motivation-dz',
  slug: 'lettre-motivation-dz',
  name: { 
    fr: 'Lettre de Motivation DZ', 
    ar: 'رسالة التحفيز', 
    en: 'Motivation Letter DZ'
  },
  description: {
    fr: 'Lettres de motivation adaptées au marché algérien (public, privé, étranger)',
    ar: 'رسائل تحفيز مكيفة للسوق الجزائري',
    en: 'Motivation letters adapted for Algerian job market'
  },
  category: 'admin-dz',
  subcategory: 'emploi',
  icon: 'PenTool',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'type_emploi', type: 'select', label: 'Type d\'employeur', options: ['Entreprise privée', 'Secteur public', 'ONG', 'Entreprise étrangère'] },
    { name: 'poste', type: 'text', label: 'Poste visé', required: true },
    { name: 'entreprise', type: 'text', label: 'Entreprise', required: true },
    { name: 'candidat_nom', type: 'text', label: 'Votre nom', required: true },
    { name: 'diplome', type: 'text', label: 'Dernier diplôme' },
    { name: 'experience', type: 'textarea', label: 'Résumé de votre expérience' },
    { name: 'competences', type: 'tags', label: 'Compétences clés' },
    { name: 'source_offre', type: 'text', label: 'Source de l\'offre (ANEM, site web...)' }
  ],
  outputs: [{ type: 'markdown', name: 'coverLetter' }],
  promptTemplate: `Tu es un conseiller en emploi expert du marché algérien.

Génère une lettre de motivation professionnelle et percutante.

POSTE : {{poste}}
ENTREPRISE : {{entreprise}}
TYPE : {{type_emploi}}
CANDIDAT : {{candidat_nom}}
DIPLOME : {{diplome}}
COMPÉTENCES : {{competences}}

[Génère une lettre complète, adaptée au contexte algérien, en français professionnel]`,
  model: 'claude',
  estimatedTime: '45s'
};

export const telecomDzAssistant: AITool = {
  id: 'telecom-dz-assistant',
  slug: 'telecom-dz-assistant',
  name: { 
    fr: 'Assistant Télécom DZ', 
    ar: 'مساعد الاتصالات', 
    en: 'Algeria Telecom Assistant'
  },
  description: {
    fr: 'Guide Mobilis, Djezzy, Ooredoo : forfaits, 4G/5G, réclamations, recharge, résiliation',
    ar: 'دليل موبيليس، جازي، أوريدو',
    en: 'Guide for Mobilis, Djezzy, Ooredoo services'
  },
  category: 'admin-dz',
  subcategory: 'services-publics',
  icon: 'Smartphone',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'operateur', type: 'select', label: 'Opérateur', required: true, options: ['Mobilis', 'Djezzy', 'Ooredoo', 'Algérie Télécom'] },
    { name: 'type_demande', type: 'select', label: 'Type de demande', options: [
      'Comparer forfaits', 'Problème réseau', 'Recharge', 'Portabilité', 'Résiliation', 'Nouvelle ligne', 'Internet fixe', 'Fibre'
    ]},
    { name: 'details', type: 'textarea', label: 'Décrivez votre besoin', required: true }
  ],
  outputs: [{ type: 'markdown', name: 'telecomHelp' }],
  promptTemplate: `Tu es un expert des opérateurs télécom algériens.

OPÉRATEUR : {{operateur}}
DEMANDE : {{type_demande}}
DÉTAILS : {{details}}

## 📱 Assistance Télécom {{operateur | uppercase}}

[Fournis une réponse complète avec les forfaits actuels, codes USSD, contacts, et procédures]

### Contacts {{operateur}}
{{#if operateur === 'Mobilis'}}
- Service client : 666 ou 888
- Site : www.mobilis.dz
- App : My Mobilis
{{/if}}
{{#if operateur === 'Djezzy'}}
- Service client : 777
- Site : www.djezzy.dz
- App : Djezzy App
{{/if}}
{{#if operateur === 'Ooredoo'}}
- Service client : 333
- Site : www.ooredoo.dz
- App : My Ooredoo
{{/if}}`,
  model: 'claude',
  estimatedTime: '20s'
};

export const algeriePosteAssistant: AITool = {
  id: 'algerie-poste-assistant',
  slug: 'algerie-poste-assistant',
  name: { 
    fr: 'Assistant Algérie Poste & CCP', 
    ar: 'مساعد بريد الجزائر', 
    en: 'Algeria Post & CCP Assistant'
  },
  description: {
    fr: 'Services postaux, CCP, BaridiMob, mandats, colis, ECCP, virement',
    ar: 'الخدمات البريدية، الحساب البريدي الجاري، باريدي موب',
    en: 'Postal services, CCP accounts, BaridiMob, transfers'
  },
  category: 'admin-dz',
  subcategory: 'services-publics',
  icon: 'Mail',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'service', type: 'select', label: 'Service', required: true, options: [
      'Compte CCP',
      'BaridiMob',
      'Virement / Mandat',
      'Colis / EMS',
      'e-CCP (services en ligne)',
      'Ouverture de compte'
    ]},
    { name: 'question', type: 'textarea', label: 'Votre question', required: true }
  ],
  outputs: [{ type: 'markdown', name: 'postalHelp' }],
  promptTemplate: `Tu es un agent expert d'Algérie Poste.

SERVICE : {{service}}
QUESTION : {{question}}

## 📮 Assistance Algérie Poste

[Fournis des informations précises sur les services postaux algériens]

### Services disponibles
- CCP : Compte Chèque Postal
- BaridiMob : Paiement mobile
- ECCP : Services en ligne (eccp.poste.dz)
- EMS : Courrier express
- Mandats : National et international

### Contacts
- Info : 1530
- Site : www.poste.dz
- BaridiMob : baridimob.poste.dz`,
  model: 'claude',
  estimatedTime: '20s'
};

export const scolariteDzAssistant: AITool = {
  id: 'scolarite-dz-assistant',
  slug: 'scolarite-dz-assistant',
  name: { 
    fr: 'Assistant Scolarité DZ', 
    ar: 'مساعد التمدرس', 
    en: 'Algeria Education Assistant'
  },
  description: {
    fr: 'Inscription scolaire, bourses, examens (BAC, BEM, 5ème), orientation universitaire',
    ar: 'التسجيل المدرسي، المنح، الامتحانات، التوجيه الجامعي',
    en: 'School enrollment, scholarships, exams, university guidance'
  },
  category: 'admin-dz',
  subcategory: 'education',
  icon: 'GraduationCap',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'niveau', type: 'select', label: 'Niveau concerné', options: ['Primaire', 'CEM', 'Lycée', 'Université', 'Formation pro'] },
    { name: 'sujet', type: 'select', label: 'Sujet', options: [
      'Inscription', 'Bourse', 'Examen BAC', 'Examen BEM', 'Examen 5ème', 'Orientation', 'Transfert', 'Équivalence'
    ]},
    { name: 'wilaya', type: 'select', label: 'Wilaya', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
    { name: 'question', type: 'textarea', label: 'Votre question', required: true }
  ],
  outputs: [{ type: 'markdown', name: 'educationHelp' }],
  promptTemplate: `Tu es un conseiller d'orientation scolaire expert du système éducatif algérien.

NIVEAU : {{niveau}}
SUJET : {{sujet}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🎓 Assistance Scolarité Algérie

[Fournis des informations précises selon le système éducatif algérien, calendrier MEN, dates importantes, procédures]

### Sites officiels
- Ministère Éducation : www.education.gov.dz
- Résultats examens : bem.onec.dz / bac.onec.dz
- Orientation universitaire : www.orientation-esi.dz
- Bourse : www.mesrs.dz`,
  model: 'claude',
  estimatedTime: '30s'
};

export const logementDzAssistant: AITool = {
  id: 'logement-dz-assistant',
  slug: 'logement-dz-assistant',
  name: { 
    fr: 'Assistant Logement AADL/LPA', 
    ar: 'مساعد السكن عدل/LPA', 
    en: 'Algeria Housing Assistant'
  },
  description: {
    fr: 'Programmes de logement AADL, LPA, LPP, social : inscription, suivi, paiement',
    ar: 'برامج السكن: عدل، LPA، LPP، الاجتماعي',
    en: 'Housing programs: AADL, LPA, LPP, social housing'
  },
  category: 'admin-dz',
  subcategory: 'logement',
  icon: 'Home',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: true,
  inputs: [
    { name: 'programme', type: 'select', label: 'Programme', required: true, options: [
      'AADL (Location-vente)',
      'LPA (Logement Promotionnel Aidé)',
      'LPP (Logement Promotionnel Public)',
      'Logement social',
      'Logement rural'
    ]},
    { name: 'demande', type: 'select', label: 'Type de demande', options: ['Éligibilité', 'Inscription', 'Suivi dossier', 'Paiement', 'Clé'] },
    { name: 'wilaya', type: 'select', label: 'Wilaya', options: ['Alger', 'Oran', 'Constantine', 'Autre'] },
    { name: 'question', type: 'textarea', label: 'Votre question', required: true }
  ],
  outputs: [{ type: 'markdown', name: 'housingHelp' }],
  promptTemplate: `Tu es un expert des programmes de logement en Algérie.

PROGRAMME : {{programme}}
DEMANDE : {{demande}}
WILAYA : {{wilaya}}
QUESTION : {{question}}

## 🏠 Assistance Logement {{programme | uppercase}}

### Conditions d'éligibilité
{{#if programme === 'AADL'}}
- Ne pas être propriétaire
- Ne pas avoir bénéficié d'aide de l'État
- Revenu : 6-12 fois le SNMG
- Âge : +21 ans
{{/if}}

### Procédure d'inscription
1. Inscription en ligne : aadl.com.dz
2. Constitution du dossier
3. Convocation et dépôt
4. Versement initial
5. Attribution

### Contacts
{{#if programme.includes('AADL')}}
- Site : www.aadl.com.dz
- Espace souscripteur : inscription.aadl.com.dz
{{/if}}`,
  model: 'claude',
  estimatedTime: '35s'
};
