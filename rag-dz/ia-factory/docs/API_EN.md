# API Documentation - IA Factory

## Overview

The IA Factory API is a REST API built with FastAPI. It provides endpoints for brand management, content creation, multi-platform distribution, and analytics.

**Base URL**: `https://www.iafactoryalgeria.com/ia-factory/api`

## Authentication

Currently, the API uses API key authentication in headers:

```
Authorization: Bearer <api_key>
```

## Endpoints

---

## 🏢 Phase 1: Brand

### Create a Brand

```http
POST /api/brand/setup
```

**Request Body**:
```json
{
  "name": "My Brand",
  "industry": "tech",
  "tone": "professional",
  "voice_description": "Innovative and accessible",
  "target_audience": "Professionals aged 25-45",
  "content_pillars": ["innovation", "tutorials", "news"],
  "visual_style": {
    "primary_color": "#2563EB",
    "secondary_color": "#1E40AF",
    "font_family": "Inter"
  }
}
```

**Response** (201 Created):
```json
{
  "id": "brand_123abc",
  "name": "My Brand",
  "industry": "tech",
  "tone": "professional",
  "created_at": "2025-01-12T10:00:00Z"
}
```

### Get a Brand

```http
GET /api/brand/{brand_id}
```

### Update a Brand

```http
PUT /api/brand/{brand_id}
```

### Create Content Pillars

```http
POST /api/brand/pillars
```

**Body**:
```json
{
  "brand_id": "brand_123abc",
  "pillars": [
    {
      "name": "Tech Innovation",
      "description": "Latest technological developments",
      "keywords": ["AI", "tech", "innovation"],
      "frequency": "weekly"
    }
  ]
}
```

### Invite Team Member

```http
POST /api/brand/team/invite
```

**Body**:
```json
{
  "brand_id": "brand_123abc",
  "email": "colleague@example.com",
  "role": "editor"
}
```

---

## 📝 Phase 2: Content

### Generate Scripts

```http
POST /api/content/generate-scripts
```

Uses Claude AI to generate video scripts.

**Body**:
```json
{
  "brand_id": "brand_123abc",
  "topic": "Introduction to Generative AI",
  "content_type": "short_video",
  "duration_seconds": 60,
  "style": "educational",
  "language": "en"
}
```

**Response**:
```json
{
  "script_id": "script_456def",
  "title": "Generative AI in 60 Seconds",
  "hook": "Did you know AI can create...",
  "body": "...",
  "call_to_action": "Subscribe for more content!",
  "estimated_duration": 58,
  "hashtags": ["#AI", "#tech", "#innovation"]
}
```

### Generate Videos

```http
POST /api/content/generate-videos
```

Uses VEO 3 via Replicate to create videos.

**Body**:
```json
{
  "script_id": "script_456def",
  "brand_id": "brand_123abc",
  "style": "modern",
  "aspect_ratio": "9:16",
  "include_subtitles": true
}
```

**Response** (Async Task):
```json
{
  "task_id": "task_789ghi",
  "status": "processing",
  "estimated_completion": "2025-01-12T10:05:00Z"
}
```

### Auto Edit

```http
POST /api/content/auto-edit
```

**Body**:
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

### Get Content Calendar

```http
GET /api/content/calendar
```

**Query Parameters**:
- `brand_id` (required): Brand ID
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

### List Contents

```http
GET /api/content/list
```

**Query Parameters**:
- `brand_id` (required)
- `status`: draft, ready, published
- `content_type`: short_video, long_video, story
- `limit`: number of results (default: 20)
- `offset`: pagination

---

## 🌐 Phase 3: Distribution

### Publish Content

```http
POST /api/distribution/publish
```

**Body**:
```json
{
  "content_id": "content_xyz",
  "platforms": ["instagram", "tiktok", "youtube"],
  "schedule": "2025-01-15T14:00:00Z",
  "captions": {
    "instagram": "Check out our latest video! 🚀 #tech",
    "tiktok": "This is amazing! 🔥 #fyp #tech",
    "youtube": "Our complete analysis of..."
  }
}
```

### Configure a Platform

```http
POST /api/distribution/platforms/connect
```

**Body**:
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

### Schedule Posts

```http
POST /api/distribution/schedule
```

**Body**:
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

### Get Publication Status

```http
GET /api/distribution/status/{publish_id}
```

---

## 📊 Phase 4: Analytics

### Dashboard

```http
GET /api/analytics/dashboard
```

**Query Parameters**:
- `brand_id` (required)
- `period`: 7d, 30d, 90d (default: 30d)

**Response**:
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

### Generate Report

```http
POST /api/analytics/reports/generate
```

**Body**:
```json
{
  "brand_id": "brand_123abc",
  "report_type": "weekly",
  "include_sections": ["overview", "content_performance", "recommendations"],
  "format": "pdf"
}
```

### AI Recommendations

```http
GET /api/analytics/recommendations
```

**Query Parameters**:
- `brand_id` (required)

**Response**:
```json
{
  "recommendations": [
    {
      "type": "timing",
      "priority": "high",
      "message": "Your Tuesday 2pm posts perform 45% better",
      "action": "Schedule more content on Tuesday afternoons"
    },
    {
      "type": "content",
      "priority": "medium", 
      "message": "Tutorials generate 2x more engagement",
      "action": "Increase tutorial frequency"
    }
  ]
}
```

### Trends

```http
GET /api/analytics/trends
```

---

## 🔧 Utilities

### Health Check

```http
GET /health
```

**Response**:
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

### API Status

```http
GET /api/status
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Successfully created |
| 400 | Invalid request |
| 401 | Not authenticated |
| 403 | Access denied |
| 404 | Resource not found |
| 422 | Validation error |
| 429 | Too many requests |
| 500 | Server error |

## Rate Limiting

- 100 requests/minute for standard endpoints
- 10 requests/minute for AI generation endpoints
- 1000 requests/hour maximum

## Webhooks

Configure webhooks to receive notifications:

```http
POST /api/webhooks/configure
```

**Body**:
```json
{
  "brand_id": "brand_123abc",
  "url": "https://your-site.com/webhook",
  "events": ["content.published", "analytics.report_ready"]
}
```

---

## SDKs and Examples

### Python

```python
import requests

API_BASE = "https://www.iafactoryalgeria.com/ia-factory/api"

# Create a brand
response = requests.post(
    f"{API_BASE}/brand/setup",
    json={
        "name": "My Brand",
        "industry": "tech",
        "tone": "professional"
    }
)
brand = response.json()

# Generate a script
script = requests.post(
    f"{API_BASE}/content/generate-scripts",
    json={
        "brand_id": brand["id"],
        "topic": "AI Introduction",
        "content_type": "short_video"
    }
).json()
```

### JavaScript/Node.js

```javascript
const API_BASE = 'https://www.iafactoryalgeria.com/ia-factory/api';

// Create a brand
const brand = await fetch(`${API_BASE}/brand/setup`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Brand',
    industry: 'tech',
    tone: 'professional'
  })
}).then(r => r.json());

// Generate a script
const script = await fetch(`${API_BASE}/content/generate-scripts`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    brand_id: brand.id,
    topic: 'AI Introduction',
    content_type: 'short_video'
  })
}).then(r => r.json());
```

### cURL

```bash
# Health check
curl https://www.iafactoryalgeria.com/ia-factory/health

# Create a brand
curl -X POST https://www.iafactoryalgeria.com/ia-factory/api/brand/setup \
  -H "Content-Type: application/json" \
  -d '{"name":"My Brand","industry":"tech","tone":"professional"}'
```
