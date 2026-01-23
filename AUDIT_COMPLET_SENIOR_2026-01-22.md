# AUDIT COMPLET IAFACTORY SAAS
## Date: 2026-01-22 | Auditeur: Claude Opus 4.5 (Senior Full-Stack + Security + Architecture)

---

# EXECUTIVE SUMMARY

| Catégorie | Score | Status |
|-----------|-------|--------|
| **Sécurité** | 3/10 | CRITIQUE |
| **Logique Métier** | 4/10 | CRITIQUE |
| **Infrastructure** | 6/10 | MOYEN |
| **DX/Ops** | 5/10 | MOYEN |
| **Production-Ready** | NO | BLOQUANT |

**Verdict Global**: Le SaaS n'est PAS prêt pour la production. Des failles critiques dans la gestion des crédits, des secrets exposés dans le repository, et des systèmes de paiement non-fonctionnels bloquent le lancement.

---

# A. INVENTAIRE MONOREPO

## Applications (apps/)

| App | Framework | Port | Rôle | Status |
|-----|-----------|------|------|--------|
| **LobeChat (root)** | Next.js 16, React 19 | 3010 | Frontend principal AI chat | OK |
| **gateway** | Fastify | 3001 | API Gateway, credits, auth | PARTIEL |
| **api** | Hono | 3002 | API microservice | CRITIQUE (CORS wildcard) |
| **bolt-ui** | Remix, React 19 | 5173 | UI no-code builder | OK |
| **web** | Next.js 15, React 19 | 3000 | Landing + auth | OK |
| **landing** | Next.js | 3003 | Page marketing | OK |
| **desktop** | Electron | - | App desktop | OK |
| **dzir-ia** | Hono + React | 8000/5173 | Backend/Frontend IA | OK |
| **b2b/video-studio** | FastAPI + Next.js | 8200/3004 | Studio vidéo IA | OK |
| **b2b/school** | Laravel 11 | 8080 | LMS (PHP) | SÉPARÉ |
| **iafactory-core** | Python | 8501-8503 | Agents IA (Streamlit) | OK |

## Packages (packages/)

| Package | Rôle | Status |
|---------|------|--------|
| **database** | Drizzle ORM, migrations | OK |
| **credits-system** | Gestion crédits | **MOCK** (non-fonctionnel) |
| **chargily-pay** | Paiements Algérie | **STUB** (non-fonctionnel) |
| **tools-registry** | Registry outils IA | OK |
| **ai-engine** | Moteur IA | OK |
| **utils** | Utilitaires | OK |

---

# B. FLUX E2E: ATTENDU VS OBSERVÉ

## Workflow Attendu

```
Landing → SignUp → Verify Email → Login → Dashboard
    ↓
Buy Credits → Chargily Payment → Webhook → Credits Added
    ↓
Use Chat → Gateway Auth → Credit Check → AI Provider → Credit Debit
    ↓
Premium Features → Subscription Check → Access Granted
```

## Workflow Observé (Réalité)

```
Landing → SignUp → Verify Email → Login → Dashboard  ✅
    ↓
Buy Credits → Chargily STUB → ❌ BLOQUÉ (retourne URL test hardcodée)
    ↓
Use Chat → Gateway Auth ✅ → Credit Check ✅ → AI Provider ✅ → Credit Debit ⚠️ RACE CONDITION
    ↓
Premium Features → ❌ PAS DE VÉRIFICATION (publicProcedure partout)
```

| Étape | Attendu | Observé | Gap |
|-------|---------|---------|-----|
| **Inscription** | Email + password | OK | - |
| **SSO OAuth** | Google, GitHub, etc. | OK (better-auth) | - |
| **Achat crédits** | Chargily checkout | STUB hardcodé | BLOQUANT |
| **Webhook paiement** | Crédits attribués | Code existe mais jamais appelé | BLOQUANT |
| **Check crédits avant AI** | Vérif atomique | Race condition possible | CRITIQUE |
| **Débit crédits streaming** | Après réponse | APRÈS envoi données | CRITIQUE |
| **Gating premium** | Vérif subscription | publicProcedure | CRITIQUE |
| **Marketplace payant** | Licence vérifiée | Aucune vérification | CRITIQUE |

---

# C. AUDIT SÉCURITÉ DÉTAILLÉ

## C.1 Secrets Exposés (CRITIQUE)

| Fichier | Secret | Statut |
|---------|--------|--------|
| `apps/gateway/.env:37` | Groq API Key `gsk_7kbT...` | **ACTIF - RÉVOQUER** |
| `apps/gateway/.env:40` | OpenRouter API Key `sk-or-v1-...` | **ACTIF - RÉVOQUER** |
| `apps/gateway/.env:43` | DeepSeek API Key `sk-1448...` | **ACTIF - RÉVOQUER** |
| `apps/gateway/.env:46` | OpenAI API Key `sk-proj-...` | **ACTIF - RÉVOQUER** |
| `orchestrators/meta/.env:1` | Google Gemini API Key | **ACTIF - RÉVOQUER** |
| `.github/workflows/*.yml` | KEY_VAULTS_SECRET hardcodé | **EXPOSÉ** |
| `.env.docker` | `POSTGRES_PASSWORD=iafactory2026` | **FAIBLE** |

## C.2 CORS Vulnérabilités

| Fichier | Config | Risque |
|---------|--------|--------|
| `apps/api/src/index.ts:8` | `cors()` sans config | CRITIQUE - Wildcard |
| `apps/bolt-ui/app/routes/api.git-proxy.*.ts` | `Access-Control-Allow-Origin: *` | CRITIQUE |
| `apps/bolt-ui/app/routes/api.system.git-info.ts` | `*` sur 9 endpoints | CRITIQUE |
| `apps/gateway/src/server.ts:32-37` | Whitelist en prod | OK |
| `apps/dzir-ia/backend/src/app.ts:31-39` | Whitelist définie | OK |

## C.3 Cookies Sans Protection

| Fichier | Cookie | Issue |
|---------|--------|-------|
| `src/layout/AuthProvider/MarketAuth/MarketAuthProvider.tsx:48` | `market-bearertoken` | Pas httpOnly - XSS vuln |
| `packages/utils/src/client/cookie.ts` | `setCookie()` | Aucun flag sécurité |

## C.4 Authentication Bypass

| Fichier | Endpoint | Issue |
|---------|----------|-------|
| `src/server/routers/lambda/plugin.ts:69` | `getPlugins` | publicProcedure |
| `src/server/routers/lambda/message.ts:68` | `getMessages` | publicProcedure |
| `src/server/routers/lambda/topic.ts:95` | `getTopics` | publicProcedure |

---

# D. AUDIT LOGIQUE MÉTIER

## D.1 Système de Crédits

### Gateway (apps/gateway/src/core/credits.ts) - IMPLÉMENTÉ mais VULNÉRABLE

```
Vulnérabilité 1: TOCTOU (Time-of-Check-Time-of-Use)
├── Line 37: Check balance (stale data)
├── [Gap: autre requête peut modifier]
└── Line 43: Update balance (race condition)

Vulnérabilité 2: Streaming Bypass
├── Line 54: Données envoyées au client
├── Line 62: Débit APRÈS envoi
└── Si déconnexion → service gratuit

Vulnérabilité 3: Release No-Op
├── Line 63-65: case 'release': return true;
└── Crédits réservés jamais libérés
```

### packages/credits-system - NON-FONCTIONNEL

```typescript
// packages/credits-system/src/index.ts
export const creditsSystem = {
    async check(userId, required): Promise<boolean> {
        return true; // TOUJOURS VRAI - MOCK
    },
    async deduct(userId, amount, toolId): Promise<void> {
        // TODO: Phase 2 - NON IMPLÉMENTÉ
    }
};
```

## D.2 Système de Paiement (Chargily)

### packages/chargily-pay - STUB INUTILISABLE

```typescript
// packages/chargily-pay/src/index.ts (10 lignes total)
export class ChargilyClient {
    constructor() { console.log("Chargily Client Initialized"); }
    async createPayment() {
        return { checkout_url: "https://chargily.com/test/checkout" }; // HARDCODÉ
    }
}
```

### apps/web/app/api/payments/webhook/route.ts - CODE EXISTE MAIS JAMAIS APPELÉ

- Signature HMAC-SHA256 implémentée (OK)
- Crédit allocation atomique (OK)
- **MAIS**: Chargily stub ne génère jamais de vrais webhooks

### Gaps Critiques Paiement

| Fonctionnalité | Status | Impact |
|----------------|--------|--------|
| Création checkout | STUB | Aucun paiement réel |
| Webhook validation | OK (code) | Jamais appelé |
| Idempotency | MANQUANT | Double crédit possible |
| Refund handling | MANQUANT | Pas de remboursement |
| Env variable mismatch | `CHARGILY_SECRET_KEY` vs `CHARGILY_SECRET` | Webhook cassé |

## D.3 Gating Marketplace/Premium

| Vérification | Status | Code |
|--------------|--------|------|
| Subscription tier check | ABSENT | Aucun code |
| License validation | ABSENT | Aucun code |
| Plugin purchase verify | ABSENT | Aucun code |
| Cloud MCP auth | Token only | Pas de subscription check |

---

# E. AUDIT INFRASTRUCTURE (DX/Ops)

## E.1 Docker

### Bonnes Pratiques (Production)

- `Dockerfile`: Multi-stage, non-root user (nextjs:1001)
- `docker-compose.algeria.prod.yml`: Bind 127.0.0.1, health checks, rate limiting

### Problèmes (Développement)

| Fichier | Issue | Risque |
|---------|-------|--------|
| `docker-compose.algeria.yml` | PostgreSQL port 5432 PUBLIC | CRITIQUE |
| `docker-compose.algeria.yml` | Redis port 6379 PUBLIC | CRITIQUE |
| `docker-compose.algeria.yml` | Adminer port 8080 PUBLIC | CRITIQUE |
| `docker-compose.switzerland.yml` | Mêmes problèmes | CRITIQUE |
| Plusieurs | `MEILI_MASTER_KEY: masterKey123` | PRÉVISIBLE |

## E.2 Migrations

### Drizzle (packages/database/migrations)
- 68 migrations
- Migrations destructives: `0009`, `0010` (DROP sans IF EXISTS)
- Pas de rollback documenté

### Prisma (apps/gateway, apps/web)
- Utilise `db push` (pas d'historique)
- 2 schémas SQLite + 1 PostgreSQL
- Inconsistance: `@db.Text` manquant dans web

## E.3 Variables d'Environnement

| Issue | Fichiers | Impact |
|-------|----------|--------|
| API Keys commités | `apps/gateway/.env`, `orchestrators/meta/.env` | CRITIQUE |
| Naming inconsistent | `AUTH_SECRET` vs `JWT_SECRET` vs `KEY_VAULTS_SECRET` | Confusion |
| Defaults faibles | `masterKey123`, `iafactory2026` | Sécurité |
| Missing validation | IP lists, URLs | Runtime errors |

---

# F. PLAN DE REMISE EN CONFORMITÉ

## Phase 1: URGENCE (24-48h)

### 1.1 Secrets (IMMÉDIAT)

```bash
# 1. Révoquer tous les API keys exposés
# Groq, OpenRouter, DeepSeek, OpenAI, Google Gemini

# 2. Mettre à jour .gitignore
echo ".env" >> .gitignore
echo ".env.*.local" >> .gitignore
echo "*.pem" >> .gitignore

# 3. Nettoyer l'historique git
git-filter-repo --invert-paths --path 'apps/gateway/.env' --force
git-filter-repo --invert-paths --path 'orchestrators/meta/.env' --force

# 4. Générer nouveaux secrets
openssl rand -base64 32  # Pour KEY_VAULTS_SECRET
openssl rand -base64 64  # Pour JWT_SECRET
```

### 1.2 CORS (IMMÉDIAT)

```typescript
// apps/api/src/index.ts - AVANT
app.use('/*', cors());

// apps/api/src/index.ts - APRÈS
app.use('/*', cors({
  origin: process.env.NODE_ENV === 'production'
    ? ['https://iafactory.dz', 'https://chat.iafactory.dz']
    : ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true,
}));
```

### 1.3 Cookie httpOnly (IMMÉDIAT)

```typescript
// src/layout/AuthProvider/MarketAuth/MarketAuthProvider.tsx
// AVANT (ligne 48)
document.cookie = `market-bearertoken=${token}; ...`;

// APRÈS: Utiliser Set-Cookie header côté serveur uniquement
```

## Phase 2: CRITIQUE (1-2 semaines)

### 2.1 Fix Credit System Race Condition

```typescript
// apps/gateway/src/core/credits.ts
// Utiliser transaction avec verrouillage pessimiste

case 'debit':
  // AVANT: Check puis update séparés

  // APRÈS: Transaction atomique avec lock
  await prisma.$transaction(async (tx) => {
    const wallet = await tx.creditWallet.findUnique({
      where: { userId },
      // SELECT FOR UPDATE implicite via Prisma interactive transaction
    });

    if (!wallet || wallet.balance < actualCost) {
      throw new GatewayError('INSUFFICIENT_CREDITS');
    }

    await tx.creditWallet.update({
      where: { id: wallet.id },
      data: { balance: { decrement: actualCost } },
    });

    await tx.usageLedger.create({ ... });
  });
```

### 2.2 Fix Streaming Bypass

```typescript
// apps/gateway/src/api/v1/chatCompletions.ts
// OPTION A: Buffer avant envoi
// OPTION B: Débit AVANT streaming (estimation)
// OPTION C: Connection lifecycle hooks

// Solution recommandée: Débit estimé + ajustement
const estimatedTokens = estimateTokens(body.messages);
await checkAndDebitCredits(user.id, body.model, 'debit', estimatedTokens);

// Après streaming: ajuster si différence significative
const actualTokens = totalTokens;
if (Math.abs(actualTokens - estimatedTokens) > 100) {
  await adjustCredits(user.id, actualTokens - estimatedTokens);
}
```

### 2.3 Implémenter Chargily Réel

```typescript
// packages/chargily-pay/src/index.ts - NOUVEAU
import Chargily from 'chargily-epay-js';

export class ChargilyClient {
  private client: Chargily;

  constructor(config: ChargilyConfig) {
    this.client = new Chargily(config.apiKey, config.apiSecret);
    this.mode = config.mode || 'test';
  }

  async createCheckout(options: CheckoutOptions): Promise<CheckoutResponse> {
    const baseUrl = this.mode === 'live'
      ? 'https://pay.chargily.net/api/v2'
      : 'https://pay.chargily.net/test/api/v2';

    const response = await fetch(`${baseUrl}/checkouts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    });

    return response.json();
  }
}
```

### 2.4 Fix Variable Mismatch

```bash
# .env.staging.example - CORRECTION
# AVANT: CHARGILY_SECRET_KEY
# APRÈS: CHARGILY_SECRET (match webhook code)
```

## Phase 3: IMPORTANT (2-4 semaines)

### 3.1 Ajouter authedProcedure

```typescript
// src/server/routers/lambda/plugin.ts
// AVANT
getPlugins: publicProcedure.query(...)

// APRÈS
getPlugins: authedProcedure.query(...)

// Faire de même pour:
// - message.ts:68 getMessages
// - topic.ts:95 getTopics
```

### 3.2 Implémenter Subscription Gating

```typescript
// src/server/middleware/subscription.ts - NOUVEAU
export const premiumProcedure = authedProcedure.use(async ({ ctx, next }) => {
  const user = await ctx.userModel.getUser();

  if (!user.subscriptionPlan || user.subscriptionPlan === 'free') {
    throw new TRPCError({
      code: 'FORBIDDEN',
      message: 'Premium subscription required',
    });
  }

  return next({ ctx });
});
```

### 3.3 Docker Security Hardening

```yaml
# docker-compose.algeria.yml - CORRECTIONS
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"  # Bind localhost only

  redis:
    ports:
      - "127.0.0.1:6379:6379"  # Bind localhost only
    command: redis-server --requirepass ${REDIS_PASSWORD}

  adminer:
    # SUPPRIMER de dev ou ajouter auth
    profiles: ["admin"]  # Opt-in only
```

### 3.4 Webhook Idempotency

```typescript
// apps/web/app/api/payments/webhook/route.ts
// Ajouter vérification idempotence

const existingTransaction = await prisma.transaction.findUnique({
  where: { chargilyId: event.data.id }
});

if (existingTransaction?.status === 'paid') {
  // Déjà traité - ignorer
  return NextResponse.json({ received: true, status: 'already_processed' });
}
```

## Phase 4: AMÉLIORATION (1-2 mois)

### 4.1 Secrets Manager

```typescript
// src/config/secrets.ts - NOUVEAU
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

export async function getSecret(name: string): Promise<string> {
  if (process.env.NODE_ENV === 'development') {
    return process.env[name] || '';
  }

  const client = new SecretsManager({ region: process.env.AWS_REGION });
  const response = await client.getSecretValue({ SecretId: name });
  return response.SecretString || '';
}
```

### 4.2 Rate Limiting Per-User

```typescript
// apps/gateway/src/server.ts
await server.register(rateLimit, {
  max: appConfig.RATE_LIMIT_MAX_REQUESTS || 100,
  timeWindow: appConfig.RATE_LIMIT_WINDOW_MS || 60000,
  keyGenerator: (request) => {
    // Rate limit par user, pas global
    return (request as any).user?.id || request.ip;
  },
});
```

### 4.3 Audit Logging

```typescript
// src/lib/audit.ts - NOUVEAU
export async function auditLog(event: AuditEvent) {
  await prisma.auditLog.create({
    data: {
      userId: event.userId,
      action: event.action,
      resource: event.resource,
      details: event.details,
      ip: event.ip,
      userAgent: event.userAgent,
      timestamp: new Date(),
    },
  });
}
```

---

# G. CHECKLIST PRE-PRODUCTION

## Sécurité

- [ ] Tous les API keys révoqués et renouvelés
- [ ] .gitignore mis à jour
- [ ] Historique git nettoyé
- [ ] CORS configuré avec whitelist
- [ ] Cookies avec httpOnly/secure/sameSite
- [ ] CSP headers activés (`ENABLED_CSP=1`)

## Logique Métier

- [ ] Race condition crédits corrigée
- [ ] Streaming bypass corrigé
- [ ] Chargily implémenté (pas stub)
- [ ] Webhook idempotent
- [ ] Subscription gating actif
- [ ] authedProcedure sur tous endpoints privés

## Infrastructure

- [ ] Bases de données bind 127.0.0.1
- [ ] Redis avec password obligatoire
- [ ] Adminer supprimé ou protégé
- [ ] Migrations avec IF EXISTS
- [ ] Health checks sur tous services
- [ ] Rate limiting per-user

## Ops

- [ ] Secrets manager configuré
- [ ] Backup strategy documentée
- [ ] Monitoring/alerting actif
- [ ] Logs centralisés
- [ ] Disaster recovery testé

---

# H. CONCLUSION

Le SaaS IAFactory présente une architecture ambitieuse avec un monorepo bien organisé et des choix technologiques solides (Next.js, Fastify, Prisma, better-auth). Cependant, l'audit révèle des failles critiques qui empêchent tout déploiement en production:

1. **Sécurité**: Secrets exposés dans git, CORS wildcard, cookies sans protection
2. **Business Logic**: Système de crédits vulnérable, paiement non-fonctionnel, gating absent
3. **Infrastructure**: Services exposés publiquement en dev, migrations risquées

**Recommandation**: Arrêter tout développement de nouvelles features et allouer 100% des ressources à la remise en conformité pendant les 2-4 prochaines semaines.

---

*Audit généré par Claude Opus 4.5 - 2026-01-22*
*Ce document est confidentiel et destiné à l'équipe IAFactory uniquement.*
