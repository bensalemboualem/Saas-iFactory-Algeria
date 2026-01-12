#!/bin/bash
# Initialization script for RAG.dz demo environment

set -e

echo "🚀 RAG.dz Initialization Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Wait for services
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check PostgreSQL
echo -e "${YELLOW}📊 Checking PostgreSQL...${NC}"
docker exec ragdz-postgres pg_isready -U postgres || {
    echo -e "${RED}❌ PostgreSQL not ready${NC}"
    exit 1
}
echo -e "${GREEN}✅ PostgreSQL ready${NC}"

# Check Redis
echo -e "${YELLOW}💾 Checking Redis...${NC}"
docker exec ragdz-redis redis-cli ping || {
    echo -e "${RED}❌ Redis not ready${NC}"
    exit 1
}
echo -e "${GREEN}✅ Redis ready${NC}"

# Check Qdrant
echo -e "${YELLOW}🔍 Checking Qdrant...${NC}"
curl -s http://localhost:6333/healthz > /dev/null || {
    echo -e "${RED}❌ Qdrant not ready${NC}"
    exit 1
}
echo -e "${GREEN}✅ Qdrant ready${NC}"

# Check Backend
echo -e "${YELLOW}🖥️  Checking Backend API...${NC}"
curl -s http://localhost:8180/health > /dev/null || {
    echo -e "${RED}❌ Backend not ready${NC}"
    exit 1
}
echo -e "${GREEN}✅ Backend ready${NC}"

# Initialize demo tenant and API key
echo ""
echo -e "${YELLOW}👤 Creating demo tenant...${NC}"
docker exec -i ragdz-postgres psql -U postgres -d archon <<EOF
INSERT INTO tenants (id, name, plan, status)
VALUES ('00000000-0000-0000-0000-000000000001'::uuid, 'Demo Company', 'pro', 'active')
ON CONFLICT (id) DO NOTHING;

INSERT INTO api_keys (key_hash, tenant_id, name, plan, rate_limit_per_minute)
VALUES ('e8c4f7b8d9e6c8a5f3b2d1a9e7c6b5a4d3c2b1a0f9e8d7c6b5a4d3c2b1a0f9e8', '00000000-0000-0000-0000-000000000001'::uuid, 'Demo API Key', 'pro', 60)
ON CONFLICT (key_hash) DO NOTHING;
EOF

echo -e "${GREEN}✅ Demo tenant created${NC}"

# Pull Ollama model
echo ""
echo -e "${YELLOW}🤖 Pulling Ollama model (this may take a while)...${NC}"
docker exec ragdz-ollama ollama pull llama3.2 || {
    echo -e "${RED}⚠️  Failed to pull Ollama model (will continue)${NC}"
}

# Display credentials
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Initialization Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}📋 Demo Credentials:${NC}"
echo -e "   API Key: ${GREEN}ragdz_dev_demo_key_12345678901234567890${NC}"
echo -e "   Tenant:  ${GREEN}Demo Company${NC}"
echo -e "   Plan:    ${GREEN}Pro${NC}"
echo ""
echo -e "${YELLOW}🌐 Service URLs:${NC}"
echo -e "   Frontend:   ${GREEN}http://localhost:5173${NC}"
echo -e "   Backend:    ${GREEN}http://localhost:8180${NC}"
echo -e "   API Docs:   ${GREEN}http://localhost:8180/docs${NC}"
echo -e "   Prometheus: ${GREEN}http://localhost:9090${NC}"
echo -e "   Grafana:    ${GREEN}http://localhost:3001${NC} (admin/admin)"
echo ""
echo -e "${YELLOW}📝 Example API Call:${NC}"
echo -e '   curl -X POST http://localhost:8180/api/upload \\'
echo -e '     -H "X-API-Key: ragdz_dev_demo_key_12345678901234567890" \\'
echo -e '     -F "file=@document.txt"'
echo ""
