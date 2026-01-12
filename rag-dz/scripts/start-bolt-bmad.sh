#!/bin/bash
# ============================================
# Start Bolt.diy + BMAD Stack (Local Docker)
# ============================================
# Usage: ./scripts/start-bolt-bmad.sh [--dev|--prod]
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$PROJECT_ROOT/infrastructure/docker"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Bolt.diy + BMAD Stack Launcher${NC}"
echo -e "${GREEN}========================================${NC}"

# Parse arguments
MODE="prod"
if [[ "$1" == "--dev" ]]; then
    MODE="dev"
fi

# Check for required env file
if [[ ! -f "$PROJECT_ROOT/.env" && ! -f "$DOCKER_DIR/.env.local" ]]; then
    echo -e "${RED}Error: No .env file found!${NC}"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running!${NC}"
    exit 1
fi

cd "$DOCKER_DIR"

echo -e "${YELLOW}Starting infrastructure...${NC}"

# Create network if not exists
docker network create iafactory-net 2>/dev/null || true

# Start database and cache first
echo -e "${YELLOW}Starting databases...${NC}"
docker-compose up -d iafactory-postgres iafactory-redis iafactory-qdrant

# Wait for databases to be healthy
echo -e "${YELLOW}Waiting for databases to be healthy...${NC}"
sleep 10

# Start backend
echo -e "${YELLOW}Starting backend API...${NC}"
docker-compose up -d iafactory-backend

# Wait for backend to be healthy
echo -e "${YELLOW}Waiting for backend to be healthy...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8180/health > /dev/null 2>&1; then
        echo -e "${GREEN}Backend is ready!${NC}"
        break
    fi
    sleep 2
done

# Start Bolt.diy with BMAD integration
echo -e "${YELLOW}Starting Bolt.diy Studio...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml up -d iafactory-bolt-studio

# Wait for Bolt.diy to be ready
echo -e "${YELLOW}Waiting for Bolt.diy to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8185/ > /dev/null 2>&1; then
        echo -e "${GREEN}Bolt.diy Studio is ready!${NC}"
        break
    fi
    sleep 2
done

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Stack is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  ${YELLOW}Backend API:${NC}     http://localhost:8180"
echo -e "  ${YELLOW}Bolt.diy Studio:${NC} http://localhost:8185"
echo -e "  ${YELLOW}API Docs:${NC}        http://localhost:8180/docs"
echo ""
echo -e "  ${YELLOW}BMAD Agents available in Bolt.diy:${NC}"
echo -e "    - Winston (Architect)"
echo -e "    - John (PM)"
echo -e "    - Amelia (Developer)"
echo -e "    - Mary (Analyst)"
echo -e "    - Murat (Test Architect)"
echo ""
echo -e "To view logs: ${YELLOW}docker-compose logs -f${NC}"
echo -e "To stop:      ${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.bolt.yml down${NC}"
