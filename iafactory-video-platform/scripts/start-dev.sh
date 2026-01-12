#!/bin/bash
# =============================================================================
# IAFactory Video Platform - Development Startup Script
# =============================================================================

echo "🚀 Starting IAFactory Video Platform (Development Mode)"
echo "========================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start infrastructure services
echo "📦 Starting infrastructure services (PostgreSQL, Redis)..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check PostgreSQL
echo "🔍 Checking PostgreSQL..."
docker-compose exec -T postgres pg_isready -U iafactory || {
    echo "❌ PostgreSQL is not ready"
    exit 1
}
echo "✅ PostgreSQL is ready"

# Check Redis
echo "🔍 Checking Redis..."
docker-compose exec -T redis redis-cli ping || {
    echo "❌ Redis is not ready"
    exit 1
}
echo "✅ Redis is ready"

echo ""
echo "========================================================"
echo "✅ Infrastructure is ready!"
echo ""
echo "To start the backend:"
echo "  cd backend && python -m uvicorn app.main:app --reload"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Or run everything with Docker:"
echo "  docker-compose --profile full up -d"
echo "========================================================"
