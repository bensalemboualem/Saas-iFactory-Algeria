#!/bin/bash
# ================================================================
# GÉNÉRATION DOCUMENTATION 43 SERVICES
# IAFactory Algeria - Infrastructure Complete
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "================================================================"
echo "📚 GÉNÉRATION DOCUMENTATION DES SERVICES"
echo "================================================================"
echo ""

OUTPUT_FILE="/opt/iafactory-rag-dz/DOCUMENTATION_43_SERVICES.md"

echo "Génération de la documentation dans: $OUTPUT_FILE"
echo ""

# ================================================================
# GÉNÉRATION DU DOCUMENT
# ================================================================

cat > "$OUTPUT_FILE" << 'DOCEOF'
# DOCUMENTATION COMPLÈTE DES SERVICES
## IAFactory Algeria - Infrastructure Production

**Date de génération:** $(date '+%d %B %Y à %H:%M')
**Serveur:** iafactorysuisse (46.224.3.125)
**Total services:** 43+ conteneurs Docker

---

## 📊 VUE D'ENSEMBLE

### Catégories de Services

1. **Services IA & ML** (4)
   - Archon, Ollama, Qdrant, N8N

2. **Applications Business** (8+)
   - PME Copilot, CRM IA, StartupDZ, etc.

3. **Monitoring & Observabilité** (7)
   - Prometheus, Grafana, Loki, AlertManager

4. **Infrastructure Core** (4)
   - PostgreSQL, Backend API, Nginx, Certbot

5. **Applications Sectorielles** (20+)
   - AgriDZ, MedDZ, PharmaDZ, BTPdz, etc.

---

# SERVICES IA & MACHINE LEARNING

## 🌟 Archon - Système de Gestion des Connaissances

### archon-server

**Container:** archon-server
**Image:** Custom build (Python 3.12)
**Port:** 8181
**Status:** Healthy
**URL:** https://archon.iafactoryalgeria.com/api/

**Description:**
Backend API principal d'Archon pour la gestion des bases de connaissances avec Model Context Protocol (MCP).

**Variables d'environnement:**
```env
SUPABASE_URL=https://cxzcmmolfgijhjbevtzi.supabase.co
SUPABASE_SERVICE_KEY=***
LOG_LEVEL=INFO
HOST=localhost
ARCHON_SERVER_PORT=8181
```

**Health Check:**
```bash
curl http://localhost:8181/health
```

**Logs:**
```bash
docker logs archon-server -f
```

**Restart:**
```bash
docker restart archon-server
```

**Dépendances:**
- Supabase (PostgreSQL + pgvector)
- Archon MCP Server

**Documentation:**
- GitHub: https://github.com/coleam00/Archon
- Docs: Voir /opt/iafactory-rag-dz/ARCHON_DEPLOIEMENT_COMPLET.md

---

### archon-mcp

**Container:** archon-mcp
**Image:** Custom build (Python 3.12)
**Port:** 8051
**Status:** Healthy

**Description:**
Serveur MCP (Model Context Protocol) pour l'intégration avec les LLM et outils externes.

**Health Check:**
```bash
curl http://localhost:8051/health
```

**Logs:**
```bash
docker logs archon-mcp -f
```

---

### archon-ui

**Container:** archon-ui
**Image:** Custom build (Node.js + Vite)
**Port:** 3737
**Status:** Healthy
**URL:** https://archon.iafactoryalgeria.com

**Description:**
Interface utilisateur React pour Archon avec design moderne et intégration SSE.

**Build:**
```bash
cd /opt/iafactory-rag-dz/frontend/archon-ui-stable
docker-compose build archon-ui
```

**Développement local:**
```bash
npm install
npm run dev
```

---

## 🤖 Ollama - LLM Local

**Container:** iaf-ollama
**Image:** ollama/ollama:latest
**Port:** 8186 → 11434 (localhost uniquement)
**Status:** Running

**Description:**
Serveur LLM local pour l'exécution de modèles llama3, qwen, etc. Conforme RGPD.

**Modèles installés:**
```bash
docker exec iaf-ollama ollama list
```

**Pull nouveau modèle:**
```bash
docker exec iaf-ollama ollama pull llama3.2
```

**Test:**
```bash
curl http://localhost:11434/api/tags
```

**Configuration:**
- Port externe: 8186 (SÉCURISÉ: localhost uniquement)
- Port interne: 11434
- GPU: CPU uniquement (pas de GPU)

**Performance:**
- RAM requise: 8GB minimum
- Temps de réponse: 2-5s par requête

---

## 🔍 Qdrant - Vector Database

**Container:** iaf-qdrant
**Image:** qdrant/qdrant:latest
**Port:** 6333 (localhost uniquement)
**Status:** Running
**Dashboard:** http://localhost:6333/dashboard

**Description:**
Base de données vectorielle pour les embeddings et recherche sémantique.

**Health Check:**
```bash
curl http://localhost:6333/health
```

**Collections:**
```bash
curl http://localhost:6333/collections
```

**Volume:**
- /qdrant/storage → qdrant_data (volume Docker)

**API Documentation:**
- http://localhost:6333/docs

---

## 🔄 N8N - Automation Workflows

**Container:** iaf-n8n
**Image:** n8nio/n8n:latest
**Port:** 5678
**URL:** https://www.iafactoryalgeria.com/n8n/

**Description:**
Plateforme d'automatisation low-code pour workflows business.

**Login:**
- URL: https://www.iafactoryalgeria.com/n8n/
- Credentials: Configurés dans interface

**Use Cases:**
- Automatisation fiscale (G50, IBS)
- Notifications clients
- Synchronisation données

---

# APPLICATIONS BUSINESS

## 💼 PME Copilot

### iaf-pme-copilot-prod

**Container:** iaf-pme-copilot-prod
**Port:** Interne
**Status:** Healthy

**Description:**
Backend API pour PME Copilot - assistant IA pour PME algériennes.

**Fonctionnalités:**
- Conseil fiscal (G50, IBS, TVA)
- Génération documents comptables
- Analyse financière

**Database:**
- PostgreSQL (iaf-postgres-prod)
- Tables: pme_*, factures, devis

---

### iaf-pme-copilot-ui-prod

**Container:** iaf-pme-copilot-ui-prod
**Port:** Exposé via Nginx
**URL:** https://www.iafactoryalgeria.com/pme/

**Description:**
Interface React pour PME Copilot.

**Features:**
- Dashboard financier
- Générateur G50
- Simulateur IBS
- Templates factures

---

## 🤝 CRM IA

### iaf-crm-ia-prod

**Container:** iaf-crm-ia-prod
**Status:** Healthy

**Description:**
Backend CRM avec IA pour gestion clients et leads.

**Modules:**
- Gestion contacts
- Pipeline ventes
- Prédictions IA (scoring leads)
- Emails automatiques

---

### iaf-crm-ia-ui-prod

**Container:** iaf-crm-ia-ui-prod
**URL:** https://www.iafactoryalgeria.com/crm/

**Description:**
Interface CRM moderne avec tableaux Kanban.

---

## 🚀 StartupDZ Onboarding

### iaf-startupdz-prod

**Container:** iaf-startupdz-prod
**Status:** Healthy

**Description:**
Backend pour onboarding startups algériennes.

**Services:**
- Création SARL/EURL
- Dossier ANADE/ANGEM
- Conformité fiscale

---

### iaf-startupdz-ui-prod

**Container:** iaf-startupdz-ui-prod
**URL:** https://www.iafactoryalgeria.com/startup/

**Description:**
Interface onboarding step-by-step.

---

## 🎙️ Voice Assistant

**Container:** iaf-voice-assistant
**Port:** 8204

**Description:**
Assistant vocal en français algérien avec Whisper.

**Features:**
- Transcription audio
- Réponses vocales
- Darija support

---

## 💰 Fiscal Assistant

**Container:** iaf-fiscal-assistant
**Port:** 8205

**Description:**
Expert fiscal algérien automatisé.

**Expertise:**
- Code général des impôts
- G50, IBS, TVA, TAP
- Déclarations fiscales

---

## ⚖️ Legal Assistant

**Container:** iaf-legal-assistant
**Port:** 8206

**Description:**
Assistant juridique pour droit algérien.

**Domaines:**
- Droit commercial
- Droit du travail
- Contrats types

---

## 💳 Billing Credits

**Container:** iaf-billing-credits

**Description:**
Système de crédits et facturation.

**Features:**
- Gestion crédits
- Facturation automatique
- Paiements CIB/Stripe

---

# MONITORING & OBSERVABILITÉ

## 📊 Grafana

**Container:** iaf-grafana
**Image:** grafana/grafana:latest
**Port:** 3033
**URL:** https://grafana.iafactoryalgeria.com (à configurer)

**Description:**
Plateforme de visualisation et dashboards.

**Login:**
- Username: admin
- Password: admin (à changer!)

**Data Sources:**
- Prometheus
- Loki
- PostgreSQL

**Dashboards:**
- Infrastructure overview
- Container metrics
- Application logs
- Business metrics

**Configuration:**
```bash
docker exec iaf-grafana grafana-cli admin reset-admin-password <nouveau-mdp>
```

---

## 📈 Prometheus

**Container:** iaf-prometheus
**Image:** prom/prometheus:latest
**Port:** 9090
**URL:** http://localhost:9090

**Description:**
Système de monitoring et alertes.

**Metrics collectées:**
- CPU, RAM, Disk par container
- Network I/O
- HTTP requests
- Custom app metrics

**Configuration:**
- /etc/prometheus/prometheus.yml

**PromQL exemples:**
```promql
# CPU usage
container_cpu_usage_seconds_total

# Memory usage
container_memory_usage_bytes

# HTTP requests
http_requests_total
```

---

## 📝 Loki

**Container:** iaf-loki
**Image:** grafana/loki:latest
**Port:** 3100

**Description:**
Agrégation et stockage logs.

**Log Sources:**
- Tous les containers Docker
- Nginx access/error logs
- Application logs

**Query:**
```logql
{container_name="iaf-backend-prod"} |= "error"
```

---

## 🚀 Promtail

**Container:** iaf-promtail
**Image:** grafana/promtail:latest

**Description:**
Agent de collecte logs vers Loki.

**Configuration:**
- Collecte tous les logs Docker
- Parse JSON logs
- Labels automatiques

---

## 🔔 AlertManager

**Container:** iaf-alertmanager
**Image:** prom/alertmanager:latest
**Port:** 9093

**Description:**
Gestion et routing des alertes.

**Notifications:**
- Email
- Slack
- Webhook

**Alertes configurées:**
- Container down
- High CPU (>80%)
- High memory (>90%)
- Disk space low (<10%)

---

## 📊 cAdvisor

**Container:** iaf-cadvisor
**Image:** gcr.io/cadvisor/cadvisor:latest
**Port:** 8888
**Status:** Healthy

**Description:**
Collecte métriques containers Docker.

**Metrics:**
- CPU, RAM, Network par container
- Filesystem usage
- Performance stats

---

## 💻 Node Exporter

**Container:** iaf-node-exporter
**Image:** prom/node-exporter:latest
**Port:** 9100

**Description:**
Métriques système hôte.

**Metrics:**
- CPU, RAM, Disk système
- Load average
- Network interfaces
- Temperature (si disponible)

---

# INFRASTRUCTURE CORE

## 🗄️ PostgreSQL + pgvector

**Container:** iaf-postgres-prod
**Image:** pgvector/pgvector:pg16
**Port:** 6330 → 5432 (localhost uniquement)
**Status:** Healthy

**Description:**
Base de données principale avec extension pgvector pour IA.

**Databases:**
- iafactory_dz (principale)
- archon_kb (Archon)
- crm_ia
- pme_copilot

**Credentials:**
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=*** (voir .env)
```

**Backups:**
- Automatiques: 2h00 chaque jour
- Rétention: 30 jours quotidiens, 12 semaines hebdo, 12 mois mensuels
- Location: /opt/backups/postgresql/

**Commandes:**
```bash
# Connexion
docker exec -it iaf-postgres-prod psql -U postgres

# Backup manuel
docker exec iaf-postgres-prod pg_dumpall -U postgres | gzip > backup.sql.gz

# Restore
zcat backup.sql.gz | docker exec -i iaf-postgres-prod psql -U postgres
```

**Extensions installées:**
- pgvector (embeddings ML)
- pg_trgm (recherche texte)
- uuid-ossp

---

## 🌐 Backend API

**Container:** iaf-backend-prod
**Image:** Custom FastAPI
**Port:** 8180
**Status:** Healthy

**Description:**
API principale IAFactory Algeria.

**Endpoints:**
- /api/v1/auth
- /api/v1/users
- /api/v1/projects
- /api/v1/knowledge
- /api/v1/agents

**Documentation:**
- Swagger: https://www.iafactoryalgeria.com/api/docs
- ReDoc: https://www.iafactoryalgeria.com/api/redoc

**Technologies:**
- FastAPI
- SQLAlchemy
- Alembic migrations
- JWT auth

---

## 🌍 Nginx Reverse Proxy

**Service:** nginx (système)
**Ports:** 80, 443
**Config:** /etc/nginx/sites-enabled/

**Description:**
Reverse proxy principal pour tous les services.

**Routes principales:**
```nginx
/ → Landing page
/api/ → Backend API (8180)
/archon/ → Archon UI (3737)
/bolt/ → Bolt.diy (5173)
/pme/ → PME Copilot
/crm/ → CRM IA
/n8n/ → N8N workflows
```

**SSL:**
- Let's Encrypt
- Auto-renewal
- HTTPS redirect

**Commands:**
```bash
# Test config
nginx -t

# Reload
systemctl reload nginx

# Logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

# APPLICATIONS SECTORIELLES

## 🌾 AgriDZ

**URL:** /agri/
**Description:** Solutions agricoles algériennes
**Features:** Irrigation, météo, marchés

## 🏥 MedDZ

**URL:** /med/
**Description:** Gestion cabinet médical
**Features:** Patients, rendez-vous, prescriptions

## 💊 PharmaDZ

**URL:** /pharma/
**Description:** Gestion pharmacie
**Features:** Stock, ventes, ordonnances

## 🏗️ BTPdz

**URL:** /btp/
**Description:** Gestion chantiers BTP
**Features:** Devis, planning, matériaux

## 📊 Data-DZ

**URL:** /data/
**Description:** Dashboards données algériennes
**Features:** Économie, démographie, stats

## 👨‍💻 Developer Portal

**URL:** /dev/
**Description:** Portail développeurs
**Features:** API docs, SDKs, exemples

---

# COMMANDES UTILES

## Gestion Containers

```bash
# Voir tous les containers
docker ps

# Logs d'un service
docker logs <container-name> -f

# Restart service
docker restart <container-name>

# Stop/Start
docker stop <container-name>
docker start <container-name>

# Stats temps réel
docker stats

# Inspecter
docker inspect <container-name>
```

## Gestion Volumes

```bash
# Lister volumes
docker volume ls

# Inspecter volume
docker volume inspect <volume-name>

# Backup volume
docker run --rm -v <volume>:/data -v $(pwd):/backup alpine tar czf /backup/volume-backup.tar.gz /data
```

## Maintenance

```bash
# Nettoyer images inutilisées
docker system prune -a

# Espace disque
docker system df

# Logs anciens
docker system prune --volumes

# Rebuild service
cd /opt/iafactory-rag-dz
docker-compose up -d --build <service-name>
```

---

# PROCÉDURES D'URGENCE

## Container down

```bash
# 1. Vérifier logs
docker logs <container-name> --tail=100

# 2. Restart
docker restart <container-name>

# 3. Si échoue, rebuild
docker-compose up -d --build <container-name>
```

## PostgreSQL corruption

```bash
# 1. Arrêter services
docker-compose stop

# 2. Restore backup
/usr/local/bin/postgres-restore.sh /opt/backups/postgresql/daily/<latest>.sql.gz

# 3. Redémarrer
docker-compose up -d
```

## Disk plein

```bash
# 1. Identifier utilisation
du -sh /var/lib/docker/volumes/*
docker system df

# 2. Nettoyer
docker system prune -a --volumes
find /var/log -name "*.log" -mtime +30 -delete

# 3. Nettoyer backups anciens
find /opt/backups -mtime +90 -delete
```

## SSL expiré

```bash
# Renouveler
certbot renew --force-renewal

# Reload Nginx
systemctl reload nginx
```

---

# CONTACTS & SUPPORT

**Admin Système:** root@iafactoryalgeria.com
**Support Technique:** support@iafactoryalgeria.com
**Urgences:** +213 XXX XXX XXX

**Documentation:**
- Repo: /opt/iafactory-rag-dz/
- Scripts: /usr/local/bin/
- Logs: /var/log/

**Monitoring:**
- Grafana: https://grafana.iafactoryalgeria.com
- Prometheus: http://localhost:9090
- AlertManager: http://localhost:9093

---

**Document généré automatiquement**
**Date:** $(date)
**Version:** 1.0
DOCEOF

echo -e "${GREEN}✅ Documentation générée${NC}"
echo ""

# Compter les services réels
CONTAINER_COUNT=$(docker ps --format '{{.Names}}' | wc -l)

echo "📊 Statistiques:"
echo "  • Containers actifs: $CONTAINER_COUNT"
echo "  • Fichier: $OUTPUT_FILE"
echo "  • Taille: $(du -h "$OUTPUT_FILE" | awk '{print $1}')"
echo ""

# Générer aussi un index JSON
echo "Génération index JSON..."

docker ps --format '{"name":"{{.Names}}","status":"{{.Status}}","ports":"{{.Ports}}"}' | \
    jq -s '.' > /opt/iafactory-rag-dz/services-index.json 2>/dev/null || echo "[]" > /opt/iafactory-rag-dz/services-index.json

echo -e "${GREEN}✅ Index JSON généré: services-index.json${NC}"
echo ""

echo "================================================================"
echo -e "${GREEN}✅ DOCUMENTATION COMPLÈTE GÉNÉRÉE${NC}"
echo "================================================================"
echo ""
echo "Fichiers créés:"
echo "  • $OUTPUT_FILE"
echo "  • /opt/iafactory-rag-dz/services-index.json"
echo ""
echo "📖 Lire la documentation:"
echo "  less $OUTPUT_FILE"
echo "  cat $OUTPUT_FILE | grep -A 10 'service-name'"
echo ""
