# 🚀 IAFactory Academy - Quick Start Deployment

Déploie ton LMS en production en **30 minutes** !

## ⚡ Déploiement Ultra-Rapide

### Étape 1: Infrastructure VPS (5 min)

```bash
# Option A: Hetzner Cloud (6€/mois) - Recommandé
1. Créer compte: https://www.hetzner.cloud
2. New Project → CX21 (2 vCPU, 4GB RAM)
3. Ubuntu 22.04 LTS
4. SSH Key setup

# Option B: DigitalOcean (5€/mois)
1. Créer compte: https://digitalocean.com
2. Droplet → Basic → 2GB Memory
3. Ubuntu 22.04 x64

# Option C: Linode (5€/mois)
1. Créer compte: https://linode.com
2. Linode 2GB
3. Ubuntu 22.04 LTS
```

### Étape 2: Installation Docker (5 min)

```bash
# SSH vers serveur
ssh root@YOUR_SERVER_IP

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

### Étape 3: Upload & Configure (10 min)

```bash
# Sur ton ordinateur local
scp -r . root@YOUR_SERVER_IP:/opt/iafactory-academy

# SSH vers serveur
ssh root@YOUR_SERVER_IP

# Navigate
cd /opt/iafactory-academy

# Copy environment
cp .env.production.example .env

# Generate secrets
nano .env

# Edit les variables:
# - SECRET_KEY=$(openssl rand -hex 32)
# - JWT_SECRET=$(openssl rand -hex 32)
# - DB_PASSWORD=$(openssl rand -hex 16)
# - POSTGRES_PASSWORD=$(openssl rand -hex 16)
```

### Étape 4: Deploy ! (5 min)

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Deploy !
./scripts/deploy.sh

# Wait for containers to start
docker-compose -f docker-compose.prod.yml logs -f
```

**✅ Application en ligne sur http://YOUR_SERVER_IP**

### Étape 5: DNS & SSL (Optional, 5 min)

```bash
# Configure DNS records:
# A record: @  → YOUR_SERVER_IP
# A record: www → YOUR_SERVER_IP

# Setup SSL automatique
./scripts/setup-ssl.sh

# Enter domain when prompted
```

**🔒 Application en ligne sur https://yourdomain.com**

---

## 📋 Vérification Post-Deploy

```bash
# 1. Check containers
docker-compose -f docker-compose.prod.yml ps

# 2. Test Backend API
curl http://localhost:8000/health
# Response: {"status":"healthy"}

# 3. Test Database
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory

# 4. Test Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
# Response: PONG

# 5. Frontend
# Open: http://YOUR_SERVER_IP
```

---

## 🔧 Commandes Essentielles

```bash
# Démarrer
docker-compose -f docker-compose.prod.yml up -d

# Arrêter
docker-compose -f docker-compose.prod.yml down

# Logs
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f db

# Database migration
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Create admin user
docker-compose -f docker-compose.prod.yml exec api python -c "
from app.models import User
from app.core.database import get_db
from app.core.security import get_password_hash

# Prompt for admin details
email = input('Admin email: ')
password = input('Admin password: ')
first_name = input('First name: ')
last_name = input('Last name: ')

# Create user
user = User(
    email=email,
    hashed_password=get_password_hash(password),
    first_name=first_name,
    last_name=last_name,
    role='admin',
    is_active=True
)
"

# Backup
./scripts/backup.sh

# Restore from backup
./scripts/restore.sh backup-2025-01-20.tar.gz
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs api

# Rebuild
docker-compose -f docker-compose.prod.yml build

# Start fresh
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Database connection error

```bash
# Check PostgreSQL
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory

# Reset database
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### Port already in use

```bash
# Check what's using port 80/443
sudo lsof -i :80
sudo lsof -i :443

# Kill process
sudo kill -9 PID

# Or change port in docker-compose.prod.yml
```

---

## 💰 Coûts Mensuels

| Provider | Instance | CPU | RAM | Price |
|----------|----------|-----|-----|-------|
| Hetzner | CX21 | 2 vCPU | 4GB | 6€ |
| DigitalOcean | Basic | 1 vCPU | 2GB | 5€ |
| Linode | 2GB | 1 vCPU | 2GB | 5€ |
| AWS | t3.small | 2 vCPU | 2GB | 25€ |
| Azure | B2s | 2 vCPU | 4GB | 40€ |

**Pour 500-5000 users: CX21 suffit !**

**Coûts annuels:**
- Serveur: 72€
- Domaine: 25€
- Email: 0€ (SendGrid gratuit)
- Monitoring: 0€ (Sentry gratuit)
- **TOTAL: 97€/an**

---

## 📊 KPIs à Tracker

```bash
# Visiter le dashboard
https://YOUR_SERVER_IP/admin

# Metrics:
- Users count
- Courses count
- Enrollments count
- Revenue
- Active sessions

# Server health:
- CPU usage
- Memory usage
- Disk usage
- Database connections
```

---

## 🚀 Prochaines Étapes

1. ✅ Deploy infrastructure
2. ✅ Setup SSL/TLS
3. ✅ Create admin account
4. [ ] Créer 3 cours pilotes
5. [ ] Inviter 50 beta users
6. [ ] Collect feedback
7. [ ] Public launch

---

## 📞 Support

**Documentation complète:**
- See: `DEPLOYMENT_GUIDE.md` (80+ pages)
- See: `COSTS_AND_OPTIONS.md` (pricing strategies)

**Questions?**
- Check logs: `docker-compose logs -f`
- Check health: `curl http://localhost:8000/health`
- Read docs: `./docs`

---

**TU ES PRÊT ! GO DEPLOY ! 🚀**
