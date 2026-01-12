# 🤖 Chatbots vs Workflows IA - IA Factory

> **Choisir le bon outil pour automatiser vos tâches**

IA Factory propose deux approches complémentaires pour créer des solutions d'intelligence artificielle personnalisées: les **Chatbots** pour les interactions conversationnelles et les **Workflows IA** pour l'automatisation complexe.

---

## 🎯 Deux Façons de Créer vos Solutions IA

### Plateforme Développeur

**Créer via notre plateforme de développement:**
```
http://localhost:8182/developer

Outils disponibles:
- Visual workflow builder
- Code editor (Python/JavaScript)
- Template library
- API integration
- Testing sandbox
- Deployment tools
```

**Pour qui:**
- Développeurs
- Équipes techniques
- Projets complexes
- Intégrations custom

---

### Deep Agent (Prompting)

**Utiliser le Deep Agent dans Studio Créatif:**
```
http://localhost:8184/studio
→ Menu "More"
→ "AI Engineer"

Approche:
- Description en langage naturel
- IA génère l'application automatiquement
- Itérations via conversation
- Déploiement en un clic
```

**Pour qui:**
- Non-développeurs
- Prototypage rapide
- Business users
- Expérimentation

---

## 💬 Chatbots: Simplifier les Conversations

### Qu'est-ce qu'un Chatbot?

**Les Chatbots sont conçus pour gérer des tâches conversationnelles.**

**Caractéristiques:**
- 🗣️ **Interface conversationnelle** - Questions/réponses naturelles
- 🎯 **Contexte spécifique** - Données métier intégrées
- 🔄 **Interactions continues** - Dialogue multi-tours
- 📊 **Réponses précises** - Basées sur connaissances fournies
- 🚀 **Déploiement rapide** - Minutes, pas jours

**Use cases idéaux:**
- Support client
- Recommandations produits
- Assistance interne équipe
- FAQ automatisées
- Onboarding utilisateurs
- Collecte d'informations

---

### Exemple Concret: Chatbot Engagement Santé

**Scénario:** Clinique médicale algérienne veut améliorer engagement patients

**Créer le Chatbot:**

```
Prompt au Deep Agent:
"Créer un chatbot pour clinique médicale qui:
1. Collecte informations sur services clinique
2. Comprend démographie patients (âge, ville, langue)
3. Définit objectifs engagement (satisfaction, suivi)
4. Génère plan personnalisé amélioration
5. Fournit contenu éducatif en français et arabe
6. Envoie rappels rendez-vous via SMS
7. Permet messagerie sécurisée patient-docteur"
```

**Résultat généré:**

```typescript
// Chatbot Healthcare Engagement - Auto-généré par Deep Agent

interface PatientProfile {
  id: string;
  nom: string;
  age: number;
  ville: string;
  langue: 'fr' | 'ar' | 'both';
  dernier_rdv: Date;
  historique_medical: string[];
}

class HealthcareEngagementBot {
  async handleMessage(message: string, patient: PatientProfile) {
    // Analyse intention
    const intent = await this.detectIntent(message);

    switch(intent) {
      case 'RAPPEL_RDV':
        return this.planifierRappel(patient);

      case 'INFO_MEDICALE':
        return this.fournirContenuEducatif(message, patient.langue);

      case 'SATISFACTION':
        return this.collecterFeedback(patient);

      case 'SUIVI_TRAITEMENT':
        return this.verifierCompliance(patient);

      default:
        return this.reponseGenerale(message);
    }
  }

  async planifierRappel(patient: PatientProfile) {
    // Générer rappel personnalisé
    const template = patient.langue === 'ar'
      ? 'تذكير: لديك موعد في {date} الساعة {time}'
      : 'Rappel: Vous avez rendez-vous le {date} à {time}';

    // Envoyer via Twilio SMS
    await this.envoyerSMS(patient.telephone, template);

    return {
      message: "Rappel programmé avec succès",
      date_envoi: this.calculerDateRappel(patient.dernier_rdv)
    };
  }

  async fournirContenuEducatif(sujet: string, langue: string) {
    // Rechercher dans base de connaissances médicale
    const contenu = await this.rechercherContenu(sujet, langue);

    return {
      titre: contenu.titre,
      resume: contenu.resume,
      liens_utiles: contenu.ressources,
      videos: contenu.videos_educatives,
      prochaines_etapes: contenu.recommendations
    };
  }

  async collecterFeedback(patient: PatientProfile) {
    return {
      message: "Comment évaluez-vous votre dernière visite?",
      options: [
        { label: "Très satisfait 😊", value: 5 },
        { label: "Satisfait 🙂", value: 4 },
        { label: "Neutre 😐", value: 3 },
        { label: "Insatisfait 😕", value: 2 },
        { label: "Très insatisfait 😞", value: 1 }
      ],
      callback: (rating) => this.enregistrerSatisfaction(patient, rating)
    };
  }
}
```

**Fonctionnalités du Chatbot:**

**1. Collecte d'Informations**
```
Bot: "Bonjour! Je suis l'assistant de la Clinique Al-Shifa.
      Comment puis-je vous aider aujourd'hui?"

Patient: "Je veux prendre rendez-vous"

Bot: "Parfait! Quel type de consultation?
      • Médecine générale
      • Cardiologie
      • Pédiatrie
      • Gynécologie"

Patient: "Cardiologie"

Bot: "Dr. Amina Benali (cardiologue) est disponible:
      • Lundi 22 janvier à 10h
      • Mercredi 24 janvier à 14h
      • Jeudi 25 janvier à 9h

      Laquelle préférez-vous?"
```

**2. Plan Personnalisé**
```
Basé sur profil patient:
- Âge: 55 ans
- Historique: Hypertension
- Langue: Français + Arabe

Plan généré:
✅ Rappels médicaments (SMS quotidien 8h)
✅ Contenu éducatif hypertension (vidéos FR/AR)
✅ Suivi tension (hebdomadaire via app)
✅ Rendez-vous contrôle (tous les 3 mois)
✅ Conseils nutrition personnalisés
```

**3. Contenu Éducatif**
```
Bot propose automatiquement:
📄 Articles: "Comprendre l'hypertension" (FR/AR)
🎥 Vidéos: "Exercices pour hypertendus" (sous-titres AR)
📊 Infographies: "Aliments à éviter"
📱 App recommendations: "Suivi tension artérielle"
```

**4. Rappels Automatiques**
```
SMS envoyés automatiquement:
- J-7: "Rappel: Rendez-vous Dr. Benali dans 7 jours"
- J-1: "Demain 10h: Consultation cardiologie"
- H-2: "Dans 2h: Rendez-vous Clinique Al-Shifa"
- Après: "Merci de votre visite! Comment s'est passé le rdv?"
```

**5. Messagerie Sécurisée**
```
Patient: "Puis-je envoyer mes résultats d'analyse au docteur?"

Bot: "Oui! Vous pouvez uploader vos résultats de manière sécurisée.
      📎 Cliquez ici pour joindre fichier (PDF/JPG/PNG)

      Vos documents seront chiffrés et accessibles uniquement
      au Dr. Benali."

[Upload interface]

Bot: "✅ Résultats reçus et transmis au Dr. Benali.
      Réponse attendue sous 24-48h."
```

**Résultats mesurés:**
- ✅ +45% satisfaction patients
- ✅ -30% rendez-vous manqués
- ✅ +60% compliance médicamenteuse
- ✅ -50% charge travail réception

---

### Avantages des Chatbots

**1. Personnalisation Élevée**
```
Intégration données contextuelles:
- Base de connaissances spécifique
- Données patients (HIPAA-compliant)
- Historique conversations
- Préférences utilisateur
- Langue maternelle
```

**2. Setup Rapide**
```
Timeline:
Jour 1: Description besoins au Deep Agent
Jour 2: Révision chatbot généré
Jour 3: Tests avec vrais utilisateurs
Jour 4: Ajustements finaux
Jour 5: Déploiement production

Total: 5 jours (vs 6-12 semaines dev classique)
```

**3. Scalabilité**
```
1 chatbot peut gérer:
- Conversations illimitées simultanées
- Multilingue (FR/AR/EN automatique)
- 24/7 disponibilité
- Aucune fatigue ou erreur humaine
```

---

## 🔄 Workflows IA: Automatiser les Opérations Complexes

### Qu'est-ce qu'un Workflow IA?

**Les Workflows IA (Agents) sont conçus pour effectuer des opérations avancées multi-étapes.**

**Caractéristiques:**
- 🔀 **Processus multi-étapes** - Orchestration complexe
- 🔌 **Intégrations externes** - API, bases de données, systèmes tiers
- 📄 **Traitement documents** - Extraction, analyse, transformation
- 🤖 **Automatisation complète** - Minimal intervention humaine
- 🧠 **Logique conditionnelle** - If/then/else avancé

**Use cases idéaux:**
- Automatisation workflows métier
- Traitement documents (contrats, factures)
- Intégration systèmes (CRM, ERP)
- Pipelines de données (ETL)
- Processus d'approbation
- Génération rapports automatiques

---

### Exemple Concret: Agent Salesforce

**Scénario:** Entreprise algérienne automatise création opportunités commerciales

**Créer le Workflow IA:**

```
Prompt au Deep Agent:
"Créer un agent Salesforce qui:
1. Reçoit requête utilisateur (nouveau prospect)
2. Valide et enrichit données (scoring qualité)
3. Crée opportunité Salesforce automatiquement
4. Assigne au bon commercial (selon région/secteur)
5. Génère tâches de suivi automatiques
6. Envoie notifications email équipe
7. Programme rappels selon SLA
8. Log toutes actions dans historique"
```

**Résultat généré:**

```python
# Salesforce Opportunity Agent - Auto-généré par Deep Agent

from salesforce_api import SalesforceClient
from enrichment import DataEnrichment
from scoring import LeadScoring
from notifications import EmailService, SlackService

class SalesforceOpportunityAgent:
    def __init__(self):
        self.sf = SalesforceClient(
            instance_url=os.getenv('SF_INSTANCE'),
            access_token=os.getenv('SF_TOKEN')
        )
        self.enrichment = DataEnrichment()
        self.scorer = LeadScoring()
        self.email = EmailService()
        self.slack = SlackService()

    async def process_lead(self, lead_data: dict):
        """
        Pipeline complet de traitement lead → opportunity
        """
        try:
            # Étape 1: Validation données
            validated_lead = await self.validate_lead(lead_data)

            # Étape 2: Enrichissement données
            enriched_lead = await self.enrich_lead(validated_lead)

            # Étape 3: Scoring qualité
            score = await self.score_lead(enriched_lead)

            # Étape 4: Vérification duplicates
            is_duplicate = await self.check_duplicates(enriched_lead)
            if is_duplicate:
                return self.handle_duplicate(enriched_lead)

            # Étape 5: Création opportunité Salesforce
            opportunity = await self.create_sf_opportunity(
                enriched_lead,
                score
            )

            # Étape 6: Assignment commercial
            sales_rep = await self.assign_sales_rep(
                enriched_lead.wilaya,
                enriched_lead.secteur
            )

            # Étape 7: Génération tâches
            tasks = await self.generate_tasks(opportunity, sales_rep)

            # Étape 8: Notifications
            await self.send_notifications(opportunity, sales_rep)

            # Étape 9: Programmation rappels
            await self.schedule_reminders(opportunity, sales_rep)

            # Étape 10: Logging
            await self.log_activity(opportunity, "created")

            return {
                "status": "success",
                "opportunity_id": opportunity.id,
                "assigned_to": sales_rep.name,
                "score": score,
                "next_actions": tasks
            }

        except Exception as e:
            await self.handle_error(e, lead_data)
            raise

    async def validate_lead(self, lead_data: dict):
        """Validation et nettoyage données"""
        required_fields = ['nom', 'entreprise', 'email', 'telephone']

        # Vérifier champs obligatoires
        for field in required_fields:
            if not lead_data.get(field):
                raise ValueError(f"Champ obligatoire manquant: {field}")

        # Nettoyer données
        cleaned = {
            'nom': lead_data['nom'].strip().title(),
            'entreprise': lead_data['entreprise'].strip(),
            'email': lead_data['email'].lower().strip(),
            'telephone': self.format_algerian_phone(lead_data['telephone']),
            'wilaya': lead_data.get('wilaya', 'Alger'),
            'secteur': lead_data.get('secteur', 'General')
        }

        # Valider email
        if not self.is_valid_email(cleaned['email']):
            raise ValueError(f"Email invalide: {cleaned['email']}")

        # Valider téléphone algérien
        if not cleaned['telephone'].startswith('+213'):
            raise ValueError(f"Numéro algérien requis: {cleaned['telephone']}")

        return cleaned

    async def enrich_lead(self, lead: dict):
        """Enrichissement avec données externes"""
        enriched = lead.copy()

        # Enrichir avec données entreprise (API externe)
        company_data = await self.enrichment.get_company_info(
            lead['entreprise']
        )

        if company_data:
            enriched.update({
                'taille_entreprise': company_data.get('employees', 'Unknown'),
                'secteur_activite': company_data.get('industry', lead['secteur']),
                'chiffre_affaires': company_data.get('revenue'),
                'site_web': company_data.get('website'),
                'linkedin': company_data.get('linkedin_url')
            })

        # Enrichir localisation
        wilaya_info = await self.get_wilaya_info(lead['wilaya'])
        enriched['region'] = wilaya_info['region']
        enriched['code_postal'] = wilaya_info['postal_code']

        return enriched

    async def score_lead(self, lead: dict):
        """Scoring qualité lead (0-100)"""
        score = 0

        # Critères scoring
        criteria = {
            'taille_entreprise': {
                '1-10': 10,
                '11-50': 20,
                '51-200': 30,
                '201-500': 40,
                '500+': 50
            },
            'secteur_activite': {
                'Tech': 40,
                'Finance': 35,
                'Santé': 30,
                'Éducation': 25,
                'General': 10
            },
            'wilaya': {
                'Alger': 30,
                'Oran': 25,
                'Constantine': 20,
                'Autres': 10
            },
            'data_completeness': 20  # Bonus si tous champs remplis
        }

        # Calculer score
        score += criteria['taille_entreprise'].get(
            lead.get('taille_entreprise', 'Unknown'), 0
        )
        score += criteria['secteur_activite'].get(
            lead.get('secteur_activite', 'General'), 10
        )
        score += criteria['wilaya'].get(lead['wilaya'], 10)

        # Bonus complétude données
        if self.is_complete(lead):
            score += criteria['data_completeness']

        return min(score, 100)  # Cap à 100

    async def create_sf_opportunity(self, lead: dict, score: int):
        """Création opportunité dans Salesforce"""

        # Déterminer stage selon score
        stage = self.get_initial_stage(score)

        opportunity_data = {
            'Name': f"{lead['entreprise']} - {lead['nom']}",
            'AccountName': lead['entreprise'],
            'ContactName': lead['nom'],
            'Email': lead['email'],
            'Phone': lead['telephone'],
            'LeadSource': 'IA Factory Agent',
            'StageName': stage,
            'Amount': self.estimate_amount(lead),
            'Probability': score,
            'CloseDate': self.calculate_close_date(score),
            'Description': self.generate_description(lead, score),
            'Wilaya__c': lead['wilaya'],  # Custom field
            'Secteur__c': lead['secteur_activite'],
            'Lead_Score__c': score
        }

        # Créer dans Salesforce
        result = await self.sf.create('Opportunity', opportunity_data)

        return result

    async def assign_sales_rep(self, wilaya: str, secteur: str):
        """Assignment intelligent au bon commercial"""

        # Règles d'assignment
        assignment_rules = {
            'Alger': {
                'Tech': 'karim.bensalem@example.dz',
                'Finance': 'amina.djelloul@example.dz',
                'default': 'sales.alger@example.dz'
            },
            'Oran': {
                'Tech': 'farid.meziane@example.dz',
                'default': 'sales.oran@example.dz'
            },
            'Constantine': {
                'default': 'sales.constantine@example.dz'
            },
            'default': 'sales@example.dz'
        }

        # Trouver commercial
        sales_email = (
            assignment_rules.get(wilaya, {}).get(secteur) or
            assignment_rules.get(wilaya, {}).get('default') or
            assignment_rules['default']
        )

        # Récupérer infos commercial depuis Salesforce
        sales_rep = await self.sf.query_user_by_email(sales_email)

        return sales_rep

    async def generate_tasks(self, opportunity, sales_rep):
        """Génération automatique tâches de suivi"""
        tasks = []

        # Tâche 1: Premier contact (J+1)
        tasks.append({
            'Subject': f"Premier contact - {opportunity.Name}",
            'Description': "Appeler le prospect pour introduction",
            'Status': 'Not Started',
            'Priority': 'High',
            'ActivityDate': datetime.now() + timedelta(days=1),
            'WhoId': opportunity.ContactId,
            'WhatId': opportunity.Id,
            'OwnerId': sales_rep.Id
        })

        # Tâche 2: Envoi documentation (J+2)
        tasks.append({
            'Subject': f"Envoyer doc commerciale - {opportunity.Name}",
            'Description': "Envoyer brochure et case studies",
            'Status': 'Not Started',
            'Priority': 'Normal',
            'ActivityDate': datetime.now() + timedelta(days=2),
            'WhatId': opportunity.Id,
            'OwnerId': sales_rep.Id
        })

        # Tâche 3: Démo produit (J+7)
        tasks.append({
            'Subject': f"Planifier démo - {opportunity.Name}",
            'Description': "Organiser démo IA Factory",
            'Status': 'Not Started',
            'Priority': 'High',
            'ActivityDate': datetime.now() + timedelta(days=7),
            'WhatId': opportunity.Id,
            'OwnerId': sales_rep.Id
        })

        # Créer tâches dans Salesforce
        for task in tasks:
            await self.sf.create('Task', task)

        return tasks

    async def send_notifications(self, opportunity, sales_rep):
        """Notifications multi-canal"""

        # Email au commercial
        await self.email.send(
            to=sales_rep.Email,
            subject=f"🎯 Nouvelle opportunité: {opportunity.Name}",
            template='new_opportunity',
            data={
                'opp_name': opportunity.Name,
                'score': opportunity.Lead_Score__c,
                'amount': opportunity.Amount,
                'wilaya': opportunity.Wilaya__c,
                'link': f"https://salesforce.com/{opportunity.Id}"
            }
        )

        # Slack au channel #sales
        await self.slack.send_message(
            channel='#sales',
            text=f"🚀 Nouvelle opportunité créée!\n"
                 f"• Entreprise: {opportunity.AccountName}\n"
                 f"• Score: {opportunity.Lead_Score__c}/100\n"
                 f"• Assigné à: {sales_rep.Name}\n"
                 f"• <https://salesforce.com/{opportunity.Id}|Voir dans SF>"
        )

    async def schedule_reminders(self, opportunity, sales_rep):
        """Programmation rappels automatiques"""

        # Rappel J+1: Premier contact
        await self.create_reminder(
            user_id=sales_rep.Id,
            opportunity_id=opportunity.Id,
            message="N'oubliez pas de contacter le prospect aujourd'hui!",
            send_at=datetime.now() + timedelta(days=1, hours=9)
        )

        # Rappel J+7: Si pas de mise à jour
        await self.create_conditional_reminder(
            opportunity_id=opportunity.Id,
            condition="stage_unchanged",
            days=7,
            message="Opportunité sans activité depuis 7 jours"
        )

        # Rappel J+30: Close date approche
        if opportunity.CloseDate:
            days_until_close = (opportunity.CloseDate - datetime.now()).days
            if days_until_close == 30:
                await self.create_reminder(
                    user_id=sales_rep.Id,
                    opportunity_id=opportunity.Id,
                    message="30 jours avant date de clôture prévue",
                    send_at=opportunity.CloseDate - timedelta(days=30)
                )

    async def log_activity(self, opportunity, action: str):
        """Logging complet dans historique"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'opportunity_id': opportunity.Id,
            'opportunity_name': opportunity.Name,
            'stage': opportunity.StageName,
            'score': opportunity.Lead_Score__c,
            'agent': 'SalesforceOpportunityAgent',
            'details': {
                'account': opportunity.AccountName,
                'amount': opportunity.Amount,
                'probability': opportunity.Probability
            }
        }

        # Log dans PostgreSQL (audit trail)
        await self.db.insert('agent_activity_log', log_entry)

        # Log dans Salesforce (historique opportunité)
        await self.sf.create('OpportunityHistory', {
            'OpportunityId': opportunity.Id,
            'StageName': opportunity.StageName,
            'CreatedById': 'AI_Agent',
            'CreatedDate': datetime.now()
        })
```

**Workflow Complet:**

```
┌─────────────────────────────────────────────────────────┐
│  Utilisateur Soumet Nouveau Prospect                    │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  1. VALIDATION DONNÉES                                  │
│  • Champs obligatoires présents?                        │
│  • Email valide?                                        │
│  • Téléphone algérien (+213)?                           │
│  ✅ OK → Continuer  ❌ Erreur → Retourner formulaire    │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  2. ENRICHISSEMENT DONNÉES                              │
│  • API entreprise → Taille, secteur, CA                 │
│  • Localisation → Région, code postal                   │
│  • LinkedIn → Profil company                            │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  3. SCORING QUALITÉ (0-100)                             │
│  • Taille entreprise: +20-50 pts                        │
│  • Secteur activité: +10-40 pts                         │
│  • Wilaya: +10-30 pts                                   │
│  • Complétude données: +20 pts                          │
│  Score final: 75/100 (High Quality)                     │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  4. VÉRIFICATION DUPLICATES                             │
│  • Recherche email dans SF                              │
│  • Recherche téléphone dans SF                          │
│  • Match trouvé? → Merge  Pas de match? → Créer        │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  5. CRÉATION OPPORTUNITÉ SALESFORCE                     │
│  • Name: "TechCorp Algeria - Ahmed Mansouri"            │
│  • Stage: "Qualification" (basé sur score 75)           │
│  • Amount: 500,000 DA (estimé)                          │
│  • Close Date: 30 mars 2025 (+60 jours)                 │
│  • Custom fields: Wilaya, Secteur, Score                │
│  ✅ Opportunity créée (ID: 006XXXXXXXXXXXX)             │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  6. ASSIGNMENT COMMERCIAL                               │
│  • Wilaya: Alger                                        │
│  • Secteur: Tech                                        │
│  • Assigné à: Karim Bensalem                            │
│  • Email: karim.bensalem@example.dz                     │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  7. GÉNÉRATION TÂCHES                                   │
│  ✅ J+1: Premier contact (High Priority)                │
│  ✅ J+2: Envoyer documentation (Normal)                 │
│  ✅ J+7: Planifier démo (High Priority)                 │
│  Toutes assignées à Karim                               │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  8. NOTIFICATIONS                                       │
│  📧 Email à karim.bensalem@example.dz                   │
│     "Nouvelle opportunité TechCorp (Score: 75/100)"     │
│  💬 Slack #sales                                        │
│     "🚀 Opp créée | TechCorp | Karim | Lien SF"         │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  9. RAPPELS AUTOMATIQUES                                │
│  ⏰ J+1, 9h: "Contacter prospect aujourd'hui"           │
│  ⏰ J+7: "Si stage inchangé → Alert manager"            │
│  ⏰ J-30 (avant close): "30j avant clôture prévue"      │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  10. LOGGING & AUDIT                                    │
│  • PostgreSQL: Audit trail complet                      │
│  • Salesforce: OpportunityHistory                       │
│  • Timestamp, action, user, details                     │
│  ✅ Traçabilité 100%                                    │
└─────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  ✅ WORKFLOW TERMINÉ AVEC SUCCÈS                        │
│  Durée: 3.2 secondes                                    │
│  Résultat: Opportunity ID 006XXXXXXXXXXXX               │
└─────────────────────────────────────────────────────────┘
```

**Résultats mesurés:**
- ✅ Temps création opportunity: 3s (vs 15 min manuel)
- ✅ Taux erreur données: -95%
- ✅ Assignment correct: 100%
- ✅ Suivi automatique: 100%
- ✅ ROI: 400% (1 agent = 4 sales ops)

---

### Avantages des Workflows IA

**1. Automatisation Complète**
```
Processus end-to-end sans intervention:
- Trigger: Formulaire web, email, webhook
- Processing: Validation, enrichissement, scoring
- Action: Création records, envoi notifications
- Follow-up: Tâches, rappels automatiques
- Reporting: Logs, analytics
```

**2. Intégrations Complexes**
```
Connexion multiple systèmes:
- Salesforce (CRM)
- PostgreSQL (database)
- APIs externes (enrichissement)
- Email (SendGrid)
- Slack (messaging)
- Calendrier (rappels)
```

**3. Logique Conditionnelle Avancée**
```python
if score > 80:
    stage = "Hot Lead"
    sla = 4  # heures
    priority = "Critical"
elif score > 60:
    stage = "Warm Lead"
    sla = 24
    priority = "High"
else:
    stage = "Cold Lead"
    sla = 72
    priority = "Normal"
```

---

## ⚖️ Chatbots vs Workflows: Choisir le Bon Outil

### Tableau Comparatif Détaillé

| Critère | Chatbots 💬 | Workflows IA 🔄 |
|---------|-------------|-----------------|
| **Use Case** | Tâches conversationnelles, FAQ, recommandations | Opérations complexes, traitement documents, automatisation |
| **Interface** | Chat (texte/voix) | Headless (API) ou UI custom |
| **Interaction** | Humain ↔ Bot | Système ↔ Agent ↔ Système(s) |
| **Personnalisation** | Élevée (intégration données contextuelles) | Très élevée (multi-step, conditionnelle) |
| **Setup Time** | Rapide (1-5 jours) | Moyen (5-15 jours) |
| **Complexité** | Simple à moyenne | Moyenne à très complexe |
| **Exemples** | Support client, onboarding, FAQ | ETL, intégrations CRM/ERP, document processing |
| **Déclencheur** | Message utilisateur | Event, schedule, webhook, API call |
| **Output** | Réponse texte/rich media | Données structurées, actions systèmes |
| **Scalabilité** | Conversations illimitées | Jobs illimités |
| **Monitoring** | Logs conversations | Logs workflow + metrics |

---

### Arbre de Décision

```
Votre besoin nécessite-t-il une interface conversationnelle?
│
├─ OUI → CHATBOT 💬
│   │
│   ├─ Support client
│   ├─ FAQ automatisée
│   ├─ Recommandations produits
│   ├─ Collecte informations
│   └─ Onboarding utilisateurs
│
└─ NON → Votre tâche implique-t-elle plusieurs systèmes?
    │
    ├─ OUI → WORKFLOW IA 🔄
    │   │
    │   ├─ Intégration CRM/ERP
    │   ├─ Synchronisation données
    │   ├─ Processus approbation
    │   └─ Pipeline ETL
    │
    └─ NON → Votre tâche est-elle multi-étapes?
        │
        ├─ OUI → WORKFLOW IA 🔄
        │   │
        │   ├─ Document processing
        │   ├─ Rapports automatiques
        │   ├─ Workflow approbation
        │   └─ Orchestration complexe
        │
        └─ NON → Démarrez avec CHATBOT 💬
            (Plus simple, évolutif vers Workflow si besoin)
```

---

### Quand Utiliser les Deux?

**Approche Hybride Recommandée:**

**Exemple: Plateforme E-commerce**

**Chatbot (Frontend):**
```
- Support client 24/7
- Recommandations produits
- Suivi commandes
- Retours/SAV

Interface utilisateur conversationnelle
```

**Workflow IA (Backend):**
```
- Traitement commandes
- Gestion stock (auto-reorder)
- Facturation automatique
- Sync avec comptabilité
- Génération rapports ventes
- Prédiction demande

Automatisation invisible pour utilisateur
```

**Communication:**
```
Chatbot Frontend
      ↓
   API Call
      ↓
Workflow Backend
      ↓
  Processing
      ↓
   Response
      ↓
Chatbot affiche résultat
```

**Exemple concret:**
```
Client (via Chatbot): "Où est ma commande #12345?"

Chatbot → API → Workflow IA:
  1. Query database commande
  2. Check statut livraison (API transporteur)
  3. Récupérer tracking number
  4. Estimer livraison
  5. Formater réponse

Workflow → API → Chatbot:
  "Votre commande est en transit.
   Livraison prévue demain entre 9h-17h.
   Tracking: DZ123456789
   [Lien suivi temps réel]"
```

---

## 🛠️ Comment Créer?

### Via Deep Agent (No-Code)

**Pour Chatbot:**
```
http://localhost:8184/studio
→ "AI Engineer"
→ "Create Chatbot"

Prompt:
"Créer un chatbot support client pour e-commerce qui:
- Répond aux questions sur produits
- Suit les commandes
- Gère les retours
- Escalade vers humain si nécessaire
- Supporte français et arabe"

→ Deep Agent génère chatbot complet
→ Test dans sandbox
→ Déploiement production
```

**Pour Workflow:**
```
http://localhost:8184/studio
→ "AI Engineer"
→ "Create Workflow"

Prompt:
"Créer un workflow qui:
1. Reçoit nouvelle commande (webhook)
2. Valide stock disponible
3. Crée facture automatique
4. Envoie email confirmation
5. Update CRM (HubSpot)
6. Programme rappel suivi J+7"

→ Deep Agent génère workflow
→ Test avec données mock
→ Connecter systèmes production
→ Déploiement
```

---

### Via Plateforme Développeur (Code)

**Pour Chatbot:**
```python
# chatbot_config.yaml
name: "Support E-commerce"
model: "gpt-4o"
temperature: 0.7
max_tokens: 500

knowledge_base:
  - source: "docs/faq.md"
  - source: "database:products"
  - source: "api:orders"

intents:
  - name: "track_order"
    examples:
      - "Où est ma commande?"
      - "Statut commande #12345"
    action: "call_order_api"

  - name: "product_info"
    examples:
      - "Info sur produit X"
      - "Prix de Y?"
    action: "query_product_db"

escalation:
  trigger: "intent:human_agent"
  action: "create_zendesk_ticket"
```

**Pour Workflow:**
```python
# workflow_definition.py
from iafactory import Workflow, Task

workflow = Workflow(name="Order Processing")

@workflow.task(trigger="webhook:/orders/new")
async def validate_stock(order_data):
    # Check stock
    product = await db.products.find_one({"id": order_data['product_id']})
    if product['stock'] < order_data['quantity']:
        raise InsufficientStockError()
    return order_data

@workflow.task(depends_on=[validate_stock])
async def create_invoice(order_data):
    invoice = await billing.create_invoice(order_data)
    return {**order_data, 'invoice_id': invoice.id}

@workflow.task(depends_on=[create_invoice])
async def send_confirmation(order_data):
    await email.send(
        to=order_data['customer_email'],
        template='order_confirmation',
        data=order_data
    )

@workflow.task(depends_on=[send_confirmation])
async def update_crm(order_data):
    await hubspot.create_deal(order_data)

@workflow.schedule(task=send_reminder, delay="7 days")
async def send_reminder(order_data):
    await email.send(
        to=order_data['customer_email'],
        template='satisfaction_survey',
        data=order_data
    )

# Deploy
workflow.deploy(environment="production")
```

---

## ✅ Checklist de Choix

### Choisir Chatbot si:

- [ ] Besoin interface conversationnelle
- [ ] Support client/FAQ
- [ ] Collecte informations via dialogue
- [ ] Réponses immédiates requises
- [ ] Multilingue important
- [ ] Setup rapide prioritaire
- [ ] Non-technique peut gérer

### Choisir Workflow IA si:

- [ ] Processus multi-étapes complexe
- [ ] Intégration systèmes multiples
- [ ] Traitement documents automatisé
- [ ] Logique conditionnelle avancée
- [ ] Aucune interaction humaine nécessaire
- [ ] Scheduling/batch processing
- [ ] Audit trail requis

### Combiner les deux si:

- [ ] Frontend conversationnel + Backend automatisé
- [ ] Chatbot trigger workflows
- [ ] Workflows notifient via chatbot
- [ ] Expérience utilisateur fluide requise
- [ ] Automatisation end-to-end

---

## 📚 Ressources

### Documentation

- 📖 [Deep Agent Guide](./GUIDE_UTILISATION_BMAD.md)
- 📖 [Playground](./PLAYGROUND_GUIDE.md)
- 📖 [Tâches Automatisées](./TACHES_AUTOMATISEES.md)
- 📖 [API Reference](http://localhost:8180/docs)

### Templates

**Chatbots:**
- Support Client E-commerce
- FAQ Entreprise
- Onboarding Employés
- Réservation Rendez-vous
- Assistant RH

**Workflows:**
- Salesforce Opportunity Creation
- Invoice Processing (OCR + Data Entry)
- Contract Review & Approval
- Customer Onboarding Automation
- Reporting Dashboard (Scheduled)

### Support

- 📧 workflows@iafactory.dz
- 💬 Chat: http://localhost:8182/support
- 📞 Tél: +213 XXX XXX XXX

---

**Version**: 1.0.0
**Dernière mise à jour**: 2025-01-18

🇩🇿 **IA Factory Algeria - Chatbots Intelligents, Workflows Puissants**

---

Copyright © 2025 IA Factory Algeria. Tous droits réservés.
