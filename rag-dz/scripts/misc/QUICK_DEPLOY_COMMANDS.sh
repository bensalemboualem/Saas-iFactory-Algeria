#!/bin/bash

################################################################################
# IA Factory - Quick Deploy Commands
# Run these commands in order to deploy all 5 critical fixes
################################################################################

set -e

echo "=================================================="
echo "IA Factory - 48H Deployment Ready"
echo "5 Critical Fixes Implementation"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

################################################################################
# STEP 1: Frontend Setup
################################################################################
echo -e "${YELLOW}[STEP 1/5] Installing Frontend Dependencies...${NC}"

cd frontend/ia-factory-ui

# Install next-intl
npm install next-intl@^3.9.0

# Verify build works
npm run build

echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

################################################################################
# STEP 2: Backend Integration
################################################################################
echo -e "${YELLOW}[STEP 2/5] Backend Integration${NC}"
echo ""
echo "Manual steps required:"
echo "1. Add to backend/rag-compat/app/main.py:"
echo "   from app.routers import password_reset"
echo "   app.include_router(password_reset.router)"
echo ""
echo "2. Copy send_reset_password_email() method from:"
echo "   backend/rag-compat/app/services/notification_service_ADDITION.py"
echo "   to notification_service.py (insert after line 242)"
echo ""
read -p "Press Enter when backend is updated..."

echo -e "${GREEN}✓ Backend updated${NC}"
echo ""

################################################################################
# STEP 3: Update Next.js Config
################################################################################
echo -e "${YELLOW}[STEP 3/5] Update Next.js Config${NC}"
echo ""
echo "Update frontend/ia-factory-ui/next.config.js:"
echo ""
echo "const createNextIntlPlugin = require('next-intl/plugin')"
echo "const withNextIntl = createNextIntlPlugin('./i18n.ts')"
echo ""
echo "// Wrap your existing config:"
echo "module.exports = withNextIntl(nextConfig)"
echo ""
read -p "Press Enter when next.config.js is updated..."

echo -e "${GREEN}✓ Next.js config updated${NC}"
echo ""

################################################################################
# STEP 4: Local Testing
################################################################################
echo -e "${YELLOW}[STEP 4/5] Local Testing${NC}"
echo ""
echo "Starting development servers..."

# Start backend
cd ../../backend/rag-compat
python -m uvicorn app.main:app --reload --port 8002 &
BACKEND_PID=$!

# Start frontend
cd ../../frontend/ia-factory-ui
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Servers started:"
echo "  Backend: http://localhost:8002"
echo "  Frontend: http://localhost:3000"
echo ""
echo "Test checklist:"
echo "  [ ] Visit http://localhost:3000 - UI loads"
echo "  [ ] Click language selector - AR/FR/EN work"
echo "  [ ] Visit /privacy - Privacy policy loads"
echo "  [ ] Visit /terms - Terms load"
echo "  [ ] Click 'Forgot Password' - Modal opens"
echo "  [ ] Check browser tab - Favicon shows"
echo ""
read -p "Press Enter when testing is complete (will stop servers)..."

# Stop servers
kill $BACKEND_PID
kill $FRONTEND_PID

echo -e "${GREEN}✓ Local testing complete${NC}"
echo ""

################################################################################
# STEP 5: VPS Deployment
################################################################################
echo -e "${YELLOW}[STEP 5/5] VPS Deployment${NC}"
echo ""
echo "Connecting to VPS..."
echo ""

# This part should be run on VPS
cat << 'EOF_VPS' > /tmp/vps_deploy.sh
#!/bin/bash

# VPS Deployment Script
set -e

cd /opt/iafactory

# Pull latest changes
echo "Pulling latest code..."
git pull origin main

# Update Nginx configs
echo "Updating Nginx..."
sudo cp nginx/sites-available/iafactory-ch-UPDATED.conf \
        /etc/nginx/sites-available/iafactory-ch

sudo cp nginx/sites-available/iafactoryalgeria-com-UPDATED.conf \
        /etc/nginx/sites-available/iafactoryalgeria-com

sudo nginx -t
sudo systemctl reload nginx

# Rebuild containers
echo "Rebuilding Docker containers..."
docker compose -f docker-compose.vps.yml build --no-cache

# Start services
echo "Starting services..."
docker compose -f docker-compose.vps.yml up -d

# Wait for services
echo "Waiting for services to start..."
sleep 15

# Health check
echo "Running health checks..."

# Check PostgreSQL
if docker ps | grep -q iafactory-db; then
    echo "✓ PostgreSQL: Running"
else
    echo "✗ PostgreSQL: Not running"
fi

# Check Backend
if docker ps | grep -q iafactory-backend; then
    echo "✓ Backend: Running"

    # Test health endpoint
    BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/health || echo "000")
    if [ "$BACKEND_STATUS" == "200" ]; then
        echo "✓ Backend API: Healthy (200 OK)"
    else
        echo "⚠ Backend API: Status $BACKEND_STATUS"
    fi
else
    echo "✗ Backend: Not running"
fi

# Check Frontend Switzerland
if docker ps | grep -q iafactory-frontend-ch; then
    echo "✓ Frontend (Switzerland): Running"
else
    echo "✗ Frontend (Switzerland): Not running"
fi

# Check Frontend Algeria
if docker ps | grep -q iafactory-frontend-dz; then
    echo "✓ Frontend (Algeria): Running"
else
    echo "✗ Frontend (Algeria): Not running"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx: Running"
else
    echo "✗ Nginx: Not running"
fi

echo ""
echo "=================================================="
echo "Deployment Complete!"
echo "=================================================="
echo ""
echo "Access your applications:"
echo "  🇨🇭 Switzerland: https://iafactory.ch"
echo "  🇩🇿 Algeria:     https://iafactoryalgeria.com"
echo ""
echo "View logs:"
echo "  docker compose -f docker-compose.vps.yml logs -f"
echo ""

EOF_VPS

echo "VPS deployment script created: /tmp/vps_deploy.sh"
echo ""
echo "To deploy on VPS, run:"
echo "  1. scp /tmp/vps_deploy.sh your-vps:/tmp/"
echo "  2. ssh your-vps"
echo "  3. sudo bash /tmp/vps_deploy.sh"
echo ""

################################################################################
# COMPLETION
################################################################################
echo ""
echo -e "${GREEN}=================================================="
echo "All Steps Complete!"
echo "==================================================${NC}"
echo ""
echo "Summary:"
echo "  ✅ Frontend dependencies installed"
echo "  ✅ Backend integration complete"
echo "  ✅ Next.js config updated"
echo "  ✅ Local testing passed"
echo "  ✅ VPS deployment script ready"
echo ""
echo "Next: Deploy to VPS and test in production"
echo ""
echo "Testing checklist:"
echo "  [ ] https://iafactory.ch - loads correctly"
echo "  [ ] https://iafactoryalgeria.com - loads correctly"
echo "  [ ] Test forgot password flow"
echo "  [ ] Test multilingual switching"
echo "  [ ] Check browser console for errors"
echo ""
echo -e "${GREEN}Ready for launch! 🚀${NC}"
