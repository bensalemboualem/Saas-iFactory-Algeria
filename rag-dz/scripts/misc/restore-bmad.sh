#!/bin/bash
set -e

echo "🚀 Restauration système BMAD complet..."

# 1. Arrêter anciens backends
echo "1️⃣ Arrêt anciens backends..."
pkill -9 -f 'uvicorn main:app' || true
sleep 2

# 2. Trouver Python avec uvicorn
echo "2️⃣ Recherche Python..."
PYTHON_CMD=$(which python3.11 || which python3.10 || which python3)
echo "Python trouvé: $PYTHON_CMD"

# 3. Démarrer backend principal sur port 8000
echo "3️⃣ Démarrage backend port 8000..."
cd /opt/iafactory-rag-dz/backend/rag-compat

nohup $PYTHON_CMD -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    > /var/log/rag-backend-8000.log 2>&1 &

sleep 5

# 4. Vérifier endpoints
echo "4️⃣ Vérification endpoints..."
curl -s http://localhost:8000/api/orchestrator/health && echo "✅ Orchestrator OK" || echo "❌ Orchestrator FAIL"
curl -s http://localhost:8000/api/coordination/health && echo "✅ Coordination OK" || echo "❌ Coordination FAIL"

# 5. Mettre à jour Nginx
echo "5️⃣ Mise à jour Nginx..."
sed -i 's/proxy_pass http:\/\/127.0.0.1:[0-9]*/proxy_pass http:\/\/127.0.0.1:8000/' \
    /etc/nginx/sites-enabled/iafactoryalgeria.com

nginx -t && nginx -s reload
echo "✅ Nginx rechargé"

# 6. Démarrer BOLT si pas running
echo "6️⃣ Vérification BOLT..."
if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    cd /opt/iafactory-rag-dz/bolt-diy
    nohup pnpm run dev --host 0.0.0.0 --port 5173 \
        > /var/log/bolt.log 2>&1 &
    echo "✅ BOLT démarré"
else
    echo "✅ BOLT déjà running"
fi

sleep 5

# 7. Tests finaux
echo ""
echo "🧪 TESTS FINAUX:"
echo "==============="

echo -n "Backend API: "
curl -s https://iafactoryalgeria.com/api/orchestrator/health > /dev/null && echo "✅ OK" || echo "❌ FAIL"

echo -n "Coordination: "
curl -s https://iafactoryalgeria.com/api/coordination/health > /dev/null && echo "✅ OK" || echo "❌ FAIL"

echo -n "BOLT: "
curl -s http://localhost:5173 > /dev/null && echo "✅ OK" || echo "❌ FAIL"

echo ""
echo "🎉 RESTAURATION TERMINÉE!"
echo ""
echo "📊 URLs disponibles:"
echo "  - BOLT avec BMAD: https://iafactoryalgeria.com/bolt/"
echo "  - Pipeline Creator: https://iafactoryalgeria.com/pipeline/"
echo "  - API Orchestrator: https://iafactoryalgeria.com/api/orchestrator/"
echo "  - API Coordination: https://iafactoryalgeria.com/api/coordination/"
echo ""
