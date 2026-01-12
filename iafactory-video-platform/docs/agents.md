# Agents IA - IAFactory Video Platform

**Version:** 1.0.0
**Dernière mise à jour:** Décembre 2024

---

## Vue d'ensemble

La plateforme utilise une architecture multi-agents où chaque agent est spécialisé dans une tâche spécifique du pipeline de création vidéo. Cette documentation détaille les capacités, configurations et interfaces de chaque agent.

---

## 1. Orchestrator Agent

### Description
L'Orchestrator est le chef d'orchestre du pipeline. Il coordonne l'exécution des autres agents, gère les dépendances et assure la cohérence du processus de création.

### Responsabilités
- Décomposition du projet en tâches
- Ordonnancement des agents
- Gestion de la parallélisation
- Monitoring et reporting de progression
- Gestion des erreurs et retry logic

### Interface

```python
class OrchestratorAgent:
    async def start_pipeline(
        self,
        project_id: UUID,
        config: PipelineConfig
    ) -> PipelineStatus:
        """Démarre le pipeline complet de création vidéo."""
        pass

    async def get_status(self, project_id: UUID) -> PipelineStatus:
        """Retourne le statut actuel du pipeline."""
        pass

    async def pause_pipeline(self, project_id: UUID) -> bool:
        """Met en pause le pipeline."""
        pass

    async def resume_pipeline(self, project_id: UUID) -> bool:
        """Reprend un pipeline en pause."""
        pass

    async def cancel_pipeline(self, project_id: UUID) -> bool:
        """Annule le pipeline et nettoie les ressources."""
        pass
```

### Configuration

```python
@dataclass
class PipelineConfig:
    # Parallélisation
    max_parallel_tasks: int = 4

    # Timeouts (secondes)
    script_timeout: int = 60
    image_timeout: int = 120
    video_timeout: int = 300
    render_timeout: int = 600

    # Retry
    max_retries: int = 3
    retry_delay: int = 5

    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600

    # Quality
    default_resolution: str = "1080p"
    default_fps: int = 30
```

### États du Pipeline

```
┌─────────┐     ┌───────────┐     ┌────────────┐     ┌───────────┐
│ CREATED │────▶│ SCRIPTING │────▶│ GENERATING │────▶│ RENDERING │
└─────────┘     └───────────┘     └────────────┘     └───────────┘
                                                            │
                      ┌─────────┐     ┌───────────┐        │
                      │ FAILED  │◀────│ PUBLISHED │◀───────┘
                      └─────────┘     └───────────┘
```

---

## 2. Script Agent

### Description
Le Script Agent analyse le prompt utilisateur et génère un script structuré avec découpage en scènes, narration et directives visuelles.

### Capacités
- Analyse NLP du prompt
- Génération de script narratif
- Découpage temporel en scènes
- Génération de prompts visuels
- Adaptation au format cible (court, moyen, long)

### Interface

```python
class ScriptAgent:
    async def generate_script(
        self,
        prompt: str,
        config: ScriptConfig
    ) -> Script:
        """Génère un script complet à partir du prompt."""
        pass

    async def refine_scene(
        self,
        scene_id: int,
        feedback: str
    ) -> Scene:
        """Affine une scène spécifique basé sur le feedback."""
        pass

    async def translate_script(
        self,
        script: Script,
        target_language: str
    ) -> Script:
        """Traduit le script dans une autre langue."""
        pass
```

### Configuration

```python
@dataclass
class ScriptConfig:
    # Durée cible
    target_duration: int  # secondes

    # Format
    format: Literal["short", "medium", "long"] = "medium"
    # short: 15-60s (TikTok, Reels)
    # medium: 1-5min (YouTube Shorts, LinkedIn)
    # long: 5-30min (YouTube, formations)

    # Style
    tone: Literal["professional", "casual", "educational", "entertaining"]

    # Langue
    language: str = "fr"

    # LLM Provider
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo"

    # Options
    include_music_suggestions: bool = True
    include_transitions: bool = True
    generate_subtitles: bool = True
```

### Output Structure

```python
@dataclass
class Script:
    title: str
    duration: int  # secondes
    scenes: List[Scene]
    metadata: ScriptMetadata

@dataclass
class Scene:
    id: int
    start_time: float  # secondes
    end_time: float
    duration: float

    # Contenu
    narration: str
    visual_description: str
    visual_prompt: str  # prompt optimisé pour génération

    # Assets suggérés
    asset_type: Literal["image", "video", "avatar"]
    music_mood: Optional[str]
    transition_in: Optional[str]
    transition_out: Optional[str]

    # Sous-titres
    subtitles: List[SubtitleEntry]
```

### Exemple d'Output

```json
{
  "title": "Introduction à l'IA Générative",
  "duration": 120,
  "scenes": [
    {
      "id": 1,
      "start_time": 0,
      "end_time": 15,
      "duration": 15,
      "narration": "Bienvenue dans cette vidéo sur l'intelligence artificielle générative...",
      "visual_description": "Animation d'ouverture avec titre et logo",
      "visual_prompt": "Modern tech intro animation, blue and purple gradient, AI neural network visualization, cinematic, 4K quality",
      "asset_type": "video",
      "music_mood": "inspiring, technology",
      "transition_in": "fade_in",
      "transition_out": "dissolve"
    }
  ]
}
```

---

## 3. Image Agent

### Description
L'Image Agent génère des images à partir de prompts textuels en utilisant différents providers de génération d'images.

### Providers Supportés

| Provider | API | Modèles | Points Forts |
|----------|-----|---------|--------------|
| OpenAI | DALL-E 3 | dall-e-3 | Qualité, compréhension |
| Black Forest Labs | Flux | flux-pro, flux-dev | Réalisme, vitesse |
| Stability AI | SDXL | sdxl-1.0, sd-3 | Personnalisation |
| Leonardo AI | Leonardo | leonardo-v2 | Styles artistiques |
| Ideogram | Ideogram | ideogram-v2 | Texte dans images |

### Interface

```python
class ImageAgent:
    async def generate_image(
        self,
        prompt: str,
        config: ImageConfig
    ) -> GeneratedImage:
        """Génère une image à partir du prompt."""
        pass

    async def generate_variations(
        self,
        image_id: UUID,
        count: int = 4
    ) -> List[GeneratedImage]:
        """Génère des variations d'une image existante."""
        pass

    async def upscale_image(
        self,
        image_id: UUID,
        scale: int = 2
    ) -> GeneratedImage:
        """Upscale une image."""
        pass

    async def edit_image(
        self,
        image_id: UUID,
        mask: bytes,
        prompt: str
    ) -> GeneratedImage:
        """Édite une zone spécifique de l'image."""
        pass
```

### Configuration

```python
@dataclass
class ImageConfig:
    # Provider
    provider: Literal["openai", "flux", "sdxl", "leonardo", "ideogram"]

    # Dimensions
    width: int = 1920
    height: int = 1080
    aspect_ratio: Optional[str] = "16:9"

    # Qualité
    quality: Literal["standard", "hd"] = "hd"

    # Style
    style: Optional[str] = None  # "vivid", "natural", "anime", etc.
    negative_prompt: Optional[str] = None

    # Génération
    num_images: int = 1
    seed: Optional[int] = None  # pour reproductibilité
```

### Optimisation des Prompts

L'agent optimise automatiquement les prompts pour chaque provider:

```python
# Prompt utilisateur
"Une ville futuriste au coucher du soleil"

# Prompt optimisé pour DALL-E 3
"A breathtaking futuristic cityscape at sunset,
flying vehicles between towering skyscrapers with
holographic advertisements, warm orange and purple
sky, cinematic lighting, ultra detailed, 8K resolution,
trending on ArtStation"
```

---

## 4. Video Agent

### Description
Le Video Agent génère des clips vidéo à partir d'images ou de prompts textuels en utilisant les derniers modèles de génération vidéo.

### Providers Supportés

| Provider | Modèle | Durée Max | Résolution | Motion Control |
|----------|--------|-----------|------------|----------------|
| Runway | Gen-3 Alpha | 10s | 1280x768 | Camera, motion brush |
| Pika Labs | Pika 1.0 | 4s | 1024x576 | Basic |
| Luma AI | Dream Machine | 5s | 1360x752 | Camera presets |
| Kling | Kling V1 | 5s | 1280x720 | Limited |
| Haiper | Haiper 2.0 | 4s | 720p | Basic |

### Interface

```python
class VideoAgent:
    async def generate_from_image(
        self,
        image: Union[UUID, bytes],
        motion_prompt: str,
        config: VideoConfig
    ) -> GeneratedVideo:
        """Génère une vidéo à partir d'une image."""
        pass

    async def generate_from_text(
        self,
        prompt: str,
        config: VideoConfig
    ) -> GeneratedVideo:
        """Génère une vidéo à partir d'un prompt texte."""
        pass

    async def extend_video(
        self,
        video_id: UUID,
        direction: Literal["forward", "backward"]
    ) -> GeneratedVideo:
        """Étend une vidéo existante."""
        pass

    async def interpolate_frames(
        self,
        video_id: UUID,
        target_fps: int = 60
    ) -> GeneratedVideo:
        """Interpole les frames pour augmenter le FPS."""
        pass
```

### Configuration

```python
@dataclass
class VideoConfig:
    # Provider
    provider: Literal["runway", "pika", "luma", "kling", "haiper"]

    # Durée
    duration: float = 4.0  # secondes

    # Qualité
    resolution: Literal["720p", "1080p", "4k"] = "1080p"
    fps: int = 24

    # Motion
    motion_amount: float = 0.5  # 0-1
    camera_motion: Optional[CameraMotion] = None

    # Style
    style_preset: Optional[str] = None

    # Seed
    seed: Optional[int] = None

@dataclass
class CameraMotion:
    type: Literal["pan", "tilt", "zoom", "orbit", "static"]
    direction: Optional[str] = None  # "left", "right", "up", "down"
    intensity: float = 0.5
```

---

## 5. Voice Agent

### Description
Le Voice Agent génère des voix off de haute qualité à partir de texte, avec support pour de nombreuses voix et langues.

### Providers Supportés

| Provider | Voices | Langues | Cloning | Emotions |
|----------|--------|---------|---------|----------|
| ElevenLabs | 100+ | 29 | Oui | Oui |
| OpenAI TTS | 6 | 57 | Non | Limité |
| Azure TTS | 400+ | 140 | Non | Oui |
| Google TTS | 200+ | 40 | Non | Limité |

### Interface

```python
class VoiceAgent:
    async def generate_speech(
        self,
        text: str,
        config: VoiceConfig
    ) -> GeneratedAudio:
        """Génère une voix off à partir du texte."""
        pass

    async def clone_voice(
        self,
        audio_samples: List[bytes],
        voice_name: str
    ) -> VoiceProfile:
        """Clone une voix à partir d'échantillons audio."""
        pass

    async def list_voices(
        self,
        provider: str,
        language: Optional[str] = None
    ) -> List[VoiceInfo]:
        """Liste les voix disponibles."""
        pass

    async def preview_voice(
        self,
        voice_id: str,
        sample_text: str
    ) -> GeneratedAudio:
        """Génère un aperçu d'une voix."""
        pass
```

### Configuration

```python
@dataclass
class VoiceConfig:
    # Provider
    provider: Literal["elevenlabs", "openai", "azure", "google"]

    # Voice
    voice_id: str

    # Style
    stability: float = 0.5  # 0-1, plus stable = moins expressif
    similarity_boost: float = 0.75
    style: float = 0.0  # expressivité

    # Format
    output_format: Literal["mp3", "wav", "ogg"] = "mp3"
    sample_rate: int = 44100

    # Options
    speed: float = 1.0  # 0.5-2.0
    pitch: float = 0.0  # -1 à +1
```

### Voix Recommandées par Langue

| Langue | Provider | Voice ID | Style |
|--------|----------|----------|-------|
| Français | ElevenLabs | `thomas` | Professionnel |
| Français | ElevenLabs | `charlotte` | Chaleureux |
| Anglais | ElevenLabs | `adam` | Narrateur |
| Arabe | Azure | `ar-SA-HamedNeural` | Standard |

---

## 6. Avatar Agent

### Description
L'Avatar Agent génère des vidéos avec des avatars parlants synchronisés avec l'audio.

### Providers Supportés

| Provider | Type | Personnalisation | Lip-Sync Quality |
|----------|------|------------------|------------------|
| HeyGen | Photo/Avatar | Haute | Excellent |
| D-ID | Photo | Moyenne | Bon |
| Synthesia | Avatar préfait | Haute | Excellent |
| SadTalker | Photo | Basique | Acceptable |

### Interface

```python
class AvatarAgent:
    async def generate_talking_head(
        self,
        audio: Union[UUID, bytes],
        avatar: AvatarConfig
    ) -> GeneratedVideo:
        """Génère une vidéo d'avatar parlant."""
        pass

    async def create_avatar_from_photo(
        self,
        photo: bytes,
        name: str
    ) -> AvatarProfile:
        """Crée un avatar personnalisé à partir d'une photo."""
        pass

    async def list_avatars(
        self,
        provider: str
    ) -> List[AvatarInfo]:
        """Liste les avatars disponibles."""
        pass
```

### Configuration

```python
@dataclass
class AvatarConfig:
    # Provider
    provider: Literal["heygen", "did", "synthesia", "sadtalker"]

    # Avatar
    avatar_id: Optional[str] = None  # avatar préfait
    custom_photo: Optional[bytes] = None  # photo personnalisée

    # Apparence
    background: Optional[str] = None  # couleur ou image
    outfit: Optional[str] = None  # pour certains avatars

    # Animation
    expression: Literal["neutral", "happy", "serious"] = "neutral"
    gestures: bool = True

    # Output
    resolution: Literal["720p", "1080p"] = "1080p"
    aspect_ratio: str = "16:9"
```

---

## 7. Montage Agent

### Description
Le Montage Agent assemble tous les assets générés en une vidéo finale cohérente, avec transitions, effets et mixage audio.

### Capacités
- Assemblage multi-piste (vidéo, audio, voix, musique)
- Transitions animées
- Effets visuels (fade, zoom, pan)
- Mixage audio automatique
- Sous-titres intégrés
- Color grading basique
- Export multi-format

### Interface

```python
class MontageAgent:
    async def create_timeline(
        self,
        project_id: UUID,
        config: TimelineConfig
    ) -> Timeline:
        """Crée une timeline à partir des assets du projet."""
        pass

    async def render_video(
        self,
        timeline: Timeline,
        config: RenderConfig
    ) -> RenderedVideo:
        """Rend la vidéo finale."""
        pass

    async def add_subtitles(
        self,
        video_id: UUID,
        subtitles: List[SubtitleEntry]
    ) -> RenderedVideo:
        """Ajoute des sous-titres à une vidéo."""
        pass

    async def preview_segment(
        self,
        timeline: Timeline,
        start: float,
        end: float
    ) -> bytes:
        """Génère un aperçu d'un segment."""
        pass
```

### Configuration Timeline

```python
@dataclass
class TimelineConfig:
    # Dimensions
    width: int = 1920
    height: int = 1080
    fps: int = 30

    # Audio
    audio_tracks: int = 3  # voix, musique, sfx
    audio_normalize: bool = True

    # Transitions par défaut
    default_transition: str = "dissolve"
    transition_duration: float = 0.5

@dataclass
class RenderConfig:
    # Format
    format: Literal["mp4", "mov", "webm"] = "mp4"
    codec: str = "h264"

    # Qualité
    bitrate: str = "10M"
    quality: Literal["draft", "preview", "final"] = "final"

    # Audio
    audio_codec: str = "aac"
    audio_bitrate: str = "320k"
```

### Pipeline FFmpeg

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FFmpeg Pipeline                               │
└─────────────────────────────────────────────────────────────────────┘

Input Streams:
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Video 1 │  │ Video 2 │  │  Voice  │  │  Music  │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │
     ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────┐
│              Filter Complex                      │
│  - Scale/Pad to uniform size                    │
│  - Apply transitions                             │
│  - Overlay text/subtitles                       │
│  - Color correction                             │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              Audio Mix                           │
│  - Normalize levels                              │
│  - Duck music under voice                       │
│  - Apply compression                            │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              Encode Output                       │
│  - H.264/H.265 video                            │
│  - AAC audio                                    │
│  - MP4 container                                │
└─────────────────────────────────────────────────┘
```

---

## 8. Publish Agent

### Description
Le Publish Agent gère la publication automatisée des vidéos sur différentes plateformes sociales.

### Plateformes Supportées

| Plateforme | API | Upload | Scheduling | Analytics |
|------------|-----|--------|------------|-----------|
| YouTube | YouTube Data API v3 | Oui | Oui | Oui |
| TikTok | TikTok for Developers | Oui | Limité | Limité |
| Instagram | Meta Graph API | Oui | Oui | Oui |
| LinkedIn | LinkedIn Marketing API | Oui | Oui | Oui |
| Twitter/X | X API v2 | Oui | Non | Oui |
| Facebook | Meta Graph API | Oui | Oui | Oui |

### Interface

```python
class PublishAgent:
    async def publish_video(
        self,
        video_id: UUID,
        platforms: List[PlatformConfig]
    ) -> PublishResult:
        """Publie une vidéo sur les plateformes spécifiées."""
        pass

    async def schedule_publish(
        self,
        video_id: UUID,
        schedule: PublishSchedule
    ) -> ScheduledPublish:
        """Planifie une publication."""
        pass

    async def get_analytics(
        self,
        publish_id: UUID
    ) -> AnalyticsData:
        """Récupère les analytics d'une publication."""
        pass

    async def connect_platform(
        self,
        platform: str,
        credentials: OAuth2Credentials
    ) -> PlatformConnection:
        """Connecte un compte de plateforme."""
        pass
```

### Configuration par Plateforme

```python
@dataclass
class YouTubeConfig:
    title: str
    description: str
    tags: List[str]
    category_id: str = "22"  # People & Blogs
    privacy_status: Literal["public", "unlisted", "private"] = "public"
    made_for_kids: bool = False
    enable_comments: bool = True
    thumbnail: Optional[bytes] = None

@dataclass
class TikTokConfig:
    description: str  # max 2200 chars
    hashtags: List[str]
    allow_comments: bool = True
    allow_duet: bool = True
    allow_stitch: bool = True

@dataclass
class InstagramConfig:
    caption: str  # max 2200 chars
    hashtags: List[str]
    location: Optional[str] = None
    share_to_facebook: bool = False

@dataclass
class LinkedInConfig:
    text: str
    visibility: Literal["PUBLIC", "CONNECTIONS"] = "PUBLIC"
    share_media_category: str = "VIDEO"
```

### Optimisation par Plateforme

L'agent adapte automatiquement le contenu pour chaque plateforme:

| Plateforme | Ratio | Durée Max | Résolution |
|------------|-------|-----------|------------|
| YouTube | 16:9 | 12h | 4K |
| YouTube Shorts | 9:16 | 60s | 1080x1920 |
| TikTok | 9:16 | 10min | 1080x1920 |
| Instagram Reels | 9:16 | 90s | 1080x1920 |
| Instagram Feed | 1:1, 4:5 | 60s | 1080x1080 |
| LinkedIn | 16:9, 1:1 | 10min | 1920x1080 |

---

## Intégration entre Agents

### Communication

Les agents communiquent via un bus de messages Redis:

```python
# Événements publiés
"agent.script.completed"
"agent.image.generated"
"agent.video.generated"
"agent.voice.generated"
"agent.montage.completed"
"agent.publish.completed"

# Exemple de payload
{
    "event": "agent.image.generated",
    "project_id": "uuid",
    "asset_id": "uuid",
    "timestamp": "2024-12-01T10:00:00Z",
    "metadata": {
        "provider": "openai",
        "prompt": "...",
        "dimensions": "1920x1080"
    }
}
```

### Dépendances

```
Script Agent ──────────────────────────────────────────────┐
     │                                                      │
     ├──▶ Image Agent ─────────────┐                       │
     │                              │                       │
     ├──▶ Video Agent ─────────────┼──▶ Montage Agent ────┼──▶ Publish Agent
     │                              │                       │
     ├──▶ Voice Agent ─────────────┤                       │
     │                              │                       │
     └──▶ Avatar Agent ────────────┘                       │
                                                            │
                                                            ▼
                                                    [Video Published]
```

---

## Gestion des Erreurs

### Retry Logic

```python
@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

    # Erreurs à retry
    retryable_errors: List[str] = field(default_factory=lambda: [
        "RATE_LIMIT_EXCEEDED",
        "TIMEOUT",
        "SERVICE_UNAVAILABLE",
        "INTERNAL_ERROR"
    ])
```

### Fallback Providers

En cas d'échec d'un provider, l'agent peut basculer sur un autre:

```python
IMAGE_FALLBACK_CHAIN = ["openai", "flux", "sdxl", "leonardo"]
VIDEO_FALLBACK_CHAIN = ["runway", "pika", "luma", "kling"]
VOICE_FALLBACK_CHAIN = ["elevenlabs", "openai", "azure"]
```

---

## Métriques et Monitoring

### Métriques par Agent

| Agent | Métriques Clés |
|-------|---------------|
| Orchestrator | `pipeline_duration`, `success_rate`, `queue_depth` |
| Script | `generation_time`, `token_usage`, `scene_count` |
| Image | `generation_time`, `provider_usage`, `cost_per_image` |
| Video | `generation_time`, `provider_usage`, `cost_per_second` |
| Voice | `character_count`, `audio_duration`, `cost` |
| Avatar | `generation_time`, `lip_sync_quality` |
| Montage | `render_time`, `output_size`, `complexity_score` |
| Publish | `upload_time`, `success_rate`, `platform_errors` |

### Dashboard

Chaque agent expose un endpoint `/health` et `/metrics`:

```json
// GET /agents/image/health
{
    "status": "healthy",
    "provider_status": {
        "openai": "operational",
        "flux": "operational",
        "sdxl": "degraded"
    },
    "queue_depth": 5,
    "last_generation": "2024-12-01T10:00:00Z"
}

// GET /agents/image/metrics
{
    "total_generations": 1523,
    "success_rate": 0.98,
    "average_duration_ms": 2500,
    "provider_breakdown": {
        "openai": 800,
        "flux": 500,
        "sdxl": 223
    }
}
```
