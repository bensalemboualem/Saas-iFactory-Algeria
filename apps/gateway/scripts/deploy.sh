#!/bin/bash
# IAFactory Gateway - Production Deployment Script
# Usage: ./scripts/deploy.sh [--migrate] [--rebuild]
#
# Options:
#   --migrate   Run database migrations
#   --rebuild   Force rebuild of Docker images
#   --logs      Show logs after deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.prod.yml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
MIGRATE=false
REBUILD=false
SHOW_LOGS=false

for arg in "$@"; do
    case $arg in
        --migrate)
            MIGRATE=true
            ;;
        --rebuild)
            REBUILD=true
            ;;
        --logs)
            SHOW_LOGS=true
            ;;
        *)
            echo -e "${RED}Unknown option: $arg${NC}"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  IAFactory Gateway - Production Deploy ${NC}"
echo -e "${GREEN}========================================${NC}"

# Check .env file exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    exit 1
fi

# Check required env vars
source "$PROJECT_DIR/.env"
REQUIRED_VARS=("POSTGRES_PASSWORD" "JWT_SECRET" "ADMIN_API_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}ERROR: Required variable $var is not set in .env${NC}"
        exit 1
    fi
done

cd "$PROJECT_DIR"

# Pull latest code (if git repo)
if [ -d ".git" ]; then
    echo -e "${YELLOW}[1/6] Pulling latest code...${NC}"
    git pull origin main || git pull origin master || true
fi

# Build images
if [ "$REBUILD" = true ]; then
    echo -e "${YELLOW}[2/6] Rebuilding Docker images (forced)...${NC}"
    docker compose -f "$COMPOSE_FILE" build --no-cache
else
    echo -e "${YELLOW}[2/6] Building Docker images...${NC}"
    docker compose -f "$COMPOSE_FILE" build
fi

# Stop existing containers
echo -e "${YELLOW}[3/6] Stopping existing containers...${NC}"
docker compose -f "$COMPOSE_FILE" down --remove-orphans

# Start new containers
echo -e "${YELLOW}[4/6] Starting containers...${NC}"
docker compose -f "$COMPOSE_FILE" up -d

# Wait for gateway to be healthy
echo -e "${YELLOW}[5/6] Waiting for gateway to be healthy...${NC}"
RETRIES=30
until docker compose -f "$COMPOSE_FILE" exec -T gateway wget -q --spider http://localhost:3001/health 2>/dev/null; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -le 0 ]; then
        echo -e "${RED}ERROR: Gateway failed to start!${NC}"
        docker compose -f "$COMPOSE_FILE" logs gateway
        exit 1
    fi
    echo "Waiting for gateway... ($RETRIES attempts left)"
    sleep 2
done

# Run migrations if requested
if [ "$MIGRATE" = true ]; then
    echo -e "${YELLOW}[6/6] Running database migrations...${NC}"
    docker compose -f "$COMPOSE_FILE" exec -T gateway pnpm prisma migrate deploy
    docker compose -f "$COMPOSE_FILE" exec -T gateway pnpm prisma generate
else
    echo -e "${YELLOW}[6/6] Skipping migrations (use --migrate to run)${NC}"
fi

# Verify deployment
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Show container status
docker compose -f "$COMPOSE_FILE" ps

# Health check
echo ""
echo -e "${YELLOW}Health check:${NC}"
curl -s http://localhost:3001/health | head -c 200
echo ""

# Show logs if requested
if [ "$SHOW_LOGS" = true ]; then
    echo ""
    echo -e "${YELLOW}Recent logs:${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=50 gateway
fi

echo ""
echo -e "${GREEN}Useful commands:${NC}"
echo "  View logs:     docker compose -f docker-compose.prod.yml logs -f"
echo "  Gateway logs:  docker compose -f docker-compose.prod.yml logs -f gateway"
echo "  Restart:       docker compose -f docker-compose.prod.yml restart"
echo "  Stop:          docker compose -f docker-compose.prod.yml down"
echo "  DB shell:      docker compose -f docker-compose.prod.yml exec postgres psql -U iafactory"
echo "  Run migration: docker compose -f docker-compose.prod.yml exec gateway pnpm prisma migrate deploy"
