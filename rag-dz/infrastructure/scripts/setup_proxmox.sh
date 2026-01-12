#!/bin/bash
set -e

echo "🏭 IA FACTORY - Setup Multi-Tenant"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "📦 System update..."
apt update && apt upgrade -y

echo "🐳 Docker install..."
curl -fsSL https://get.docker.com | sh
systemctl enable docker

echo "📥 Ollama install..."
curl -fsSL https://ollama.ai/install.sh | sh

echo "✅ Setup complete!"
echo "📍 Next: docker-compose up -d"
