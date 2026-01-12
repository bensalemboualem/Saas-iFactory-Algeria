param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSCommandPath
$videoDir = Join-Path $repoRoot 'agents\video-operator'

Write-Host "[1/4] Vérification du réseau Docker" -ForegroundColor Cyan
$networkName = 'iafactory-network'
$networkId = docker network ls --filter name="${networkName}" --format '{{.ID}}'
if (-not $networkId) {
    Write-Host "Création du réseau ${networkName}" -ForegroundColor Yellow
    docker network create $networkName | Out-Null
} else {
    Write-Host "Réseau ${networkName} déjà présent" -ForegroundColor Green
}

Write-Host "[2/4] Démarrage du service video-operator" -ForegroundColor Cyan
Push-Location $videoDir
try {
    docker compose pull | Out-Null
} catch {
    Write-Host "Impossible de pull les images (controle offline)." -ForegroundColor Yellow
}
docker compose up -d
Pop-Location

Write-Host "[3/4] Vérification du conteneur" -ForegroundColor Cyan
$containerId = docker ps --filter name=iafactory-video-operator --format '{{.ID}}'
if (-not $containerId) {
    throw "Le conteneur iafactory-video-operator ne tourne pas après le up"
}
Write-Host "Conteneur en run : $containerId" -ForegroundColor Green

Write-Host "[4/4] Ping du service" -ForegroundColor Cyan
$timeout = 10
while ($timeout -gt 0) {
    try {
        $response = curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8085/
        if ($response -match '^(200|405)$') {
            Write-Host "Service HTTP répond ($response)" -ForegroundColor Green
            break
        }
    } catch {
        Start-Sleep -Seconds 2
        $timeout--
        continue
    }
    Start-Sleep -Seconds 2
    $timeout--
}
if ($timeout -le 0) {
    Write-Warning "Le service ne répond pas encore, vérifie les logs avec : docker logs iafactory-video-operator"
}

Write-Host "✅ Video ecosystem prêt" -ForegroundColor Magenta
