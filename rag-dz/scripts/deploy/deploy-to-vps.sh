#!/bin/bash
# =============================================================================
# IAFactory RAG-DZ - Deployment Script to VPS
# =============================================================================
# Usage:
#   ./deploy-to-vps.sh [environment]
#
# Environments: dev, staging, prod (default: prod)
# =============================================================================

set -e  # Exit on error

# =============================================================================
# CONFIGURATION
# =============================================================================

VPS_HOST="${VPS_HOST:-root@46.224.3.125}"
VPS_DIR="${VPS_DIR:-/opt/iafactory-rag-dz}"
ENVIRONMENT="${1:-prod}"
COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."

    # Check if docker-compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Docker compose file not found: $COMPOSE_FILE"
        exit 1
    fi

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        log_warning ".env file not found - you'll need to create it on VPS"
    fi

    # Check SSH connection
    if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$VPS_HOST" exit 2>/dev/null; then
        log_error "Cannot connect to VPS: $VPS_HOST"
        log_info "Make sure SSH keys are set up or provide password when prompted"
    fi

    log_success "Requirements check passed"
}

create_vps_directory() {
    log_info "Creating VPS directory: $VPS_DIR"
    ssh "$VPS_HOST" "mkdir -p $VPS_DIR"
    log_success "VPS directory created"
}

sync_files() {
    log_info "Syncing files to VPS..."

    # Exclude patterns
    EXCLUDE=(
        ".git"
        ".vite"
        "node_modules"
        "__pycache__"
        "*.pyc"
        ".env"
        ".env.local"
        "*.log"
        "dist"
        "build"
        ".DS_Store"
    )

    # Build rsync exclude arguments
    EXCLUDE_ARGS=""
    for pattern in "${EXCLUDE[@]}"; do
        EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$pattern"
    done

    # Sync files using rsync
    rsync -avz --progress \
        $EXCLUDE_ARGS \
        --delete \
        ./ "$VPS_HOST:$VPS_DIR/"

    log_success "Files synced to VPS"
}

setup_environment() {
    log_info "Setting up environment on VPS..."

    ssh "$VPS_HOST" bash << EOF
        cd $VPS_DIR

        # Copy .env.example to .env if it doesn't exist
        if [ ! -f .env ]; then
            echo "Creating .env from .env.example..."
            cp .env.example .env
            echo ""
            echo "⚠️  IMPORTANT: You need to edit .env and add your secrets!"
            echo "Run: ssh $VPS_HOST 'nano $VPS_DIR/.env'"
        fi

        # Make scripts executable
        chmod +x *.sh 2>/dev/null || true

        echo "✅ Environment setup complete"
EOF

    log_success "Environment setup complete"
}

build_containers() {
    log_info "Building Docker containers on VPS..."

    ssh "$VPS_HOST" bash << EOF
        cd $VPS_DIR

        # Pull latest images
        docker-compose -f $COMPOSE_FILE pull

        # Build containers
        docker-compose -f $COMPOSE_FILE build --no-cache

        echo "✅ Containers built successfully"
EOF

    log_success "Containers built"
}

start_services() {
    log_info "Starting services on VPS..."

    ssh "$VPS_HOST" bash << EOF
        cd $VPS_DIR

        # Stop existing services
        docker-compose -f $COMPOSE_FILE down

        # Start services
        docker-compose -f $COMPOSE_FILE up -d

        echo "✅ Services started"
EOF

    log_success "Services started"
}

verify_deployment() {
    log_info "Verifying deployment..."

    sleep 10  # Wait for services to start

    ssh "$VPS_HOST" bash << 'EOF'
        cd /opt/iafactory-rag-dz

        echo ""
        echo "=== RUNNING CONTAINERS ==="
        docker-compose ps

        echo ""
        echo "=== HEALTH CHECKS ==="

        # Check backend health
        if curl -f http://localhost:8181/health 2>/dev/null; then
            echo "✅ Backend is healthy"
        else
            echo "❌ Backend is not responding"
        fi

        # Check frontend
        if curl -f http://localhost:3000 2>/dev/null; then
            echo "✅ Frontend is accessible"
        else
            echo "❌ Frontend is not responding"
        fi

        # Check database
        if docker-compose exec -T postgres-prod pg_isready 2>/dev/null; then
            echo "✅ PostgreSQL is ready"
        else
            echo "❌ PostgreSQL is not ready"
        fi

        # Check Redis
        if docker-compose exec -T redis-cache redis-cli ping 2>/dev/null; then
            echo "✅ Redis is responding"
        else
            echo "❌ Redis is not responding"
        fi

        echo ""
        echo "=== RECENT LOGS ==="
        docker-compose logs --tail=20
EOF

    log_success "Deployment verification complete"
}

show_info() {
    log_info "Deployment Information:"
    echo ""
    echo "  VPS Host:     $VPS_HOST"
    echo "  VPS Dir:      $VPS_DIR"
    echo "  Environment:  $ENVIRONMENT"
    echo "  Compose File: $COMPOSE_FILE"
    echo ""
    echo "Access URLs (update with your domain):"
    echo "  Frontend:     http://<YOUR-DOMAIN>:3000"
    echo "  Backend API:  http://<YOUR-DOMAIN>:8181"
    echo "  API Docs:     http://<YOUR-DOMAIN>:8181/docs"
    echo ""
    echo "Useful commands:"
    echo "  View logs:    ssh $VPS_HOST 'cd $VPS_DIR && docker-compose logs -f'"
    echo "  Restart:      ssh $VPS_HOST 'cd $VPS_DIR && docker-compose restart'"
    echo "  Stop:         ssh $VPS_HOST 'cd $VPS_DIR && docker-compose down'"
    echo ""
}

# =============================================================================
# MAIN DEPLOYMENT FLOW
# =============================================================================

main() {
    echo ""
    echo "=========================================="
    echo "IAFactory RAG-DZ Deployment"
    echo "=========================================="
    echo ""

    check_requirements
    create_vps_directory
    sync_files
    setup_environment

    # Ask for confirmation before building
    read -p "Continue with building and starting services? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Deployment stopped by user"
        exit 0
    fi

    build_containers
    start_services
    verify_deployment

    echo ""
    log_success "=========================================="
    log_success "Deployment Complete!"
    log_success "=========================================="
    echo ""

    show_info
}

# Run main function
main "$@"
