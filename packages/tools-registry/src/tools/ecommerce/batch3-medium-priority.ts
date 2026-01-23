import { AITool } from '../../types';

export const supplierEmailTemplate: AITool = {
  id: 'supplier-email-template',
  slug: 'supplier-email-template',
  name: { fr: 'Email Fournisseurs', ar: 'بريد الموردين', en: 'Supplier Email Template' },
  description: {
    fr: 'Rédigez des emails professionnels pour contacter et négocier avec vos fournisseurs',
    ar: 'اكتب رسائل بريد احترافية للتواصل والتفاوض مع الموردين',
    en: 'Write professional emails to contact and negotiate with suppliers'
  },
  category: 'ecommerce',
  subcategory: 'b2b',
  icon: 'Factory',
  credits: 12,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'email_type', type: 'select', label: 'Type d\'email', required: true, options: [
      'Premier contact',
      'Demande de devis',
      'Négociation de prix',
      'Demande d\'échantillons',
      'Problème de commande',
      'Conditions de paiement',
      'Demande d\'exclusivité'
    ]},
    { name: 'your_company', type: 'text', label: 'Votre entreprise', required: true },
    { name: 'supplier_name', type: 'text', label: 'Nom du fournisseur' },
    { name: 'product_interest', type: 'text', label: 'Produit(s) concerné(s)' },
    { name: 'order_volume', type: 'text', label: 'Volume de commande estimé' },
    { name: 'specific_request', type: 'textarea', label: 'Demande spécifique' }
  ],
  outputs: [{ type: 'markdown', name: 'email_template' }],
  promptTemplate: `Tu es un acheteur professionnel expérimenté.

TYPE : {{email_type}}
VOTRE ENTREPRISE : {{your_company}}
FOURNISSEUR : {{supplier_name}}
PRODUIT : {{product_interest}}
VOLUME : {{order_volume}}
DEMANDE : {{specific_request}}

## 📧 EMAIL FOURNISSEUR

{{#if email_type.includes('Premier contact')}}
### Premier Contact

**Objet :** Business Inquiry - {{your_company}} - [Product Category]

---

Dear [Name/Sir/Madam],

I am [Your Name], [Position] at {{your_company}}, a [description of your business] based in [Country].

We are currently looking for a reliable supplier for {{product_interest}} and came across your company through [source: Alibaba/Trade show/Referral].

**About us:**
- [Brief company description]
- [Market/Countries served]
- [Current monthly/annual volume]

**Our requirements:**
- Product: {{product_interest}}
- Estimated volume: {{order_volume}}
- Target price range: [if applicable]

Could you please provide:
1. Your product catalog and price list
2. MOQ (Minimum Order Quantity)
3. Lead times
4. Payment terms

We would also be interested in receiving samples if possible.

Looking forward to your reply.

Best regards,

[Your Name]
[Position]
{{your_company}}
[Phone] | [Email] | [Website]
{{/if}}

{{#if email_type.includes('Négociation')}}
### Négociation de Prix

**Objet :** RE: Quote - Request for Better Pricing - {{order_volume}} units

---

Dear [Name],

Thank you for the quotation received on [date].

We have reviewed your pricing for {{product_interest}} and would like to discuss the following:

**Current quote:** $X per unit
**Our target:** $Y per unit

**Why we believe this is achievable:**
1. We are committing to {{order_volume}} units
2. We plan to place regular orders ([frequency])
3. We have received competitive quotes from other suppliers

**Our proposal:**
- Price: $Y per unit for orders of {{order_volume}}+
- Or: $Z per unit with [longer payment terms / annual contract]

We value building a long-term partnership and believe this pricing would allow us to grow our orders significantly.

Could we schedule a call to discuss?

Best regards,
[Signature]
{{/if}}

{{#if email_type.includes('Demande d\'échantillons')}}
### Demande d'Échantillons

**Objet :** Sample Request - {{product_interest}} - {{your_company}}

---

Dear [Name],

Following our recent discussions, we would like to request samples of:

**Products:**
1. [Product 1] - [Specifications]
2. [Product 2] - [Specifications]

**Purpose:** [Quality evaluation / Customer testing / Compliance testing]

**Questions:**
- What is the sample cost?
- Can sample cost be refunded with first order?
- What is the delivery time for samples?

Please provide shipping costs to: [Your address]

Thank you for your assistance.

Best regards,
[Signature]
{{/if}}

---

### Versions FR/AR disponibles

**Version Française :**
[Même structure en français formel]

**Version Arabe (pour fournisseurs MENA) :**
[Version arabe formelle]

---

**Conseils négociation fournisseurs :**
✅ Toujours demander 3+ devis
✅ Négocier après échantillons validés
✅ Mentionner le volume potentiel futur
✅ Demander des conditions de paiement (30/60/90 jours)
✅ Ne jamais accepter le premier prix`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const wholesaleInquiryResponse: AITool = {
  id: 'wholesale-inquiry-response',
  slug: 'wholesale-inquiry-response',
  name: { fr: 'Réponses Demandes B2B', ar: 'ردود الاستفسارات B2B', en: 'Wholesale Inquiry Response' },
  description: {
    fr: 'Répondez professionnellement aux demandes de grossistes et revendeurs',
    ar: 'رد باحترافية على استفسارات تجار الجملة',
    en: 'Respond professionally to wholesaler and reseller inquiries'
  },
  category: 'ecommerce',
  subcategory: 'b2b',
  icon: 'Building2',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'inquiry_type', type: 'select', label: 'Type de demande', options: [
      'Devenir revendeur',
      'Prix de gros',
      'Commande en volume',
      'Marque blanche',
      'Partenariat'
    ]},
    { name: 'your_brand', type: 'text', label: 'Votre marque', required: true },
    { name: 'wholesale_terms', type: 'textarea', label: 'Vos conditions de gros (MOQ, remises...)' },
    { name: 'inquiry_details', type: 'textarea', label: 'Détails de la demande reçue' }
  ],
  outputs: [{ type: 'markdown', name: 'response' }],
  promptTemplate: `Tu es un responsable commercial B2B.

TYPE : {{inquiry_type}}
MARQUE : {{your_brand}}
CONDITIONS : {{wholesale_terms}}
DEMANDE : {{inquiry_details}}

## 📧 RÉPONSE DEMANDE B2B

{{#if inquiry_type.includes('Devenir revendeur')}}
### Réponse Demande Revendeur

**Objet :** RE: Demande de partenariat revendeur - {{your_brand}}

---

Bonjour [Nom],

Merci pour votre intérêt à devenir revendeur {{your_brand}} !

Nous sommes toujours à la recherche de partenaires de qualité pour développer notre réseau de distribution.

**Notre programme revendeur :**

📦 **Conditions :**
- MOQ (Commande minimum) : [X] unités ou [X]€
- Remise revendeur : [X]% à [X]% selon volume

💰 **Grille tarifaire :**
| Volume | Remise |
|--------|--------|
| [X-X] unités | -X% |
| [X-X] unités | -X% |
| [X+] unités | -X% |

📋 **Pour postuler, merci de nous fournir :**
- [ ] Numéro SIRET / Registre du commerce
- [ ] Description de votre activité
- [ ] Canaux de distribution (boutique, web, marketplace...)
- [ ] Volume de commande estimé

🎁 **Avantages revendeurs :**
- Tarifs préférentiels
- Support marketing (visuels, argumentaires)
- Accès aux nouveautés en avant-première
- Gestionnaire de compte dédié

Seriez-vous disponible pour un appel cette semaine afin d'en discuter ?

Cordialement,

[Votre nom]
Responsable Commercial B2B
{{your_brand}}
{{/if}}

{{#if inquiry_type.includes('Marque blanche')}}
### Réponse Demande Marque Blanche

**Objet :** RE: Demande de marque blanche - {{your_brand}}

---

Bonjour [Nom],

Merci pour votre demande concernant nos solutions en marque blanche.

**Notre offre Private Label :**

✅ **Ce que nous proposons :**
- Personnalisation packaging à votre marque
- Formulation/produit identique ou adapté
- Accompagnement réglementaire
- MOQ : [X] unités

💰 **Processus :**
1. Définition de vos besoins
2. Échantillon personnalisé
3. Validation et devis
4. Production
5. Livraison

📋 **Informations nécessaires :**
- Votre marque et positionnement
- Volumes estimés annuels
- Spécificités souhaitées

Pouvons-nous organiser un appel pour en discuter ?

Cordialement,
[Signature]
{{/if}}

---

**Templates réponses rapides :**

✅ **Accusé de réception :**
"Bonjour, merci pour votre demande. Notre équipe commerciale vous répondra sous 48h."

❌ **Refus poli :**
"Merci pour votre intérêt. Malheureusement, nous ne sommes pas en mesure de répondre favorablement à votre demande pour le moment. Nous vous souhaitons bonne continuation."`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const dropshippingProductCopy: AITool = {
  id: 'dropshipping-product-copy',
  slug: 'dropshipping-product-copy',
  name: { fr: 'Copy Produit Dropshipping', ar: 'نص منتج دروبشيبينغ', en: 'Dropshipping Product Copy' },
  description: {
    fr: 'Transformez les descriptions fournisseurs en fiches produit vendeuses',
    ar: 'حول أوصاف الموردين إلى صفحات منتج بيعية',
    en: 'Transform supplier descriptions into selling product pages'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Truck',
  credits: 12,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'supplier_description', type: 'textarea', label: 'Description fournisseur (AliExpress, etc.)', required: true },
    { name: 'product_images_count', type: 'number', label: 'Nombre d\'images disponibles' },
    { name: 'target_price', type: 'number', label: 'Prix de vente visé' },
    { name: 'niche', type: 'text', label: 'Niche/Marché cible' },
    { name: 'brand_name', type: 'text', label: 'Nom de votre boutique' },
    { name: 'unique_angle', type: 'text', label: 'Angle de vente unique' }
  ],
  outputs: [{ type: 'markdown', name: 'product_copy' }],
  promptTemplate: `Tu es un expert en dropshipping et copywriting de conversion.

DESCRIPTION FOURNISSEUR :
"{{supplier_description}}"

PRIX CIBLE : {{target_price}}€
NICHE : {{niche}}
BOUTIQUE : {{brand_name}}
ANGLE : {{unique_angle}}

## 🚀 FICHE PRODUIT DROPSHIPPING OPTIMISÉE

### AVANT (Description fournisseur)
❌ Traduction automatique pauvre
❌ Pas d'émotion
❌ Caractéristiques brutes
❌ Pas de bénéfices

### APRÈS (Votre version)

**Titre produit :**
"[Titre accrocheur avec bénéfice principal]"

**Sous-titre :**
"[Tagline émotionnelle]"

---

**Description courte (100 mots) :**
"[Accroche émotionnelle]

[Problème que résout le produit]

[Solution = votre produit]

[CTA implicite]"

---

**Description complète :**

## [Headline bénéfice]

[Paragraphe storytelling - identification au problème]

### ✨ Pourquoi vous allez l'adorer :

✅ **[Bénéfice 1]** - [Explication courte]
✅ **[Bénéfice 2]** - [Explication courte]
✅ **[Bénéfice 3]** - [Explication courte]
✅ **[Bénéfice 4]** - [Explication courte]
✅ **[Bénéfice 5]** - [Explication courte]

### 📦 Caractéristiques :

| | |
|---|---|
| Matériau | [Matériau amélioré] |
| Dimensions | [Dimensions claires] |
| Poids | [Poids] |
| Couleurs | [Couleurs disponibles] |

### 🎁 Contenu du package :
- 1x [Produit principal]
- [Accessoires si applicable]

### 💡 Conseils d'utilisation :
[Instructions simples]

### ⚠️ Note :
[Disclaimer si nécessaire - délai livraison, etc.]

---

**Bullet points style Amazon :**
- [Bénéfice 1 avec feature]
- [Bénéfice 2]
- [Bénéfice 3]
- [Bénéfice 4]
- [Garantie/SAV]

---

**Éléments de réassurance à ajouter :**
✅ Livraison gratuite
✅ Satisfait ou remboursé 30 jours
✅ Support client 7j/7
✅ Paiement sécurisé

---

**⚠️ Erreurs dropshipping à éviter :**
- Ne pas copier-coller la description AliExpress
- Éviter les fausses urgences ("Plus que 3 en stock")
- Être transparent sur les délais de livraison
- Ne pas mentir sur l'origine du produit`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const marketplaceListingOptimizer: AITool = {
  id: 'marketplace-listing-optimizer',
  slug: 'marketplace-listing-optimizer',
  name: { fr: 'Optimiseur Listing Marketplace', ar: 'محسن قوائم الأسواق', en: 'Marketplace Listing Optimizer' },
  description: {
    fr: 'Optimisez vos listings Amazon, eBay, Etsy pour maximiser les ventes',
    ar: 'حسّن قوائمك على أمازون وإيباي وإتسي لزيادة المبيعات',
    en: 'Optimize your Amazon, eBay, Etsy listings to maximize sales'
  },
  category: 'ecommerce',
  subcategory: 'seo',
  icon: 'Store',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'marketplace', type: 'select', label: 'Marketplace', required: true, options: [
      'Amazon',
      'eBay',
      'Etsy',
      'Cdiscount',
      'Fnac Marketplace'
    ]},
    { name: 'current_listing', type: 'textarea', label: 'Listing actuel (titre + description)' },
    { name: 'product_category', type: 'text', label: 'Catégorie du produit' },
    { name: 'target_keywords', type: 'text', label: 'Mots-clés cibles' },
    { name: 'competitors', type: 'textarea', label: 'Titres des concurrents (top 3)' }
  ],
  outputs: [{ type: 'markdown', name: 'optimized_listing' }],
  promptTemplate: `Tu es un expert en optimisation de listings marketplace.

MARKETPLACE : {{marketplace}}
LISTING ACTUEL : {{current_listing}}
CATÉGORIE : {{product_category}}
MOTS-CLÉS : {{target_keywords}}
CONCURRENTS : {{competitors}}

## 🏪 LISTING OPTIMISÉ {{marketplace | uppercase}}

{{#if marketplace === 'Amazon'}}
### AMAZON - Listing Optimisé

**TITRE (200 caractères max) :**
Format : [Marque] + [Produit] + [Caractéristique 1] + [Caractéristique 2] + [Taille/Quantité] + [Couleur]

"[Titre optimisé avec mots-clés]"

✅ Caractères : X/200
✅ Mots-clés intégrés : [liste]

---

**BULLET POINTS (5 x 500 caractères) :**

- **[MOT-CLÉ EN MAJUSCULE]** - [Bénéfice principal]. [Détails]. [Preuve/specs].

- **[MOT-CLÉ 2]** - [Bénéfice]. [Détails].

- **[MOT-CLÉ 3]** - [Bénéfice]. [Détails].

- **[MOT-CLÉ 4]** - [Bénéfice]. [Détails].

- **SATISFACTION GARANTIE** - [Politique SAV]. [Réassurance].

---

**DESCRIPTION (2000 caractères) :**

[Description avec mise en forme HTML Amazon]

<h3>[Titre section]</h3>
<p>[Paragraphe avec mots-clés]</p>

<ul>
<li>[Point 1]</li>
<li>[Point 2]</li>
</ul>

---

**BACKEND KEYWORDS (250 caractères) :**
"[mot-clé1] [mot-clé2] [mot-clé3] [synonyme1] [synonyme2]..."

⚠️ Règles :
- Pas de virgules, juste des espaces
- Pas de répétition du titre
- Pas de marques concurrentes
{{/if}}

{{#if marketplace === 'Etsy'}}
### ETSY - Listing Optimisé

**TITRE (140 caractères) :**
"[Titre avec mots-clés longue traîne, occasion, style]"

Exemple : "[Produit] [Adjectif] [Style] | [Occasion] | [Pour qui] | [Matériau]"

---

**TAGS (13 tags max) :**
1. [Tag principal]
2. [Tag longue traîne]
3-13. [Tags variés]

---

**DESCRIPTION :**

[Première ligne = accroche avec mot-clé]

✨ **À propos de ce [produit] :**
[Description avec storytelling artisanal]

📦 **Ce que vous recevez :**
- [Item 1]
- [Item 2]

📏 **Dimensions :**
[Détails]

🎨 **Personnalisation :**
[Options si applicable]

🚚 **Livraison :**
[Délais et méthode]

💬 **Une question ?**
N'hésitez pas à me contacter !

---

**SECTIONS À REMPLIR :**
- [ ] Materials
- [ ] Occasion
- [ ] Style
- [ ] When it's made
{{/if}}

{{#if marketplace === 'eBay'}}
### EBAY - Listing Optimisé

**TITRE (80 caractères) :**
"[Mot-clé principal] [Marque] [Attributs] [État] [Livraison]"

**ITEM SPECIFICS :**
[Remplir TOUS les champs proposés par eBay]

**DESCRIPTION HTML :**
[Template HTML responsive]
{{/if}}

---

**Score d'optimisation estimé : X/100**

| Critère | Score | Action |
|---------|-------|--------|
| Mots-clés titre | X/25 | [Action] |
| Bullet points | X/25 | [Action] |
| Backend SEO | X/25 | [Action] |
| Images | X/25 | [Action] |`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const printOnDemandDescription: AITool = {
  id: 'print-on-demand-description',
  slug: 'print-on-demand-description',
  name: { fr: 'Description Print-on-Demand', ar: 'وصف الطباعة عند الطلب', en: 'Print-on-Demand Description' },
  description: {
    fr: 'Créez des descriptions vendeuses pour vos produits POD (t-shirts, mugs...)',
    ar: 'أنشئ أوصاف بيعية لمنتجات POD',
    en: 'Create selling descriptions for POD products (t-shirts, mugs...)'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Shirt',
  credits: 10,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_type', type: 'select', label: 'Type de produit', required: true, options: [
      'T-shirt',
      'Sweat/Hoodie',
      'Mug',
      'Poster/Affiche',
      'Coque de téléphone',
      'Tote bag',
      'Sticker',
      'Coussin'
    ]},
    { name: 'design_description', type: 'textarea', label: 'Description du design', required: true },
    { name: 'design_theme', type: 'text', label: 'Thème/Niche', placeholder: 'Humour, Gaming, Motivation...' },
    { name: 'target_audience', type: 'text', label: 'Audience cible' },
    { name: 'platform', type: 'select', label: 'Plateforme POD', options: ['Redbubble', 'Teepublic', 'Spreadshirt', 'Printful', 'Merch by Amazon', 'Etsy'] }
  ],
  outputs: [{ type: 'markdown', name: 'pod_description' }],
  promptTemplate: `Tu es un expert en Print-on-Demand et marketing de niche.

PRODUIT : {{product_type}}
DESIGN : {{design_description}}
THÈME : {{design_theme}}
AUDIENCE : {{target_audience}}
PLATEFORME : {{platform}}

## 👕 FICHE PRODUIT POD

### TITRE (optimisé SEO)

{{#if product_type === 'T-shirt'}}
**Format Merch by Amazon :**
"[Design Theme] [Descripteur] T-Shirt | [Occasion/Pour qui] | [Style] Tee"

**Format Etsy :**
"[Design] Shirt, [Theme] T-shirt, [Occasion] Gift, [Audience] Tee, [Style] Top"

**Format Redbubble :**
"[Design Description] - [Theme] [Audience]"
{{/if}}

{{#if product_type === 'Mug'}}
"[Design] Mug, [Theme] Coffee Cup, [Occasion] Gift for [Audience], [Adjectif] Tea Mug"
{{/if}}

---

### DESCRIPTION

**Version courte (150 mots) :**

"🎨 **[Accroche liée au design]**

Le cadeau parfait pour [audience cible] !

Ce {{product_type}} [description du design] est idéal pour :
✨ [Occasion 1]
✨ [Occasion 2]
✨ [Occasion 3]

**Qualité premium :**
{{#if product_type === 'T-shirt'}}
- 100% coton peigné (ou mélange selon modèle)
- Impression DTG haute qualité
- Coupe unisexe confortable
- Lavable en machine
{{/if}}
{{#if product_type === 'Mug'}}
- Céramique de haute qualité
- Impression sublimation (ne s'efface pas)
- Compatible lave-vaisselle et micro-ondes
- Contenance : 11oz / 15oz
{{/if}}

🎁 **Idée cadeau parfaite** pour [occasions : anniversaire, Noël, etc.]

[CTA]"

---

### TAGS/MOTS-CLÉS (15)

{{#if platform === 'Redbubble' || platform === 'Teepublic'}}
1. [Tag principal - thème]
2. [Tag design]
3. [Tag audience]
4. [Tag occasion]
5. [Tag style]
6-15. [Tags variés et synonymes]
{{/if}}

{{#if platform === 'Merch by Amazon'}}
**Bullet Points (2) :**
- [Bénéfice 1 avec mots-clés]
- [Bénéfice 2 avec mots-clés]
{{/if}}

---

### DÉCLINAISONS SUGGÉRÉES

**Couleurs populaires pour ce design :**
- {{#if product_type === 'tshirt'}}Noir, Blanc, Gris chiné, Navy{{else}}Blanc, Noir{{/if}}

**Produits complémentaires :**
- [Suggestion 1]
- [Suggestion 2]

---

### CONSEILS POD

✅ **Meilleures pratiques :**
- Uploader sur plusieurs plateformes
- Tester différentes niches
- Analyser les tendances saisonnières
- Utiliser des mockups de qualité

📊 **Niches rentables 2025 :**
- [Niche 1 liée au thème]
- [Niche 2]
- [Niche 3]

**Pricing suggéré :**
- T-shirt : [X-X€]
- Mug : [X-X€]
- Poster : [X-X€]`,
  model: 'gpt4',
  estimatedTime: '30s'
};
