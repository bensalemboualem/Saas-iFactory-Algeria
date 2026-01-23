# وثائق Webhooks API

**IAFACTORY - وثائق Webhooks**

*آخر تحديث: 19 يناير 2026*

---

## جدول المحتويات

1. [مقدمة](#1-مقدمة)
2. [التكوين](#2-التكوين)
3. [الأحداث المتاحة](#3-الأحداث-المتاحة)
4. [تنسيق البيانات](#4-تنسيق-البيانات)
5. [الأمان](#5-الأمان)
6. [إدارة الأخطاء](#6-إدارة-الأخطاء)
7. [أمثلة التكامل](#7-أمثلة-التكامل)

---

## 1. مقدمة

تتيح webhooks IAFACTORY لتطبيقك تلقي إشعارات في الوقت الفعلي عند حدوث أحداث في حسابك.

### حالات الاستخدام

- مزامنة بيانات المستخدم مع CRM الخاص بك
- تشغيل إجراءات بعد إنشاء المحتوى
- مراقبة استخدام الأرصدة
- أتمتة الفوترة

---

## 2. التكوين

### 2.1 عبر لوحة التحكم

1. سجل الدخول إلى [app.iafactory.ai](https://app.iafactory.ai)
2. انتقل إلى **الإعدادات** > **المطورين** > **Webhooks**
3. انقر على **إضافة نقطة نهاية**
4. أدخل عنوان URL لنقطة النهاية
5. حدد الأحداث للاستماع إليها
6. انسخ **مفتاح التوقيع** المُنشأ

### 2.2 عبر API

```bash
POST /api/v1/webhooks/endpoints
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/iafactory",
  "events": ["conversation.created", "credits.low"],
  "description": "Webhook الإنتاج"
}
```

**الاستجابة:**

```json
{
  "id": "we_123abc",
  "url": "https://your-app.com/webhooks/iafactory",
  "events": ["conversation.created", "credits.low"],
  "secret": "whsec_xxxxxxxxxxxxx",
  "status": "active",
  "created_at": "2026-01-19T10:00:00Z"
}
```

---

## 3. الأحداث المتاحة

### 3.1 المحادثات

| الحدث | الوصف |
|-------|-------|
| `conversation.created` | محادثة جديدة أُنشئت |
| `conversation.updated` | محادثة معدّلة (العنوان، إلخ) |
| `conversation.deleted` | محادثة محذوفة |
| `message.created` | رسالة جديدة (مستخدم أو مساعد) |

### 3.2 التوليد

| الحدث | الوصف |
|-------|-------|
| `generation.started` | بدأ توليد الذكاء الاصطناعي |
| `generation.completed` | اكتمل توليد الذكاء الاصطناعي بنجاح |
| `generation.failed` | فشل التوليد |
| `image.generated` | صورة مُنشأة (DALL-E، إلخ) |

### 3.3 الأرصدة

| الحدث | الوصف |
|-------|-------|
| `credits.consumed` | أرصدة مُستهلكة |
| `credits.low` | الحد الأدنى (< 10% متبقي) |
| `credits.depleted` | الأرصدة منتهية |
| `credits.reset` | الأرصدة الشهرية أُعيد تعيينها |

### 3.4 الاشتراك

| الحدث | الوصف |
|-------|-------|
| `subscription.created` | اشتراك جديد |
| `subscription.updated` | الباقة معدّلة |
| `subscription.canceled` | الاشتراك ملغى |
| `subscription.renewed` | الاشتراك مُجدد |
| `payment.succeeded` | الدفع ناجح |
| `payment.failed` | فشل الدفع |

### 3.5 المستخدم

| الحدث | الوصف |
|-------|-------|
| `user.created` | الحساب أُنشئ |
| `user.updated` | الملف الشخصي محدّث |
| `user.deleted` | الحساب محذوف |

---

## 4. تنسيق البيانات

### 4.1 الهيكل العام

جميع webhooks تتبع هذا الهيكل:

```json
{
  "id": "evt_abc123",
  "type": "conversation.created",
  "created_at": "2026-01-19T10:30:00Z",
  "data": {
    // بيانات خاصة بالحدث
  },
  "metadata": {
    "user_id": "usr_xyz",
    "account_id": "acc_123"
  }
}
```

### 4.2 أمثلة حسب النوع

#### conversation.created

```json
{
  "id": "evt_conv_001",
  "type": "conversation.created",
  "created_at": "2026-01-19T10:30:00Z",
  "data": {
    "conversation": {
      "id": "conv_abc123",
      "title": "محادثة جديدة",
      "model": "gpt-4",
      "created_at": "2026-01-19T10:30:00Z"
    }
  },
  "metadata": {
    "user_id": "usr_xyz"
  }
}
```

#### credits.low

```json
{
  "id": "evt_cred_001",
  "type": "credits.low",
  "created_at": "2026-01-19T10:32:00Z",
  "data": {
    "current_credits": 850,
    "total_credits": 10000,
    "percentage_remaining": 8.5,
    "estimated_depletion": "2026-01-21T00:00:00Z"
  },
  "metadata": {
    "user_id": "usr_xyz",
    "plan": "pro"
  }
}
```

---

## 5. الأمان

### 5.1 التحقق من التوقيع

كل طلب webhook يتضمن header `X-IAFactory-Signature` يحتوي على توقيع HMAC-SHA256.

**تنسيق Header:**
```
X-IAFactory-Signature: t=1705661400,v1=5257a869e7...
```

### 5.2 تنفيذ التحقق

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const parts = signature.split(',').reduce((acc, part) => {
    const [key, value] = part.split('=');
    acc[key] = value;
    return acc;
  }, {} as Record<string, string>);

  const t = parts['t'];
  const v1 = parts['v1'];

  // التحقق من الطابع الزمني (رفض إذا > 5 دقائق)
  const now = Math.floor(Date.now() / 1000);
  if (now - parseInt(t) > 300) {
    return false;
  }

  // حساب التوقيع المتوقع
  const signedPayload = `${t}.${payload}`;
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(v1),
    Buffer.from(expectedSignature)
  );
}
```

### 5.3 أفضل الممارسات

1. **تحقق دائماً من التوقيع** قبل معالجة webhook
2. **تحقق من الطابع الزمني** لتجنب هجمات إعادة التشغيل
3. **استخدم HTTPS** لنقطة النهاية
4. **حدد عناوين IP** إن أمكن

---

## 6. إدارة الأخطاء

### 6.1 سياسة إعادة المحاولة

| المحاولة | التأخير |
|----------|---------|
| 1 | فوري |
| 2 | 1 دقيقة |
| 3 | 5 دقائق |
| 4 | 30 دقيقة |
| 5 | 2 ساعة |
| 6 | 6 ساعات |
| 7 | 24 ساعة |

### 6.2 رموز الاستجابة المتوقعة

| الرمز | التفسير |
|-------|---------|
| 2xx | نجاح، لا إعادة محاولة |
| 4xx | فشل دائم، لا إعادة محاولة |
| 429 | حد المعدل، إعادة محاولة مع تراجع |
| 5xx | إعادة محاولة حسب السياسة |

### 6.3 المهلة الزمنية

- **مهلة الاتصال**: 10 ثواني
- **مهلة الاستجابة**: 30 ثانية

---

## 7. أمثلة التكامل

### 7.1 Node.js / Express

```typescript
import express from 'express';
import crypto from 'crypto';

const app = express();

app.post('/webhooks/iafactory',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const signature = req.headers['x-iafactory-signature'] as string;
    const payload = req.body.toString();

    if (!verifyWebhookSignature(payload, signature, process.env.WEBHOOK_SECRET!)) {
      return res.status(401).json({ error: 'توقيع غير صالح' });
    }

    const event = JSON.parse(payload);

    switch (event.type) {
      case 'credits.low':
        sendLowCreditsAlert(event.data);
        break;
      case 'payment.failed':
        handleFailedPayment(event.data);
        break;
    }

    res.status(200).json({ received: true });
  }
);
```

### 7.2 Python / FastAPI

```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import time
import json
import os

app = FastAPI()
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]

def verify_signature(payload: bytes, signature: str) -> bool:
    parts = dict(p.split("=") for p in signature.split(","))
    timestamp = parts["t"]
    expected_sig = parts["v1"]

    if time.time() - int(timestamp) > 300:
        return False

    signed_payload = f"{timestamp}.{payload.decode()}"
    computed_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_sig, expected_sig)

@app.post("/webhooks/iafactory")
async def handle_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-IAFactory-Signature")

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="توقيع غير صالح")

    event = json.loads(payload)

    if event["type"] == "credits.low":
        await send_low_credits_alert(event["data"])

    return {"received": True}
```

---

## التواصل

لأي استفسارات حول webhooks:
- التوثيق: docs.iafactory.ai/webhooks
- الدعم: api-support@iafactory.ai
- Discord: قناة #developers
