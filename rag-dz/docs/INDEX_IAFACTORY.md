# 🇩🇿 Bienvenue sur IA Factory Algeria

> **Plateforme d'Intelligence Artificielle Souveraine pour l'Algérie**

Votre ressource complète pour tout ce qui concerne IA Factory - de la création de contenu multimédia à l'automatisation d'entreprise.

---

## 🌟 Explorez Notre Documentation

### 🎨 Studio Créatif & Deep Agent
**Accédez aux guides pour notre plateforme tout-en-un de création IA**

Création multimédia avec accès aux meilleurs modèles open-source et propriétaires (Sora 2, FLUX Pro, ElevenLabs...)

**Liens Rapides**
- → [Introduction au Studio](./STUDIO_CREATIF_GUIDE.md)
- → [Deep Agent Workflow](./WORKFLOW_BMAD_ARCHON.md)
- → [Création d'Applications](./GUIDE_STUDIO_VIDEO.md)
- → [Astuces de Prompting](./GUIDE_UTILISATION_BMAD.md)

**URL**: `http://localhost:8184/studio`

---

### 💻 IA Factory Desktop
**Découvrez notre assistant de bureau alimenté par IA**

CLI de codage, éditeur intelligent et capacités d'écoute en temps réel

**Liens Rapides**
- → [Introduction Desktop](../README.md)
- → [Intégration MCP](./ETAT_ACTUEL_BMAD_WORKFLOW.md)
- → [Règles IA Factory](../.claude/project-rules.md)
- → [AbacusAI Listener](./ARCHITECTURE_INTEGREE.md)

**URL**: `http://localhost:8182` (Archon Hub)

---

### 🏢 Plateforme Entreprise
**Apprenez à utiliser notre plateforme IA complète**

Chatbots et workflows IA à l'échelle de l'entreprise avec guides end-to-end

**Liens Rapides**
- → [Introduction Enterprise](./ARCHITECTURE.md)
- → [Workflows IA & Framework Agentique](./ORCHESTRATION_COMPLETE.md)
- → [Chatbots Personnalisés](./NOUVEAU_WORKFLOW_SIMPLE.md)
- → [Choisir le Type de Projet](./PHASE_1_COMPLETED.md)

**URLs**:
- Backend API: `http://localhost:8180`
- Docs UI: `http://localhost:8183`
- n8n: `http://localhost:8185`

---

### 🔌 Connecteurs
**Tutoriels d'intégration avec vos sources de données existantes**

**Liens Rapides**
- → [Vue d'ensemble Connecteurs](./DEPLOIEMENT_HETZNER.md)
- → [Connecteurs Utilisateur](./CONFIGURATION_GROQ_IMMEDIAT.md)
- → [Connecteurs Base de Données](./AUDIT_FINAL_GLOBAL.md)
- → [Authentification](./GUIDE_INSTALLATION_VPS.md)

**Services Supportés**:
- PostgreSQL (PGVector)
- Redis Cache
- Qdrant Vector DB
- Twilio (SMS/WhatsApp)
- Google Calendar/Tasks
- Slack, Notion, GitHub

---

### 🐍 Python SDK
**Accès programmatique aux fonctionnalités IA Factory**

**Liens Rapides**
- → [Démarrage Rapide](./QUICK_START.md)
- → [Workflows IA](./WORKFLOW_BOLT_BMAD_ARCHON.md)
- → [Invocation LLMs](./SOLUTIONS_ECONOMIQUES_AI.md)
- → [GitHub CI/CD](./DEPLOIEMENT_AUTOMATIQUE.md)

**Installation**:
```bash
pip install -r backend/rag-compat/requirements.txt
```

---

### 📚 Référence API
**Documentation complète de l'API REST**

**Liens Rapides**
- → [Référence API](http://localhost:8180/docs)
- → [Classes API](http://localhost:8180/redoc)
- → [Inputs API](./RESUME_FINAL_WORKFLOW.md)

**Base URL**: `http://localhost:8180/api/v1`

---

## 🎯 La Plateforme IA Factory

La Plateforme Développeur IA Factory s'intègre parfaitement avec **Studio Créatif & Archon Hub**, permettant à tout chatbot ou agent personnalisé d'être déployé directement aux utilisateurs.

**Et le meilleur?** Studio Créatif & Archon Hub viennent chargés de fonctionnalités extensives prêtes à l'emploi que vous pouvez utiliser dès le premier jour.

### 🏗️ Architecture Complète

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Studio Créatif<br/>:8184] --> |MCP| B[Archon Hub<br/>:8182]
        B --> C[Docs UI<br/>:8183]
    end

    subgraph "Backend Services"
        D[Backend API<br/>:8180] --> E[(PostgreSQL<br/>PGVector)]
        D --> F[(Redis Cache)]
        D --> G[(Qdrant VectorDB)]
    end

    subgraph "Automation & AI"
        H[n8n Workflows<br/>:8185]
        I[BMAD Agents]
        J[Ollama Local<br/>:8186]
    end

    subgraph "MCP Servers"
        K[GitHub]
        L[Playwright]
        M[PostgreSQL]
        N[Google Tasks]
    end

    A --> D
    B --> D
    C --> D
    D --> H
    D --> I
    I --> J

    A -.MCP.-> K
    A -.MCP.-> L
    A -.MCP.-> M
    A -.MCP.-> N
```

---

## 🚀 Démarrage Rapide

### 1️⃣ Installation Complète

```bash
# Cloner le projet
cd rag-dz

# Configuration
cp .env.example .env.local
# Éditer .env.local avec vos API keys

# Démarrer tous les services
docker-compose up -d

# Avec monitoring (optionnel)
docker-compose --profile monitoring up -d

# Avec Ollama local (optionnel)
docker-compose --profile ollama up -d
```

### 2️⃣ Accès aux Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| **Studio Créatif** | http://localhost:8184/studio | Création multimédia IA |
| **Archon Hub** | http://localhost:8182 | Dashboard principal |
| **Docs UI** | http://localhost:8183 | Gestion documentaire |
| **Backend API** | http://localhost:8180 | API REST |
| **n8n** | http://localhost:8185 | Automatisation workflows |
| **Ollama** | http://localhost:8186 | Modèles IA locaux |
| **Prometheus** | http://localhost:8187 | Métriques |
| **Grafana** | http://localhost:8188 | Monitoring |

### 3️⃣ Configuration API Keys

Éditez `.env.local`:

```bash
# ══════════════════════════════════════════════════════════════
# IA FACTORY - CONFIGURATION COMPLÈTE
# ══════════════════════════════════════════════════════════════

# LLM Providers
GROQ_API_KEY=gsk_xxxxxxxxxxxxx              # Gratuit, rapide
OPENAI_API_KEY=sk-xxxxxxxxxxxxx             # GPT-4, Sora 2
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx      # Claude
GOOGLE_GENERATIVE_AI_API_KEY=xxxxxxxxxxxxx  # Gemini, Veo 3
DEEPSEEK_API_KEY=xxxxxxxxxxxxx              # DeepSeek

# MCP Servers
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
BRAVE_API_KEY=BSA_xxxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
NOTION_API_KEY=secret_xxxxxxxxxxxxx

# Twilio (SMS/WhatsApp)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+213xxxxxxxxx

# Google Services
GOOGLE_CALENDAR_CREDS='{"type":"service_account",...}'
GOOGLE_DRIVE_CREDS='{"type":"service_account",...}'

# Base de données
POSTGRES_PASSWORD=votre-mot-de-passe-securise

# n8n
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
```

### 4️⃣ Test du Système

```bash
# Vérifier tous les services
docker-compose ps

# Logs en temps réel
docker logs iaf-dz-studio --follow
docker logs iaf-dz-backend --follow

# Health check
curl http://localhost:8180/health

# Test Studio
open http://localhost:8184/studio
```

---

## 📊 Cas d'Usage

### 🎬 Création de Contenu Vidéo

```bash
# Studio Créatif
1. Accéder à http://localhost:8184/studio
2. Taper: "Vidéo promotionnelle startup tech algérienne"
3. Sélection auto: Video-Gen (Sora 2)
4. Génération 30s en HD
5. Publication: YouTube + TikTok + Instagram via n8n
```

### 📄 Génération de Documents

```bash
# Archon Hub
1. Accéder à http://localhost:8182
2. Aller dans "Documents"
3. Uploader PDF/Word/Excel
4. Agent BMAD analyse et extrait
5. Export dans tous formats
```

### 💻 Développement Assisté

```bash
# MCP GitHub Integration
1. Activer GitHub MCP dans Studio
2. Taper: "Créer API REST Python FastAPI"
3. Code généré avec bonnes pratiques
4. Push automatique vers repo GitHub
5. CI/CD déclenché
```

### 🤖 Automatisation WhatsApp

```bash
# Backend + Twilio
1. Configurer Twilio credentials
2. Créer workflow n8n
3. Recevoir message WhatsApp
4. Agent BMAD répond intelligemment
5. Log dans PostgreSQL
```

---

## 🎓 Formations & Ressources

### Vidéos Tutoriels
- [Installation Complète](./GUIDE_INSTALLATION_VPS.md)
- [Studio Créatif Workflow](./GUIDE_STUDIO_VIDEO.md)
- [BMAD Agents](./GUIDE_UTILISATION_BMAD.md)
- [Déploiement VPS](./DEPLOIEMENT_HETZNER.md)

### Documentation Technique
- [Architecture Complète](./ARCHITECTURE.md)
- [Audit & Roadmap](./AUDIT_FINAL_GLOBAL.md)
- [Tests Validés](./TESTS_VALIDES.md)
- [Dette Technique](./TECHNICAL_DEBT.md)

### Guides de Déploiement
- [Hetzner Cloud](./DEPLOIEMENT_HETZNER.md)
- [Manuel Simple](./DEPLOIEMENT_MANUEL_SIMPLE.md)
- [Automatique](./DEPLOIEMENT_AUTOMATIQUE.md)
- [Recovery Plan](./RECOVERY_PLAN.md)

---

## 🆘 Support & Communauté

### 📧 Contact
- Email: support@iafactory.dz
- WhatsApp: +213 xxx xxx xxx
- Slack: [IA Factory Community](http://localhost:8185/slack)

### 🐛 Bugs & Issues
- GitHub Issues: [github.com/iafactory/rag-dz](https://github.com)
- Diagnostic: [DIAGNOSTIC_COMPLET.md](./DIAGNOSTIC_COMPLET.md)

### 📚 Ressources Additionnelles
- [FAQ](./FAQS.md) (TODO)
- [Blog](https://iafactory.dz/blog) (TODO)
- [Changelog](./STATUS_DASHBOARD.md)

---

## 🔒 Sécurité

- ✅ **Souveraineté**: Toutes les données restent en Algérie
- ✅ **Encryption**: SSL/TLS sur toutes les communications
- ✅ **Auth**: JWT + API Keys + OAuth
- ✅ **RGPD**: Conforme RGPD/LGPD
- ✅ **Audit**: Logs complets dans PostgreSQL

---

## 📈 Roadmap 2025

### Q1 2025 ✅
- [x] Studio Créatif avec 17 outils
- [x] MCP Integration (12 serveurs)
- [x] Backend BMAD complet
- [x] n8n Workflows
- [x] Documentation complète

### Q2 2025 🚧
- [ ] Application mobile (React Native)
- [ ] Modèles IA locaux algériens
- [ ] Intégration Algérie Poste
- [ ] Support Tamazight (ⵜⴰⵎⴰⵣⵉⵖⵜ)

### Q3-Q4 2025 📋
- [ ] Marketplace d'agents
- [ ] Formation certifiante
- [ ] API publique v2
- [ ] Support multilingue complet (AR/FR/EN/Tamazight)

---

## 🏆 Pourquoi IA Factory?

| Critère | IA Factory 🇩🇿 | Autres Plateformes |
|---------|----------------|---------------------|
| **Souveraineté** | ✅ Données en Algérie | ❌ Cloud US/EU |
| **Prix** | ✅ 70% moins cher | ⚠️ Cher |
| **Multilingue** | ✅ AR/FR/EN/Tamazight | ⚠️ EN only |
| **Support Local** | ✅ 24/7 DZ | ❌ Fuseau horaire US |
| **Personnalisation** | ✅ Complète | ⚠️ Limitée |
| **Open Source** | ✅ Oui | ❌ Propriétaire |

---

## 🎉 Commencez Maintenant!

```bash
# 1. Cloner
git clone https://github.com/iafactory/rag-dz
cd rag-dz

# 2. Configurer
cp .env.example .env.local
nano .env.local

# 3. Démarrer
docker-compose up -d

# 4. Tester
open http://localhost:8184/studio
```

---

**Version**: 1.0.0 | **Dernière mise à jour**: 2025-01-18

**IA Factory Algeria** 🇩🇿 - *L'Intelligence Artificielle Souveraine*

---

Copyright © 2025 IA Factory Algeria. Tous droits réservés.
