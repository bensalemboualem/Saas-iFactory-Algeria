#!/bin/bash
# FIX BOLT - À copier-coller dans Console Hetzner

# Nettoyage
pkill -9 -f "vite"
pkill -9 -f "pnpm.*dev"
pkill -9 -f "docker-compose.*bolt"
sleep 3

# Démarrage
export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
cd /opt/iafactory-rag-dz/bolt-diy
nohup pnpm run dev --host 0.0.0.0 --port 5173 > /var/log/bolt.log 2>&1 &

# Attente
sleep 30

# Test
echo "=== TEST ==="
netstat -tlnp | grep 5173
curl -I http://localhost:5173
curl -I https://bolt.iafactoryalgeria.com
