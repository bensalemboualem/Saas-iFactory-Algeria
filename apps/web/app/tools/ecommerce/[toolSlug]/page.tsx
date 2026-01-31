'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, ShoppingCart, Sparkles, Copy, Check, Loader2 } from 'lucide-react';
import { ecommerceTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

interface FormField {
  name: string;
  type: 'text' | 'textarea' | 'select' | 'checkbox' | 'number' | 'tags' | 'multiselect';
  label: string;
  required?: boolean;
  placeholder?: string;
  options?: string[] | { value: string; label: string }[];
}

interface FormConfig {
  fields: FormField[];
  promptTemplate: string;
}

// Configuration des formulaires par outil
const toolFormConfigs: Record<string, FormConfig> = {
  // ===== BATCH 1 - CRITIQUE (10 outils) =====

  'product-description-generator': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Nom du produit', required: true, placeholder: 'Ex: Montre connectée Sport Pro' },
      { name: 'product_category', type: 'text', label: 'Catégorie', required: true, placeholder: 'Ex: Électronique, Mode, Maison...' },
      { name: 'key_features', type: 'textarea', label: 'Caractéristiques principales', required: true, placeholder: 'Listez les features clés (une par ligne)' },
      { name: 'target_customer', type: 'text', label: 'Client cible', placeholder: 'Ex: Sportifs, Parents, Professionnels...' },
      { name: 'price_range', type: 'select', label: 'Gamme de prix', options: ['Budget', 'Milieu de gamme', 'Premium', 'Luxe'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Fun', 'Luxe', 'Technique', 'Émotionnel'] },
      { name: 'platform', type: 'select', label: 'Plateforme', options: ['Shopify', 'WooCommerce', 'Amazon', 'Etsy', 'Générique'] },
    ],
    promptTemplate: `Tu es un expert e-commerce avec des taux de conversion de 5%+.

PRODUIT : {{product_name}}
CATÉGORIE : {{product_category}}
CARACTÉRISTIQUES : {{key_features}}
CLIENT : {{target_customer}}
GAMME : {{price_range}}
TON : {{tone}}
PLATEFORME : {{platform}}

## 📦 FICHE PRODUIT COMPLÈTE

### TITRE PRODUIT (3 versions)
1. "[Titre SEO avec mot-clé principal pour {{product_name}}]"
2. "[Titre bénéfice-oriented]"
3. "[Titre émotionnel]"

---

### DESCRIPTION COURTE (150 caractères)
"[Accroche percutante pour les listings de {{product_name}}]"

---

### DESCRIPTION COMPLÈTE

**[Accroche émotionnelle - 1 ligne qui capture l'attention]**

[Paragraphe 1 : Le problème que résout {{product_name}}]

[Paragraphe 2 : La solution - votre produit]

**✨ Pourquoi vous allez l'adorer :**

✅ [Bénéfice 1 - pas feature, mais résultat pour {{target_customer}}]
✅ [Bénéfice 2]
✅ [Bénéfice 3]
✅ [Bénéfice 4]
✅ [Bénéfice 5]

**📋 Caractéristiques :**

| Caractéristique | Détail |
|-----------------|--------|
| [Feature 1] | [Spec] |
| [Feature 2] | [Spec] |
| [Feature 3] | [Spec] |

**🎁 Ce que vous recevez :**
- {{product_name}}
- [Accessoire inclus si applicable]
- [Guide/Manuel]

---

### BULLET POINTS {{platform}} (5)
- [Bullet 1 : Bénéfice principal + feature]
- [Bullet 2 : Qualité/Matériaux]
- [Bullet 3 : Facilité d'utilisation]
- [Bullet 4 : Polyvalence]
- [Bullet 5 : Garantie/SAV]

---

### MOTS-CLÉS SEO
**Primary :** [mot-clé principal]
**Secondary :** [mot-clé 2], [mot-clé 3]
**Long-tail :** [phrase clé 1], [phrase clé 2]

---

**Formule utilisée : AIDA + PAS**
- Attention → Accroche
- Intérêt → Problème/Solution
- Désir → Bénéfices
- Action → CTA implicite`
  },

  'product-title-optimizer': {
    fields: [
      { name: 'current_title', type: 'text', label: 'Titre actuel', required: true, placeholder: 'Votre titre produit actuel' },
      { name: 'product_type', type: 'text', label: 'Type de produit', placeholder: 'Ex: T-shirt, Casque audio, Crème...' },
      { name: 'brand', type: 'text', label: 'Marque', placeholder: 'Nom de votre marque' },
      { name: 'key_attributes', type: 'text', label: 'Attributs clés', placeholder: 'Ex: XL, Noir, Bio, 100ml...' },
      { name: 'platform', type: 'select', label: 'Plateforme', required: true, options: ['Amazon', 'Shopify', 'eBay', 'Etsy', 'Google Shopping'] },
    ],
    promptTemplate: `Tu es un expert SEO e-commerce.

TITRE ACTUEL : {{current_title}}
PRODUIT : {{product_type}}
MARQUE : {{brand}}
ATTRIBUTS : {{key_attributes}}
PLATEFORME : {{platform}}

## 🏷️ 10 TITRES OPTIMISÉS POUR {{platform}}

{{#if platform === 'Amazon'}}
**Format Amazon (200 caractères max) :**
[Marque] + [Produit] + [Caractéristique principale] + [Taille/Quantité] + [Couleur]
{{/if}}

{{#if platform === 'Google Shopping'}}
**Format Google Shopping (150 caractères) :**
[Produit] + [Marque] + [Attributs] + [Couleur] + [Taille]
{{/if}}

{{#if platform === 'Etsy'}}
**Format Etsy (140 caractères) :**
[Mot-clé principal] + [Descripteur] + [Usage/Occasion]
{{/if}}

### 10 TITRES OPTIMISÉS

1. "{{brand}} - {{product_type}} {{key_attributes}} [Bénéfice principal]"
2. "[Mot-clé principal] {{brand}} - [Attribut] pour [Usage]"
3. "{{product_type}} [Qualité] {{brand}} - [Attributs] [Taille]"
4. "[Bénéfice] {{product_type}} - {{brand}} [Attributs]"
5. "{{brand}} {{product_type}} [Caractéristique unique] - [Cible]"
6. "[Mot-clé longue traîne] - {{brand}} {{product_type}}"
7. "{{product_type}} {{brand}} [Premium/Pro/Elite] - {{key_attributes}}"
8. "[Adjectif accrocheur] {{product_type}} {{brand}} [Attributs]"
9. "{{brand}} - {{product_type}} [Pour X] {{key_attributes}}"
10. "[Meilleur/Top] {{product_type}} {{brand}} - [Attributs]"

---

### 📊 ANALYSE DES TITRES

| Titre | Caractères | Mots-clés | Score SEO |
|-------|------------|-----------|-----------|
| 1 | X/200 | ✅ | ⭐⭐⭐⭐⭐ |
| 2 | X/200 | ✅ | ⭐⭐⭐⭐ |
| 3 | X/200 | ✅ | ⭐⭐⭐⭐ |

---

### ✅ BONNES PRATIQUES {{platform}}

✅ Mot-clé principal en début
✅ Marque visible
✅ Attributs clés inclus
✅ Respect de la limite de caractères

### ❌ À ÉVITER

❌ Majuscules abusives
❌ Caractères spéciaux (★, ♥)
❌ Mots promotionnels (PROMO, SOLDES)
❌ Répétition de mots-clés`
  },

  'ecommerce-ad-copy-generator': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Produit', required: true },
      { name: 'unique_selling_point', type: 'text', label: 'Argument clé de vente', placeholder: 'Ce qui vous différencie' },
      { name: 'target_audience', type: 'textarea', label: 'Audience cible', placeholder: 'Décrivez votre client idéal' },
      { name: 'offer', type: 'text', label: 'Offre/Promotion', placeholder: '-20%, Livraison gratuite...' },
      { name: 'platform', type: 'select', label: 'Plateforme', required: true, options: ['Facebook/Instagram', 'Google Search', 'Google Shopping', 'TikTok'] },
      { name: 'ad_objective', type: 'select', label: 'Objectif', options: ['Conversions', 'Trafic', 'Notoriété', 'Retargeting'] },
    ],
    promptTemplate: `Tu es un expert en publicité e-commerce avec des ROAS de 4x+.

PRODUIT : {{product_name}}
USP : {{unique_selling_point}}
AUDIENCE : {{target_audience}}
OFFRE : {{offer}}
PLATEFORME : {{platform}}
OBJECTIF : {{ad_objective}}

## 📣 COPIES PUBLICITAIRES {{platform}}

{{#if platform === 'Facebook/Instagram'}}
### FACEBOOK/INSTAGRAM ADS

**Ad 1 : Pain Point**

🎯 **Primary Text :**
"[Question sur le problème de {{target_audience}}]

{{product_name}} est la solution.

{{unique_selling_point}}

{{offer}}

👉 Cliquez pour découvrir !"

**Headline :** [6-8 mots max avec bénéfice]
**Description :** {{offer}} - Livraison rapide
**CTA Button :** Shop Now

---

**Ad 2 : Social Proof**

⭐ **Primary Text :**
"Plus de [X] clients satisfaits !

"[Témoignage court]" - Marie P.

{{product_name}} - {{unique_selling_point}}

{{offer}}

🛒 Commandez maintenant !"

**Headline :** [X] clients nous font confiance
**CTA Button :** Shop Now

---

**Ad 3 : FOMO/Urgence**

🔥 **Primary Text :**
"⚠️ Stock limité !

{{product_name}} - {{unique_selling_point}}

{{offer}}

⏰ Plus que [X] disponibles !

👉 Ne ratez pas cette offre !"

---

**Ad 4 : UGC Style**

📱 **Primary Text :**
"POV : Tu découvres enfin {{product_name}} 😍

[Description bénéfice casual]

Le lien est dans notre bio 👆"
{{/if}}

{{#if platform === 'Google Search'}}
### GOOGLE SEARCH ADS

**Ad 1 :**
- **Headline 1 (30 car.) :** "{{product_name}} - {{offer}}"
- **Headline 2 (30 car.) :** "{{unique_selling_point}}"
- **Headline 3 (30 car.) :** "Livraison Gratuite dès [X]€"
- **Description 1 (90 car.) :** "[Description avec mots-clés et bénéfices]"
- **Description 2 (90 car.) :** "[Social proof + CTA urgent]"

**Ad 2 :**
- **Headline 1 :** "[Mot-clé] - Qualité Premium"
- **Headline 2 :** "{{offer}} | Stock Limité"
- **Headline 3 :** "Satisfait ou Remboursé"

**Extensions suggérées :**
- **Sitelinks :** Nouveautés, Promotions, FAQ, Contact
- **Callouts :** Livraison 24h, Retours gratuits, Paiement sécurisé
- **Structured snippets :** Types: [variantes produit]
{{/if}}

---

### 🎯 A/B TESTS RECOMMANDÉS

1. Hook émotionnel vs rationnel
2. Avec vs sans émojis
3. Prix affiché vs "Découvrir l'offre"
4. Témoignage vs statistique`
  },

  'collection-description-generator': {
    fields: [
      { name: 'collection_name', type: 'text', label: 'Nom de la collection', required: true },
      { name: 'products_included', type: 'textarea', label: 'Types de produits inclus', placeholder: 'Décrivez les produits de cette collection' },
      { name: 'target_keywords', type: 'text', label: 'Mots-clés SEO cibles', placeholder: 'Ex: robe été, chaussures femme...' },
      { name: 'brand_voice', type: 'select', label: 'Ton', options: ['Professionnel', 'Casual', 'Luxe', 'Éco-responsable', 'Tech'] },
      { name: 'word_count', type: 'select', label: 'Longueur', options: ['Court (100 mots)', 'Moyen (250 mots)', 'Long (500 mots)'] },
    ],
    promptTemplate: `Tu es un expert SEO e-commerce.

COLLECTION : {{collection_name}}
PRODUITS : {{products_included}}
MOTS-CLÉS : {{target_keywords}}
TON : {{brand_voice}}
LONGUEUR : {{word_count}}

## 📁 DESCRIPTION DE COLLECTION "{{collection_name}}"

### H1 : {{collection_name}}

[Paragraphe d'introduction avec "{{target_keywords}}" dans les 100 premiers mots]

**Découvrez notre sélection de {{collection_name}} :**

[Paragraphe décrivant la variété et la qualité des produits]

**Pourquoi choisir notre collection {{collection_name}} ?**

✅ [Avantage 1 - Qualité]
✅ [Avantage 2 - Variété]
✅ [Avantage 3 - Prix/Valeur]
✅ [Avantage 4 - Service]

[Paragraphe avec mots-clés secondaires naturellement intégrés]

**Explorez notre collection et trouvez votre bonheur !**

---

### VERSION COURTE (Listings)

"[Description 150 caractères pour {{collection_name}}]"

---

### META DESCRIPTION (155 caractères)

"[Meta description optimisée : {{target_keywords}} + CTA + valeur unique]"

---

### 📊 OPTIMISATION SEO

**Densité mots-clés :**
- {{target_keywords}} : 2-3 occurrences
- Mots-clés secondaires : 1-2 occurrences

**Structure Hn suggérée :**
- H1 : {{collection_name}}
- H2 : Pourquoi choisir notre collection ?
- H2 : Nos produits phares
- H2 : Guide d'achat`
  },

  'customer-review-response': {
    fields: [
      { name: 'review_text', type: 'textarea', label: 'Texte de l\'avis', required: true, placeholder: 'Copiez l\'avis client ici' },
      { name: 'rating', type: 'select', label: 'Note', required: true, options: ['5 étoiles', '4 étoiles', '3 étoiles', '2 étoiles', '1 étoile'] },
      { name: 'review_type', type: 'select', label: 'Type de problème (si négatif)', options: ['Qualité produit', 'Livraison', 'Service client', 'Produit différent', 'Produit endommagé', 'Autre', 'Aucun (avis positif)'] },
      { name: 'brand_name', type: 'text', label: 'Nom de la marque', required: true },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Chaleureux', 'Apologétique'] },
    ],
    promptTemplate: `Tu es un expert en service client e-commerce.

AVIS : "{{review_text}}"
NOTE : {{rating}}
PROBLÈME : {{review_type}}
MARQUE : {{brand_name}}
TON : {{tone}}

## ⭐ RÉPONSE À L'AVIS

{{#if rating === '5 étoiles' || rating === '4 étoiles'}}
### Réponse Avis Positif ({{rating}})

"Bonjour [Prénom si visible],

Merci infiniment pour ce retour et cette belle note ! 🙏

[Réponse personnalisée à un point spécifique mentionné dans l'avis]

Nous sommes ravis que [produit/aspect mentionné] vous ait plu.

N'hésitez pas à nous contacter si vous avez besoin de quoi que ce soit. Au plaisir de vous revoir !

L'équipe {{brand_name}}"

---

**Variante plus courte :**

"Merci beaucoup pour votre avis ! 🙏 Nous sommes ravis que [aspect positif]. À très bientôt ! - L'équipe {{brand_name}}"
{{/if}}

{{#if rating === '3 étoiles'}}
### Réponse Avis Mitigé ({{rating}})

"Bonjour [Prénom],

Merci d'avoir pris le temps de partager votre expérience.

Nous sommes contents que [aspect positif mentionné], mais sincèrement désolés que [aspect négatif].

[Explication ou solution proposée pour améliorer]

Nous aimerions en discuter avec vous - contactez-nous à [email] pour qu'on puisse améliorer votre expérience.

Cordialement,
L'équipe {{brand_name}}"
{{/if}}

{{#if rating === '2 étoiles' || rating === '1 étoile'}}
### Réponse Avis Négatif ({{rating}})

"Bonjour [Prénom],

Nous sommes sincèrement désolés d'apprendre votre déception. Ce n'est absolument pas l'expérience que nous souhaitons offrir à nos clients.

{{#if review_type === 'Livraison'}}
Nous comprenons à quel point un retard de livraison peut être frustrant. Nous prenons ce problème très au sérieux et travaillons avec nos partenaires logistiques pour améliorer nos délais.
{{/if}}

{{#if review_type === 'Qualité produit'}}
La qualité est notre priorité absolue. Nous souhaitons comprendre ce qui s'est passé pour vous offrir une solution.
{{/if}}

Nous aimerions vraiment nous rattraper. Pourriez-vous nous contacter à [email] avec votre numéro de commande ? Nous trouverons une solution ensemble.

Avec toutes nos excuses,
L'équipe {{brand_name}}"
{{/if}}

---

### ✅ RÈGLES D'OR RÉPONSES AVIS

✅ Répondre en < 24-48h
✅ Toujours remercier (même avis négatif)
✅ Personnaliser la réponse
✅ Ne jamais être défensif
✅ Proposer une solution concrète
✅ Déplacer en privé si sensible`
  },

  'ecommerce-faq-generator': {
    fields: [
      { name: 'business_type', type: 'select', label: 'Type de business', required: true, options: ['Produits physiques', 'Produits digitaux', 'Services', 'Abonnement'] },
      { name: 'product_category', type: 'text', label: 'Catégorie de produits', required: true },
      { name: 'shipping_info', type: 'textarea', label: 'Infos livraison', placeholder: 'Délais, zones, frais...' },
      { name: 'return_policy', type: 'textarea', label: 'Politique de retour', placeholder: 'Délai, conditions...' },
      { name: 'payment_methods', type: 'text', label: 'Moyens de paiement', placeholder: 'CB, PayPal, virement...' },
      { name: 'common_questions', type: 'textarea', label: 'Questions fréquentes reçues', placeholder: 'Questions que vous recevez souvent' },
    ],
    promptTemplate: `Tu es un expert en expérience client e-commerce.

BUSINESS : {{business_type}}
CATÉGORIE : {{product_category}}
LIVRAISON : {{shipping_info}}
RETOURS : {{return_policy}}
PAIEMENTS : {{payment_methods}}
QUESTIONS COURANTES : {{common_questions}}

## ❓ FAQ E-COMMERCE COMPLÈTE

### 📦 COMMANDES & LIVRAISON

**Q : Quels sont les délais de livraison ?**
R : {{shipping_info}}. Les commandes passées avant 14h sont généralement expédiées le jour même.

**Q : Comment suivre ma commande ?**
R : Vous recevrez un email avec votre numéro de suivi dès l'expédition. Vous pouvez également suivre votre commande depuis votre espace client.

**Q : Livrez-vous à l'international ?**
R : [Réponse basée sur zones de livraison]

**Q : Quels sont les frais de livraison ?**
R : [Grille tarifaire ou seuil gratuit]

**Q : Ma commande n'est pas arrivée, que faire ?**
R : Contactez-nous à [email] avec votre numéro de commande. Nous enquêterons immédiatement.

---

### 💳 PAIEMENT

**Q : Quels moyens de paiement acceptez-vous ?**
R : Nous acceptons : {{payment_methods}}. Tous les paiements sont sécurisés.

**Q : Le paiement est-il sécurisé ?**
R : Absolument ! Nous utilisons le protocole SSL et travaillons avec des partenaires de paiement certifiés (Stripe, PayPal).

**Q : Puis-je payer en plusieurs fois ?**
R : [Politique de paiement fractionné si applicable]

---

### 🔄 RETOURS & REMBOURSEMENTS

**Q : Quelle est votre politique de retour ?**
R : {{return_policy}}

**Q : Comment retourner un article ?**
R : 1) Connectez-vous à votre compte 2) Sélectionnez la commande 3) Demandez un retour 4) Imprimez l'étiquette 5) Déposez le colis

**Q : Sous quel délai serai-je remboursé ?**
R : Votre remboursement sera effectué sous 5-7 jours ouvrés après réception du retour.

---

### 🛍️ PRODUITS - {{product_category}}

**Q : [Question spécifique au produit 1] ?**
R : [Réponse détaillée]

**Q : [Question spécifique au produit 2] ?**
R : [Réponse détaillée]

---

### 📞 CONTACT & SUPPORT

**Q : Comment vous contacter ?**
R : Email : [email] | Chat : disponible sur le site | Téléphone : [numéro] (Lun-Ven 9h-18h)

---

### 📋 SCHEMA FAQ (JSON-LD)

\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Réponse]"
      }
    }
  ]
}
\`\`\``
  },

  'shipping-policy-generator': {
    fields: [
      { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
      { name: 'shipping_zones', type: 'text', label: 'Zones de livraison', placeholder: 'Algérie, Tunisie, Maroc...' },
      { name: 'carriers', type: 'text', label: 'Transporteurs utilisés', placeholder: 'Colissimo, Chronopost, DHL...' },
      { name: 'processing_time', type: 'text', label: 'Délai de traitement', placeholder: 'Ex: 24-48h' },
      { name: 'shipping_options', type: 'textarea', label: 'Options de livraison', placeholder: 'Standard, Express, Point relais...' },
      { name: 'free_shipping_threshold', type: 'text', label: 'Seuil livraison gratuite', placeholder: 'Ex: 50€' },
    ],
    promptTemplate: `Génère une politique de livraison complète et professionnelle.

ENTREPRISE : {{business_name}}
ZONES : {{shipping_zones}}
TRANSPORTEURS : {{carriers}}
TRAITEMENT : {{processing_time}}
OPTIONS : {{shipping_options}}
GRATUIT À PARTIR DE : {{free_shipping_threshold}}

## 🚚 POLITIQUE DE LIVRAISON - {{business_name}}

### 1. ZONES DE LIVRAISON

{{business_name}} livre actuellement dans les pays/régions suivants :
{{shipping_zones}}

Pour les destinations non listées, contactez-nous pour un devis personnalisé.

### 2. DÉLAIS DE LIVRAISON

| Destination | Livraison Standard | Livraison Express |
|-------------|-------------------|-------------------|
| France métropolitaine | 3-5 jours ouvrés | 24-48h |
| Belgique / Luxembourg | 4-6 jours ouvrés | 48-72h |
| Maroc | 5-7 jours ouvrés | 3-4 jours |
| DOM-TOM | 7-14 jours | Sur devis |

**Note :** Ces délais sont donnés à titre indicatif à partir de l'expédition et ne tiennent pas compte des weekends et jours fériés.

### 3. FRAIS DE LIVRAISON

| Destination | Standard | Express | Point Relais |
|-------------|----------|---------|--------------|
| France | X€ | X€ | X€ |
| Belgique | X€ | X€ | X€ |

{{#if free_shipping_threshold}}
**🎁 Livraison GRATUITE** à partir de {{free_shipping_threshold}} d'achat (France métropolitaine).
{{/if}}

### 4. TRAITEMENT DES COMMANDES

- Les commandes sont préparées sous **{{processing_time}}** (jours ouvrés)
- Les commandes passées après 14h sont traitées le jour ouvré suivant
- Un email de confirmation avec numéro de suivi vous sera envoyé à l'expédition

### 5. TRANSPORTEURS

Nous travaillons avec des transporteurs de confiance : {{carriers}}

### 6. SUIVI DE COMMANDE

Dès l'expédition, vous recevrez un email contenant :
- Votre numéro de suivi
- Un lien vers le site du transporteur
- La date de livraison estimée

### 7. PROBLÈMES DE LIVRAISON

**Colis perdu :** Contactez-nous immédiatement. Nous ouvrirons une enquête et vous renverrons votre commande.

**Colis endommagé :** Refusez le colis ou notez les dommages sur le bon de livraison. Contactez-nous avec photos.

### 8. CONTACT

Pour toute question concernant la livraison :
📧 Email : [email]
📞 Téléphone : [numéro]

---
*Dernière mise à jour : [Date]*`
  },

  'return-policy-generator': {
    fields: [
      { name: 'business_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
      { name: 'return_window', type: 'select', label: 'Délai de retour', required: true, options: ['14 jours', '30 jours', '60 jours', '90 jours'] },
      { name: 'condition_required', type: 'select', label: 'État requis', options: ['Neuf avec étiquettes', 'Neuf sans étiquettes', 'Tout état accepté'] },
      { name: 'refund_method', type: 'select', label: 'Mode de remboursement', options: ['Moyen de paiement original', 'Avoir en magasin', 'Les deux au choix'] },
      { name: 'return_shipping', type: 'select', label: 'Frais de retour', options: ['Gratuits (prépayés)', 'À la charge du client', 'Selon motif'] },
      { name: 'exceptions', type: 'textarea', label: 'Produits exclus des retours', placeholder: 'Sous-vêtements, produits personnalisés...' },
    ],
    promptTemplate: `Génère une politique de retour claire et rassurante.

ENTREPRISE : {{business_name}}
DÉLAI : {{return_window}}
ÉTAT REQUIS : {{condition_required}}
REMBOURSEMENT : {{refund_method}}
FRAIS RETOUR : {{return_shipping}}
EXCEPTIONS : {{exceptions}}

## 🔄 POLITIQUE DE RETOUR & REMBOURSEMENT - {{business_name}}

### NOTRE ENGAGEMENT

Chez {{business_name}}, votre satisfaction est notre priorité. Si vous n'êtes pas entièrement satisfait de votre achat, nous sommes là pour vous aider.

---

### 1. DÉLAI DE RETOUR

Vous disposez de **{{return_window}}** à compter de la réception de votre commande pour nous retourner un article.

### 2. CONDITIONS DE RETOUR

Pour être éligible au retour, l'article doit être :

{{#if condition_required === 'Neuf avec étiquettes'}}
✅ Non porté / non utilisé
✅ Dans son emballage d'origine
✅ Avec toutes les étiquettes attachées
{{/if}}

{{#if condition_required === 'Neuf sans étiquettes'}}
✅ Non porté / non utilisé
✅ En parfait état
✅ Dans son emballage si possible
{{/if}}

### 3. COMMENT RETOURNER UN ARTICLE ?

**Étape 1 :** Connectez-vous à votre compte ou contactez-nous à [email]

**Étape 2 :** Demandez un numéro de retour (RMA)

**Étape 3 :** Emballez soigneusement l'article

**Étape 4 :** Expédiez à l'adresse fournie

### 4. FRAIS DE RETOUR

{{#if return_shipping === 'Gratuits (prépayés)'}}
🎁 Les frais de retour sont **GRATUITS**. Une étiquette prépayée vous sera envoyée par email.
{{/if}}

{{#if return_shipping === 'À la charge du client'}}
Les frais de retour sont à la charge du client, sauf en cas d'erreur de notre part ou de produit défectueux.
{{/if}}

### 5. REMBOURSEMENT

Une fois le retour reçu et inspecté (sous 48h) :
- **Délai de remboursement :** 5-7 jours ouvrés
- **Mode :** {{refund_method}}

### 6. ÉCHANGES

Vous souhaitez une autre taille/couleur ? Contactez-nous ! Nous ferons notre maximum pour vous satisfaire.

### 7. ARTICLES NON RETOURNABLES

Pour des raisons d'hygiène et de sécurité, les articles suivants ne peuvent être retournés :
{{exceptions}}

### 8. ARTICLES DÉFECTUEUX

Vous avez reçu un article défectueux ? Contactez-nous immédiatement avec photos. Nous vous enverrons un remplacement sans frais.

---

*Conformément à l'article L221-18 du Code de la consommation (droit de rétractation de 14 jours)*`
  },

  'upsell-cross-sell-generator': {
    fields: [
      { name: 'main_product', type: 'text', label: 'Produit principal', required: true },
      { name: 'product_price', type: 'text', label: 'Prix du produit', placeholder: 'Ex: 49€' },
      { name: 'product_category', type: 'text', label: 'Catégorie', placeholder: 'Ex: Électronique, Mode...' },
      { name: 'available_products', type: 'textarea', label: 'Autres produits disponibles', placeholder: 'Listez vos autres produits' },
      { name: 'strategy', type: 'select', label: 'Stratégie', required: true, options: ['Upsell', 'Cross-sell', 'Bundle', 'Toutes'] },
    ],
    promptTemplate: `Tu es un expert en optimisation de panier e-commerce.

PRODUIT : {{main_product}}
PRIX : {{product_price}}
CATÉGORIE : {{product_category}}
CATALOGUE : {{available_products}}
STRATÉGIE : {{strategy}}

## 💰 STRATÉGIES UPSELL/CROSS-SELL POUR {{main_product}}

### 📈 UPSELL (Version supérieure)

**Produit recommandé :** [Version Premium de {{main_product}}]
**Prix suggéré :** [+30-50% vs {{product_price}}]

**Copy page produit :**
"🌟 **Version Premium disponible !**

Pour seulement [X€] de plus, obtenez :
✅ [Avantage Premium 1]
✅ [Avantage Premium 2]
✅ [Avantage Premium 3]

👉 [BOUTON : Passer à la version Premium]"

**Copy panier :**
"💎 **Upgrade recommandé**
Passez à {{main_product}} Pro pour [X€] de plus et bénéficiez de [avantage clé] !"

---

### 🛒 CROSS-SELL (Produits complémentaires)

**Produits suggérés :**

1. **[Produit A]** - [Prix]
   → Pourquoi : [Complémentarité avec {{main_product}}]

2. **[Produit B]** - [Prix]
   → Pourquoi : [Améliore l'expérience]

3. **[Produit C]** - [Prix]
   → Pourquoi : [Achat fréquent ensemble]

**Copy page produit :**
"👥 **Les clients ont aussi acheté :**"
[Carrousel de produits complémentaires]

**Copy panier :**
"🎯 **Complétez votre commande :**
Ajoutez [Produit A] pour seulement [X€] de plus !"

**Copy checkout :**
"⚡ **Dernière chance !**
[Produit B] - Seulement [X€] - Ajouter en 1 clic"

---

### 📦 BUNDLE (Pack)

**Pack suggéré :** {{main_product}} + [Produit B] + [Produit C]

**Prix bundle :** [X€] au lieu de [Y€] (**-Z%**)

**Copy page produit :**
"📦 **PACK COMPLET** - Économisez [Z]% !

Tout ce qu'il vous faut pour [objectif/usage] :

✅ {{main_product}} (valeur [X€])
✅ [Produit B] (valeur [X€])
✅ [Produit C] (valeur [X€])

~~[Prix total]€~~ → **[Prix bundle]€**

👉 [BOUTON : Ajouter le pack au panier]"

---

### 📍 EMPLACEMENTS RECOMMANDÉS

| Stratégie | Emplacement | Moment optimal |
|-----------|-------------|----------------|
| Upsell | Page produit | Avant ajout panier |
| Cross-sell | Sous description | Pendant navigation |
| Cross-sell | Panier | Avant checkout |
| Bundle | Page produit | Section dédiée |
| Upsell | Checkout | Dernière chance |

### 📊 MÉTRIQUES À SUIVRE

- Taux d'acceptation upsell
- AOV (Average Order Value)
- Taux de conversion bundle
- Revenue par visiteur`
  },

  'seo-product-optimizer': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
      { name: 'current_title', type: 'text', label: 'Titre actuel', placeholder: 'Votre title tag actuel' },
      { name: 'current_description', type: 'textarea', label: 'Description actuelle', placeholder: 'Votre meta description actuelle' },
      { name: 'target_keywords', type: 'text', label: 'Mots-clés cibles', required: true, placeholder: 'Mot-clé principal, mot-clé secondaire...' },
      { name: 'competitors', type: 'textarea', label: 'URLs concurrentes (optionnel)', placeholder: 'URLs de concurrents bien positionnés' },
    ],
    promptTemplate: `Tu es un expert SEO e-commerce.

PRODUIT : {{product_name}}
TITRE ACTUEL : {{current_title}}
DESCRIPTION : {{current_description}}
MOTS-CLÉS : {{target_keywords}}
CONCURRENTS : {{competitors}}

## 🔍 AUDIT SEO PRODUIT - {{product_name}}

### 📊 SCORE ACTUEL : X/100

| Élément | Score | Statut | Recommandation |
|---------|-------|--------|----------------|
| Title tag | X/15 | ⚠️ | [Action requise] |
| Meta description | X/15 | ✅ | [Optimisation mineure] |
| H1 | X/10 | ❌ | [Problème critique] |
| Contenu | X/20 | ⚠️ | [Amélioration suggérée] |
| Images | X/15 | ❌ | [ALT manquants] |
| URL | X/10 | ✅ | OK |
| Schema | X/15 | ❌ | [Non implémenté] |

---

### 🔧 OPTIMISATIONS RECOMMANDÉES

**1. TITLE TAG (50-60 caractères)**

❌ Actuel : "{{current_title}}"
✅ Optimisé : "{{target_keywords}} - [Bénéfice] | [Marque]"

**Alternatives :**
- "[Mot-clé] [Attribut] - [Bénéfice] | [Marque]"
- "[Marque] [Produit] - [USP] | [CTA]"

---

**2. META DESCRIPTION (150-160 caractères)**

"[Description optimisée incluant {{target_keywords}}, un bénéfice clé et un CTA]. ✓ Livraison gratuite | ✓ Retours faciles"

---

**3. URL SLUG**

❌ Actuel : /produit-12345
✅ Recommandé : /{{target_keywords}}-[attribut]

---

**4. STRUCTURE Hn**

- **H1 :** {{product_name}} - [Mot-clé secondaire]
- **H2 :** Description
- **H2 :** Caractéristiques
- **H2 :** Avis clients (X avis)
- **H2 :** FAQ

---

**5. BALISES ALT IMAGES**

- Image principale : "{{product_name}} - [vue principale]"
- Image 2 : "{{product_name}} - [vue détail/usage]"
- Image 3 : "{{product_name}} - [vue lifestyle]"

---

**6. SCHEMA PRODUCT (JSON-LD)**

\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{product_name}}",
  "description": "[Description]",
  "image": "[URL image]",
  "brand": {
    "@type": "Brand",
    "name": "[Marque]"
  },
  "offers": {
    "@type": "Offer",
    "price": "[Prix]",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[Note]",
    "reviewCount": "[Nombre avis]"
  }
}
\`\`\`

---

### 🎯 MOTS-CLÉS RECOMMANDÉS

| Mot-clé | Volume mensuel | Difficulté | Priorité |
|---------|---------------|------------|----------|
| {{target_keywords}} | X | Moyenne | 🔴 Haute |
| [Mot-clé 2] | X | Faible | 🟠 Moyenne |
| [Mot-clé longue traîne] | X | Faible | 🟢 Quick win |`
  },

  // ===== BATCH 2 - HAUTE PRIORITÉ (10 outils) =====

  'price-comparison-copy': {
    fields: [
      { name: 'products', type: 'textarea', label: 'Produits à comparer', required: true, placeholder: 'Listez les produits avec leurs prix' },
      { name: 'comparison_type', type: 'select', label: 'Type de comparaison', options: ['Nos produits entre eux', 'Vs concurrents', 'Plans/Abonnements'] },
      { name: 'highlight_product', type: 'text', label: 'Produit à mettre en avant', placeholder: 'Le produit recommandé' },
    ],
    promptTemplate: `Tu es un expert en conversion e-commerce.

PRODUITS : {{products}}
TYPE : {{comparison_type}}
PRODUIT RECOMMANDÉ : {{highlight_product}}

## 📊 TABLEAU COMPARATIF

### Format tableau

| Caractéristique | Produit A | **{{highlight_product}}** ⭐ | Produit C |
|-----------------|-----------|------------------------------|-----------|
| Prix | X€ | **X€** | X€ |
| [Feature 1] | ✅ | ✅ | ❌ |
| [Feature 2] | ❌ | ✅ | ✅ |
| [Feature 3] | ✅ | ✅ | ❌ |

**Notre recommandation :** {{highlight_product}} - Le meilleur rapport qualité/prix

---

### Copy d'accompagnement

"Pas sûr de votre choix ? Comparez nos [catégorie] et trouvez celui qui vous correspond."

[CTA : Voir le comparatif complet]`
  },

  'product-launch-copy': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
      { name: 'launch_date', type: 'text', label: 'Date de lancement' },
      { name: 'key_features', type: 'textarea', label: 'Features principales' },
      { name: 'launch_offer', type: 'text', label: 'Offre de lancement', placeholder: '-20%, bonus early bird...' },
      { name: 'target_audience', type: 'text', label: 'Audience cible' },
    ],
    promptTemplate: `Tu es un expert en lancement produit.

PRODUIT : {{product_name}}
DATE : {{launch_date}}
FEATURES : {{key_features}}
OFFRE : {{launch_offer}}
AUDIENCE : {{target_audience}}

## 🚀 KIT LANCEMENT {{product_name}}

### Email teaser (J-7)

**Objet :** Quelque chose d'excitant arrive... 👀

"Préparez-vous. Le {{launch_date}}, tout change.
[Teaser sans révéler le produit]
Restez à l'écoute..."

---

### Email annonce (Jour J)

**Objet :** 🚀 C'est officiel : {{product_name}} est là !

"Le jour est arrivé !
Découvrez {{product_name}} - [Tagline]
{{key_features}}
**Offre de lancement :** {{launch_offer}}
[CTA : Découvrir maintenant]"

---

### Posts réseaux sociaux

**Instagram/Facebook :**
"🚀 NOUVEAU : {{product_name}} est enfin disponible !
[Description courte]
{{launch_offer}} jusqu'au [date]
Lien en bio 👆"

**Story sequence :**
1. Teaser
2. Reveal
3. Features
4. Offre
5. CTA

---

### Landing page sections

1. Hero avec offre
2. Problème/Solution
3. Features
4. Social proof
5. FAQ
6. CTA final`
  },

  'seasonal-promotion-generator': {
    fields: [
      { name: 'event', type: 'select', label: 'Événement', required: true, options: ['Black Friday', 'Cyber Monday', 'Noël', 'Soldes d\'été', 'Soldes d\'hiver', 'Saint-Valentin', 'Fête des mères', 'Rentrée', 'Autre'] },
      { name: 'discount', type: 'text', label: 'Réduction offerte', placeholder: '-30%, -50€, Livraison gratuite...' },
      { name: 'products_concerned', type: 'text', label: 'Produits concernés', placeholder: 'Tout le site, catégorie spécifique...' },
      { name: 'duration', type: 'text', label: 'Durée de l\'offre', placeholder: '24h, 1 semaine...' },
    ],
    promptTemplate: `Tu es un expert en promotions e-commerce.

ÉVÉNEMENT : {{event}}
RÉDUCTION : {{discount}}
PRODUITS : {{products_concerned}}
DURÉE : {{duration}}

## 🎉 CAMPAGNE {{event}}

### Bannière site

**Headline :** "{{event}} - {{discount}} sur {{products_concerned}}"
**Sub-headline :** "Offre valable {{duration}} seulement !"
**CTA :** "J'en profite"

---

### Email promotionnel

**Objet :** 🔥 {{event}} : {{discount}} - C'est maintenant !

"[Prénom],

C'est {{event}} chez [Marque] !

**{{discount}} sur {{products_concerned}}**

⏰ Plus que {{duration}} pour en profiter !

[BOUTON : Shopper maintenant]"

---

### Posts sociaux

**Facebook/Instagram :**
"🔥 {{event}} 🔥
{{discount}} sur {{products_concerned}}
⏰ {{duration}} seulement !
Lien en bio 👆
#{{event}} #Promo #Shopping"

---

### Countdown urgence

"⏰ Plus que [X]h [X]min pour profiter de {{discount}} !"

---

### Retargeting

"Vous avez oublié ? {{discount}} expire bientôt !
Finalisez votre commande avant qu'il soit trop tard."`
  },

  'loyalty-program-copy': {
    fields: [
      { name: 'program_name', type: 'text', label: 'Nom du programme', placeholder: 'Ex: Club VIP, Points Fidélité...' },
      { name: 'rewards', type: 'textarea', label: 'Récompenses offertes', placeholder: 'Points, réductions, cadeaux...' },
      { name: 'tiers', type: 'textarea', label: 'Niveaux (si applicable)', placeholder: 'Bronze, Silver, Gold...' },
      { name: 'earning_method', type: 'text', label: 'Comment gagner des points', placeholder: '1€ = 1 point...' },
    ],
    promptTemplate: `Tu es un expert en programmes de fidélité.

PROGRAMME : {{program_name}}
RÉCOMPENSES : {{rewards}}
NIVEAUX : {{tiers}}
GAINS : {{earning_method}}

## 🎁 PROGRAMME {{program_name}}

### Page principale

**Headline :** "Rejoignez {{program_name}} - Soyez récompensé à chaque achat !"

**Comment ça marche :**
1. 📝 Inscrivez-vous gratuitement
2. 🛒 Achetez et cumulez des points ({{earning_method}})
3. 🎁 Échangez vos points contre des récompenses

**Récompenses disponibles :**
{{rewards}}

**Niveaux {{program_name}} :**
{{tiers}}

[CTA : Rejoindre gratuitement]

---

### Email invitation

**Objet :** 🎁 [Prénom], rejoignez {{program_name}} et gagnez [X] points !

"Devenez membre {{program_name}} et profitez d'avantages exclusifs :
✅ [Avantage 1]
✅ [Avantage 2]
✅ [Avantage 3]

C'est gratuit et ça prend 30 secondes !

[CTA : Je m'inscris]"`
  },

  'cart-abandonment-popup': {
    fields: [
      { name: 'incentive', type: 'select', label: 'Incentive offert', options: ['Réduction %', 'Livraison gratuite', 'Cadeau', 'Code promo', 'Aucun'] },
      { name: 'incentive_value', type: 'text', label: 'Valeur de l\'incentive', placeholder: '10%, 5€...' },
      { name: 'urgency', type: 'select', label: 'Type d\'urgence', options: ['Stock limité', 'Offre temporaire', 'Panier sauvegardé', 'Aucune'] },
      { name: 'brand_tone', type: 'select', label: 'Ton', options: ['Amical', 'Urgent', 'Humoristique', 'Premium'] },
    ],
    promptTemplate: `Tu es un expert en conversion e-commerce.

INCENTIVE : {{incentive}} - {{incentive_value}}
URGENCE : {{urgency}}
TON : {{brand_tone}}

## 🛒 POPUPS ABANDON PANIER

### Popup 1 : Exit-intent classique

**Headline :** "Attendez ! Vous oubliez quelque chose 😢"

**Body :**
"Votre panier vous attend...

{{#if incentive !== 'Aucun'}}
Pour vous aider à vous décider :
**{{incentive_value}} de réduction** avec le code STAY10
{{/if}}

[BOUTON : Finaliser ma commande]
[Lien : Non merci]"

---

### Popup 2 : Urgence

**Headline :** "⏰ Votre panier expire bientôt !"

**Body :**
"Les articles de votre panier ne sont pas réservés.

{{#if urgency === 'Stock limité'}}
⚠️ Stock limité - Ne ratez pas votre chance !
{{/if}}

[BOUTON : Sécuriser ma commande]"

---

### Popup 3 : Social proof

**Headline :** "Vous avez bon goût ! 👍"

**Body :**
"[X] personnes regardent aussi ces articles en ce moment.

Finalisez votre commande avant rupture de stock.

[BOUTON : Commander maintenant]"

---

### Popup 4 : Email capture

**Headline :** "On garde votre panier au chaud ? 📧"

**Body :**
"Laissez votre email et retrouvez votre panier plus tard.

{{#if incentive !== 'Aucun'}}
+ Recevez {{incentive_value}} de réduction !
{{/if}}

[Input email]
[BOUTON : Envoyer mon panier]"

---

### A/B Tests recommandés

- Avec vs sans incentive
- Urgence vs empathie
- Popup immédiat vs délayé (5s)`
  },

  'product-comparison-table': {
    fields: [
      { name: 'products', type: 'textarea', label: 'Produits à comparer', required: true },
      { name: 'features', type: 'textarea', label: 'Caractéristiques à comparer' },
      { name: 'recommended', type: 'text', label: 'Produit recommandé' },
    ],
    promptTemplate: `Génère un tableau comparatif professionnel.

PRODUITS : {{products}}
FEATURES : {{features}}
RECOMMANDÉ : {{recommended}}

## 📊 TABLEAU COMPARATIF

| Feature | Produit A | **{{recommended}}** ⭐ | Produit C |
|---------|-----------|------------------------|-----------|
| Prix | X€ | **X€** | X€ |
{{#each features}}
| {{this}} | [✅/❌/Valeur] | [✅/❌/Valeur] | [✅/❌/Valeur] |
{{/each}}

**Notre choix :** {{recommended}} - [Raison en 1 ligne]

[CTA : Voir {{recommended}}]`
  },

  'size-guide-generator': {
    fields: [
      { name: 'product_type', type: 'select', label: 'Type de produit', required: true, options: ['Vêtements femme', 'Vêtements homme', 'Chaussures', 'Accessoires', 'Enfant'] },
      { name: 'brand_sizing', type: 'select', label: 'Taillant', options: ['Normal', 'Petit (prendre 1 taille au-dessus)', 'Grand (prendre 1 taille en-dessous)'] },
      { name: 'measurements', type: 'textarea', label: 'Mesures spécifiques', placeholder: 'Mesures particulières à votre produit' },
    ],
    promptTemplate: `Génère un guide des tailles professionnel.

TYPE : {{product_type}}
TAILLANT : {{brand_sizing}}
MESURES : {{measurements}}

## 📏 GUIDE DES TAILLES - {{product_type}}

### Comment prendre vos mesures

1. **Tour de poitrine** : Mesurez horizontalement à l'endroit le plus fort
2. **Tour de taille** : Mesurez au niveau du nombril
3. **Tour de hanches** : Mesurez à l'endroit le plus large

### Tableau des tailles

| Taille | Tour poitrine | Tour taille | Tour hanches |
|--------|--------------|-------------|--------------|
| XS (34-36) | 82-86 cm | 62-66 cm | 88-92 cm |
| S (38) | 86-90 cm | 66-70 cm | 92-96 cm |
| M (40) | 90-94 cm | 70-74 cm | 96-100 cm |
| L (42) | 94-98 cm | 74-78 cm | 100-104 cm |
| XL (44) | 98-102 cm | 78-82 cm | 104-108 cm |

### Note sur le taillant

⚠️ {{brand_sizing}}

### Besoin d'aide ?

Contactez-nous à [email] - Nous vous aiderons à trouver votre taille !`
  },

  'product-qa-generator': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
      { name: 'product_features', type: 'textarea', label: 'Caractéristiques du produit' },
      { name: 'common_concerns', type: 'textarea', label: 'Préoccupations courantes des clients' },
    ],
    promptTemplate: `Génère des Q&A produit optimisées.

PRODUIT : {{product_name}}
FEATURES : {{product_features}}
PRÉOCCUPATIONS : {{common_concerns}}

## ❓ Q&A - {{product_name}}

### Questions fréquentes

**Q : [Question sur les dimensions/taille] ?**
R : [Réponse détaillée avec mesures exactes]

**Q : [Question sur les matériaux/composition] ?**
R : [Réponse avec détails qualité]

**Q : [Question sur l'utilisation] ?**
R : [Réponse avec instructions/conseils]

**Q : [Question sur la compatibilité] ?**
R : [Réponse claire]

**Q : [Question sur l'entretien] ?**
R : [Instructions d'entretien]

**Q : Ce produit est-il garanti ?**
R : Oui, [détails garantie]

**Q : [Question de la préoccupation 1] ?**
R : [Réponse rassurante]

---

### Questions à anticiper

- [Question potentielle 1]
- [Question potentielle 2]
- [Question potentielle 3]`
  },

  'inventory-alert-copy': {
    fields: [
      { name: 'alert_type', type: 'select', label: 'Type d\'alerte', required: true, options: ['Stock bas', 'Dernières pièces', 'Rupture imminente', 'Back in stock', 'Précommande'] },
      { name: 'product_name', type: 'text', label: 'Produit concerné' },
      { name: 'stock_level', type: 'text', label: 'Niveau de stock', placeholder: 'Ex: 3, <10...' },
    ],
    promptTemplate: `Génère des alertes stock créant l'urgence.

TYPE : {{alert_type}}
PRODUIT : {{product_name}}
STOCK : {{stock_level}}

## ⚠️ ALERTES STOCK

{{#if alert_type === 'Stock bas'}}
### Badge produit
"⚠️ Plus que {{stock_level}} en stock !"

### Popup
"🔥 {{product_name}} part vite !
Seulement {{stock_level}} restants.
[BOUTON : Ajouter au panier]"

### Email
**Objet :** ⚠️ [Prénom], {{product_name}} est presque épuisé !
"Plus que {{stock_level}} disponibles..."
{{/if}}

{{#if alert_type === 'Back in stock'}}
### Email notification
**Objet :** 🎉 {{product_name}} est de retour !
"Bonne nouvelle ! L'article que vous attendiez est à nouveau disponible.
⚠️ Stock limité - Ne ratez pas votre chance !
[BOUTON : Commander maintenant]"
{{/if}}`
  },

  'gift-guide-generator': {
    fields: [
      { name: 'occasion', type: 'select', label: 'Occasion', required: true, options: ['Noël', 'Anniversaire', 'Fête des mères', 'Fête des pères', 'Saint-Valentin', 'Pendaison de crémaillère', 'Autre'] },
      { name: 'recipient', type: 'select', label: 'Pour qui', options: ['Femme', 'Homme', 'Enfant', 'Ado', 'Couple', 'Collègue', 'Tous'] },
      { name: 'budget_range', type: 'select', label: 'Budget', options: ['< 25€', '25-50€', '50-100€', '100-200€', '> 200€', 'Tous budgets'] },
      { name: 'products', type: 'textarea', label: 'Produits à inclure' },
    ],
    promptTemplate: `Génère un guide cadeaux engageant.

OCCASION : {{occasion}}
POUR : {{recipient}}
BUDGET : {{budget_range}}
PRODUITS : {{products}}

## 🎁 GUIDE CADEAUX {{occasion}} - Pour {{recipient}}

### Introduction

"Trouvez le cadeau parfait pour {{occasion}} ! Notre sélection pour {{recipient}} - Budget : {{budget_range}}"

---

### Nos coups de coeur

**1. [Produit A]** - [Prix]
"Idéal pour : [Type de personne]
Pourquoi on l'aime : [Raison]"
⭐ Bestseller

**2. [Produit B]** - [Prix]
"Idéal pour : [Type de personne]
Pourquoi on l'aime : [Raison]"

**3. [Produit C]** - [Prix]
"Idéal pour : [Type de personne]
Pourquoi on l'aime : [Raison]"
💡 Notre coup de coeur

---

### Par budget

**Moins de 25€**
- [Produit]
- [Produit]

**25-50€**
- [Produit]
- [Produit]

**50€ et plus**
- [Produit]
- [Produit]

---

### CTA

"Besoin d'aide pour choisir ? Contactez-nous !"
[BOUTON : Voir tous les cadeaux {{occasion}}]`
  },

  // ===== BATCH 3 - MOYENNE PRIORITÉ (5 outils) =====

  'supplier-email-template': {
    fields: [
      { name: 'email_type', type: 'select', label: 'Type d\'email', required: true, options: [
        { value: 'first_contact', label: '👋 Premier contact' },
        { value: 'quote_request', label: '💰 Demande de devis' },
        { value: 'price_negotiation', label: '📉 Négociation de prix' },
        { value: 'sample_request', label: '📦 Demande d\'échantillons' },
        { value: 'order_issue', label: '⚠️ Problème de commande' },
        { value: 'payment_terms', label: '💳 Conditions de paiement' }
      ]},
      { name: 'your_company', type: 'text', label: 'Votre entreprise', required: true },
      { name: 'supplier_name', type: 'text', label: 'Nom du fournisseur' },
      { name: 'product_interest', type: 'text', label: 'Produit(s) concerné(s)' },
      { name: 'order_volume', type: 'text', label: 'Volume de commande estimé' },
      { name: 'specific_request', type: 'textarea', label: 'Demande spécifique' },
    ],
    promptTemplate: `Tu es un acheteur professionnel expérimenté.

TYPE : {{email_type}}
VOTRE ENTREPRISE : {{your_company}}
FOURNISSEUR : {{supplier_name}}
PRODUIT : {{product_interest}}
VOLUME : {{order_volume}}
DEMANDE : {{specific_request}}

## 📧 EMAIL FOURNISSEUR

{{#if email_type === 'first_contact'}}
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

{{#if email_type === 'price_negotiation'}}
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

{{#if email_type === 'sample_request'}}
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

{{#if email_type === 'quote_request'}}
### Demande de Devis

**Objet :** Quote Request - {{product_interest}} - {{your_company}}

---

Dear [Name],

We are interested in placing an order for {{product_interest}}.

**Order details:**
- Product: {{product_interest}}
- Quantity: {{order_volume}}
- Delivery to: [Country/City]
- Required by: [Date]

Please provide:
1. Unit price for this quantity
2. Bulk pricing tiers
3. Shipping costs
4. Lead time
5. Payment terms

{{specific_request}}

Looking forward to your quote.

Best regards,
[Signature]
{{/if}}

---

### Versions FR/AR disponibles

**Version Française :**
[Même structure en français formel]

---

**Conseils négociation fournisseurs :**
✅ Toujours demander 3+ devis
✅ Négocier après échantillons validés
✅ Mentionner le volume potentiel futur
✅ Demander des conditions de paiement (30/60/90 jours)
✅ Ne jamais accepter le premier prix`
  },

  'wholesale-inquiry-response': {
    fields: [
      { name: 'inquiry_type', type: 'select', label: 'Type de demande', required: true, options: [
        { value: 'become_reseller', label: '🏪 Devenir revendeur' },
        { value: 'wholesale_pricing', label: '💰 Prix de gros' },
        { value: 'bulk_order', label: '📦 Commande en volume' },
        { value: 'private_label', label: '🏷️ Marque blanche' },
        { value: 'partnership', label: '🤝 Partenariat' }
      ]},
      { name: 'your_brand', type: 'text', label: 'Votre marque', required: true },
      { name: 'wholesale_terms', type: 'textarea', label: 'Vos conditions de gros (MOQ, remises...)' },
      { name: 'inquiry_details', type: 'textarea', label: 'Détails de la demande reçue' },
    ],
    promptTemplate: `Tu es un responsable commercial B2B.

TYPE : {{inquiry_type}}
MARQUE : {{your_brand}}
CONDITIONS : {{wholesale_terms}}
DEMANDE : {{inquiry_details}}

## 📧 RÉPONSE DEMANDE B2B

{{#if inquiry_type === 'become_reseller'}}
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

{{#if inquiry_type === 'private_label'}}
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

{{#if inquiry_type === 'wholesale_pricing'}}
### Réponse Demande Prix de Gros

**Objet :** RE: Demande de tarifs grossiste - {{your_brand}}

---

Bonjour [Nom],

Merci pour votre intérêt pour nos produits en gros !

**Nos conditions grossiste :**

{{wholesale_terms}}

📦 **Grille tarifaire :**
| Volume | Remise |
|--------|--------|
| 50-99 unités | -15% |
| 100-499 unités | -25% |
| 500+ unités | -35% |

📋 **Pour ouvrir un compte pro :**
1. Envoyez votre SIRET/Kbis
2. Validation sous 24-48h
3. Accès aux tarifs pro

Cordialement,
[Signature]
{{/if}}

---

**Templates réponses rapides :**

✅ **Accusé de réception :**
"Bonjour, merci pour votre demande. Notre équipe commerciale vous répondra sous 48h."

❌ **Refus poli :**
"Merci pour votre intérêt. Malheureusement, nous ne sommes pas en mesure de répondre favorablement à votre demande pour le moment. Nous vous souhaitons bonne continuation."`
  },

  'dropshipping-product-copy': {
    fields: [
      { name: 'supplier_description', type: 'textarea', label: 'Description fournisseur (AliExpress, etc.)', required: true },
      { name: 'product_images_count', type: 'number', label: 'Nombre d\'images disponibles' },
      { name: 'target_price', type: 'number', label: 'Prix de vente visé (€)' },
      { name: 'niche', type: 'text', label: 'Niche/Marché cible' },
      { name: 'brand_name', type: 'text', label: 'Nom de votre boutique' },
      { name: 'unique_angle', type: 'text', label: 'Angle de vente unique' },
    ],
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
- Ne pas mentir sur l'origine du produit`
  },

  'marketplace-listing-optimizer': {
    fields: [
      { name: 'marketplace', type: 'select', label: 'Marketplace', required: true, options: [
        { value: 'amazon', label: '🟠 Amazon' },
        { value: 'ebay', label: '🔵 eBay' },
        { value: 'etsy', label: '🟤 Etsy' },
        { value: 'cdiscount', label: '🔴 Cdiscount' },
        { value: 'fnac', label: '🟡 Fnac Marketplace' }
      ]},
      { name: 'current_listing', type: 'textarea', label: 'Listing actuel (titre + description)', required: true },
      { name: 'product_category', type: 'text', label: 'Catégorie du produit' },
      { name: 'target_keywords', type: 'text', label: 'Mots-clés cibles' },
      { name: 'competitors', type: 'textarea', label: 'Titres des concurrents (top 3)' },
    ],
    promptTemplate: `Tu es un expert en optimisation de listings marketplace.

MARKETPLACE : {{marketplace}}
LISTING ACTUEL : {{current_listing}}
CATÉGORIE : {{product_category}}
MOTS-CLÉS : {{target_keywords}}
CONCURRENTS : {{competitors}}

## 🏪 LISTING OPTIMISÉ {{marketplace | uppercase}}

{{#if marketplace === 'amazon'}}
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

{{#if marketplace === 'etsy'}}
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

{{#if marketplace === 'ebay'}}
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
| Images | X/25 | [Action] |`
  },

  'print-on-demand-description': {
    fields: [
      { name: 'product_type', type: 'select', label: 'Type de produit', required: true, options: [
        { value: 'tshirt', label: '👕 T-shirt' },
        { value: 'hoodie', label: '🧥 Sweat/Hoodie' },
        { value: 'mug', label: '☕ Mug' },
        { value: 'poster', label: '🖼️ Poster/Affiche' },
        { value: 'phone_case', label: '📱 Coque de téléphone' },
        { value: 'tote_bag', label: '👜 Tote bag' },
        { value: 'sticker', label: '🏷️ Sticker' },
        { value: 'cushion', label: '🛋️ Coussin' }
      ]},
      { name: 'design_description', type: 'textarea', label: 'Description du design', required: true },
      { name: 'design_theme', type: 'text', label: 'Thème/Niche', placeholder: 'Humour, Gaming, Motivation...' },
      { name: 'target_audience', type: 'text', label: 'Audience cible' },
      { name: 'platform', type: 'select', label: 'Plateforme POD', options: [
        { value: 'redbubble', label: 'Redbubble' },
        { value: 'teepublic', label: 'TeePublic' },
        { value: 'spreadshirt', label: 'Spreadshirt' },
        { value: 'printful', label: 'Printful' },
        { value: 'merch_by_amazon', label: 'Merch by Amazon' },
        { value: 'etsy', label: 'Etsy POD' }
      ]},
    ],
    promptTemplate: `Tu es un expert en Print-on-Demand et marketing de niche.

PRODUIT : {{product_type}}
DESIGN : {{design_description}}
THÈME : {{design_theme}}
AUDIENCE : {{target_audience}}
PLATEFORME : {{platform}}

## 👕 FICHE PRODUIT POD

### TITRE (optimisé SEO)

{{#if product_type === 'tshirt'}}
**Format Merch by Amazon :**
"[Design Theme] [Descripteur] T-Shirt | [Occasion/Pour qui] | [Style] Tee"

**Format Etsy :**
"[Design] Shirt, [Theme] T-shirt, [Occasion] Gift, [Audience] Tee, [Style] Top"

**Format Redbubble :**
"[Design Description] - [Theme] [Audience]"
{{/if}}

{{#if product_type === 'mug'}}
"[Design] Mug, [Theme] Coffee Cup, [Occasion] Gift for [Audience], [Adjectif] Tea Mug"
{{/if}}

{{#if product_type === 'hoodie'}}
"[Design] Hoodie, [Theme] Sweatshirt, [Occasion] Gift, Unisex [Style] Pullover"
{{/if}}

---

### DESCRIPTION

**Version courte (150 mots) :**

"🎨 **[Accroche liée au design]**

Le cadeau parfait pour {{target_audience}} !

Ce {{product_type}} [description du design] est idéal pour :
✨ [Occasion 1]
✨ [Occasion 2]
✨ [Occasion 3]

**Qualité premium :**
{{#if product_type === 'tshirt'}}
- 100% coton peigné (ou mélange selon modèle)
- Impression DTG haute qualité
- Coupe unisexe confortable
- Lavable en machine
{{/if}}
{{#if product_type === 'mug'}}
- Céramique de haute qualité
- Impression sublimation (ne s'efface pas)
- Compatible lave-vaisselle et micro-ondes
- Contenance : 11oz / 15oz
{{/if}}
{{#if product_type === 'hoodie'}}
- 80% coton, 20% polyester
- Doublure polaire intérieure
- Capuche avec cordon
- Impression durable
{{/if}}

🎁 **Idée cadeau parfaite** pour anniversaire, Noël, fête des pères/mères !

[CTA]"

---

### TAGS/MOTS-CLÉS (15)

{{#if platform === 'redbubble' || platform === 'teepublic'}}
1. [Tag principal - thème]
2. [Tag design]
3. [Tag audience]
4. [Tag occasion]
5. [Tag style]
6-15. [Tags variés et synonymes]
{{/if}}

{{#if platform === 'merch_by_amazon'}}
**Bullet Points (2) :**
- [Bénéfice 1 avec mots-clés]
- [Bénéfice 2 avec mots-clés]
{{/if}}

---

### DÉCLINAISONS SUGGÉRÉES

**Couleurs populaires pour ce design :**
{{#if product_type === 'tshirt'}}
- Noir, Blanc, Gris chiné, Navy, Rouge
{{/if}}
{{#if product_type === 'mug'}}
- Blanc, Noir
{{/if}}

**Produits complémentaires :**
- [Suggestion 1 - autre produit même design]
- [Suggestion 2]

---

### CONSEILS POD

✅ **Meilleures pratiques :**
- Uploader sur plusieurs plateformes
- Tester différentes niches
- Analyser les tendances saisonnières
- Utiliser des mockups de qualité

📊 **Niches rentables :**
- [Niche 1 liée au thème]
- [Niche 2]
- [Niche 3]

**Pricing suggéré :**
- T-shirt : 19-29€
- Mug : 12-18€
- Poster : 15-35€
- Hoodie : 35-55€`
  },
};

// Config par défaut
const defaultFormConfig: FormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez générer...' },
    { name: 'product_type', type: 'text', label: 'Type de produit' },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Casual', 'Luxe', 'Technique'] },
  ],
  promptTemplate: `Génère du contenu e-commerce basé sur cette demande...`
};

export default function EcommerceToolPage({ params }: PageProps) {
  const tool = ecommerceTools.find(t => t.slug === params.toolSlug);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [result, setResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!tool) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Outil non trouvé</h1>
          <p className="text-gray-500 mb-4">L'outil "{params.toolSlug}" n'existe pas.</p>
          <Link href="/tools/ecommerce" className="text-green-600 hover:underline">
            Retour aux outils E-commerce
          </Link>
        </div>
      </div>
    );
  }

  const formConfig = toolFormConfigs[tool.slug] || defaultFormConfig;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult('');

    setTimeout(() => {
      const mockResult = `# Résultat généré par ${tool.name.fr}

## Contenu Généré

${Object.entries(formData).map(([key, value]) => `**${key}**: ${value}`).join('\n')}

---

### Résultat Principal

Ce contenu a été généré par l'IA d'IAFactory Algeria pour optimiser votre e-commerce.

### Points Clés

1. **Conversion optimisée** : Copy testé pour maximiser les ventes
2. **SEO-friendly** : Optimisé pour les moteurs de recherche
3. **Multi-plateforme** : Adapté à Shopify, Amazon, WooCommerce...

### Prochaines Étapes

- Personnalisez le contenu avec vos informations
- Testez A/B différentes versions
- Analysez les métriques de conversion

---
*Généré avec ${tool.credits} crédits • ${new Date().toLocaleDateString('fr-FR')}*`;

      setResult(mockResult);
      setIsLoading(false);
    }, 2500);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFieldChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools/ecommerce" className="text-gray-400 hover:text-gray-600">
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

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Tool Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 bg-green-100 rounded-xl flex items-center justify-center">
              <ShoppingCart className="w-7 h-7 text-green-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
              <p className="text-gray-600 mt-1">{tool.description.fr}</p>
              <div className="flex items-center gap-3 mt-3">
                <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-sm font-medium">
                  {tool.credits} crédits
                </span>
                {tool.priority === 'critical' && (
                  <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-sm font-medium">
                    🔥 Essentiel
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-green-500" />
              Paramètres
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
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
                      required={field.required}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    />
                  )}
                  {field.type === 'textarea' && (
                    <textarea
                      placeholder={field.placeholder}
                      required={field.required}
                      rows={3}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    />
                  )}
                  {field.type === 'select' && (
                    <select
                      required={field.required}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    >
                      <option value="">Sélectionner...</option>
                      {field.options?.map((opt) => (
                        <option key={typeof opt === 'string' ? opt : opt.value} value={typeof opt === 'string' ? opt : opt.value}>
                          {typeof opt === 'string' ? opt : opt.label}
                        </option>
                      ))}
                    </select>
                  )}
                  {field.type === 'number' && (
                    <input
                      type="number"
                      placeholder={field.placeholder}
                      required={field.required}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    />
                  )}
                  {field.type === 'checkbox' && (
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formData[field.name] === 'true'}
                        onChange={(e) => handleFieldChange(field.name, e.target.checked ? 'true' : 'false')}
                        className="w-4 h-4 text-green-600 rounded focus:ring-green-500"
                      />
                      <span className="text-sm text-gray-600">{field.label}</span>
                    </label>
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Générer ({tool.credits} crédits)
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Result */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Résultat</h2>
              {result && (
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4 text-green-600" />
                      Copié !
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copier
                    </>
                  )}
                </button>
              )}
            </div>
            {result ? (
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-lg overflow-auto max-h-[600px]">
                  {result}
                </pre>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <ShoppingCart className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Le résultat apparaîtra ici</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
