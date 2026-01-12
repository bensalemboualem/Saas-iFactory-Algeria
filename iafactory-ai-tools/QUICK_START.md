# 🚀 iafactory AI Tools - Quick Start Guide

## Installation en 5 minutes

### Prérequis
- Docker & Docker Compose installés
- Clés API OpenAI (obligatoire)
- Python 3.10+ (pour développement local)

---

## Option 1: Démarrage rapide avec Docker (Recommandé)

### 1. Cloner le projet
```bash
cd /path/to/iafactory
cp -r /path/to/iafactory-ai-tools-integration ./ai-tools
cd ai-tools
```

### 2. Configuration
```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env et ajouter ta clé OpenAI
nano .env
# Ajouter: OPENAI_API_KEY=sk-proj-...
```

### 3. Lancer tous les services
```bash
# Démarrer PostgreSQL, Redis, Backend
docker-compose up -d

# Vérifier que tout fonctionne
docker-compose ps

# Voir les logs
docker-compose logs -f backend
```

### 4. Tester l'API
```bash
# Ouvrir dans le navigateur
http://localhost:8001/api/v1/docs

# Ou tester avec curl
curl http://localhost:8001/api/v1/health
```

### 5. Première traduction
```bash
curl -X POST "http://localhost:8001/api/v1/translator/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjour le monde",
    "source_language": "fr",
    "target_language": "ar",
    "tenant_id": "rag-dz"
  }'
```

**Résultat attendu:**
```json
{
  "success": true,
  "translated_text": "مرحبا بالعالم",
  "source_language": "fr",
  "target_language": "ar",
  "character_count": 15,
  "provider": "openai"
}
```

---

## Option 2: Développement local sans Docker

### 1. Installation
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp ../.env.example .env
# Éditer .env avec tes clés API
```

### 3. Lancer le serveur
```bash
# Depuis backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 4. Accéder à l'API
```
http://localhost:8001/api/v1/docs
```

---

## Endpoints disponibles

### 1. Translation
```bash
POST /api/v1/translator/translate
POST /api/v1/translator/translate/batch
GET  /api/v1/translator/languages
```

### 2. Speech-to-Text (à implémenter)
```bash
POST /api/v1/speech-to-text/transcribe
```

### 3. Text Generation (à implémenter)
```bash
POST /api/v1/text-generator/generate
POST /api/v1/text-generator/improve
```

### 4. Image Generation (à implémenter)
```bash
POST /api/v1/image-generator/generate
POST /api/v1/image-generator/batch
```

### 5. Background Removal (à implémenter)
```bash
POST /api/v1/background-remover/remove
```

### 6. Image Upscaling (à implémenter)
```bash
POST /api/v1/image-upscaler/upscale
```

### 7. Image Transformation (à implémenter)
```bash
POST /api/v1/image-transformer/transform
```

---

## Architecture des fichiers

```
iafactory-ai-tools-integration/
├── README.md                     # Documentation principale
├── QUICK_START.md               # Ce fichier
├── .env.example                 # Template configuration
├── docker-compose.yml           # Orchestration Docker
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # Application FastAPI
│       ├── core/
│       │   └── config.py       # Configuration
│       ├── api/
│       │   └── v1/
│       │       ├── router.py   # Router principal
│       │       └── endpoints/
│       │           └── translator.py  # Endpoint traduction
│       ├── services/
│       │   └── ai_providers/
│       │       ├── openai_service.py
│       │       └── background_removal_service.py
│       └── models/
│           ├── requests.py     # Modèles de requêtes
│           └── responses.py    # Modèles de réponses
│
└── frontend/                    # À implémenter
    └── components/
```

---

## Intégration dans iafactory

### Pour rag-dz (Marché algérien)
```python
# Exemple d'utilisation dans ton app
import requests

response = requests.post(
    "http://localhost:8001/api/v1/translator/translate",
    json={
        "text": "Texte à traduire",
        "source_language": "fr",
        "target_language": "ar",
        "tenant_id": "rag-dz"
    }
)
```

### Pour Helvetia (Marché suisse)
```python
response = requests.post(
    "http://localhost:8001/api/v1/translator/translate",
    json={
        "text": "Text to translate",
        "source_language": "en",
        "target_language": "fr",
        "tenant_id": "helvetia"
    }
)
```

---

## Prochaines étapes

1. ✅ **Translation** - Fonctionnel
2. ⏳ **Implémenter les autres endpoints** (copier le pattern de translator.py)
3. ⏳ **Ajouter authentification JWT**
4. ⏳ **Créer le frontend React**
5. ⏳ **Ajouter rate limiting**
6. ⏳ **Monitoring et logging avancé**
7. ⏳ **Tests unitaires et intégration**
8. ⏳ **Déployer sur VPS (Algérie + Suisse)**

---

## Support

Pour les questions ou problèmes:
1. Vérifier les logs: `docker-compose logs -f backend`
2. Tester la santé de l'API: `http://localhost:8001/api/v1/health`
3. Vérifier la documentation: `http://localhost:8001/api/v1/docs`

---

## Coûts estimés (avec OpenAI)

- **Traduction** (GPT-4o-mini): ~$0.15 / 1M caractères
- **Génération de texte**: ~$0.15 / 1M tokens
- **Speech-to-Text** (Whisper): $0.006 / minute
- **Image generation** (DALL-E 3): $0.04 / image standard

**Total estimé pour 1000 requêtes mixtes: ~$5-10/mois**

---

Bon développement ! 🚀
