#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Automated deployment script for IA Factory on a VPS
# Usage (on the VPS as root or sudo):
#   curl -fsSL https://example.com/deploy-vps-auto.sh -o deploy-vps-auto.sh
#   chmod +x deploy-vps-auto.sh
#   ./deploy-vps-auto.sh --domain yourdomain.tld --email admin@yourdomain.tld

LOGFILE=/var/log/iafactory-deploy.log
exec > >(tee -a "$LOGFILE") 2>&1

function usage() {
  cat <<'USAGE'
deploy-vps-auto.sh - Deploy IA Factory to a VPS (assumes Debian/Ubuntu)

Usage: sudo ./deploy-vps-auto.sh [--domain <domain>] [--email <email>] [--git-ref <ref>] [--no-cert]

Options:
  --domain   Primary domain (e.g., iafactory.example.com). Optional, but recommended for SSL.
  --email    Email address for Let's Encrypt registration (required if --domain set).
  --git-ref  Git reference (branch/tag/commit) to checkout. Defaults to 'main'.
  --no-cert  Skip obtaining TLS certificates (useful for testing/local deploy).
  -h, --help Show this help and exit.
USAGE
  exit 1
}

DOMAIN=""
EMAIL=""
GIT_REF="main"
NO_CERT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain)
      DOMAIN="$2"; shift 2; ;;
    --email)
      EMAIL="$2"; shift 2; ;;
    --git-ref)
      GIT_REF="$2"; shift 2; ;;
    --no-cert)
      NO_CERT=true; shift 1; ;;
    -h|--help)
      usage; ;;
    *)
      echo "Unknown option: $1"; usage; ;;
  esac
done

function require_root() {
  if [[ $(id -u) -ne 0 ]]; then
    echo "This script must be run as root (sudo)." >&2
    exit 1
  fi
}

function install_prereqs() {
  echo "==> Install system packages (Docker, git, nginx, certbot)"
  apt-get update
  apt-get install -y ca-certificates curl gnupg lsb-release git ufw jq software-properties-common

  # Docker
  if ! command -v docker >/dev/null 2>&1; then
    echo "Installing Docker"
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
      | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  else
    echo "Docker already installed"
  fi

  # Nginx & certbot
  if ! command -v nginx >/dev/null 2>&1; then
    apt-get install -y nginx
  fi
  if [[ "$NO_CERT" = false ]] && ! command -v certbot >/dev/null 2>&1; then
    apt-get install -y certbot python3-certbot-nginx
  fi
}

function clone_repo() {
  echo "==> Clone or update repository"
  TARGET_DIR=/opt/iafactory
  if [[ -d "$TARGET_DIR/.git" ]]; then
    echo "Repository exists - pulling"
    cd "$TARGET_DIR"
    git fetch origin "$GIT_REF" && git checkout "$GIT_REF" && git pull || true
  else
    echo "Cloning repository into $TARGET_DIR"
    git clone https://github.com/bensalemboualem/rag-dz.git "$TARGET_DIR"
    cd "$TARGET_DIR"
    git checkout "$GIT_REF" || true
  fi
}

function generate_secret() {
  # Generate a 32-byte hex secret
  openssl rand -hex 32
}

function ensure_env() {
  echo "==> Ensure .env has required variables"
  cd /opt/iafactory || exit 1

  if [[ ! -f .env ]]; then
    if [[ -f .env.example ]]; then
      cp .env.example .env
    else
      touch .env
    fi
  fi
  cp .env .env.bak_$(date +%s)

  # Insert or update secrets
  if ! grep -q '^API_SECRET_KEY=' .env; then
    echo "API_SECRET_KEY=$(generate_secret)" >> .env
    echo "Generated API_SECRET_KEY"
  fi
  if ! grep -q '^JWT_SECRET_KEY=' .env; then
    echo "JWT_SECRET_KEY=$(generate_secret)" >> .env
    echo "Generated JWT_SECRET_KEY"
  fi
  if ! grep -q '^POSTGRES_PASSWORD=' .env; then
    echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env
    echo "Generated POSTGRES_PASSWORD"
  fi

  # Ensure POSTGRES_URL is present for prod compose
  if ! grep -q '^POSTGRES_URL=' .env; then
    PG_USER=$(grep -m1 '^POSTGRES_USER=' .env | cut -d= -f2 || echo "postgres")
    PG_PASS=$(grep -m1 '^POSTGRES_PASSWORD=' .env | cut -d= -f2 || echo "${POSTGRES_PASSWORD:-}")
    PG_DB=$(grep -m1 '^POSTGRES_DB=' .env | cut -d= -f2 || echo "iafactory_dz")
    echo "POSTGRES_URL=postgresql://$PG_USER:$PG_PASS@postgres-prod:5432/$PG_DB" >> .env
    echo "Set POSTGRES_URL"
  fi

  # Ensure VITE front-end vars
  if ! grep -q '^VITE_API_URL=' .env; then
    echo "VITE_API_URL=http://localhost:8180" >> .env
  fi
  if ! grep -q '^VITE_WS_URL=' .env; then
    echo "VITE_WS_URL=ws://localhost:8180" >> .env
  fi

  # Ensure .env.local is ignored by git
  if ! git check-ignore -q .env.local 2>/dev/null; then
    echo ".env.local" >> .git/info/exclude || true
  fi
}

function docker_compose_up() {
  echo "==> Build and start docker compose (prod)"
  cd /opt/iafactory
  if [[ -f docker-compose.prod.yml ]]; then
    docker compose -f docker-compose.prod.yml pull || true
    docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
  else
    echo "docker-compose.prod.yml not found in repo. Aborting" >&2
    exit 1
  fi
  sleep 5
}

function run_migrations() {
  echo "==> Running database migrations"
  cd /opt/iafactory
  # Execute SQL files in migrations or infrastructure
  for sql in backend/rag-compat/migrations/*.sql infrastructure/sql/*.sql; do
    if [[ -f $sql ]]; then
       echo "Applying $sql"
       docker exec -i iaf-dz-postgres psql -U postgres -d iafactory_dz < "$sql" || true
    fi
  done
}

function configure_nginx() {
  if [[ -z "$DOMAIN" || "$NO_CERT" = true ]]; then
    echo "Skipping Nginx domain configuration or certbot (no domain provided or disabled)"
    return
  fi

  echo "==> Configuring Nginx for domain $DOMAIN"
  if [[ -f /etc/nginx/sites-available/iafactory ]]; then
    echo "Existing nginx vhost found - backing up"
    mv /etc/nginx/sites-available/iafactory /etc/nginx/sites-available/iafactory.bak || true
  fi

  cat > /etc/nginx/sites-available/iafactory <<EOF
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  server_name $DOMAIN www.$DOMAIN;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name $DOMAIN;
  # Let certbot manage the cert paths (certbot --nginx will update)
  root /opt/iafactory/landing;

  location / {
    try_files $uri @app;
  }
  location @app {
    proxy_pass http://127.0.0.1:8182; # Hub, routed by path if needed
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
  }

  location /api/ {
    proxy_pass http://127.0.0.1:8180;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
  }
  location /docs/ {
    proxy_pass http://127.0.0.1:8180/docs/;
  }
  location /studio/ {
    proxy_pass http://127.0.0.1:8184/;
  }
}
EOF

  ln -sf /etc/nginx/sites-available/iafactory /etc/nginx/sites-enabled/iafactory
  nginx -t
  systemctl reload nginx

  # Run certbot (if EMAIL provided)
  if [[ -n "$EMAIL" ]]; then
    echo "Running certbot for $DOMAIN and www.$DOMAIN"
    certbot --nginx --non-interactive --agree-tos --redirect -m "$EMAIL" -d "$DOMAIN" -d "www.$DOMAIN" || true
  else
    echo "No email specified; skipping certbot registration (if you want certs, run certbot manually later)"
  fi
}

function final_checks() {
  echo "==> Final health checks"
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
  echo "Backend health check:"
  sleep 2
  curl -s http://127.0.0.1:8180/health || true
  echo "Hub front-end available at: http://127.0.0.1:8182"
  if [[ -n "$DOMAIN" ]]; then
    echo "Hub public URL: https://$DOMAIN" | tee -a "$LOGFILE"
  fi
}

function post_deploy_notes() {
  echo "==> Post-deploy tips"
  echo "- If you see the hub page broken, run: docker compose -f docker-compose.frontend.yml build --no-cache iafactory-hub && docker compose -f docker-compose.frontend.yml up -d iafactory-hub"
  echo "- Use 'docker compose -f docker-compose.prod.yml logs -f' to inspect logs"
  echo "- Run health check curl http://localhost:8180/health and curl http://localhost:8182"
}

#################################################################
require_root
install_prereqs
clone_repo
ensure_env
docker_compose_up
run_migrations
configure_nginx
final_checks
post_deploy_notes

echo "Deployment completed. Logs: $LOGFILE"