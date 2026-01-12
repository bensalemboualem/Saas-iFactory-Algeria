#!/usr/bin/env bash
set -euo pipefail

SCENARIO=${1:-orchestrator-smoke}
SCRIPT_PATH="tests/load/k6/${SCENARIO}.js"

if [[ ! -f "${SCRIPT_PATH}" ]]; then
  echo "❌ Scénario introuvable: ${SCRIPT_PATH}"
  exit 1
fi

K6_IMAGE=${K6_IMAGE:-grafana/k6:latest}
BASE_URL=${K6_BASE_URL:-http://host.docker.internal:8180}
API_KEY=${K6_API_KEY:-change-me-in-production}
VUS=${K6_VUS:-10}
DURATION=${K6_DURATION:-1m}

echo "🚀 Lancement k6 (${SCENARIO}) contre ${BASE_URL}..."

docker run --rm -i \
  -e K6_BASE_URL="${BASE_URL}" \
  -e K6_API_KEY="${API_KEY}" \
  -e K6_VUS="${VUS}" \
  -e K6_DURATION="${DURATION}" \
  -v "$(pwd)/tests/load/k6:/scripts" \
  "${K6_IMAGE}" run "/scripts/${SCENARIO}.js"

