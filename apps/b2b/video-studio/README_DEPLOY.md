# 🚀 DÉPLOIEMENT VIDEO STUDIO - GUIDE ULTRA-RAPIDE

## ✅ TOUT EST PRÊT!

Toutes vos clés API sont déjà configurées dans `.env.ready`:
- ✅ Anthropic (Claude)
- ✅ OpenAI, Groq, Gemini, Mistral
- ✅ Kling AI, Luma AI (2 comptes), Runway ML, MiniMax, Pika
- ✅ Replicate, Stability AI
- ✅ Qwen (Alibaba)
- ✅ Google Translate

**Manquant uniquement:**
- ElevenLabs (voix Darija)
- Cloudflare R2 (stockage vidéos)
- Stripe (paiements)

---

## 🎯 DÉPLOIEMENT EN 3 COMMANDES

### **1. Copier sur le VPS** (30 secondes)

**Depuis votre machine Windows:**
```powershell
# Remplacer VOTRE_IP_VPS par l'IP de votre Hetzner
scp -r D:\IAFactory\rag-dz\apps\video-studio root@VOTRE_IP_VPS:/opt/iafactory/
```

---

### **2. Installer** (3 minutes)

**Sur le VPS:**
```bash
# Se connecter
ssh root@VOTRE_IP_VPS

# Aller dans le dossier
cd /opt/iafactory/video-studio

# Rendre les scripts exécutables
chmod +x *.sh

# Installation automatique
./deploy.sh
```

**Le script va:**
- Installer Docker, FFmpeg, Nginx
- Créer le fichier .env
- Lancer les containers

---

### **3. Configurer le .env** (1 minute)

```bash
# Générer automatiquement le .env avec vos clés
./setup-env.sh
```

**Il va vous demander:**
- Clé ElevenLabs (ou skip)
- Clés Cloudflare R2 (ou skip)
- Clés Stripe (ou skip)

**Puis il génère automatiquement:**
- JWT_SECRET
- NEXTAUTH_SECRET
- Et copie toutes vos 30+ clés API!

---

## 🌐 BONUS: Nginx + SSL (5 minutes)

```bash
# Configuration automatique Nginx + certificats SSL
./setup-nginx.sh
```

**Il va demander:**
- Domaine frontend: `video-studio.iafactoryalgeria.com`
- Domaine API: `api.iafactoryalgeria.com`
- Email: `votre@email.com`

**Il va:**
- Configurer Nginx reverse proxy
- Obtenir les certificats SSL Let's Encrypt
- Activer HTTPS

**Avant de lancer, configurer vos DNS:**
```
Type A: video-studio.iafactoryalgeria.com → IP_VPS
Type A: api.iafactoryalgeria.com → IP_VPS
```

---

## ✅ VÉRIFICATION

```bash
# Lancer les tests automatiques
./test-deploy.sh
```

**Résultat attendu:**
```
✅ Docker installé
✅ Backend API répond
✅ Frontend Next.js répond
✅ PostgreSQL opérationnel
✅ Redis opérationnel
✅ Toutes les clés API configurées
```

---

## 🎉 C'EST EN LIGNE!

**Accès:**
- Frontend: https://video-studio.iafactoryalgeria.com
- API: https://api.iafactoryalgeria.com
- Docs: https://api.iafactoryalgeria.com/docs

---

## 📊 COMMANDES UTILES

```bash
# Voir l'état
cd /opt/iafactory/video-studio
docker-compose ps

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Redémarrer
docker-compose restart

# Arrêter
docker-compose down

# Rebuild
docker-compose up -d --build

# Tester l'API
curl https://api.iafactoryalgeria.com/health
curl https://api.iafactoryalgeria.com/docs
```

---

## 🗂️ FICHIERS CRÉÉS

| Fichier | Description |
|---------|-------------|
| `deploy.sh` | Script d'installation automatique (Docker, FFmpeg, Nginx) |
| `setup-env.sh` | Configuration automatique du .env avec vos clés |
| `setup-nginx.sh` | Configuration Nginx + SSL automatique |
| `test-deploy.sh` | Tests automatiques de l'installation |
| `.env.ready` | Toutes vos clés API pré-configurées |
| `QUICK_DEPLOY.md` | Guide détaillé |
| `DEPLOY_VPS.md` | Guide complet (troubleshooting) |
| `PRODUCTION_CHECKLIST.md` | Checklist complète |

---

## 🔑 CLÉS API CONFIGURÉES

### **✅ Déjà dans .env.ready:**

**LLMs (7):**
- Anthropic (Claude)
- OpenAI
- Groq
- Gemini
- Mistral
- DeepSeek
- Cohere

**Génération Vidéo (7):**
- Kling AI
- Luma AI (Algérie + Algeria)
- Runway ML
- MiniMax
- Pika Labs
- Replicate
- Stability AI (2 clés)

**Autres (4):**
- Qwen (Alibaba Cloud)
- Together AI
- Open Router
- Google Translate

### **⚠️ À ajouter (optionnel):**

**ElevenLabs (Voix Darija)** - 22€/mois
```bash
# Créer compte: https://elevenlabs.io
# Plan Creator recommandé
ELEVENLABS_API_KEY=sk_xxxxx
```

**Cloudflare R2 (Stockage)** - Gratuit jusqu'à 10GB
```bash
# Créer bucket sur Cloudflare
S3_ACCESS_KEY=xxxxx
S3_SECRET_KEY=xxxxx
S3_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com
```

**Stripe (Paiements)** - Gratuit
```bash
# Créer compte Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

---

## 💰 COÛTS MENSUELS

| Service | Coût |
|---------|------|
| VPS Hetzner (déjà payé) | 15-40€ |
| **Génération vidéo (pay-as-you-go):** | |
| - Luma AI | ~0.50€/vidéo |
| - Kling AI | ~0.30€/vidéo |
| - Runway ML | ~0.70€/vidéo |
| - MiniMax | ~0.20€/vidéo |
| **LLMs (pay-as-you-go):** | |
| - Claude (scripts) | ~5-10€ |
| - OpenAI | ~5-10€ |
| **Optionnel:** | |
| - ElevenLabs | 22€/mois |
| - Cloudflare R2 | 0€ (gratuit 10GB) |
| - Stripe | 0€ (commission 2.9%) |
| **TOTAL** | **~50-100€/mois** |

**100 vidéos/mois = ~30-50€ de coûts IA**

---

## 🎯 PROCHAINES ÉTAPES

Après déploiement:

1. **Tester la génération de vidéos**
   - Luma AI (principal)
   - Kling AI (backup)
   - MiniMax (rapide/économique)

2. **Configurer Stripe Webhooks**
   ```
   URL: https://api.iafactoryalgeria.com/webhooks/stripe
   Events: checkout.session.completed, payment_intent.succeeded
   ```

3. **Monitoring (optionnel)**
   - Sentry pour les erreurs
   - Prometheus + Grafana pour les métriques

4. **Backups automatiques**
   ```bash
   # Crontab daily backup
   0 2 * * * docker exec video-studio-db-1 pg_dump -U postgres iafactory_video > /backups/db_$(date +\%Y\%m\%d).sql
   ```

---

## ⚡ RECAP ULTRA-RAPIDE

**3 commandes pour déployer:**
```bash
# 1. Copier (Windows → VPS)
scp -r D:\IAFactory\rag-dz\apps\video-studio root@IP_VPS:/opt/iafactory/

# 2. Installer (sur VPS)
cd /opt/iafactory/video-studio && ./deploy.sh

# 3. Configurer (sur VPS)
./setup-env.sh
```

**Puis optionnel (Nginx + SSL):**
```bash
./setup-nginx.sh
```

**C'EST TOUT!** 🎉
