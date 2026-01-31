# Script de configuration de la base de données Gateway
# ========================================================

Write-Host "🗄️  Configuration de la base de données Gateway..." -ForegroundColor Cyan

# 1. Générer le client Prisma
Write-Host "`n📦 Génération du client Prisma..." -ForegroundColor Yellow
pnpm db:generate

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la génération Prisma" -ForegroundColor Red
    exit 1
}

# 2. Appliquer les migrations (créer les tables)
Write-Host "`n🔄 Application des migrations..." -ForegroundColor Yellow
pnpm db:push

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors des migrations" -ForegroundColor Red
    exit 1
}

# 3. Seed (données initiales)
Write-Host "`n🌱 Insertion des données initiales..." -ForegroundColor Yellow
pnpm db:seed

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Warning: Seed échoué (peut-être déjà fait)" -ForegroundColor Yellow
}

Write-Host "`n✅ Base de données configurée avec succès!" -ForegroundColor Green
Write-Host "Vous pouvez maintenant démarrer le Gateway avec: pnpm dev" -ForegroundColor Cyan
