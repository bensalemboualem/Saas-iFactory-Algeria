#!/bin/bash

echo "🔍 Health Check Nexus AI Platform"
echo "═══════════════════════════════════════"
echo ""

check_service() {
    local url=$1
    local name=$2
    
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "  ✅ $name"
        return 0
    else
        echo "  ❌ $name (non accessible)"
        return 1
    fi
}

errors=0

check_service "http://localhost:${META_PORT:-8100}/health" "Meta-Orchestrator (:${META_PORT:-8100})" || ((errors++))
check_service "http://localhost:${ARCHON_SERVER_PORT:-8181}/health" "Archon Server (:${ARCHON_SERVER_PORT:-8181})" || ((errors++))
check_service "http://localhost:${ARCHON_UI_PORT:-3737}" "Archon UI (:${ARCHON_UI_PORT:-3737})" || ((errors++))
check_service "http://localhost:${BOLT_PORT:-5173}" "Bolt.diy (:${BOLT_PORT:-5173})" || ((errors++))

# Redis check
if docker exec nexus-redis redis-cli ping > /dev/null 2>&1; then
    echo "  ✅ Redis"
else
    echo "  ❌ Redis"
    ((errors++))
fi

echo ""
echo "═══════════════════════════════════════"

if [ $errors -eq 0 ]; then
    echo "✅ Tous les services sont opérationnels"
    exit 0
else
    echo "⚠️  $errors service(s) non disponible(s)"
    exit 1
fi
