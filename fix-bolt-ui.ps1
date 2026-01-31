# Script de réparation Bolt-UI
# =============================

Write-Host "🔧 Réparation de Bolt-UI..." -ForegroundColor Cyan

$root = "C:\Users\bbens\iafactorychatgpt_v2"
Set-Location $root

# 1. Nettoyer seulement le cache problématique
Write-Host "`n📦 Nettoyage du cache @rollup..." -ForegroundColor Yellow
if (Test-Path "node_modules\.pnpm\@rollup+rollup-win32-x64-msvc*") {
    Remove-Item "node_modules\.pnpm\@rollup+rollup-win32-x64-msvc*" -Recurse -Force
    Write-Host "✅ Cache rollup nettoyé" -ForegroundColor Green
}

# 2. Installer le module manquant
Write-Host "`n📥 Installation de @rollup/rollup-win32-x64-msvc..." -ForegroundColor Yellow
pnpm add -D @rollup/rollup-win32-x64-msvc@4.56.0 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Module installé" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installation partielle, essayez pnpm install à la racine" -ForegroundColor Yellow
}

# 3. Lancer Bolt-UI
Write-Host "`n🚀 Démarrage de Bolt-UI..." -ForegroundColor Cyan
Set-Location "$root\apps\bolt-ui"
pnpm dev
