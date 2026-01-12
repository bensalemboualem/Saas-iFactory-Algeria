#!/bin/bash
set -euo pipefail

###############################################################################
# Script de Monitoring et Backup pour IAFactory RAG-DZ
# Ce script configure le monitoring, les alertes et les backups automatiques
###############################################################################

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Configuration
BACKUP_DIR="/backup/iafactory"
LOG_DIR="/var/log/iafactory"
APP_DIR="/opt/iafactory"
RETENTION_DAYS=7

main() {
    log_info "Configuration du monitoring et des backups..."

    # Créer les répertoires
    mkdir -p $BACKUP_DIR
    mkdir -p $LOG_DIR

    # =================================================================
    # 1. SCRIPT DE HEALTH CHECK
    # =================================================================
    log_info "Création du script de health check..."
    cat > /usr/local/bin/iafactory-health.sh << 'EOF'
#!/bin/bash
###############################################################################
# IAFactory Health Check Script
###############################################################################

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════════"
echo "  IAFactory RAG-DZ - État des Services"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd /opt/iafactory

# Services Docker
echo "🐳 Services Docker:"
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
echo ""

# Backend Health
echo "🔧 Backend API:"
BACKEND_HEALTH=$(curl -s http://localhost:8180/health 2>/dev/null || echo '{"status":"error"}')
BACKEND_STATUS=$(echo $BACKEND_HEALTH | jq -r '.status // "error"' 2>/dev/null || echo "error")
if [ "$BACKEND_STATUS" = "ok" ] || [ "$BACKEND_STATUS" = "healthy" ]; then
    echo -e "   ${GREEN}✓${NC} Backend: Healthy"
else
    echo -e "   ${RED}✗${NC} Backend: Unhealthy"
fi

# Frontend Check
echo ""
echo "🌐 Frontends:"
for PORT in 8182 8183 8184; do
    if curl -sf http://localhost:$PORT > /dev/null 2>&1; then
        echo -e "   ${GREEN}✓${NC} Port $PORT: Accessible"
    else
        echo -e "   ${RED}✗${NC} Port $PORT: Inaccessible"
    fi
done

# Database Check
echo ""
echo "💾 Database:"
DB_RESULT=$(docker exec iaf-dz-postgres pg_isready -U iafactory_admin 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✓${NC} PostgreSQL: Ready"
else
    echo -e "   ${RED}✗${NC} PostgreSQL: Not Ready"
fi

# Redis Check
echo ""
echo "🔴 Cache:"
REDIS_PING=$(docker exec iaf-dz-redis redis-cli ping 2>/dev/null || echo "FAIL")
if [ "$REDIS_PING" = "PONG" ]; then
    echo -e "   ${GREEN}✓${NC} Redis: Responding"
else
    echo -e "   ${RED}✗${NC} Redis: Not Responding"
fi

# Disk Usage
echo ""
echo "💿 Espace Disque:"
df -h / | tail -1 | awk '{printf "   Utilisé: %s / %s (%s)\n", $3, $2, $5}'

# Memory Usage
echo ""
echo "🧠 Mémoire:"
free -h | grep Mem | awk '{printf "   Utilisée: %s / %s\n", $3, $2}'

# Docker Stats (last 5 seconds average)
echo ""
echo "📊 Consommation Docker:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -10

echo ""
echo "═══════════════════════════════════════════════════════════════"
EOF

    chmod +x /usr/local/bin/iafactory-health.sh
    log_success "Script de health check créé"

    # =================================================================
    # 2. SCRIPT DE BACKUP
    # =================================================================
    log_info "Création du script de backup..."
    cat > /usr/local/bin/iafactory-backup.sh << 'EOF'
#!/bin/bash
set -euo pipefail

###############################################################################
# IAFactory Backup Script
###############################################################################

BACKUP_DIR="/backup/iafactory"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/iafactory/backup.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "===== Démarrage du backup ====="

# Créer le répertoire de backup
mkdir -p $BACKUP_DIR

# 1. Backup PostgreSQL
log "Backup PostgreSQL..."
if docker exec iaf-dz-postgres pg_dump -U iafactory_admin iafactory_prod | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz; then
    log "✓ PostgreSQL backup: OK"
else
    log "✗ PostgreSQL backup: FAILED"
fi

# 2. Backup Qdrant (vector database)
log "Backup Qdrant..."
if docker exec iaf-dz-qdrant tar czf - /qdrant/storage > $BACKUP_DIR/qdrant_$DATE.tar.gz; then
    log "✓ Qdrant backup: OK"
else
    log "✗ Qdrant backup: FAILED"
fi

# 3. Backup Redis (si nécessaire pour données persistantes)
log "Backup Redis..."
if docker exec iaf-dz-redis redis-cli SAVE > /dev/null 2>&1; then
    docker cp iaf-dz-redis:/data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb
    gzip $BACKUP_DIR/redis_$DATE.rdb
    log "✓ Redis backup: OK"
else
    log "✗ Redis backup: FAILED"
fi

# 4. Backup configuration files
log "Backup configuration..."
tar czf $BACKUP_DIR/config_$DATE.tar.gz -C /opt/iafactory .env docker-compose.yml 2>/dev/null
log "✓ Configuration backup: OK"

# 5. Backup uploaded files (if any)
if [ -d "/opt/iafactory/data" ]; then
    log "Backup uploaded files..."
    tar czf $BACKUP_DIR/data_$DATE.tar.gz -C /opt/iafactory data/
    log "✓ Files backup: OK"
fi

# Nettoyer les anciens backups (garder 7 jours)
log "Nettoyage des anciens backups..."
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +7 -delete
log "✓ Nettoyage: OK"

# Calculer la taille totale des backups
TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
log "Taille totale des backups: $TOTAL_SIZE"

log "===== Backup terminé ====="
echo ""
EOF

    chmod +x /usr/local/bin/iafactory-backup.sh
    log_success "Script de backup créé"

    # =================================================================
    # 3. SCRIPT DE RESTAURATION
    # =================================================================
    log_info "Création du script de restauration..."
    cat > /usr/local/bin/iafactory-restore.sh << 'EOF'
#!/bin/bash
set -euo pipefail

###############################################################################
# IAFactory Restore Script
###############################################################################

BACKUP_DIR="/backup/iafactory"

# Liste des backups disponibles
echo "═══════════════════════════════════════════════════════════════"
echo "  Backups Disponibles"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "PostgreSQL:"
ls -lh $BACKUP_DIR/postgres_*.sql.gz 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Qdrant:"
ls -lh $BACKUP_DIR/qdrant_*.tar.gz 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""

read -p "Entrez le timestamp du backup à restaurer (ex: 20250124_153000): " TIMESTAMP

if [ -z "$TIMESTAMP" ]; then
    echo "Annulé"
    exit 1
fi

# Confirmer
echo ""
echo "⚠️  ATTENTION: Cette opération va écraser les données actuelles!"
read -p "Continuer? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Annulé"
    exit 1
fi

# Restaurer PostgreSQL
echo ""
echo "Restauration PostgreSQL..."
if [ -f "$BACKUP_DIR/postgres_$TIMESTAMP.sql.gz" ]; then
    gunzip -c $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz | docker exec -i iaf-dz-postgres psql -U iafactory_admin iafactory_prod
    echo "✓ PostgreSQL restauré"
else
    echo "✗ Fichier postgres_$TIMESTAMP.sql.gz introuvable"
fi

# Restaurer Qdrant
echo ""
echo "Restauration Qdrant..."
if [ -f "$BACKUP_DIR/qdrant_$TIMESTAMP.tar.gz" ]; then
    docker stop iaf-dz-qdrant
    docker exec iaf-dz-qdrant rm -rf /qdrant/storage/*
    gunzip -c $BACKUP_DIR/qdrant_$TIMESTAMP.tar.gz | docker exec -i iaf-dz-qdrant tar xzf - -C /
    docker start iaf-dz-qdrant
    echo "✓ Qdrant restauré"
else
    echo "✗ Fichier qdrant_$TIMESTAMP.tar.gz introuvable"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Restauration Terminée"
echo "═══════════════════════════════════════════════════════════════"
EOF

    chmod +x /usr/local/bin/iafactory-restore.sh
    log_success "Script de restauration créé"

    # =================================================================
    # 4. SCRIPT D'ALERTES
    # =================================================================
    log_info "Création du script d'alertes..."
    cat > /usr/local/bin/iafactory-alerts.sh << 'EOF'
#!/bin/bash
###############################################################################
# IAFactory Alert Script
###############################################################################

cd /opt/iafactory

# Vérifier les services critiques
ALERTS=""

# Backend
if ! curl -sf http://localhost:8180/health > /dev/null 2>&1; then
    ALERTS="${ALERTS}\n⚠️  Backend API: DOWN"
fi

# Database
if ! docker exec iaf-dz-postgres pg_isready -U iafactory_admin > /dev/null 2>&1; then
    ALERTS="${ALERTS}\n⚠️  PostgreSQL: DOWN"
fi

# Redis
if ! docker exec iaf-dz-redis redis-cli ping > /dev/null 2>&1; then
    ALERTS="${ALERTS}\n⚠️  Redis: DOWN"
fi

# Disk space > 80%
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    ALERTS="${ALERTS}\n⚠️  Disk Usage: ${DISK_USAGE}%"
fi

# Memory > 90%
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ $MEM_USAGE -gt 90 ]; then
    ALERTS="${ALERTS}\n⚠️  Memory Usage: ${MEM_USAGE}%"
fi

# Si des alertes existent, les afficher et logger
if [ ! -z "$ALERTS" ]; then
    echo -e "\n🚨 ALERTES IAFactory:\n$ALERTS" | tee -a /var/log/iafactory/alerts.log

    # Optionnel: Envoyer un email ou un webhook
    # curl -X POST https://your-webhook-url.com -d "alerts=$ALERTS"
fi
EOF

    chmod +x /usr/local/bin/iafactory-alerts.sh
    log_success "Script d'alertes créé"

    # =================================================================
    # 5. SCRIPT DE MAINTENANCE
    # =================================================================
    log_info "Création du script de maintenance..."
    cat > /usr/local/bin/iafactory-maintenance.sh << 'EOF'
#!/bin/bash
###############################################################################
# IAFactory Maintenance Script
###############################################################################

echo "═══════════════════════════════════════════════════════════════"
echo "  IAFactory - Maintenance"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd /opt/iafactory

# Nettoyer les logs Docker
echo "🧹 Nettoyage des logs Docker..."
truncate -s 0 /var/lib/docker/containers/*/*-json.log 2>/dev/null
echo "✓ Logs nettoyés"

# Nettoyer les images Docker inutilisées
echo ""
echo "🐳 Nettoyage des images Docker..."
docker image prune -af --filter "until=72h"
echo "✓ Images nettoyées"

# Nettoyer les volumes non utilisés
echo ""
echo "📦 Nettoyage des volumes..."
docker volume prune -f
echo "✓ Volumes nettoyés"

# Optimiser PostgreSQL
echo ""
echo "🗄️  Optimisation PostgreSQL..."
docker exec iaf-dz-postgres psql -U iafactory_admin -d iafactory_prod -c "VACUUM ANALYZE;"
echo "✓ PostgreSQL optimisé"

# Statistiques
echo ""
echo "📊 Statistiques:"
echo "   Docker images: $(docker images -q | wc -l)"
echo "   Docker volumes: $(docker volume ls -q | wc -l)"
echo "   Espace disque libre: $(df -h / | tail -1 | awk '{print $4}')"

echo ""
echo "═══════════════════════════════════════════════════════════════"
EOF

    chmod +x /usr/local/bin/iafactory-maintenance.sh
    log_success "Script de maintenance créé"

    # =================================================================
    # 6. CRONTAB - Tâches Planifiées
    # =================================================================
    log_info "Configuration des tâches planifiées..."

    # Ajouter les tâches cron
    (crontab -l 2>/dev/null || true; cat << 'CRON'
# IAFactory RAG-DZ - Tâches Planifiées

# Backup quotidien à 2h du matin
0 2 * * * /usr/local/bin/iafactory-backup.sh >> /var/log/iafactory/backup.log 2>&1

# Vérification de santé toutes les 5 minutes
*/5 * * * * /usr/local/bin/iafactory-alerts.sh

# Maintenance hebdomadaire (dimanche à 3h)
0 3 * * 0 /usr/local/bin/iafactory-maintenance.sh >> /var/log/iafactory/maintenance.log 2>&1

# Renouvellement SSL automatique (quotidien à 3h30)
30 3 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'

CRON
) | crontab -

    log_success "Tâches planifiées configurées"

    # =================================================================
    # 7. LOGROTATE
    # =================================================================
    log_info "Configuration de logrotate..."
    cat > /etc/logrotate.d/iafactory << 'EOF'
/var/log/iafactory/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        systemctl reload rsyslog > /dev/null 2>&1 || true
    endscript
}
EOF

    log_success "Logrotate configuré"

    # =================================================================
    # 8. SCRIPT DE DÉMARRAGE RAPIDE
    # =================================================================
    log_info "Création du script de démarrage rapide..."
    cat > /usr/local/bin/iafactory << 'EOF'
#!/bin/bash
###############################################################################
# IAFactory Quick Command
###############################################################################

COMMAND=${1:-help}

case $COMMAND in
    start)
        echo "🚀 Démarrage des services IAFactory..."
        cd /opt/iafactory && docker-compose up -d
        ;;
    stop)
        echo "🛑 Arrêt des services IAFactory..."
        cd /opt/iafactory && docker-compose stop
        ;;
    restart)
        echo "🔄 Redémarrage des services IAFactory..."
        cd /opt/iafactory && docker-compose restart
        ;;
    status)
        /usr/local/bin/iafactory-health.sh
        ;;
    logs)
        cd /opt/iafactory && docker-compose logs -f --tail=100 ${2:-}
        ;;
    backup)
        /usr/local/bin/iafactory-backup.sh
        ;;
    restore)
        /usr/local/bin/iafactory-restore.sh
        ;;
    maintenance)
        /usr/local/bin/iafactory-maintenance.sh
        ;;
    update)
        echo "📦 Mise à jour de IAFactory..."
        cd /opt/iafactory
        git pull
        docker-compose pull
        docker-compose up -d --build
        ;;
    help|*)
        echo "IAFactory RAG-DZ - Commandes Rapides"
        echo ""
        echo "Usage: iafactory <command>"
        echo ""
        echo "Commandes disponibles:"
        echo "  start        - Démarrer tous les services"
        echo "  stop         - Arrêter tous les services"
        echo "  restart      - Redémarrer tous les services"
        echo "  status       - Vérifier l'état des services"
        echo "  logs [svc]   - Voir les logs (optionnel: nom du service)"
        echo "  backup       - Créer un backup"
        echo "  restore      - Restaurer depuis un backup"
        echo "  maintenance  - Exécuter la maintenance"
        echo "  update       - Mettre à jour l'application"
        echo "  help         - Afficher cette aide"
        ;;
esac
EOF

    chmod +x /usr/local/bin/iafactory
    log_success "Commande rapide 'iafactory' créée"

    # Afficher le résumé
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    log_success "Monitoring et Backups Configurés!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "📋 Scripts créés:"
    echo "   /usr/local/bin/iafactory              - Commande rapide"
    echo "   /usr/local/bin/iafactory-health.sh    - Health check"
    echo "   /usr/local/bin/iafactory-backup.sh    - Backup"
    echo "   /usr/local/bin/iafactory-restore.sh   - Restauration"
    echo "   /usr/local/bin/iafactory-alerts.sh    - Alertes"
    echo "   /usr/local/bin/iafactory-maintenance.sh - Maintenance"
    echo ""
    echo "⏰ Tâches planifiées (cron):"
    echo "   02:00 - Backup quotidien"
    echo "   03:00 - Maintenance hebdomadaire (dimanche)"
    echo "   03:30 - Renouvellement SSL"
    echo "   */5   - Alertes (toutes les 5 minutes)"
    echo ""
    echo "📁 Répertoires:"
    echo "   Backups: $BACKUP_DIR"
    echo "   Logs:    $LOG_DIR"
    echo ""
    echo "🚀 Commandes rapides:"
    echo "   iafactory status      - État des services"
    echo "   iafactory logs        - Voir les logs"
    echo "   iafactory backup      - Créer un backup"
    echo "   iafactory help        - Aide complète"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

# Exécution
main "$@"
