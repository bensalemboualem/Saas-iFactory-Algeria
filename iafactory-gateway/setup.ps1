# IAFactory Gateway - Setup Automatique
Write-Host "🚀 Installation IAFactory Gateway..." -ForegroundColor Cyan

# 1. Vérifier Docker
Write-Host "`n1️⃣ Vérification Docker..." -ForegroundColor Yellow
$dockerRunning = $false
try {
    docker ps 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
        Write-Host "✅ Docker est actif" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Docker n'est pas disponible" -ForegroundColor Yellow
}

# 2. Générer Prisma Client
Write-Host "`n2️⃣ Génération Prisma Client..." -ForegroundColor Yellow
npm run db:generate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Prisma client généré" -ForegroundColor Green
} else {
    Write-Host "❌ Erreur génération Prisma" -ForegroundColor Red
    exit 1
}

# 3. Démarrer services
if ($dockerRunning) {
    Write-Host "`n3️⃣ Démarrage containers Docker..." -ForegroundColor Yellow
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Containers démarrés" -ForegroundColor Green
        
        # Attendre que Postgres soit prêt
        Write-Host "`n⏳ Attente Postgres..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        # Lancer migrations
        Write-Host "`n4️⃣ Migrations base de données..." -ForegroundColor Yellow
        npm run db:push
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Base de données créée" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Erreur migrations (normal si DB existe déjà)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Erreur démarrage Docker" -ForegroundColor Red
    }
} else {
    Write-Host "`n⚠️ Docker non disponible - Mode sans DB" -ForegroundColor Yellow
    Write-Host "Pour activer l'auth et les crédits, installe Docker Desktop" -ForegroundColor Gray
}

# 5. Afficher statut
Write-Host "`n✅ Setup terminé!" -ForegroundColor Green
Write-Host "`n📍 Gateway disponible sur:" -ForegroundColor Cyan
Write-Host "   http://localhost:3001" -ForegroundColor White
Write-Host "   http://localhost:3001/health (health check)" -ForegroundColor Gray
Write-Host "   http://localhost:3001/v1/models (API)" -ForegroundColor Gray

Write-Host "`n🔧 Commandes utiles:" -ForegroundColor Cyan
Write-Host "   npm run dev          - Démarrer en dev" -ForegroundColor Gray
Write-Host "   docker-compose logs  - Voir logs" -ForegroundColor Gray
Write-Host "   docker-compose down  - Arrêter services" -ForegroundColor Gray
