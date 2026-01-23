import { AITool } from '../../types';

export const emailSubjectLineGenerator: AITool = {
  id: 'email-subject-line-generator',
  slug: 'email-subject-line-generator',
  name: { fr: 'Générateur d\'Objets Email', ar: 'مولد عناوين البريد', en: 'Email Subject Line Generator' },
  description: {
    fr: 'Créez des objets d\'email irrésistibles qui boostent vos taux d\'ouverture',
    ar: 'أنشئ عناوين بريد لا تقاوم تزيد معدلات الفتح',
    en: 'Create irresistible email subject lines that boost open rates'
  },
  category: 'email',
  subcategory: 'optimization',
  icon: 'Mail',
  credits: 8,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'email_topic', type: 'text', label: 'Sujet de l\'email', required: true },
    { name: 'email_type', type: 'select', label: 'Type d\'email', options: [
      'Newsletter',
      'Promotionnel',
      'Cold Email',
      'Relance',
      'Bienvenue',
      'Transactionnel'
    ]},
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Casual', 'Urgent', 'Curieux', 'Personnel'] },
    { name: 'include_emoji', type: 'boolean', label: 'Inclure des émojis' },
    { name: 'include_personalization', type: 'boolean', label: 'Inclure [Prénom]' },
    { name: 'industry', type: 'text', label: 'Secteur (optionnel)' }
  ],
  outputs: [{ type: 'markdown', name: 'subjects' }],
  promptTemplate: `Tu es un expert en email marketing avec des taux d'ouverture de 40%+.

SUJET : {{email_topic}}
TYPE : {{email_type}}
TON : {{tone}}
ÉMOJIS : {{include_emoji}}
PERSONNALISATION : {{include_personalization}}

## 📧 20 OBJETS D'EMAIL

### 🔥 Curiosité (5)
1. "[Objet qui crée un mystère]"
2. "{{#if include_personalization}}[Prénom], {{/if}}[Question intrigante]"
3. "[Début de phrase incomplète...]"
4. "Ce que personne ne vous dit sur [sujet]"
5. "J'ai une confession à vous faire..."

### ⏰ Urgence/FOMO (5)
6. "{{#if include_emoji}}⚠️ {{/if}}Dernier jour pour [offre]"
7. "Plus que [X] places disponibles"
8. "[Prénom], vous allez rater ça..."
9. "Offre flash : -[X]% pendant 24h"
10. "C'est maintenant ou jamais"

### 💡 Bénéfice direct (5)
11. "Comment [obtenir résultat] en [temps]"
12. "[X] façons de [résoudre problème]"
13. "Votre guide pour [objectif]"
14. "Le secret pour [bénéfice]"
15. "[Prénom], voici votre [ressource]"

### 🎯 Personnel/Conversationnel (5)
16. "Une question rapide..."
17. "J'ai pensé à vous"
18. "Vous avez 5 minutes ?"
19. "Entre nous..."
20. "Re: votre demande"

---

**Analyse des objets :**

| # | Objet | Caractères | Score estimé |
|---|-------|------------|--------------|
| 1 | [Objet] | X/50 | ⭐⭐⭐⭐⭐ |
| 2 | [Objet] | X/50 | ⭐⭐⭐⭐ |
...

**Règles d'or :**
✅ 30-50 caractères (idéal mobile)
✅ Personnalisation = +26% d'ouverture
✅ Émoji en début = +15% (selon audience)
✅ Éviter : SPAM, !!!, €€€, GRATUIT
✅ A/B tester systématiquement`,
  model: 'gpt4',
  estimatedTime: '20s'
};

export const coldEmailGenerator: AITool = {
  id: 'cold-email-generator',
  slug: 'cold-email-generator',
  name: { fr: 'Générateur Cold Email', ar: 'مولد البريد البارد', en: 'Cold Email Generator' },
  description: {
    fr: 'Rédigez des cold emails qui obtiennent des réponses',
    ar: 'اكتب رسائل بريد باردة تحصل على ردود',
    en: 'Write cold emails that get responses'
  },
  category: 'email',
  subcategory: 'outreach',
  icon: 'Send',
  credits: 15,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'recipient_role', type: 'text', label: 'Rôle du destinataire', required: true, placeholder: 'CEO, Directeur Marketing...' },
    { name: 'recipient_company', type: 'text', label: 'Entreprise cible' },
    { name: 'your_offer', type: 'textarea', label: 'Votre offre/proposition', required: true },
    { name: 'value_proposition', type: 'text', label: 'Bénéfice principal pour eux' },
    { name: 'social_proof', type: 'text', label: 'Preuve sociale (clients, résultats...)' },
    { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Meeting', 'Call', 'Reply', 'Demo', 'Resource'] },
    { name: 'email_length', type: 'select', label: 'Longueur', options: ['Ultra-short', 'Short', 'Medium'] }
  ],
  outputs: [{ type: 'markdown', name: 'email' }],
  promptTemplate: `Tu es un expert en cold outreach B2B avec 30%+ de taux de réponse.

CIBLE : {{recipient_role}} chez {{recipient_company}}
OFFRE : {{your_offer}}
BÉNÉFICE : {{value_proposition}}
PREUVE : {{social_proof}}
CTA : {{cta}}
LONGUEUR : {{email_length}}

## ❄️ 3 COLD EMAILS

### Email 1 : Ultra-personnalisé (AIDA)

**Objet :** [Objet personnalisé mentionnant l'entreprise]

---

Bonjour [Prénom],

[ATTENTION - 1 ligne personnalisée sur l'entreprise/la personne]

[INTÉRÊT - 1-2 lignes sur le problème que vous résolvez]

[DÉSIR - Preuve sociale ou résultat concret]
→ "Nous avons aidé [client similaire] à [résultat chiffré]"

[ACTION - CTA simple]
Seriez-vous disponible pour un appel de 15 min cette semaine ?

[Signature courte]

---

### Email 2 : Format PAS (Problem-Agitate-Solve)

**Objet :** [Question sur un problème connu]

---

Bonjour [Prénom],

**Problème :** [Question sur un problème que {{recipient_role}} rencontre]

**Agitation :** [Conséquences de ne pas résoudre ce problème]

**Solution :** [Votre offre en 1 phrase]

[Preuve sociale courte]

Un call de 15 min pour voir si ça peut vous aider ?

[Signature]

---

### Email 3 : Format "Before-After-Bridge"

**Objet :** Idée pour {{recipient_company}}

---

Bonjour [Prénom],

**Avant :** [Situation actuelle probable]
**Après :** [Situation idéale avec résultat]
**Le pont :** [Votre solution]

[CTA]

---

**Checklist Cold Email :**
✅ Max 100 mots (idéal : 50-75)
✅ 1 seul CTA clair
✅ Personnalisation visible
✅ Pas de pièces jointes
✅ Signature simple
✅ Relance J+3 et J+7`,
  model: 'gpt4',
  estimatedTime: '40s'
};

export const newsletterGenerator: AITool = {
  id: 'newsletter-generator',
  slug: 'newsletter-generator',
  name: { fr: 'Générateur de Newsletter', ar: 'مولد النشرة الإخبارية', en: 'Newsletter Generator' },
  description: {
    fr: 'Créez des newsletters engageantes que vos abonnés adorent lire',
    ar: 'أنشئ نشرات إخبارية جذابة يحب المشتركون قراءتها',
    en: 'Create engaging newsletters your subscribers love to read'
  },
  category: 'email',
  subcategory: 'content',
  icon: 'Newspaper',
  credits: 20,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'newsletter_name', type: 'text', label: 'Nom de la newsletter' },
    { name: 'main_topic', type: 'text', label: 'Sujet principal', required: true },
    { name: 'newsletter_type', type: 'select', label: 'Format', options: [
      'Curation (liens + commentaires)',
      'Éducatif (article long)',
      'Mixte (intro + liens + CTA)',
      'Personnel (réflexions)'
    ]},
    { name: 'sections', type: 'text', label: 'Sections à inclure (Intro, Article, Liens, Astuce...)' },
    { name: 'tone', type: 'select', options: ['Professionnel', 'Conversationnel', 'Humoristique', 'Inspirant'] },
    { name: 'word_count', type: 'select', label: 'Longueur', options: ['Court (300)', 'Moyen (600)', 'Long (1000)'] }
  ],
  outputs: [{ type: 'markdown', name: 'newsletter' }],
  promptTemplate: `Tu es un expert en newsletters avec 50%+ de taux d'ouverture.

NEWSLETTER : {{newsletter_name}}
SUJET : {{main_topic}}
FORMAT : {{newsletter_type}}
SECTIONS : {{sections}}
TON : {{tone}}

## 📰 NEWSLETTER COMPLÈTE

### OBJET + PREVIEW

**Objet :** [Objet accrocheur]
**Preview text :** [Texte qui complète l'objet - 90 car.]

---

### CONTENU

{{#if sections.includes('Intro')}}
**👋 INTRO**

Salut !

[Accroche personnelle ou actualité]

Dans cette édition :
- [Point 1]
- [Point 2]
- [Point 3]

C'est parti ! 👇

---
{{/if}}

{{#if sections.includes('Article')}}
**📖 ARTICLE PRINCIPAL**

## [Titre accrocheur]

[Contenu éducatif ou réflexion - 300-500 mots]

**À retenir :**
→ [Point clé 1]
→ [Point clé 2]
→ [Point clé 3]

---
{{/if}}

{{#if sections.includes('Liens')}}
**🔗 LIENS DE LA SEMAINE**

1. **[Titre]** - [Source]
   [1 ligne de commentaire]
   → [Lien]

2. **[Titre]** - [Source]
   [1 ligne de commentaire]
   → [Lien]

3. **[Titre]** - [Source]
   [1 ligne de commentaire]
   → [Lien]

---
{{/if}}

{{#if sections.includes('Astuce')}}
**💡 ASTUCE DE LA SEMAINE**

[Conseil actionnable en 2-3 phrases]

---
{{/if}}

{{#if sections.includes('Outil')}}
**🛠️ OUTIL DÉCOUVERTE**

**[Nom de l'outil]** - [Catégorie]
[Description courte + pourquoi c'est utile]
→ [Lien]

---
{{/if}}

{{#if sections.includes('Citation')}}
**💬 CITATION**

> "[Citation inspirante]"
> — [Auteur]

---
{{/if}}

{{#if sections.includes('CTA')}}
**🎯 AVANT DE PARTIR**

[CTA vers produit, service ou action]

[Bouton CTA]

---
{{/if}}

**OUTRO**

À [fréquence],
[Signature]

P.S. [Bonus ou teaser prochaine édition]

---

**Template prêt pour Mailchimp/ConvertKit :**
[Structure HTML suggérée]`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const emailSequenceGenerator: AITool = {
  id: 'email-sequence-generator',
  slug: 'email-sequence-generator',
  name: { fr: 'Générateur de Séquence Email', ar: 'مولد تسلسل البريد', en: 'Email Sequence Generator' },
  description: {
    fr: 'Créez des séquences email automatisées qui convertissent',
    ar: 'أنشئ تسلسلات بريد آلية تحول الزوار',
    en: 'Create automated email sequences that convert'
  },
  category: 'email',
  subcategory: 'automation',
  icon: 'GitBranch',
  credits: 30,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'sequence_type', type: 'select', label: 'Type de séquence', required: true, options: [
      'Welcome sequence (nouveaux inscrits)',
      'Nurture sequence (éducation)',
      'Launch sequence (lancement produit)',
      'Panier abandonné',
      'Onboarding (nouveaux clients)',
      'Ré-engagement (inactifs)'
    ]},
    { name: 'product_service', type: 'text', label: 'Produit/Service à promouvoir' },
    { name: 'sequence_length', type: 'select', label: 'Nombre d\'emails', options: ['3', '5', '7', '10'] },
    { name: 'main_cta', type: 'text', label: 'Action finale souhaitée' },
    { name: 'brand_voice', type: 'select', options: ['Professionnel', 'Amical', 'Expert', 'Inspirant'] }
  ],
  outputs: [{ type: 'markdown', name: 'sequence' }],
  promptTemplate: `Tu es un expert en email automation et funnel marketing.

TYPE : {{sequence_type}}
PRODUIT : {{product_service}}
LONGUEUR : {{sequence_length}} emails
CTA FINAL : {{main_cta}}
TON : {{brand_voice}}

## 📧 SÉQUENCE EMAIL ({{sequence_length}} emails)

{{#if sequence_type.includes('Welcome')}}
### WELCOME SEQUENCE

**Email 1 - J+0 (immédiat) : Bienvenue + Livraison**
Objet : "Bienvenue ! Voici [ce qui était promis]"

[Contenu : Remerciement + livraison du lead magnet + présentation rapide]

---

**Email 2 - J+1 : Votre histoire**
Objet : "Pourquoi j'ai créé [entreprise/produit]"

[Contenu : Storytelling + valeurs + ce que vous allez leur apporter]

---

**Email 3 - J+3 : Valeur pure**
Objet : "[X] conseils pour [résoudre leur problème]"

[Contenu : Tips actionnables sans vendre]

---

**Email 4 - J+5 : Preuve sociale**
Objet : "Comment [client] a obtenu [résultat]"

[Contenu : Cas d'étude ou témoignage]

---

**Email 5 - J+7 : Soft pitch**
Objet : "Prêt à passer au niveau supérieur ?"

[Contenu : Présentation de l'offre + CTA]
{{/if}}

{{#if sequence_type.includes('Panier')}}
### SÉQUENCE PANIER ABANDONNÉ

**Email 1 - H+1 : Rappel doux**
Objet : "Vous avez oublié quelque chose 👀"

[Contenu : Rappel produit + bouton retour panier]

---

**Email 2 - H+24 : Urgence**
Objet : "Votre panier expire bientôt"

[Contenu : Création d'urgence + bénéfices produit]

---

**Email 3 - H+48 : Incentive**
Objet : "Un petit coup de pouce : -10% pour finaliser"

[Contenu : Code promo limité + dernier rappel]
{{/if}}

---

### 📊 STRUCTURE DE LA SÉQUENCE

| Email | Timing | Objectif | CTA |
|-------|--------|----------|-----|
| 1 | J+0 | [Objectif] | [CTA] |
| 2 | J+X | [Objectif] | [CTA] |
| ... | ... | ... | ... |

### 📈 MÉTRIQUES À SUIVRE

- Taux d'ouverture par email
- Taux de clic
- Taux de conversion final
- Taux de désinscription`,
  model: 'gpt4',
  estimatedTime: '90s'
};

export const followUpEmailGenerator: AITool = {
  id: 'follow-up-email-generator',
  slug: 'follow-up-email-generator',
  name: { fr: 'Générateur de Relances', ar: 'مولد رسائل المتابعة', en: 'Follow-up Email Generator' },
  description: {
    fr: 'Rédigez des emails de relance qui obtiennent des réponses sans être insistant',
    ar: 'اكتب رسائل متابعة تحصل على ردود دون إلحاح',
    en: 'Write follow-up emails that get responses without being pushy'
  },
  category: 'email',
  subcategory: 'outreach',
  icon: 'RefreshCw',
  credits: 10,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'context', type: 'select', label: 'Contexte de la relance', required: true, options: [
      'Pas de réponse au premier email',
      'Après une réunion',
      'Après envoi d\'une proposition',
      'Après une démo',
      'Rappel de paiement',
      'Prise de nouvelles'
    ]},
    { name: 'previous_interaction', type: 'textarea', label: 'Résumé de l\'interaction précédente' },
    { name: 'days_since', type: 'select', label: 'Jours depuis le dernier contact', options: ['3', '7', '14', '30'] },
    { name: 'desired_outcome', type: 'text', label: 'Résultat souhaité' }
  ],
  outputs: [{ type: 'markdown', name: 'followups' }],
  promptTemplate: `Tu es un expert en relances commerciales non-agressives.

CONTEXTE : {{context}}
INTERACTION PRÉCÉDENTE : {{previous_interaction}}
DÉLAI : {{days_since}} jours
OBJECTIF : {{desired_outcome}}

## 🔄 3 EMAILS DE RELANCE

### Relance 1 : Douce (J+3)

**Objet :** Re: [Objet précédent]

---

Bonjour [Prénom],

Je me permets de revenir vers vous concernant [sujet].

[1 phrase de valeur ajoutée ou nouvelle info]

Seriez-vous disponible pour [CTA] ?

Bien cordialement,
[Signature]

---

### Relance 2 : Valeur ajoutée (J+7)

**Objet :** [Nouvelle accroche - pas "Relance"]

---

Bonjour [Prénom],

Je voulais partager avec vous [ressource/info utile] qui pourrait vous intéresser sur [sujet].

[Lien ou info]

Par ailleurs, ma proposition concernant [sujet initial] tient toujours.

Qu'en pensez-vous ?

[Signature]

---

### Relance 3 : Breakup email (J+14)

**Objet :** Dois-je fermer votre dossier ?

---

Bonjour [Prénom],

Je n'ai pas eu de retour de votre part, je comprends que vous devez être très occupé(e).

Je vais considérer que ce n'est pas le bon moment pour [proposition].

Si jamais votre situation change, n'hésitez pas à me recontacter.

Je vous souhaite une excellente continuation !

[Signature]

---

**Règles de relance :**
✅ Max 3 relances
✅ Espacer de 3-7 jours minimum
✅ Chaque relance apporte de la valeur
✅ Le "breakup email" a souvent le meilleur taux de réponse
✅ Ne jamais culpabiliser le destinataire`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const promotionalEmailGenerator: AITool = {
  id: 'promotional-email-generator',
  slug: 'promotional-email-generator',
  name: { fr: 'Email Promotionnel', ar: 'بريد ترويجي', en: 'Promotional Email' },
  description: {
    fr: 'Créez des emails promotionnels qui convertissent sans être spammy',
    ar: 'أنشئ رسائل ترويجية تحول دون أن تكون مزعجة',
    en: 'Create promotional emails that convert without being spammy'
  },
  category: 'email',
  subcategory: 'sales',
  icon: 'Tag',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'offer', type: 'text', label: 'Offre/Promotion', required: true },
    { name: 'discount_type', type: 'select', label: 'Type de réduction', options: ['Percentage', 'Fixed amount', 'Free shipping', 'Bundle', 'Gift', 'Early access'] },
    { name: 'discount_value', type: 'text', label: 'Valeur de la réduction' },
    { name: 'urgency', type: 'select', label: 'Type d\'urgence', options: ['Deadline', 'Limited stock', 'Early bird', 'Flash sale', 'None'] },
    { name: 'deadline', type: 'text', label: 'Date limite (si applicable)' },
    { name: 'target_segment', type: 'text', label: 'Segment cible (VIP, inactifs...)' }
  ],
  outputs: [{ type: 'markdown', name: 'email' }],
  promptTemplate: `Tu es un expert en email marketing e-commerce.

OFFRE : {{offer}}
RÉDUCTION : {{discount_type}} - {{discount_value}}
URGENCE : {{urgency}}
DEADLINE : {{deadline}}
SEGMENT : {{target_segment}}

## 🏷️ 3 EMAILS PROMOTIONNELS

### Version 1 : Urgence + Bénéfice

**Objet :** {{discount_value}} de réduction - Plus que 24h ⏰
**Preview :** Ne ratez pas cette offre exclusive...

---

[Prénom],

**{{discount_value}} de réduction sur [produit/catégorie]** 🎉

{{#if urgency === 'Deadline'}}
⏰ **Attention :** Cette offre expire le {{deadline}} à minuit.
{{/if}}

**Pourquoi en profiter maintenant :**
✅ [Bénéfice 1]
✅ [Bénéfice 2]
✅ [Bénéfice 3]

👉 **[BOUTON : J'en profite]**

[Code promo si applicable : CODE]

À très vite,
[Signature]

---

### Version 2 : Storytelling

**Objet :** On a une surprise pour vous...

---

[Histoire courte expliquant pourquoi cette offre]

[Offre]

[CTA]

---

### Version 3 : FOMO

**Objet :** 🔥 [X] personnes ont déjà profité de l'offre

---

[Créer l'urgence par la preuve sociale]

[Offre + deadline]

[CTA]

---

**Structure email promo efficace :**
1. Objet accrocheur (pas de spam words)
2. Header visuel avec offre
3. Bénéfices (pas features)
4. Social proof
5. CTA clair et répété
6. Urgence en footer`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const welcomeEmailGenerator: AITool = {
  id: 'welcome-email-generator',
  slug: 'welcome-email-generator',
  name: { fr: 'Email de Bienvenue', ar: 'بريد الترحيب', en: 'Welcome Email' },
  description: {
    fr: 'Créez des emails de bienvenue mémorables qui engagent dès le premier jour',
    ar: 'أنشئ رسائل ترحيب لا تنسى تشرك من اليوم الأول',
    en: 'Create memorable welcome emails that engage from day one'
  },
  category: 'email',
  subcategory: 'automation',
  icon: 'UserPlus',
  credits: 12,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'business_type', type: 'select', label: 'Type de business', options: ['SaaS', 'Ecommerce', 'Newsletter', 'Service', 'Community', 'Course'] },
    { name: 'lead_magnet', type: 'text', label: 'Lead magnet promis (si applicable)' },
    { name: 'brand_personality', type: 'select', options: ['Professionnel', 'Amical', 'Fun', 'Premium', 'Expert'] },
    { name: 'next_steps', type: 'textarea', label: 'Prochaines étapes pour l\'utilisateur' },
    { name: 'social_links', type: 'textarea', label: 'Liens réseaux sociaux' }
  ],
  outputs: [{ type: 'markdown', name: 'email' }],
  promptTemplate: `Tu es un expert en onboarding et première impression.

BUSINESS : {{business_type}}
LEAD MAGNET : {{lead_magnet}}
PERSONNALITÉ : {{brand_personality}}
ÉTAPES SUIVANTES : {{next_steps}}

## 👋 EMAIL DE BIENVENUE

### Version complète

**Objet :** Bienvenue chez [Marque] ! 🎉 Voici [ce qui était promis]
**Preview :** + un cadeau spécial pour bien commencer...

---

Salut [Prénom] ! 👋

**Bienvenue dans la communauté [Marque] !**

Je suis [Nom], [Rôle], et je suis ravi(e) de vous compter parmi nous.

{{#if lead_magnet}}
**📥 Votre [lead magnet] vous attend :**
[BOUTON : Télécharger maintenant]
{{/if}}

---

**🎯 Pour bien commencer, voici les 3 prochaines étapes :**

1️⃣ **[Étape 1]**
   [Description courte]

2️⃣ **[Étape 2]**
   [Description courte]

3️⃣ **[Étape 3]**
   [Description courte]

---

**💡 Ce que vous pouvez attendre de nous :**

- [Bénéfice/contenu 1]
- [Bénéfice/contenu 2]
- [Bénéfice/contenu 3]

---

**🤝 Restons connectés :**

[Icônes réseaux sociaux avec liens]

---

**❓ Une question ?**

Répondez simplement à cet email, je lis personnellement tous les messages.

À très vite,

[Signature]

P.S. [Bonus surprise ou teaser]

---

**Checklist email de bienvenue :**
✅ Livrer ce qui était promis immédiatement
✅ Guider vers la prochaine action
✅ Humaniser (photo, histoire)
✅ Définir les attentes
✅ Un seul CTA principal`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const emailCtaGenerator: AITool = {
  id: 'email-cta-generator',
  slug: 'email-cta-generator',
  name: { fr: 'Générateur de CTA Email', ar: 'مولد دعوات البريد', en: 'Email CTA Generator' },
  description: {
    fr: 'Créez des call-to-action email irrésistibles qui boostent les clics',
    ar: 'أنشئ دعوات عمل بريدية لا تقاوم تزيد النقرات',
    en: 'Create irresistible email CTAs that boost clicks'
  },
  category: 'email',
  subcategory: 'optimization',
  icon: 'MousePointer',
  credits: 8,
  priority: 'critical',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'action_type', type: 'select', label: 'Type d\'action', required: true, options: [
      'Achat',
      'Inscription',
      'Téléchargement',
      'Réservation/RDV',
      'En savoir plus',
      'Répondre'
    ]},
    { name: 'offer_context', type: 'text', label: 'Contexte de l\'offre' },
    { name: 'urgency_level', type: 'select', label: 'Niveau d\'urgence', options: ['None', 'Low', 'Medium', 'High'] },
    { name: 'button_style', type: 'select', label: 'Style de bouton', options: ['Action', 'Benefit', 'Personal', 'Urgent', 'Casual'] }
  ],
  outputs: [{ type: 'markdown', name: 'ctas' }],
  promptTemplate: `Tu es un expert en copywriting et conversion.

ACTION : {{action_type}}
CONTEXTE : {{offer_context}}
URGENCE : {{urgency_level}}
STYLE : {{button_style}}

## 🖱️ 20 CTA EMAIL

### Style Action (verbe d'action)
1. "Commencer maintenant"
2. "Télécharger gratuitement"
3. "Réserver ma place"
4. "Obtenir mon accès"
5. "Découvrir l'offre"

### Style Bénéfice (résultat)
6. "Oui, je veux [bénéfice]"
7. "Accéder à [résultat]"
8. "Débloquer [avantage]"
9. "Recevoir [livrable]"
10. "Obtenir mes [X] gratuits"

### Style Personnel (1ère personne)
11. "Je m'inscris"
12. "Je veux essayer"
13. "C'est parti !"
14. "J'en profite"
15. "Je réserve ma place"

### Style Urgent
16. "Profiter de -X% maintenant"
17. "Ne pas rater ça"
18. "Dernière chance"
19. "Oui, avant qu'il soit trop tard"
20. "Sécuriser mon offre"

---

**Bonnes pratiques CTA :**
✅ Verbe d'action au début
✅ Spécifique > générique
✅ Créer de la valeur perçue
✅ 2-5 mots idéalement
✅ Contraste visuel fort
✅ Un seul CTA principal par email

**À éviter :**
❌ "Cliquez ici"
❌ "Soumettre"
❌ "Envoyer"
❌ Plusieurs CTA concurrents`,
  model: 'gpt4',
  estimatedTime: '15s'
};
