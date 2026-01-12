#!/usr/bin/env bash
# ==============================================
# IAFactory RAG-DZ - Script de Backup Automatique
# ==============================================
# Sauvegarde PostgreSQL, Redis, volumes Docker
# Compression et upload vers S3 (optionnel)
# ==============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/var/backups/iafactory}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y-%m-%d)

# Docker containers
POSTGRES_CONTAINER="iaf-dz-postgres"
REDIS_CONTAINER="iaf-dz-redis"

# S3 Configuration (optionnel)
S3_ENABLED="${S3_ENABLED:-false}"
S3_BUCKET="${S3_BUCKET:-iafactory-backups-dz}"
AWS_REGION="${AWS_REGION:-eu-central-1}"

# Notification (optionnel)
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
EMAIL_TO="${EMAIL_TO:-admin@iafactoryalgeria.com}"

echo -e "${BLUE}==============================================\${NC}"
echo -e "${CYAN}💾 IAFactory RAG-DZ - Backup${NC}"
echo -e "${CYAN}Date: $(date)${NC}"
echo -e "${BLUE}==============================================\${NC}"

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR/$DATE"

# Fonction: Notification Slack
notify_slack() {
    local message=$1
    local status=$2

    if [ -n "$SLACK_WEBHOOK" ]; then
        local color="good"
        [ "$status" == "error" ] && color="danger"
        [ "$status" == "warning" ] && color="warning"

        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"$message\",\"color\":\"$color\"}" \
            "$SLACK_WEBHOOK" 2>/dev/null || true
    fi
}

# Fonction: Notification Email
notify_email() {
    local subject=$1
    local body=$2

    if command -v mail &> /dev/null && [ -n "$EMAIL_TO" ]; then
        echo "$body" | mail -s "$subject" "$EMAIL_TO" || true
    fi
}

# Fonction: Backup PostgreSQL
backup_postgres() {
    echo -e "${YELLOW}📊 Backup PostgreSQL...${NC}"

    if ! docker ps | grep -q "$POSTGRES_CONTAINER"; then
        echo -e "${RED}❌ Container PostgreSQL non trouvé: $POSTGRES_CONTAINER${NC}"
        return 1
    fi

    local backup_file="$BACKUP_DIR/$DATE/postgres_${TIMESTAMP}.sql.gz"

    # Dump de la base de données
    docker exec "$POSTGRES_CONTAINER" pg_dumpall -U postgres | gzip > "$backup_file"

    if [ -f "$backup_file" ]; then
        local size=$(du -h "$backup_file" | cut -f1)
        echo -e "${GREEN}✅ PostgreSQL sauvegardé: $backup_file ($size)${NC}"
        return 0
    else
        echo -e "${RED}❌ Échec du backup PostgreSQL${NC}"
        return 1
    fi
}

# Fonction: Backup Redis
backup_redis() {
    echo -e "${YELLOW}📊 Backup Redis...${NC}"

    if ! docker ps | grep -q "$REDIS_CONTAINER"; then
        echo -e "${RED}❌ Container Redis non trouvé: $REDIS_CONTAINER${NC}"
        return 1
    fi

    local backup_file="$BACKUP_DIR/$DATE/redis_${TIMESTAMP}.rdb"

    # Forcer la sauvegarde Redis
    docker exec "$REDIS_CONTAINER" redis-cli BGSAVE || true
    sleep 2

    # Copier le fichier dump.rdb
    docker cp "$REDIS_CONTAINER:/data/dump.rdb" "$backup_file" 2>/dev/null || true

    if [ -f "$backup_file" ]; then
        gzip "$backup_file"
        local size=$(du -h "$backup_file.gz" | cut -f1)
        echo -e "${GREEN}✅ Redis sauvegardé: $backup_file.gz ($size)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Backup Redis ignoré (pas de dump.rdb)${NC}"
        return 0
    fi
}

# Fonction: Backup volumes Docker
backup_docker_volumes() {
    echo -e "${YELLOW}📦 Backup volumes Docker...${NC}"

    local volumes=(
        "iaf-dz-postgres-data"
        "iaf-dz-redis-data"
        "iaf-dz-qdrant-data"
        "iaf-dz-backend-cache"
        "iaf-dz-n8n-data"
    )

    for volume in "${volumes[@]}"; do
        if docker volume ls | grep -q "$volume"; then
            local backup_file="$BACKUP_DIR/$DATE/volume_${volume}_${TIMESTAMP}.tar.gz"

            echo -e "${YELLOW}  • Sauvegarde volume: $volume${NC}"

            # Créer un container temporaire pour sauvegarder le volume
            docker run --rm \
                -v "$volume:/data" \
                -v "$BACKUP_DIR/$DATE:/backup" \
                alpine \
                tar czf "/backup/volume_${volume}_${TIMESTAMP}.tar.gz" -C /data .

            if [ -f "$backup_file" ]; then
                local size=$(du -h "$backup_file" | cut -f1)
                echo -e "${GREEN}    ✅ $volume ($size)${NC}"
            fi
        fi
    done

    echo -e "${GREEN}✅ Volumes Docker sauvegardés${NC}"
}

# Fonction: Backup fichiers de configuration
backup_config() {
    echo -e "${YELLOW}⚙️  Backup configuration...${NC}"

    local backup_file="$BACKUP_DIR/$DATE/config_${TIMESTAMP}.tar.gz"

    # Fichiers à sauvegarder
    local config_files=(
        "/opt/iafactory/.env.production"
        "/opt/iafactory/docker-compose.yml"
        "/opt/iafactory/nginx/nginx.conf"
        "/etc/nginx/nginx.conf"
        "/etc/letsencrypt"
    )

    # Créer une archive
    tar czf "$backup_file" \
        -C / \
        --ignore-failed-read \
        $(printf " %s" "${config_files[@]}") 2>/dev/null || true

    if [ -f "$backup_file" ]; then
        local size=$(du -h "$backup_file" | cut -f1)
        echo -e "${GREEN}✅ Configuration sauvegardée: $backup_file ($size)${NC}"
    fi
}

# Fonction: Upload vers S3
upload_to_s3() {
    if [ "$S3_ENABLED" != "true" ]; then
        echo -e "${YELLOW}⏭️  Upload S3 désactivé${NC}"
        return
    fi

    echo -e "${YELLOW}☁️  Upload vers S3...${NC}"

    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI non installé${NC}"
        return 1
    fi

    # Upload du répertoire de backup
    aws s3 sync "$BACKUP_DIR/$DATE" "s3://$S3_BUCKET/$DATE/" \
        --region "$AWS_REGION" \
        --storage-class STANDARD_IA

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backups uploadés vers S3: s3://$S3_BUCKET/$DATE/${NC}"
    else
        echo -e "${RED}❌ Échec de l'upload S3${NC}"
        return 1
    fi
}

# Fonction: Nettoyage des anciens backups
cleanup_old_backups() {
    echo -e "${YELLOW}🧹 Nettoyage des anciens backups...${NC}"

    # Supprimer les backups locaux de plus de RETENTION_DAYS jours
    find "$BACKUP_DIR" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} + 2>/dev/null || true

    # Supprimer les backups S3 (si activé)
    if [ "$S3_ENABLED" == "true" ] && command -v aws &> /dev/null; then
        local cutoff_date=$(date -d "$RETENTION_DAYS days ago" +%Y-%m-%d 2>/dev/null || date -v -${RETENTION_DAYS}d +%Y-%m-%d)

        aws s3 ls "s3://$S3_BUCKET/" --region "$AWS_REGION" | while read -r line; do
            local date_folder=$(echo "$line" | awk '{print $2}' | tr -d '/')
            if [[ "$date_folder" < "$cutoff_date" ]]; then
                echo -e "${YELLOW}  • Suppression S3: $date_folder${NC}"
                aws s3 rm "s3://$S3_BUCKET/$date_folder/" --recursive --region "$AWS_REGION" || true
            fi
        done
    fi

    echo -e "${GREEN}✅ Nettoyage terminé (rétention: $RETENTION_DAYS jours)${NC}"
}

# Fonction: Calcul de la taille totale
calculate_total_size() {
    local total_size=$(du -sh "$BACKUP_DIR/$DATE" 2>/dev/null | cut -f1 || echo "0")
    echo -e "${CYAN}📊 Taille totale: $total_size${NC}"
}

# Fonction: Génération du rapport
generate_report() {
    local status=$1
    local duration=$2

    local report_file="$BACKUP_DIR/$DATE/backup_report_${TIMESTAMP}.txt"

    cat > "$report_file" << EOF
IAFactory RAG-DZ - Rapport de Backup
=====================================

Date: $(date)
Status: $status
Durée: ${duration}s
Répertoire: $BACKUP_DIR/$DATE

Fichiers sauvegardés:
$(ls -lh "$BACKUP_DIR/$DATE" 2>/dev/null || echo "Aucun fichier")

Taille totale: $(du -sh "$BACKUP_DIR/$DATE" 2>/dev/null | cut -f1 || echo "0")

Volumes Docker:
$(docker volume ls | grep iaf-dz || echo "Aucun volume")

S3 Upload: $([ "$S3_ENABLED" == "true" ] && echo "Activé" || echo "Désactivé")

=====================================
EOF

    echo -e "${GREEN}✅ Rapport généré: $report_file${NC}"

    # Afficher le rapport
    cat "$report_file"
}

# ==============================================
# EXÉCUTION PRINCIPALE
# ==============================================

main() {
    local start_time=$(date +%s)
    local status="SUCCESS"
    local error_count=0

    # Backup PostgreSQL
    if ! backup_postgres; then
        ((error_count++))
        status="PARTIAL_SUCCESS"
    fi

    # Backup Redis
    if ! backup_redis; then
        ((error_count++))
        status="PARTIAL_SUCCESS"
    fi

    # Backup volumes Docker
    backup_docker_volumes || ((error_count++))

    # Backup configuration
    backup_config || ((error_count++))

    # Upload vers S3
    if ! upload_to_s3; then
        ((error_count++))
        status="PARTIAL_SUCCESS"
    fi

    # Nettoyage
    cleanup_old_backups

    # Calculer la durée
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # Taille totale
    calculate_total_size

    # Générer le rapport
    generate_report "$status" "$duration"

    # Notifications
    if [ $error_count -eq 0 ]; then
        echo -e "${GREEN}✅ Backup terminé avec succès !${NC}"
        notify_slack "✅ Backup IAFactory réussi ($duration secondes)" "good"
        notify_email "✅ Backup IAFactory réussi" "Backup terminé avec succès en $duration secondes"
    else
        echo -e "${YELLOW}⚠️  Backup terminé avec $error_count erreur(s)${NC}"
        notify_slack "⚠️ Backup IAFactory partiellement réussi ($error_count erreurs)" "warning"
        notify_email "⚠️ Backup IAFactory partiellement réussi" "Backup terminé avec $error_count erreur(s)"
    fi

    echo -e "${BLUE}==============================================\${NC}"
}

# Vérifier si root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    exit 1
fi

# Lancer le backup
main

# Log
echo "[$(date)] Backup IAFactory terminé" >> /var/log/iafactory-backup.log
