# IA Factory - Complete Content Automation Platform

Une plateforme d'automatisation de contenu propulsée par l'IA pour créer, éditer et distribuer des vidéos sur plusieurs plateformes.

## 🚀 Fonctionnalités

### Phase 1: Configuration de Marque
- Configuration de la voix et du ton de marque
- Définition des piliers de contenu
- Gestion d'équipe avec invitations

### Phase 2: Génération de Contenu
- Génération de scripts avec Claude AI
- Création de vidéos avec VEO 3 (Replicate)
- Édition automatique avec FFmpeg
- Calendrier de contenu intelligent

### Phase 3: Distribution Multi-Plateformes
- Publication sur Instagram, TikTok, YouTube, LinkedIn
- Conversion automatique des formats vidéo
- Adaptation des captions et hashtags
- Planification des publications

### Phase 4: Analytics & Optimisation
- Tableau de bord unifié
- Recommandations AI pour améliorer la performance
- Rapports automatisés
- Détection des tendances

## 📋 Prérequis

- Python 3.11+
- MongoDB 7.0+
- Redis 7+
- FFmpeg
- Docker & Docker Compose (recommandé)

## 🛠 Installation

### Option 1: Docker Compose (Recommandé)

```bash
# Cloner le repository
cd ia-factory

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos clés API
nano .env

# Lancer les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f
```

### Option 2: Installation Locale

```bash
# Créer un environnement virtuel
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp ../.env.example .env

# Lancer MongoDB et Redis (ou utiliser des services cloud)
# ...

# Lancer l'application
uvicorn app.main:app --reload --port 8000
```

## 🔑 Configuration

### Variables d'Environnement Requises

```env
# AI Services
ANTHROPIC_API_KEY=sk-ant-...      # Requis pour génération de scripts
REPLICATE_API_TOKEN=r8_...         # Requis pour génération vidéo

# Base de données
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0

# Plateformes sociales (optionnel)
INSTAGRAM_ACCESS_TOKEN=...
TIKTOK_ACCESS_TOKEN=...
YOUTUBE_CLIENT_ID=...
LINKEDIN_ACCESS_TOKEN=...
```

## 📚 API Documentation

Une fois l'application lancée, accédez à:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints Principaux

| Endpoint | Description |
|----------|-------------|
| `POST /api/brand/setup` | Configurer une nouvelle marque |
| `POST /api/content/generate-scripts` | Générer des scripts |
| `POST /api/content/generate-videos` | Créer des vidéos |
| `POST /api/content/auto-edit` | Éditer automatiquement |
| `POST /api/distribution/publish` | Publier du contenu |
| `GET /api/analytics/dashboard` | Tableau de bord analytics |

## 🏗 Architecture

```
ia-factory/
├── backend/
│   ├── app/
│   │   ├── api/           # Routes FastAPI
│   │   ├── models/        # Modèles Pydantic
│   │   ├── services/      # Logique métier
│   │   ├── tasks/         # Tâches Celery
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Connexion MongoDB
│   │   └── main.py        # Point d'entrée
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # (À venir)
├── docker-compose.yml
└── .env.example
```

## 🔄 Workflow Typique

1. **Configuration Initiale**
   ```
   POST /api/brand/setup
   {
     "name": "Ma Marque",
     "industry": "tech",
     "tone": "professional",
     "content_pillars": ["innovation", "tutoriels"]
   }
   ```

2. **Génération de Script**
   ```
   POST /api/content/generate-scripts
   {
     "brand_id": "...",
     "topic": "Introduction à l'IA",
     "content_type": "short_video"
   }
   ```

3. **Création de Vidéo**
   ```
   POST /api/content/generate-videos
   {
     "script_id": "...",
     "brand_id": "...",
     "style": "modern"
   }
   ```

4. **Publication**
   ```
   POST /api/distribution/publish
   {
     "content_id": "...",
     "platforms": ["instagram", "tiktok"]
   }
   ```

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app
```

## 📈 Monitoring

- Health Check: `GET /health`
- Status API: `GET /api/status`

## 🔒 Sécurité

- Toutes les clés API doivent être stockées dans des variables d'environnement
- Les credentials des plateformes sont chiffrés en base de données
- CORS configuré pour la production

## 📝 License

MIT License

## 🤝 Support

Pour toute question ou support, contactez l'équipe IA Factory.
