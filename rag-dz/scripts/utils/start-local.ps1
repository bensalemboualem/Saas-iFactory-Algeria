# ==============================================
# LANCEMENT LOCAL - IAFactory RAG-DZ
# ==============================================
# Script PowerShell pour Windows
# ==============================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "🚀 LANCEMENT IAFactory RAG-DZ - Mode LOCAL" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier Docker
Write-Host "[1/5] Vérification Docker..." -ForegroundColor Blue
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker installé: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker non trouvé. Installez Docker Desktop pour Windows" -ForegroundColor Red
    Write-Host "   https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Vérifier Docker Compose
Write-Host ""
Write-Host "[2/5] Vérification Docker Compose..." -ForegroundColor Blue
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose installé: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose non trouvé" -ForegroundColor Red
    exit 1
}

# Créer .env.local si pas existant
Write-Host ""
Write-Host "[3/5] Configuration environnement..." -ForegroundColor Blue
if (-Not (Test-Path ".env.local")) {
    Write-Host "📝 Création .env.local..." -ForegroundColor Yellow

    # Générer des secrets aléatoires
    $postgresPassword = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
    $secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
    $jwtSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})

    @"
# IAFactory RAG-DZ - Local Development
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Region
SOVEREIGNTY_REGION=DZ
SOVEREIGNTY_LABEL=Algérie
TZ=Africa/Algiers

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$postgresPassword
POSTGRES_DB=iafactory_dz
DATABASE_URL=postgresql://postgres:$postgresPassword@iafactory-postgres:5432/iafactory_dz

# Redis
REDIS_URL=redis://iafactory-redis:6379/0
REDIS_PASSWORD=

# Qdrant
QDRANT_URL=http://iafactory-qdrant:6333
QDRANT_API_KEY=

# API Keys (CONFIGURER VOS CLÉS ICI)
# Groq (Recommandé - gratuit)
GROQ_API_KEY=

# OpenAI
OPENAI_API_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# Google
GOOGLE_API_KEY=

# DeepSeek
DEEPSEEK_API_KEY=

# Security
SECRET_KEY=$secretKey
JWT_SECRET=$jwtSecret

# Server
PORT=8180
HOST=0.0.0.0
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8180
"@ | Out-File -FilePath ".env.local" -Encoding UTF8

    Write-Host "✅ .env.local créé" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Configurez vos clés API dans .env.local" -ForegroundColor Yellow
    Write-Host "   Au minimum, ajoutez une clé Groq (gratuite): https://console.groq.com" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env.local existe déjà" -ForegroundColor Green
}

# Arrêter les conteneurs existants
Write-Host ""
Write-Host "[4/5] Nettoyage des conteneurs existants..." -ForegroundColor Blue
docker-compose down 2>$null
Write-Host "✅ Conteneurs arrêtés" -ForegroundColor Green

# Démarrer les services
Write-Host ""
Write-Host "[5/5] Démarrage des services Docker..." -ForegroundColor Blue
Write-Host "⏳ Cela peut prendre 2-3 minutes au premier lancement..." -ForegroundColor Yellow
Write-Host ""

docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Services démarrés avec succès!" -ForegroundColor Green
    Write-Host ""

    # Attendre que les services soient prêts
    Write-Host "⏳ Attente du démarrage complet (30 secondes)..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30

    # Afficher le statut
    Write-Host ""
    Write-Host "📊 Statut des services:" -ForegroundColor Cyan
    docker-compose ps

    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "✅ IAFactory RAG-DZ est maintenant EN LIGNE!" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 URLS disponibles:" -ForegroundColor Cyan
    Write-Host "   • Health Check: http://localhost:8180/health" -ForegroundColor White
    Write-Host "   • API Docs:     http://localhost:8180/docs" -ForegroundColor White
    Write-Host "   • API Backend:  http://localhost:8180/api/" -ForegroundColor White
    Write-Host ""
    Write-Host "📦 Base de données:" -ForegroundColor Cyan
    Write-Host "   • PostgreSQL:   localhost:6330" -ForegroundColor White
    Write-Host "   • Redis:        localhost:6331" -ForegroundColor White
    Write-Host "   • Qdrant:       localhost:6332" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Commandes utiles:" -ForegroundColor Cyan
    Write-Host "   • Logs:         docker-compose logs -f" -ForegroundColor White
    Write-Host "   • Arrêter:      docker-compose down" -ForegroundColor White
    Write-Host "   • Redémarrer:   docker-compose restart" -ForegroundColor White
    Write-Host ""

    # Test du health check
    Write-Host "🧪 Test du health check..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8180/health" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Health check OK!" -ForegroundColor Green
            Write-Host "   Réponse: $($response.Content)" -ForegroundColor White
        }
    } catch {
        Write-Host "⚠️  Le backend démarre encore... Réessayez dans 1-2 minutes" -ForegroundColor Yellow
        Write-Host "   Commande: curl http://localhost:8180/health" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 PROCHAINES ÉTAPES:" -ForegroundColor Yellow
    Write-Host "   1. Configurez vos clés API dans .env.local" -ForegroundColor White
    Write-Host "   2. Redémarrez: docker-compose restart" -ForegroundColor White
    Write-Host "   3. Testez l'API: http://localhost:8180/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Pour déployer en production sur VPS:" -ForegroundColor Yellow
    Write-Host "   Voir: DEPLOIEMENT_VPS_RAPIDE.md" -ForegroundColor White
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan

} else {
    Write-Host ""
    Write-Host "❌ Erreur lors du démarrage des services" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 Vérifiez les logs:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs" -ForegroundColor White
    Write-Host ""
    exit 1
}
