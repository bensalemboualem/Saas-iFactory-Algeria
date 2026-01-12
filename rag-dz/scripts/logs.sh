#!/bin/bash
# ============================================
# IAFactory Logs Viewer
# ============================================
# View logs for specific services
# Usage: ./scripts/logs.sh [service-name] [--follow]
# ============================================

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVICE=$1
FOLLOW=""

if [[ "$2" == "--follow" ]] || [[ "$2" == "-f" ]]; then
  FOLLOW="-f"
fi

# Map friendly names to container names
declare -A SERVICES=(
  ["backend"]="iaf-dz-backend"
  ["hub"]="iaf-dz-hub"
  ["docs"]="iaf-dz-docs"
  ["postgres"]="iaf-dz-postgres"
  ["redis"]="iaf-dz-redis"
  ["qdrant"]="iaf-dz-qdrant"
  ["n8n"]="iaf-dz-n8n"
  ["studio"]="iaf-dz-studio"
)

if [ -z "$SERVICE" ]; then
  echo -e "${BOLD}Available services:${NC}"
  for key in "${!SERVICES[@]}"; do
    echo -e "  - ${GREEN}$key${NC} (${SERVICES[$key]})"
  done
  echo -e "\n${BOLD}Usage:${NC}"
  echo -e "  ./scripts/logs.sh <service> [--follow]"
  echo -e "\n${BOLD}Examples:${NC}"
  echo -e "  ./scripts/logs.sh backend"
  echo -e "  ./scripts/logs.sh backend --follow"
  echo -e "  ./scripts/logs.sh all --follow"
  exit 0
fi

if [ "$SERVICE" == "all" ]; then
  echo -e "${BOLD}Showing logs for all services...${NC}\n"
  docker-compose logs $FOLLOW
else
  CONTAINER_NAME=${SERVICES[$SERVICE]}
  if [ -z "$CONTAINER_NAME" ]; then
    echo -e "${YELLOW}Unknown service: $SERVICE${NC}"
    echo -e "Run ${BOLD}./scripts/logs.sh${NC} to see available services."
    exit 1
  fi

  echo -e "${BOLD}Showing logs for: ${GREEN}$SERVICE${NC} ($CONTAINER_NAME)\n"
  docker logs $FOLLOW --tail 100 "$CONTAINER_NAME"
fi
