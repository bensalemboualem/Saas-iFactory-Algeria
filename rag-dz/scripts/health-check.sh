#!/bin/bash
# ============================================
# IAFactory Health Check Script
# ============================================
# Validates all services are running correctly
# Usage: ./scripts/health-check.sh [--wait]
# ============================================

set -e

WAIT_MODE=false
if [[ "$1" == "--wait" ]]; then
  WAIT_MODE=true
fi

BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}IAFactory Health Check${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Function to check service health
check_service() {
  local service_name=$1
  local url=$2
  local max_attempts=${3:-30}
  local attempt=1

  echo -n "Checking ${service_name}... "

  while [ $attempt -le $max_attempts ]; do
    if curl -sf "$url" > /dev/null 2>&1; then
      echo -e "${GREEN}✓ HEALTHY${NC}"
      return 0
    fi

    if [ "$WAIT_MODE" = true ]; then
      sleep 2
      attempt=$((attempt + 1))
    else
      echo -e "${RED}✗ FAILED${NC}"
      return 1
    fi
  done

  echo -e "${RED}✗ TIMEOUT${NC}"
  return 1
}

# Function to check Docker container status
check_container() {
  local container_name=$1
  echo -n "Container ${container_name}... "

  if docker ps --filter "name=${container_name}" --filter "status=running" | grep -q "${container_name}"; then
    echo -e "${GREEN}✓ RUNNING${NC}"
    return 0
  else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    return 1
  fi
}

# Check Docker daemon
echo -e "${BOLD}[1/4] Docker Infrastructure${NC}"
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}✗ Docker daemon not running!${NC}"
  echo -e "${YELLOW}Please start Docker Desktop and retry.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Docker daemon running${NC}\n"

# Check containers
echo -e "${BOLD}[2/4] Container Status${NC}"
CONTAINERS=(
  "iaf-dz-postgres"
  "iaf-dz-redis"
  "iaf-dz-qdrant"
  "iaf-dz-backend"
  "iaf-dz-hub"
  "iaf-dz-docs"
  "iaf-dz-n8n"
)

FAILED_CONTAINERS=()
for container in "${CONTAINERS[@]}"; do
  if ! check_container "$container"; then
    FAILED_CONTAINERS+=("$container")
  fi
done

if [ ${#FAILED_CONTAINERS[@]} -gt 0 ]; then
  echo -e "\n${YELLOW}⚠ Some containers are not running:${NC}"
  for container in "${FAILED_CONTAINERS[@]}"; do
    echo -e "  - ${container}"
  done
  echo ""
fi

# Check service endpoints
echo -e "\n${BOLD}[3/4] Service Health Endpoints${NC}"
SERVICES=(
  "Backend API:http://localhost:8180/health"
  "Frontend Hub:http://localhost:8182"
  "Frontend Docs:http://localhost:8183"
  "n8n Workflow:http://localhost:8185"
)

FAILED_SERVICES=()
for service_def in "${SERVICES[@]}"; do
  IFS=':' read -r name url <<< "$service_def"
  if ! check_service "$name" "$url" 10; then
    FAILED_SERVICES+=("$name")
  fi
done

# Check database connectivity
echo -e "\n${BOLD}[4/4] Database Connectivity${NC}"
echo -n "PostgreSQL connection... "
if docker exec iaf-dz-postgres pg_isready -U postgres > /dev/null 2>&1; then
  echo -e "${GREEN}✓ CONNECTED${NC}"
else
  echo -e "${RED}✗ FAILED${NC}"
  FAILED_SERVICES+=("PostgreSQL")
fi

echo -n "Redis connection... "
if docker exec iaf-dz-redis redis-cli ping > /dev/null 2>&1; then
  echo -e "${GREEN}✓ CONNECTED${NC}"
else
  echo -e "${RED}✗ FAILED${NC}"
  FAILED_SERVICES+=("Redis")
fi

# Summary
echo -e "\n${BOLD}======================================${NC}"
if [ ${#FAILED_CONTAINERS[@]} -eq 0 ] && [ ${#FAILED_SERVICES[@]} -eq 0 ]; then
  echo -e "${GREEN}✓ All systems operational!${NC}"
  echo -e "\n${BOLD}Access Points:${NC}"
  echo -e "  Backend API:  http://localhost:8180/docs"
  echo -e "  Hub UI:       http://localhost:8182"
  echo -e "  Docs UI:      http://localhost:8183"
  echo -e "  n8n:          http://localhost:8185"
  exit 0
else
  echo -e "${RED}✗ System health check failed!${NC}"
  echo -e "\n${YELLOW}Troubleshooting:${NC}"
  echo -e "  1. Check Docker logs: ${BOLD}docker logs <container-name>${NC}"
  echo -e "  2. Restart services: ${BOLD}./scripts/restart-stack.sh${NC}"
  echo -e "  3. Full rebuild: ${BOLD}./scripts/rebuild-all.sh${NC}"
  exit 1
fi
