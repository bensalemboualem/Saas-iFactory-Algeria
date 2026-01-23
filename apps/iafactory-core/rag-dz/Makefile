# Makefile pour RAG.dz
.PHONY: help start stop restart logs clean test test-backend test-frontend setup ports

# Couleurs pour output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Affiche l'aide
	@echo "$(GREEN)RAG.dz - Commandes disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Configuration initiale
	@echo "$(GREEN)Configuration initiale...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)✓ .env créé. Éditez-le avant de continuer!$(NC)"; \
	else \
		echo "$(YELLOW)✓ .env existe déjà$(NC)"; \
	fi

# ========================================
# Gestion des Services
# ========================================

start: ## Démarre tous les services (sauf Bolt)
	@echo "$(GREEN)Démarrage de RAG.dz...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services démarrés$(NC)"
	@make ports

start-all: ## Démarre TOUS les services (inclus Bolt)
	@echo "$(GREEN)Démarrage de TOUS les services...$(NC)"
	docker-compose --profile bolt up -d
	@echo "$(GREEN)✓ Tous les services démarrés$(NC)"
	@make ports

start-archon: ## Démarre uniquement Archon UI (port 3747)
	@echo "$(BLUE)Démarrage Archon UI...$(NC)"
	docker-compose up -d frontend
	@echo "$(GREEN)✓ Archon UI: http://localhost:3747$(NC)"

start-ragui: ## Démarre uniquement RAG-UI Simple (port 5183)
	@echo "$(BLUE)Démarrage RAG-UI Simple...$(NC)"
	docker-compose up -d rag-ui
	@echo "$(GREEN)✓ RAG-UI: http://localhost:5183$(NC)"

start-bolt: ## Démarre uniquement Bolt.diy (port 5184)
	@echo "$(BLUE)Démarrage Bolt.diy...$(NC)"
	docker-compose --profile bolt up -d bolt-diy
	@echo "$(GREEN)✓ Bolt.diy: http://localhost:5184$(NC)"

start-monitoring: ## Démarre Prometheus + Grafana
	@echo "$(BLUE)Démarrage monitoring...$(NC)"
	docker-compose --profile monitoring up -d iafactory-prometheus iafactory-grafana
	@echo "$(GREEN)✓ Prometheus: http://localhost:8187$(NC)"
	@echo "$(GREEN)✓ Grafana   : http://localhost:8188$(NC)"

stop-monitoring: ## Arrête Prometheus + Grafana
	@echo "$(YELLOW)Arrêt monitoring...$(NC)"
	docker-compose --profile monitoring stop iafactory-prometheus iafactory-grafana
	@echo "$(GREEN)✓ Monitoring arrêté$(NC)"

# ========================================
# Autres commandes
# ========================================

stop: ## Arrête tous les services
	@echo "$(YELLOW)Arrêt des services...$(NC)"
	docker-compose --profile bolt down
	@echo "$(GREEN)✓ Services arrêtés$(NC)"

restart: ## Redémarre tous les services
	@make stop
	@make start

restart-all: ## Redémarre TOUS les services (inclus Bolt)
	@make stop
	@make start-all

# ========================================
# Logs
# ========================================

logs: ## Affiche les logs (tous les services)
	docker-compose logs -f

logs-backend: ## Logs backend uniquement
	docker-compose logs -f backend

logs-archon: ## Logs Archon UI
	docker-compose logs -f frontend

logs-ragui: ## Logs RAG-UI Simple
	docker-compose logs -f rag-ui

logs-bolt: ## Logs Bolt.diy
	docker-compose logs -f bolt-diy

logs-db: ## Logs PostgreSQL
	docker-compose logs -f postgres

load-test: ## Lance le test de charge k6 (ex: make load-test SCENARIO=orchestrator-smoke)
	@SCENARIO=$${SCENARIO:-orchestrator-smoke} ./scripts/load-test.sh $$SCENARIO

# ========================================
# Status et Tests
# ========================================

status: ## Affiche le status des services
	@echo "$(GREEN)Status des services:$(NC)"
	@docker-compose ps

ports: ## Test tous les ports et affiche les URLs
	@echo "$(GREEN)Test de tous les ports...$(NC)"
	@python test_all_ports.py

urls: ## Affiche les URLs des services
	@echo "$(GREEN)═══════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)        RAG.dz - Interfaces Disponibles       $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(BLUE)🎨 Frontends:$(NC)"
	@echo "  • Archon UI:       http://localhost:3747"
	@echo "  • RAG-UI Simple:   http://localhost:5183"
	@echo "  • Bolt.diy:        http://localhost:5184"
	@echo ""
	@echo "$(BLUE)⚡ Backend & API:$(NC)"
	@echo "  • API Docs:        http://localhost:8188/docs"
	@echo "  • Health Check:    http://localhost:8188/health"
	@echo "  • Metrics:         http://localhost:8188/metrics"
	@echo ""
	@echo "$(BLUE)📊 Monitoring:$(NC)"
	@echo "  • Grafana:         http://localhost:3011 (admin/admin)"
	@echo "  • Prometheus:      http://localhost:9090"
	@echo "  • Qdrant:          http://localhost:6333/dashboard"
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════$(NC)"

health: ## Vérifie la santé des services
	@echo "$(GREEN)Vérification santé...$(NC)"
	@curl -s http://localhost:8188/health | jq '.' || echo "Backend non disponible"

test: ## Lance tous les tests
	@echo "$(GREEN)Lancement de tous les tests...$(NC)"
	@make test-ports
	@make test-backend
	@make test-frontend

test-ports: ## Test de tous les ports
	@python test_all_ports.py

test-backend: ## Tests backend (pytest)
	@echo "$(GREEN)Tests backend...$(NC)"
	cd rag-compat && pytest -v --cov=app

test-frontend: ## Tests frontend (vitest)
	@echo "$(GREEN)Tests frontend...$(NC)"
	cd rag-ui && npm run test

test-security: ## Tests de sécurité uniquement
	cd rag-compat && pytest -v -m security

install-backend: ## Installe dépendances backend
	cd rag-compat && pip install -r requirements.txt

install-frontend: ## Installe dépendances frontend
	cd rag-ui && npm install

clean: ## Nettoie les volumes et images
	@echo "$(YELLOW)Nettoyage des volumes...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)✓ Nettoyage terminé$(NC)"

clean-cache: ## Vide le cache Redis
	@echo "$(YELLOW)Vidage du cache Redis...$(NC)"
	docker-compose exec redis redis-cli FLUSHALL
	@echo "$(GREEN)✓ Cache vidé$(NC)"

db-shell: ## Ouvre un shell PostgreSQL
	docker-compose exec postgres psql -U postgres -d archon

redis-cli: ## Ouvre redis-cli
	docker-compose exec redis redis-cli

backup-db: ## Backup PostgreSQL
	@echo "$(GREEN)Backup PostgreSQL...$(NC)"
	docker-compose exec postgres pg_dump -U postgres archon > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Backup créé$(NC)"

restore-db: ## Restore PostgreSQL (usage: make restore-db FILE=backup.sql)
	@echo "$(YELLOW)Restore PostgreSQL...$(NC)"
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make restore-db FILE=backup.sql"; \
		exit 1; \
	fi
	docker-compose exec -T postgres psql -U postgres archon < $(FILE)
	@echo "$(GREEN)✓ Restore terminé$(NC)"

dev-backend: ## Mode dev backend (hot reload)
	cd rag-compat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8188

dev-frontend: ## Mode dev frontend (hot reload)
	cd rag-ui && npm run dev

metrics: ## Affiche les métriques Prometheus
	@curl -s http://localhost:8188/metrics | head -20

cache-stats: ## Stats du cache Redis
	@docker-compose exec redis redis-cli INFO stats | grep -E "(keyspace_hits|keyspace_misses)"

# Production
prod-build: ## Build pour production
	docker-compose -f docker-compose.yml build

prod-deploy: ## Deploy en production
	@echo "$(YELLOW)Deploy production...$(NC)"
	docker-compose -f docker-compose.yml up -d
	@echo "$(GREEN)✓ Déployé$(NC)"

# Qualité du code
lint-backend: ## Lint backend (ruff)
	cd rag-compat && ruff check .

lint-frontend: ## Lint frontend (eslint)
	cd rag-ui && npm run lint

format-backend: ## Format backend (black)
	cd rag-compat && black .

format-frontend: ## Format frontend (prettier)
	cd rag-ui && npm run format

# Documentation
docs-api: ## Ouvre la doc API
	@echo "$(GREEN)Documentation API:$(NC)"
	@echo "  http://localhost:8188/docs"
	@xdg-open http://localhost:8188/docs 2>/dev/null || open http://localhost:8188/docs 2>/dev/null || echo "Ouvrez manuellement"

# Monitoring
grafana-open: ## Ouvre Grafana
	@xdg-open http://localhost:3011 2>/dev/null || open http://localhost:3011 2>/dev/null || echo "http://localhost:3011"

prometheus-open: ## Ouvre Prometheus
	@xdg-open http://localhost:9090 2>/dev/null || open http://localhost:9090 2>/dev/null || echo "http://localhost:9090"

# ========================================
# 🔧 MIGRATION & AUDIT (décembre 2024)
# ========================================

audit: ## Affiche le rapport d'audit
	@echo "$(GREEN)📊 Rapport d'audit disponible:$(NC)"
	@echo "  $(YELLOW)docs/AUDIT.md$(NC)"
	@cat docs/AUDIT.md | head -100

migrate-p0: ## 🔴 Execute migration P0 (CRITIQUE - sécurité)
	@echo "$(RED)🔴 MIGRATION P0 - Actions critiques$(NC)"
	@echo "Actions: suppression rag-compat, node_modules, .env exposés"
	@echo ""
	@if [ -f scripts/migration/p0-critical.ps1 ]; then \
		powershell -ExecutionPolicy Bypass -File scripts/migration/p0-critical.ps1; \
	else \
		echo "Script non trouvé. Exécuter manuellement:"; \
		echo "  rm -rf services/backend/rag-compat/"; \
		echo "  git rm -r --cached apps/video-studio/frontend/node_modules/"; \
		echo "  git rm --cached apps/interview/.env.local"; \
	fi

migrate-p1: ## 🟠 Execute migration P1 (réorganisation)
	@echo "$(YELLOW)🟠 MIGRATION P1 - Réorganisation$(NC)"
	@echo "Actions: archivage apps vides, consolidation shared/"
	@powershell -ExecutionPolicy Bypass -File scripts/migration/p1-reorganize.ps1

migrate-p2: ## 🟡 Execute migration P2 (documentation)
	@echo "$(BLUE)🟡 MIGRATION P2 - Documentation$(NC)"
	@echo "Actions: génération README, .env.example"
	@powershell -ExecutionPolicy Bypass -File scripts/migration/p2-documentation.ps1

migrate-all: migrate-p0 migrate-p1 migrate-p2 ## Execute toutes les migrations (P0 → P2)
	@echo "$(GREEN)✅ Toutes les migrations exécutées$(NC)"
	@echo "N'oubliez pas: git add -A && git commit -m 'chore: complete P0-P2 migration'"

migrate-status: ## Affiche le statut de migration
	@echo "$(GREEN)📋 STATUT MIGRATION$(NC)"
	@echo ""
	@echo "P0 - Critique:"
	@if [ -d "services/backend/rag-compat" ]; then echo "  $(RED)❌ rag-compat existe encore$(NC)"; else echo "  $(GREEN)✅ rag-compat supprimé$(NC)"; fi
	@if [ -d "apps/video-studio/frontend/node_modules" ]; then echo "  $(RED)❌ node_modules commité$(NC)"; else echo "  $(GREEN)✅ node_modules OK$(NC)"; fi
	@if [ -f "apps/interview/.env.local" ]; then echo "  $(RED)❌ .env.local exposé$(NC)"; else echo "  $(GREEN)✅ secrets protégés$(NC)"; fi
	@echo ""
	@echo "P1 - Réorganisation:"
	@if [ -d "apps/_archived" ]; then echo "  $(GREEN)✅ apps/_archived créé$(NC)"; else echo "  $(YELLOW)⏳ apps/_archived à créer$(NC)"; fi
	@if [ -d "packages/shared" ]; then echo "  $(GREEN)✅ packages/shared créé$(NC)"; else echo "  $(YELLOW)⏳ shared à consolider$(NC)"; fi
	@echo ""
	@echo "P2 - Documentation:"
	@echo "  README: $$(find apps -maxdepth 2 -name 'README.md' | wc -l) fichiers"
	@echo "  .env.example: $$(find apps -maxdepth 2 -name '.env.example' | wc -l) fichiers"

clean-git-cache: ## Nettoie le cache git (après suppression fichiers)
	@echo "$(YELLOW)Nettoyage cache git...$(NC)"
	git rm -r --cached . 2>/dev/null || true
	git add .
	@echo "$(GREEN)✅ Cache nettoyé. Faire 'git status' pour vérifier$(NC)"
