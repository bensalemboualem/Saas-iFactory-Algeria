# Architecture - IAFactory Video Platform

**Version:** 1.0.0
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

IAFactory Video Platform est une plateforme de création vidéo automatisée utilisant une architecture multi-agents. Le système orchestre 8 agents IA spécialisés pour transformer une description en langage naturel en une vidéo publiable.

---

## Architecture Système

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Next.js 15 Frontend                                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │   Project    │  │   Asset      │  │   Timeline   │  │   Publish    │   │ │
│  │  │   Manager    │  │   Library    │  │   Editor     │  │   Dashboard  │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                           │
│                                      │ REST API / WebSocket                      │
│                                      ▼                                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                     FastAPI Application (Port 8001)                         │ │
│  │                                                                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │  /projects  │  │  /assets    │  │  /videos    │  │  /publish   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                                                              │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │               Authentication & Authorization (JWT)                    │   │ │
│  │  └─────────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           AGENT ORCHESTRATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                    ┌─────────────────────────────────────┐                       │
│                    │         ORCHESTRATOR AGENT          │                       │
│                    │    (Pipeline Coordinator & Router)  │                       │
│                    └─────────────────┬───────────────────┘                       │
│                                      │                                           │
│     ┌────────────────────────────────┼────────────────────────────────┐         │
│     │                                │                                │         │
│     ▼                                ▼                                ▼         │
│  ┌─────────────┐              ┌─────────────┐              ┌─────────────┐      │
│  │   SCRIPT    │              │   IMAGE     │              │   VIDEO     │      │
│  │   AGENT     │              │   AGENT     │              │   AGENT     │      │
│  │             │              │             │              │             │      │
│  │ - Script    │              │ - DALL-E 3  │              │ - Runway    │      │
│  │ - Timeline  │              │ - Flux      │              │ - Pika      │      │
│  │ - Scenes    │              │ - SDXL      │              │ - Luma      │      │
│  │ - Prompts   │              │ - Leonardo  │              │ - Kling     │      │
│  └──────┬──────┘              └──────┬──────┘              └──────┬──────┘      │
│         │                            │                            │             │
│         ▼                            ▼                            ▼             │
│  ┌─────────────┐              ┌─────────────┐              ┌─────────────┐      │
│  │   VOICE     │              │   AVATAR    │              │  MONTAGE    │      │
│  │   AGENT     │              │   AGENT     │              │   AGENT     │      │
│  │             │              │             │              │             │      │
│  │ - ElevenLabs│              │ - HeyGen    │              │ - FFmpeg    │      │
│  │ - OpenAI    │              │ - D-ID      │              │ - Timeline  │      │
│  │ - Whisper   │              │ - Synthesia │              │ - Effects   │      │
│  └─────────────┘              │ - SadTalker │              │ - Audio Mix │      │
│                               └─────────────┘              └──────┬──────┘      │
│                                                                   │             │
│                               ┌─────────────────────────────────────┘             │
│                               ▼                                                  │
│                        ┌─────────────┐                                          │
│                        │   PUBLISH   │                                          │
│                        │   AGENT     │                                          │
│                        │             │                                          │
│                        │ - YouTube   │                                          │
│                        │ - TikTok    │                                          │
│                        │ - Instagram │                                          │
│                        │ - LinkedIn  │                                          │
│                        └─────────────┘                                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA & STORAGE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  PostgreSQL  │  │    Redis     │  │    MinIO     │  │   Celery     │        │
│  │   Database   │  │    Cache     │  │   Storage    │  │   Workers    │        │
│  │   (Port 5433)│  │  (Port 6380) │  │ (Port 9000)  │  │              │        │
│  │              │  │              │  │              │  │              │        │
│  │ - Projects   │  │ - Sessions   │  │ - Videos     │  │ - Render     │        │
│  │ - Assets     │  │ - Cache      │  │ - Images     │  │ - Upload     │        │
│  │ - Timelines  │  │ - Queues     │  │ - Audio      │  │ - Publish    │        │
│  │ - Users      │  │              │  │ - Temp       │  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL AI PROVIDERS                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                              LLM PROVIDERS                               │    │
│  │  OpenAI │ Anthropic │ Groq │ DeepSeek │ Mistral │ Google Gemini        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                            IMAGE GENERATORS                              │    │
│  │  DALL-E 3 │ Flux │ Stable Diffusion XL │ Leonardo │ Ideogram            │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                            VIDEO GENERATORS                              │    │
│  │  Runway Gen-3 │ Pika Labs │ Luma │ Kling │ Haiper                       │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                            AVATAR & VOICE                                │    │
│  │  HeyGen │ D-ID │ Synthesia │ ElevenLabs │ OpenAI TTS │ Whisper          │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                            MUSIC GENERATORS                              │    │
│  │  Suno │ Udio │ MusicGen │ AudioCraft                                    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Flux de Données

### Pipeline de Création Vidéo

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         VIDEO CREATION PIPELINE                                 │
└────────────────────────────────────────────────────────────────────────────────┘

1. CRÉATION DE PROJET
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Client    │────▶│   API       │────▶│   Database  │
   │   Request   │     │  /projects  │     │   Storage   │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
         ▼
2. GÉNÉRATION DE SCRIPT
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Script    │────▶│   LLM       │────▶│   Script    │
   │   Agent     │     │  Provider   │     │   + Scenes  │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
         ▼
3. GÉNÉRATION D'ASSETS (Parallèle)
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Image     │────▶│   DALL-E/   │────▶│   Images    │
   │   Agent     │     │   Flux/SDXL │     │   .png/.jpg │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Voice     │────▶│ ElevenLabs/ │────▶│   Audio     │
   │   Agent     │     │   OpenAI    │     │   .mp3/.wav │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Video     │────▶│  Runway/    │────▶│   Clips     │
   │   Agent     │     │  Pika/Luma  │     │   .mp4      │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
         ▼
4. MONTAGE FINAL
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Montage   │────▶│   FFmpeg    │────▶│   Final     │
   │   Agent     │     │   Pipeline  │     │   Video.mp4 │
   └─────────────┘     └─────────────┘     └─────────────┘
         │
         ▼
5. PUBLICATION
   ┌─────────────┐     ┌─────────────────────────────────────┐
   │   Publish   │────▶│        PLATFORM APIs                │
   │   Agent     │     │  YouTube │ TikTok │ Instagram │ ... │
   └─────────────┘     └─────────────────────────────────────┘
```

---

## Composants Détaillés

### 1. Orchestrator Agent

**Responsabilités:**
- Coordination du pipeline de création
- Gestion des dépendances entre agents
- Monitoring de progression
- Gestion des erreurs et retry

**Configuration:**
```python
class OrchestratorConfig:
    max_parallel_agents: int = 4
    retry_attempts: int = 3
    timeout_per_step: int = 300  # seconds
    enable_caching: bool = True
```

### 2. Script Agent

**Responsabilités:**
- Analyse du prompt utilisateur
- Génération du script structuré
- Découpage en scènes
- Génération des prompts pour chaque asset

**Output Structure:**
```json
{
  "title": "Titre de la vidéo",
  "duration": 120,
  "scenes": [
    {
      "id": 1,
      "duration": 15,
      "narration": "Texte de la voix off...",
      "visual_prompt": "Description pour génération d'image/vidéo...",
      "music_mood": "upbeat, corporate"
    }
  ]
}
```

### 3. Image Agent

**Providers supportés:**
| Provider | Modèle | Résolution Max | Format |
|----------|--------|----------------|--------|
| OpenAI | DALL-E 3 | 1792x1024 | PNG |
| Black Forest | Flux Pro | 2048x2048 | PNG |
| Stability | SDXL | 1024x1024 | PNG |
| Leonardo | Leonardo V2 | 1024x1024 | PNG |
| Ideogram | Ideogram V2 | 1024x1024 | PNG |

### 4. Video Agent

**Providers supportés:**
| Provider | Modèle | Durée Max | Résolution |
|----------|--------|-----------|------------|
| Runway | Gen-3 Alpha | 10s | 1280x768 |
| Pika Labs | Pika 1.0 | 4s | 1024x576 |
| Luma AI | Dream Machine | 5s | 1360x752 |
| Kling | Kling V1 | 5s | 1280x720 |

### 5. Voice Agent

**Providers supportés:**
| Provider | Voices | Langues | Qualité |
|----------|--------|---------|---------|
| ElevenLabs | 100+ | 29 | Premium |
| OpenAI TTS | 6 | 57 | High |
| Whisper | N/A | 99 | Transcription |

### 6. Avatar Agent

**Providers supportés:**
| Provider | Type | Personnalisation | Lip-Sync |
|----------|------|------------------|----------|
| HeyGen | Photo/Avatar | Haute | Oui |
| D-ID | Photo | Moyenne | Oui |
| Synthesia | Avatar | Haute | Oui |
| SadTalker | Photo | Basse | Oui |

### 7. Montage Agent

**Capacités FFmpeg:**
- Assemblage multi-piste (vidéo, audio, voix, musique)
- Transitions (fade, dissolve, wipe)
- Sous-titres et text overlays
- Color grading basique
- Export multi-format

### 8. Publish Agent

**Plateformes supportées:**
| Plateforme | API | Scheduling | Analytics |
|------------|-----|------------|-----------|
| YouTube | YouTube Data API v3 | Oui | Oui |
| TikTok | TikTok for Developers | Oui | Limité |
| Instagram | Meta Graph API | Oui | Oui |
| LinkedIn | LinkedIn Marketing API | Oui | Oui |
| Twitter/X | X API v2 | Oui | Oui |

---

## Modèles de Données

### Project

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    -- draft, scripting, generating, rendering, published
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Asset

```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    type VARCHAR(50) NOT NULL,
    -- image, video, audio, voice, music
    provider VARCHAR(100),
    prompt TEXT,
    file_path VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Timeline

```sql
CREATE TABLE timelines (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    duration_ms INTEGER,
    tracks JSONB,
    -- [{type: "video", clips: [...]}]
    render_status VARCHAR(50),
    output_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Sécurité

### Authentification

- **JWT Tokens** avec refresh tokens
- **OAuth2** pour les plateformes de publication
- **API Keys** pour les providers externes

### Stockage des Secrets

```yaml
# Configuration via variables d'environnement
OPENAI_API_KEY: ${OPENAI_API_KEY}
ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
ELEVENLABS_API_KEY: ${ELEVENLABS_API_KEY}
# ... autres clés
```

### Rate Limiting

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| /projects | 100 req | 1 min |
| /assets/generate | 20 req | 1 min |
| /videos/render | 5 req | 1 min |
| /publish | 10 req | 1 hour |

---

## Performance

### Caching Strategy

- **Redis**: Sessions, résultats LLM, metadata assets
- **MinIO**: Assets générés (images, vidéos, audio)
- **CDN**: Vidéos finales pour distribution

### Optimisations

1. **Génération parallèle** des assets indépendants
2. **Progressive rendering** pour prévisualisation
3. **Chunked upload** pour les gros fichiers
4. **WebSocket** pour les mises à jour en temps réel

---

## Monitoring

### Métriques Clés

| Métrique | Description | Alerte |
|----------|-------------|--------|
| `pipeline_duration` | Durée totale du pipeline | > 10 min |
| `agent_error_rate` | Taux d'erreur par agent | > 5% |
| `render_queue_size` | Taille de la queue de rendu | > 50 |
| `storage_usage` | Utilisation du stockage | > 80% |

### Logs

```python
# Format de log structuré
{
    "timestamp": "2024-12-01T10:00:00Z",
    "level": "INFO",
    "service": "video-platform",
    "agent": "image_agent",
    "project_id": "uuid",
    "message": "Image generated successfully",
    "duration_ms": 2500
}
```

---

## Déploiement

### Environnements

| Env | URL | Base de données |
|-----|-----|-----------------|
| Dev | localhost:8001 | PostgreSQL local |
| Staging | staging.video.iafactory.dz | Supabase staging |
| Prod | api.video.iafactory.dz | Supabase prod |

### Ressources Recommandées

| Service | CPU | RAM | Storage |
|---------|-----|-----|---------|
| API | 2 cores | 4 GB | 10 GB |
| Workers | 4 cores | 8 GB | 50 GB |
| PostgreSQL | 2 cores | 4 GB | 100 GB |
| Redis | 1 core | 2 GB | 5 GB |
| MinIO | 2 cores | 4 GB | 500 GB |

---

## Références

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [OpenAI API](https://platform.openai.com/docs)
- [ElevenLabs API](https://docs.elevenlabs.io/)
