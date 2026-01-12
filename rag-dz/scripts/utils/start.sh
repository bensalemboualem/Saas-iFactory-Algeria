#!/bin/bash
# Script de démarrage rapide pour RAG.dz

set -e

echo "🚀 RAG.dz - Démarrage rapide"
echo "================================"

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📋 Copie de .env.example vers .env..."
    cp .env.example .env
    echo "✅ Fichier .env créé"
    echo ""
    echo "⚠️  IMPORTANT: Éditez .env et configurez:"
    echo "   - POSTGRES_PASSWORD"
    echo "   - API_SECRET_KEY (générez avec: openssl rand -hex 32)"
    echo "   - GRAFANA_PASSWORD"
    echo ""
    read -p "Appuyez sur Entrée pour continuer après avoir configuré .env..."
fi

echo ""
echo "🐳 Démarrage des services Docker..."
echo "================================"

# Démarrer infrastructure
echo "1️⃣  Démarrage de l'infrastructure (PostgreSQL, Redis, Qdrant)..."
docker-compose up -d postgres redis qdrant

echo "⏳ Attente des healthchecks (30s)..."
sleep 30

# Vérifier status
echo ""
echo "📊 Status des services:"
docker-compose ps

# Démarrer backend et frontend
echo ""
echo "2️⃣  Démarrage du backend et frontend..."
docker-compose up -d backend frontend

echo "⏳ Attente du démarrage (15s)..."
sleep 15

# Démarrer monitoring
echo ""
echo "3️⃣  Démarrage du monitoring..."
docker-compose up -d prometheus grafana

echo ""
echo "✅ Tous les services sont démarrés!"
echo ""
echo "🌐 URLs disponibles:"
echo "================================"
echo "  Frontend:    http://localhost:5173"
echo "  Backend API: http://localhost:8180"
echo "  API Docs:    http://localhost:8180/docs"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3001 (admin/admin)"
echo ""
echo "📊 Vérification santé backend..."
curl -s http://localhost:8180/health | jq '.' || echo "Backend pas encore prêt"

echo ""
echo "📝 Commandes utiles:"
echo "================================"
echo "  Logs backend:   docker-compose logs -f backend"
echo "  Logs frontend:  docker-compose logs -f frontend"
echo "  Arrêter tout:   docker-compose down"
echo "  Redémarrer:     docker-compose restart"
echo ""
echo "🎉 Prêt à utiliser RAG.dz!"
