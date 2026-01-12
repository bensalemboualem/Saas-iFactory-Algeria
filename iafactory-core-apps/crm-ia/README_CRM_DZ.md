# 📋 Module 11 : CRM IA — Gestion de Dossiers & Clients

## 🎯 Vue d'ensemble

Le **CRM IA** est un système de gestion de la relation client intelligent conçu pour iaFactory Algeria. Il permet de gérer les clients, les dossiers (juridiques, fiscaux, administratifs, business) avec une automatisation IA intégrée.

## 🚀 Fonctionnalités

### 👥 Gestion des Clients
- Création et suivi des clients
- Informations de contact complètes
- Historique des dossiers par client

### 📁 Gestion des Dossiers
- Types de dossiers : Juridique, Fiscal, Administratif, Business, Autre
- Statuts : Nouveau, En cours, Attente client, Résolu, Fermé
- Priorités : Basse, Normale, Haute, Urgente

### 📝 Notes et Documents
- Ajout de notes par dossier (Général, Appel, Réunion, Email, Tâche)
- Upload et téléchargement de fichiers
- Historique complet des interactions

### 🤖 Analyse IA
- Résumé automatique du dossier
- Évaluation des risques
- Recommandations intelligentes
- Prochaines étapes suggérées
- Références légales pertinentes

## 🔗 Accès

| Service | URL | Description |
|---------|-----|-------------|
| CRM UI | https://www.iafactoryalgeria.com/crm/ | Interface utilisateur |
| CRM API | https://www.iafactoryalgeria.com/api/crm/ | API REST |

## 📡 Endpoints API

### Clients
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/crm/client` | Créer un client |
| GET | `/api/crm/client` | Lister les clients |
| GET | `/api/crm/client/{id}` | Obtenir un client |

### Dossiers
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/crm/case` | Créer un dossier |
| GET | `/api/crm/case` | Lister les dossiers |
| GET | `/api/crm/case/{id}` | Obtenir un dossier |
| PATCH | `/api/crm/case/{id}` | Mettre à jour un dossier |
| DELETE | `/api/crm/case/{id}` | Supprimer un dossier |

### Notes
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/crm/case/{id}/note` | Ajouter une note |
| GET | `/api/crm/case/{id}/note` | Lister les notes |

### Fichiers
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/crm/case/{id}/file` | Uploader un fichier |
| GET | `/api/crm/case/{id}/file` | Lister les fichiers |
| GET | `/api/crm/case/{id}/file/{file_id}` | Télécharger un fichier |

### Analyse IA
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/crm/case/{id}/ai-analyze` | Lancer l'analyse IA |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CRM IA Interface                         │
│                  (Port 8213 - Nginx)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Clients   │    │   Dossiers  │    │  Analyse IA │    │
│  │   CRUD      │    │   CRUD      │    │  Intégrée   │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                   CRM API Backend                           │
│                (Port 8212 - FastAPI)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Legal     │    │   Fiscal    │    │     RAG     │    │
│  │   Module    │    │   Module    │    │   Module    │    │
│  │  (8181)     │    │  (8183)     │    │  (8185)     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🐳 Conteneurs Docker

| Conteneur | Port | Image | Status |
|-----------|------|-------|--------|
| iaf-crm-ia-prod | 8212 | iaf-crm-ia:latest | ✅ Running |
| iaf-crm-ia-ui-prod | 8213 | iaf-crm-ia-ui:latest | ✅ Running |

## 📦 Exemple d'utilisation API

### Créer un client
```bash
curl -X POST https://www.iafactoryalgeria.com/api/crm/client \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SARL Algérie Tech",
    "email": "contact@algerietech.dz",
    "phone": "+213 555 123 456",
    "company": "Algérie Tech SARL",
    "address": "123 Rue Didouche Mourad, Alger"
  }'
```

### Créer un dossier
```bash
curl -X POST https://www.iafactoryalgeria.com/api/crm/case \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Constitution SARL",
    "client_id": "CLIENT_ID",
    "case_type": "legal",
    "priority": "high",
    "description": "Création d'une SARL dans le secteur technologique"
  }'
```

### Lancer analyse IA
```bash
curl -X POST https://www.iafactoryalgeria.com/api/crm/case/{case_id}/ai-analyze
```

## 🔧 Configuration Nginx

Les routes sont configurées dans `/etc/nginx/sites-enabled/iafactoryalgeria.com` :

```nginx
# CRM IA API
location /api/crm/ {
    proxy_pass http://127.0.0.1:8212/api/crm/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# CRM IA UI
location /crm/ {
    proxy_pass http://127.0.0.1:8213/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 📊 Intégration avec autres modules

Le CRM IA s'intègre avec les modules existants :

- **Module Juridique** (8181) : Consultation légale pour dossiers juridiques
- **Module Fiscal** (8183) : Consultation fiscale pour dossiers fiscaux  
- **Module RAG** (8185) : Recherche documentaire intelligente
- **Module Billing** (8207) : Suivi de facturation par client/dossier

## 🛡️ Sécurité

- Validation des entrées avec Pydantic
- Limitation de taille des fichiers uploadés
- Stockage sécurisé des documents
- HTTPS obligatoire via Let's Encrypt

## 📈 Évolutions futures

1. **Persistance PostgreSQL** : Migration vers base de données permanente
2. **Authentification** : Intégration avec système d'auth centralisé
3. **Notifications** : Alertes automatiques par email/SMS
4. **Reporting** : Tableaux de bord et rapports automatisés
5. **Multi-utilisateurs** : Gestion des permissions par rôle

---

**iaFactory Algeria** - Module CRM IA v1.0  
*Gestion intelligente de la relation client* 🇩🇿
