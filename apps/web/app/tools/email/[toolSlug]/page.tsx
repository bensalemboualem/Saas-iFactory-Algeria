'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Mail, Sparkles, Copy, Check, Loader2 } from 'lucide-react';
import { emailTools } from '@/lib/tools-data';

interface PageProps {
  params: { toolSlug: string };
}

interface FormField {
  name: string;
  type: 'text' | 'textarea' | 'select' | 'checkbox' | 'multiselect';
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
  // ===== BATCH 1 - CRITIQUE (8 outils) =====

  'email-subject-line-generator': {
    fields: [
      { name: 'email_topic', type: 'text', label: 'Sujet de l\'email', required: true, placeholder: 'Ex: Lancement nouvelle collection, Offre Black Friday...' },
      { name: 'email_type', type: 'select', label: 'Type d\'email', required: true, options: ['Newsletter', 'Promotionnel', 'Cold Email', 'Relance', 'Bienvenue', 'Transactionnel'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Casual', 'Urgent', 'Curieux', 'Personnel'] },
      { name: 'include_emoji', type: 'checkbox', label: 'Inclure des émojis' },
      { name: 'include_personalization', type: 'checkbox', label: 'Inclure [Prénom]' },
      { name: 'industry', type: 'text', label: 'Secteur (optionnel)', placeholder: 'Ex: SaaS, E-commerce, Formation...' },
    ],
    promptTemplate: `Tu es un expert en email marketing avec des taux d'ouverture de 40%+.

SUJET : {{email_topic}}
TYPE : {{email_type}}
TON : {{tone}}
ÉMOJIS : {{include_emoji}}
PERSONNALISATION : {{include_personalization}}
SECTEUR : {{industry}}

## 📧 20 OBJETS D'EMAIL

### 🔥 Curiosité (5)
1. "[Objet qui crée un mystère autour de {{email_topic}}]"
2. "{{#if include_personalization}}[Prénom], {{/if}}[Question intrigante sur {{email_topic}}]"
3. "[Début de phrase incomplète...]"
4. "Ce que personne ne vous dit sur {{email_topic}}"
5. "J'ai une confession à vous faire..."

### ⏰ Urgence/FOMO (5)
6. "{{#if include_emoji}}⚠️ {{/if}}Dernier jour pour [offre liée à {{email_topic}}]"
7. "Plus que [X] places disponibles"
8. "[Prénom], vous allez rater ça..."
9. "Offre flash : -[X]% pendant 24h"
10. "C'est maintenant ou jamais"

### 💡 Bénéfice direct (5)
11. "Comment [obtenir résultat] en [temps]"
12. "[X] façons de [résoudre problème lié à {{email_topic}}]"
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

### 📊 ANALYSE DES OBJETS

| # | Objet | Caractères | Score estimé |
|---|-------|------------|--------------|
| 1 | [Meilleur objet] | X/50 | ⭐⭐⭐⭐⭐ |
| 2 | [2ème meilleur] | X/50 | ⭐⭐⭐⭐⭐ |
| 3 | [3ème meilleur] | X/50 | ⭐⭐⭐⭐ |

---

### ✅ RÈGLES D'OR

✅ 30-50 caractères (idéal mobile)
✅ Personnalisation = +26% d'ouverture
✅ Émoji en début = +15% (selon audience)
✅ Tester A/B systématiquement

### ❌ À ÉVITER

❌ TOUT EN MAJUSCULES
❌ Trop de !!! ou ???
❌ Mots spam : GRATUIT, €€€, Urgent!!!
❌ Promesses exagérées`
  },

  'cold-email-generator': {
    fields: [
      { name: 'recipient_role', type: 'text', label: 'Rôle du destinataire', required: true, placeholder: 'Ex: CEO, Directeur Marketing, Head of Sales...' },
      { name: 'recipient_company', type: 'text', label: 'Entreprise cible', placeholder: 'Nom de l\'entreprise' },
      { name: 'your_offer', type: 'textarea', label: 'Votre offre/proposition', required: true, placeholder: 'Décrivez ce que vous proposez...' },
      { name: 'value_proposition', type: 'text', label: 'Bénéfice principal pour eux', placeholder: 'Ex: Augmenter les ventes de 30%' },
      { name: 'social_proof', type: 'text', label: 'Preuve sociale', placeholder: 'Ex: Utilisé par 500+ entreprises, +40% de conversion...' },
      { name: 'cta', type: 'select', label: 'Call-to-action', options: ['Meeting 15min', 'Appel découverte', 'Répondre à l\'email', 'Démo produit', 'Ressource gratuite'] },
      { name: 'email_length', type: 'select', label: 'Longueur', options: ['Ultra-court (50 mots)', 'Court (75 mots)', 'Moyen (100 mots)'] },
    ],
    promptTemplate: `Tu es un expert en cold outreach B2B avec 30%+ de taux de réponse.

CIBLE : {{recipient_role}} chez {{recipient_company}}
OFFRE : {{your_offer}}
BÉNÉFICE : {{value_proposition}}
PREUVE : {{social_proof}}
CTA : {{cta}}
LONGUEUR : {{email_length}}

## ❄️ 3 COLD EMAILS

### Email 1 : Ultra-personnalisé (AIDA)

**Objet :** [Objet personnalisé mentionnant {{recipient_company}}]

---

Bonjour [Prénom],

[ATTENTION - 1 ligne personnalisée sur {{recipient_company}} ou {{recipient_role}}]

[INTÉRÊT - 1-2 lignes sur le problème que vous résolvez]

[DÉSIR - Preuve sociale]
→ "Nous avons aidé [client similaire] à {{value_proposition}}"

[ACTION - CTA simple]
Seriez-vous disponible pour {{cta}} cette semaine ?

[Signature courte]

---

### Email 2 : Format PAS (Problem-Agitate-Solve)

**Objet :** Question sur [problème courant des {{recipient_role}}]

---

Bonjour [Prénom],

**Problème :** [Question sur un problème que {{recipient_role}} rencontre]

**Agitation :** [Conséquences de ne pas résoudre ce problème]

**Solution :** {{your_offer}} en 1 phrase.

{{social_proof}}

{{cta}} pour voir si ça peut vous aider ?

[Signature]

---

### Email 3 : Format "Before-After-Bridge"

**Objet :** Idée pour {{recipient_company}}

---

Bonjour [Prénom],

**Avant :** [Situation actuelle probable pour {{recipient_role}}]
**Après :** [Situation idéale : {{value_proposition}}]
**Le pont :** {{your_offer}}

{{cta}} ?

[Signature]

---

### ✅ CHECKLIST COLD EMAIL

✅ Max 100 mots (idéal : 50-75)
✅ 1 seul CTA clair
✅ Personnalisation visible dès la 1ère ligne
✅ Pas de pièces jointes
✅ Signature simple (nom, poste, entreprise)
✅ Envoyer du mardi au jeudi, 9h-11h

### 📅 SÉQUENCE DE RELANCE

- **J+3 :** Relance douce (valeur ajoutée)
- **J+7 :** Relance avec nouvelle info
- **J+14 :** Breakup email`
  },

  'newsletter-generator': {
    fields: [
      { name: 'newsletter_name', type: 'text', label: 'Nom de la newsletter', placeholder: 'Ex: La Weekly, Le Brief Marketing...' },
      { name: 'main_topic', type: 'text', label: 'Sujet principal', required: true, placeholder: 'Ex: Les tendances IA de la semaine' },
      { name: 'newsletter_type', type: 'select', label: 'Format', required: true, options: ['Curation (liens + commentaires)', 'Éducatif (article long)', 'Mixte (intro + liens + CTA)', 'Personnel (réflexions)'] },
      { name: 'sections', type: 'multiselect', label: 'Sections à inclure', options: ['Intro', 'Article principal', 'Liens utiles', 'Citation', 'Astuce', 'Outil', 'Actualités', 'CTA'] },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Conversationnel', 'Humoristique', 'Inspirant'] },
      { name: 'word_count', type: 'select', label: 'Longueur', options: ['Court (300 mots)', 'Moyen (600 mots)', 'Long (1000 mots)'] },
    ],
    promptTemplate: `Tu es un expert en newsletters avec 50%+ de taux d'ouverture.

NEWSLETTER : {{newsletter_name}}
SUJET : {{main_topic}}
FORMAT : {{newsletter_type}}
SECTIONS : {{sections}}
TON : {{tone}}
LONGUEUR : {{word_count}}

## 📰 NEWSLETTER COMPLÈTE

### 📧 OBJET + PREVIEW

**Objet :** [Objet accrocheur sur {{main_topic}}]
**Preview text :** [Texte qui complète l'objet - 90 caractères max]

---

### 👋 INTRO

Salut !

[Accroche personnelle ou actualité liée à {{main_topic}}]

Dans cette édition :
• [Point 1]
• [Point 2]
• [Point 3]

C'est parti ! 👇

---

### 📖 ARTICLE PRINCIPAL

## [Titre accrocheur sur {{main_topic}}]

[Contenu éducatif ou réflexion - adapté à {{word_count}}]

**À retenir :**
→ [Point clé 1]
→ [Point clé 2]
→ [Point clé 3]

---

### 🔗 LIENS DE LA SEMAINE

**1. [Titre]** - [Source]
[1 ligne de commentaire personnel]
→ [Lien]

**2. [Titre]** - [Source]
[1 ligne de commentaire personnel]
→ [Lien]

**3. [Titre]** - [Source]
[1 ligne de commentaire personnel]
→ [Lien]

---

### 💡 ASTUCE DE LA SEMAINE

[Conseil actionnable en 2-3 phrases sur {{main_topic}}]

---

### 🛠️ OUTIL DÉCOUVERTE

**[Nom de l'outil]** - [Catégorie]
[Description courte + pourquoi c'est utile]
→ [Lien]

---

### 💬 CITATION

> "[Citation inspirante liée à {{main_topic}}]"
> — [Auteur]

---

### 🎯 AVANT DE PARTIR

[CTA vers produit, service ou action]

[BOUTON CTA]

---

### OUTRO

À [fréquence],
[Signature]

P.S. [Bonus ou teaser prochaine édition]

---

### 📊 TEMPLATE EMAIL (Structure HTML)

\`\`\`
Header : Logo + date
Section 1 : Intro (background clair)
Section 2 : Article principal (fond blanc)
Section 3 : Liens (fond gris clair)
Section 4 : Astuce (encadré coloré)
Section 5 : CTA (bouton centré)
Footer : Désabonnement + réseaux sociaux
\`\`\``
  },

  'email-sequence-generator': {
    fields: [
      { name: 'sequence_type', type: 'select', label: 'Type de séquence', required: true, options: ['Welcome (nouveaux inscrits)', 'Nurture (éducation)', 'Launch (lancement produit)', 'Panier abandonné', 'Onboarding (nouveaux clients)', 'Ré-engagement (inactifs)'] },
      { name: 'product_service', type: 'text', label: 'Produit/Service à promouvoir', required: true },
      { name: 'sequence_length', type: 'select', label: 'Nombre d\'emails', options: ['3 emails', '5 emails', '7 emails', '10 emails'] },
      { name: 'main_cta', type: 'text', label: 'Action finale souhaitée', placeholder: 'Ex: Acheter le cours, Réserver une démo...' },
      { name: 'brand_voice', type: 'select', label: 'Ton de la marque', options: ['Professionnel', 'Amical', 'Expert', 'Inspirant'] },
    ],
    promptTemplate: `Tu es un expert en email automation et funnel marketing.

TYPE : {{sequence_type}}
PRODUIT : {{product_service}}
LONGUEUR : {{sequence_length}}
CTA FINAL : {{main_cta}}
TON : {{brand_voice}}

## 📧 SÉQUENCE EMAIL COMPLÈTE

### 🎯 STRATÉGIE DE LA SÉQUENCE

**Objectif :** Convertir vers {{main_cta}}
**Durée totale :** [X jours]
**Ton :** {{brand_voice}}

---

### EMAIL 1 - J+0 (Immédiat) : Bienvenue + Livraison

**Objet :** Bienvenue ! Voici [ce qui était promis] 🎉
**Timing :** Immédiat après inscription

---

Salut [Prénom] ! 👋

Bienvenue dans [communauté/liste] !

**Voici ce que vous avez demandé :**
[BOUTON : Télécharger / Accéder]

**Ce que vous pouvez attendre de moi :**
• [Contenu 1]
• [Contenu 2]
• [Contenu 3]

À très vite,
[Signature]

---

### EMAIL 2 - J+1 : Votre histoire / Connexion

**Objet :** Pourquoi j'ai créé {{product_service}}
**Timing :** 24h après

---

[Prénom],

[Storytelling personnel - 3-4 paragraphes]

• Pourquoi ce projet existe
• Ce que j'aurais aimé savoir avant
• Ce que je veux pour vous

[Transition vers la valeur à venir]

[Signature]

---

### EMAIL 3 - J+3 : Valeur pure

**Objet :** [X] conseils pour [résoudre leur problème]
**Timing :** 3 jours après

---

[Prénom],

Aujourd'hui, je partage avec vous [X] conseils que j'aurais aimé connaître plus tôt.

**Conseil 1 : [Titre]**
[Explication actionnable]

**Conseil 2 : [Titre]**
[Explication actionnable]

**Conseil 3 : [Titre]**
[Explication actionnable]

[Teaser vers {{product_service}}]

[Signature]

---

### EMAIL 4 - J+5 : Preuve sociale

**Objet :** Comment [Client] a obtenu [Résultat]
**Timing :** 5 jours après

---

[Prénom],

Je voulais vous partager l'histoire de [Client].

**Avant :** [Situation problématique]
**Après :** [Résultat obtenu avec {{product_service}}]

[Témoignage ou cas d'étude détaillé]

[Soft CTA vers {{main_cta}}]

[Signature]

---

### EMAIL 5 - J+7 : L'offre

**Objet :** [Prénom], prêt(e) à [bénéfice] ?
**Timing :** 7 jours après

---

[Prénom],

Cette semaine, je vous ai partagé :
• [Récap valeur 1]
• [Récap valeur 2]
• [Récap valeur 3]

**Maintenant, il est temps de passer à l'action.**

[Présentation de {{product_service}}]

**Ce que vous obtenez :**
✅ [Bénéfice 1]
✅ [Bénéfice 2]
✅ [Bénéfice 3]

[BOUTON : {{main_cta}}]

[Signature]

---

### 📊 STRUCTURE DE LA SÉQUENCE

| Email | Timing | Objectif | Taux ouv. cible |
|-------|--------|----------|-----------------|
| 1 | J+0 | Livrer + Accueillir | 60%+ |
| 2 | J+1 | Connecter | 45%+ |
| 3 | J+3 | Éduquer | 40%+ |
| 4 | J+5 | Prouver | 35%+ |
| 5 | J+7 | Convertir | 30%+ |

### 📈 MÉTRIQUES À SUIVRE

• Taux d'ouverture par email
• Taux de clic
• Taux de conversion final
• Taux de désinscription (< 0.5%)`
  },

  'follow-up-email-generator': {
    fields: [
      { name: 'context', type: 'select', label: 'Contexte de la relance', required: true, options: ['Pas de réponse au premier email', 'Après une réunion', 'Après envoi d\'une proposition', 'Après une démo', 'Rappel de paiement', 'Prise de nouvelles'] },
      { name: 'previous_interaction', type: 'textarea', label: 'Résumé de l\'interaction précédente', required: true, placeholder: 'Décrivez brièvement ce qui s\'est passé avant...' },
      { name: 'days_since', type: 'select', label: 'Jours depuis le dernier contact', options: ['3 jours', '7 jours', '14 jours', '30 jours'] },
      { name: 'desired_outcome', type: 'text', label: 'Résultat souhaité', placeholder: 'Ex: Obtenir un RDV, Valider la proposition...' },
    ],
    promptTemplate: `Tu es un expert en relances commerciales non-agressives.

CONTEXTE : {{context}}
INTERACTION PRÉCÉDENTE : {{previous_interaction}}
DÉLAI : {{days_since}}
OBJECTIF : {{desired_outcome}}

## 🔄 3 EMAILS DE RELANCE

### Relance 1 : Douce (J+3)

**Objet :** Re: [Objet de l'email précédent]

---

Bonjour [Prénom],

Je me permets de revenir vers vous concernant {{previous_interaction}}.

[1 phrase de valeur ajoutée ou rappel du bénéfice]

Seriez-vous disponible pour {{desired_outcome}} ?

Bien cordialement,
[Signature]

---

### Relance 2 : Valeur ajoutée (J+7)

**Objet :** [Nouvelle accroche - PAS "Relance"]

---

Bonjour [Prénom],

Je voulais partager avec vous [ressource/info utile] qui pourrait vous intéresser :

[Lien ou information pertinente]

Par ailleurs, ma proposition concernant {{previous_interaction}} tient toujours.

Qu'en pensez-vous ?

[Signature]

---

### Relance 3 : Breakup email (J+14)

**Objet :** Dois-je fermer votre dossier ?

---

Bonjour [Prénom],

Je n'ai pas eu de retour de votre part concernant {{previous_interaction}}.

Je comprends que vous devez être très occupé(e), je vais donc considérer que ce n'est pas le bon moment.

Si jamais votre situation change, n'hésitez pas à me recontacter - je serai ravi(e) de reprendre notre conversation.

Je vous souhaite une excellente continuation !

[Signature]

---

### ✅ RÈGLES DE RELANCE

✅ Maximum 3 relances
✅ Espacer de 3-7 jours minimum
✅ Chaque relance apporte de la valeur
✅ Le "breakup email" a souvent le meilleur taux de réponse
✅ Ne jamais culpabiliser le destinataire
✅ Toujours laisser la porte ouverte

### 📊 STATISTIQUES

• 80% des ventes nécessitent 5+ contacts
• Le breakup email obtient 25-30% de réponses
• Meilleur moment : Mardi/Mercredi 9h-11h`
  },

  'promotional-email-generator': {
    fields: [
      { name: 'offer', type: 'text', label: 'Offre/Promotion', required: true, placeholder: 'Ex: -30% sur toute la collection' },
      { name: 'discount_type', type: 'select', label: 'Type de réduction', options: ['Pourcentage', 'Montant fixe', 'Livraison gratuite', 'Bundle/Pack', 'Cadeau offert', 'Accès anticipé'] },
      { name: 'discount_value', type: 'text', label: 'Valeur de la réduction', placeholder: 'Ex: 30%, 50€, Gratuit...' },
      { name: 'urgency', type: 'select', label: 'Type d\'urgence', options: ['Date limite', 'Stock limité', 'Early bird', 'Vente flash', 'Aucune'] },
      { name: 'deadline', type: 'text', label: 'Date limite (si applicable)', placeholder: 'Ex: Dimanche minuit' },
      { name: 'target_segment', type: 'text', label: 'Segment cible', placeholder: 'Ex: VIP, Inactifs, Nouveaux...' },
    ],
    promptTemplate: `Tu es un expert en email marketing e-commerce avec +25% de taux de conversion.

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

**{{discount_value}} de réduction sur {{offer}}** 🎉

{{#if urgency === 'deadline'}}
⏰ **Attention :** Cette offre expire {{deadline}}.
{{/if}}

**Pourquoi en profiter maintenant :**
✅ [Bénéfice 1 - économie]
✅ [Bénéfice 2 - qualité]
✅ [Bénéfice 3 - exclusivité]

👉 **[BOUTON : J'en profite maintenant]**

[Code promo si applicable : CODE]

À très vite,
[Signature]

---

### Version 2 : Storytelling

**Objet :** On a une surprise pour vous... 🎁

---

[Prénom],

[Histoire courte expliquant pourquoi cette offre existe]

**Votre cadeau :** {{discount_value}} sur {{offer}}

[BOUTON : Découvrir l'offre]

[Signature]

---

### Version 3 : FOMO / Social Proof

**Objet :** 🔥 [X] personnes ont déjà profité de l'offre

---

[Prénom],

Depuis ce matin, **[X] personnes** ont profité de notre offre {{offer}}.

**Ce qu'ils ont aimé :**
⭐ "[Témoignage court 1]"
⭐ "[Témoignage court 2]"

**Il reste encore quelques heures pour vous aussi :**

[BOUTON : Je rejoins les [X] autres]

{{deadline}}

[Signature]

---

### 📧 STRUCTURE EMAIL PROMO EFFICACE

1. **Objet** : Accrocheur (pas de spam words)
2. **Header** : Visuel avec offre claire
3. **Bénéfices** : Pas features, mais résultats
4. **Social proof** : Témoignages, nombres
5. **CTA** : Clair et répété 2-3 fois
6. **Urgence** : En footer

### ❌ MOTS À ÉVITER (Spam filters)

❌ GRATUIT, FREE, €€€
❌ URGENT, DERNIÈRE CHANCE
❌ Gagner, Félicitations
❌ Trop de majuscules/points d'exclamation`
  },

  'welcome-email-generator': {
    fields: [
      { name: 'business_type', type: 'select', label: 'Type de business', required: true, options: ['SaaS', 'E-commerce', 'Newsletter', 'Service/Consulting', 'Communauté', 'Formation/Cours'] },
      { name: 'lead_magnet', type: 'text', label: 'Lead magnet promis', placeholder: 'Ex: Ebook, Checklist, Accès gratuit...' },
      { name: 'brand_personality', type: 'select', label: 'Personnalité de marque', options: ['Professionnel', 'Amical', 'Fun', 'Premium', 'Expert'] },
      { name: 'next_steps', type: 'textarea', label: 'Prochaines étapes pour l\'utilisateur', placeholder: 'Que doit faire le nouvel inscrit ensuite ?' },
      { name: 'social_links', type: 'text', label: 'Réseaux sociaux', placeholder: 'Ex: LinkedIn, Twitter, Instagram...' },
    ],
    promptTemplate: `Tu es un expert en onboarding et première impression.

BUSINESS : {{business_type}}
LEAD MAGNET : {{lead_magnet}}
PERSONNALITÉ : {{brand_personality}}
ÉTAPES SUIVANTES : {{next_steps}}
RÉSEAUX : {{social_links}}

## 👋 EMAIL DE BIENVENUE

### Version complète

**Objet :** Bienvenue chez [Marque] ! 🎉 Voici {{lead_magnet}}
**Preview :** + un cadeau spécial pour bien commencer...

---

Salut [Prénom] ! 👋

**Bienvenue dans la communauté [Marque] !**

Je suis [Nom], [Rôle], et je suis ravi(e) de vous compter parmi nous.

{{#if lead_magnet}}
---

**📥 Votre {{lead_magnet}} vous attend :**

[BOUTON : Télécharger maintenant]

{{/if}}

---

**🎯 Pour bien commencer, voici vos 3 prochaines étapes :**

1️⃣ **[Étape 1]**
   [Description courte + lien si nécessaire]

2️⃣ **[Étape 2]**
   [Description courte + lien si nécessaire]

3️⃣ **[Étape 3]**
   [Description courte + lien si nécessaire]

---

**💡 Ce que vous pouvez attendre de nous :**

• [Contenu/valeur 1 que vous envoyez]
• [Contenu/valeur 2]
• [Contenu/valeur 3]

---

**🤝 Restons connectés :**

[Icônes réseaux sociaux : {{social_links}}]

---

**❓ Une question ?**

Répondez simplement à cet email - je lis personnellement tous les messages.

À très vite,

[Signature avec photo]

P.S. [Bonus surprise ou teaser de ce qui arrive]

---

### ✅ CHECKLIST EMAIL DE BIENVENUE

✅ Livrer ce qui était promis IMMÉDIATEMENT
✅ Guider vers la prochaine action claire
✅ Humaniser (photo, ton personnel)
✅ Définir les attentes (fréquence, contenu)
✅ Un seul CTA principal
✅ P.S. avec bonus ou teaser

### 📊 BENCHMARKS

• Taux d'ouverture cible : 50-70%
• Taux de clic cible : 15-25%
• Envoyer dans les 5 minutes après inscription`
  },

  'email-cta-generator': {
    fields: [
      { name: 'action_type', type: 'select', label: 'Type d\'action', required: true, options: ['Achat', 'Inscription', 'Téléchargement', 'Réservation/RDV', 'En savoir plus', 'Répondre'] },
      { name: 'offer_context', type: 'text', label: 'Contexte de l\'offre', required: true, placeholder: 'Ex: Formation en ligne, Produit SaaS, Ebook...' },
      { name: 'urgency_level', type: 'select', label: 'Niveau d\'urgence', options: ['Aucune', 'Légère', 'Moyenne', 'Forte'] },
      { name: 'button_style', type: 'select', label: 'Style de bouton', options: ['Action directe', 'Bénéfice', 'Personnel (Je...)', 'Urgent', 'Casual'] },
    ],
    promptTemplate: `Tu es un expert en copywriting et conversion email.

ACTION : {{action_type}}
CONTEXTE : {{offer_context}}
URGENCE : {{urgency_level}}
STYLE : {{button_style}}

## 🖱️ 25 CTA EMAIL POUR {{offer_context}}

### 🎯 Style Action (verbe d'action)
1. "Commencer maintenant"
2. "Télécharger gratuitement"
3. "Réserver ma place"
4. "Obtenir mon accès"
5. "Découvrir l'offre"

### 💎 Style Bénéfice (résultat)
6. "Oui, je veux [bénéfice lié à {{offer_context}}]"
7. "Accéder à [résultat]"
8. "Débloquer [avantage]"
9. "Recevoir [livrable]"
10. "Obtenir mes [X] gratuits"

### 👤 Style Personnel (1ère personne)
11. "Je m'inscris"
12. "Je veux essayer"
13. "C'est parti !"
14. "J'en profite"
15. "Je réserve ma place"

### ⏰ Style Urgent
16. "Profiter de -X% maintenant"
17. "Ne pas rater ça"
18. "Dernière chance"
19. "Oui, avant qu'il soit trop tard"
20. "Sécuriser mon offre"

### 😊 Style Casual
21. "Je jette un œil"
22. "Ça m'intéresse"
23. "Montre-moi ça"
24. "J'y vais"
25. "Let's go !"

---

### 📊 TOP 5 RECOMMANDÉS POUR {{offer_context}}

| Rang | CTA | Pourquoi |
|------|-----|----------|
| 1 | "[CTA adapté]" | [Raison] |
| 2 | "[CTA adapté]" | [Raison] |
| 3 | "[CTA adapté]" | [Raison] |
| 4 | "[CTA adapté]" | [Raison] |
| 5 | "[CTA adapté]" | [Raison] |

---

### ✅ BONNES PRATIQUES CTA

✅ Verbe d'action au début
✅ Spécifique > générique
✅ Créer de la valeur perçue
✅ 2-5 mots idéalement
✅ Contraste visuel fort (bouton)
✅ Un seul CTA principal par email

### ❌ À ÉVITER

❌ "Cliquez ici" (trop générique)
❌ "Soumettre" (trop froid)
❌ "Envoyer" (pas engageant)
❌ Plusieurs CTA concurrents
❌ CTA en fin d'email uniquement

### 💡 ASTUCE PRO

Répéter le CTA 2-3 fois dans l'email :
1. Après l'intro
2. Au milieu du contenu
3. En conclusion (bouton principal)`
  },

  // ===== BATCH 2 - HAUTE PRIORITÉ (8 outils) =====

  'abandoned-cart-email': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Produit abandonné', required: true },
      { name: 'product_price', type: 'text', label: 'Prix du produit' },
      { name: 'incentive', type: 'select', label: 'Incentive à offrir', options: ['Aucun', '-10% de réduction', '-15% de réduction', 'Livraison gratuite', 'Cadeau offert'] },
      { name: 'brand_tone', type: 'select', label: 'Ton', options: ['Amical', 'Professionnel', 'Humoristique', 'Urgent'] },
    ],
    promptTemplate: `Tu es expert en récupération de paniers abandonnés e-commerce.

PRODUIT : {{product_name}}
PRIX : {{product_price}}
INCENTIVE : {{incentive}}
TON : {{brand_tone}}

## 🛒 SÉQUENCE PANIER ABANDONNÉ (3 emails)

### Email 1 - H+1 : Rappel doux

**Objet :** Vous avez oublié quelque chose 👀
**Preview :** Votre {{product_name}} vous attend...

---

[Prénom],

On a remarqué que vous avez laissé {{product_name}} dans votre panier.

[IMAGE PRODUIT]

Pas de souci, on vous l'a gardé ! 😊

👉 [BOUTON : Finaliser ma commande]

Des questions ? Répondez à cet email !

[Signature]

---

### Email 2 - H+24 : Urgence douce

**Objet :** Votre panier expire bientôt ⏰

---

[Prénom],

Votre {{product_name}} est toujours disponible, mais pas pour longtemps...

**Pourquoi les autres l'adorent :**
⭐ [Avantage 1]
⭐ [Avantage 2]
⭐ [Avantage 3]

👉 [BOUTON : Récupérer mon panier]

[Signature]

---

### Email 3 - H+48 : Incentive

**Objet :** Un petit coup de pouce : {{incentive}} 🎁

---

[Prénom],

On voulait vraiment que {{product_name}} soit à vous...

**Alors voici {{incentive}} pour vous décider !**

Code : [CODE]
Valable 24h

👉 [BOUTON : Utiliser mon code]

C'est notre dernière relance - après ça, on vous laisse tranquille ! 😊

[Signature]

---

### 📊 TIMING OPTIMAL

• H+1 : Rappel immédiat (40% récupération)
• H+24 : Urgence (25% supplémentaire)
• H+48 : Incentive (15% supplémentaire)`
  },

  're-engagement-email': {
    fields: [
      { name: 'inactive_period', type: 'select', label: 'Période d\'inactivité', required: true, options: ['30 jours', '60 jours', '90 jours', '6 mois', '1 an'] },
      { name: 'reason_to_return', type: 'text', label: 'Raison de revenir', placeholder: 'Ex: Nouvelles fonctionnalités, Contenu exclusif...' },
      { name: 'incentive', type: 'text', label: 'Incentive offert', placeholder: 'Ex: -20%, accès gratuit 1 mois...' },
      { name: 'tone', type: 'select', label: 'Ton', options: ['Nostalgique', 'Direct', 'Humoristique', 'Sincère'] },
    ],
    promptTemplate: `Tu es expert en ré-engagement d'abonnés inactifs.

INACTIVITÉ : {{inactive_period}}
RAISON DE REVENIR : {{reason_to_return}}
INCENTIVE : {{incentive}}
TON : {{tone}}

## 🔄 3 EMAILS DE RÉ-ENGAGEMENT

### Email 1 : Nostalgique

**Objet :** [Prénom], vous nous manquez 😢
**Preview :** Ça fait {{inactive_period}} qu'on ne s'est pas parlé...

---

[Prénom],

Ça fait un moment qu'on ne s'est pas vu(e)s...

Depuis votre dernière visite, voici ce qui a changé :
✨ {{reason_to_return}}
✨ [Nouveauté 2]
✨ [Nouveauté 3]

On aimerait vous revoir !

👉 [BOUTON : Découvrir les nouveautés]

[Signature]

---

### Email 2 : Direct + Incentive

**Objet :** {{incentive}} pour votre retour 🎁

---

[Prénom],

On va être honnête : vous nous manquez.

Pour vous inciter à revenir, voici {{incentive}}.

👉 [BOUTON : J'en profite]

[Signature]

---

### Email 3 : Dernière chance

**Objet :** On se dit au revoir ? 👋

---

[Prénom],

On n'a pas eu de nouvelles depuis {{inactive_period}}.

On comprend - les priorités changent.

Si vous voulez rester avec nous, un simple clic :
👉 [BOUTON : Je reste !]

Sinon, on vous désinscrit automatiquement dans 7 jours.

Pas de rancune ! 😊

[Signature]`
  },

  'testimonial-request-email': {
    fields: [
      { name: 'product_service', type: 'text', label: 'Produit/Service concerné', required: true },
      { name: 'customer_result', type: 'text', label: 'Résultat obtenu par le client', placeholder: 'Ex: +50% de ventes, 10h gagnées/semaine...' },
      { name: 'testimonial_type', type: 'select', label: 'Type de témoignage', options: ['Écrit (court)', 'Écrit (détaillé)', 'Vidéo', 'Avis Google/Trustpilot'] },
      { name: 'incentive', type: 'text', label: 'Incentive (optionnel)', placeholder: 'Ex: -10% prochaine commande...' },
    ],
    promptTemplate: `Tu es expert en collecte de témoignages clients.

PRODUIT : {{product_service}}
RÉSULTAT CLIENT : {{customer_result}}
TYPE : {{testimonial_type}}
INCENTIVE : {{incentive}}

## ⭐ 3 EMAILS DEMANDE DE TÉMOIGNAGE

### Email 1 : Simple et direct

**Objet :** [Prénom], 2 minutes pour nous aider ? 🙏

---

[Prénom],

Félicitations pour {{customer_result}} avec {{product_service}} ! 🎉

Votre succès nous inspire, et on aimerait le partager avec d'autres.

**Accepteriez-vous de partager votre expérience en 2 minutes ?**

👉 [BOUTON : Laisser un témoignage]

Merci infiniment !

[Signature]

---

### Email 2 : Guidé (avec questions)

**Objet :** Votre avis compte énormément pour nous ⭐

---

[Prénom],

On aimerait entendre votre histoire avec {{product_service}}.

**3 questions rapides (2 min) :**

1. Quel problème aviez-vous avant ?
2. Comment {{product_service}} vous a aidé ?
3. Quel résultat avez-vous obtenu ?

👉 [BOUTON : Partager mon expérience]

{{#if incentive}}
**Bonus :** {{incentive}} pour vous remercier !
{{/if}}

[Signature]

---

### Email 3 : Avec preuve sociale

**Objet :** Rejoignez nos 100+ clients satisfaits 🌟

---

[Prénom],

Plus de 100 clients ont déjà partagé leur expérience.

Voici ce qu'ils disent :
⭐ "[Témoignage 1]"
⭐ "[Témoignage 2]"

**Et vous, quelle est votre histoire ?**

👉 [BOUTON : Ajouter mon témoignage]

[Signature]`
  },

  'referral-email': {
    fields: [
      { name: 'reward_referrer', type: 'text', label: 'Récompense parrain', required: true, placeholder: 'Ex: 20€ de crédit, 1 mois gratuit...' },
      { name: 'reward_referee', type: 'text', label: 'Récompense filleul', required: true, placeholder: 'Ex: -20% première commande...' },
      { name: 'product_service', type: 'text', label: 'Produit/Service' },
      { name: 'sharing_method', type: 'select', label: 'Méthode de partage', options: ['Lien unique', 'Code promo', 'Email direct'] },
    ],
    promptTemplate: `Tu es expert en programmes de parrainage.

RÉCOMPENSE PARRAIN : {{reward_referrer}}
RÉCOMPENSE FILLEUL : {{reward_referee}}
PRODUIT : {{product_service}}
MÉTHODE : {{sharing_method}}

## 🎁 EMAIL PROGRAMME DE PARRAINAGE

### Version principale

**Objet :** Gagnez {{reward_referrer}} en partageant {{product_service}} 🎉
**Preview :** + {{reward_referee}} pour vos amis !

---

[Prénom],

**Vous aimez {{product_service}} ?**

Partagez-le et gagnez {{reward_referrer}} pour chaque ami inscrit !

**Comment ça marche :**

1️⃣ Partagez votre lien unique
2️⃣ Votre ami s'inscrit et bénéficie de {{reward_referee}}
3️⃣ Vous recevez {{reward_referrer}} 🎁

**Votre lien de parrainage :**
[LIEN UNIQUE]

👉 [BOUTON : Inviter mes amis]

Pas de limite ! Plus vous parrainez, plus vous gagnez.

[Signature]

---

### 📧 EMAIL POUR LE FILLEUL

**Objet :** [Prénom du parrain] vous offre {{reward_referee}} 🎁

---

Bonjour,

[Prénom du parrain] pense que {{product_service}} pourrait vous plaire !

**Votre cadeau de bienvenue :** {{reward_referee}}

👉 [BOUTON : Profiter de l'offre]

[Description courte du produit/service]

[Signature]`
  },

  'event-invitation-email': {
    fields: [
      { name: 'event_name', type: 'text', label: 'Nom de l\'événement', required: true },
      { name: 'event_type', type: 'select', label: 'Type', options: ['Webinar', 'Workshop', 'Conférence', 'Lancement', 'Networking', 'Formation'] },
      { name: 'event_date', type: 'text', label: 'Date et heure', required: true },
      { name: 'event_description', type: 'textarea', label: 'Description', placeholder: 'Ce que les participants vont apprendre/obtenir...' },
      { name: 'speaker', type: 'text', label: 'Intervenant(s)', placeholder: 'Nom et titre' },
    ],
    promptTemplate: `Tu es expert en marketing événementiel.

ÉVÉNEMENT : {{event_name}}
TYPE : {{event_type}}
DATE : {{event_date}}
DESCRIPTION : {{event_description}}
INTERVENANT : {{speaker}}

## 📅 3 EMAILS INVITATION ÉVÉNEMENT

### Email 1 : Invitation principale

**Objet :** [Prénom], vous êtes invité(e) à {{event_name}} 🎉
**Preview :** {{event_date}} - Places limitées !

---

[Prénom],

**Vous êtes invité(e) à {{event_name}} !**

📅 **Date :** {{event_date}}
🎤 **Intervenant :** {{speaker}}
💻 **Format :** {{event_type}} en ligne

**Ce que vous allez apprendre :**
✅ [Point 1]
✅ [Point 2]
✅ [Point 3]

👉 [BOUTON : Réserver ma place]

⚠️ Places limitées - Inscrivez-vous maintenant !

[Signature]

---

### Email 2 : Rappel J-3

**Objet :** Plus que 3 jours pour {{event_name}} ⏰

---

[Prénom],

{{event_name}} approche !

📅 {{event_date}}

**Dernière chance de vous inscrire.**

👉 [BOUTON : Je m'inscris]

[Signature]

---

### Email 3 : Rappel J-1 (inscrits)

**Objet :** C'est demain ! Votre lien pour {{event_name}} 🔗

---

[Prénom],

**C'est demain !**

📅 {{event_date}}
🔗 **Votre lien d'accès :** [LIEN]

**Pour bien vous préparer :**
• [Conseil 1]
• [Conseil 2]

À demain !

[Signature]`
  },

  'product-launch-email': {
    fields: [
      { name: 'product_name', type: 'text', label: 'Nom du produit', required: true },
      { name: 'product_description', type: 'textarea', label: 'Description courte', required: true },
      { name: 'key_benefits', type: 'textarea', label: 'Bénéfices principaux (3-5)', placeholder: 'Un par ligne' },
      { name: 'launch_offer', type: 'text', label: 'Offre de lancement', placeholder: 'Ex: -30% early bird, bonus exclusif...' },
      { name: 'launch_date', type: 'text', label: 'Date de lancement' },
    ],
    promptTemplate: `Tu es expert en lancement de produit.

PRODUIT : {{product_name}}
DESCRIPTION : {{product_description}}
BÉNÉFICES : {{key_benefits}}
OFFRE : {{launch_offer}}
DATE : {{launch_date}}

## 🚀 SÉQUENCE LANCEMENT PRODUIT

### Email 1 : Teaser (J-7)

**Objet :** Quelque chose d'excitant arrive... 👀

---

[Prénom],

On prépare quelque chose de spécial pour vous.

{{product_description}} (sans révéler le nom)

**Rendez-vous {{launch_date}}.**

Restez à l'écoute...

[Signature]

---

### Email 2 : Annonce (Jour J)

**Objet :** 🚀 C'est officiel : {{product_name}} est là !

---

[Prénom],

**Le jour est arrivé !**

Découvrez **{{product_name}}** :

{{product_description}}

**Ce que vous obtenez :**
{{key_benefits}}

**🎁 Offre de lancement :** {{launch_offer}}
⏰ Valable jusqu'à [date]

👉 [BOUTON : Découvrir {{product_name}}]

[Signature]

---

### Email 3 : Urgence (J+3)

**Objet :** L'offre {{launch_offer}} expire bientôt ⏰

---

[Prénom],

Plus que [X] heures pour profiter de {{launch_offer}} sur {{product_name}}.

**Ce qu'ils en disent déjà :**
⭐ "[Témoignage early adopter]"

👉 [BOUTON : Profiter de l'offre]

[Signature]`
  },

  'thank-you-email': {
    fields: [
      { name: 'occasion', type: 'select', label: 'Occasion', required: true, options: ['Achat', 'Inscription', 'Participation événement', 'Témoignage', 'Parrainage', 'Fidélité'] },
      { name: 'product_service', type: 'text', label: 'Produit/Service concerné' },
      { name: 'next_action', type: 'text', label: 'Prochaine action suggérée', placeholder: 'Ex: Utiliser le produit, Rejoindre la communauté...' },
      { name: 'bonus', type: 'text', label: 'Bonus/Cadeau (optionnel)', placeholder: 'Ex: Ebook gratuit, code promo...' },
    ],
    promptTemplate: `Tu es expert en relation client.

OCCASION : {{occasion}}
PRODUIT : {{product_service}}
PROCHAINE ACTION : {{next_action}}
BONUS : {{bonus}}

## 🙏 EMAIL DE REMERCIEMENT

### Version principale

**Objet :** Merci [Prénom] ! 🙏
**Preview :** Votre confiance nous touche...

---

[Prénom],

**Un grand MERCI pour {{occasion}} !**

Votre confiance signifie énormément pour nous. 🙏

{{#if bonus}}
**Pour vous remercier, voici un petit cadeau :**
🎁 {{bonus}}

👉 [BOUTON : Récupérer mon cadeau]
{{/if}}

**Prochaine étape :**
{{next_action}}

Des questions ? Répondez simplement à cet email.

Avec gratitude,
[Signature]

---

### 📧 VARIANTES PAR OCCASION

**Achat :**
"Merci pour votre commande ! Voici ce qui se passe ensuite..."

**Inscription :**
"Bienvenue ! Votre aventure commence ici..."

**Événement :**
"Merci d'avoir participé ! Voici le replay..."

**Témoignage :**
"Merci pour vos mots ! Ils vont inspirer d'autres..."

**Parrainage :**
"Merci de nous recommander ! Voici votre récompense..."

**Fidélité :**
"1 an ensemble ! Merci de votre confiance..."`
  },

  'apology-email': {
    fields: [
      { name: 'incident_type', type: 'select', label: 'Type d\'incident', required: true, options: ['Erreur technique', 'Retard livraison', 'Mauvais produit envoyé', 'Problème facturation', 'Mauvaise communication', 'Service indisponible'] },
      { name: 'incident_description', type: 'textarea', label: 'Description de l\'incident', required: true },
      { name: 'resolution', type: 'textarea', label: 'Solution apportée', placeholder: 'Comment vous avez résolu le problème...' },
      { name: 'compensation', type: 'text', label: 'Compensation offerte', placeholder: 'Ex: Remboursement, crédit, cadeau...' },
    ],
    promptTemplate: `Tu es expert en gestion de crise et relation client.

INCIDENT : {{incident_type}}
DESCRIPTION : {{incident_description}}
RÉSOLUTION : {{resolution}}
COMPENSATION : {{compensation}}

## 😔 EMAIL D'EXCUSES PROFESSIONNEL

### Version principale

**Objet :** Nos excuses sincères - [Sujet de l'incident]
**Preview :** Nous prenons l'entière responsabilité...

---

[Prénom],

**Nous vous devons des excuses.**

{{incident_description}}

Nous prenons l'entière responsabilité de cette situation et comprenons votre frustration.

**Ce que nous avons fait pour résoudre le problème :**
{{resolution}}

**Pour vous dédommager :**
🎁 {{compensation}}

👉 [BOUTON : Utiliser ma compensation]

**Ce que nous faisons pour que ça n'arrive plus :**
• [Mesure corrective 1]
• [Mesure corrective 2]

Encore une fois, veuillez accepter nos sincères excuses.

[Signature - Nom du responsable]

P.S. Si vous avez besoin d'autre chose, répondez directement à cet email.

---

### ✅ CHECKLIST EMAIL D'EXCUSES

✅ Reconnaître l'erreur clairement
✅ Prendre la responsabilité (pas de "si vous avez été gêné")
✅ Expliquer sans se justifier excessivement
✅ Donner la solution/résolution
✅ Offrir une compensation appropriée
✅ Montrer les actions préventives
✅ Rester humble et sincère

### ❌ À ÉVITER

❌ "Nous sommes désolés SI vous avez été dérangé"
❌ Rejeter la faute sur le client ou des tiers
❌ Minimiser le problème
❌ Être trop technique/froid
❌ Promettre sans tenir`
  },

  // ===== BATCH 3 - MOYENNE PRIORITÉ (4 outils) =====

  'feedback-request-email': {
    fields: [
      { name: 'product_service', type: 'text', label: 'Produit/Service concerné', required: true },
      { name: 'feedback_type', type: 'select', label: 'Type de feedback', options: ['Satisfaction générale', 'NPS (recommandation)', 'Fonctionnalités', 'Support client', 'Prix/Valeur'] },
      { name: 'survey_length', type: 'select', label: 'Longueur du sondage', options: ['1 question', '3 questions', '5 questions', 'Sondage complet'] },
      { name: 'incentive', type: 'text', label: 'Incentive (optionnel)', placeholder: 'Ex: Tirage au sort, code promo...' },
    ],
    promptTemplate: `Tu es expert en collecte de feedback client.

PRODUIT : {{product_service}}
TYPE : {{feedback_type}}
LONGUEUR : {{survey_length}}
INCENTIVE : {{incentive}}

## 📝 EMAIL DEMANDE DE FEEDBACK

**Objet :** Votre avis en {{survey_length}} ? 🙏

---

[Prénom],

Votre opinion compte énormément pour améliorer {{product_service}}.

**{{survey_length}} pour nous aider :**

[Question principale basée sur {{feedback_type}}]

👉 [BOUTON : Donner mon avis]

{{#if incentive}}
**Bonus :** {{incentive}} pour vous remercier !
{{/if}}

Merci d'avance,
[Signature]`
  },

  'milestone-email': {
    fields: [
      { name: 'milestone_type', type: 'select', label: 'Type de milestone', required: true, options: ['Anniversaire inscription', 'X commandes', 'X mois/années client', 'Niveau atteint', 'Objectif complété'] },
      { name: 'milestone_value', type: 'text', label: 'Valeur du milestone', placeholder: 'Ex: 1 an, 10 commandes, niveau Gold...' },
      { name: 'reward', type: 'text', label: 'Récompense offerte', placeholder: 'Ex: Badge, réduction, accès VIP...' },
      { name: 'personalization', type: 'textarea', label: 'Élément personnalisé', placeholder: 'Statistiques du client, progression...' },
    ],
    promptTemplate: `Tu es expert en programmes de fidélité.

MILESTONE : {{milestone_type}}
VALEUR : {{milestone_value}}
RÉCOMPENSE : {{reward}}
PERSONNALISATION : {{personalization}}

## 🎉 EMAIL MILESTONE/ANNIVERSAIRE

**Objet :** [Prénom], félicitations pour {{milestone_value}} ! 🎉

---

[Prénom],

**C'est un grand jour !**

{{milestone_type}} : **{{milestone_value}}** 🎉

{{personalization}}

**Pour célébrer, voici votre cadeau :**
🎁 {{reward}}

👉 [BOUTON : Récupérer mon cadeau]

Merci d'être là depuis le début. Vivement la suite !

[Signature]`
  },

  'unsubscribe-win-back': {
    fields: [
      { name: 'reason_staying', type: 'textarea', label: 'Raison de rester', required: true, placeholder: 'Valeur que vous apportez...' },
      { name: 'options', type: 'select', label: 'Options proposées', options: ['Réduire fréquence', 'Choisir les sujets', 'Pause temporaire', 'Aucune option'] },
      { name: 'last_chance_offer', type: 'text', label: 'Offre de dernière chance', placeholder: 'Ex: Contenu exclusif, réduction...' },
    ],
    promptTemplate: `Tu es expert en rétention d'abonnés.

RAISON DE RESTER : {{reason_staying}}
OPTIONS : {{options}}
OFFRE : {{last_chance_offer}}

## 👋 EMAIL RECONQUÊTE DÉSABONNÉ

### Page de désabonnement

**Titre :** Êtes-vous sûr(e) de vouloir partir ? 😢

---

[Prénom],

Avant de partir, on voulait vous dire...

{{reason_staying}}

**Peut-être préférez-vous :**
• Recevoir moins d'emails
• Choisir les sujets qui vous intéressent
• Faire une pause de 30 jours

👉 [BOUTON : Modifier mes préférences]

{{#if last_chance_offer}}
**Dernière chance :** {{last_chance_offer}}
👉 [BOUTON : Je reste !]
{{/if}}

---

👉 [Lien : Non merci, je me désinscris]

On respecte votre choix. 🙏

[Signature]`
  },

  'email-signature-generator': {
    fields: [
      { name: 'full_name', type: 'text', label: 'Nom complet', required: true },
      { name: 'job_title', type: 'text', label: 'Poste', required: true },
      { name: 'company', type: 'text', label: 'Entreprise', required: true },
      { name: 'phone', type: 'text', label: 'Téléphone' },
      { name: 'email', type: 'text', label: 'Email' },
      { name: 'website', type: 'text', label: 'Site web' },
      { name: 'social_links', type: 'text', label: 'Réseaux sociaux', placeholder: 'LinkedIn, Twitter...' },
      { name: 'style', type: 'select', label: 'Style', options: ['Minimaliste', 'Professionnel', 'Créatif', 'Corporate'] },
    ],
    promptTemplate: `Tu es expert en personal branding.

NOM : {{full_name}}
POSTE : {{job_title}}
ENTREPRISE : {{company}}
TÉLÉPHONE : {{phone}}
EMAIL : {{email}}
SITE : {{website}}
RÉSEAUX : {{social_links}}
STYLE : {{style}}

## ✍️ 3 SIGNATURES EMAIL

### Signature 1 : {{style}} - Standard

---

**{{full_name}}**
{{job_title}} | {{company}}

📧 {{email}}
📱 {{phone}}
🌐 {{website}}

[LinkedIn] [Twitter]

---

### Signature 2 : {{style}} - Avec CTA

---

**{{full_name}}**
{{job_title}} @ {{company}}

📞 {{phone}} | 🌐 {{website}}

📚 Téléchargez mon [ressource gratuite] →

---

### Signature 3 : {{style}} - Minimaliste

---

{{full_name}} · {{job_title}}
{{company}} · {{website}}

---

### 💡 BONNES PRATIQUES

✅ Max 4-5 lignes
✅ Une seule photo (ou logo)
✅ Liens cliquables
✅ Cohérence avec la marque
✅ Mobile-friendly

### 🎨 CODE HTML (à copier)

\`\`\`html
<table style="font-family: Arial, sans-serif; font-size: 14px;">
  <tr>
    <td style="padding-right: 15px;">
      [Photo/Logo]
    </td>
    <td>
      <b>{{full_name}}</b><br>
      {{job_title}} | {{company}}<br>
      {{phone}} | {{website}}
    </td>
  </tr>
</table>
\`\`\``
  },
};

// Config par défaut
const defaultFormConfig: FormConfig = {
  fields: [
    { name: 'input', type: 'textarea', label: 'Votre demande', required: true, placeholder: 'Décrivez ce que vous souhaitez générer...' },
    { name: 'email_type', type: 'select', label: 'Type d\'email', options: ['Newsletter', 'Promotionnel', 'Cold Email', 'Relance', 'Automatisé'] },
    { name: 'tone', type: 'select', label: 'Ton', options: ['Professionnel', 'Amical', 'Urgent', 'Inspirant'] },
  ],
  promptTemplate: `Génère un email marketing basé sur cette demande...`
};

export default function EmailToolPage({ params }: PageProps) {
  const tool = emailTools.find(t => t.slug === params.toolSlug);
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
          <Link href="/tools/email" className="text-orange-600 hover:underline">
            Retour aux outils Email Marketing
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

Voici le contenu généré basé sur vos paramètres:

${Object.entries(formData).map(([key, value]) => `**${key}**: ${value}`).join('\n')}

---

### Résultat Principal

Ce contenu a été généré par l'IA d'IAFactory Algeria pour optimiser vos campagnes email.

### Points Clés

1. **Taux d'ouverture optimisé** : Objets et preview testés pour maximiser l'engagement
2. **Conversion** : CTAs stratégiques et copywriting persuasif
3. **Délivrabilité** : Respecte les bonnes pratiques anti-spam

### Prochaines Étapes

- Personnalisez le contenu avec vos informations
- Testez A/B différentes versions
- Analysez les métriques

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
            <Link href="/tools/email" className="text-gray-400 hover:text-gray-600">
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
            <div className="w-14 h-14 bg-orange-100 rounded-xl flex items-center justify-center">
              <Mail className="w-7 h-7 text-orange-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{tool.name.fr}</h1>
              <p className="text-gray-600 mt-1">{tool.description.fr}</p>
              <div className="flex items-center gap-3 mt-3">
                <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-sm font-medium">
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
              <Sparkles className="w-5 h-5 text-orange-500" />
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
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    />
                  )}
                  {field.type === 'textarea' && (
                    <textarea
                      placeholder={field.placeholder}
                      required={field.required}
                      rows={3}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    />
                  )}
                  {field.type === 'select' && (
                    <select
                      required={field.required}
                      value={formData[field.name] || ''}
                      onChange={(e) => handleFieldChange(field.name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                    >
                      <option value="">Sélectionner...</option>
                      {field.options?.map((opt) => (
                        <option key={typeof opt === 'string' ? opt : opt.value} value={typeof opt === 'string' ? opt : opt.value}>
                          {typeof opt === 'string' ? opt : opt.label}
                        </option>
                      ))}
                    </select>
                  )}
                  {field.type === 'checkbox' && (
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formData[field.name] === 'true'}
                        onChange={(e) => handleFieldChange(field.name, e.target.checked ? 'true' : 'false')}
                        className="w-4 h-4 text-orange-600 rounded focus:ring-orange-500"
                      />
                      <span className="text-sm text-gray-600">{field.label}</span>
                    </label>
                  )}
                </div>
              ))}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-orange-600 text-white py-3 rounded-lg font-medium hover:bg-orange-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
                <Mail className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Le résultat apparaîtra ici</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
