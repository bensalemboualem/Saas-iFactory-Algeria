#!/bin/bash
set -e

echo "🚀 Démarrage Nexus AI Platform..."
echo ""

# Vérifier .env
if [ ! -f .env ]; then
    echo "❌ Fichier .env manquant!"
    echo "   Copiez .env.example → .env et configurez vos clés API"
    echo "   cp .env.example .env"
    exit 1
fi

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non installé"
    exit 1
fi

# Démarrer les services
echo "📦 Démarrage des containers..."
docker compose up -d --build

# Attendre
echo ""
echo "⏳ Attente du démarrage des services (45s)..."
sleep 45

# Health check
echo ""
echo "🔍 Vérification des services..."
./scripts/health-check.sh

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ NEXUS AI PLATFORM DÉMARRÉ"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📍 Services disponibles:"
echo ""
echo "   🧠 Meta-Orchestrator:  http://localhost:${META_PORT:-8100}"
echo "   📚 Archon UI:          http://localhost:${ARCHON_UI_PORT:-3737}"
echo "   🔌 Archon API:         http://localhost:${ARCHON_SERVER_PORT:-8181}"
echo "   🔗 Archon MCP:         http://localhost:${ARCHON_MCP_PORT:-8051}"
echo "   ⚡ Bolt.diy:           http://localhost:${BOLT_PORT:-5173}"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📖 Commandes utiles:"
echo "   ./scripts/stop.sh        - Arrêter les services"
echo "   ./scripts/health-check.sh - Vérifier la santé"
echo "   docker compose logs -f   - Voir les logs"
echo ""
