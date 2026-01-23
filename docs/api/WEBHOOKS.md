# Webhooks API Documentation

**IAFACTORY - Documentation des Webhooks**

*Dernière mise à jour : 19 janvier 2026*

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Configuration](#2-configuration)
3. [Événements disponibles](#3-événements-disponibles)
4. [Format des payloads](#4-format-des-payloads)
5. [Sécurité](#5-sécurité)
6. [Gestion des erreurs](#6-gestion-des-erreurs)
7. [Exemples d'intégration](#7-exemples-dintégration)

---

## 1. Introduction

Les webhooks IAFACTORY permettent à votre application de recevoir des notifications en temps réel lorsque des événements se produisent sur votre compte.

### Cas d'usage

- Synchroniser les données utilisateur avec votre CRM
- Déclencher des actions après la génération de contenu
- Monitorer l'utilisation des crédits
- Automatiser la facturation

---

## 2. Configuration

### 2.1 Via le Dashboard

1. Connectez-vous à [app.iafactory.ai](https://app.iafactory.ai)
2. Allez dans **Paramètres** > **Développeurs** > **Webhooks**
3. Cliquez sur **Ajouter un endpoint**
4. Entrez l'URL de votre endpoint
5. Sélectionnez les événements à écouter
6. Copiez le **signing secret** généré

### 2.2 Via l'API

```bash
POST /api/v1/webhooks/endpoints
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/iafactory",
  "events": ["conversation.created", "credits.low"],
  "description": "Production webhook"
}
```

**Réponse :**

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

## 3. Événements disponibles

### 3.1 Conversations

| Événement | Description |
|-----------|-------------|
| `conversation.created` | Nouvelle conversation créée |
| `conversation.updated` | Conversation modifiée (titre, etc.) |
| `conversation.deleted` | Conversation supprimée |
| `message.created` | Nouveau message (user ou assistant) |

### 3.2 Génération

| Événement | Description |
|-----------|-------------|
| `generation.started` | Génération IA démarrée |
| `generation.completed` | Génération IA terminée avec succès |
| `generation.failed` | Échec de la génération |
| `image.generated` | Image générée (DALL-E, etc.) |

### 3.3 Crédits

| Événement | Description |
|-----------|-------------|
| `credits.consumed` | Crédits consommés |
| `credits.low` | Seuil bas atteint (< 10% restant) |
| `credits.depleted` | Crédits épuisés |
| `credits.reset` | Crédits mensuels réinitialisés |

### 3.4 Abonnement

| Événement | Description |
|-----------|-------------|
| `subscription.created` | Nouvel abonnement |
| `subscription.updated` | Plan modifié |
| `subscription.canceled` | Abonnement annulé |
| `subscription.renewed` | Abonnement renouvelé |
| `payment.succeeded` | Paiement réussi |
| `payment.failed` | Échec de paiement |

### 3.5 Utilisateur

| Événement | Description |
|-----------|-------------|
| `user.created` | Compte créé |
| `user.updated` | Profil mis à jour |
| `user.deleted` | Compte supprimé |

### 3.6 Agents & Workflows

| Événement | Description |
|-----------|-------------|
| `agent.run.started` | Exécution d'agent démarrée |
| `agent.run.completed` | Exécution d'agent terminée |
| `agent.run.failed` | Échec d'exécution d'agent |
| `workflow.triggered` | Workflow déclenché |
| `workflow.completed` | Workflow terminé |

---

## 4. Format des payloads

### 4.1 Structure générale

Tous les webhooks suivent cette structure :

```json
{
  "id": "evt_abc123",
  "type": "conversation.created",
  "created_at": "2026-01-19T10:30:00Z",
  "data": {
    // Données spécifiques à l'événement
  },
  "metadata": {
    "user_id": "usr_xyz",
    "account_id": "acc_123"
  }
}
```

### 4.2 Exemples par type

#### conversation.created

```json
{
  "id": "evt_conv_001",
  "type": "conversation.created",
  "created_at": "2026-01-19T10:30:00Z",
  "data": {
    "conversation": {
      "id": "conv_abc123",
      "title": "New conversation",
      "model": "gpt-4",
      "created_at": "2026-01-19T10:30:00Z"
    }
  },
  "metadata": {
    "user_id": "usr_xyz"
  }
}
```

#### message.created

```json
{
  "id": "evt_msg_001",
  "type": "message.created",
  "created_at": "2026-01-19T10:31:00Z",
  "data": {
    "message": {
      "id": "msg_def456",
      "conversation_id": "conv_abc123",
      "role": "assistant",
      "content": "Hello! How can I help you today?",
      "model": "gpt-4",
      "tokens": {
        "input": 15,
        "output": 12
      },
      "credits_consumed": 2
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

#### payment.succeeded

```json
{
  "id": "evt_pay_001",
  "type": "payment.succeeded",
  "created_at": "2026-01-19T10:35:00Z",
  "data": {
    "payment": {
      "id": "pay_ghi789",
      "amount": 2500,
      "currency": "DZD",
      "description": "Pro subscription - January 2026",
      "invoice_url": "https://api.iafactory.ai/invoices/inv_123.pdf"
    },
    "subscription": {
      "id": "sub_jkl012",
      "plan": "pro",
      "period_start": "2026-01-19",
      "period_end": "2026-02-19"
    }
  },
  "metadata": {
    "user_id": "usr_xyz"
  }
}
```

---

## 5. Sécurité

### 5.1 Vérification de signature

Chaque requête webhook inclut un header `X-IAFactory-Signature` contenant une signature HMAC-SHA256.

**Header format :**
```
X-IAFactory-Signature: t=1705661400,v1=5257a869e7...
```

### 5.2 Implémentation de la vérification

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const [timestamp, hash] = signature.split(',').map(part => {
    const [key, value] = part.split('=');
    return { key, value };
  });

  const t = timestamp.value;
  const v1 = hash.value;

  // Verify timestamp (reject if > 5 minutes old)
  const now = Math.floor(Date.now() / 1000);
  if (now - parseInt(t) > 300) {
    return false;
  }

  // Compute expected signature
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

### 5.3 Bonnes pratiques

1. **Toujours vérifier la signature** avant de traiter le webhook
2. **Vérifier le timestamp** pour éviter les attaques par rejeu
3. **Utiliser HTTPS** pour votre endpoint
4. **Limiter les IPs** si possible (voir section ci-dessous)

### 5.4 IPs source

Les webhooks sont envoyés depuis ces plages d'IP :

```
Production:
- 51.159.XXX.0/24
- 62.210.XXX.0/24

Sandbox:
- 212.129.XXX.0/24
```

---

## 6. Gestion des erreurs

### 6.1 Politique de retry

| Tentative | Délai |
|-----------|-------|
| 1 | Immédiat |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 heures |
| 6 | 6 heures |
| 7 | 24 heures |

Après 7 échecs, le webhook est marqué comme **failed** et une notification est envoyée.

### 6.2 Codes de réponse attendus

| Code | Interprétation |
|------|----------------|
| 2xx | Succès, pas de retry |
| 3xx | Suivre la redirection |
| 4xx | Échec permanent, pas de retry (sauf 429) |
| 429 | Rate limit, retry avec backoff |
| 5xx | Retry selon la politique |

### 6.3 Timeout

- **Timeout de connexion** : 10 secondes
- **Timeout de réponse** : 30 secondes

Votre endpoint doit répondre dans ce délai. Pour les traitements longs, renvoyez `202 Accepted` et traitez en asynchrone.

### 6.4 Idempotence

Utilisez l'`id` de l'événement pour assurer l'idempotence :

```typescript
async function handleWebhook(event: WebhookEvent) {
  // Check if already processed
  const existing = await db.processedEvents.findUnique({
    where: { eventId: event.id }
  });

  if (existing) {
    return { status: 'already_processed' };
  }

  // Process the event
  await processEvent(event);

  // Mark as processed
  await db.processedEvents.create({
    data: { eventId: event.id, processedAt: new Date() }
  });

  return { status: 'processed' };
}
```

---

## 7. Exemples d'intégration

### 7.1 Node.js / Express

```typescript
import express from 'express';
import crypto from 'crypto';

const app = express();

// Use raw body for signature verification
app.post('/webhooks/iafactory',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const signature = req.headers['x-iafactory-signature'] as string;
    const payload = req.body.toString();

    if (!verifyWebhookSignature(payload, signature, process.env.WEBHOOK_SECRET!)) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const event = JSON.parse(payload);

    switch (event.type) {
      case 'credits.low':
        // Send email alert
        sendLowCreditsAlert(event.data);
        break;
      case 'payment.failed':
        // Update user status
        handleFailedPayment(event.data);
        break;
      // ... handle other events
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

app = FastAPI()
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]

def verify_signature(payload: bytes, signature: str) -> bool:
    parts = dict(p.split("=") for p in signature.split(","))
    timestamp = parts["t"]
    expected_sig = parts["v1"]

    # Check timestamp
    if time.time() - int(timestamp) > 300:
        return False

    # Compute signature
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
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = json.loads(payload)

    if event["type"] == "credits.low":
        await send_low_credits_alert(event["data"])
    elif event["type"] == "payment.failed":
        await handle_failed_payment(event["data"])

    return {"received": True}
```

### 7.3 PHP / Laravel

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class WebhookController extends Controller
{
    public function handle(Request $request)
    {
        $signature = $request->header('X-IAFactory-Signature');
        $payload = $request->getContent();

        if (!$this->verifySignature($payload, $signature)) {
            return response()->json(['error' => 'Invalid signature'], 401);
        }

        $event = json_decode($payload, true);

        match($event['type']) {
            'credits.low' => $this->handleLowCredits($event['data']),
            'payment.failed' => $this->handleFailedPayment($event['data']),
            default => null,
        };

        return response()->json(['received' => true]);
    }

    private function verifySignature(string $payload, string $signature): bool
    {
        $parts = [];
        foreach (explode(',', $signature) as $part) {
            [$key, $value] = explode('=', $part, 2);
            $parts[$key] = $value;
        }

        $timestamp = $parts['t'];
        $expectedSig = $parts['v1'];

        if (time() - (int)$timestamp > 300) {
            return false;
        }

        $signedPayload = "{$timestamp}.{$payload}";
        $computedSig = hash_hmac('sha256', $signedPayload, env('WEBHOOK_SECRET'));

        return hash_equals($computedSig, $expectedSig);
    }
}
```

---

## 8. Testing

### 8.1 Sandbox

Utilisez l'environnement sandbox pour tester :

```
Endpoint: https://sandbox.api.iafactory.ai
```

### 8.2 Envoyer un test webhook

```bash
POST /api/v1/webhooks/endpoints/{endpoint_id}/test
Authorization: Bearer YOUR_API_KEY

{
  "event_type": "credits.low"
}
```

### 8.3 Logs des webhooks

Consultez l'historique des webhooks dans le dashboard :

**Paramètres** > **Développeurs** > **Webhooks** > **Logs**

Chaque log inclut :
- Timestamp
- Événement
- Payload envoyé
- Réponse reçue
- Temps de réponse
- Statut (success/failed/retrying)

---

## Contact

Pour toute question sur les webhooks :
- Documentation : docs.iafactory.ai/webhooks
- Support : api-support@iafactory.ai
- Discord : canal #developers
