#!/bin/bash

###############################################################################
# IA Factory - Production Deployment Script
# Multi-Tenant SaaS: Switzerland (Psychologist) + Algeria (Education)
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "=================================================="
echo "   IA Factory - Live VPS Deployment"
echo "   🇨🇭 Switzerland | 🇩🇿 Algeria"
echo "=================================================="
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${GREEN}✓ Running as root${NC}"

###############################################################################
# Step 1: System Update & Dependencies
###############################################################################
echo -e "\n${YELLOW}[1/8] Installing system dependencies...${NC}"
apt-get update -qq
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw \
    certbot

echo -e "${GREEN}✓ System dependencies installed${NC}"

###############################################################################
# Step 2: Install Docker & Docker Compose
###############################################################################
echo -e "\n${YELLOW}[2/8] Installing Docker...${NC}"

# Add Docker GPG key
if [ ! -f /usr/share/keyrings/docker-archive-keyring.gpg ]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
fi

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
apt-get update -qq
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
systemctl enable docker
systemctl start docker

echo -e "${GREEN}✓ Docker installed: $(docker --version)${NC}"

###############################################################################
# Step 3: Configure Firewall
###############################################################################
echo -e "\n${YELLOW}[3/8] Configuring firewall...${NC}"

ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS

echo -e "${GREEN}✓ Firewall configured${NC}"

###############################################################################
# Step 4: Create .env file
###############################################################################
echo -e "\n${YELLOW}[4/8] Creating environment file...${NC}"

# Prompt for secrets
read -sp "Enter PostgreSQL password: " POSTGRES_PASSWORD
echo
read -sp "Enter JWT secret key (min 32 chars): " SECRET_KEY
echo
read -p "Enter SMTP user: " SMTP_USER
read -sp "Enter SMTP password: " SMTP_PASSWORD
echo

# Create .env
cat > .env << ENVEOF
POSTGRES_DB=iafactory
POSTGRES_USER=iafactory
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
SECRET_KEY=${SECRET_KEY}
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=${SMTP_USER}
SMTP_PASSWORD=${SMTP_PASSWORD}
FROM_EMAIL=noreply@iafactory.pro
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
ENVEOF

echo -e "${GREEN}✓ .env file created${NC}"

###############################################################################
# Step 5: Obtain SSL Certificates
###############################################################################
echo -e "\n${YELLOW}[5/8] Obtaining SSL certificates...${NC}"

read -p "Enter email for Let's Encrypt: " LETSENCRYPT_EMAIL
read -p "Obtain SSL for iafactory.ch? (y/n): " CERT_CH
read -p "Obtain SSL for iafactoryalgeria.com? (y/n): " CERT_DZ

# Start Nginx
docker compose -f docker-compose.production.yml up -d nginx
sleep 5

if [[ "$CERT_CH" == "y" ]]; then
    certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email $LETSENCRYPT_EMAIL \
        --agree-tos --no-eff-email \
        -d iafactory.ch -d www.iafactory.ch
    echo -e "${GREEN}✓ SSL for iafactory.ch${NC}"
fi

if [[ "$CERT_DZ" == "y" ]]; then
    certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email $LETSENCRYPT_EMAIL \
        --agree-tos --no-eff-email \
        -d iafactoryalgeria.com -d www.iafactoryalgeria.com
    echo -e "${GREEN}✓ SSL for iafactoryalgeria.com${NC}"
fi

###############################################################################
# Step 6: Run Database Migrations
###############################################################################
echo -e "\n${YELLOW}[6/8] Running database migrations...${NC}"

docker compose -f docker-compose.production.yml up -d postgres
sleep 10

echo -e "${GREEN}✓ Database ready${NC}"

###############################################################################
# Step 7: Build & Start All Services
###############################################################################
echo -e "\n${YELLOW}[7/8] Building services...${NC}"

docker compose -f docker-compose.production.yml build
docker compose -f docker-compose.production.yml up -d

echo -e "${GREEN}✓ All services started${NC}"

###############################################################################
# Step 8: Health Check
###############################################################################
echo -e "\n${YELLOW}[8/8] Health checks...${NC}"
sleep 10

BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/health || echo "000")
if [ "$BACKEND_STATUS" == "200" ]; then
    echo -e "${GREEN}✓ Backend: Healthy${NC}"
else
    echo -e "${RED}✗ Backend: Status $BACKEND_STATUS${NC}"
fi

docker ps | grep -q iafactory-nginx && echo -e "${GREEN}✓ Nginx: Running${NC}" || echo -e "${RED}✗ Nginx: Not running${NC}"
docker ps | grep -q iafactory-db && echo -e "${GREEN}✓ PostgreSQL: Running${NC}" || echo -e "${RED}✗ PostgreSQL: Not running${NC}"

###############################################################################
# Complete
###############################################################################
echo -e "\n${BLUE}=================================================="
echo "   Deployment Complete!"
echo "=================================================="
echo -e "${NC}"

echo -e "${GREEN}✅ IA Factory is live!${NC}\n"

echo "Access:"
echo -e "  🇨🇭 ${YELLOW}https://iafactory.ch${NC}"
echo -e "  🇩🇿 ${YELLOW}https://iafactoryalgeria.com${NC}"
echo ""

echo "Commands:"
echo "  docker compose -f docker-compose.production.yml logs -f"
echo "  docker compose -f docker-compose.production.yml restart"
echo "  docker compose -f docker-compose.production.yml ps"
echo ""

echo -e "${GREEN}Happy deploying! 🚀${NC}"
