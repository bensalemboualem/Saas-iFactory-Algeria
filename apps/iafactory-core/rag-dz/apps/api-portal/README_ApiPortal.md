# iaFactory API Portal - Module 16

## 🚀 Overview

Dashboard développeur complet façon **OpenAI / Stripe** permettant aux développeurs de :

- 🔑 **Gérer leurs clés API** (création, révocation)
- 📊 **Voir les statistiques d'usage** (requêtes, erreurs, latence)
- 💰 **Suivre la consommation de crédits** (intégration Module 8 Billing)
- 📚 **Lire la documentation API** (endpoints, paramètres, exemples)
- 🧪 **Tester les endpoints** (API Playground interactif)

---

## 📁 Structure du Module

```
apps/api-portal/
├── backend/
│   ├── __init__.py              # Router principal
│   └── routers/
│       ├── dev_api_keys.py      # Gestion clés API
│       ├── dev_usage.py         # Stats & logs
│       └── dev_playground.py    # Console de test
│
├── frontend/
│   ├── src/
│   │   └── components/
│   │       ├── ApiPortalHome.tsx       # Layout principal
│   │       ├── ApiOverview.tsx         # Vue d'ensemble
│   │       ├── ApiKeysManager.tsx      # Gestion clés
│   │       ├── ApiUsageOverview.tsx    # Statistiques
│   │       ├── ApiLogsTable.tsx        # Logs récents
│   │       ├── ApiDocsPlayground.tsx   # Docs & test
│   │       └── index.ts                # Exports
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
└── README_ApiPortal.md
```

---

## 🔧 Installation

### Backend (FastAPI)

Ajouter le router dans votre app FastAPI principale :

```python
from apps.api_portal.backend import dev_portal_router

app.include_router(dev_portal_router)
```

### Frontend (React)

```bash
cd apps/api-portal/frontend
npm install
npm run dev
```

---

## 🌐 Endpoints Backend

### API Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dev/api-keys` | Liste les clés de l'utilisateur |
| POST | `/api/dev/api-keys` | Crée une nouvelle clé |
| POST | `/api/dev/api-keys/{id}/revoke` | Révoque une clé |
| GET | `/api/dev/api-keys/{id}/stats` | Stats d'une clé |

### Usage & Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dev/usage` | Stats agrégées (avec filtres) |
| GET | `/api/dev/logs` | Logs paginés (avec filtres) |
| GET | `/api/dev/credits` | Vue crédits |
| GET | `/api/dev/overview` | Dashboard rapide |

### Playground

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dev/playground/endpoints` | Liste endpoints testables |
| POST | `/api/dev/playground/execute` | Exécute une requête test |
| GET | `/api/dev/playground/docs/{name}` | Doc détaillée endpoint |

---

## 🔐 Sécurité

### Clés API

- Les clés sont générées avec 32 bytes aléatoires (`secrets.token_urlsafe`)
- Format : `IAFK_live_<random_32_chars>`
- **Seul le hash SHA-256** est stocké en base
- La clé complète n'est affichée **qu'une seule fois** à la création
- Préfixe visible : `IAFK_live_xxxx...yyyy`

### Authentification

- Toutes les routes `/api/dev/*` nécessitent une **session utilisateur valide**
- L'utilisateur ne peut voir que **ses propres** clés, logs et crédits
- Le Playground n'expose pas la clé réelle dans le frontend

### Rate Limiting

| Plan | Limite |
|------|--------|
| Free | 100 req/min |
| Pro | 500 req/min |
| Business | 1000 req/min |

---

## 🎨 Composants Frontend

### ApiPortalHome

Layout principal avec sidebar de navigation :

```tsx
import { ApiPortalHome } from '@iafactory/api-portal';

function App() {
  return <ApiPortalHome />;
}
```

### Sections

1. **Overview** - Stats rapides en 4 cards + graphiques
2. **API Keys** - Table des clés + modales création/révocation
3. **Usage** - Graphiques détaillés + table endpoints
4. **Logs** - Table paginée avec filtres
5. **Docs & Playground** - Documentation interactive

---

## 📊 Intégration Billing/Credits

Le portail affiche automatiquement :

- Crédits restants (`user_credits.current_credits`)
- Consommation du mois (`usage_events`)
- Plan actuel (Free / Pro / Business)
- Barre de progression avec alertes à 80%

Lien vers la page Billing (Module 8) :

```tsx
<a href="/billing">Voir la facturation →</a>
```

---

## 🐳 Docker

### Build

```bash
docker build -t iafactory/api-portal ./apps/api-portal/frontend
```

### docker-compose.yml

```yaml
iafactory-api-portal:
  build:
    context: ./apps/api-portal/frontend
    dockerfile: Dockerfile
  container_name: iaf-dz-api-portal
  depends_on:
    - iafactory-backend
  environment:
    VITE_API_URL: ${VITE_API_URL:-http://localhost:8180}
  ports:
    - "8219:3000"
  networks:
    - iafactory-net
  restart: unless-stopped
```

---

## 📝 Créer une Clé API

1. Aller dans **API Keys**
2. Cliquer **"+ Créer une clé"**
3. Entrer un nom descriptif (ex: "Backend Prod")
4. **COPIER LA CLÉ IMMÉDIATEMENT** ⚠️
5. La clé est prête à l'emploi

### Utilisation

```bash
curl https://api.iafactoryalgeria.com/api/v1/rag/query \
  -H "Authorization: Bearer IAFK_live_xxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "Taux TVA Algérie"}'
```

---

## 🧪 Tester avec le Playground

1. Aller dans **Docs & Playground**
2. Choisir un endpoint (RAG, Legal, Fiscal...)
3. Cliquer **"🧪 Tester"**
4. Modifier le JSON si nécessaire
5. Cliquer **"🚀 Envoyer la requête"**
6. Voir la réponse formatée

Le Playground utilise votre session - pas besoin de copier la clé !

---

## 🔗 Liens Connexes

- [Module 6 - API Publique](/docs/module-6-api.md)
- [Module 8 - Billing & Credits](/docs/module-8-billing.md)
- [Documentation API Complète](https://docs.iafactoryalgeria.com/api)

---

## 📈 Roadmap

- [ ] Export logs CSV/JSON
- [ ] Webhooks pour alertes usage
- [ ] OAuth2 / API tokens scoped
- [ ] Rate limit personnalisable
- [ ] Historique des clés révoquées

---

**iaFactory Algeria** - Module 16 API Portal
