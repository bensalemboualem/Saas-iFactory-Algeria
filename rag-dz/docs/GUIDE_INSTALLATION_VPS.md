# 🚀 Guide Installation VPS - Solution 100% Économique

**Date**: 2025-01-20
**Cible**: VPS Production avec Ollama Local
**Coût total**: $20-40/mois (VPS) + $0 AI APIs

---

## 🎯 Objectif

Déployer RAG.dz sur VPS avec:
- ✅ **Ollama local** pour agents BMAD (GRATUIT)
- ✅ **Groq** pour Bolt génération (GRATUIT, 14k req/jour)
- ✅ **DeepSeek** en backup ($0-5/mois)

**Économie**: $300-500/mois vs Claude/OpenAI

---

## 📋 Prérequis VPS

### Recommandations Serveur:

#### Option A: CPU Only (Budget)
- **RAM**: 16GB minimum
- **CPU**: 4 cores minimum
- **Disk**: 100GB SSD
- **Providers**:
  - Hetzner CPX31 (~$15/mois)
  - OVH VPS ~$20/mois
  - Contabo (~$12/mois)

#### Option B: Avec GPU (Performance)
- **RAM**: 16GB+
- **GPU**: NVIDIA 8GB+ VRAM
- **Providers**:
  - Vast.ai (~$0.20/h = $150/mois)
  - RunPod (~$0.30/h = $220/mois)
  - Lambda Labs (~$0.50/h)

**Recommandation**: **Option A (CPU)** pour commencer
- Ollama fonctionne bien sur CPU
- Moins cher
- Suffisant pour 10-50 users

---

## 🔧 Installation Étape par Étape

### Étape 1: Préparer le VPS

```bash
# SSH dans ton VPS
ssh root@ton-vps-ip

# Mettre à jour le système
apt update && apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Installer Docker Compose
apt install docker-compose-plugin -y

# Vérifier installation
docker --version
docker compose version
```

### Étape 2: Cloner le Projet

```bash
# Créer répertoire
mkdir -p /opt/ragdz
cd /opt/ragdz

# Cloner (ou copier depuis GitHub)
git clone https://github.com/ton-repo/rag-dz.git .

# Ou uploader via SCP
# scp -r /local/path/rag-dz root@vps-ip:/opt/ragdz
```

### Étape 3: Configurer .env

```bash
# Copier template
cp .env.example .env

# Éditer avec nano
nano .env
```

**Configuration .env VPS**:
```env
# ===== AI PROVIDERS =====
# DeepSeek (backup uniquement)
DEEPSEEK_API_KEY=sk_YOUR_DEEPSEEK_API_KEY_HERE

# Groq (gratuit, backup Ollama)
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE

# ===== BMAD CONFIGURATION =====
# Provider principal
BMAD_PROVIDER=ollama  # ollama | groq | deepseek
USE_OLLAMA=true
OLLAMA_API_BASE_URL=http://ollama:11434/v1

# Fallback si Ollama fail
BMAD_FALLBACK_PROVIDER=groq
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE

# ===== DATABASE =====
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD_123
POSTGRES_USER=postgres
POSTGRES_DB=archon

# ===== SECURITY =====
JWT_SECRET_KEY=CHANGE_ME_RANDOM_STRING_VERY_LONG_32CHARS
API_SECRET_KEY=CHANGE_ME_ANOTHER_RANDOM_STRING
```

### Étape 4: Démarrer les Services

```bash
# Démarrer tous les containers
docker compose up -d

# Vérifier status
docker compose ps

# Attendre que tout soit up (2-3 min)
watch -n 2 'docker compose ps'
```

### Étape 5: Installer Modèles Ollama

```bash
# Modèles recommandés pour BMAD agents
docker exec ragdz-ollama ollama pull llama3.2:3b        # 2GB - Conversations
docker exec ragdz-ollama ollama pull qwen2.5-coder:7b   # 4GB - Code
docker exec ragdz-ollama ollama pull deepseek-r1:7b     # 4GB - Reasoning

# Alternative ultra-légère (si RAM limitée)
docker exec ragdz-ollama ollama pull gemma2:2b          # 1.5GB

# Vérifier modèles installés
docker exec ragdz-ollama ollama list
```

**Temps de téléchargement**: 10-30 minutes selon connexion

### Étape 6: Tester l'Installation

```bash
# 1. Test Backend
curl http://localhost:8180/health

# 2. Test BMAD Health
curl http://localhost:8180/api/bmad/chat/health

# 3. Test Ollama
curl http://localhost:11434/api/tags

# 4. Test Agent BMAD avec Ollama
curl -X POST http://localhost:8180/api/bmad/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "bmm-architect",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Étape 7: Configurer Firewall

```bash
# Ouvrir ports nécessaires
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw allow 8180/tcp    # Backend API
ufw allow 5174/tcp    # Bolt.DIY
ufw allow 3737/tcp    # Archon UI
ufw allow 5173/tcp    # RAG-UI

# Activer firewall
ufw enable
```

### Étape 8: Configurer Nginx (Reverse Proxy)

```bash
# Installer Nginx
apt install nginx -y

# Créer config
nano /etc/nginx/sites-available/ragdz
```

**Configuration Nginx**:
```nginx
server {
    listen 80;
    server_name ton-domaine.com;

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8180/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Bolt.DIY
    location / {
        proxy_pass http://localhost:5174;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

server {
    listen 80;
    server_name archon.ton-domaine.com;

    location / {
        proxy_pass http://localhost:3737;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }
}

server {
    listen 80;
    server_name rag.ton-domaine.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }
}
```

```bash
# Activer config
ln -s /etc/nginx/sites-available/ragdz /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Étape 9: HTTPS avec Let's Encrypt

```bash
# Installer Certbot
apt install certbot python3-certbot-nginx -y

# Obtenir certificats SSL
certbot --nginx -d ton-domaine.com -d archon.ton-domaine.com -d rag.ton-domaine.com

# Auto-renewal
certbot renew --dry-run
```

---

## 🎨 Architecture VPS Finale

```
Internet
   ↓
Nginx (Port 80/443) + SSL
   ↓
┌──────────────────────────────────────────┐
│              VPS SERVER                  │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Ollama (Port 11434)               │ │
│  │  - llama3.2:3b (conversations)     │ │
│  │  - qwen2.5-coder:7b (code)         │ │
│  │  - deepseek-r1:7b (reasoning)      │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Backend API (Port 8180)           │ │
│  │  - BMAD → Ollama local             │ │
│  │  - Fallback → Groq (gratuit)       │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Bolt.DIY (Port 5174)              │ │
│  │  - Provider: Groq (gratuit)        │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  PostgreSQL + Redis + Qdrant       │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## 📊 Performance Attendue

### Sur VPS CPU (16GB RAM):

| Opération | Temps | Coût |
|-----------|-------|------|
| **Génération code Bolt** | 2-5s | $0 (Groq) |
| **Chat agent BMAD** | 3-8s | $0 (Ollama) |
| **Orchestration 5 agents** | 20-40s | $0 |
| **Création projet Archon** | 1-2s | $0 |

### Throughput:
- **10 users simultanés**: OK ✅
- **50 users**: Possible avec Groq fallback ✅
- **100+ users**: Besoin upgrade RAM ou GPU ⚠️

---

## 🔧 Maintenance & Monitoring

### Commandes Utiles:

```bash
# Logs en temps réel
docker compose logs -f backend
docker compose logs -f ollama

# Redémarrer service
docker compose restart backend

# Mettre à jour
git pull
docker compose pull
docker compose up -d --build

# Vérifier espace disque
df -h
du -sh /var/lib/docker/volumes/

# Monitorer ressources
docker stats
```

### Scripts Automatiques:

```bash
# Script backup quotidien
nano /opt/ragdz/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
docker exec ragdz-postgres pg_dump -U postgres archon > /backups/ragdz-$DATE.sql
find /backups -name "ragdz-*.sql" -mtime +7 -delete
```

```bash
chmod +x /opt/ragdz/backup.sh
crontab -e
# Ajouter:
0 2 * * * /opt/ragdz/backup.sh
```

---

## 💰 Coûts Finaux

### VPS + Services:

```
VPS Hetzner CPX31:        $15/mois
Domaine (Cloudflare):     $10/an
SSL (Let's Encrypt):      GRATUIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL Infrastructure:     ~$16/mois
```

### AI APIs:

```
Ollama local (BMAD):      $0/mois ✅
Groq (Bolt):              $0/mois ✅
DeepSeek (backup):        $0-2/mois ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL AI:                 $0-2/mois ✅
```

### **TOTAL MENSUEL**: **~$16-18/mois**

**vs Claude/OpenAI**: **$300-500/mois**

**ÉCONOMIE**: **$282-484/mois (94-97%)**

---

## 🚨 Troubleshooting

### Problème 1: Ollama Out of Memory

```bash
# Réduire taille modèle
docker exec ragdz-ollama ollama rm qwen2.5-coder:7b
docker exec ragdz-ollama ollama pull gemma2:2b  # Plus léger

# Ou augmenter swap
fallocate -l 8G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

### Problème 2: Ollama trop lent

```bash
# Basculer sur Groq
nano .env
# Change:
BMAD_PROVIDER=groq
USE_OLLAMA=false

docker compose restart backend
```

### Problème 3: Rate Limit Groq

```bash
# Activer DeepSeek en fallback
nano .env
BMAD_FALLBACK_PROVIDER=deepseek

docker compose restart backend
```

---

## ✅ Checklist Déploiement

### Avant déploiement:
- [ ] VPS provisionné (16GB RAM min)
- [ ] Domaines configurés (DNS)
- [ ] Clés API testées localement
- [ ] Backup .env et docker-compose.yml

### Pendant déploiement:
- [ ] Docker + Docker Compose installés
- [ ] Projet cloné/copié
- [ ] .env configuré
- [ ] Services démarrés
- [ ] Modèles Ollama téléchargés
- [ ] Tests API passés

### Après déploiement:
- [ ] Nginx configuré
- [ ] HTTPS activé (SSL)
- [ ] Firewall configuré
- [ ] Backup automatique actif
- [ ] Monitoring configuré
- [ ] Tests end-to-end OK

---

## 🎉 Félicitations!

Tu as maintenant:
- ✅ RAG.dz déployé sur VPS
- ✅ Ollama local pour AI (GRATUIT)
- ✅ Groq en backup (GRATUIT)
- ✅ HTTPS + Domaines
- ✅ Coût total: ~$16-18/mois

**Économie annuelle**: **$3,384-5,808** 💰

---

**Support**: Vérifie `docs/SOLUTIONS_ECONOMIQUES_AI.md` pour optimisations
**Problèmes**: Check logs avec `docker compose logs -f`
