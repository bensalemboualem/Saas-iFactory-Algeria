# 🚀 CHECKLIST MISE EN PRODUCTION - VIDEO STUDIO PRO

## ✅ STATUT ACTUEL

| Élément | Statut | Priorité |
|---------|--------|----------|
| Frontend Next.js | ✅ Développé | P0 |
| Backend FastAPI | 🟡 À vérifier | P0 |
| Base de données | ❌ À configurer | P0 |
| Intégrations IA | 🟡 Partielles | P0 |
| Tests | ❌ À faire | P1 |
| Documentation | 🟡 Partielle | P2 |
| Landing page | ✅ Intégré | P0 |

---

## 📋 CHECKLIST DÉTAILLÉE

### 🔴 PRIORITÉ 0 - BLOQUANT (Must Have)

#### 1. Configuration Backend

- [ ] **Vérifier que le backend FastAPI existe et fonctionne**
  ```bash
  cd apps/video-studio/backend
  ls -la  # Vérifier la présence de main.py
  ```

- [ ] **Créer/Vérifier requirements.txt**
  ```bash
  # Dépendances minimales requises:
  - fastapi>=0.104.1
  - uvicorn[standard]>=0.24.0
  - sqlalchemy>=2.0.23
  - alembic>=1.12.1
  - asyncpg>=0.29.0
  - redis>=5.0.1
  - python-multipart>=0.0.6
  - pydantic>=2.5.0
  - fal-client>=0.3.0
  - replicate>=0.15.0
  - elevenlabs>=0.2.0
  ```

- [ ] **Créer les variables d'environnement de production**
  ```bash
  cp .env.example .env.production
  # Remplir avec les vraies valeurs
  ```

#### 2. Base de Données

- [ ] **Créer la base de données PostgreSQL**
  ```sql
  CREATE DATABASE iafactory_video;
  CREATE USER video_studio WITH PASSWORD 'secure_password';
  GRANT ALL PRIVILEGES ON DATABASE iafactory_video TO video_studio;
  ```

- [ ] **Créer les migrations Alembic**
  ```bash
  cd apps/video-studio/backend
  alembic init alembic
  # Créer les modèles dans models/
  # Créer la première migration
  alembic revision --autogenerate -m "Initial schema"
  alembic upgrade head
  ```

- [ ] **Schéma minimal requis:**
  - Table `users` (id, email, created_at)
  - Table `projects` (id, user_id, name, status, created_at)
  - Table `videos` (id, project_id, url, metadata, created_at)
  - Table `credits` (id, user_id, balance, updated_at)
  - Table `transactions` (id, user_id, amount, type, created_at)

#### 3. Configuration Redis

- [ ] **Installer Redis**
  ```bash
  # Docker
  docker run -d --name redis -p 6379:6379 redis:7-alpine

  # Ou via système
  sudo apt install redis-server  # Ubuntu
  brew install redis  # macOS
  ```

- [ ] **Tester la connexion**
  ```bash
  redis-cli ping  # Doit retourner PONG
  ```

#### 4. Intégrations IA - Clés API

- [ ] **Fal.ai**
  - Obtenir clé API: https://fal.ai/dashboard
  - Tester avec un appel simple
  - Budget: $50 minimum pour démarrer

- [ ] **Replicate**
  - Obtenir token: https://replicate.com/account
  - Vérifier quota
  - Budget: $50 minimum

- [ ] **ElevenLabs (Voix Darija)**
  - Créer compte: https://elevenlabs.io
  - Cloner voix darija ou utiliser voix preset
  - Tester synthèse vocale
  - Budget: $22/mois (Creator plan)

- [ ] **Stripe (Paiement)**
  - Compte Stripe actif
  - Webhooks configurés
  - Produit "IAF-Tokens" créé
  - Mode test validé

#### 5. Stockage Vidéos (Cloudflare R2 ou S3)

- [ ] **Créer bucket de stockage**
  ```bash
  # Cloudflare R2 recommandé (moins cher que S3)
  # Créer bucket: iafactory-videos
  # Configurer CORS
  ```

- [ ] **Configuration CORS**
  ```json
  [
    {
      "AllowedOrigins": ["https://video-studio.iafactory.ch"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3600
    }
  ]
  ```

- [ ] **Tester upload/download**

#### 6. Frontend - Build de Production

- [ ] **Optimiser le build Next.js**
  ```bash
  cd apps/video-studio/frontend
  npm run build
  npm run start  # Tester en local
  ```

- [ ] **Vérifier les variables d'environnement**
  ```bash
  # .env.production
  NEXT_PUBLIC_API_URL=https://api.iafactory.ch
  NEXTAUTH_URL=https://video-studio.iafactory.ch
  NEXTAUTH_SECRET=...
  ```

- [ ] **Optimiser les images**
  - Compresser les images du dossier /public
  - Utiliser next/image partout

#### 7. Docker & Déploiement

- [ ] **Créer Dockerfile pour le backend**
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

- [ ] **Créer Dockerfile pour le frontend**
  ```dockerfile
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  FROM node:20-alpine
  WORKDIR /app
  COPY --from=builder /app/.next ./.next
  COPY --from=builder /app/public ./public
  COPY --from=builder /app/package*.json ./
  RUN npm ci --production
  CMD ["npm", "start"]
  ```

- [ ] **Mettre à jour docker-compose.yml**
  ```yaml
  version: '3.8'
  services:
    frontend:
      build: ./frontend
      ports:
        - "3000:3000"
      environment:
        - NEXT_PUBLIC_API_URL=http://backend:8000

    backend:
      build: ./backend
      ports:
        - "8000:8000"
      depends_on:
        - db
        - redis
      environment:
        - DATABASE_URL=postgresql+asyncpg://...
        - REDIS_URL=redis://redis:6379

    db:
      image: postgres:16-alpine
      volumes:
        - postgres_data:/var/lib/postgresql/data
      environment:
        - POSTGRES_DB=iafactory_video
        - POSTGRES_USER=video_studio
        - POSTGRES_PASSWORD=${DB_PASSWORD}

    redis:
      image: redis:7-alpine

  volumes:
    postgres_data:
  ```

---

### 🟡 PRIORITÉ 1 - Important (Should Have)

#### 8. Tests

- [ ] **Tests backend (pytest)**
  ```bash
  cd backend
  pip install pytest pytest-asyncio httpx
  pytest tests/
  ```

- [ ] **Tests e2e frontend (Playwright)**
  ```bash
  cd frontend
  npm run test:e2e
  ```

- [ ] **Tests de charge (k6 ou locust)**

#### 9. Monitoring & Logs

- [ ] **Configurer Sentry**
  - Frontend: sentry/next
  - Backend: sentry-sdk[fastapi]

- [ ] **Configurer logs structurés**
  ```python
  # backend
  import structlog
  logger = structlog.get_logger()
  ```

- [ ] **Healthcheck endpoints**
  ```python
  @app.get("/health")
  async def health():
      return {"status": "healthy"}
  ```

#### 10. Sécurité

- [ ] **Rate limiting (Redis)**
  ```python
  from slowapi import Limiter
  limiter = Limiter(key_func=get_remote_address)
  ```

- [ ] **CORS configuré correctement**
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://video-studio.iafactory.ch"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

- [ ] **Validation des inputs (Pydantic)**

- [ ] **Authentification JWT vérifiée**

#### 11. Performance

- [ ] **Activer caching Redis**
  - Cache des résultats de génération
  - Cache des requêtes fréquentes

- [ ] **Optimiser les requêtes DB**
  - Index sur les colonnes fréquemment requêtées
  - Pagination partout

- [ ] **CDN pour les assets statiques**

---

### 🔵 PRIORITÉ 2 - Nice to Have (Could Have)

#### 12. Documentation

- [ ] **API Documentation (Swagger)**
  - Accessible sur /docs
  - Exemples de requêtes

- [ ] **Guide utilisateur**
  - How-to en FR/AR/EN
  - Tutoriels vidéo

- [ ] **Documentation développeur**
  - Architecture
  - Guide de contribution

#### 13. Analytics

- [ ] **Google Analytics / Plausible**

- [ ] **Tracking des conversions**

- [ ] **Dashboard admin**
  - Métriques d'usage
  - Revenus
  - Erreurs

#### 14. CI/CD

- [ ] **GitHub Actions**
  ```yaml
  name: Deploy
  on:
    push:
      branches: [main]
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Build & Deploy
          run: |
            docker-compose build
            docker-compose up -d
  ```

---

## 🌐 INFRASTRUCTURE PRODUCTION

### Option 1: VPS Classique (Hetzner, OVH)

**Recommandé pour démarrer:**
- **Serveur:** Hetzner CPX31 (4 vCPU, 8GB RAM) - 15€/mois
- **Stack:** Nginx reverse proxy + Docker Compose
- **Coût total:** ~20€/mois + coûts IA

**Configuration:**
```bash
# Installer Docker
curl -fsSL https://get.docker.com | sh

# Cloner le repo
git clone <repo> /opt/video-studio
cd /opt/video-studio/apps/video-studio

# Lancer
docker-compose -f docker-compose.prod.yml up -d

# Nginx config
server {
    server_name video-studio.iafactory.ch;
    location / {
        proxy_pass http://localhost:3000;
    }
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### Option 2: Cloud Native (AWS, GCP)

**Pour scale:**
- Frontend: Vercel (Next.js) - Gratuit jusqu'à 100GB bandwidth
- Backend: Cloud Run / ECS
- DB: RDS PostgreSQL ou Neon.tech
- Cache: Elasticache Redis ou Upstash
- Storage: S3 / Cloudflare R2

---

## 💰 BUDGET ESTIMÉ (par mois)

| Service | Coût | Notes |
|---------|------|-------|
| VPS (Hetzner CPX31) | 15€ | 4 vCPU, 8GB RAM |
| PostgreSQL (Neon) | 0-25€ | 0.5GB gratuit, puis $25/mo |
| Redis (Upstash) | 0€ | 10k commandes/jour gratuit |
| Cloudflare R2 | 0-10€ | 10GB gratuit/mois |
| ElevenLabs (Voix) | 22€ | Creator plan |
| Fal.ai (Vidéo) | ~50€ | Pay-as-you-go |
| Replicate | ~50€ | Pay-as-you-go |
| **TOTAL** | **150-200€/mois** | Pour démarrer |

---

## 🎯 PLAN DE LANCEMENT

### Semaine 1: Infrastructure
- [ ] Configurer VPS
- [ ] Installer Docker
- [ ] Configurer base de données
- [ ] Configurer Redis

### Semaine 2: Backend
- [ ] Finaliser API endpoints
- [ ] Tests unitaires
- [ ] Intégrations IA
- [ ] Documentation API

### Semaine 3: Frontend
- [ ] Build de production
- [ ] Tests e2e
- [ ] Optimisations
- [ ] Traductions

### Semaine 4: Beta Test
- [ ] Déployer en staging
- [ ] Inviter 10 beta testeurs
- [ ] Collecter feedback
- [ ] Corriger bugs

### Semaine 5: Production
- [ ] Déploiement production
- [ ] Monitoring actif
- [ ] Support utilisateurs
- [ ] Marketing

---

## 🚨 POINTS DE BLOCAGE POTENTIELS

1. **Coûts IA trop élevés**
   - Solution: Limiter génération gratuite à 3 vidéos/jour
   - Système de crédits IAF-Tokens

2. **Temps de génération trop long**
   - Solution: File d'attente asynchrone
   - Notifications par email

3. **Stockage vidéos**
   - Solution: Auto-delete après 30 jours
   - Upgrade storage plan si besoin

4. **Voix Darija pas assez naturelle**
   - Solution: Cloner voix native + fine-tuning
   - Budget: 200€ one-time

---

## 📞 SUPPORT

**Problèmes techniques:**
- GitHub Issues: https://github.com/iafactory/video-studio/issues
- Email: support@iafactory.ch

**Business:**
- Email: contact@iafactory.ch
