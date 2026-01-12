#!/bin/bash
set -e

# =============================================================================
# IAFactory Video Platform - Backup Script
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_ROOT/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Create backup directory
mkdir -p "$BACKUP_DIR"

backup_database() {
    log_info "Backing up PostgreSQL database..."

    BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

    docker-compose exec -T postgres pg_dump -U postgres iafactory_video | gzip > "$BACKUP_FILE"

    log_info "Database backup saved to: $BACKUP_FILE"
}

backup_minio() {
    log_info "Backing up MinIO data..."

    BACKUP_FILE="$BACKUP_DIR/minio_backup_$TIMESTAMP.tar.gz"

    # Use mc (MinIO Client) if available, otherwise tar the volume
    if command -v mc &> /dev/null; then
        mc mirror local/video-platform-assets "$BACKUP_DIR/minio_$TIMESTAMP/" --overwrite
        tar -czf "$BACKUP_FILE" -C "$BACKUP_DIR" "minio_$TIMESTAMP"
        rm -rf "$BACKUP_DIR/minio_$TIMESTAMP"
    else
        # Backup Docker volume directly
        docker run --rm \
            -v iafactory-video-platform_minio_data:/data \
            -v "$BACKUP_DIR:/backup" \
            alpine tar -czf /backup/minio_backup_$TIMESTAMP.tar.gz -C /data .
    fi

    log_info "MinIO backup saved to: $BACKUP_FILE"
}

backup_redis() {
    log_info "Backing up Redis data..."

    BACKUP_FILE="$BACKUP_DIR/redis_backup_$TIMESTAMP.rdb"

    # Trigger Redis save
    docker-compose exec -T redis redis-cli BGSAVE

    sleep 2

    # Copy dump file
    docker cp $(docker-compose ps -q redis):/data/dump.rdb "$BACKUP_FILE" 2>/dev/null || \
        log_warn "No Redis dump file found (may be empty)"

    log_info "Redis backup saved to: $BACKUP_FILE"
}

backup_env() {
    log_info "Backing up environment configuration..."

    BACKUP_FILE="$BACKUP_DIR/env_backup_$TIMESTAMP.tar.gz"

    tar -czf "$BACKUP_FILE" \
        -C "$PROJECT_ROOT" \
        .env \
        docker-compose.yml \
        docker-compose.prod.yml \
        2>/dev/null || log_warn "Some config files not found"

    log_info "Environment backup saved to: $BACKUP_FILE"
}

cleanup_old_backups() {
    log_info "Cleaning up old backups (keeping last 7 days)..."

    find "$BACKUP_DIR" -type f -mtime +7 -delete

    log_info "Cleanup completed"
}

# Main
main() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  IAFactory Video Platform - Backup"
    echo "  Timestamp: $TIMESTAMP"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    backup_database
    backup_minio
    backup_redis
    backup_env
    cleanup_old_backups

    echo ""
    log_info "All backups completed!"
    echo ""
    echo "Backup files:"
    ls -lh "$BACKUP_DIR"/*$TIMESTAMP* 2>/dev/null || echo "  No files found"
    echo ""
}

main
