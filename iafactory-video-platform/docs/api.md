# API Reference - IAFactory Video Platform

**Version:** 1.0.0
**Base URL:** `http://localhost:8001/api/v1`
**Dernière mise à jour:** Décembre 2024

---

## Authentification

Toutes les requêtes API nécessitent un token JWT dans l'en-tête Authorization.

```http
Authorization: Bearer <access_token>
```

### Obtenir un Token

```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Réponse:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

---

## Projects

### Créer un Projet

```http
POST /projects
Content-Type: application/json
Authorization: Bearer <token>

{
    "title": "Ma Vidéo IA",
    "description": "Une vidéo générée par IA sur le machine learning",
    "prompt": "Créer une vidéo explicative de 2 minutes sur le machine learning pour débutants, avec un ton professionnel et des animations modernes",
    "config": {
        "target_duration": 120,
        "format": "medium",
        "language": "fr",
        "style": "professional"
    }
}
```

**Réponse:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Ma Vidéo IA",
    "description": "Une vidéo générée par IA sur le machine learning",
    "status": "draft",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
}
```

### Lister les Projets

```http
GET /projects?page=1&limit=10&status=draft
Authorization: Bearer <token>
```

**Paramètres Query:**
| Paramètre | Type | Description |
|-----------|------|-------------|
| `page` | int | Numéro de page (défaut: 1) |
| `limit` | int | Nombre par page (défaut: 10, max: 100) |
| `status` | string | Filtrer par statut |
| `search` | string | Recherche dans titre/description |

**Réponse:**
```json
{
    "items": [...],
    "total": 42,
    "page": 1,
    "limit": 10,
    "pages": 5
}
```

### Obtenir un Projet

```http
GET /projects/{project_id}
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Ma Vidéo IA",
    "description": "...",
    "status": "generating",
    "progress": {
        "overall": 45,
        "current_step": "image_generation",
        "steps": {
            "script": { "status": "completed", "progress": 100 },
            "images": { "status": "in_progress", "progress": 60 },
            "videos": { "status": "pending", "progress": 0 },
            "voice": { "status": "pending", "progress": 0 },
            "montage": { "status": "pending", "progress": 0 }
        }
    },
    "assets": [...],
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:30:00Z"
}
```

### Démarrer le Pipeline

```http
POST /projects/{project_id}/start
Authorization: Bearer <token>
Content-Type: application/json

{
    "pipeline_config": {
        "skip_steps": [],
        "providers": {
            "llm": "openai",
            "image": "dalle3",
            "video": "runway",
            "voice": "elevenlabs"
        }
    }
}
```

**Réponse:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "scripting",
    "pipeline_id": "pipe-123456",
    "estimated_duration": 300,
    "message": "Pipeline started successfully"
}
```

### Obtenir le Statut du Pipeline

```http
GET /projects/{project_id}/status
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "pipeline_id": "pipe-123456",
    "status": "generating",
    "progress": 45,
    "current_step": {
        "name": "image_generation",
        "agent": "image_agent",
        "started_at": "2024-12-01T10:15:00Z",
        "items_total": 10,
        "items_completed": 6
    },
    "steps_completed": ["script"],
    "steps_remaining": ["videos", "voice", "montage"],
    "estimated_remaining_seconds": 180,
    "logs": [
        {
            "timestamp": "2024-12-01T10:15:00Z",
            "level": "info",
            "message": "Starting image generation for 10 scenes"
        }
    ]
}
```

### Annuler un Pipeline

```http
POST /projects/{project_id}/cancel
Authorization: Bearer <token>
```

---

## Assets

### Générer des Images

```http
POST /assets/images/generate
Authorization: Bearer <token>
Content-Type: application/json

{
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "prompts": [
        {
            "scene_id": 1,
            "prompt": "A futuristic city skyline at sunset, cyberpunk style, neon lights",
            "negative_prompt": "blurry, low quality"
        }
    ],
    "config": {
        "provider": "openai",
        "model": "dall-e-3",
        "size": "1792x1024",
        "quality": "hd",
        "style": "vivid"
    }
}
```

**Réponse:**
```json
{
    "batch_id": "batch-123456",
    "status": "processing",
    "images": [
        {
            "id": "img-001",
            "scene_id": 1,
            "status": "pending",
            "prompt": "..."
        }
    ]
}
```

### Générer de la Voix

```http
POST /assets/voice/generate
Authorization: Bearer <token>
Content-Type: application/json

{
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "segments": [
        {
            "scene_id": 1,
            "text": "Bienvenue dans cette vidéo sur l'intelligence artificielle...",
            "voice_id": "thomas",
            "language": "fr"
        }
    ],
    "config": {
        "provider": "elevenlabs",
        "stability": 0.5,
        "similarity_boost": 0.75,
        "output_format": "mp3"
    }
}
```

**Réponse:**
```json
{
    "batch_id": "batch-789012",
    "status": "processing",
    "segments": [
        {
            "id": "voice-001",
            "scene_id": 1,
            "status": "processing",
            "estimated_duration": 15.5
        }
    ]
}
```

### Générer de la Musique

```http
POST /assets/music/generate
Authorization: Bearer <token>
Content-Type: application/json

{
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "prompt": "Upbeat corporate background music, inspiring, technology theme",
    "config": {
        "provider": "suno",
        "duration": 120,
        "style": "instrumental",
        "tempo": "medium"
    }
}
```

### Lister les Assets d'un Projet

```http
GET /assets?project_id={project_id}&type=image
Authorization: Bearer <token>
```

**Paramètres Query:**
| Paramètre | Type | Description |
|-----------|------|-------------|
| `project_id` | uuid | ID du projet |
| `type` | string | Type d'asset (image, video, voice, music) |
| `status` | string | Statut (pending, processing, completed, failed) |

### Télécharger un Asset

```http
GET /assets/{asset_id}/download
Authorization: Bearer <token>
```

Retourne le fichier binaire avec le Content-Type approprié.

---

## Videos

### Créer une Timeline

```http
POST /videos/timeline
Authorization: Bearer <token>
Content-Type: application/json

{
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "config": {
        "resolution": "1920x1080",
        "fps": 30,
        "background_color": "#000000"
    },
    "tracks": [
        {
            "type": "video",
            "clips": [
                {
                    "asset_id": "img-001",
                    "start_time": 0,
                    "duration": 5,
                    "transition_in": "fade",
                    "transition_out": "dissolve"
                }
            ]
        },
        {
            "type": "audio",
            "clips": [
                {
                    "asset_id": "voice-001",
                    "start_time": 0,
                    "volume": 1.0
                }
            ]
        },
        {
            "type": "music",
            "clips": [
                {
                    "asset_id": "music-001",
                    "start_time": 0,
                    "volume": 0.3,
                    "duck_under_voice": true
                }
            ]
        }
    ]
}
```

**Réponse:**
```json
{
    "id": "timeline-123456",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "duration": 120.5,
    "tracks": [...],
    "status": "draft",
    "created_at": "2024-12-01T11:00:00Z"
}
```

### Lancer le Rendu

```http
POST /videos/render
Authorization: Bearer <token>
Content-Type: application/json

{
    "timeline_id": "timeline-123456",
    "config": {
        "format": "mp4",
        "codec": "h264",
        "quality": "high",
        "bitrate": "10M",
        "audio_codec": "aac",
        "audio_bitrate": "320k"
    },
    "output": {
        "include_subtitles": true,
        "subtitle_style": "default"
    }
}
```

**Réponse:**
```json
{
    "render_id": "render-123456",
    "timeline_id": "timeline-123456",
    "status": "queued",
    "position_in_queue": 3,
    "estimated_duration": 180,
    "message": "Render job queued successfully"
}
```

### Obtenir le Statut du Rendu

```http
GET /videos/render/{render_id}/status
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "render_id": "render-123456",
    "status": "rendering",
    "progress": 65,
    "current_stage": "encoding",
    "stages": {
        "preparation": { "status": "completed", "duration": 5 },
        "compositing": { "status": "completed", "duration": 45 },
        "encoding": { "status": "in_progress", "progress": 65 },
        "finalization": { "status": "pending" }
    },
    "started_at": "2024-12-01T11:05:00Z",
    "estimated_completion": "2024-12-01T11:10:00Z"
}
```

### Télécharger la Vidéo Rendue

```http
GET /videos/{video_id}/download
Authorization: Bearer <token>
```

---

## Publication

### Publier une Vidéo

```http
POST /publish
Authorization: Bearer <token>
Content-Type: application/json

{
    "video_id": "video-123456",
    "platforms": [
        {
            "platform": "youtube",
            "config": {
                "title": "Introduction à l'IA - Tutoriel Complet",
                "description": "Dans cette vidéo, nous explorons...",
                "tags": ["IA", "machine learning", "tutoriel"],
                "category_id": "28",
                "privacy_status": "public",
                "thumbnail_asset_id": "thumb-001"
            }
        },
        {
            "platform": "linkedin",
            "config": {
                "text": "Nouvelle vidéo sur l'IA! #AI #MachineLearning",
                "visibility": "PUBLIC"
            }
        }
    ]
}
```

**Réponse:**
```json
{
    "publish_batch_id": "pub-123456",
    "status": "processing",
    "publications": [
        {
            "id": "pub-yt-001",
            "platform": "youtube",
            "status": "uploading",
            "progress": 0
        },
        {
            "id": "pub-li-001",
            "platform": "linkedin",
            "status": "queued"
        }
    ]
}
```

### Planifier une Publication

```http
POST /publish/schedule
Authorization: Bearer <token>
Content-Type: application/json

{
    "video_id": "video-123456",
    "schedule": {
        "publish_at": "2024-12-15T14:00:00Z",
        "timezone": "Europe/Paris"
    },
    "platforms": [...]
}
```

### Obtenir le Statut de Publication

```http
GET /publish/{publish_id}/status
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "publish_id": "pub-yt-001",
    "platform": "youtube",
    "status": "published",
    "published_at": "2024-12-01T12:00:00Z",
    "platform_url": "https://youtube.com/watch?v=abc123",
    "platform_id": "abc123",
    "analytics": {
        "views": 150,
        "likes": 12,
        "comments": 3,
        "last_updated": "2024-12-01T15:00:00Z"
    }
}
```

### Lister les Connexions de Plateformes

```http
GET /publish/connections
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "connections": [
        {
            "platform": "youtube",
            "connected": true,
            "account_name": "Ma Chaîne",
            "expires_at": "2025-01-01T00:00:00Z"
        },
        {
            "platform": "tiktok",
            "connected": false
        }
    ]
}
```

### Connecter une Plateforme

```http
GET /publish/connect/{platform}
Authorization: Bearer <token>
```

Redirige vers le flux OAuth de la plateforme.

---

## Voix

### Lister les Voix Disponibles

```http
GET /voices?provider=elevenlabs&language=fr
Authorization: Bearer <token>
```

**Réponse:**
```json
{
    "voices": [
        {
            "id": "thomas",
            "name": "Thomas",
            "provider": "elevenlabs",
            "language": "fr",
            "gender": "male",
            "style": "professional",
            "preview_url": "https://..."
        }
    ]
}
```

### Prévisualiser une Voix

```http
POST /voices/{voice_id}/preview
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "Bonjour, ceci est un test de voix.",
    "provider": "elevenlabs"
}
```

---

## Webhooks

### Configurer un Webhook

```http
POST /webhooks
Authorization: Bearer <token>
Content-Type: application/json

{
    "url": "https://myapp.com/webhook",
    "events": [
        "project.completed",
        "render.completed",
        "publish.completed"
    ],
    "secret": "my-webhook-secret"
}
```

### Événements Disponibles

| Événement | Description |
|-----------|-------------|
| `project.created` | Projet créé |
| `project.started` | Pipeline démarré |
| `project.completed` | Pipeline terminé |
| `project.failed` | Pipeline échoué |
| `render.started` | Rendu démarré |
| `render.completed` | Rendu terminé |
| `render.failed` | Rendu échoué |
| `publish.completed` | Publication réussie |
| `publish.failed` | Publication échouée |

### Format des Webhooks

```json
{
    "event": "project.completed",
    "timestamp": "2024-12-01T12:00:00Z",
    "data": {
        "project_id": "550e8400-e29b-41d4-a716-446655440000",
        "video_url": "https://storage.iafactory.dz/videos/...",
        "duration": 120
    },
    "signature": "sha256=..."
}
```

---

## Codes d'Erreur

| Code | Signification |
|------|---------------|
| 400 | Bad Request - Paramètres invalides |
| 401 | Unauthorized - Token manquant ou invalide |
| 403 | Forbidden - Accès refusé |
| 404 | Not Found - Ressource introuvable |
| 409 | Conflict - Conflit (ex: projet déjà en cours) |
| 422 | Unprocessable Entity - Validation échouée |
| 429 | Too Many Requests - Rate limit dépassé |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Service temporairement indisponible |

### Format des Erreurs

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Le champ 'title' est requis",
        "details": {
            "field": "title",
            "constraint": "required"
        }
    }
}
```

---

## Rate Limiting

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| Général | 1000 req | 1 min |
| `/projects` | 100 req | 1 min |
| `/assets/*/generate` | 20 req | 1 min |
| `/videos/render` | 5 req | 1 min |
| `/publish` | 10 req | 1 heure |

Les headers de réponse incluent:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1701432000
```

---

## WebSocket API

### Connexion

```javascript
const ws = new WebSocket('wss://api.video.iafactory.dz/ws');
ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer <access_token>'
}));
```

### Événements en Temps Réel

```javascript
// Écouter les mises à jour de projet
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'project:550e8400-e29b-41d4-a716-446655440000'
}));

// Recevoir les mises à jour
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // { type: 'progress', progress: 45, step: 'image_generation' }
};
```

---

## SDKs

### Python

```python
from iafactory_video import VideoClient

client = VideoClient(api_key="your-api-key")

# Créer un projet
project = client.projects.create(
    title="Ma Vidéo",
    prompt="Créer une vidéo sur l'IA..."
)

# Démarrer le pipeline
client.projects.start(project.id)

# Attendre la fin
result = client.projects.wait_for_completion(project.id)
```

### JavaScript/TypeScript

```typescript
import { VideoClient } from '@iafactory/video-sdk';

const client = new VideoClient({ apiKey: 'your-api-key' });

// Créer et générer
const project = await client.projects.create({
    title: 'Ma Vidéo',
    prompt: 'Créer une vidéo sur l\'IA...'
});

await client.projects.start(project.id);

// Suivre la progression
client.projects.onProgress(project.id, (progress) => {
    console.log(`Progress: ${progress.percentage}%`);
});
```
