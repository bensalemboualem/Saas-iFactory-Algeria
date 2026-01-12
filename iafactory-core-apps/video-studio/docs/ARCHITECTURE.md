# Architecture Technique - IAFactory Video Studio Pro

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           IAFACTORY VIDEO STUDIO PRO                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   FRONTEND  │    │   BACKEND   │    │   WORKERS   │    │    MEDIA    │  │
│  │   Next.js   │◄──►│   FastAPI   │◄──►│   Celery    │◄──►│   Storage   │  │
│  │   React     │    │   Python    │    │   Redis     │    │   S3/Minio  │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                  │                  │                  │          │
│         │                  │                  │                  │          │
│  ┌──────┴──────────────────┴──────────────────┴──────────────────┴──────┐  │
│  │                           API GATEWAY (nginx)                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│  ┌───────────────────────────────────┴───────────────────────────────────┐  │
│  │                          AGENTS IA ORCHESTRATOR                        │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │  │
│  │  │Scénarist│ │Storyboar│ │Director │ │ Growth  │ │  Distributor    │  │  │
│  │  │(Opus 4) │ │(Sonnet) │ │(FFmpeg) │ │ Hacker  │ │  (n8n)          │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│  ┌───────────────────────────────────┴───────────────────────────────────┐  │
│  │                          SERVICES EXTERNES                             │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │  │
│  │  │ MiniMax │ │ElevenLab│ │ Fal.ai  │ │  Suno   │ │  Anthropic API  │  │  │
│  │  │(Video)  │ │ (TTS)   │ │(Images) │ │(Musique)│ │  (Claude)       │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Flux de Production Vidéo

### Pipeline Principal

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PIPELINE DE PRODUCTION VIDÉO                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. INPUT UTILISATEUR                                                        │
│     └──► Sujet/Brief + Paramètres (durée, ton, audience, plateforme)        │
│                                                                              │
│  2. AGENT SCÉNARISTE (Claude Opus 4)                                        │
│     ├──► Recherche tendances (RAG TikTok/YouTube)                           │
│     ├──► Génération script avec timestamps                                   │
│     ├──► Hooks viraux (3 premières secondes)                                │
│     └──► Segmentation pour Shorts (moments clés)                            │
│                                                                              │
│  3. AGENT STORYBOARDER                                                       │
│     ├──► Découpage scènes visuelles                                         │
│     ├──► Génération images (Fal.ai/DALL-E)                                  │
│     ├──► Suggestions B-roll                                                  │
│     └──► Création thumbnails                                                 │
│                                                                              │
│  4. GÉNÉRATION ASSETS PARALLÈLE                                             │
│     ├──► Vidéo: MiniMax/Luma (scenes principales)                           │
│     ├──► Audio: ElevenLabs (voix-off)                                       │
│     └──► Musique: Suno AI (bande sonore)                                    │
│                                                                              │
│  5. AGENT RÉALISATEUR (Montage)                                             │
│     ├──► Assemblage FFmpeg                                                   │
│     ├──► Synchronisation audio/vidéo                                        │
│     ├──► Sous-titres multilingues (RTL support)                             │
│     ├──► Transitions et effets                                               │
│     └──► Export multi-formats (9:16, 16:9, 1:1)                             │
│                                                                              │
│  6. AGENT GROWTH HACKER                                                      │
│     ├──► Analyse viralité                                                    │
│     ├──► A/B testing titres                                                  │
│     ├──► Optimisation hashtags                                               │
│     └──► Scoring engagement prédit                                           │
│                                                                              │
│  7. AGENT DISTRIBUTEUR (n8n)                                                │
│     ├──► Upload YouTube                                                      │
│     ├──► Publication TikTok                                                  │
│     ├──► Post Instagram Reels                                                │
│     └──► Planification intelligente                                          │
│                                                                              │
│  8. OUTPUT                                                                   │
│     ├──► Podcast complet (format long)                                       │
│     ├──► 3-5 Shorts viraux (format court)                                   │
│     └──► Assets marketing (thumbnails, descriptions)                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Modèles de Données

### Script Video
```python
class VideoScript(BaseModel):
    id: UUID
    title: str
    topic: str
    target_audience: str
    platform: Literal["youtube", "tiktok", "instagram", "all"]
    duration_target: int  # en secondes
    language: Literal["fr", "ar", "darija", "en", "de", "it"]
    
    # Structure du script
    hook: str  # 3 premières secondes
    intro: str
    segments: List[ScriptSegment]
    outro: str
    cta: str  # Call to action
    
    # Metadata
    viral_score: float  # 0-100
    suggested_hashtags: List[str]
    created_at: datetime
    status: Literal["draft", "approved", "in_production", "completed"]

class ScriptSegment(BaseModel):
    timestamp_start: float
    timestamp_end: float
    content: str
    speaker: Optional[str]
    visual_direction: str
    b_roll_suggestion: Optional[str]
```

### Video Project
```python
class VideoProject(BaseModel):
    id: UUID
    user_id: UUID
    script_id: UUID
    
    # Assets générés
    video_clips: List[VideoClip]
    audio_tracks: List[AudioTrack]
    music_track: Optional[MusicTrack]
    subtitles: Dict[str, SubtitleTrack]  # langue -> piste
    thumbnail: Optional[str]  # URL
    
    # Outputs finaux
    outputs: Dict[str, str]  # format -> URL
    # Ex: {"youtube": "s3://...", "tiktok": "s3://...", "instagram": "s3://..."}
    
    # Coûts
    tokens_used: int
    cost_breakdown: Dict[str, int]
    
    # État
    status: ProjectStatus
    progress: float  # 0-100
    created_at: datetime
    completed_at: Optional[datetime]
```

---

## API Endpoints

### Scripts
```
POST   /api/v1/scripts/generate          # Générer un script
GET    /api/v1/scripts/{id}              # Récupérer un script
PUT    /api/v1/scripts/{id}              # Modifier un script
POST   /api/v1/scripts/{id}/approve      # Approuver pour production
```

### Vidéo
```
POST   /api/v1/video/generate            # Lancer génération vidéo
GET    /api/v1/video/{id}/status         # Statut de génération
GET    /api/v1/video/{id}/preview        # Prévisualisation
POST   /api/v1/video/{id}/render         # Rendu final
```

### Audio
```
POST   /api/v1/audio/tts                 # Text-to-Speech
POST   /api/v1/audio/music               # Générer musique
POST   /api/v1/audio/clone               # Cloner une voix
```

### Publication
```
POST   /api/v1/publish/youtube           # Publier YouTube
POST   /api/v1/publish/tiktok            # Publier TikTok
POST   /api/v1/publish/instagram         # Publier Instagram
POST   /api/v1/publish/schedule          # Planifier publication
```

### Tokens
```
GET    /api/v1/tokens/balance            # Solde tokens
POST   /api/v1/tokens/estimate           # Estimation coût
GET    /api/v1/tokens/history            # Historique utilisation
```

---

## Configuration Services Externes

### MiniMax (Hailuo AI)
```python
MINIMAX_CONFIG = {
    "api_base": "https://api.minimaxi.chat/v1",
    "models": {
        "video": "video-01",
        "image": "image-01"
    },
    "max_duration": 6,  # secondes par requête
    "resolution": "1080p"
}
```

### ElevenLabs
```python
ELEVENLABS_CONFIG = {
    "api_base": "https://api.elevenlabs.io/v1",
    "voices": {
        "fr_male": "voice_id_fr_m",
        "fr_female": "voice_id_fr_f",
        "ar_male": "voice_id_ar_m",
        "darija": "voice_id_darija"
    },
    "models": {
        "default": "eleven_multilingual_v2",
        "turbo": "eleven_turbo_v2"
    }
}
```

### Fal.ai
```python
FAL_CONFIG = {
    "api_base": "https://fal.run",
    "models": {
        "text_to_image": "fal-ai/flux/schnell",
        "image_to_video": "fal-ai/kling-video/v1.5/pro/image-to-video",
        "text_to_video": "fal-ai/minimax-video"
    }
}
```

### Suno AI
```python
SUNO_CONFIG = {
    "api_base": "https://api.suno.ai/v1",
    "styles": [
        "ambient", "upbeat", "dramatic", 
        "podcast_intro", "transition"
    ],
    "max_duration": 120  # secondes
}
```

---

## Système de Queues (Celery)

```python
# Queues par priorité
CELERY_QUEUES = {
    "high": {
        "exchange": "high",
        "routing_key": "high"
    },
    "default": {
        "exchange": "default", 
        "routing_key": "default"
    },
    "media": {
        "exchange": "media",
        "routing_key": "media"
    }
}

# Tâches
TASK_ROUTES = {
    "generate_script": "high",
    "generate_video": "media",
    "generate_audio": "media",
    "montage": "media",
    "publish": "default"
}
```

---

## Stockage Media

### Structure S3/MinIO
```
bucket: iafactory-video-studio
├── users/{user_id}/
│   ├── projects/{project_id}/
│   │   ├── scripts/
│   │   ├── assets/
│   │   │   ├── video/
│   │   │   ├── audio/
│   │   │   ├── images/
│   │   │   └── music/
│   │   ├── outputs/
│   │   │   ├── youtube/
│   │   │   ├── tiktok/
│   │   │   └── instagram/
│   │   └── thumbnails/
│   └── voice_clones/
└── public/
    ├── templates/
    └── samples/
```

---

## Sécurité

### Authentification
- JWT Tokens avec refresh
- OAuth2 (Google, GitHub)
- Rate limiting par utilisateur

### Permissions
```python
PERMISSIONS = {
    "free": {
        "monthly_tokens": 100,
        "max_video_duration": 60,
        "platforms": ["youtube"]
    },
    "pro": {
        "monthly_tokens": 1000,
        "max_video_duration": 600,
        "platforms": ["youtube", "tiktok", "instagram"]
    },
    "enterprise": {
        "monthly_tokens": "unlimited",
        "max_video_duration": 3600,
        "platforms": "all",
        "api_access": True
    }
}
```

---

## Monitoring

### Métriques clés
- Temps de génération par étape
- Taux de succès/échec
- Consommation tokens
- Coûts API externes
- Engagement des vidéos publiées

### Outils
- Prometheus + Grafana
- Sentry pour les erreurs
- CloudWatch/DataDog
