#!/bin/bash
# ============================================
# IAFactory Full Rebuild Script
# ============================================
# Complete rebuild of all Docker images
# Usage: ./scripts/rebuild-all.sh [--no-cache]
# ============================================

set -e

NO_CACHE=""
if [[ "$1" == "--no-cache" ]]; then
  NO_CACHE="--no-cache"
fi

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}IAFactory Full Rebuild${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Confirm rebuild
echo -e "${YELLOW}⚠ This will rebuild all Docker images.${NC}"
echo -e "${YELLOW}⚠ This may take 10-15 minutes.${NC}\n"
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 1
fi

echo -e "\n${BOLD}[1/6] Stopping all services...${NC}"
docker-compose down
echo -e "${GREEN}✓ Services stopped${NC}\n"

echo -e "${BOLD}[2/6] Removing old images...${NC}"
docker-compose rm -f
echo -e "${GREEN}✓ Containers removed${NC}\n"

echo -e "${BOLD}[3/6] Building backend...${NC}"
docker-compose build $NO_CACHE iafactory-backend
echo -e "${GREEN}✓ Backend built${NC}\n"

echo -e "${BOLD}[4/6] Building frontends...${NC}"
docker-compose build $NO_CACHE iafactory-hub iafactory-docs
echo -e "${GREEN}✓ Frontends built${NC}\n"

echo -e "${BOLD}[5/6] Starting all services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services starting${NC}\n"

echo -e "${BOLD}[6/6] Running health checks...${NC}\n"
sleep 15
./scripts/health-check.sh --wait

echo -e "\n${GREEN}✓ Rebuild complete!${NC}"
echo -e "\n${BOLD}Service URLs:${NC}"
echo -e "  Backend:  http://localhost:8180/docs"
echo -e "  Hub:      http://localhost:8182"
echo -e "  Docs:     http://localhost:8183"
echo -e "  n8n:      http://localhost:8185"
