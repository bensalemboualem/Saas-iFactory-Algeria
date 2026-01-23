# IA Factory Video Operator

Agent de montage vidéo automatique propulsé par l'IA pour les réseaux sociaux.

## 🎬 Fonctionnalités

- **Analyse automatique** : Détection de scènes, transcription audio, analyse de contenu
- **Planification IA** : Claude génère un plan de montage optimisé pour l'engagement
- **Export multi-plateforme** : Instagram Reels, TikTok, YouTube Shorts
- **Sous-titres automatiques** : Via Whisper avec style personnalisable
- **Templates prédéfinis** : Product Demo, Talking Head, Food Promo, Real Estate, etc.
- **Trilingue** : Français, Arabe, Anglais

## 🏗️ Architecture

```
iafactory-operator/
├── api/                    # FastAPI endpoints
│   └── main.py
├── core/                   # Configuration et modèles
│   ├── config.py          # Settings Pydantic
│   ├── models.py          # API models
│   └── state.py           # Internal state
├── pipeline/              # Pipeline de traitement
│   ├── analyzer.py        # Analyse vidéo (FFmpeg + Whisper)
│   ├── planner.py         # Planification (Claude LLM)
│   └── executor.py        # Exécution (FFmpeg/MoviePy)
├── services/              # Services externes
│   ├── llm_client.py      # Claude/OpenAI
│   ├── whisper_client.py  # Transcription
│   ├── storage.py         # S3 storage
│   └── queue.py           # Redis/RQ
├── worker/                # Background worker
│   ├── tasks.py
│   └── worker.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Installation

### Avec Docker (Recommandé)

```bash
# Copier la configuration
cp .env.example .env
# Éditer .env avec vos clés API

# Démarrer
docker-compose up -d
```

### Sans Docker

```bash
# Prérequis: Python 3.12, FFmpeg, Redis

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env

# Démarrer Redis
redis-server &

# Démarrer API
uvicorn api.main:app --host 0.0.0.0 --port 8085

# Démarrer Worker (autre terminal)
python worker/worker.py
```

## 📡 API

### Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/operator/video/jobs` | Créer un job de montage |
| GET | `/operator/video/jobs/{id}` | Statut du job |
| DELETE | `/operator/video/jobs/{id}` | Annuler un job |
| GET | `/operator/templates` | Liste des templates |
| GET | `/operator/platforms` | Plateformes supportées |
| GET | `/operator/health` | Health check |

### Exemple de requête

```bash
curl -X POST https://iafactoryalgeria.com/operator/video/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "source_video_url": "https://example.com/video.mp4",
    "template": "product_demo",
    "target_duration": 15,
    "platforms": ["instagram_reels", "tiktok"],
    "language": "fr",
    "add_captions": true
  }'
```

### Réponse

```json
{
  "job_id": "opv_20251206_abc123",
  "status": "pending",
  "progress": 0,
  "created_at": "2025-12-06T10:00:00Z"
}
```

## 🎨 Templates

| ID | Nom | Description |
|----|-----|-------------|
| `product_demo` | Démo Produit | Pour présenter des produits |
| `talking_head` | Face Caméra | Pour les interviews/vlogs |
| `food_promo` | Promo Restaurant | Pour la restauration |
| `real_estate` | Immobilier | Pour les biens immobiliers |
| `algerian_minimal` | Minimal Algérien | Style épuré local |
| `energetic` | Énergétique | Dynamique et rapide |
| `cinematic` | Cinématique | Style film |

## 📱 Plateformes

| ID | Résolution | Ratio | Durée Max |
|----|------------|-------|-----------|
| `instagram_reels` | 1080x1920 | 9:16 | 90s |
| `tiktok` | 1080x1920 | 9:16 | 180s |
| `youtube_shorts` | 1080x1920 | 9:16 | 60s |
| `square` | 1080x1080 | 1:1 | 60s |

## 🔧 Configuration

Variables d'environnement requises:

```env
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Storage S3
S3_ENDPOINT=https://s3.eu-west-1.amazonaws.com
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_BUCKET=iafactory-videos
S3_REGION=eu-west-1

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 🇩🇿 Made for Algeria

Optimisé pour le marché algérien avec support trilingue (FR/AR/EN) et templates adaptés aux besoins locaux.

---

**IA Factory** - Automatisation intelligente pour les créateurs de contenu
