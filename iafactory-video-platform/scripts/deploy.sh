#!/bin/bash
set -e

# =============================================================================
# IAFactory Video Platform - Deployment Script
# =============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT="${1:-production}"
VERSION="${2:-latest}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     IAFactory Video Platform - Deployment                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi

    log_info "All requirements satisfied"
}

load_env() {
    log_info "Loading environment variables..."

    ENV_FILE="$PROJECT_ROOT/.env.$ENVIRONMENT"
    if [ ! -f "$ENV_FILE" ]; then
        ENV_FILE="$PROJECT_ROOT/.env"
    fi

    if [ -f "$ENV_FILE" ]; then
        export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
        log_info "Loaded environment from $ENV_FILE"
    else
        log_warn "No .env file found, using defaults"
    fi
}

build_images() {
    log_info "Building Docker images..."

    cd "$PROJECT_ROOT"

    # Build backend
    docker build -t iafactory-video-backend:$VERSION -f backend/Dockerfile backend/

    # Build frontend
    docker build -t iafactory-video-frontend:$VERSION -f frontend/Dockerfile frontend/

    log_info "Images built successfully"
}

deploy_services() {
    log_info "Deploying services for $ENVIRONMENT..."

    cd "$PROJECT_ROOT"

    COMPOSE_FILE="docker-compose.yml"
    if [ "$ENVIRONMENT" = "production" ]; then
        COMPOSE_FILE="docker-compose.prod.yml"
    fi

    # Pull latest images if using remote registry
    if [ -n "$DOCKER_REGISTRY" ]; then
        docker-compose -f "$COMPOSE_FILE" pull
    fi

    # Deploy with zero-downtime
    docker-compose -f "$COMPOSE_FILE" up -d --remove-orphans

    log_info "Services deployed"
}

run_migrations() {
    log_info "Running database migrations..."

    cd "$PROJECT_ROOT"

    # Wait for database to be ready
    sleep 5

    # Run migrations
    docker-compose exec -T backend alembic upgrade head || true

    log_info "Migrations completed"
}

health_check() {
    log_info "Running health checks..."

    MAX_RETRIES=30
    RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")

        if [ "$HTTP_CODE" = "200" ]; then
            log_info "Backend is healthy"
            break
        fi

        RETRY_COUNT=$((RETRY_COUNT + 1))
        log_warn "Waiting for backend to be ready... ($RETRY_COUNT/$MAX_RETRIES)"
        sleep 2
    done

    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        log_error "Backend health check failed"
        exit 1
    fi

    # Check frontend
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        log_info "Frontend is healthy"
    else
        log_warn "Frontend may not be ready yet"
    fi
}

cleanup_old() {
    log_info "Cleaning up old resources..."

    # Remove dangling images
    docker image prune -f

    # Remove unused volumes (be careful in production)
    if [ "$ENVIRONMENT" != "production" ]; then
        docker volume prune -f
    fi

    log_info "Cleanup completed"
}

print_status() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                  Deployment Complete!                       ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Environment: ${BLUE}$ENVIRONMENT${NC}"
    echo -e "Version: ${BLUE}$VERSION${NC}"
    echo ""
    echo "Services:"
    docker-compose ps
    echo ""
    echo -e "Access the application at:"
    echo -e "  Frontend: ${BLUE}http://localhost:3000${NC}"
    echo -e "  Backend API: ${BLUE}http://localhost:8000${NC}"
    echo -e "  API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    if [ "$ENVIRONMENT" = "production" ]; then
        echo -e "  Prometheus: ${BLUE}http://localhost:9090${NC}"
        echo -e "  Grafana: ${BLUE}http://localhost:3001${NC}"
    fi
    echo ""
}

# Main execution
main() {
    echo "Deploying to: $ENVIRONMENT"
    echo "Version: $VERSION"
    echo ""

    check_requirements
    load_env
    build_images
    deploy_services
    run_migrations
    health_check
    cleanup_old
    print_status
}

# Handle signals
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main
main
