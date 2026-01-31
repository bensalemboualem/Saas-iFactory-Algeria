# IAFactory Algeria - Architecture

> Plateforme IA souveraine pour l'Algérie

---

## Informations Générales

| Paramètre | Valeur |
|-----------|--------|
| **Région** | Algérie (DZ) |
| **Devise** | DZD (Dinar Algérien) |
| **Langues** | Français, Arabe, Darija |
| **Timezone** | Africa/Algiers |
| **Domaine** | iafactoryalgeria.com |
| **Hébergement** | Algérie |

---

## Paiements

### Chargily Pay

Intégration native avec Chargily Pay pour les paiements algériens.

**Méthodes supportées:**
- CIB (Carte Interbancaire)
- Edahabia (Algérie Poste)
- BaridiMob

### Configuration

```env
PAYMENT_PROVIDER=chargily
PAYMENT_CURRENCY=DZD
CHARGILY_API_KEY=your_api_key
CHARGILY_SECRET_KEY=your_secret_key
```

---

## Stack Technique

```
Frontend:     Next.js 16 + React 19
Backend:      Node.js + tRPC
Database:     PostgreSQL
Cache:        Redis
Auth:         Better Auth / Clerk
AI:           Claude, DeepSeek, OpenAI
Search:       SearXNG
```

---

## Structure des Services

```
┌─────────────────────────────────────────┐
│              Load Balancer              │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌─────▼─────┐   ┌───▼───┐
│ Web   │   │    API    │   │ Admin │
│ App   │   │  Server   │   │ Panel │
└───┬───┘   └─────┬─────┘   └───┬───┘
    │             │             │
    └─────────────┼─────────────┘
                  │
         ┌───────▼───────┐
         │   Database    │
         │  PostgreSQL   │
         └───────────────┘
```

---

## Variables d'Environnement

```env
# Région
REGION=algeria
TIMEZONE=Africa/Algiers
DEFAULT_LOCALE=fr-FR

# Domaine
DOMAIN=iafactoryalgeria.com
API_URL=https://api.iafactoryalgeria.com
APP_URL=https://app.iafactoryalgeria.com

# Paiement
PAYMENT_PROVIDER=chargily
PAYMENT_CURRENCY=DZD

# Légal
LEGAL_FRAMEWORK=algeria
DATA_RESIDENCY=DZ
```

---

## Contact

- **Email:** contact@iafactoryalgeria.com
- **Support:** support@iafactoryalgeria.com
- **Localisation:** Alger, Algérie
