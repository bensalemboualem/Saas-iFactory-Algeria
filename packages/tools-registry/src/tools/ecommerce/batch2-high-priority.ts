import { AITool } from '../../types';

export const priceComparisonCopy: AITool = {
  id: 'price-comparison-copy',
  slug: 'price-comparison-copy',
  name: { fr: 'Copy Comparatif de Prix', ar: 'نص مقارنة الأسعار', en: 'Price Comparison Copy' },
  description: {
    fr: 'Créez des comparatifs de prix convaincants qui justifient votre valeur',
    ar: 'أنشئ مقارنات أسعار مقنعة تبرر قيمتك',
    en: 'Create convincing price comparisons that justify your value'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'Scale',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'your_product', type: 'text', label: 'Votre produit', required: true },
    { name: 'your_price', type: 'number', label: 'Votre prix' },
    { name: 'competitor_products', type: 'textarea', label: 'Produits concurrents + prix' },
    { name: 'your_advantages', type: 'textarea', label: 'Vos avantages uniques' },
    { name: 'comparison_angle', type: 'select', label: 'Angle de comparaison', options: [
      'Meilleur rapport qualité/prix',
      'Premium justifié',
      'Option économique',
      'Plus de fonctionnalités'
    ]}
  ],
  outputs: [{ type: 'markdown', name: 'comparison' }],
  promptTemplate: `Tu es un expert en copywriting de conversion.

PRODUIT : {{your_product}}
PRIX : {{your_price}}
CONCURRENTS : {{competitor_products}}
AVANTAGES : {{your_advantages}}
ANGLE : {{comparison_angle}}

## ⚖️ COPY COMPARATIF DE PRIX

### Version 1 : Tableau comparatif

**Headline :** "Pourquoi payer plus... ou moins ?"

| Caractéristique | {{your_product}} | Concurrent A | Concurrent B |
|-----------------|------------------|--------------|--------------|
| Prix | {{your_price}} ✅ | [Prix A] | [Prix B] |
| [Feature 1] | ✅ | ❌ | ✅ |
| [Feature 2] | ✅ | ✅ | ❌ |
| [Feature 3] | ✅ | ❌ | ❌ |
| **Verdict** | **Meilleur choix** | [Verdict] | [Verdict] |

---

### Version 2 : Storytelling valeur

"**[Concurrent] = {{prix_concurrent}}**
*Mais sans [avantage 1], sans [avantage 2], et avec [inconvénient].*

**{{your_product}} = {{your_price}}**
*Avec [avantage 1], [avantage 2], ET [avantage 3].*

Faites le calcul. 🧮"

---

### Version 3 : Calcul ROI

"**Le vrai coût de [concurrent] :**
- Prix d'achat : X€
- + [Coût caché 1] : X€
- + [Coût caché 2] : X€
- **= Total réel : X€**

**{{your_product}} :**
- Tout inclus : {{your_price}}
- **Économie : X€** ✅"

---

### Version 4 : Social proof

"**92% de nos clients ont essayé [concurrent] avant.**
Voici pourquoi ils ont changé :

💬 '[Témoignage sur la valeur]' - [Client]"

---

**Placements suggérés :**
- Page produit (section dédiée)
- Landing page comparatif
- Email marketing
- Publicités retargeting`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const productLaunchCopy: AITool = {
  id: 'product-launch-copy',
  slug: 'product-launch-copy',
  name: { fr: 'Copy Lancement Produit', ar: 'نص إطلاق المنتج', en: 'Product Launch Copy' },
  description: {
    fr: 'Créez tous les textes pour un lancement produit réussi',
    ar: 'أنشئ جميع النصوص لإطلاق منتج ناجح',
    en: 'Create all copy for a successful product launch'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'Rocket',
  credits: 25,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
    { name: 'product_description', type: 'textarea', label: 'Description du produit' },
    { name: 'launch_date', type: 'text', label: 'Date de lancement' },
    { name: 'launch_offer', type: 'text', label: 'Offre de lancement', placeholder: '-20% early bird...' },
    { name: 'target_audience', type: 'text', label: 'Audience cible' },
    { name: 'problem_solved', type: 'textarea', label: 'Problème résolu' }
  ],
  outputs: [{ type: 'markdown', name: 'launch_copy' }],
  promptTemplate: `Tu es un expert en lancement de produits e-commerce.

PRODUIT : {{product_name}}
DESCRIPTION : {{product_description}}
DATE : {{launch_date}}
OFFRE : {{launch_offer}}
AUDIENCE : {{target_audience}}
PROBLÈME : {{problem_solved}}

## 🚀 KIT COMPLET LANCEMENT PRODUIT

### 1. TEASER (J-7)

**Email Teaser :**
Objet : "Quelque chose d'ÉNORME arrive le {{launch_date}}... 👀"

"[Prénom],

On prépare quelque chose de spécial depuis des mois...

Le {{launch_date}}, tout change pour [audience cible].

Indice : [teaser mystérieux]

Restez connecté.

[Signature]

P.S. Les premiers à répondre à cet email auront une surprise... 🎁"

---

**Post Social Teaser :**
"⏰ Countdown activé.

[Date]. [Heure].

Quelque chose arrive qui va [bénéfice].

🔔 Activez les notifs pour ne pas rater ça."

---

### 2. ANNONCE JOUR J

**Email Lancement :**
Objet : "🚀 C'EST LIVE ! Découvrez {{product_name}}"

"[Prénom],

Le jour est arrivé ! 🎉

**Présentation de {{product_name}}** - [tagline produit]

[Paragraphe problème/solution]

**Ce que vous obtenez :**
✅ [Bénéfice 1]
✅ [Bénéfice 2]
✅ [Bénéfice 3]

**🎁 OFFRE DE LANCEMENT :**
{{launch_offer}} - Valable jusqu'au [date fin]

[BOUTON : Découvrir maintenant]

[Signature]"

---

**Post Social Lancement :**
"🚀 **C'EST OFFICIEL !**

Après [X] mois de travail, {{product_name}} est enfin disponible !

[Description courte]

🎁 **Offre lancement :** {{launch_offer}}
⏰ **Jusqu'au :** [Date]

Lien en bio 👆

#launch #nouveau #[niche]"

---

### 3. RELANCES

**Email J+2 :**
Objet : "Plus que [X] jours pour l'offre de lancement..."

**Email J+5 (Dernier jour) :**
Objet : "⏰ DERNIÈRES HEURES - {{launch_offer}} expire à minuit"

---

### 4. PAGE PRODUIT

**Headline :** "[Bénéfice principal] - Enfin disponible"
**Subheadline :** "[Problème] ? {{product_name}} est la solution."

[Contenu page produit optimisé]

---

### 📅 CALENDRIER LANCEMENT

| Jour | Action | Canal |
|------|--------|-------|
| J-7 | Teaser mystère | Email + Social |
| J-3 | Reveal partiel | Story + Email |
| J-1 | Countdown | Tous canaux |
| J | Lancement | Tous canaux |
| J+2 | Rappel | Email |
| J+5 | Urgence finale | Email + Social |`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const seasonalPromotionGenerator: AITool = {
  id: 'seasonal-promotion-generator',
  slug: 'seasonal-promotion-generator',
  name: { fr: 'Générateur Promos Saisonnières', ar: 'مولد العروض الموسمية', en: 'Seasonal Promotion Generator' },
  description: {
    fr: 'Créez des campagnes pour Black Friday, Soldes, Noël et toutes les occasions',
    ar: 'أنشئ حملات للجمعة السوداء والتخفيضات وعيد الميلاد',
    en: 'Create campaigns for Black Friday, Sales, Christmas and all occasions'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'Calendar',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'occasion', type: 'select', label: 'Occasion', required: true, options: [
      'Black Friday',
      'Cyber Monday',
      'Noël',
      'Nouvel An',
      'Saint-Valentin',
      'Fête des Mères',
      'Fête des Pères',
      'Soldes d\'été',
      'Soldes d\'hiver',
      'Rentrée',
      'Ramadan',
      'Aïd'
    ]},
    { name: 'discount', type: 'text', label: 'Réduction/Offre', required: true },
    { name: 'duration', type: 'text', label: 'Durée de l\'offre' },
    { name: 'products', type: 'text', label: 'Produits concernés' },
    { name: 'brand_name', type: 'text', label: 'Nom de la marque' }
  ],
  outputs: [{ type: 'markdown', name: 'promotion' }],
  promptTemplate: `Tu es un expert en marketing saisonnier e-commerce.

OCCASION : {{occasion}}
RÉDUCTION : {{discount}}
DURÉE : {{duration}}
PRODUITS : {{products}}
MARQUE : {{brand_name}}

## 🎉 CAMPAGNE {{occasion | uppercase}}

### EMAILS (3)

{{#if occasion === 'Black Friday'}}
**Email 1 - Teaser (J-3) :**
Objet : "🖤 Le Black Friday {{brand_name}} arrive... Préparez-vous"

"[Prénom],

Dans 3 jours, les prix s'effondrent. 📉

**{{discount}}** sur [produits]

Mais attention : stocks limités.

Ajoutez vos favoris au panier maintenant 👇

[BOUTON]"

---

**Email 2 - Jour J :**
Objet : "🖤 BLACK FRIDAY : {{discount}} - C'EST MAINTENANT !"

---

**Email 3 - Dernières heures :**
Objet : "⏰ Minuit = Fin du Black Friday. Dernière chance."
{{/if}}

{{#if occasion === 'Ramadan'}}
**Email 1 - Début Ramadan :**
Objet : "🌙 Ramadan Moubarak ! Notre offre spéciale"

"Salam [Prénom],

À l'occasion du mois sacré du Ramadan, {{brand_name}} vous offre {{discount}}.

[Contenu adapté]

Ramadan Kareem 🌙"
{{/if}}

---

### POSTS SOCIAUX

**Post Annonce :**
"{{#if occasion === 'Black Friday'}}🖤{{/if}} **{{occasion | uppercase}}**

{{discount}} sur {{products}} !

⏰ {{duration}}

Lien en bio 🔗

#BlackFriday #Promo #{{brand_name}}"

---

**Story avec countdown :**
[Sticker compte à rebours]
"Plus que [X] heures !"

---

### BANNIÈRE SITE

**Texte bannière :**
"🖤 BLACK FRIDAY : {{discount}} | Code : BLACKFRIDAY | Jusqu'au [date]"

---

### POPUP

**Titre :** "🖤 OFFRE BLACK FRIDAY"
**Corps :** "{{discount}} sur tout le site !"
**CTA :** "J'en profite"
**Code :** [CODE]

---

### SMS (160 caractères)

"{{brand_name}} : BLACK FRIDAY {{discount}} ! Rdv sur [lien court]. Offre valable {{duration}}. STOP au XXXXX"`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const loyaltyProgramCopy: AITool = {
  id: 'loyalty-program-copy',
  slug: 'loyalty-program-copy',
  name: { fr: 'Copy Programme Fidélité', ar: 'نص برنامج الولاء', en: 'Loyalty Program Copy' },
  description: {
    fr: 'Créez tous les textes pour votre programme de fidélité',
    ar: 'أنشئ جميع نصوص برنامج الولاء',
    en: 'Create all copy for your loyalty program'
  },
  category: 'ecommerce',
  subcategory: 'customer_service',
  icon: 'Award',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'program_name', type: 'text', label: 'Nom du programme', required: true },
    { name: 'brand_name', type: 'text', label: 'Nom de la marque' },
    { name: 'points_system', type: 'textarea', label: 'Système de points (1€ = X points...)' },
    { name: 'rewards', type: 'textarea', label: 'Récompenses disponibles' },
    { name: 'tiers', type: 'textarea', label: 'Niveaux (Bronze, Silver, Gold...)' }
  ],
  outputs: [{ type: 'markdown', name: 'loyalty_copy' }],
  promptTemplate: `Tu es un expert en fidélisation client.

PROGRAMME : {{program_name}}
MARQUE : {{brand_name}}
POINTS : {{points_system}}
RÉCOMPENSES : {{rewards}}
NIVEAUX : {{tiers}}

## 🏆 PROGRAMME FIDÉLITÉ {{program_name}}

### PAGE DE PRÉSENTATION

**Headline :** "Rejoignez {{program_name}} et soyez récompensé à chaque achat"

**Introduction :**
"Chez {{brand_name}}, votre fidélité compte. C'est pourquoi nous avons créé {{program_name}} - un programme qui vous remercie d'être là.

**Comment ça marche ?**

1️⃣ **Inscrivez-vous** (gratuit !)
2️⃣ **Gagnez des points** à chaque achat
3️⃣ **Échangez** contre des récompenses exclusives

---

**💎 SYSTÈME DE POINTS**

{{points_system}}

| Action | Points gagnés |
|--------|---------------|
| 1€ dépensé | X points |
| Parrainage | X points |
| Anniversaire | X points |
| Avis produit | X points |

---

**🎁 VOS RÉCOMPENSES**

| Points | Récompense |
|--------|------------|
| X pts | [Récompense 1] |
| X pts | [Récompense 2] |
| X pts | [Récompense 3] |

---

**⭐ NIVEAUX DE FIDÉLITÉ**

| Niveau | Condition | Avantages |
|--------|-----------|-----------|
| 🥉 Bronze | Inscription | [Avantages] |
| 🥈 Silver | X points | [Avantages] |
| 🥇 Gold | X points | [Avantages] |
| 💎 Platinum | X points | [Avantages VIP] |"

---

### EMAILS DU PROGRAMME

**Email Bienvenue :**
Objet : "Bienvenue dans {{program_name}} ! 🎉 Voici vos premiers points"

**Email Points gagnés :**
Objet : "Vous avez gagné X points ! 🏆"

**Email Niveau atteint :**
Objet : "Félicitations ! Vous êtes maintenant [Niveau] 🌟"

**Email Récompense disponible :**
Objet : "Vous pouvez échanger vos points ! 🎁"

---

### FAQ PROGRAMME

**Q : Le programme est-il gratuit ?**
R : Oui, l'inscription est 100% gratuite !

**Q : Mes points expirent-ils ?**
R : [Politique d'expiration]

**Q : Comment utiliser mes points ?**
R : [Instructions]`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const cartAbandonmentPopup: AITool = {
  id: 'cart-abandonment-popup',
  slug: 'cart-abandonment-popup',
  name: { fr: 'Popups Abandon de Panier', ar: 'نوافذ التخلي عن السلة', en: 'Cart Abandonment Popups' },
  description: {
    fr: 'Créez des popups exit-intent qui sauvent les ventes',
    ar: 'أنشئ نوافذ تنقذ المبيعات',
    en: 'Create exit-intent popups that save sales'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'ShoppingCart',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'popup_type', type: 'select', label: 'Type de popup', options: [
      'Offrir une réduction',
      'Livraison gratuite',
      'Urgence/Stock',
      'Rappel par email',
      'Preuve sociale'
    ]},
    { name: 'offer', type: 'text', label: 'Offre à proposer', placeholder: '-10%, Livraison offerte...' },
    { name: 'brand_voice', type: 'select', options: ['Professionnel', 'Amical', 'Urgent', 'Humoristique'] }
  ],
  outputs: [{ type: 'markdown', name: 'popup' }],
  promptTemplate: `Tu es un expert en optimisation de conversion e-commerce.

TYPE : {{popup_type}}
OFFRE : {{offer}}
TON : {{brand_voice}}

## 🛒 POPUPS ABANDON DE PANIER

{{#if popup_type.includes('réduction')}}
### Popup Réduction

**Design suggéré :** Centré, fond overlay sombre

**Titre :** "Attendez ! 🛑"
**Sous-titre :** "Votre panier se sent abandonné..."
**Corps :** "On vous offre **{{offer}}** pour finaliser votre commande !"
**Code promo :** [CODE]
**CTA principal :** "Appliquer et continuer"
**CTA secondaire :** "Non merci, je paierai plein tarif"
**Timer :** "Offre valable 15 minutes"
{{/if}}

{{#if popup_type.includes('Livraison')}}
### Popup Livraison Gratuite

**Titre :** "Plus que X€ pour la livraison GRATUITE ! 🚚"
**Corps :** "Ajoutez [montant] à votre panier et économisez [frais de port]."
**Barre de progression :** [###------] X€ / Y€
**CTA :** "Voir les suggestions"
**Suggestions :** [3 produits < montant manquant]
{{/if}}

{{#if popup_type.includes('Urgence')}}
### Popup Urgence

**Titre :** "⚠️ Stock limité !"
**Corps :** "[Produit X] dans votre panier n'est plus qu'en [X] exemplaires."
**Sous-texte :** "[X] personnes regardent ce produit en ce moment"
**CTA :** "Finaliser ma commande"
{{/if}}

{{#if popup_type.includes('Rappel')}}
### Popup Rappel Email

**Titre :** "Gardez votre panier ! 📧"
**Corps :** "Entrez votre email et on vous l'envoie pour plus tard."
**Input :** [Email]
**CTA :** "Recevoir mon panier"
**Mention RGPD :** "Nous ne spammons jamais."
{{/if}}

{{#if popup_type.includes('Preuve')}}
### Popup Preuve Sociale

**Titre :** "[Prénom] vient d'acheter ça ! 🛍️"
**Corps :** "[X] personnes ont acheté ce produit aujourd'hui"
**Avis :** ⭐⭐⭐⭐⭐ "[Avis court]"
**CTA :** "Finaliser comme eux"
{{/if}}

---

### VARIANTES A/B À TESTER

| Version | Élément testé | Hypothèse |
|---------|--------------|-----------|
| A | Offre {{offer}} | Conversion par incentive |
| B | Sans offre (urgence) | Conversion par FOMO |
| C | Email capture | Récupération ultérieure |

---

**Timing recommandé :**
- Exit intent : Quand souris quitte la fenêtre
- Inactivité : Après 30-60 secondes sans action
- Scroll : Au scroll vers le haut`,
  model: 'gpt4',
  estimatedTime: '25s'
};

export const productComparisonTable: AITool = {
  id: 'product-comparison-table',
  slug: 'product-comparison-table',
  name: { fr: 'Tableau Comparatif Produits', ar: 'جدول مقارنة المنتجات', en: 'Product Comparison Table' },
  description: {
    fr: 'Créez des tableaux comparatifs pour aider les clients à choisir',
    ar: 'أنشئ جداول مقارنة لمساعدة العملاء في الاختيار',
    en: 'Create comparison tables to help customers choose'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Table',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'products', type: 'textarea', label: 'Produits à comparer (nom, prix, specs)', required: true },
    { name: 'comparison_criteria', type: 'text', label: 'Critères de comparaison' },
    { name: 'highlight_product', type: 'text', label: 'Produit à mettre en avant (optionnel)' },
    { name: 'table_style', type: 'select', options: ['Detailed', 'Simple', 'Visual'] }
  ],
  outputs: [{ type: 'markdown', name: 'table' }],
  promptTemplate: `Tu es un expert e-commerce en aide à la décision.

PRODUITS : {{products}}
CRITÈRES : {{comparison_criteria}}
HIGHLIGHT : {{highlight_product}}
STYLE : {{table_style}}

## 📊 TABLEAU COMPARATIF

### Titre section
"**Quel [type de produit] choisir ?** Comparez nos modèles"

---

### Tableau détaillé

|  | [Produit A] | [Produit B] {{#if highlight_product}}⭐{{/if}} | [Produit C] |
|--|-------------|--------------|--------------|
| **Prix** | X€ | X€ | X€ |
| **[Critère 1]** | [Valeur] | [Valeur] ✅ | [Valeur] |
| **[Critère 2]** | [Valeur] | [Valeur] | [Valeur] ✅ |
| **[Critère 3]** | ❌ | ✅ | ✅ |
| **[Critère 4]** | [Valeur] | [Valeur] | [Valeur] |
| **Idéal pour** | [Profil] | [Profil] | [Profil] |
| **Notre avis** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
|  | [CTA] | **[CTA Highlight]** | [CTA] |

---

### Résumé rapide

"**En résumé :**
- 💰 **Meilleur rapport qualité/prix :** [Produit]
- 👑 **Le plus complet :** [Produit]
- 🎯 **Pour les débutants :** [Produit]"

---

### Guide de choix

"**Choisissez [Produit A] si :**
- Vous [critère 1]
- Vous [critère 2]

**Choisissez [Produit B] si :**
- Vous [critère 1]
- Vous [critère 2]"

---

**Code HTML/CSS suggéré :**
\`\`\`html
[Structure responsive du tableau]
\`\`\``,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const sizeGuideGenerator: AITool = {
  id: 'size-guide-generator',
  slug: 'size-guide-generator',
  name: { fr: 'Générateur Guide des Tailles', ar: 'مولد دليل المقاسات', en: 'Size Guide Generator' },
  description: {
    fr: 'Créez des guides des tailles clairs pour réduire les retours',
    ar: 'أنشئ أدلة مقاسات واضحة لتقليل المرتجعات',
    en: 'Create clear size guides to reduce returns'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'Ruler',
  credits: 12,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_type', type: 'select', label: 'Type de produit', required: true, options: [
      'Top (Hauts)',
      'Bas (Pantalons)',
      'Robes',
      'Chaussures',
      'Sous-vêtements',
      'Accessoires',
      'Enfants'
    ]},
    { name: 'size_system', type: 'select', label: 'Système de tailles', options: ['EU', 'US', 'UK', 'International'] },
    { name: 'brand_specific', type: 'textarea', label: 'Spécificités de vos tailles (taille grand/petit...)' },
    { name: 'include_measurements', type: 'boolean', label: 'Inclure les instructions de mesure' }
  ],
  outputs: [{ type: 'markdown', name: 'size_guide' }],
  promptTemplate: `Tu es un expert e-commerce mode.

TYPE : {{product_type}}
SYSTÈME : {{size_system}}
SPÉCIFICITÉS : {{brand_specific}}

## 📏 GUIDE DES TAILLES

{{#if product_type.includes('Top')}}
### Guide des tailles - Hauts

**Comment prendre vos mesures :**

1. **Tour de poitrine** : Mesurez horizontalement à l'endroit le plus fort
2. **Tour de taille** : Mesurez au niveau du nombril
3. **Longueur** : Du haut de l'épaule jusqu'en bas du vêtement

[IMAGE : Schéma avec points de mesure]

---

**Tableau des tailles :**

| Taille | Tour de poitrine | Tour de taille | Équivalence |
|--------|-----------------|----------------|-------------|
| XS | 82-86 cm | 62-66 cm | 34 EU |
| S | 86-90 cm | 66-70 cm | 36 EU |
| M | 90-94 cm | 70-74 cm | 38 EU |
| L | 94-98 cm | 74-78 cm | 40 EU |
| XL | 98-102 cm | 78-82 cm | 42 EU |
| XXL | 102-106 cm | 82-86 cm | 44 EU |

{{#if brand_specific}}
⚠️ **Note :** {{brand_specific}}
{{/if}}
{{/if}}

{{#if product_type.includes('Chaussures')}}
### Guide des tailles - Chaussures

**Comment mesurer votre pied :**
1. Posez votre pied sur une feuille de papier
2. Tracez le contour de votre pied
3. Mesurez la longueur du talon aux orteils

| EU | US Homme | US Femme | UK | Longueur (cm) |
|----|----------|----------|-----|---------------|
| 36 | 4 | 5.5 | 3.5 | 22.5 |
| 37 | 5 | 6.5 | 4.5 | 23.5 |
| 38 | 5.5 | 7 | 5 | 24 |
| ... | ... | ... | ... | ... |

💡 **Conseil :** Entre deux tailles ? Prenez la plus grande.
{{/if}}

---

### FAQ Tailles

**Q : Vos vêtements taillent-ils grand ou petit ?**
R : {{brand_specific}}

**Q : Je suis entre deux tailles, que faire ?**
R : [Recommandation]

**Q : Puis-je échanger si la taille ne convient pas ?**
R : [Politique d'échange]`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const productQaGenerator: AITool = {
  id: 'product-qa-generator',
  slug: 'product-qa-generator',
  name: { fr: 'Générateur Q&A Produit', ar: 'مولد أسئلة وأجوبة المنتج', en: 'Product Q&A Generator' },
  description: {
    fr: 'Créez des questions/réponses pour vos pages produit (style Amazon)',
    ar: 'أنشئ أسئلة وأجوبة لصفحات منتجاتك',
    en: 'Create Q&A for your product pages (Amazon style)'
  },
  category: 'ecommerce',
  subcategory: 'product',
  icon: 'MessageCircle',
  credits: 10,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
    { name: 'product_specs', type: 'textarea', label: 'Spécifications du produit' },
    { name: 'common_concerns', type: 'textarea', label: 'Préoccupations courantes des clients' },
    { name: 'category', type: 'text', label: 'Catégorie de produit' }
  ],
  outputs: [{ type: 'markdown', name: 'qa' }],
  promptTemplate: `Tu es un expert en expérience client e-commerce.

PRODUIT : {{product_name}}
SPECS : {{product_specs}}
PRÉOCCUPATIONS : {{common_concerns}}
CATÉGORIE : {{category}}

## ❓ Q&A PRODUIT (15 questions)

### Questions sur le produit

**Q : [Question sur une caractéristique clé] ?**
R : [Réponse détaillée et rassurante]
👍 X personnes ont trouvé cette réponse utile

---

**Q : [Question sur la compatibilité] ?**
R : [Réponse précise]

---

**Q : [Question sur les dimensions/taille] ?**
R : [Réponse avec mesures exactes]

---

### Questions sur l'utilisation

**Q : [Question sur l'installation/utilisation] ?**
R : [Instructions claires]

---

**Q : [Question sur l'entretien] ?**
R : [Conseils d'entretien]

---

### Questions sur l'achat

**Q : Ce produit est-il garanti ?**
R : [Politique de garantie]

---

**Q : Puis-je retourner le produit s'il ne me convient pas ?**
R : [Politique de retour]

---

**Q : Quand vais-je recevoir ma commande ?**
R : [Délais de livraison]

---

### Questions techniques

**Q : [Question technique spécifique] ?**
R : [Réponse technique accessible]

---

**Q : [Question sur les matériaux/composition] ?**
R : [Détails matériaux]

---

### Préoccupations courantes

{{common_concerns}}
**Q : [Concern] ?**
R : [Réponse rassurante]

---

**Schema FAQ JSON-LD :**
\`\`\`json
[Code pour SEO]
\`\`\``,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const inventoryAlertCopy: AITool = {
  id: 'inventory-alert-copy',
  slug: 'inventory-alert-copy',
  name: { fr: 'Alertes Stock & Rupture', ar: 'تنبيهات المخزون', en: 'Inventory Alert Copy' },
  description: {
    fr: 'Créez des messages d\'alerte stock pour créer l\'urgence',
    ar: 'أنشئ رسائل تنبيه المخزون لخلق الاستعجال',
    en: 'Create stock alert messages to create urgency'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'AlertTriangle',
  credits: 8,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'alert_type', type: 'select', label: 'Type d\'alerte', options: [
      'Stock faible',
      'Retour en stock',
      'Rupture de stock',
      'Précommande',
      'Dernières pièces'
    ]},
    { name: 'product_name', type: 'text', label: 'Nom du produit' },
    { name: 'stock_quantity', type: 'number', label: 'Quantité restante (si applicable)' }
  ],
  outputs: [{ type: 'markdown', name: 'alert' }],
  promptTemplate: `Tu es un expert en psychologie de la conversion.

TYPE : {{alert_type}}
PRODUIT : {{product_name}}
STOCK : {{stock_quantity}}

## 🚨 MESSAGES D'ALERTE STOCK

{{#if alert_type.includes('Stock faible')}}
### Alertes Stock Faible

**Badge produit :**
"⚠️ Plus que {{stock_quantity}} en stock !"

**Message page produit :**
"🔥 **Stock limité** - Seulement {{stock_quantity}} exemplaires disponibles. Commandez maintenant pour ne pas rater votre chance !"

**Popup urgence :**
"⏰ **Attention !**
{{product_name}} n'est plus qu'en {{stock_quantity}} exemplaires.
[X] personnes regardent ce produit en ce moment.
[Ajouter au panier]"

**Email alerte :**
Objet : "⚠️ {{product_name}} bientôt en rupture - Plus que {{stock_quantity}} !"
{{/if}}

{{#if alert_type.includes('Retour')}}
### Alertes Retour en Stock

**Email :**
Objet : "🎉 DE RETOUR ! {{product_name}} est à nouveau disponible"

"[Prénom],

Bonne nouvelle ! {{product_name}} est enfin de retour en stock !

Vous étiez [X] à l'attendre... ne traînez pas !

[BOUTON : Acheter maintenant]

⚠️ Attention, stock limité."

**SMS :**
"{{product_name}} est de retour ! 🎉 Disponible maintenant sur [lien]. Stock limité !"

**Push notification :**
"🔔 {{product_name}} est de retour ! Foncez avant rupture →"
{{/if}}

{{#if alert_type.includes('Rupture')}}
### Messages Rupture de Stock

**Badge produit :**
"❌ Rupture de stock"

**Message page :**
"Ce produit est actuellement indisponible.
📧 **Soyez prévenu dès son retour :**
[Input email] [M'alerter]"

**Email confirmation inscription :**
Objet : "Vous serez prévenu dès le retour de {{product_name}}"
{{/if}}

{{#if alert_type.includes('Précommande')}}
### Messages Précommande

**Badge :**
"📦 Précommande - Livraison [date]"

**Message :**
"Réservez le vôtre maintenant ! Livraison prévue le [date].
✅ Paiement à l'expédition
✅ Annulation gratuite"
{{/if}}

---

**Éléments visuels suggérés :**
- Couleur rouge/orange pour l'urgence
- Icône de flamme 🔥 ou alerte ⚠️
- Compteur de stock en temps réel
- Indicateur "X personnes regardent"`,
  model: 'gpt4',
  estimatedTime: '15s'
};

export const giftGuideGenerator: AITool = {
  id: 'gift-guide-generator',
  slug: 'gift-guide-generator',
  name: { fr: 'Générateur Guides Cadeaux', ar: 'مولد أدلة الهدايا', en: 'Gift Guide Generator' },
  description: {
    fr: 'Créez des guides cadeaux pour toutes les occasions',
    ar: 'أنشئ أدلة هدايا لجميع المناسبات',
    en: 'Create gift guides for all occasions'
  },
  category: 'ecommerce',
  subcategory: 'conversion',
  icon: 'Gift',
  credits: 15,
  priority: 'high',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'occasion', type: 'select', label: 'Occasion', options: [
      'Noël', 'Anniversaire', 'Fête des Mères', 'Fête des Pères', 'Saint-Valentin', 'Mariage', 'Naissance', 'Général'
    ]},
    { name: 'recipient', type: 'select', label: 'Pour qui', options: [
      'Femme', 'Homme', 'Enfant', 'Ado', 'Couple', 'Collègue', 'Ami', 'Parents'
    ]},
    { name: 'budget_ranges', type: 'text', label: 'Tranches de budget', placeholder: '<20€, 20-50€, 50-100€...' },
    { name: 'products_available', type: 'textarea', label: 'Produits de votre catalogue' }
  ],
  outputs: [{ type: 'markdown', name: 'guide' }],
  promptTemplate: `Tu es un personal shopper expert.

OCCASION : {{occasion}}
DESTINATAIRE : {{recipient}}
BUDGETS : {{budget_ranges}}
PRODUITS : {{products_available}}

## 🎁 GUIDE CADEAUX {{occasion | uppercase}}

### Introduction

"**Trouver le cadeau parfait pour {{recipient}} ?**
On a fait le travail pour vous ! Découvrez notre sélection [occasion] par budget."

---

### Par Budget

{{budget_ranges}}
#### 💰 [Budget]

**[Produit 1]** - [Prix]
"[Description courte + pourquoi c'est un bon cadeau]"
⭐ Idéal pour : [type de personne]
[BOUTON : Voir le produit]

**[Produit 2]** - [Prix]
"[Description]"
⭐ Idéal pour : [type de personne]

**[Produit 3]** - [Prix]
"[Description]"

---

### Par Personnalité

**🎨 Pour les créatifs :**
- [Produit] - [Prix]
- [Produit] - [Prix]

**💪 Pour les sportifs :**
- [Produit] - [Prix]

**📚 Pour les intellectuels :**
- [Produit] - [Prix]

**🌿 Pour les éco-responsables :**
- [Produit] - [Prix]

---

### Nos Coups de Cœur ❤️

"Les cadeaux qui font toujours plaisir :"

1. **[Produit star]** - [Prix]
   "[Pourquoi on l'adore]"

2. **[Produit star]** - [Prix]
   "[Pourquoi on l'adore]"

---

### Options Cadeau

🎀 **Emballage cadeau** : X€
📝 **Message personnalisé** : Gratuit
🚚 **Livraison express** : [Délai]
🎁 **Carte cadeau** : De X€ à X€

---

**CTA final :**
"Besoin d'aide ? Notre équipe est là pour vous conseiller 💬"`,
  model: 'gpt4',
  estimatedTime: '45s'
};
