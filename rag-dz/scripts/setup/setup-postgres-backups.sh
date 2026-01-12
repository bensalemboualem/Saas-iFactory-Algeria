#!/bin/bash
# ================================================================
# CONFIGURATION BACKUPS POSTGRESQL AUTOMATIQUES
# IAFactory Algeria - Production
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "💾 CONFIGURATION BACKUPS POSTGRESQL AUTOMATIQUES"
echo "================================================================"
echo ""

# ================================================================
# CONFIGURATION
# ================================================================

BACKUP_DIR="/opt/backups/postgresql"
BACKUP_RETENTION_DAYS=30
POSTGRES_CONTAINER="iaf-postgres-prod"
POSTGRES_USER="postgres"
POSTGRES_DB="iafactory_dz"

echo -e "${BLUE}Configuration:${NC}"
echo "  • Répertoire backups: $BACKUP_DIR"
echo "  • Rétention: $BACKUP_RETENTION_DAYS jours"
echo "  • Container: $POSTGRES_CONTAINER"
echo "  • Base de données: $POSTGRES_DB"
echo ""

# ================================================================
# ÉTAPE 1: CRÉATION STRUCTURE
# ================================================================

echo -e "${BLUE}[1/6]${NC} Création de la structure de backups..."

mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR/daily"
mkdir -p "$BACKUP_DIR/weekly"
mkdir -p "$BACKUP_DIR/monthly"
mkdir -p /var/log/backups

echo -e "${GREEN}✅ Structure créée${NC}"
echo ""

# ================================================================
# ÉTAPE 2: SCRIPT BACKUP QUOTIDIEN
# ================================================================

echo -e "${BLUE}[2/6]${NC} Création du script de backup quotidien..."

cat > /usr/local/bin/postgres-backup-daily.sh << 'BACKUPSCRIPT'
#!/bin/bash
# Backup quotidien PostgreSQL - IAFactory Algeria

set -e

# Configuration
BACKUP_DIR="/opt/backups/postgresql/daily"
LOG_FILE="/var/log/backups/postgres-daily.log"
DATE=$(date +%Y%m%d_%H%M%S)
DAY_OF_WEEK=$(date +%u)
DAY_OF_MONTH=$(date +%d)
RETENTION_DAYS=30
POSTGRES_CONTAINER="iaf-postgres-prod"

# Logging
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "================================================================"
echo "PostgreSQL Backup - $(date)"
echo "================================================================"

# Vérifier que le container tourne
if ! docker ps | grep -q "$POSTGRES_CONTAINER"; then
    echo "❌ ERREUR: Container $POSTGRES_CONTAINER non trouvé"
    exit 1
fi

# Backup complet (pg_dumpall)
echo "📦 Création backup complet..."
BACKUP_FILE="$BACKUP_DIR/postgres_all_${DATE}.sql.gz"

if docker exec "$POSTGRES_CONTAINER" pg_dumpall -U postgres | gzip > "$BACKUP_FILE"; then
    SIZE=$(du -h "$BACKUP_FILE" | awk '{print $1}')
    echo "✅ Backup créé: $BACKUP_FILE ($SIZE)"
else
    echo "❌ ERREUR: Backup échoué"
    exit 1
fi

# Backup base spécifique
echo "📦 Création backup base iafactory_dz..."
BACKUP_DB_FILE="$BACKUP_DIR/iafactory_dz_${DATE}.sql.gz"

if docker exec "$POSTGRES_CONTAINER" pg_dump -U postgres iafactory_dz | gzip > "$BACKUP_DB_FILE"; then
    SIZE=$(du -h "$BACKUP_DB_FILE" | awk '{print $1}')
    echo "✅ Backup DB créé: $BACKUP_DB_FILE ($SIZE)"
fi

# Copie hebdomadaire (dimanche)
if [ "$DAY_OF_WEEK" = "7" ]; then
    echo "📅 Copie hebdomadaire (dimanche)..."
    cp "$BACKUP_FILE" "/opt/backups/postgresql/weekly/postgres_weekly_$(date +%Y_W%V).sql.gz"
    echo "✅ Backup hebdomadaire créé"
fi

# Copie mensuelle (1er du mois)
if [ "$DAY_OF_MONTH" = "01" ]; then
    echo "📅 Copie mensuelle (1er du mois)..."
    cp "$BACKUP_FILE" "/opt/backups/postgresql/monthly/postgres_monthly_$(date +%Y_%m).sql.gz"
    echo "✅ Backup mensuel créé"
fi

# Nettoyage anciens backups quotidiens
echo "🧹 Nettoyage anciens backups (> $RETENTION_DAYS jours)..."
find "$BACKUP_DIR" -name "postgres_*.sql.gz" -mtime +$RETENTION_DAYS -delete
DELETED=$(find "$BACKUP_DIR" -name "postgres_*.sql.gz" -mtime +$RETENTION_DAYS 2>/dev/null | wc -l)
echo "✅ $DELETED fichiers supprimés"

# Nettoyage hebdomadaires (garder 12 semaines)
find /opt/backups/postgresql/weekly -name "postgres_weekly_*.sql.gz" -mtime +84 -delete

# Nettoyage mensuels (garder 12 mois)
find /opt/backups/postgresql/monthly -name "postgres_monthly_*.sql.gz" -mtime +365 -delete

# Résumé
echo ""
echo "📊 Résumé backups:"
echo "  • Quotidiens: $(ls -1 $BACKUP_DIR/postgres_*.sql.gz 2>/dev/null | wc -l) fichiers"
echo "  • Hebdomadaires: $(ls -1 /opt/backups/postgresql/weekly/*.sql.gz 2>/dev/null | wc -l) fichiers"
echo "  • Mensuels: $(ls -1 /opt/backups/postgresql/monthly/*.sql.gz 2>/dev/null | wc -l) fichiers"
echo "  • Espace total: $(du -sh /opt/backups/postgresql | awk '{print $1}')"
echo ""
echo "✅ Backup terminé avec succès"
echo "================================================================"
BACKUPSCRIPT

chmod +x /usr/local/bin/postgres-backup-daily.sh

echo -e "${GREEN}✅ Script créé: /usr/local/bin/postgres-backup-daily.sh${NC}"
echo ""

# ================================================================
# ÉTAPE 3: TEST BACKUP
# ================================================================

echo -e "${BLUE}[3/6]${NC} Test du backup..."
echo ""

if /usr/local/bin/postgres-backup-daily.sh; then
    echo -e "${GREEN}✅ Test backup réussi${NC}"
else
    echo -e "${RED}❌ Test backup échoué${NC}"
    exit 1
fi

echo ""

# ================================================================
# ÉTAPE 4: CRON JOB
# ================================================================

echo -e "${BLUE}[4/6]${NC} Configuration cron job..."

# Backup à 2h du matin chaque jour
CRON_LINE="0 2 * * * /usr/local/bin/postgres-backup-daily.sh >> /var/log/backups/postgres-cron.log 2>&1"

# Vérifier si déjà présent
if crontab -l 2>/dev/null | grep -q "postgres-backup-daily.sh"; then
    echo -e "${YELLOW}⚠️  Cron job déjà configuré${NC}"
else
    # Ajouter au crontab
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo -e "${GREEN}✅ Cron job ajouté${NC}"
fi

echo "  • Horaire: Tous les jours à 2h00 du matin"
echo ""

# ================================================================
# ÉTAPE 5: SCRIPT RESTORE
# ================================================================

echo -e "${BLUE}[5/6]${NC} Création du script de restauration..."

cat > /usr/local/bin/postgres-restore.sh << 'RESTORESCRIPT'
#!/bin/bash
# Restauration PostgreSQL - IAFactory Algeria

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup-file.sql.gz>"
    echo ""
    echo "Exemples:"
    echo "  $0 /opt/backups/postgresql/daily/postgres_all_20251204_020000.sql.gz"
    echo "  $0 /opt/backups/postgresql/weekly/postgres_weekly_2025_W49.sql.gz"
    echo ""
    echo "Backups disponibles:"
    echo ""
    echo "Quotidiens (derniers 7):"
    ls -lht /opt/backups/postgresql/daily/*.sql.gz 2>/dev/null | head -7 || echo "  Aucun"
    echo ""
    echo "Hebdomadaires:"
    ls -lht /opt/backups/postgresql/weekly/*.sql.gz 2>/dev/null | head -5 || echo "  Aucun"
    echo ""
    echo "Mensuels:"
    ls -lht /opt/backups/postgresql/monthly/*.sql.gz 2>/dev/null | head -5 || echo "  Aucun"
    exit 1
fi

BACKUP_FILE="$1"
POSTGRES_CONTAINER="iaf-postgres-prod"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ ERREUR: Fichier non trouvé: $BACKUP_FILE"
    exit 1
fi

echo "================================================================"
echo "⚠️  RESTAURATION POSTGRESQL"
echo "================================================================"
echo ""
echo "Fichier: $BACKUP_FILE"
echo "Taille: $(du -h "$BACKUP_FILE" | awk '{print $1}')"
echo ""
echo "⚠️  ATTENTION: Cette opération va ÉCRASER toutes les données actuelles!"
echo ""
read -p "Êtes-vous sûr? Tapez 'RESTORE' pour confirmer: " CONFIRM

if [ "$CONFIRM" != "RESTORE" ]; then
    echo "❌ Restauration annulée"
    exit 1
fi

echo ""
echo "📦 Décompression et restauration..."

if zcat "$BACKUP_FILE" | docker exec -i "$POSTGRES_CONTAINER" psql -U postgres; then
    echo ""
    echo "✅ Restauration terminée avec succès"
    echo ""
    echo "🔄 Redémarrage des services..."
    cd /opt/iafactory-rag-dz
    docker-compose restart iaf-backend-prod
    echo "✅ Services redémarrés"
else
    echo "❌ ERREUR: Restauration échouée"
    exit 1
fi

echo ""
echo "================================================================"
RESTORESCRIPT

chmod +x /usr/local/bin/postgres-restore.sh

echo -e "${GREEN}✅ Script créé: /usr/local/bin/postgres-restore.sh${NC}"
echo ""

# ================================================================
# ÉTAPE 6: MONITORING BACKUPS
# ================================================================

echo -e "${BLUE}[6/6]${NC} Configuration monitoring backups..."

cat > /usr/local/bin/postgres-backup-check.sh << 'CHECKSCRIPT'
#!/bin/bash
# Vérification backups PostgreSQL

BACKUP_DIR="/opt/backups/postgresql/daily"
MAX_AGE_HOURS=26

# Trouver le backup le plus récent
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/postgres_all_*.sql.gz 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ CRITIQUE: Aucun backup trouvé"
    exit 2
fi

# Vérifier l'âge
AGE_SECONDS=$(( $(date +%s) - $(stat -c %Y "$LATEST_BACKUP") ))
AGE_HOURS=$(( AGE_SECONDS / 3600 ))

echo "📊 Status backups PostgreSQL:"
echo "  • Dernier backup: $LATEST_BACKUP"
echo "  • Âge: $AGE_HOURS heures"
echo "  • Taille: $(du -h "$LATEST_BACKUP" | awk '{print $1}')"

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
    echo "❌ ALERTE: Dernier backup trop ancien (> $MAX_AGE_HOURS heures)"
    exit 1
else
    echo "✅ Backups OK"
    exit 0
fi
CHECKSCRIPT

chmod +x /usr/local/bin/postgres-backup-check.sh

echo -e "${GREEN}✅ Script monitoring créé${NC}"
echo ""

# ================================================================
# RÉSUMÉ
# ================================================================

echo "================================================================"
echo -e "${GREEN}✅ CONFIGURATION BACKUPS TERMINÉE${NC}"
echo "================================================================"
echo ""

echo "📋 RÉSUMÉ:"
echo ""
echo "Structure:"
echo "  • /opt/backups/postgresql/daily/     - Backups quotidiens (30 jours)"
echo "  • /opt/backups/postgresql/weekly/    - Backups hebdomadaires (12 semaines)"
echo "  • /opt/backups/postgresql/monthly/   - Backups mensuels (12 mois)"
echo ""

echo "Scripts créés:"
echo "  • /usr/local/bin/postgres-backup-daily.sh   - Backup automatique"
echo "  • /usr/local/bin/postgres-restore.sh        - Restauration"
echo "  • /usr/local/bin/postgres-backup-check.sh   - Vérification"
echo ""

echo "Cron job:"
echo "  • Tous les jours à 2h00 du matin"
echo "  • Logs: /var/log/backups/postgres-daily.log"
echo ""

echo "Backups actuels:"
ls -lh /opt/backups/postgresql/daily/*.sql.gz 2>/dev/null | tail -5 || echo "  (premier backup créé)"
echo ""

echo "Espace utilisé:"
du -sh /opt/backups/postgresql
echo ""

echo "🔧 COMMANDES UTILES:"
echo ""
echo "Backup manuel:"
echo "  /usr/local/bin/postgres-backup-daily.sh"
echo ""
echo "Restaurer un backup:"
echo "  /usr/local/bin/postgres-restore.sh <fichier.sql.gz>"
echo ""
echo "Vérifier backups:"
echo "  /usr/local/bin/postgres-backup-check.sh"
echo ""
echo "Voir les backups:"
echo "  ls -lht /opt/backups/postgresql/daily/"
echo "  ls -lht /opt/backups/postgresql/weekly/"
echo "  ls -lht /opt/backups/postgresql/monthly/"
echo ""
echo "Logs:"
echo "  tail -f /var/log/backups/postgres-daily.log"
echo ""

echo "================================================================"
echo "✅ Backups PostgreSQL configurés avec succès!"
echo "================================================================"
echo ""
