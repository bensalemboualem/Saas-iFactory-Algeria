#!/bin/bash
set -e

# =============================================================================
# IAFactory Video Platform - Initial Setup Script
# =============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║     ██╗ █████╗ ███████╗ █████╗  ██████╗████████╗ ██████╗ ██╗   ║"
echo "║     ██║██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██║   ║"
echo "║     ██║███████║█████╗  ███████║██║        ██║   ██║   ██║██║   ║"
echo "║     ██║██╔══██║██╔══╝  ██╔══██║██║        ██║   ██║   ██║╚═╝   ║"
echo "║     ██║██║  ██║██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██╗   ║"
echo "║     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝   ║"
echo "║                                                                  ║"
echo "║              VIDEO PLATFORM - Initial Setup                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log_info() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo ""
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
}

# Check system requirements
check_system() {
    log_step "Checking System Requirements"

    # Check OS
    OS=$(uname -s)
    log_info "Operating System: $OS"

    # Check Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
        log_info "Docker: $DOCKER_VERSION"
    else
        log_error "Docker is not installed. Please install Docker first."
        echo "  Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check Docker Compose
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version --short)
        log_info "Docker Compose: $COMPOSE_VERSION"
    elif command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
        log_info "Docker Compose: $COMPOSE_VERSION"
    else
        log_error "Docker Compose is not installed."
        exit 1
    fi

    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        log_info "Git: $GIT_VERSION"
    else
        log_warn "Git is not installed (optional)"
    fi

    # Check available disk space
    AVAILABLE_SPACE=$(df -h "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    log_info "Available disk space: $AVAILABLE_SPACE"
}

# Create directory structure
create_directories() {
    log_step "Creating Directory Structure"

    DIRS=(
        "data/postgres"
        "data/redis"
        "data/minio"
        "data/uploads"
        "data/exports"
        "logs"
        "backups"
    )

    for dir in "${DIRS[@]}"; do
        mkdir -p "$PROJECT_ROOT/$dir"
        log_info "Created: $dir"
    done
}

# Setup environment files
setup_environment() {
    log_step "Setting Up Environment"

    ENV_FILE="$PROJECT_ROOT/.env"

    if [ -f "$ENV_FILE" ]; then
        log_warn ".env file already exists. Skipping..."
        read -p "Do you want to overwrite it? (y/N): " OVERWRITE
        if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
            return
        fi
    fi

    # Generate secrets
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET=$(openssl rand -hex 32)
    POSTGRES_PASSWORD=$(openssl rand -hex 16)
    MINIO_SECRET=$(openssl rand -hex 16)

    cat > "$ENV_FILE" << EOF
# =============================================================================
# IAFactory Video Platform - Environment Configuration
# Generated on: $(date)
# =============================================================================

# Application
APP_NAME=IAFactory Video Platform
APP_ENV=development
DEBUG=true
SECRET_KEY=$SECRET_KEY

# Database
DATABASE_URL=postgresql+asyncpg://postgres:$POSTGRES_PASSWORD@postgres:5432/iafactory_video
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=iafactory_video

# Redis
REDIS_URL=redis://redis:6379/0

# MinIO (S3-compatible storage)
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=iafactory
MINIO_SECRET_KEY=$MINIO_SECRET
MINIO_SECURE=false

# JWT Authentication
JWT_SECRET=$JWT_SECRET
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# =============================================================================
# AI Provider API Keys (Add your keys here)
# =============================================================================

# OpenAI (GPT-4, DALL-E, Whisper, TTS)
OPENAI_API_KEY=

# Anthropic (Claude)
ANTHROPIC_API_KEY=

# ElevenLabs (Voice synthesis)
ELEVENLABS_API_KEY=

# Replicate (Flux, SDXL, SVD)
REPLICATE_API_TOKEN=

# Runway (Gen-3 video)
RUNWAY_API_KEY=

# Luma (Dream Machine)
LUMA_API_KEY=

# FAL.ai (Fast Flux)
FAL_KEY=

# Leonardo.ai
LEONARDO_API_KEY=

# HeyGen (Avatars)
HEYGEN_API_KEY=

# D-ID (Avatars)
DID_API_KEY=

# Suno (Music generation)
SUNO_API_KEY=

# Groq (Fast inference)
GROQ_API_KEY=

# DeepSeek
DEEPSEEK_API_KEY=

# =============================================================================
# Default Providers
# =============================================================================

DEFAULT_LLM_PROVIDER=openai
DEFAULT_IMAGE_PROVIDER=dalle
DEFAULT_VIDEO_PROVIDER=runway
DEFAULT_TTS_PROVIDER=elevenlabs
DEFAULT_STT_PROVIDER=whisper

# =============================================================================
# Social Media API Keys (for publishing)
# =============================================================================

# YouTube
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=

# TikTok
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=

# Instagram/Facebook
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=

# LinkedIn
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=

# Twitter/X
TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=

# =============================================================================
# Monitoring (Production)
# =============================================================================

# Sentry
SENTRY_DSN=

# Analytics
ANALYTICS_ID=

EOF

    log_info "Created .env file"
    log_warn "Please edit .env and add your API keys!"
}

# Setup Python virtual environment (for local development)
setup_python_env() {
    log_step "Setting Up Python Environment (Local Dev)"

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_info "Python: $PYTHON_VERSION"

        cd "$PROJECT_ROOT/backend"

        if [ ! -d "venv" ]; then
            python3 -m venv venv
            log_info "Created virtual environment"
        fi

        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        log_info "Installed Python dependencies"

        deactivate
    else
        log_warn "Python3 not found. Skipping local Python setup."
        log_info "You can still run the app with Docker."
    fi
}

# Setup Node.js environment (for local development)
setup_node_env() {
    log_step "Setting Up Node.js Environment (Local Dev)"

    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_info "Node.js: $NODE_VERSION"

        cd "$PROJECT_ROOT/frontend"

        if command -v pnpm &> /dev/null; then
            pnpm install
            log_info "Installed Node dependencies with pnpm"
        elif command -v npm &> /dev/null; then
            npm install
            log_info "Installed Node dependencies with npm"
        fi
    else
        log_warn "Node.js not found. Skipping local Node setup."
        log_info "You can still run the app with Docker."
    fi
}

# Start services with Docker
start_services() {
    log_step "Starting Services"

    cd "$PROJECT_ROOT"

    echo ""
    read -p "Start Docker services now? (Y/n): " START_DOCKER

    if [ "$START_DOCKER" != "n" ] && [ "$START_DOCKER" != "N" ]; then
        docker-compose up -d

        echo ""
        log_info "Services starting..."
        sleep 5

        # Show status
        docker-compose ps
    else
        log_info "Skipped. Run 'docker-compose up -d' to start services."
    fi
}

# Print final instructions
print_instructions() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Setup Complete!                              ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo ""
    echo "  1. Edit .env file and add your API keys:"
    echo -e "     ${BLUE}nano $PROJECT_ROOT/.env${NC}"
    echo ""
    echo "  2. Start the application:"
    echo -e "     ${BLUE}docker-compose up -d${NC}"
    echo ""
    echo "  3. Access the application:"
    echo -e "     Frontend:  ${BLUE}http://localhost:3000${NC}"
    echo -e "     API:       ${BLUE}http://localhost:8000${NC}"
    echo -e "     API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "     MinIO:     ${BLUE}http://localhost:9001${NC}"
    echo ""
    echo -e "${YELLOW}Important:${NC} Add at least one LLM API key (OpenAI, Anthropic, or Groq)"
    echo "  to enable AI features."
    echo ""
    echo -e "${CYAN}Useful Commands:${NC}"
    echo "  docker-compose logs -f      # View logs"
    echo "  docker-compose ps           # Check status"
    echo "  docker-compose down         # Stop services"
    echo "  ./scripts/deploy.sh         # Deploy to production"
    echo ""
}

# Main execution
main() {
    check_system
    create_directories
    setup_environment
    setup_python_env
    setup_node_env
    start_services
    print_instructions
}

main
