# IA Factory - Contexte pour Claude Code

## 🎯 RÉSUMÉ DU PROJET

**IA Factory** est une plateforme complète d'automatisation de contenu déployée sur le VPS `iafactorysuisse` (46.224.3.125).

**Date de création** : 6 décembre 2025
**Status** : ✅ DÉPLOYÉ ET FONCTIONNEL

---

## 📁 STRUCTURE DES DOSSIERS

```
d:\IAFactory\rag-dz\ia-factory\
├── backend/
│   ├── app/
│   │   ├── api/                    # Routes FastAPI
│   │   │   ├── __init__.py
│   │   │   ├── brand.py            # /api/brand/* endpoints
│   │   │   ├── content.py          # /api/content/* endpoints
│   │   │   ├── distribution.py     # /api/distribution/* endpoints
│   │   │   └── analytics.py        # /api/analytics/* endpoints
│   │   │
│   │   ├── models/                 # Modèles Pydantic
│   │   │   ├── __init__.py
│   │   │   ├── brand.py            # BrandVoice, ContentPillar, UserProfile
│   │   │   ├── content.py          # Script, VideoJob, ContentItem
│   │   │   ├── distribution.py     # Platform, PlatformCredentials, ScheduledPost
│   │   │   └── analytics.py        # ContentMetrics, AnalyticsSummary
│   │   │
│   │   ├── services/               # Logique métier
│   │   │   ├── __init__.py
│   │   │   ├── script_generation.py    # Claude AI pour scripts
│   │   │   ├── video_generation.py     # VEO 3 / Replicate
│   │   │   ├── video_operator.py       # FFmpeg auto-editing
│   │   │   ├── content_calendar.py     # Planification mensuelle
│   │   │   ├── platform_converter.py   # Conversion formats vidéo
│   │   │   ├── content_adapter.py      # Adaptation captions/hashtags
│   │   │   ├── platform_publishers.py  # Publication multi-plateformes
│   │   │   └── analytics_engine.py     # Métriques et recommandations AI
│   │   │
│   │   ├── tasks/                  # Tâches Celery (background)
│   │   │   ├── __init__.py         # Configuration Celery
│   │   │   ├── video_tasks.py      # Tâches génération vidéo
│   │   │   ├── publishing_tasks.py # Tâches publication
│   │   │   └── analytics_tasks.py  # Tâches analytics
│   │   │
│   │   ├── config.py               # Settings Pydantic
│   │   ├── database.py             # MongoDB Motor async
│   │   └── main.py                 # FastAPI entry point
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml              # API + MongoDB + Redis
├── .env.example                    # Template variables d'environnement
├── nginx-snippet.conf              # Config nginx pour reverse proxy
├── deploy.sh                       # Script déploiement VPS
└── README.md                       # Documentation
```

---

## 🔧 CONFIGURATION VPS

### Emplacement sur le serveur
```
/opt/ia-factory/
```

### Containers Docker actifs
| Container | Port Interne | Port Externe | Status |
|-----------|--------------|--------------|--------|
| ia-factory-api | 8000 | 8087 | ✅ Healthy |
| ia-factory-mongodb | 27017 | 27018 | ✅ Healthy |
| ia-factory-redis | 6379 | 6380 | ✅ Healthy |

### URLs Publiques
- **API**: `https://www.iafactoryalgeria.com/ia-factory/`
- **Swagger Docs**: `https://www.iafactoryalgeria.com/ia-factory/docs`
- **Health Check**: `https://www.iafactoryalgeria.com/ia-factory/health`

### Nginx Config
Ajouté dans `/etc/nginx/sites-available/iafactoryalgeria.com` :
```nginx
location /ia-factory/ {
    proxy_pass http://127.0.0.1:8087/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300s;
    client_max_body_size 500M;
}
```

---

## 🔑 CLÉS API CONFIGURÉES

Dans `/opt/ia-factory/.env` :
- ✅ OPENAI_API_KEY
- ✅ ANTHROPIC_API_KEY
- ✅ GROQ_API_KEY
- ✅ GOOGLE_GENERATIVE_AI_API_KEY
- ✅ MISTRAL_API_KEY
- ✅ DEEPSEEK_API_KEY
- ✅ COHERE_API_KEY
- ✅ TOGETHER_API_KEY
- ✅ OPEN_ROUTER_API_KEY

---

## 📚 API ENDPOINTS DISPONIBLES

### Phase 1: Brand Configuration (`/api/brand`)
```
POST   /api/brand/setup                    # Créer une marque
GET    /api/brand/{brand_id}               # Récupérer une marque
PUT    /api/brand/{brand_id}               # Modifier une marque
POST   /api/brand/{brand_id}/pillars       # Ajouter des piliers de contenu
GET    /api/brand/{brand_id}/pillars       # Lister les piliers
GET    /api/brand/{brand_id}/guidelines    # Obtenir les guidelines complètes
POST   /api/brand/{brand_id}/team/invite   # Inviter un membre
GET    /api/brand/{brand_id}/team          # Lister l'équipe
PUT    /api/brand/{brand_id}/featured-topic # Définir le sujet vedette
```

### Phase 2: Content Generation (`/api/content`)
```
POST   /api/content/scripts/generate       # Générer scripts avec Claude
GET    /api/content/scripts/{brand_id}     # Lister les scripts
POST   /api/content/videos/generate        # Générer vidéos avec VEO 3
GET    /api/content/job/{job_id}           # Status d'un job
POST   /api/content/videos/edit            # Auto-éditer les vidéos
POST   /api/content/calendar/create        # Créer calendrier de contenu
GET    /api/content/calendar/{brand_id}    # Voir le calendrier
POST   /api/content/generate-all           # Workflow complet
```

### Phase 3: Distribution (`/api/distribution`)
```
GET    /api/distribution/platforms         # Plateformes supportées
POST   /api/distribution/{brand_id}/platforms/connect  # Connecter plateforme
GET    /api/distribution/{brand_id}/platforms          # Plateformes connectées
POST   /api/distribution/convert           # Convertir vidéo pour plateformes
POST   /api/distribution/adapt             # Adapter caption/hashtags
POST   /api/distribution/publish           # Publier du contenu
POST   /api/distribution/schedule          # Planifier une publication
GET    /api/distribution/scheduled/{brand_id}  # Posts planifiés
```

### Phase 4: Analytics (`/api/analytics`)
```
GET    /api/analytics/dashboard/{brand_id}        # Tableau de bord
GET    /api/analytics/content/{content_id}        # Performance d'un contenu
POST   /api/analytics/content/{content_id}/metrics # Enregistrer métriques
GET    /api/analytics/pillars/{brand_id}          # Performance par pilier
GET    /api/analytics/platforms/{brand_id}        # Performance par plateforme
GET    /api/analytics/recommendations/{brand_id}  # Recommandations AI
GET    /api/analytics/content-ideas/{brand_id}    # Idées de contenu AI
GET    /api/analytics/report/{brand_id}           # Rapport complet
GET    /api/analytics/trending/{brand_id}         # Contenu tendance
GET    /api/analytics/best-times/{brand_id}       # Meilleurs horaires
```

### System
```
GET    /health      # Health check
GET    /            # Info API
GET    /api/status  # Status détaillé des services
```

---

## ⚠️ POINTS D'ATTENTION

### 1. Préfixes des routes API
Les routers dans `app/api/*.py` n'ont PAS de préfixe local car le préfixe est défini dans `main.py` :
```python
# main.py
app.include_router(brand.router, prefix="/api/brand", ...)
app.include_router(content.router, prefix="/api/content", ...)
# etc.

# api/brand.py
router = APIRouter(tags=["Brand Configuration"])  # PAS de prefix ici !
```

### 2. Database
- MongoDB utilise Motor (async)
- Database name: `iafactory`
- Connection string dans Docker: `mongodb://mongodb:27017`

### 3. Imports dans database.py
```python
from app.database import get_db, Collections
# Collections.BRANDS, Collections.PILLARS, Collections.SCRIPTS, etc.
```

### 4. Services existants sur le même VPS
| Service | Port | Path |
|---------|------|------|
| video-operator v1 | 8085 | /video-operator/ |
| iafactory-operator v2 | 8086 | /operator/ |
| **ia-factory** | 8087 | /ia-factory/ |

---

## 🚀 COMMANDES UTILES

### Redémarrer l'API
```bash
ssh root@46.224.3.125 "cd /opt/ia-factory && docker-compose restart ia-factory-api"
```

### Voir les logs
```bash
ssh root@46.224.3.125 "docker logs ia-factory-api --tail 100"
```

### Rebuild complet
```bash
ssh root@46.224.3.125 "cd /opt/ia-factory && docker-compose up -d --build"
```

### Copier fichiers modifiés
```bash
scp D:/IAFactory/rag-dz/ia-factory/backend/app/api/*.py root@46.224.3.125:/opt/ia-factory/backend/app/api/
```

---

## 📝 DERNIÈRES MODIFICATIONS

1. **Correction préfixes API** (6 déc 2025) : Enlevé les préfixes locaux des routers pour éviter `/api/brand/api/brand/`
2. **Ajout clés API** (6 déc 2025) : Toutes les clés AI providers ajoutées au `.env`
3. **Config Nginx** (6 déc 2025) : Ajout du location block pour `/ia-factory/`

---

## 🧪 TEST RAPIDE

```bash
# Health
curl https://www.iafactoryalgeria.com/ia-factory/health

# Status
curl https://www.iafactoryalgeria.com/ia-factory/api/status

# Créer une marque
curl -X POST "https://www.iafactoryalgeria.com/ia-factory/api/brand/setup" \
  -H "Content-Type: application/json" \
  -d '{"brand_name":"Ma Marque","tone":"professional","tone_description":"Pro","key_values":["Quality"],"target_audience":"Everyone","audience_description":"All"}'
```
