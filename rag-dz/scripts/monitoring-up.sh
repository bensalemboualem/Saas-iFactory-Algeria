#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Démarrage du stack de monitoring (Prometheus + Grafana)..."

docker compose --profile monitoring up -d iafactory-prometheus iafactory-grafana
docker compose --profile monitoring ps

echo ""
echo "Prometheus: http://localhost:8187"
echo "Grafana   : http://localhost:8188 (admin / ${GRAFANA_PASSWORD:-admin})"

