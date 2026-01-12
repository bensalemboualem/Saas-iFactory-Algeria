#!/bin/bash
# ============================================
# IAFactory Database Backup Script
# ============================================
# Creates timestamped backups of PostgreSQL
# Usage: ./scripts/db-backup.sh [backup-name]
# ============================================

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME=${1:-"backup_${TIMESTAMP}"}
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.sql"

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}IAFactory Database Backup${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Check if container is running
if ! docker ps | grep -q "iaf-dz-postgres"; then
  echo -e "${YELLOW}⚠ PostgreSQL container not running!${NC}"
  exit 1
fi

echo -e "${BOLD}Creating backup: ${GREEN}${BACKUP_NAME}${NC}"
docker exec iaf-dz-postgres pg_dump -U postgres iafactory_dz > "$BACKUP_FILE"

# Compress backup
echo -e "\n${BOLD}Compressing backup...${NC}"
gzip -f "$BACKUP_FILE"

BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
echo -e "${GREEN}✓ Backup created: ${BACKUP_FILE}.gz (${BACKUP_SIZE})${NC}"

# List recent backups
echo -e "\n${BOLD}Recent backups:${NC}"
ls -lh "$BACKUP_DIR" | tail -5

echo -e "\n${BOLD}Restore command:${NC}"
echo -e "  gunzip < ${BACKUP_FILE}.gz | docker exec -i iaf-dz-postgres psql -U postgres iafactory_dz"
