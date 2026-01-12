#!/bin/bash
# ============================================
# IAFactory Development Setup
# ============================================
# Sets up local development environment
# Usage: ./scripts/dev-setup.sh
# ============================================

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}IAFactory Development Setup${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Check prerequisites
echo -e "${BOLD}[1/7] Checking prerequisites...${NC}"

check_command() {
  if command -v "$1" &> /dev/null; then
    echo -e "  ✓ $1 installed"
    return 0
  else
    echo -e "  ${RED}✗ $1 not found${NC}"
    return 1
  fi
}

MISSING=()
check_command "docker" || MISSING+=("Docker")
check_command "docker-compose" || MISSING+=("Docker Compose")
check_command "git" || MISSING+=("Git")
check_command "node" || MISSING+=("Node.js")
check_command "python3" || MISSING+=("Python 3")

if [ ${#MISSING[@]} -gt 0 ]; then
  echo -e "\n${RED}Missing required tools:${NC}"
  for tool in "${MISSING[@]}"; do
    echo -e "  - $tool"
  done
  exit 1
fi
echo -e "${GREEN}✓ All prerequisites installed${NC}\n"

# Check .env file
echo -e "${BOLD}[2/7] Checking environment configuration...${NC}"
if [ ! -f ".env.local" ]; then
  echo -e "${YELLOW}⚠ .env.local not found${NC}"
  if [ -f ".env.example" ]; then
    echo -e "Copying from .env.example..."
    cp .env.example .env.local
    echo -e "${GREEN}✓ Created .env.local${NC}"
    echo -e "${YELLOW}⚠ Please edit .env.local with your API keys${NC}"
  else
    echo -e "${RED}✗ .env.example not found!${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}✓ .env.local exists${NC}"
fi
echo ""

# Create required directories
echo -e "${BOLD}[3/7] Creating directories...${NC}"
mkdir -p backups logs scripts infrastructure/sql infrastructure/monitoring infrastructure/n8n/workflows
echo -e "${GREEN}✓ Directories created${NC}\n"

# Make scripts executable
echo -e "${BOLD}[4/7] Setting script permissions...${NC}"
chmod +x scripts/*.sh 2>/dev/null || true
echo -e "${GREEN}✓ Scripts are executable${NC}\n"

# Pull Docker images
echo -e "${BOLD}[5/7] Pulling Docker images...${NC}"
docker-compose pull
echo -e "${GREEN}✓ Images pulled${NC}\n"

# Build custom images
echo -e "${BOLD}[6/7] Building custom images...${NC}"
docker-compose build
echo -e "${GREEN}✓ Images built${NC}\n"

# Start services
echo -e "${BOLD}[7/7] Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}\n"

# Wait for health
echo -e "${BOLD}Running health checks...${NC}\n"
sleep 15
./scripts/health-check.sh --wait

echo -e "\n${BOLD}======================================${NC}"
echo -e "${GREEN}✓ Development environment ready!${NC}"
echo -e "${BOLD}======================================${NC}\n"

echo -e "${BOLD}Quick Start:${NC}"
echo -e "  View logs:    ${GREEN}./scripts/logs.sh backend --follow${NC}"
echo -e "  Health check: ${GREEN}./scripts/health-check.sh${NC}"
echo -e "  Restart:      ${GREEN}./scripts/restart-stack.sh${NC}"
echo -e "  Backup DB:    ${GREEN}./scripts/db-backup.sh${NC}"

echo -e "\n${BOLD}Access URLs:${NC}"
echo -e "  Backend API:  ${GREEN}http://localhost:8180/docs${NC}"
echo -e "  Hub UI:       ${GREEN}http://localhost:8182${NC}"
echo -e "  Docs UI:      ${GREEN}http://localhost:8183${NC}"
echo -e "  n8n:          ${GREEN}http://localhost:8185${NC}"

echo -e "\n${BOLD}Important Files:${NC}"
echo -e "  Environment:  ${GREEN}.env.local${NC}"
echo -e "  Docker:       ${GREEN}docker-compose.yml${NC}"
echo -e "  Logs:         ${GREEN}./scripts/logs.sh${NC}"
