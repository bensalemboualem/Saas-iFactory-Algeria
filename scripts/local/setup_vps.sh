#!/bin/bash
# setup_vps.sh

# Exit on error
set -e

echo "🚀 Starting IA Factory Staging Setup..."

# 1. Install Docker & Tools
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
else
    echo "✅ Docker already installed"
fi

# 2. Setup Directory
echo "📂 Setting up directories..."
mkdir -p /opt/iafactory
cd /opt/iafactory

# 3. Extract Source
if [ -f "iafactory-source.tar.gz" ]; then
    echo "📦 Extracting source..."
    tar -xzvf iafactory-source.tar.gz
    rm iafactory-source.tar.gz
else
    echo "⚠️ iafactory-source.tar.gz not found!"
fi

# 4. Configure Environment
if [ ! -f ".env.staging" ]; then
    echo "⚙️ Creating .env.staging from example..."
    cp .env.staging.example .env.staging
    echo "⚠️ IMPORTANT: Please edit .env.staging with real secrets!"
fi

# 5. Build and Launch
echo "🏗️ Building Docker containers..."
docker compose -f docker-compose.staging.yml build

echo "🚀 Launching Services..."
docker compose -f docker-compose.staging.yml up -d

echo "✅ Deployment Complete!"
echo "👉 Check logs: docker compose -f docker-compose.staging.yml logs -f"
