import { AITool } from '../../types';

export const productDescriptionGenerator: AITool = {
  id: 'product-description-generator',
  slug: 'product-description-generator',
  name: { fr: 'Générateur de Fiches Produit', ar: 'مولد وصف المنتجات', en: 'Product Description Generator' },
  description: {
    fr: 'Créez des descriptions produit qui convertissent les visiteurs en acheteurs',
    ar: 'أنشئ أوصاف منتجات تحول الزوار إلى مشترين',
    en: 'Create product descriptions that convert visitors into buyers'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Package',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
    { name: 'product_category', type: 'text', label: 'Catégorie', required: true },
    { name: 'key_features', type: 'textarea', label: 'Caractéristiques principales', required: true },
    { name: 'target_customer', type: 'text', label: 'Client cible' },
    { name: 'price_range', type: 'select', label: 'Gamme de prix', options: ['Budget', 'Mid-range', 'Premium', 'Luxury'] },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Fun', 'Luxe', 'Technique', 'Emotionnel'] },
    { name: 'platform', type: 'select', label: 'Plateforme', options: ['Shopify', 'WooCommerce', 'Amazon', 'Etsy', 'Generic'] }
  ],
  outputs: [{ type: 'markdown', name: 'description' }],
  promptTemplate: `Tu es un expert e-commerce avec des taux de conversion de 5%+.

PRODUIT : {{product_name}}
CATÉGORIE : {{product_category}}
CARACTÉRISTIQUES : {{key_features}}
CLIENT : {{target_customer}}
GAMME : {{price_range}}
TON : {{tone}}

## 📦 FICHE PRODUIT COMPLÈTE

### TITRE PRODUIT (3 versions)
1. "[Titre SEO avec mot-clé principal]"
2. "[Titre bénéfice-oriented]"
3. "[Titre émotionnel]"

---

### DESCRIPTION COURTE (150 caractères)
"[Accroche percutante pour les listings]"

---

### DESCRIPTION COMPLÈTE

**[Accroche émotionnelle - 1 ligne qui capture l'attention]**

[Paragraphe 1 : Le problème que résout le produit]

[Paragraphe 2 : La solution - votre produit]

**✨ Pourquoi vous allez l'adorer :**

✅ [Bénéfice 1 - pas feature]
✅ [Bénéfice 2]
✅ [Bénéfice 3]
✅ [Bénéfice 4]
✅ [Bénéfice 5]

**📋 Caractéristiques :**

| Caractéristique | Détail |
|-----------------|--------|
| [Feature 1] | [Spec] |
| [Feature 2] | [Spec] |
| ... | ... |

**🎁 Ce que vous recevez :**
- [Contenu du package]

**⚠️ Note :** [Information importante si applicable]

---

### BULLET POINTS AMAZON (5)
- [Bullet 1 : Bénéfice principal + feature]
- [Bullet 2]
- [Bullet 3]
- [Bullet 4]
- [Bullet 5 : Garantie/SAV]

---

### MOTS-CLÉS SEO
Primary : [mot-clé principal]
Secondary : [mot-clé 2], [mot-clé 3]
Long-tail : [phrase clé 1], [phrase clé 2]

---

**Formule utilisée : AIDA + PAS**
- Attention → Accroche
- Intérêt → Problème/Solution
- Désir → Bénéfices
- Action → CTA implicite`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const productTitleOptimizer: AITool = {
  id: 'product-title-optimizer',
  slug: 'product-title-optimizer',
  name: { fr: 'Optimiseur de Titres Produit', ar: 'محسن عناوين المنتجات', en: 'Product Title Optimizer' },
  description: {
    fr: 'Optimisez vos titres produit pour le SEO et les conversions',
    ar: 'حسّن عناوين منتجاتك للسيو والتحويلات',
    en: 'Optimize product titles for SEO and conversions'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Type',
  credits: 8,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'current_title', type: 'text', label: 'Titre actuel', required: true },
    { name: 'product_type', type: 'text', label: 'Type de produit' },
    { name: 'brand', type: 'text', label: 'Marque' },
    { name: 'key_attributes', type: 'text', label: 'Attributs clés (taille, couleur, matière...)' },
    { name: 'platform', type: 'select', label: 'Plateforme', options: ['Amazon', 'Shopify', 'eBay', 'Etsy', 'Google Shopping'] }
  ],
  outputs: [{ type: 'markdown', name: 'titles' }],
  promptTemplate: `Tu es un expert SEO e-commerce.

TITRE ACTUEL : {{current_title}}
PRODUIT : {{product_type}}
MARQUE : {{brand}}
ATTRIBUTS : {{key_attributes}}
PLATEFORME : {{platform}}

## 🏷️ 10 TITRES OPTIMISÉS

{{#if platform === 'Amazon'}}
**Format Amazon (200 caractères max) :**
[Marque] + [Produit] + [Caractéristique principale] + [Taille/Quantité] + [Couleur]

1. "{{brand}} - [Produit] [Attribut clé] pour [Usage] - [Taille] [Couleur]"
2. ...
{{/if}}

{{#if platform === 'Google Shopping'}}
**Format Google Shopping (150 caractères) :**
[Produit] + [Marque] + [Attributs] + [Couleur] + [Taille]

1. "[Produit] {{brand}} [Attribut] - [Couleur], [Taille]"
2. ...
{{/if}}

{{#if platform === 'Etsy'}}
**Format Etsy (140 caractères) :**
[Mot-clé principal] + [Descripteur] + [Usage/Occasion]

1. "[Produit] [Adjectif], [Usage], [Occasion], [Style]"
2. ...
{{/if}}

---

**Analyse SEO :**

| Titre | Caractères | Mots-clés | Score |
|-------|------------|-----------|-------|
| 1 | X/200 | ✅ | ⭐⭐⭐⭐⭐ |
| 2 | X/200 | ✅ | ⭐⭐⭐⭐ |

**Mots-clés à inclure :**
- [Mot-clé 1] - Volume : X
- [Mot-clé 2] - Volume : X

**À éviter :**
❌ Majuscules abusives
❌ Caractères spéciaux (★, ♥)
❌ Mots promotionnels (PROMO, SOLDES)
❌ Répétition de mots-clés`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const ecommerceAdCopyGenerator: AITool = {
  id: 'ecommerce-ad-copy-generator',
  slug: 'ecommerce-ad-copy-generator',
  name: { fr: 'Générateur de Pubs E-commerce', ar: 'مولد إعلانات التجارة', en: 'E-commerce Ad Copy Generator' },
  description: {
    fr: 'Créez des publicités Facebook/Google Ads qui convertissent',
    ar: 'أنشئ إعلانات فيسبوك/جوجل تحول الزوار',
    en: 'Create Facebook/Google Ads that convert'
  },
  category: 'ecommerce',
  subcategory: 'advertising',
  icon: 'Megaphone',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_name', type: 'text', label: 'Produit', required: true },
    { name: 'unique_selling_point', type: 'text', label: 'Argument clé de vente' },
    { name: 'target_audience', type: 'textarea', label: 'Audience cible' },
    { name: 'offer', type: 'text', label: 'Offre/Promotion', placeholder: '-20%, Livraison gratuite...' },
    { name: 'platform', type: 'select', label: 'Plateforme', options: ['Facebook', 'Instagram', 'Google Search', 'Google Shopping', 'TikTok'] },
    { name: 'ad_objective', type: 'select', label: 'Objectif', options: ['Conversions', 'Traffic', 'Awareness', 'Retargeting'] }
  ],
  outputs: [{ type: 'markdown', name: 'ads' }],
  promptTemplate: `Tu es un expert en publicité e-commerce avec des ROAS de 4x+.

PRODUIT : {{product_name}}
USP : {{unique_selling_point}}
AUDIENCE : {{target_audience}}
OFFRE : {{offer}}
PLATEFORME : {{platform}}
OBJECTIF : {{ad_objective}}

## 📣 COPIES PUBLICITAIRES

{{#if platform.includes('Facebook') || platform.includes('Instagram')}}
### FACEBOOK/INSTAGRAM ADS

**Ad 1 : Pain Point**

🎯 **Primary Text :**
"[Question sur le problème]

[Présentation solution]

{{offer}}

👉 [CTA]"

**Headline :** [6-8 mots max]
**Description :** [1 ligne]
**CTA Button :** Shop Now

---

**Ad 2 : Social Proof**

⭐ **Primary Text :**
"Plus de [X] clients satisfaits !

"[Témoignage court]" - [Prénom]

[Offre]

🛒 [CTA]"

---

**Ad 3 : FOMO/Urgence**

🔥 **Primary Text :**
"⚠️ Stock limité !

[Bénéfice produit]

{{offer}} - Plus que [X] disponibles

⏰ [CTA urgent]"

---

**Ad 4 : UGC Style**

📱 **Primary Text :**
"POV : Tu découvres enfin [solution à leur problème] 😍

[Description bénéfice]

Le lien est dans notre bio 👆"
{{/if}}

{{#if platform === 'Google Search'}}
### GOOGLE SEARCH ADS

**Ad 1 :**
- Headline 1 (30 car.) : "[Mot-clé] - {{offer}}"
- Headline 2 (30 car.) : "[Bénéfice principal]"
- Headline 3 (30 car.) : "[CTA + Urgence]"
- Description 1 (90 car.) : "[Description avec mots-clés]"
- Description 2 (90 car.) : "[Social proof + CTA]"

**Ad 2 :**
[Variante]

**Extensions suggérées :**
- Sitelinks : [4 suggestions]
- Callouts : [4 suggestions]
- Structured snippets : [suggestions]
{{/if}}

---

**A/B Tests recommandés :**
1. Hook émotionnel vs rationnel
2. Avec vs sans émojis
3. Prix affiché vs "Voir l'offre"
4. Témoignage vs statistique`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const collectionDescriptionGenerator: AITool = {
  id: 'collection-description-generator',
  slug: 'collection-description-generator',
  name: { fr: 'Description de Collection', ar: 'وصف المجموعة', en: 'Collection Description' },
  description: {
    fr: 'Rédigez des descriptions de collections/catégories optimisées SEO',
    ar: 'اكتب أوصاف مجموعات محسنة للسيو',
    en: 'Write SEO-optimized collection/category descriptions'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Layers',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'collection_name', type: 'text', label: 'Nom de la collection', required: true },
    { name: 'products_included', type: 'textarea', label: 'Types de produits inclus' },
    { name: 'target_keywords', type: 'text', label: 'Mots-clés SEO cibles' },
    { name: 'brand_voice', type: 'select', options: ['Professionnel', 'Casual', 'Luxe', 'Eco', 'Tech'] },
    { name: 'word_count', type: 'select', label: 'Longueur', options: ['Short (100)', 'Medium (250)', 'Long (500)'] }
  ],
  outputs: [{ type: 'markdown', name: 'description' }],
  promptTemplate: `Tu es un expert SEO e-commerce.

COLLECTION : {{collection_name}}
PRODUITS : {{products_included}}
MOTS-CLÉS : {{target_keywords}}
TON : {{brand_voice}}
LONGUEUR : {{word_count}}

## 📁 DESCRIPTION DE COLLECTION

### Version SEO Complète

**H1 :** {{collection_name}}

[Paragraphe d'introduction avec mot-clé principal dans les 100 premiers mots]

**Découvrez notre sélection de [catégorie] :**

[Paragraphe décrivant la variété de produits]

**Pourquoi choisir notre collection [nom] ?**

✅ [Avantage 1]
✅ [Avantage 2]
✅ [Avantage 3]

[Paragraphe avec mots-clés secondaires]

**[CTA vers les produits]**

---

### Version Courte (listings)

"[Description 100-150 caractères pour les métadonnées]"

---

### Meta Description (155 car.)

"[Meta description optimisée avec mot-clé et CTA]"

---

**Densité mots-clés :**
- {{keyword1}} : X occurrences
- {{keyword2}} : X occurrences

**Structure Hn suggérée :**
- H1 : [Titre collection]
- H2 : [Sous-section 1]
- H2 : [Sous-section 2]`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const customerReviewResponse: AITool = {
  id: 'customer-review-response',
  slug: 'customer-review-response',
  name: { fr: 'Réponses aux Avis Clients', ar: 'الرد على تقييمات العملاء', en: 'Customer Review Response' },
  description: {
    fr: 'Rédigez des réponses professionnelles aux avis positifs et négatifs',
    ar: 'اكتب ردودًا احترافية على التقييمات الإيجابية والسلبية',
    en: 'Write professional responses to positive and negative reviews'
  },
  category: 'ecommerce',
  subcategory: 'customer_service',
  icon: 'Star',
  credits: 8,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'review_text', type: 'textarea', label: 'Texte de l\'avis', required: true },
    { name: 'rating', type: 'select', label: 'Note', options: ['5 stars', '4 stars', '3 stars', '2 stars', '1 star'] },
    { name: 'review_type', type: 'select', label: 'Type de problème (si négatif)', options: [
      'Quality', 'Shipping', 'Customer Service', 'Not as described', 'Damaged', 'Other', 'None'
    ]},
    { name: 'brand_name', type: 'text', label: 'Nom de la marque' },
    { name: 'tone', type: 'select', options: ['Professionnel', 'Chaleureux', 'Apologetic'] }
  ],
  outputs: [{ type: 'markdown', name: 'response' }],
  promptTemplate: `Tu es un expert en service client e-commerce.

AVIS : "{{review_text}}"
NOTE : {{rating}}
PROBLÈME : {{review_type}}
MARQUE : {{brand_name}}

## ⭐ RÉPONSE À L'AVIS

{{#if rating.includes('5') || rating.includes('4')}}
### Réponse Avis Positif

"Bonjour [Prénom si visible],

Merci infiniment pour votre retour et cette belle note ! 🙏

[Réponse personnalisée à un point spécifique mentionné]

Nous sommes ravis que [produit/service] vous ait plu.

N'hésitez pas à nous contacter si vous avez besoin de quoi que ce soit.

À très bientôt !

L'équipe {{brand_name}}"
{{/if}}

{{#if rating.includes('3')}}
### Réponse Avis Mitigé

"Bonjour [Prénom],

Merci d'avoir pris le temps de partager votre expérience.

Nous sommes contents que [aspect positif], mais désolés que [aspect négatif].

[Explication ou solution proposée]

Nous aimerions en discuter avec vous - contactez-nous à [email] pour qu'on puisse améliorer votre expérience.

Cordialement,
{{brand_name}}"
{{/if}}

{{#if rating.includes('2') || rating.includes('1')}}
### Réponse Avis Négatif

"Bonjour [Prénom],

Nous sommes sincèrement désolés d'apprendre votre déception. Ce n'est pas l'expérience que nous souhaitons offrir.

{{#if review_type.includes('Shipping')}}
[Réponse spécifique problème livraison]
{{/if}}
{{#if review_type.includes('Quality')}}
[Réponse spécifique problème qualité]
{{/if}}

Nous aimerions vraiment nous rattraper. Pourriezvous nous contacter à [email] avec votre numéro de commande ? Nous trouverons une solution ensemble.

Avec toutes nos excuses,
L'équipe {{brand_name}}"
{{/if}}

---

**Règles d'or :**
✅ Répondre en < 24-48h
✅ Toujours remercier
✅ Personnaliser la réponse
✅ Ne jamais être défensif
✅ Proposer une solution (pas d'excuses vides)
✅ Déplacer en privé si sensible`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const ecommerceFaqGenerator: AITool = {
  id: 'ecommerce-faq-generator',
  slug: 'ecommerce-faq-generator',
  name: { fr: 'Générateur de FAQ E-commerce', ar: 'مولد الأسئلة الشائعة', en: 'E-commerce FAQ Generator' },
  description: {
    fr: 'Créez une FAQ complète pour réduire les questions au support',
    ar: 'أنشئ أسئلة شائعة شاملة لتقليل أسئلة الدعم',
    en: 'Create comprehensive FAQ to reduce support inquiries'
  },
  category: 'ecommerce',
  subcategory: 'customer_service',
  icon: 'HelpCircle',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_type', type: 'select', label: 'Type de business', options: ['Physical Products', 'Digital Products', 'Services', 'Subscription'] },
    { name: 'product_category', type: 'text', label: 'Catégorie de produits' },
    { name: 'shipping_info', type: 'textarea', label: 'Infos livraison (délais, zones...)' },
    { name: 'return_policy', type: 'textarea', label: 'Politique de retour' },
    { name: 'payment_methods', type: 'text', label: 'Moyens de paiement' },
    { name: 'common_questions', type: 'textarea', label: 'Questions fréquentes reçues' }
  ],
  outputs: [{ type: 'markdown', name: 'faq' }],
  promptTemplate: `Tu es un expert en expérience client e-commerce.

BUSINESS : {{business_type}}
CATÉGORIE : {{product_category}}
LIVRAISON : {{shipping_info}}
RETOURS : {{return_policy}}
PAIEMENTS : {{payment_methods}}

## ❓ FAQ E-COMMERCE COMPLÈTE

### 📦 COMMANDES & LIVRAISON

**Q : Quels sont les délais de livraison ?**
R : [Réponse basée sur {{shipping_info}}]

**Q : Comment suivre ma commande ?**
R : [Processus de suivi]

**Q : Livrez-vous à l'international ?**
R : [Zones de livraison]

**Q : Quels sont les frais de livraison ?**
R : [Grille tarifaire]

**Q : Ma commande n'est pas arrivée, que faire ?**
R : [Procédure]

---

### 💳 PAIEMENT

**Q : Quels moyens de paiement acceptez-vous ?**
R : Nous acceptons : {{payment_methods}}

**Q : Le paiement est-il sécurisé ?**
R : [Réassurance sécurité]

**Q : Puis-je payer en plusieurs fois ?**
R : [Politique de paiement fractionné]

---

### 🔄 RETOURS & REMBOURSEMENTS

**Q : Quelle est votre politique de retour ?**
R : [Basé sur {{return_policy}}]

**Q : Comment retourner un article ?**
R : [Procédure étape par étape]

**Q : Sous quel délai serai-je remboursé ?**
R : [Délais de remboursement]

**Q : Les frais de retour sont-ils à ma charge ?**
R : [Politique frais de retour]

---

### 📞 CONTACT & SUPPORT

**Q : Comment vous contacter ?**
R : [Canaux de contact]

**Q : Quels sont vos horaires de service client ?**
R : [Horaires]

---

### 🛍️ PRODUITS

**Q : [Question spécifique produit 1] ?**
R : [Réponse]

**Q : [Question spécifique produit 2] ?**
R : [Réponse]

---

**Schema FAQ (JSON-LD) :**
\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}
\`\`\``,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const shippingPolicyGenerator: AITool = {
  id: 'shipping-policy-generator',
  slug: 'shipping-policy-generator',
  name: { fr: 'Générateur Politique de Livraison', ar: 'مولد سياسة الشحن', en: 'Shipping Policy Generator' },
  description: {
    fr: 'Créez une politique de livraison claire et professionnelle',
    ar: 'أنشئ سياسة شحن واضحة واحترافية',
    en: 'Create a clear and professional shipping policy'
  },
  category: 'ecommerce',
  subcategory: 'legal',
  icon: 'Truck',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'shipping_zones', type: 'textarea', label: 'Zones de livraison' },
    { name: 'carriers', type: 'text', label: 'Transporteurs utilisés' },
    { name: 'processing_time', type: 'text', label: 'Délai de traitement' },
    { name: 'shipping_options', type: 'textarea', label: 'Options de livraison (standard, express...)' },
    { name: 'free_shipping_threshold', type: 'text', label: 'Seuil livraison gratuite' }
  ],
  outputs: [{ type: 'markdown', name: 'policy' }],
  promptTemplate: `Génère une politique de livraison complète et professionnelle.

ENTREPRISE : {{business_name}}
ZONES : {{shipping_zones}}
TRANSPORTEURS : {{carriers}}
TRAITEMENT : {{processing_time}}
OPTIONS : {{shipping_options}}
GRATUIT À PARTIR DE : {{free_shipping_threshold}}

## 🚚 POLITIQUE DE LIVRAISON

### 1. ZONES DE LIVRAISON

{{business_name}} livre actuellement dans les pays/régions suivants :
{{shipping_zones}}

### 2. DÉLAIS DE LIVRAISON

| Zone | Délai standard | Délai express |
|------|---------------|---------------|
| France | X-X jours | X-X jours |
| Belgique | X-X jours | X-X jours |
| ... | ... | ... |

**Note :** Ces délais sont donnés à titre indicatif et ne tiennent pas compte des weekends et jours fériés.

### 3. FRAIS DE LIVRAISON

| Destination | Standard | Express |
|-------------|----------|---------|
| France | X€ | X€ |
| ... | ... | ... |

{{#if free_shipping_threshold}}
**🎁 Livraison gratuite** à partir de {{free_shipping_threshold}} d'achat (France métropolitaine).
{{/if}}

### 4. TRAITEMENT DES COMMANDES

- Les commandes sont préparées sous {{processing_time}}
- Les commandes passées après [heure] sont traitées le jour ouvré suivant
- Un email de confirmation avec numéro de suivi vous sera envoyé

### 5. SUIVI DE COMMANDE

[Instructions pour suivre sa commande]

### 6. PROBLÈMES DE LIVRAISON

[Procédure en cas de colis perdu/endommagé]

### 7. CONTACT

Pour toute question : [email/téléphone]

---
*Dernière mise à jour : [Date]*`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const returnPolicyGenerator: AITool = {
  id: 'return-policy-generator',
  slug: 'return-policy-generator',
  name: { fr: 'Générateur Politique de Retour', ar: 'مولد سياسة الإرجاع', en: 'Return Policy Generator' },
  description: {
    fr: 'Créez une politique de retour qui rassure les clients',
    ar: 'أنشئ سياسة إرجاع تطمئن العملاء',
    en: 'Create a return policy that reassures customers'
  },
  category: 'ecommerce',
  subcategory: 'legal',
  icon: 'RotateCcw',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'return_window', type: 'select', label: 'Délai de retour', options: ['14 jours', '30 jours', '60 jours', '90 jours'] },
    { name: 'condition_required', type: 'select', label: 'État requis', options: ['Non utilisé avec étiquettes', 'Non utilisé', 'Tout état'] },
    { name: 'refund_method', type: 'select', label: 'Mode de remboursement', options: ['Original payment', 'Store credit', 'Both'] },
    { name: 'return_shipping', type: 'select', label: 'Frais de retour', options: ['Gratuit', 'Client paye', 'Dépend'] },
    { name: 'exceptions', type: 'textarea', label: 'Produits exclus des retours' }
  ],
  outputs: [{ type: 'markdown', name: 'policy' }],
  promptTemplate: `Génère une politique de retour claire et rassurante.

ENTREPRISE : {{business_name}}
DÉLAI : {{return_window}}
ÉTAT REQUIS : {{condition_required}}
REMBOURSEMENT : {{refund_method}}
FRAIS RETOUR : {{return_shipping}}
EXCEPTIONS : {{exceptions}}

## 🔄 POLITIQUE DE RETOUR & REMBOURSEMENT

### NOTRE ENGAGEMENT

Chez {{business_name}}, votre satisfaction est notre priorité. Si vous n'êtes pas entièrement satisfait de votre achat, nous sommes là pour vous aider.

### 1. DÉLAI DE RETOUR

Vous disposez de **{{return_window}}** à compter de la réception de votre commande pour nous retourner un article.

### 2. CONDITIONS DE RETOUR

Pour être éligible au retour, l'article doit être :
{{#if condition_required.includes('étiquettes')}}
- Non porté / non utilisé
- Dans son emballage d'origine
- Avec toutes les étiquettes attachées
{{/if}}

### 3. COMMENT RETOURNER UN ARTICLE ?

**Étape 1 :** Connectez-vous à votre compte ou contactez-nous à [email]
**Étape 2 :** Demandez un numéro de retour (RMA)
**Étape 3 :** Emballez soigneusement l'article
**Étape 4 :** Expédiez à : [Adresse de retour]

### 4. FRAIS DE RETOUR

{{#if return_shipping === 'Gratuit'}}
Les frais de retour sont **gratuits**. Une étiquette prépayée vous sera envoyée.
{{/if}}
{{#if return_shipping === 'Client paye'}}
Les frais de retour sont à la charge du client, sauf en cas d'erreur de notre part.
{{/if}}

### 5. REMBOURSEMENT

Une fois le retour reçu et inspecté :
- Délai de traitement : 5-7 jours ouvrés
- Mode de remboursement : {{refund_method}}

### 6. ÉCHANGES

[Politique d'échange]

### 7. ARTICLES NON RETOURNABLES

{{exceptions}}

### 8. ARTICLES DÉFECTUEUX

[Procédure spécifique]

---
*Conformément au Code de la consommation (droit de rétractation)*`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const upsellCrossSellGenerator: AITool = {
  id: 'upsell-cross-sell-generator',
  slug: 'upsell-cross-sell-generator',
  name: { fr: 'Générateur Upsell/Cross-sell', ar: 'مولد البيع المتقاطع', en: 'Upsell/Cross-sell Generator' },
  description: {
    fr: 'Créez des suggestions de produits qui augmentent le panier moyen',
    ar: 'أنشئ اقتراحات منتجات تزيد متوسط السلة',
    en: 'Create product suggestions that increase average order value'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'TrendingUp',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'main_product', type: 'text', label: 'Produit principal', required: true },
    { name: 'product_price', type: 'number', label: 'Prix du produit' },
    { name: 'product_category', type: 'text', label: 'Catégorie' },
    { name: 'available_products', type: 'textarea', label: 'Autres produits disponibles' },
    { name: 'strategy', type: 'select', label: 'Stratégie', options: ['Upsell', 'Cross-sell', 'Bundle', 'All'] }
  ],
  outputs: [{ type: 'markdown', name: 'suggestions' }],
  promptTemplate: `Tu es un expert en optimisation de panier e-commerce.

PRODUIT : {{main_product}}
PRIX : {{product_price}}
CATÉGORIE : {{product_category}}
CATALOGUE : {{available_products}}

## 💰 STRATÉGIES UPSELL/CROSS-SELL

### UPSELL (Version supérieure)

**Produit recommandé :** [Version premium]
**Prix :** [+X% vs produit actuel]

**Copy :**
"🌟 **Version Premium disponible !**
Pour seulement [X€] de plus, obtenez :
✅ [Avantage 1]
✅ [Avantage 2]
✅ [Avantage 3]

[BOUTON : Upgrader]"

---

### CROSS-SELL (Produits complémentaires)

**Produits suggérés :**
1. [Produit A] - [Prix] - Raison : [Pourquoi pertinent]
2. [Produit B] - [Prix] - Raison : [Pourquoi pertinent]
3. [Produit C] - [Prix] - Raison : [Pourquoi pertinent]

**Copy page produit :**
"👥 **Les clients ont aussi acheté :**"

**Copy panier :**
"🎯 **Complétez votre commande :**
[Produit] - Seulement [X€] de plus !"

---

### BUNDLE (Pack)

**Pack suggéré :** {{main_product}} + [Produit B] + [Produit C]
**Prix bundle :** [X€] au lieu de [Y€] (-Z%)

**Copy :**
"📦 **PACK COMPLET** - Économisez [X]% !
Tout ce qu'il vous faut pour [objectif] :
- {{main_product}}
- [Produit B]
- [Produit C]

[Prix barré] → **[Prix bundle]**

[BOUTON : Ajouter le pack]"

---

### EMPLACEMENTS RECOMMANDÉS

| Stratégie | Emplacement | Moment |
|-----------|-------------|--------|
| Upsell | Page produit | Avant ajout panier |
| Cross-sell | Page produit | Sous description |
| Cross-sell | Panier | Avant checkout |
| Bundle | Page produit | Section dédiée |
| Upsell | Checkout | Dernière chance |`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const seoProductOptimizer: AITool = {
  id: 'seo-product-optimizer',
  slug: 'seo-product-optimizer',
  name: { fr: 'Optimiseur SEO Produit', ar: 'محسن سيو المنتج', en: 'Product SEO Optimizer' },
  description: {
    fr: 'Optimisez vos pages produit pour le référencement naturel',
    ar: 'حسّن صفحات منتجاتك لمحركات البحث',
    en: 'Optimize your product pages for organic search'
  },
  category: 'ecommerce',
  subcategory: 'seo',
  icon: 'Search',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
    { name: 'current_title', type: 'text', label: 'Titre actuel' },
    { name: 'current_description', type: 'textarea', label: 'Description actuelle' },
    { name: 'target_keywords', type: 'text', label: 'Mots-clés cibles' },
    { name: 'competitors', type: 'textarea', label: 'URLs concurrentes (optionnel)' }
  ],
  outputs: [{ type: 'markdown', name: 'optimization' }],
  promptTemplate: `Tu es un expert SEO e-commerce.

PRODUIT : {{product_name}}
TITRE ACTUEL : {{current_title}}
DESCRIPTION : {{current_description}}
MOTS-CLÉS : {{target_keywords}}

## 🔍 AUDIT SEO PRODUIT

### SCORE ACTUEL : X/100

| Élément | Score | Statut |
|---------|-------|--------|
| Title tag | X/15 | ✅/⚠️/❌ |
| Meta description | X/15 | ✅/⚠️/❌ |
| H1 | X/10 | ✅/⚠️/❌ |
| Contenu | X/20 | ✅/⚠️/❌ |
| Images | X/15 | ✅/⚠️/❌ |
| URL | X/10 | ✅/⚠️/❌ |
| Schema | X/15 | ✅/⚠️/❌ |

---

### OPTIMISATIONS RECOMMANDÉES

**1. Title Tag (50-60 caractères)**
Actuel : "{{current_title}}"
Optimisé : "[Titre optimisé avec mot-clé]"

**2. Meta Description (150-160 caractères)**
"[Description optimisée avec mot-clé + CTA]"

**3. URL Slug**
Recommandé : /[url-optimisee]

**4. Structure Hn**
- H1 : [Titre produit avec mot-clé]
- H2 : Description
- H2 : Caractéristiques
- H2 : Avis clients

**5. Balises Alt Images**
- Image 1 : "[Alt text optimisé]"
- Image 2 : "[Alt text optimisé]"

**6. Schema Product (JSON-LD)**
\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{product_name}}",
  ...
}
\`\`\`

---

### MOTS-CLÉS RECOMMANDÉS

| Mot-clé | Volume | Difficulté | Priorité |
|---------|--------|------------|----------|
| {{keyword1}} | X | X | 🔴 |
| {{keyword2}} | X | X | 🟠 |`,
  model: 'gpt4',
  estimatedTime: '60s'
};
