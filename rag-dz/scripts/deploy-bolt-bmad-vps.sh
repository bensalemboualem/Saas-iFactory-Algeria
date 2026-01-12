#!/bin/bash
# ============================================
# Deploy Bolt.diy + BMAD Stack to VPS
# ============================================
# Usage: ./scripts/deploy-bolt-bmad-vps.sh [--full|--update]
# VPS: 46.224.3.125
# ============================================

set -e

# Configuration
VPS_HOST="${VPS_HOST:-46.224.3.125}"
VPS_USER="${VPS_USER:-root}"
VPS_PATH="/opt/iafactory"
SSH_KEY="${SSH_KEY:-}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  VPS Deployment: Bolt.diy + BMAD${NC}"
echo -e "${BLUE}  Target: $VPS_USER@$VPS_HOST${NC}"
echo -e "${BLUE}========================================${NC}"

# Parse arguments
DEPLOY_MODE="update"
if [[ "$1" == "--full" ]]; then
    DEPLOY_MODE="full"
fi

# Build SSH command
SSH_CMD="ssh"
if [[ -n "$SSH_KEY" ]]; then
    SSH_CMD="ssh -i $SSH_KEY"
fi

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection...${NC}"
if ! $SSH_CMD $VPS_USER@$VPS_HOST "echo 'Connection successful'" 2>/dev/null; then
    echo -e "${RED}Error: Cannot connect to VPS!${NC}"
    echo "Make sure SSH key is configured or set VPS_USER and SSH_KEY"
    exit 1
fi

echo -e "${GREEN}SSH connection successful!${NC}"

# Deploy based on mode
if [[ "$DEPLOY_MODE" == "full" ]]; then
    echo -e "${YELLOW}Full deployment mode...${NC}"

    $SSH_CMD $VPS_USER@$VPS_HOST << 'REMOTE_SCRIPT'
set -e

echo "=== Updating system ==="
apt-get update -qq

echo "=== Installing Docker (if needed) ==="
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

echo "=== Creating project directory ==="
mkdir -p /opt/iafactory
cd /opt/iafactory

echo "=== Cloning/updating repository ==="
if [ -d ".git" ]; then
    git fetch origin
    git reset --hard origin/main
else
    git clone https://github.com/iafactory/rag-dz.git .
fi

echo "=== Creating Docker network ==="
docker network create iafactory-net 2>/dev/null || true

echo "=== Setting up environment ==="
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "IMPORTANT: Please configure .env file!"
fi

echo "=== Building and starting containers ==="
cd infrastructure/docker
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml build
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml up -d

echo "=== Deployment complete! ==="
docker-compose ps
REMOTE_SCRIPT

else
    echo -e "${YELLOW}Update deployment mode...${NC}"

    $SSH_CMD $VPS_USER@$VPS_HOST << 'REMOTE_SCRIPT'
set -e

cd /opt/iafactory

echo "=== Pulling latest changes ==="
git fetch origin
git reset --hard origin/main

echo "=== Rebuilding and restarting Bolt.diy ==="
cd infrastructure/docker
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml build iafactory-bolt-studio
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml up -d iafactory-bolt-studio

echo "=== Update complete! ==="
docker-compose -f docker-compose.yml -f docker-compose.bolt.yml ps
REMOTE_SCRIPT

fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  ${YELLOW}VPS Access:${NC}"
echo -e "    Backend API:     http://$VPS_HOST:8180"
echo -e "    Bolt.diy Studio: http://$VPS_HOST:8185"
echo -e "    API Docs:        http://$VPS_HOST:8180/docs"
echo ""
echo -e "  ${YELLOW}Commands:${NC}"
echo -e "    View logs:    $SSH_CMD $VPS_USER@$VPS_HOST 'cd $VPS_PATH && docker-compose logs -f'"
echo -e "    Restart:      $SSH_CMD $VPS_USER@$VPS_HOST 'cd $VPS_PATH && docker-compose restart'"
echo ""
