# توثيق API - IA Factory

## نظرة عامة

API الخاص بـ IA Factory هو واجهة برمجة REST مبنية على FastAPI. يوفر نقاط نهاية لإدارة العلامات التجارية وإنشاء المحتوى والتوزيع متعدد المنصات والتحليلات.

**عنوان URL الأساسي**: `https://www.iafactoryalgeria.com/ia-factory/api`

## المصادقة

حالياً، يستخدم API المصادقة بمفتاح API في الرؤوس:

```
Authorization: Bearer <api_key>
```

## نقاط النهاية

---

## 🏢 المرحلة 1: العلامة التجارية (Brand)

### إنشاء علامة تجارية

```http
POST /api/brand/setup
```

**جسم الطلب**:
```json
{
  "name": "علامتي التجارية",
  "industry": "tech",
  "tone": "professional",
  "voice_description": "مبتكر وسهل الوصول",
  "target_audience": "محترفون بعمر 25-45 سنة",
  "content_pillars": ["ابتكار", "دروس تعليمية", "أخبار"],
  "visual_style": {
    "primary_color": "#2563EB",
    "secondary_color": "#1E40AF",
    "font_family": "Inter"
  }
}
```

**الاستجابة** (201 Created):
```json
{
  "id": "brand_123abc",
  "name": "علامتي التجارية",
  "industry": "tech",
  "tone": "professional",
  "created_at": "2025-01-12T10:00:00Z"
}
```

### استرجاع علامة تجارية

```http
GET /api/brand/{brand_id}
```

### تحديث علامة تجارية

```http
PUT /api/brand/{brand_id}
```

### إنشاء أعمدة المحتوى

```http
POST /api/brand/pillars
```

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "pillars": [
    {
      "name": "الابتكار التقني",
      "description": "آخر التطورات التكنولوجية",
      "keywords": ["AI", "tech", "ابتكار"],
      "frequency": "weekly"
    }
  ]
}
```

### دعوة عضو فريق

```http
POST /api/brand/team/invite
```

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "email": "colleague@example.com",
  "role": "editor"
}
```

---

## 📝 المرحلة 2: المحتوى (Content)

### توليد النصوص

```http
POST /api/content/generate-scripts
```

يستخدم Claude AI لتوليد نصوص الفيديو.

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "topic": "مقدمة في الذكاء الاصطناعي التوليدي",
  "content_type": "short_video",
  "duration_seconds": 60,
  "style": "educational",
  "language": "ar"
}
```

**الاستجابة**:
```json
{
  "script_id": "script_456def",
  "title": "الذكاء الاصطناعي التوليدي في 60 ثانية",
  "hook": "هل تعلم أن الذكاء الاصطناعي يمكنه إنشاء...",
  "body": "...",
  "call_to_action": "اشترك للمزيد من المحتوى!",
  "estimated_duration": 58,
  "hashtags": ["#AI", "#تقنية", "#ابتكار"]
}
```

### توليد الفيديوهات

```http
POST /api/content/generate-videos
```

يستخدم VEO 3 عبر Replicate لإنشاء الفيديوهات.

**الجسم**:
```json
{
  "script_id": "script_456def",
  "brand_id": "brand_123abc",
  "style": "modern",
  "aspect_ratio": "9:16",
  "include_subtitles": true
}
```

**الاستجابة** (مهمة غير متزامنة):
```json
{
  "task_id": "task_789ghi",
  "status": "processing",
  "estimated_completion": "2025-01-12T10:05:00Z"
}
```

### التحرير التلقائي

```http
POST /api/content/auto-edit
```

**الجسم**:
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

### استرجاع تقويم المحتوى

```http
GET /api/content/calendar
```

**معلمات الاستعلام**:
- `brand_id` (مطلوب): معرف العلامة التجارية
- `start_date`: تاريخ البداية (YYYY-MM-DD)
- `end_date`: تاريخ النهاية (YYYY-MM-DD)

### قائمة المحتويات

```http
GET /api/content/list
```

**معلمات الاستعلام**:
- `brand_id` (مطلوب)
- `status`: draft, ready, published
- `content_type`: short_video, long_video, story
- `limit`: عدد النتائج (افتراضي: 20)
- `offset`: التصفح

---

## 🌐 المرحلة 3: التوزيع (Distribution)

### نشر المحتوى

```http
POST /api/distribution/publish
```

**الجسم**:
```json
{
  "content_id": "content_xyz",
  "platforms": ["instagram", "tiktok", "youtube"],
  "schedule": "2025-01-15T14:00:00Z",
  "captions": {
    "instagram": "شاهد آخر فيديو لنا! 🚀 #تقنية",
    "tiktok": "هذا مذهل! 🔥 #fyp #تقنية",
    "youtube": "تحليلنا الكامل لـ..."
  }
}
```

### تكوين منصة

```http
POST /api/distribution/platforms/connect
```

**الجسم**:
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

### جدولة المنشورات

```http
POST /api/distribution/schedule
```

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "schedule_rules": {
    "instagram": {
      "best_times": ["09:00", "12:00", "18:00"],
      "timezone": "Africa/Algiers",
      "max_per_day": 3
    }
  }
}
```

### الحصول على حالة النشر

```http
GET /api/distribution/status/{publish_id}
```

---

## 📊 المرحلة 4: التحليلات (Analytics)

### لوحة التحكم

```http
GET /api/analytics/dashboard
```

**معلمات الاستعلام**:
- `brand_id` (مطلوب)
- `period`: 7d, 30d, 90d (افتراضي: 30d)

**الاستجابة**:
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

### توليد تقرير

```http
POST /api/analytics/reports/generate
```

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "report_type": "weekly",
  "include_sections": ["overview", "content_performance", "recommendations"],
  "format": "pdf"
}
```

### توصيات الذكاء الاصطناعي

```http
GET /api/analytics/recommendations
```

**معلمات الاستعلام**:
- `brand_id` (مطلوب)

**الاستجابة**:
```json
{
  "recommendations": [
    {
      "type": "timing",
      "priority": "high",
      "message": "منشوراتك يوم الثلاثاء الساعة 2 ظهراً تحقق أداء أفضل بنسبة 45%",
      "action": "جدول المزيد من المحتوى ظهر يوم الثلاثاء"
    },
    {
      "type": "content",
      "priority": "medium", 
      "message": "الدروس التعليمية تولد تفاعل أكثر بمرتين",
      "action": "زد من تكرار الدروس التعليمية"
    }
  ]
}
```

### الاتجاهات

```http
GET /api/analytics/trends
```

---

## 🔧 الأدوات المساعدة

### فحص الصحة

```http
GET /health
```

**الاستجابة**:
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

### حالة API

```http
GET /api/status
```

---

## رموز الأخطاء

| الرمز | الوصف |
|------|-------|
| 200 | نجاح |
| 201 | تم الإنشاء بنجاح |
| 400 | طلب غير صالح |
| 401 | غير مصادق |
| 403 | الوصول مرفوض |
| 404 | المورد غير موجود |
| 422 | خطأ في التحقق |
| 429 | طلبات كثيرة جداً |
| 500 | خطأ في الخادم |

## تحديد المعدل

- 100 طلب/دقيقة لنقاط النهاية العادية
- 10 طلبات/دقيقة لنقاط نهاية توليد الذكاء الاصطناعي
- 1000 طلب/ساعة كحد أقصى

## Webhooks

قم بتكوين webhooks لتلقي الإشعارات:

```http
POST /api/webhooks/configure
```

**الجسم**:
```json
{
  "brand_id": "brand_123abc",
  "url": "https://your-site.com/webhook",
  "events": ["content.published", "analytics.report_ready"]
}
```

---

## SDKs والأمثلة

### Python

```python
import requests

API_BASE = "https://www.iafactoryalgeria.com/ia-factory/api"

# إنشاء علامة تجارية
response = requests.post(
    f"{API_BASE}/brand/setup",
    json={
        "name": "علامتي التجارية",
        "industry": "tech",
        "tone": "professional"
    }
)
brand = response.json()

# توليد نص
script = requests.post(
    f"{API_BASE}/content/generate-scripts",
    json={
        "brand_id": brand["id"],
        "topic": "مقدمة في الذكاء الاصطناعي",
        "content_type": "short_video"
    }
).json()
```

### JavaScript/Node.js

```javascript
const API_BASE = 'https://www.iafactoryalgeria.com/ia-factory/api';

// إنشاء علامة تجارية
const brand = await fetch(`${API_BASE}/brand/setup`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'علامتي التجارية',
    industry: 'tech',
    tone: 'professional'
  })
}).then(r => r.json());

// توليد نص
const script = await fetch(`${API_BASE}/content/generate-scripts`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    brand_id: brand.id,
    topic: 'مقدمة في الذكاء الاصطناعي',
    content_type: 'short_video'
  })
}).then(r => r.json());
```

### cURL

```bash
# فحص الصحة
curl https://www.iafactoryalgeria.com/ia-factory/health

# إنشاء علامة تجارية
curl -X POST https://www.iafactoryalgeria.com/ia-factory/api/brand/setup \
  -H "Content-Type: application/json" \
  -d '{"name":"علامتي التجارية","industry":"tech","tone":"professional"}'
```
