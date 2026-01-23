# Billing & Pricing Documentation

**IAFACTORY - Billing and Pricing System**

*Last updated: January 19, 2026*

---

## Table of Contents

1. [Overview](#1-overview)
2. [Plans and Pricing](#2-plans-and-pricing)
3. [Credits System](#3-credits-system)
4. [Payment Methods](#4-payment-methods)
5. [Billing Cycle](#5-billing-cycle)
6. [Subscription Management](#6-subscription-management)
7. [Technical Integration](#7-technical-integration)

---

## 1. Overview

### Billing System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    IAFACTORY Billing System                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Chargily   │    │    Stripe    │    │   Credits    │  │
│  │  (Algeria)   │    │ (Internat.)  │    │   System     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │          │
│         └───────────────────┼───────────────────┘          │
│                             ▼                               │
│                    ┌──────────────┐                         │
│                    │  Billing DB  │                         │
│                    │  (Postgres)  │                         │
│                    └──────────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Related Packages

- `packages/credits-system/` - Credits management
- `packages/chargily-pay/` - Chargily integration (Algeria)
- `src/services/billing/` - Billing services

---

## 2. Plans and Pricing

### Available Plans

| Plan | Price DZD | Price USD | Credits/month | Features |
|------|-----------|-----------|---------------|----------|
| **Free** | 0 | $0 | 100 | Basic AI chat |
| **Pro** | 2,500 | $9.99 | 10,000 | + All models |
| **Pro+** | 5,000 | $19.99 | 50,000 | + Agents, API |
| **Enterprise** | Custom | Custom | Unlimited | + Dedicated support |

### Features by Plan

```typescript
// types/subscription.ts
export interface PlanFeatures {
  id: 'free' | 'pro' | 'pro_plus' | 'enterprise';
  name: string;
  credits: number;
  features: {
    models: string[];
    maxFileSize: number; // MB
    maxConversations: number;
    apiAccess: boolean;
    agentsAccess: boolean;
    workflowsAccess: boolean;
    prioritySupport: boolean;
    customBranding: boolean;
    sso: boolean;
  };
}

export const PLANS: Record<string, PlanFeatures> = {
  free: {
    id: 'free',
    name: 'Free',
    credits: 100,
    features: {
      models: ['gpt-3.5-turbo', 'claude-instant'],
      maxFileSize: 5,
      maxConversations: 10,
      apiAccess: false,
      agentsAccess: false,
      workflowsAccess: false,
      prioritySupport: false,
      customBranding: false,
      sso: false,
    },
  },
  pro: {
    id: 'pro',
    name: 'Pro',
    credits: 10000,
    features: {
      models: ['gpt-4', 'gpt-4-turbo', 'claude-3-sonnet', 'gemini-pro'],
      maxFileSize: 20,
      maxConversations: -1, // unlimited
      apiAccess: true,
      agentsAccess: false,
      workflowsAccess: false,
      prioritySupport: true,
      customBranding: false,
      sso: false,
    },
  },
  pro_plus: {
    id: 'pro_plus',
    name: 'Pro+',
    credits: 50000,
    features: {
      models: ['gpt-4o', 'claude-3-opus', 'gemini-ultra', 'all'],
      maxFileSize: 100,
      maxConversations: -1,
      apiAccess: true,
      agentsAccess: true,
      workflowsAccess: true,
      prioritySupport: true,
      customBranding: false,
      sso: false,
    },
  },
  enterprise: {
    id: 'enterprise',
    name: 'Enterprise',
    credits: -1, // unlimited
    features: {
      models: ['all'],
      maxFileSize: 500,
      maxConversations: -1,
      apiAccess: true,
      agentsAccess: true,
      workflowsAccess: true,
      prioritySupport: true,
      customBranding: true,
      sso: true,
    },
  },
};
```

---

## 3. Credits System

### Credit Pricing by Model

| Model | Input (1K tokens) | Output (1K tokens) |
|-------|-------------------|-------------------|
| GPT-3.5 Turbo | 0.5 credits | 1.5 credits |
| GPT-4 | 10 credits | 30 credits |
| GPT-4 Turbo | 5 credits | 15 credits |
| GPT-4o | 3 credits | 12 credits |
| Claude 3 Haiku | 0.5 credits | 2 credits |
| Claude 3 Sonnet | 3 credits | 15 credits |
| Claude 3 Opus | 15 credits | 75 credits |
| Gemini Pro | 0.5 credits | 1.5 credits |
| DALL-E 3 | 50 credits/image | - |
| Whisper | 10 credits/min | - |

### Credit Calculation

```typescript
// services/credits/calculator.ts
export function calculateCredits(
  model: string,
  inputTokens: number,
  outputTokens: number
): number {
  const pricing = MODEL_PRICING[model];
  if (!pricing) throw new Error(`Unknown model: ${model}`);

  const inputCredits = (inputTokens / 1000) * pricing.inputRate;
  const outputCredits = (outputTokens / 1000) * pricing.outputRate;

  return Math.ceil(inputCredits + outputCredits);
}
```

### Additional Credit Packs

| Pack | Credits | Price DZD | Price USD | Savings |
|------|---------|-----------|-----------|---------|
| Starter | 5,000 | 500 | $4.99 | - |
| Standard | 20,000 | 1,800 | $17.99 | 10% |
| Premium | 100,000 | 8,000 | $79.99 | 20% |
| Ultimate | 500,000 | 35,000 | $349.99 | 30% |

---

## 4. Payment Methods

### Algeria - Chargily Pay

```typescript
// packages/chargily-pay/src/index.ts
import { ChargilyClient } from '@chargily/chargily-pay';

export const chargilyClient = new ChargilyClient({
  apiKey: process.env.CHARGILY_API_KEY!,
  mode: process.env.NODE_ENV === 'production' ? 'live' : 'test',
});

export async function createChargilyCheckout(params: {
  amount: number;
  userId: string;
  planId: string;
}) {
  return chargilyClient.createCheckout({
    amount: params.amount,
    currency: 'DZD',
    success_url: `${process.env.APP_URL}/billing/success`,
    failure_url: `${process.env.APP_URL}/billing/failed`,
    webhook_endpoint: `${process.env.API_URL}/webhooks/chargily`,
    metadata: {
      userId: params.userId,
      planId: params.planId,
    },
  });
}
```

### International - Stripe

```typescript
// services/billing/stripe.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function createStripeCheckout(params: {
  priceId: string;
  userId: string;
  email: string;
}) {
  return stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    customer_email: params.email,
    line_items: [{ price: params.priceId, quantity: 1 }],
    success_url: `${process.env.APP_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.APP_URL}/billing/canceled`,
    metadata: { userId: params.userId },
  });
}
```

---

## 5. Billing Cycle

### Billing Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│  Checkout   │────▶│  Payment    │
│  selects    │     │   Session   │     │  Provider   │
│   plan      │     │  created    │     │  (Stripe/   │
└─────────────┘     └─────────────┘     │  Chargily)  │
                                        └──────┬──────┘
                                               │
                    ┌─────────────┐            │
                    │  Webhook    │◀───────────┘
                    │  received   │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Update     │     │   Grant     │     │   Send      │
│  user plan  │     │  credits    │     │  invoice    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Automatic Renewal

```typescript
// jobs/billing/renewal.ts
export async function processRenewal(subscriptionId: string) {
  const subscription = await db.subscription.findUnique({
    where: { id: subscriptionId },
    include: { user: true },
  });

  if (!subscription) return;

  // Check if billing is due
  if (subscription.currentPeriodEnd > new Date()) return;

  try {
    // Attempt to charge
    await chargeSubscription(subscription);

    // Reset credits
    await db.user.update({
      where: { id: subscription.userId },
      data: {
        credits: PLANS[subscription.planId].credits,
        creditsResetAt: new Date(),
      },
    });

    // Update period
    await db.subscription.update({
      where: { id: subscriptionId },
      data: {
        currentPeriodStart: new Date(),
        currentPeriodEnd: addMonths(new Date(), 1),
      },
    });
  } catch (error) {
    await handleFailedPayment(subscription, error);
  }
}
```

---

## 6. Subscription Management

### User Actions

| Action | Endpoint | Description |
|--------|----------|-------------|
| Upgrade | `POST /api/billing/upgrade` | Switch to higher plan |
| Downgrade | `POST /api/billing/downgrade` | Switch to lower plan |
| Cancel | `POST /api/billing/cancel` | Cancel subscription |
| Reactivate | `POST /api/billing/reactivate` | Reactivate after cancellation |

### Plan Change Policies

```typescript
// Upgrade: Prorated and applied immediately
// Downgrade: Effective at end of current period
// Cancel: Access maintained until end of period

export async function handlePlanChange(
  userId: string,
  newPlanId: string,
  currentPlanId: string
) {
  const isUpgrade = isPlanUpgrade(currentPlanId, newPlanId);

  if (isUpgrade) {
    // Calculate prorata and charge difference
    const prorataAmount = calculateProrata(currentPlanId, newPlanId);
    await chargeProrata(userId, prorataAmount);
    await activateNewPlan(userId, newPlanId);
  } else {
    // Schedule downgrade for end of period
    await scheduleDowngrade(userId, newPlanId);
  }
}
```

---

## 7. Technical Integration

### Environment Variables

```env
# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_PRO=price_xxx
STRIPE_PRICE_PRO_PLUS=price_xxx

# Chargily
CHARGILY_API_KEY=xxx
CHARGILY_WEBHOOK_SECRET=xxx

# Credits
CREDITS_FREE_MONTHLY=100
CREDITS_PRO_MONTHLY=10000
CREDITS_PRO_PLUS_MONTHLY=50000
```

### Webhooks

```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Webhook signature verification failed', { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object);
      break;
    case 'invoice.paid':
      await handleInvoicePaid(event.data.object);
      break;
    case 'customer.subscription.deleted':
      await handleSubscriptionCanceled(event.data.object);
      break;
  }

  return new Response('OK');
}
```

### Database Schema

```prisma
// prisma/schema.prisma

model User {
  id              String        @id @default(cuid())
  credits         Int           @default(100)
  creditsResetAt  DateTime?
  subscription    Subscription?
  invoices        Invoice[]
  creditHistory   CreditHistory[]
}

model Subscription {
  id                 String   @id @default(cuid())
  userId             String   @unique
  user               User     @relation(fields: [userId], references: [id])
  planId             String
  status             SubscriptionStatus
  stripeSubId        String?
  chargilySubId      String?
  currentPeriodStart DateTime
  currentPeriodEnd   DateTime
  cancelAtPeriodEnd  Boolean  @default(false)
  createdAt          DateTime @default(now())
  updatedAt          DateTime @updatedAt
}

model Invoice {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  amount      Int
  currency    String
  status      InvoiceStatus
  pdfUrl      String?
  createdAt   DateTime @default(now())
}

model CreditHistory {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  amount      Int      // positive = added, negative = consumed
  reason      String
  metadata    Json?
  createdAt   DateTime @default(now())
}

enum SubscriptionStatus {
  ACTIVE
  PAST_DUE
  CANCELED
  UNPAID
}

enum InvoiceStatus {
  DRAFT
  OPEN
  PAID
  VOID
  UNCOLLECTIBLE
}
```

---

## Contact

For billing questions:
- Email: billing@iafactory.ai
- Support: support@iafactory.ai
