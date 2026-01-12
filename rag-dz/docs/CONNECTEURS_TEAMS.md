# 🔌 Connecteurs Teams IA Factory

Guide complet pour connecter vos applications et données à IA Factory Teams.

---

## 📑 Table des Matières

1. [Introduction](#introduction)
2. [Qu'est-ce que IA Factory Teams ?](#quest-ce-que-ia-factory-teams-)
3. [Connecteurs First-Party](#connecteurs-first-party)
4. [Configuration Rapide](#configuration-rapide)
5. [Connecteurs Disponibles](#connecteurs-disponibles)
6. [Guide de Configuration par Connecteur](#guide-de-configuration-par-connecteur)
7. [Utilisation avec Chatbots et BMAD](#utilisation-avec-chatbots-et-bmad)
8. [Gestion des Connexions](#gestion-des-connexions)
9. [Sécurité et Permissions](#sécurité-et-permissions)
10. [Cas d'Usage Entreprise](#cas-dusage-entreprise)
11. [Dépannage](#dépannage)

---

## 🎯 Introduction

IA Factory offre une **méthode simple et sécurisée** pour connecter vos applications, bases de données et services cloud à **IA Factory Teams**. Une fois configurés, tous vos chatbots et agents BMAD peuvent interroger ces données intelligemment via des prompts en langage naturel.

### Pourquoi Utiliser les Connecteurs Teams ?

✅ **Configuration en 2 clics** - Interface intuitive, pas de code requis
✅ **Sécurité Enterprise** - OAuth 2.0, chiffrement end-to-end, audit complet
✅ **Données en temps réel** - Accès direct sans synchronisation
✅ **Multi-sources** - Combinez données de plusieurs connecteurs dans une seule requête
✅ **Permissions granulaires** - Contrôlez qui accède à quoi
✅ **Algérie-first** - Support Algérie Télécom, CCP, ENIE, CNAS, etc.

---

## 🏢 Qu'est-ce que IA Factory Teams ?

**IA Factory Teams** est la version collaborative d'IA Factory conçue pour les entreprises algériennes.

### Différences Teams vs Standard

| Fonctionnalité | IA Factory Standard | IA Factory Teams |
|----------------|---------------------|-------------------|
| **Utilisateurs** | 1 compte individuel | Équipe illimitée |
| **Connecteurs** | 3 connecteurs max | Connecteurs illimités |
| **Partage** | Non disponible | Partage chatbots/workflows |
| **SSO** | Non | SAML, OAuth, LDAP |
| **Audit** | Basique | Logs complets + conformité |
| **Support** | Email | Dédié 24/7 + Account Manager |
| **Prix** | 9,900-19,900 DA/mois | À partir de 499,000 DA/an |

**👥 Idéal pour :**
- PME et grandes entreprises algériennes
- Équipes de 5+ personnes
- Départements (Finance, RH, IT, Commercial)
- Projets nécessitant collaboration et gouvernance

---

## 🔌 Connecteurs First-Party

### Qu'est-ce qu'un Connecteur First-Party ?

**First-party** signifie que le connecteur est **développé et maintenu directement par IA Factory**, garantissant :

✅ **Fiabilité maximale** - Testé et optimisé par nos équipes
✅ **Mises à jour automatiques** - Nouvelles fonctionnalités sans intervention
✅ **Support prioritaire** - Assistance directe de nos ingénieurs
✅ **Conformité garantie** - RGPD, Loi 18-07, ISO 27001
✅ **Performance optimale** - Requêtes ultra-rapides via cache intelligent

---

## ⚡ Configuration Rapide

### Étape 1 : Accéder aux Connecteurs

```
Navigation :
Hub IA → ⚙️ Paramètres → 🔌 Connecteurs → ➕ Nouveau Connecteur
```

**Interface principale :**

```
┌─────────────────────────────────────────────────────────────┐
│  🔌 Connecteurs IA Factory Teams                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [🔍 Rechercher un connecteur...]                           │
│                                                             │
│  📊 Catégories :                                            │
│  [Tous] [Bases de données] [Cloud] [Communication]         │
│  [Finance] [RH] [Productivité] [Algérie] [Développement]   │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  💾 Bases de Données                                        │
│                                                             │
│  📘 PostgreSQL                   [✅ Configuré] [⚙️ Gérer]   │
│     3 connexions actives • Dernière sync : Il y a 2 min    │
│                                                             │
│  🟧 MySQL                         [➕ Ajouter]              │
│     Base de données relationnelle populaire                │
│                                                             │
│  🍃 MongoDB                       [➕ Ajouter]              │
│     Base de données NoSQL document-oriented                │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  ☁️ Services Cloud                                          │
│                                                             │
│  📁 Google Drive                 [✅ Configuré] [⚙️ Gérer]   │
│     benali@votreentreprise.dz • 245 fichiers              │
│                                                             │
│  📧 Gmail                         [➕ Ajouter]              │
│     Accès emails et calendrier                             │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  💼 Outils Entreprise                                       │
│                                                             │
│  💬 Slack                        [✅ Configuré] [⚙️ Gérer]   │
│     Workspace : VotreEntreprise • 12 channels              │
│                                                             │
│  📊 Salesforce                    [➕ Ajouter]              │
│     CRM et gestion commerciale                             │
│                                                             │
│  🎫 Jira                          [➕ Ajouter]              │
│     Gestion de projets Agile                               │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  🇩🇿 Services Algériens                                     │
│                                                             │
│  🏦 BaridiMob API                 [➕ Ajouter]              │
│     Paiements CCP, consultations soldes                    │
│                                                             │
│  📱 Mobilis API                   [➕ Ajouter]              │
│     SMS, recharges, consultation consommation              │
│                                                             │
│  💳 SATIM Gateway                 [➕ Ajouter]              │
│     Paiements cartes bancaires algériennes                 │
│                                                             │
│  🏛️ CNAS API                      [➕ Ajouter]              │
│     Consultation dossiers sécurité sociale                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Étape 2 : Créer une Connexion

**Exemple : Connecter PostgreSQL**

```
1. Cliquez sur [➕ Ajouter] à côté de PostgreSQL

┌─────────────────────────────────────────────────────┐
│  🔌 Nouveau Connecteur PostgreSQL                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Nom de la connexion *                             │
│  [Base de Données Production]                      │
│                                                     │
│  Hôte *                                            │
│  [db.votreentreprise.dz]                           │
│                                                     │
│  Port *                                            │
│  [5432]                                            │
│                                                     │
│  Base de données *                                 │
│  [prod_db]                                         │
│                                                     │
│  Utilisateur *                                     │
│  [iafactory_readonly]                              │
│                                                     │
│  Mot de passe *                                    │
│  [••••••••••••••]                                  │
│                                                     │
│  SSL/TLS                                           │
│  [✓] Utiliser connexion sécurisée (recommandé)     │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  🔐 Permissions d'accès                            │
│                                                     │
│  Qui peut utiliser ce connecteur ?                 │
│  ○ Moi uniquement                                  │
│  ● Mon équipe (Département Finance)                │
│  ○ Toute l'organisation                            │
│                                                     │
│  Tables accessibles :                              │
│  [✓] clients                                       │
│  [✓] factures                                      │
│  [✓] produits                                      │
│  [ ] salaires  (Sensible - Désactivé)              │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  [🧪 Tester la Connexion]  [❌ Annuler]  [✅ Créer] │
│                                                     │
└─────────────────────────────────────────────────────┘

2. Remplissez les informations de connexion
3. Cliquez sur [🧪 Tester la Connexion]

┌─────────────────────────────────────────────────────┐
│  ✅ Test de Connexion Réussi                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ⏱️ Latence : 12 ms                                 │
│  📊 Tables détectées : 24                           │
│  📝 Schémas trouvés : public, analytics             │
│  🔐 SSL/TLS : Actif (TLS 1.3)                       │
│                                                     │
│  Aperçu des données :                              │
│  • Table 'clients' : 1,245 lignes                  │
│  • Table 'factures' : 8,932 lignes                 │
│  • Table 'produits' : 156 lignes                   │
│                                                     │
│  ✅ Prêt à utiliser !                               │
│                                                     │
└─────────────────────────────────────────────────────┘

4. Cliquez sur [✅ Créer]

✅ Connecteur PostgreSQL créé avec succès !
Vous pouvez maintenant l'utiliser dans vos chatbots et workflows BMAD.
```

---

### Étape 3 : Utiliser le Connecteur

**Une fois configuré, utilisez-le dans n'importe quel chat :**

```
Vous : @PostgreSQL Combien de factures impayées avons-nous ?

IA : 📊 Analyse des Factures Impayées

[Requête exécutée sur 'Base de Données Production']

SELECT
    COUNT(*) as total,
    SUM(montant) as montant_total
FROM factures
WHERE statut = 'impayé'
AND date_echeance < CURRENT_DATE;

Résultats :
• 47 factures impayées
• Montant total : 2,345,000 DA
• Plus ancienne : 15/11/2024 (62 jours de retard)

📋 Détail par client :
1. Sonatrach : 15 factures (850,000 DA)
2. Cevital : 8 factures (425,000 DA)
3. Condor Electronics : 6 factures (320,000 DA)
...

💡 Suggestion : Lancer relances automatiques via workflow BMAD
```

---

## 🗂️ Connecteurs Disponibles

### 💾 Bases de Données

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **PostgreSQL** | 📘 | Base relationnelle puissante | ERP, Analytics, Production |
| **MySQL** | 🟧 | Base populaire LAMP stack | Sites web, Applications |
| **MongoDB** | 🍃 | Base NoSQL documents | Apps modernes, IoT, Logs |
| **Redis** | 🔴 | Cache in-memory | Sessions, Real-time, Queues |
| **SQLite** | 📱 | Base embarquée | Apps mobiles, Edge devices |
| **Oracle DB** | 🔺 | Base enterprise (legacy) | SAP, Grandes entreprises |
| **SQL Server** | 🟦 | Microsoft SQL Server | Écosystème Microsoft |
| **MariaDB** | 🐬 | Fork MySQL open-source | Alternative MySQL |

---

### ☁️ Stockage Cloud

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **Google Drive** | 📁 | Stockage Google Workspace | Documents, Collaboration |
| **OneDrive** | ☁️ | Stockage Microsoft 365 | Entreprises Microsoft |
| **Dropbox** | 📦 | Stockage cloud simple | Partage fichiers |
| **SharePoint** | 🔷 | Plateforme Microsoft | Intranets, Gestion docs |
| **Box** | 📤 | Stockage enterprise | Conformité, Sécurité |
| **S3 (AWS)** | 🪣 | Object storage AWS | Sauvegardes, CDN |

---

### 💬 Communication

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **Slack** | 💬 | Messagerie d'équipe | Collaboration, Bots |
| **Microsoft Teams** | 👥 | Messagerie Microsoft | Entreprises Microsoft |
| **Gmail** | 📧 | Email Google | Emails, Calendrier |
| **Outlook** | 📮 | Email Microsoft | Entreprises Microsoft |
| **WhatsApp Business** | 📱 | Messagerie clients | Support, Marketing |
| **Telegram** | ✈️ | Messagerie sécurisée | Notifications, Bots |
| **Discord** | 🎮 | Chat communautés | Support, Communities |

---

### 💼 Outils Entreprise

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **Salesforce** | ☁️ | CRM leader mondial | Ventes, Marketing |
| **HubSpot** | 🟠 | CRM marketing | Inbound, Automation |
| **Zoho CRM** | 🔴 | Suite business | PME, All-in-one |
| **SAP** | 🔵 | ERP enterprise | Grandes entreprises |
| **Odoo** | 🟣 | ERP open-source | PME algériennes |
| **Jira** | 🎫 | Gestion projets Agile | Dev, IT, Product |
| **Asana** | 🔺 | Gestion tâches | Marketing, Opérations |
| **Trello** | 📋 | Kanban boards | Projets légers |
| **Monday.com** | 🌈 | Work OS | Tous départements |
| **Notion** | 📝 | Workspace collaboratif | Documentation, Wiki |

---

### 💰 Finance & Comptabilité

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **QuickBooks** | 💚 | Comptabilité PME | Facturation, Compta |
| **Xero** | 🔵 | Comptabilité cloud | PME internationales |
| **Sage** | 🟢 | ERP comptable | Entreprises françaises |
| **WinBooks** | 📊 | Logiciel belge populaire | PME Maghreb/Europe |
| **PC Compta** | 💼 | Logiciel algérien | Conformité DZ |
| **Stripe** | 💳 | Paiements en ligne | E-commerce |
| **PayPal** | 💙 | Paiements internationaux | Marketplace |

---

### 👥 Ressources Humaines

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **BambooHR** | 🎋 | SIRH moderne | PME, Startups |
| **Workday** | 🔵 | SIRH enterprise | Grandes entreprises |
| **ADP** | 🔴 | Paie & RH | Paie complexe |
| **Gusto** | 💚 | Paie PME USA | Startups US |
| **Factorial** | 🟣 | SIRH européen | PME Europe/Maghreb |

---

### 🇩🇿 Services Algériens (Exclusif IA Factory)

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **BaridiMob API** | 🏦 | Algérie Poste CCP | Paiements, Soldes |
| **Mobilis API** | 📱 | Opérateur mobile | SMS, Recharges |
| **Djezzy API** | 🟠 | Opérateur mobile | SMS, Notifications |
| **Ooredoo API** | 🔴 | Opérateur mobile | SMS, Bulk messaging |
| **SATIM Gateway** | 💳 | Paiements CB algériennes | E-commerce DZ |
| **CNAS API** | 🏛️ | Sécurité sociale | Consultation dossiers |
| **CASNOS API** | 💼 | Sécurité sociale indépendants | Non-salariés |
| **ENIE Cadastre** | 🏢 | Registre du commerce | Vérification entreprises |
| **Douanes DZ** | 📦 | Suivi import/export | Logistique |
| **Sonelgaz API** | ⚡ | Électricité & Gaz | Factures, Consommation |

---

### 🛠️ Développement & DevOps

| Connecteur | Logo | Description | Cas d'Usage |
|------------|------|-------------|-------------|
| **GitHub** | 🐙 | Hébergement code | Dev, CI/CD |
| **GitLab** | 🦊 | DevOps platform | Self-hosted, CI/CD |
| **Bitbucket** | 🪣 | Atlassian Git | Équipes Jira |
| **Jenkins** | 👨‍🔧 | CI/CD automation | Legacy pipelines |
| **Docker Hub** | 🐳 | Registry containers | DevOps, Kubernetes |
| **AWS** | 🟧 | Cloud Amazon | Infrastructure cloud |
| **Azure** | 🔵 | Cloud Microsoft | Entreprises Microsoft |
| **Google Cloud** | 🔴 | Cloud Google | ML, Analytics |

---

## 📚 Guide de Configuration par Connecteur

### 📘 PostgreSQL

**Prérequis :**
- PostgreSQL 10+ installé
- Accès réseau (whitelister IPs IA Factory)
- Utilisateur avec permissions lecture

**Configuration :**

```sql
-- 1. Créer utilisateur lecture seule
CREATE USER iafactory_readonly WITH PASSWORD 'mot_de_passe_securise';

-- 2. Accorder permissions sur database
GRANT CONNECT ON DATABASE prod_db TO iafactory_readonly;
GRANT USAGE ON SCHEMA public TO iafactory_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO iafactory_readonly;

-- 3. Permissions futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO iafactory_readonly;

-- 4. Vérifier
\du iafactory_readonly
```

**Whitelist IPs :**

```bash
# /etc/postgresql/14/main/pg_hba.conf
host  prod_db  iafactory_readonly  185.98.138.30/32  scram-sha-256
host  prod_db  iafactory_readonly  185.98.138.31/32  scram-sha-256
host  prod_db  iafactory_readonly  185.98.138.32/32  scram-sha-256
```

**Formulaire IA Factory :**

```
Nom : Base de Données Production
Hôte : db.votreentreprise.dz
Port : 5432
Database : prod_db
User : iafactory_readonly
Password : ••••••••••••••
SSL : ✓ Activé
```

---

### 📁 Google Drive

**Prérequis :**
- Compte Google Workspace (ou Gmail)
- Administrateur pour partage équipe

**Configuration (OAuth 2.0) :**

```
1. Cliquez sur [➕ Ajouter] Google Drive

┌─────────────────────────────────────────────────────┐
│  📁 Connecter Google Drive                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  IA Factory a besoin des permissions suivantes :   │
│                                                     │
│  ✓ Voir fichiers Google Drive                      │
│  ✓ Télécharger fichiers                            │
│  ✓ Rechercher dans Drive                           │
│                                                     │
│  ❌ IA Factory NE POURRA PAS :                      │
│  • Supprimer vos fichiers                          │
│  • Modifier vos fichiers                           │
│  • Partager à votre place                          │
│                                                     │
│  [🔐 Se connecter avec Google]                      │
│                                                     │
└─────────────────────────────────────────────────────┘

2. Cliquez sur [🔐 Se connecter avec Google]
3. Choisissez votre compte Google
4. Autorisez les permissions

┌─────────────────────────────────────────────────────┐
│  ✅ Google Drive Connecté                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📧 Compte : benali@votreentreprise.dz              │
│  📊 Fichiers accessibles : 1,245                    │
│  💾 Espace utilisé : 24 GB / 30 GB                  │
│                                                     │
│  📁 Dossiers partagés :                             │
│  • 💼 Département Finance (156 fichiers)            │
│  • 📊 Rapports Mensuels (89 fichiers)               │
│  • 🏢 Projets Clients (234 fichiers)                │
│                                                     │
│  [✅ Terminer]                                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 💬 Slack

**Prérequis :**
- Workspace Slack
- Administrateur Slack (pour installer app)

**Configuration :**

```
1. Cliquez sur [➕ Ajouter] Slack

2. Autorisez IA Factory dans votre Workspace

┌─────────────────────────────────────────────────────┐
│  💬 Installer IA Factory dans Slack                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Workspace : votreentreprise.slack.com              │
│                                                     │
│  IA Factory demande les permissions suivantes :    │
│                                                     │
│  ✓ Lire messages (channels publics uniquement)     │
│  ✓ Envoyer messages                                │
│  ✓ Lire liste utilisateurs                         │
│  ✓ Uploader fichiers                               │
│                                                     │
│  Channels qui seront accessibles :                 │
│  [✓] #general                                      │
│  [✓] #finance                                      │
│  [✓] #support-client                               │
│  [ ] #rh-confidentiel (privé - non accessible)     │
│                                                     │
│  [✅ Autoriser]  [❌ Annuler]                        │
│                                                     │
└─────────────────────────────────────────────────────┘

3. Configuration terminée !

✅ Slack connecté avec succès
Invitez @IA-Factory-Bot dans vos channels pour commencer à l'utiliser.
```

**Utilisation :**

```
Dans Slack :

@IA-Factory-Bot Résume les discussions de #support-client aujourd'hui

IA Factory Bot :
📊 Résumé #support-client (15/01/2024)

💬 45 messages analysés (8h-18h)

🎫 Tickets mentionnés :
• #2451 - Problème connexion app mobile (Sarah K.)
  → Résolu par Ahmed (10h30)
• #2452 - Facture manquante (Client Sonatrach)
  → En cours - Fatima suit le dossier
• #2453 - Bug affichage dashboard (Client Cevital)
  → Escaladé à équipe dev

😊 Sentiment général : Positif (82%)
⚠️ 3 clients en attente de réponse (>2h)

💡 Suggestion : Répondre en priorité à messages de :
• Mohammed B. (depuis 3h15)
• Karim S. (depuis 2h40)
```

---

### 🏦 BaridiMob API (Algérie Poste)

**Prérequis :**
- Compte CCP Professionnel
- API Key BaridiMob (demande via agence)

**Configuration :**

```
┌─────────────────────────────────────────────────────┐
│  🏦 Connecter BaridiMob API                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Nom de la connexion                               │
│  [Compte CCP Entreprise]                           │
│                                                     │
│  Numéro CCP *                                      │
│  [1234567890123]  (13 chiffres)                    │
│                                                     │
│  Clé RIP *                                         │
│  [00]                                              │
│                                                     │
│  API Key BaridiMob *                               │
│  [bmob_live_xxxxxxxxxxxxxxxxxx]                    │
│                                                     │
│  API Secret *                                      │
│  [••••••••••••••••••••••••••••]                    │
│                                                     │
│  Environnement                                     │
│  ● Production                                      │
│  ○ Sandbox (test)                                  │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  Fonctionnalités activées :                        │
│  [✓] Consultation solde                            │
│  [✓] Historique transactions (30 derniers jours)   │
│  [✓] Paiements sortants                            │
│  [ ] Paiements entrants (webhook)                  │
│                                                     │
│  [🧪 Tester]  [❌ Annuler]  [✅ Connecter]           │
│                                                     │
└─────────────────────────────────────────────────────┘

Résultat du test :
✅ Connexion réussie
💰 Solde actuel : 2,450,000.00 DA
📊 15 transactions trouvées (derniers 30 jours)
```

**Utilisation :**

```
Vous : @BaridiMob Quel est mon solde CCP ?

IA : 💰 Solde CCP Entreprise (au 15/01/2024 10:30)

Compte : 1234567890123 - Clé 00
Solde disponible : 2,450,000.00 DA
Solde réservé : 150,000.00 DA (paiements en attente)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Mouvements récents (5 derniers) :

15/01 09:15  ➕ Virement reçu       +500,000 DA
             De : Sonatrach (Facture #F-2024-0045)

14/01 14:30  ➖ Paiement fournisseur -85,000 DA
             À : Algérie Télécom (Internet Janvier)

14/01 10:00  ➖ Salaires             -950,000 DA
             Virement groupé (8 bénéficiaires)

13/01 16:45  ➕ Virement reçu       +320,000 DA
             De : Cevital (Facture #F-2024-0042)

12/01 11:20  ➖ Charge fiscale      -125,000 DA
             À : CNAS (Cotisations Décembre)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Tendance : -215,000 DA cette semaine
⚠️ Paiements planifiés : 150,000 DA (17/01)

💡 Suggestion : Solde confortable, mais suivre les
   paiements planifiés pour éviter découvert.
```

---

## 🤖 Utilisation avec Chatbots et BMAD

### Dans les Chatbots

**Une fois connectés, tous vos chatbots peuvent interroger vos données :**

```
Exemple : Chatbot Support Client

Client : Je n'ai pas reçu ma facture de décembre

Bot : [Interroge automatiquement PostgreSQL + Gmail]

Bonjour ! 👋

J'ai vérifié votre dossier :

📧 Email : Facture #F-2024-0312 envoyée le 05/12/2024
   À : client@sonatrach.dz
   Statut : ✅ Livré et ouvert le 05/12 à 14:32

💾 Base de données : Facture générée le 03/12/2024
   Montant : 450,000 DA TTC
   Échéance : 03/01/2025

📎 Je vous renvoie la facture par email immédiatement.

Souhaitez-vous également recevoir les prochaines factures
par SMS (nouveau service gratuit) ?
```

---

### Avec BMAD (Deep Agent)

**BMAD peut orchestrer plusieurs connecteurs pour des workflows complexes :**

```
Prompt BMAD :
"Crée un workflow qui, chaque lundi matin :
1. Récupère les nouvelles leads Salesforce
2. Enrichit avec données LinkedIn
3. Vérifie si entreprise existe dans ENIE (Registre Commerce Algérie)
4. Calcule score de qualification
5. Assigne au commercial approprié
6. Envoie résumé par Slack"

BMAD génère automatiquement le workflow avec :
✅ Connecteur Salesforce (leads)
✅ Connecteur LinkedIn (enrichissement)
✅ Connecteur ENIE API (vérification légale DZ)
✅ Logique de scoring (IA)
✅ Connecteur Salesforce (assignment)
✅ Connecteur Slack (notifications)

Déployé et actif en 3 minutes ! 🚀
```

---

## 🗂️ Gestion des Connexions

### Tableau de Bord des Connecteurs

```
Hub IA → ⚙️ Paramètres → 🔌 Connecteurs → 📊 Vue d'ensemble
```

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Mes Connecteurs - Vue d'Ensemble                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📈 Statistiques (30 derniers jours)                        │
│                                                             │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │ 🔌 Actifs   │ 📊 Requêtes │ ⚡ Uptime    │ 💾 Data     │ │
│  │     12      │   24,589    │   99.98%    │   4.2 GB    │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  🔌 Connecteurs Actifs                                      │
│                                                             │
│  📘 PostgreSQL - Base Production                           │
│     🟢 En ligne • 8,234 requêtes ce mois • 12ms latence    │
│     Dernière sync : Il y a 2 minutes                       │
│     [📊 Stats] [⚙️ Configurer] [🗑️ Supprimer]              │
│                                                             │
│  📁 Google Drive - benali@votreentreprise.dz                │
│     🟢 En ligne • 3,421 accès ce mois • 245 fichiers       │
│     Dernière sync : Il y a 5 minutes                       │
│     [📊 Stats] [⚙️ Configurer] [🗑️ Supprimer]              │
│                                                             │
│  💬 Slack - Workspace Entreprise                            │
│     🟢 En ligne • 1,256 messages lus • 12 channels         │
│     Dernière sync : Il y a 1 minute                        │
│     [📊 Stats] [⚙️ Configurer] [🗑️ Supprimer]              │
│                                                             │
│  🏦 BaridiMob - Compte CCP Pro                              │
│     🟢 En ligne • 234 consultations • Solde : 2.4M DA      │
│     Dernière sync : Il y a 30 secondes                     │
│     [📊 Stats] [⚙️ Configurer] [🗑️ Supprimer]              │
│                                                             │
│  🟠 MySQL - Base Clients                                    │
│     🟡 Ralenti • 892 requêtes • 450ms latence (⚠️ élevé)   │
│     Dernière sync : Il y a 15 minutes                      │
│     [📊 Stats] [⚙️ Configurer] [🔧 Diagnostiquer]          │
│                                                             │
│  📊 Salesforce CRM                                          │
│     🔴 Hors ligne • Token expiré                           │
│     Dernière sync : Il y a 2 heures                        │
│     [🔄 Reconnecter] [⚙️ Configurer] [🗑️ Supprimer]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Statistiques Détaillées

**Cliquez sur [📊 Stats] pour voir les détails :**

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Statistiques - PostgreSQL (Base Production)             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📅 Période : 30 derniers jours                             │
│                                                             │
│  📈 Activité                                                │
│                                                             │
│        Requêtes                                             │
│  400 │     ╭─╮                                              │
│  300 │  ╭──╯ ╰─╮    ╭──╮                                    │
│  200 │╭─╯      ╰────╯  ╰──╮                                 │
│  100 │╯                    ╰──────                          │
│      └─────────────────────────────────────                │
│       1/01  7/01  14/01  21/01  28/01                      │
│                                                             │
│  🔝 Requêtes les plus fréquentes (top 5) :                  │
│                                                             │
│  1. SELECT * FROM factures WHERE statut='impayé'           │
│     2,456 fois • Temps moyen : 8ms                         │
│                                                             │
│  2. SELECT * FROM clients WHERE ville='Alger'              │
│     1,892 fois • Temps moyen : 5ms                         │
│                                                             │
│  3. SELECT SUM(montant) FROM commandes WHERE...            │
│     1,234 fois • Temps moyen : 15ms                        │
│                                                             │
│  👥 Utilisateurs actifs :                                   │
│  • Benali Sarah (Finance) : 4,521 requêtes                 │
│  • Ahmed Karim (Commercial) : 2,134 requêtes               │
│  • Fatima Benali (Support) : 1,579 requêtes                │
│                                                             │
│  ⏱️ Performance :                                            │
│  • Latence moyenne : 12ms                                   │
│  • Latence P95 : 45ms                                       │
│  • Latence P99 : 120ms                                      │
│  • Uptime : 99.98%                                          │
│                                                             │
│  💾 Données :                                               │
│  • Tables accessibles : 24                                  │
│  • Lignes totales : ~2.4M                                   │
│  • Taille base : 4.2 GB                                     │
│  • Transfert ce mois : 385 MB                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Révocation d'Accès

**Pour révoquer un connecteur :**

```
1. Cliquez sur [🗑️ Supprimer]

┌─────────────────────────────────────────────────────┐
│  ⚠️ Supprimer le Connecteur ?                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Vous êtes sur le point de supprimer :             │
│  📘 PostgreSQL - Base Production                    │
│                                                     │
│  ⚠️ Conséquences :                                  │
│                                                     │
│  • Les chatbots ne pourront plus interroger        │
│    cette base de données                           │
│                                                     │
│  • Les workflows BMAD utilisant ce connecteur      │
│    cesseront de fonctionner (3 workflows)          │
│                                                     │
│  • L'historique des requêtes sera conservé         │
│    pendant 90 jours (conformité)                   │
│                                                     │
│  • Vous pourrez reconnecter à tout moment          │
│                                                     │
│  ❌ Cette action est réversible                     │
│                                                     │
│  [↩️ Annuler]  [🗑️ Supprimer Définitivement]        │
│                                                     │
└─────────────────────────────────────────────────────┘

2. Confirmez la suppression

✅ Connecteur PostgreSQL supprimé
L'accès a été révoqué côté IA Factory et côté base de données.
```

---

## 🔐 Sécurité et Permissions

### Principes de Sécurité

```
🔒 Sécurité Multi-Couches

┌─────────────────────────────────────────────┐
│  1️⃣ AUTHENTIFICATION                        │
│     • OAuth 2.0 (Google, Slack, etc.)       │
│     • API Keys chiffrées (bases de données) │
│     • Rotation automatique tokens (30j)     │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  2️⃣ AUTORISATION                            │
│     • Permissions granulaires par utilisateur│
│     • RBAC (Role-Based Access Control)      │
│     • Principe du moindre privilège         │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  3️⃣ CHIFFREMENT                             │
│     • En transit : TLS 1.3                  │
│     • Au repos : AES-256-GCM                │
│     • Credentials : HashiCorp Vault         │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  4️⃣ AUDIT                                   │
│     • Logs complets toutes requêtes         │
│     • Traçabilité utilisateur/timestamp     │
│     • Rétention 2 ans (conformité)          │
└─────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────┐
│  5️⃣ SURVEILLANCE                            │
│     • Détection anomalies (IA)              │
│     • Alertes temps réel                    │
│     • SOC 24/7 (Enterprise)                 │
└─────────────────────────────────────────────┘
```

---

### Permissions Granulaires

**Contrôlez précisément qui accède à quoi :**

```
⚙️ Configuration Permissions - PostgreSQL (Base Production)

┌─────────────────────────────────────────────────────────────┐
│  🔐 Gestion des Permissions                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👥 Qui peut utiliser ce connecteur ?                       │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Utilisateur / Équipe          │ Permissions           │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 👤 Benali Sarah (Moi)         │ ✅ Admin (Propriétaire)│ │
│  │ 👥 Équipe Finance (8 membres) │ ✏️ Lecture/Écriture   │ │
│  │ 👥 Équipe Commercial (12)     │ 👁️ Lecture seule      │ │
│  │ 👤 Ahmed Karim (Commercial)   │ 🚫 Accès refusé       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [➕ Ajouter Utilisateur/Équipe]                            │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  📊 Tables et Colonnes Accessibles                          │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Table          │ Finance │ Commercial │ Ahmed K.     │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 👥 clients     │ ✅ Tout  │ 👁️ Lecture  │ 👁️ Lecture   │ │
│  │ 💰 factures    │ ✅ Tout  │ 👁️ Lecture  │ 👁️ Lecture   │ │
│  │ 💳 paiements   │ ✅ Tout  │ 🚫 Aucun    │ 🚫 Aucun     │ │
│  │ 💼 salaires    │ ✅ Tout  │ 🚫 Aucun    │ 🚫 Aucun     │ │
│  │ 📦 produits    │ 👁️ Lecture│ ✅ Tout     │ 👁️ Lecture   │ │
│  │ 📊 commandes   │ ✅ Tout  │ ✅ Tout     │ 👁️ Lecture   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ⚙️ Configuration avancée :                                 │
│                                                             │
│  [ ] Masquer colonnes sensibles (ex: salaires.montant)    │
│  [✓] Limiter à 1000 lignes par requête                    │
│  [✓] Interdire DELETE/UPDATE/DROP                         │
│  [✓] Logger toutes les requêtes (audit)                   │
│  [ ] Nécessiter approbation pour requêtes >10k lignes     │
│                                                             │
│  [💾 Sauvegarder]  [❌ Annuler]                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💼 Cas d'Usage Entreprise

### 1. Support Client Intelligent

**Configuration :**
- PostgreSQL (base clients + tickets)
- Gmail (emails)
- Slack (communication interne)
- Notion (base de connaissances)

**Workflow :**

```
Client envoie email → Gmail connecteur détecte
                   ↓
IA Factory analyse l'email
                   ↓
Recherche client dans PostgreSQL
                   ↓
Cherche solutions dans Notion KB
                   ↓
Génère réponse personnalisée
                   ↓
Envoie par Gmail + notifie équipe sur Slack
```

**Résultats :**
- ⏱️ Temps de réponse : 2 min (vs 2h manuellement)
- 😊 Satisfaction client : +35%
- 💰 Coût support : -60%

---

### 2. Analyse Financière Automatisée

**Configuration :**
- PostgreSQL (comptabilité)
- BaridiMob (CCP)
- QuickBooks (facturation)
- Google Sheets (rapports)

**Prompt :**

```
Vous : Génère le rapport financier mensuel avec :
       - Chiffre d'affaires
       - Dépenses par catégorie
       - Solde CCP
       - Factures impayées
       - Prévisions mois prochain

IA : 📊 Rapport Financier - Janvier 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 CHIFFRE D'AFFAIRES
   Total : 8,450,000 DA
   vs Décembre : +12%
   vs Janvier 2024 : +28%

   Par secteur :
   • B2B : 6,200,000 DA (73%)
   • B2C : 2,250,000 DA (27%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💸 DÉPENSES
   Total : 5,120,000 DA

   Répartition :
   • Salaires : 2,800,000 DA (55%)
   • Loyers : 950,000 DA (19%)
   • Matériel : 620,000 DA (12%)
   • Marketing : 450,000 DA (9%)
   • Divers : 300,000 DA (5%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 TRÉSORERIE
   Solde CCP actuel : 2,450,000 DA
   Encaissements en attente : 1,800,000 DA
   Décaissements planifiés : 950,000 DA

   → Solde prévisionnel fin février : 3,300,000 DA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FACTURES IMPAYÉES
   47 factures • Total : 2,345,000 DA

   Top 5 clients :
   1. Sonatrach : 850,000 DA (15 factures)
   2. Cevital : 425,000 DA (8 factures)
   3. Condor : 320,000 DA (6 factures)
   ...

   ⚠️ Actions urgentes :
   • Relancer 12 factures >45 jours (680k DA)
   • 3 clients en retard récurrent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 PRÉVISIONS FÉVRIER 2025
   CA estimé : 9,200,000 DA (+9% vs janvier)
   Basé sur : 23 devis en cours (6.8M DA)
              Récurrence clients (2.4M DA)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Export disponible : Google Sheets, PDF, Excel
📧 Rapport envoyé à : direction@votreentreprise.dz
```

---

## 🛠️ Dépannage

### ❌ "Connecteur hors ligne"

```
Causes possibles :
1. Token OAuth expiré (Google, Slack, etc.)
2. Credentials changés (base de données)
3. IP bloquée par pare-feu
4. Service distant indisponible

Solutions :
```

```
1. Vérifier statut du service
   Hub IA → 🔌 Connecteurs → [📊 Stats] → Vérifier "Uptime"

2. Reconnecter (OAuth)
   Cliquez sur [🔄 Reconnecter] → Autorisez à nouveau

3. Mettre à jour credentials (DB)
   [⚙️ Configurer] → Modifier mot de passe → [🧪 Tester]

4. Vérifier whitelist IP
   Voir WHITELIST_IP.md pour IPs IA Factory

5. Contacter support si persiste
   support@iafactory.dz
```

---

### ⚠️ "Permissions insuffisantes"

```
Symptôme :
"Erreur : Permission denied for table 'salaires'"

Solutions :
```

```sql
-- PostgreSQL : Vérifier permissions utilisateur
SELECT
    grantee,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'iafactory_readonly';

-- Accorder permissions manquantes
GRANT SELECT ON TABLE salaires TO iafactory_readonly;
```

---

### 🐌 "Requêtes lentes"

```
Symptôme :
Latence >500ms, timeouts fréquents

Solutions :
```

```
1. Vérifier indexes base de données

-- PostgreSQL : Trouver tables sans index
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Créer indexes sur colonnes fréquentes
CREATE INDEX idx_factures_statut ON factures(statut);
CREATE INDEX idx_clients_ville ON clients(ville);

2. Optimiser requêtes dans IA Factory
   Hub IA → 🔌 Connecteurs → [📊 Stats] → "Requêtes lentes"
   → Identifier requêtes problématiques

3. Activer cache (Enterprise)
   [⚙️ Configurer] → Cache → [✓] Activer (TTL: 5 min)
```

---

## 📞 Support

### Besoin d'Aide pour les Connecteurs ?

```
📧 Email : connectors@iafactory.dz
💬 Chat : Hub IA → 💬 Support → "Connecteurs"
📱 WhatsApp Enterprise : +213 560 XX XX XX
📞 Hotline : +213 21 XX XX XX (7j/7, 8h-20h)
```

### Documentation Complémentaire

- 🔐 [Whitelist IP](WHITELIST_IP.md)
- 🔌 [Serveurs MCP Détaillés](CONNECTEURS_IAFACTORY.md)
- 🔒 [Sécurité et Conformité](SECURITE_DONNEES.md)
- 🤖 [Guide BMAD](INDEX_IAFACTORY.md#bmad)

---

**🇩🇿 IA Factory Teams - Connectez Vos Données en 2 Clics**

*Documentation mise à jour : Janvier 2025*
