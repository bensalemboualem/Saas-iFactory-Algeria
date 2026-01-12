# =============================================================================
# IAFactory Video Platform - Makefile
# =============================================================================

.PHONY: help dev prod down logs clean build test

# Default target
help:
	@echo "IAFactory Video Platform - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-full     - Start with all services (frontend, workers)"
	@echo "  make logs         - View logs"
	@echo "  make down         - Stop all services"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment"
	@echo "  make prod-build   - Build and start production"
	@echo ""
	@echo "Utilities:"
	@echo "  make build        - Build all containers"
	@echo "  make clean        - Remove all containers and volumes"
	@echo "  make test         - Run tests"
	@echo "  make migrate      - Run database migrations"
	@echo "  make shell        - Open shell in backend container"
	@echo ""

# Development
dev:
	docker-compose up -d postgres redis
	@echo "Infrastructure started. Run backend manually:"
	@echo "  cd backend && uvicorn app.main:app --reload"

dev-full:
	docker-compose --profile full up -d

# Production
prod:
	docker-compose -f docker-compose.prod.yml up -d

prod-build:
	docker-compose -f docker-compose.prod.yml up -d --build

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-worker:
	docker-compose logs -f celery-worker

# Stop
down:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Build
build:
	docker-compose build

build-prod:
	docker-compose -f docker-compose.prod.yml build

# Clean
clean:
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.prod.yml down -v --remove-orphans 2>/dev/null || true
	docker system prune -f

# Test
test:
	cd backend && pytest -v

test-cov:
	cd backend && pytest --cov=app --cov-report=html

# Database
migrate:
	docker-compose exec backend alembic upgrade head

migrate-create:
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

# Shell
shell:
	docker-compose exec backend /bin/bash

shell-db:
	docker-compose exec postgres psql -U iafactory -d video_platform

shell-redis:
	docker-compose exec redis redis-cli

# Frontend
frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-install:
	cd frontend && npm install

# Backend
backend-dev:
	cd backend && uvicorn app.main:app --reload

backend-install:
	cd backend && pip install -r requirements.txt

# Initial setup
setup:
	cp .env.example .env
	cp backend/.env.example backend/.env
	@echo ""
	@echo "Environment files created!"
	@echo "Please edit .env and backend/.env with your API keys"
	@echo ""
	@echo "Then run: make dev"
