# DZ-LegalAssistant 🇩🇿⚖️

**Module 3 de IAFactory Algeria - Assistant Juridique & Administratif spécialisé Algérie**

## 📋 Description

DZ-LegalAssistant est un assistant conversationnel spécialisé dans les procédures administratives et aspects juridiques de base en Algérie. Il utilise :

- **RAG DZ** : Base de connaissances alimentée par les sources officielles algériennes
- **LLM (GROQ)** : Génération de réponses structurées
- **Prompts spécialisés** : Contexte juridique et administratif algérien

## 🚀 Fonctionnalités

### Catégories supportées

| Catégorie | Description | Exemples |
|-----------|-------------|----------|
| `procédure_administrative` | Démarches administratives | Registre de commerce, Carte d'artisan |
| `droit_des_affaires` | Création et gestion d'entreprise | EURL, SARL, SPA, Dissolution |
| `social_cnas_casnos` | Sécurité sociale | Affiliation, Cotisations, Déclarations |
| `impôts_dgi` | Fiscalité | IRG, IBS, TVA, TAP, G50 |
| `douane_import_export` | Commerce international | Import, Export, Dédouanement |
| `autre` | Questions diverses | - |

### Réponse structurée

Chaque réponse inclut :
- **Summary** : Résumé en 3-8 phrases
- **Steps** : Étapes détaillées avec checklists
- **Important Notes** : Points critiques (délais, documents, frais)
- **Risks & Limits** : Incertitudes et limites de la réponse
- **References** : Sources documentaires (JORADP, DGI, CNRC, etc.)
- **Disclaimer** : Avertissement légal
- **Followup Questions** : Questions de suivi suggérées

## 🔧 API Endpoints

### POST `/api/dz-legal/answer`

Répondre à une question juridique/administrative.

**Request:**
```json
{
  "question": "Quelles sont les étapes pour créer une EURL en Algérie ?",
  "category": "droit_des_affaires",
  "user_context": "Je suis développeur freelance à Alger"
}
```

**Response:**
```json
{
  "summary": "Pour créer une EURL en Algérie...",
  "category": "droit_des_affaires",
  "steps": [
    {
      "title": "1. Rédaction des statuts",
      "description": "Préparer les statuts avec un notaire",
      "checklist": ["Objet social", "Capital", "Gérant", "Siège"]
    }
  ],
  "important_notes": ["Capital minimum: 100 000 DA"],
  "risks_and_limits": ["Délais variables selon wilaya"],
  "references": [
    {
      "label": "Code de commerce",
      "source_name": "JORADP",
      "source_url": null,
      "date": null
    }
  ],
  "disclaimer": "Cette réponse est fournie à titre informatif...",
  "followup_questions": ["Quel est le capital minimum ?"]
}
```

### GET `/api/dz-legal/categories`

Liste des catégories disponibles.

### GET `/api/dz-legal/examples`

Exemples de questions fréquentes.

### GET `/health`

Vérification de santé de l'API.

## 🐳 Déploiement Docker

### Build
```bash
docker build -t iaf-legal-assistant .
```

### Run
```bash
docker run -d \
  --name iaf-legal-assistant-prod \
  --network iaf-prod-network \
  -p 8197:8197 \
  -e GROQ_API_KEY=your_key \
  -e RAG_API_URL=http://iaf-dz-connectors-prod:8195 \
  iaf-legal-assistant
```

## 🌐 Frontend

Le frontend est une application HTML/Tailwind statique accessible sur le port 8198.

**Fonctionnalités UI :**
- Sélection de catégorie intuitive
- Zone de question avec validation
- Contexte optionnel
- Affichage structuré des réponses
- Questions de suivi cliquables
- Exemples de questions

## 📦 Structure

```
dz-legal-assistant/
├── Dockerfile
├── README.md
└── backend/
    └── main.py          # API FastAPI

apps/legal-assistant/
└── index.html           # Frontend
```

## ⚠️ Avertissement

**DZ-LegalAssistant n'est PAS un avocat.**

Cet outil fournit des informations générales à titre indicatif. Pour toute démarche officielle ou question juridique complexe, veuillez consulter :
- Un avocat inscrit au barreau
- Un notaire agréé
- Les autorités compétentes (CNRC, DGI, CNAS, CASNOS, etc.)

## 🔗 Intégration IAFactory

| Service | Port | Route |
|---------|------|-------|
| Backend API | 8197 | `/api/dz-legal/` |
| Frontend | 8198 | `/legal/` |
| RAG DZ | 8195 | `/api/dz/` |
| Data DZ | 8196 | `/data-dz/` |

## 📝 Licence

Module de IAFactory Algeria - Usage interne
