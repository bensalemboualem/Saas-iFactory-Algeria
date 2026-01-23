import { AITool } from '../../types';

export const partnershipProposal: AITool = {
  id: 'partnership-proposal',
  slug: 'partnership-proposal',
  name: { fr: 'Proposition de Partenariat', ar: 'عرض الشراكة', en: 'Partnership Proposal' },
  description: {
    fr: 'Créez des propositions de partenariat convaincantes pour développer votre réseau',
    ar: 'أنشئ عروض شراكة مقنعة لتطوير شبكتك',
    en: 'Create convincing partnership proposals to grow your network'
  },
  category: 'business',
  subcategory: 'documents',
  icon: 'Handshake',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'your_company', type: 'text', label: 'Votre entreprise', required: true },
    { name: 'partner_company', type: 'text', label: 'Entreprise partenaire visée', required: true },
    { name: 'partnership_type', type: 'select', label: 'Type de partenariat', options: [
      'Commercial (co-selling)',
      'Marketing (co-marketing)',
      'Technologique (intégration)',
      'Distribution',
      'Stratégique',
      'Affiliation'
    ]},
    { name: 'value_for_partner', type: 'textarea', label: 'Valeur pour le partenaire' },
    { name: 'value_for_you', type: 'textarea', label: 'Valeur pour vous' },
    { name: 'proposed_activities', type: 'textarea', label: 'Activités proposées' }
  ],
  outputs: [{ type: 'markdown', name: 'proposal' }],
  promptTemplate: `Tu es un expert en développement de partenariats stratégiques.

VOTRE ENTREPRISE : {{your_company}}
PARTENAIRE VISÉ : {{partner_company}}
TYPE : {{partnership_type}}
VALEUR PARTENAIRE : {{value_for_partner}}
VALEUR POUR VOUS : {{value_for_you}}
ACTIVITÉS : {{proposed_activities}}

## 🤝 PROPOSITION DE PARTENARIAT

---

# PROPOSITION DE PARTENARIAT
## {{your_company}} × {{partner_company}}

**Date :** [Date]
**Préparée par :** [Nom], [Titre]
**Contact :** [Email] | [Téléphone]

---

## RÉSUMÉ EXÉCUTIF

[2-3 phrases résumant l'opportunité de partenariat et les bénéfices mutuels]

---

## 1. QUI SOMMES-NOUS ?

### {{your_company}}

**En bref :**
[Description courte de votre entreprise]

**Chiffres clés :**
- 📊 [Métrique 1 : clients, CA, croissance...]
- 👥 [Métrique 2 : audience, utilisateurs...]
- 🏆 [Réalisation notable]

**Notre expertise :**
- [Compétence 1]
- [Compétence 2]
- [Compétence 3]

---

## 2. POURQUOI {{partner_company}} ?

Nous avons identifié {{partner_company}} comme partenaire idéal car :

✅ **Complémentarité :** [Explication]
✅ **Audience commune :** [Explication]
✅ **Valeurs alignées :** [Explication]
✅ **Synergies potentielles :** [Explication]

---

## 3. L'OPPORTUNITÉ

### Le constat
[Problème ou opportunité du marché]

### La solution : un partenariat {{partnership_type}}
[Comment le partenariat répond à cette opportunité]

---

## 4. CE QUE NOUS PROPOSONS

### 4.1 Activités du partenariat

{{#if partnership_type.includes('Marketing')}}
**Co-Marketing :**
- 📝 Co-création de contenus (webinars, articles, études)
- 📧 Cross-promotion email
- 📱 Campagnes social media conjointes
- 🎤 Events co-brandés
{{/if}}

{{#if partnership_type.includes('Commercial')}}
**Co-Selling :**
- 🤝 Référencement mutuel de clients
- 📦 Offres bundlées
- 💰 Commission sur ventes référées
- 🎯 Leads partagés
{{/if}}

{{#if partnership_type.includes('Technologique')}}
**Intégration Technologique :**
- 🔗 Intégration API
- 📲 Connecteur natif
- 🛠️ Développement conjoint
- 📚 Documentation commune
{{/if}}

### 4.2 Engagements mutuels

| {{your_company}} s'engage à | {{partner_company}} s'engage à |
|-----------------------------|--------------------------------|
| [Engagement 1] | [Engagement attendu 1] |
| [Engagement 2] | [Engagement attendu 2] |
| [Engagement 3] | [Engagement attendu 3] |

---

## 5. BÉNÉFICES POUR {{partner_company}}

🎯 **Pour vous :**

1. **[Bénéfice 1]**
   → [Détail et quantification]

2. **[Bénéfice 2]**
   → [Détail et quantification]

3. **[Bénéfice 3]**
   → [Détail et quantification]

**ROI estimé :** [Estimation]

---

## 6. MODÈLE ÉCONOMIQUE

### Option A : [Nom du modèle]
- [Description]
- Partage : [X/X]

### Option B : [Nom du modèle]
- [Description]
- Commission : [X%]

---

## 7. ROADMAP PROPOSÉE

| Phase | Durée | Actions | Objectifs |
|-------|-------|---------|-----------|
| Pilote | 3 mois | [Actions] | [KPIs] |
| Déploiement | 6 mois | [Actions] | [KPIs] |
| Optimisation | Ongoing | [Actions] | [KPIs] |

---

## 8. PROCHAINES ÉTAPES

1. 📞 Call de découverte (30 min)
2. 🤝 Rencontre équipes
3. 📝 Définition du scope
4. ✍️ Signature accord
5. 🚀 Lancement pilote

**Disponibilité :** [Dates proposées]

---

## 9. RÉFÉRENCES

### Partenariats existants
- [Partenaire 1] - [Type] - [Résultat]
- [Partenaire 2] - [Type] - [Résultat]

### Témoignage
> "[Citation d'un partenaire actuel]"
> — [Nom], [Titre], [Entreprise]

---

**CONTACT**

[Nom]
[Titre]
{{your_company}}

📧 [Email]
📱 [Téléphone]
🔗 [LinkedIn]

---

*Nous sommes convaincus que ce partenariat créera une valeur significative pour nos deux entreprises. Au plaisir d'en discuter !*`,
  model: 'gpt4',
  estimatedTime: '60s'
};

export const pressReleaseGenerator: AITool = {
  id: 'press-release-generator',
  slug: 'press-release-generator',
  name: { fr: 'Générateur de Communiqué de Presse', ar: 'مولد البيان الصحفي', en: 'Press Release Generator' },
  description: {
    fr: 'Rédigez des communiqués de presse professionnels pour vos annonces',
    ar: 'اكتب بيانات صحفية احترافية لإعلاناتك',
    en: 'Write professional press releases for your announcements'
  },
  category: 'business',
  subcategory: 'marketing',
  icon: 'Newspaper',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'announcement_type', type: 'select', label: 'Type d\'annonce', options: [
      'Lancement produit',
      'Levée de fonds',
      'Partenariat',
      'Acquisition',
      'Milestone/Record',
      'Événement',
      'Nomination',
      'Expansion'
    ]},
    { name: 'headline', type: 'text', label: 'Titre principal', required: true },
    { name: 'key_facts', type: 'textarea', label: 'Faits clés à communiquer', required: true },
    { name: 'quote_person', type: 'text', label: 'Personne citée (Nom, Titre)' },
    { name: 'quote_content', type: 'textarea', label: 'Citation' },
    { name: 'release_date', type: 'text', label: 'Date de publication' }
  ],
  outputs: [{ type: 'markdown', name: 'press_release' }],
  promptTemplate: `Tu es un expert en relations presse et communication corporate.

ENTREPRISE : {{company_name}}
TYPE : {{announcement_type}}
TITRE : {{headline}}
FAITS : {{key_facts}}
CITATION PAR : {{quote_person}}
CITATION : {{quote_content}}
DATE : {{release_date}}

## 📰 COMMUNIQUÉ DE PRESSE

---

**COMMUNIQUÉ DE PRESSE**
{{#if release_date === 'immediate'}}
**Pour diffusion immédiate**
{{else}}
**Embargo jusqu'au {{release_date}}**
{{/if}}

---

# {{headline}}

**[Sous-titre accrocheur résumant l'annonce]**

---

**[Ville], le [Date]** — {{company_name}} [verbe d'action] [annonce principale en une phrase percutante].

[Paragraphe 1 : Développement de l'annonce - Quoi, Qui, Quand, Où, Pourquoi]

[Paragraphe 2 : Contexte et importance de l'annonce]

{{#if announcement_type.includes('Levée')}}
Cette levée de fonds de [montant] a été menée par [investisseur lead], avec la participation de [autres investisseurs]. Les fonds seront utilisés pour [objectifs : recrutement, R&D, expansion...].
{{/if}}

{{#if announcement_type.includes('Lancement')}}
[Nom du produit] permet à [audience cible] de [bénéfice principal]. Parmi les fonctionnalités clés : [liste des features principales].
{{/if}}

---

**« {{quote_content}} »** déclare {{quote_person}}.

---

[Paragraphe 3 : Détails supplémentaires, chiffres, impact]

[Paragraphe 4 : Prochaines étapes ou disponibilité]

---

### À PROPOS DE {{company_name | uppercase}}

{{company_name}} est [description factuelle de l'entreprise en 2-3 phrases]. Fondée en [année], l'entreprise [activité principale]. [Chiffre clé ou fait notable].

Pour plus d'informations : [site web]

---

### CONTACT PRESSE

**[Nom du contact]**
[Titre]
📧 [Email presse]
📱 [Téléphone]

---

### RESSOURCES

- 🖼️ Kit presse : [Lien]
- 📸 Photos HD : [Lien]
- 🎥 Vidéo : [Lien si applicable]

---

**###**

*[Note aux rédacteurs si nécessaire]*

---

## VERSIONS ALTERNATIVES

### Version courte (100 mots)
*Pour : Dépêches, réseaux sociaux*

"{{company_name}} annonce [annonce] [date]. [Détail principal]. [Citation courte]. [Call-to-action]."

### Version email pitch journaliste

**Objet :** [Accroche journalistique] - {{company_name}}

"Bonjour [Prénom],

[1 phrase d'accroche personnalisée]

{{company_name}} vient de [annonce] et je pense que cela pourrait intéresser vos lecteurs car [angle éditorial].

**En bref :**
- [Fait 1]
- [Fait 2]
- [Fait 3]

Je serais ravi de vous envoyer le communiqué complet ou d'organiser une interview avec [porte-parole].

Cordialement,
[Signature]"`,
  model: 'gpt4',
  estimatedTime: '45s'
};

export const jobDescriptionGenerator: AITool = {
  id: 'job-description-generator',
  slug: 'job-description-generator',
  name: { fr: 'Générateur de Fiches de Poste', ar: 'مولد توصيف الوظائف', en: 'Job Description Generator' },
  description: {
    fr: 'Créez des offres d\'emploi attractives qui attirent les meilleurs talents',
    ar: 'أنشئ عروض عمل جذابة تجذب أفضل المواهب',
    en: 'Create attractive job postings that attract top talent'
  },
  category: 'business',
  subcategory: 'hr',
  icon: 'UserPlus',
  credits: 12,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'job_title', type: 'text', label: 'Intitulé du poste', required: true },
    { name: 'department', type: 'text', label: 'Département/Équipe' },
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'location', type: 'text', label: 'Localisation' },
    { name: 'contract_type', type: 'select', label: 'Type de contrat', options: ['CDI', 'CDD', 'Freelance', 'Stage', 'Alternance'] },
    { name: 'experience_level', type: 'select', label: 'Niveau d\'expérience', options: ['Junior', 'Confirmé', 'Senior', 'Lead', 'Executive'] },
    { name: 'responsibilities', type: 'textarea', label: 'Missions principales', required: true },
    { name: 'requirements', type: 'textarea', label: 'Compétences requises' },
    { name: 'salary_range', type: 'text', label: 'Fourchette de salaire (optionnel)' },
    { name: 'benefits', type: 'textarea', label: 'Avantages' }
  ],
  outputs: [{ type: 'markdown', name: 'job_description' }],
  promptTemplate: `Tu es un expert en recrutement et marque employeur.

POSTE : {{job_title}}
DÉPARTEMENT : {{department}}
ENTREPRISE : {{company_name}}
LIEU : {{location}}
CONTRAT : {{contract_type}}
NIVEAU : {{experience_level}}
MISSIONS : {{responsibilities}}
COMPÉTENCES : {{requirements}}
SALAIRE : {{salary_range}}
AVANTAGES : {{benefits}}

## 👔 OFFRE D'EMPLOI

---

# {{job_title}}
## {{company_name}} | {{location}}

**Type :** {{contract_type | uppercase}}
**Expérience :** {{experience_level}}
**Département :** {{department}}
{{#if salary_range}}**Rémunération :** {{salary_range}}{{/if}}

---

### 🚀 REJOIGNEZ L'AVENTURE {{company_name | uppercase}} !

[Accroche engageante sur l'entreprise et le contexte du recrutement]

---

### 🎯 VOTRE MISSION

En tant que {{job_title}}, vous serez responsable de :

**Responsabilités principales :**
- [Mission 1 - avec impact attendu]
- [Mission 2 - avec impact attendu]
- [Mission 3 - avec impact attendu]
- [Mission 4 - avec impact attendu]
- [Mission 5 - avec impact attendu]

**Au quotidien, vous allez :**
- [Activité quotidienne 1]
- [Activité quotidienne 2]
- [Activité quotidienne 3]

---

### 👤 VOTRE PROFIL

**Indispensable :**
- ✅ [Compétence requise 1]
- ✅ [Compétence requise 2]
- ✅ [Compétence requise 3]
- ✅ [X] années d'expérience en [domaine]

**Un plus :**
- ➕ [Compétence bonus 1]
- ➕ [Compétence bonus 2]
- ➕ [Compétence bonus 3]

**Soft skills :**
- 💡 [Qualité 1]
- 🤝 [Qualité 2]
- 📈 [Qualité 3]

---

### 🎁 CE QUE NOUS OFFRONS

{{#if salary_range}}
💰 **Rémunération :** {{salary_range}}
{{/if}}

**Avantages :**
- [Avantage 1 : Télétravail, RTT...]
- [Avantage 2 : Tickets resto, mutuelle...]
- [Avantage 3 : Formation, évolution...]
- [Avantage 4 : Équipe, culture...]
- [Avantage 5 : Équipement, bureaux...]

---

### 🏢 POURQUOI {{company_name | uppercase}} ?

**Notre culture :**
[Description de la culture d'entreprise]

**Nos valeurs :**
- [Valeur 1]
- [Valeur 2]
- [Valeur 3]

**Témoignage équipe :**
> "[Citation d'un membre de l'équipe]"
> — [Prénom], [Poste]

---

### 📝 PROCESSUS DE RECRUTEMENT

1. 📞 Échange téléphonique (15 min)
2. 💻 Entretien visio RH (45 min)
3. 🎯 Entretien technique/métier (1h)
4. 🤝 Rencontre équipe (30 min)
5. ✅ Offre

**Délai moyen :** [X] semaines

---

### 📩 POSTULER

Envoyez votre CV et lettre de motivation à : [email]

Ou postulez directement sur : [lien]

---

*{{company_name}} s'engage en faveur de la diversité et de l'égalité des chances. Tous nos postes sont ouverts aux personnes en situation de handicap.*

---

## VERSION LINKEDIN

**[Version optimisée pour LinkedIn Jobs - 2000 caractères]**

## VERSION INDEED

**[Version optimisée pour Indeed - avec mots-clés]**`,
  model: 'gpt4',
  estimatedTime: '30s'
};

export const onboardingChecklist: AITool = {
  id: 'onboarding-checklist',
  slug: 'onboarding-checklist',
  name: { fr: 'Checklist d\'Onboarding', ar: 'قائمة تأهيل الموظفين', en: 'Onboarding Checklist' },
  description: {
    fr: 'Créez un parcours d\'intégration complet pour vos nouveaux collaborateurs',
    ar: 'أنشئ مسار إدماج شامل لموظفيك الجدد',
    en: 'Create a comprehensive onboarding journey for new hires'
  },
  category: 'business',
  subcategory: 'hr',
  icon: 'CheckCircle',
  credits: 15,
  priority: 'medium',
  isAlgeriaExclusive: false,
  inputs: [
    { name: 'company_name', type: 'text', label: 'Nom de l\'entreprise', required: true },
    { name: 'role_type', type: 'select', label: 'Type de poste', options: [
      'Tech/IT',
      'Commercial/Sales',
      'Marketing',
      'Opérations',
      'RH',
      'Finance',
      'Général'
    ]},
    { name: 'company_size', type: 'select', label: 'Taille entreprise', options: ['Startup', 'PME', 'ETI', 'Grande Entreprise'] },
    { name: 'onboarding_duration', type: 'select', label: 'Durée de l\'onboarding', options: ['1 semaine', '2 semaines', '1 mois', '3 mois'] },
    { name: 'remote_hybrid', type: 'select', label: 'Mode de travail', options: ['Présentiel', 'Hybride', 'Full Remote'] }
  ],
  outputs: [{ type: 'markdown', name: 'checklist' }],
  promptTemplate: `Tu es un expert RH en expérience collaborateur et onboarding.

ENTREPRISE : {{company_name}}
TYPE POSTE : {{role_type}}
TAILLE : {{company_size}}
DURÉE : {{onboarding_duration}}
MODE : {{remote_hybrid}}

## ✅ PARCOURS D'ONBOARDING

---

# PARCOURS D'INTÉGRATION
## {{company_name}}

**Nouveau collaborateur :** [Nom]
**Poste :** [Intitulé]
**Date d'arrivée :** [Date]
**Manager :** [Nom du manager]
**Buddy :** [Nom du buddy]

---

## 📅 AVANT L'ARRIVÉE (J-7 à J-1)

### Pour le Manager
- [ ] Préparer le poste de travail
- [ ] Commander le matériel informatique
- [ ] Créer les accès (email, outils, badges)
- [ ] Prévenir l'équipe de l'arrivée
- [ ] Planifier les premières réunions
- [ ] Désigner un buddy

### Pour les RH
- [ ] Envoyer le welcome pack / email de bienvenue
- [ ] Préparer le contrat et documents administratifs
- [ ] Planifier la session RH
- [ ] Ajouter au planning de paie

### Pour l'IT
- [ ] Configurer le poste de travail
- [ ] Créer les comptes (email, Slack, outils métier)
- [ ] Préparer les accès VPN si {{remote_hybrid}} !== 'Présentiel'

---

## 🎉 JOUR 1

### Matin

| Heure | Activité | Responsable | Lieu |
|-------|----------|-------------|------|
| 09:00 | ☕ Accueil café | Manager | Hall |
| 09:30 | 📝 Formalités RH | RH | Bureau RH |
| 10:30 | 💻 Installation poste | IT | Bureau |
| 11:30 | 🏢 Visite des locaux | Buddy | Tous les étages |

### Après-midi

| Heure | Activité | Responsable |
|-------|----------|-------------|
| 14:00 | 👥 Présentation à l'équipe | Manager |
| 14:30 | 🎯 Présentation du poste et objectifs | Manager |
| 15:30 | 🛠️ Configuration outils | Buddy |
| 16:30 | ☕ Café avec le buddy | Buddy |
| 17:00 | 📋 Débrief de la journée | Manager |

### Checklist Jour 1
- [ ] Badge/accès remis
- [ ] Poste de travail fonctionnel
- [ ] Email configuré
- [ ] Outils principaux installés
- [ ] Présentation équipe faite
- [ ] Déjeuner avec l'équipe
- [ ] Buddy identifié

---

## 📆 SEMAINE 1

### Objectifs
- Comprendre l'entreprise et sa culture
- Maîtriser les outils de base
- Rencontrer les interlocuteurs clés
- Commencer les premières tâches

### Planning

| Jour | Focus | Activités |
|------|-------|-----------|
| J1 | Intégration | Accueil, admin, découverte |
| J2 | Culture | Présentation valeurs, histoire |
| J3 | Produit | Démo produit/service |
| J4 | Process | Outils et méthodes de travail |
| J5 | Équipe | 1:1 avec membres de l'équipe |

### Checklist Semaine 1
- [ ] Tous les accès fonctionnels
- [ ] Organigramme compris
- [ ] Valeurs de l'entreprise présentées
- [ ] Produit/service démontré
- [ ] Premiers objectifs fixés
- [ ] Point avec le manager
- [ ] Feedback recueilli

---

## 📆 MOIS 1

### Semaine 2
- [ ] Formation métier approfondie
- [ ] Premières missions autonomes
- [ ] Rencontre avec les autres départements
- [ ] Point buddy hebdo

### Semaine 3
- [ ] Montée en charge progressive
- [ ] Participation aux rituels d'équipe
- [ ] 1:1 manager hebdomadaire
- [ ] Retour sur les premières missions

### Semaine 4
- [ ] Bilan du premier mois
- [ ] Ajustement des objectifs
- [ ] Feedback 360° informel
- [ ] Plan pour le mois 2

### Checklist Mois 1
- [ ] Toutes les formations de base terminées
- [ ] Autonome sur les tâches courantes
- [ ] Intégré à l'équipe
- [ ] Objectifs du mois compris
- [ ] Rapport d'étonnement rédigé
- [ ] Point RH "1 mois"

---

## 📆 MOIS 2-3

### Objectifs
- Autonomie croissante
- Contribution significative
- Développement des compétences
- Intégration culturelle complète

### Checklist
- [ ] Responsable de projets/missions
- [ ] Feedback régulier du manager
- [ ] Participation aux événements d'entreprise
- [ ] Objectifs de période d'essai définis
- [ ] Point à mi-période d'essai
- [ ] Bilan de fin de période d'essai

---

## 📊 SUIVI & FEEDBACK

### Points de suivi

| Échéance | Type | Participants |
|----------|------|--------------|
| J+1 | Débrief jour 1 | Manager |
| J+7 | Point semaine 1 | Manager + RH |
| J+30 | Bilan mois 1 | Manager + RH |
| J+60 | Mi-période d'essai | Manager + RH |
| J+90 | Fin période d'essai | Manager + RH + N+2 |

### Rapport d'étonnement
*À remplir par le nouveau collaborateur après 1 mois*

1. Ce qui m'a positivement surpris :
2. Ce qui pourrait être amélioré :
3. Questions encore en suspens :
4. Suggestions :

---

## 📚 RESSOURCES

### Documents à lire
- [ ] Règlement intérieur
- [ ] Charte informatique
- [ ] Politique de congés
- [ ] Process [spécifique métier]

### Formations obligatoires
- [ ] Sécurité
- [ ] RGPD
- [ ] Outils internes
- [ ] [Formation métier]

### Contacts utiles
| Service | Contact | Email |
|---------|---------|-------|
| RH | [Nom] | [Email] |
| IT Support | [Nom] | [Email] |
| Office Manager | [Nom] | [Email] |

---

**Signature manager :** _________________ Date : _______
**Signature collaborateur :** _________________ Date : _______`,
  model: 'gpt4',
  estimatedTime: '45s'
};
