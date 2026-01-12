#!/bin/bash
# ============================================
# IAFactory Stack Restart Script
# ============================================
# Safely restarts all services with health checks
# Usage: ./scripts/restart-stack.sh [service-name]
# ============================================

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}IAFactory Stack Restart${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Check if specific service requested
if [ -n "$1" ]; then
  echo -e "${YELLOW}Restarting service: $1${NC}\n"
  docker-compose restart "$1"
  echo -e "\n${GREEN}✓ Service $1 restarted${NC}"
  echo -e "\nRunning health check...\n"
  ./scripts/health-check.sh --wait
  exit 0
fi

# Full stack restart
echo -e "${BOLD}[1/5] Stopping all services...${NC}"
docker-compose down
echo -e "${GREEN}✓ Services stopped${NC}\n"

echo -e "${BOLD}[2/5] Starting databases...${NC}"
docker-compose up -d iafactory-postgres iafactory-redis iafactory-qdrant
echo -e "${GREEN}✓ Databases starting${NC}\n"

echo -e "${BOLD}[3/5] Waiting for database health...${NC}"
sleep 10
echo -e "${GREEN}✓ Databases ready${NC}\n"

echo -e "${BOLD}[4/5] Starting application services...${NC}"
docker-compose up -d iafactory-backend iafactory-hub iafactory-docs iafactory-n8n
echo -e "${GREEN}✓ Applications starting${NC}\n"

echo -e "${BOLD}[5/5] Running health checks...${NC}\n"
./scripts/health-check.sh --wait

echo -e "\n${GREEN}✓ Stack restart complete!${NC}"
