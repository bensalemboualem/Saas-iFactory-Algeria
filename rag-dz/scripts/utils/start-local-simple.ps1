# IAFactory RAG-DZ - Lancement Local
# PowerShell Script pour Windows

Write-Host "================================================================================"
Write-Host "LANCEMENT IAFactory RAG-DZ - Mode LOCAL"
Write-Host "================================================================================"
Write-Host ""

# Check Docker
Write-Host "[1/5] Verification Docker..."
try {
    $dockerVersion = docker --version
    Write-Host "OK Docker installe: $dockerVersion"
} catch {
    Write-Host "ERREUR: Docker non trouve"
    Write-Host "Installez Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
}

# Check Docker Compose
Write-Host ""
Write-Host "[2/5] Verification Docker Compose..."
try {
    $composeVersion = docker-compose --version
    Write-Host "OK Docker Compose installe: $composeVersion"
} catch {
    Write-Host "ERREUR: Docker Compose non trouve"
    exit 1
}

# Create .env.local if not exists
Write-Host ""
Write-Host "[3/5] Configuration environnement..."
if (-Not (Test-Path ".env.local")) {
    Write-Host "Creation .env.local..."

    $content = @"
# IAFactory RAG-DZ - Local Development
SOVEREIGNTY_REGION=DZ
SOVEREIGNTY_LABEL=Algerie
TZ=Africa/Algiers
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme123
POSTGRES_DB=iafactory_dz
DATABASE_URL=postgresql://postgres:changeme123@iafactory-postgres:5432/iafactory_dz
REDIS_URL=redis://iafactory-redis:6379/0
REDIS_PASSWORD=
QDRANT_URL=http://iafactory-qdrant:6333
QDRANT_API_KEY=
GROQ_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
DEEPSEEK_API_KEY=
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production
PORT=8180
HOST=0.0.0.0
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"@

    $content | Out-File -FilePath ".env.local" -Encoding ASCII
    Write-Host "OK .env.local cree"
} else {
    Write-Host "OK .env.local existe"
}

# Stop existing containers
Write-Host ""
Write-Host "[4/5] Nettoyage conteneurs existants..."
docker-compose down 2>$null
Write-Host "OK Conteneurs arretes"

# Start services
Write-Host ""
Write-Host "[5/5] Demarrage services Docker..."
Write-Host "Attente 2-3 minutes au premier lancement..."
Write-Host ""

docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "OK Services demarres!"
    Write-Host ""
    Write-Host "Attente du demarrage complet (30 secondes)..."
    Start-Sleep -Seconds 30

    Write-Host ""
    Write-Host "Status des services:"
    docker-compose ps

    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "IAFactory RAG-DZ est EN LIGNE!"
    Write-Host "================================================================================"
    Write-Host ""
    Write-Host "URLS disponibles:"
    Write-Host "  Health Check: http://localhost:8180/health"
    Write-Host "  API Docs:     http://localhost:8180/docs"
    Write-Host "  API Backend:  http://localhost:8180/api/"
    Write-Host ""
    Write-Host "Bases de donnees:"
    Write-Host "  PostgreSQL:   localhost:6330"
    Write-Host "  Redis:        localhost:6331"
    Write-Host "  Qdrant:       localhost:6332"
    Write-Host ""
    Write-Host "Commandes utiles:"
    Write-Host "  Logs:         docker-compose logs -f"
    Write-Host "  Arreter:      docker-compose down"
    Write-Host "  Redemarrer:   docker-compose restart"
    Write-Host ""
    Write-Host "================================================================================"

} else {
    Write-Host ""
    Write-Host "ERREUR lors du demarrage"
    Write-Host "Verifiez les logs: docker-compose logs"
    exit 1
}
