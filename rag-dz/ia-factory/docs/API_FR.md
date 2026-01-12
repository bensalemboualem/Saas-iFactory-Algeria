# Documentation API - IA Factory

## Vue d'ensemble

L'API IA Factory est une API REST construite avec FastAPI. Elle fournit des endpoints pour la gestion de marque, la création de contenu, la distribution multi-plateforme et les analytics.

**URL de Base**: `https://www.iafactoryalgeria.com/ia-factory/api`

## Authentification

Actuellement, l'API utilise une authentification par clé API dans les headers:

```
Authorization: Bearer <api_key>
```

## Endpoints

---

## 🏢 Phase 1: Marque (Brand)

### Créer une Marque

```http
POST /api/brand/setup
```

**Corps de la Requête**:
```json
{
  "name": "Ma Marque",
  "industry": "tech",
  "tone": "professional",
  "voice_description": "Innovant et accessible",
  "target_audience": "Professionnels 25-45 ans",
  "content_pillars": ["innovation", "tutoriels", "actualités"],
  "visual_style": {
    "primary_color": "#2563EB",
    "secondary_color": "#1E40AF",
    "font_family": "Inter"
  }
}
```

**Réponse** (201 Created):
```json
{
  "id": "brand_123abc",
  "name": "Ma Marque",
  "industry": "tech",
  "tone": "professional",
  "created_at": "2025-01-12T10:00:00Z"
}
```

### Récupérer une Marque

```http
GET /api/brand/{brand_id}
```

### Mettre à Jour une Marque

```http
PUT /api/brand/{brand_id}
```

### Créer des Piliers de Contenu

```http
POST /api/brand/pillars
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "pillars": [
    {
      "name": "Innovation Tech",
      "description": "Dernières nouveautés technologiques",
      "keywords": ["AI", "tech", "innovation"],
      "frequency": "weekly"
    }
  ]
}
```

### Inviter un Membre d'Équipe

```http
POST /api/brand/team/invite
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "email": "collegue@example.com",
  "role": "editor"
}
```

---

## 📝 Phase 2: Contenu (Content)

### Générer des Scripts

```http
POST /api/content/generate-scripts
```

Utilise Claude AI pour générer des scripts de vidéo.

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "topic": "Introduction à l'IA générative",
  "content_type": "short_video",
  "duration_seconds": 60,
  "style": "educational",
  "language": "fr"
}
```

**Réponse**:
```json
{
  "script_id": "script_456def",
  "title": "L'IA Générative en 60 secondes",
  "hook": "Saviez-vous que l'IA peut créer...",
  "body": "...",
  "call_to_action": "Abonnez-vous pour plus de contenu!",
  "estimated_duration": 58,
  "hashtags": ["#AI", "#tech", "#innovation"]
}
```

### Générer des Vidéos

```http
POST /api/content/generate-videos
```

Utilise VEO 3 via Replicate pour créer des vidéos.

**Corps**:
```json
{
  "script_id": "script_456def",
  "brand_id": "brand_123abc",
  "style": "modern",
  "aspect_ratio": "9:16",
  "include_subtitles": true
}
```

**Réponse** (Tâche Async):
```json
{
  "task_id": "task_789ghi",
  "status": "processing",
  "estimated_completion": "2025-01-12T10:05:00Z"
}
```

### Édition Automatique

```http
POST /api/content/auto-edit
```

**Corps**:
```json
{
  "video_id": "video_abc123",
  "edits": {
    "add_intro": true,
    "add_outro": true,
    "add_music": true,
    "music_style": "upbeat",
    "color_grade": "vibrant"
  }
}
```

### Récupérer le Calendrier de Contenu

```http
GET /api/content/calendar
```

**Paramètres Query**:
- `brand_id` (requis): ID de la marque
- `start_date`: Date de début (YYYY-MM-DD)
- `end_date`: Date de fin (YYYY-MM-DD)

### Lister les Contenus

```http
GET /api/content/list
```

**Paramètres Query**:
- `brand_id` (requis)
- `status`: draft, ready, published
- `content_type`: short_video, long_video, story
- `limit`: nombre de résultats (défaut: 20)
- `offset`: pagination

---

## 🌐 Phase 3: Distribution

### Publier du Contenu

```http
POST /api/distribution/publish
```

**Corps**:
```json
{
  "content_id": "content_xyz",
  "platforms": ["instagram", "tiktok", "youtube"],
  "schedule": "2025-01-15T14:00:00Z",
  "captions": {
    "instagram": "Découvrez notre dernière vidéo! 🚀 #tech",
    "tiktok": "C'est incroyable! 🔥 #fyp #tech",
    "youtube": "Notre analyse complète de..."
  }
}
```

### Configurer une Plateforme

```http
POST /api/distribution/platforms/connect
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "platform": "instagram",
  "credentials": {
    "access_token": "...",
    "account_id": "..."
  }
}
```

### Planifier des Publications

```http
POST /api/distribution/schedule
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "schedule_rules": {
    "instagram": {
      "best_times": ["09:00", "12:00", "18:00"],
      "timezone": "Europe/Paris",
      "max_per_day": 3
    }
  }
}
```

### Récupérer le Statut de Publication

```http
GET /api/distribution/status/{publish_id}
```

---

## 📊 Phase 4: Analytics

### Tableau de Bord

```http
GET /api/analytics/dashboard
```

**Paramètres Query**:
- `brand_id` (requis)
- `period`: 7d, 30d, 90d (défaut: 30d)

**Réponse**:
```json
{
  "summary": {
    "total_views": 125000,
    "total_engagement": 8500,
    "engagement_rate": 6.8,
    "followers_gained": 1200
  },
  "by_platform": {
    "instagram": {
      "views": 50000,
      "likes": 4200,
      "comments": 380,
      "shares": 120
    },
    "tiktok": {
      "views": 75000,
      "likes": 6100,
      "comments": 520,
      "shares": 890
    }
  },
  "top_content": [
    {
      "content_id": "...",
      "title": "...",
      "views": 25000,
      "engagement_rate": 12.5
    }
  ]
}
```

### Générer un Rapport

```http
POST /api/analytics/reports/generate
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "report_type": "weekly",
  "include_sections": ["overview", "content_performance", "recommendations"],
  "format": "pdf"
}
```

### Recommandations AI

```http
GET /api/analytics/recommendations
```

**Paramètres Query**:
- `brand_id` (requis)

**Réponse**:
```json
{
  "recommendations": [
    {
      "type": "timing",
      "priority": "high",
      "message": "Vos posts du mardi à 14h performent 45% mieux",
      "action": "Planifiez plus de contenu le mardi après-midi"
    },
    {
      "type": "content",
      "priority": "medium", 
      "message": "Les tutoriels génèrent 2x plus d'engagement",
      "action": "Augmentez la fréquence des tutoriels"
    }
  ]
}
```

### Tendances

```http
GET /api/analytics/trends
```

---

## 🔧 Utilitaires

### Health Check

```http
GET /health
```

**Réponse**:
```json
{
  "status": "healthy",
  "services": {
    "mongodb": "connected",
    "redis": "connected",
    "ai_services": "operational"
  },
  "version": "1.0.0"
}
```

### Statut API

```http
GET /api/status
```

---

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé avec succès |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Accès refusé |
| 404 | Ressource non trouvée |
| 422 | Erreur de validation |
| 429 | Trop de requêtes |
| 500 | Erreur serveur |

## Rate Limiting

- 100 requêtes/minute pour les endpoints standard
- 10 requêtes/minute pour les endpoints de génération AI
- 1000 requêtes/heure maximum

## Webhooks

Configurez des webhooks pour recevoir des notifications:

```http
POST /api/webhooks/configure
```

**Corps**:
```json
{
  "brand_id": "brand_123abc",
  "url": "https://votre-site.com/webhook",
  "events": ["content.published", "analytics.report_ready"]
}
```

---

## SDKs et Exemples

### Python

```python
import requests

API_BASE = "https://www.iafactoryalgeria.com/ia-factory/api"

# Créer une marque
response = requests.post(
    f"{API_BASE}/brand/setup",
    json={
        "name": "Ma Marque",
        "industry": "tech",
        "tone": "professional"
    }
)
brand = response.json()

# Générer un script
script = requests.post(
    f"{API_BASE}/content/generate-scripts",
    json={
        "brand_id": brand["id"],
        "topic": "Introduction AI",
        "content_type": "short_video"
    }
).json()
```

### JavaScript/Node.js

```javascript
const API_BASE = 'https://www.iafactoryalgeria.com/ia-factory/api';

// Créer une marque
const brand = await fetch(`${API_BASE}/brand/setup`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Ma Marque',
    industry: 'tech',
    tone: 'professional'
  })
}).then(r => r.json());

// Générer un script
const script = await fetch(`${API_BASE}/content/generate-scripts`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    brand_id: brand.id,
    topic: 'Introduction AI',
    content_type: 'short_video'
  })
}).then(r => r.json());
```

### cURL

```bash
# Health check
curl https://www.iafactoryalgeria.com/ia-factory/health

# Créer une marque
curl -X POST https://www.iafactoryalgeria.com/ia-factory/api/brand/setup \
  -H "Content-Type: application/json" \
  -d '{"name":"Ma Marque","industry":"tech","tone":"professional"}'
```
