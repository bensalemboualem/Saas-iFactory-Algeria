#!/bin/bash
# IA Factory - Deployment Script for VPS
# Run this on iafactorysuisse (46.224.3.125)

set -e

echo "🚀 Deploying IA Factory Platform..."

# Configuration
PROJECT_DIR="/opt/ia-factory"
BACKUP_DIR="/opt/backups/ia-factory"

# Create directories
sudo mkdir -p $PROJECT_DIR
sudo mkdir -p $BACKUP_DIR

# Navigate to project
cd $PROJECT_DIR

# Stop existing services (if running)
if [ -f "docker-compose.yml" ]; then
    echo "📦 Stopping existing services..."
    docker-compose down || true
fi

# Copy project files (run this from local machine first)
echo "📂 Project files should be in $PROJECT_DIR"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from example..."
    cp .env.example .env
    echo "❗ Please edit .env file with your API keys:"
    echo "   sudo nano $PROJECT_DIR/.env"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🏥 Checking health..."
curl -s http://localhost:8087/health | jq .

# Add nginx configuration
echo "📝 Adding Nginx configuration..."
if ! grep -q "ia-factory" /etc/nginx/sites-available/iafactoryalgeria.com; then
    echo "Adding IA Factory location block to nginx..."
    # The nginx snippet should be manually added
    echo "⚠️  Please add the nginx configuration from nginx-snippet.conf"
fi

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "✅ IA Factory Deployment Complete!"
echo ""
echo "📍 Endpoints:"
echo "   - API: https://www.iafactoryalgeria.com/ia-factory/"
echo "   - Health: https://www.iafactoryalgeria.com/ia-factory/health"
echo "   - Docs: https://www.iafactoryalgeria.com/ia-factory/docs"
echo ""
echo "📊 Docker Status:"
docker-compose ps
echo ""
echo "📋 Logs: docker-compose logs -f"
