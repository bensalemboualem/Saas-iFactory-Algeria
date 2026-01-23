# Documentation des Webhooks API

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
  "url": "https://votre-app.com/webhooks/iafactory",
  "events": ["conversation.created", "credits.low"],
  "description": "Webhook de production"
}
```

**Réponse :**

```json
{
  "id": "we_123abc",
  "url": "https://votre-app.com/webhooks/iafactory",
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
| `message.created` | Nouveau message (utilisateur ou assistant) |

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
      "title": "Nouvelle conversation",
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

## 5. Sécurité

### 5.1 Vérification de signature

Chaque requête webhook inclut un header `X-IAFactory-Signature` contenant une signature HMAC-SHA256.

**Format du header :**
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
  const parts = signature.split(',').reduce((acc, part) => {
    const [key, value] = part.split('=');
    acc[key] = value;
    return acc;
  }, {} as Record<string, string>);

  const t = parts['t'];
  const v1 = parts['v1'];

  // Vérifier le timestamp (rejeter si > 5 minutes)
  const now = Math.floor(Date.now() / 1000);
  if (now - parseInt(t) > 300) {
    return false;
  }

  // Calculer la signature attendue
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
4. **Limiter les IPs** si possible

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

### 6.2 Codes de réponse attendus

| Code | Interprétation |
|------|----------------|
| 2xx | Succès, pas de retry |
| 4xx | Échec permanent, pas de retry |
| 429 | Rate limit, retry avec backoff |
| 5xx | Retry selon la politique |

### 6.3 Timeout

- **Timeout de connexion** : 10 secondes
- **Timeout de réponse** : 30 secondes

---

## 7. Exemples d'intégration

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
      return res.status(401).json({ error: 'Signature invalide' });
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
        raise HTTPException(status_code=401, detail="Signature invalide")

    event = json.loads(payload)

    if event["type"] == "credits.low":
        await send_low_credits_alert(event["data"])

    return {"received": True}
```

---

## Contact

Pour toute question sur les webhooks :
- Documentation : docs.iafactory.ai/webhooks
- Support : api-support@iafactory.ai
- Discord : canal #developers
