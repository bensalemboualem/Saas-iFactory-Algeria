param (
    [string]$BaseUrl = 'https://www.iafactoryalgeria.com:8085',
    [string]$JobId
)

function Format-Title($text) {
    Write-Host "`n=== $text ===" -ForegroundColor Cyan
}

function Invoke-Endpoint([string]$Path) {
    $uri = "${BaseUrl.TrimEnd('/')}/${Path.TrimStart('/')}"
    try {
        $response = Invoke-RestMethod -Uri $uri -Method Get -UseBasicParsing -TimeoutSec 30
        return @{ status = 'Success'; data = $response }
    } catch {
        return @{ status = 'Error'; message = $_.Exception.Message }
    }
}

Write-Host "🚀 Automation rapide – video-operator QA" -ForegroundColor Green

Format-Title 'Health Check'
$health = Invoke-Endpoint -Path '/health'
if ($health.status -eq 'Success') {
    Write-Host "Status: OK" -ForegroundColor Green
    Write-Host ($health.data | ConvertTo-Json -Depth 3)
} else {
    Write-Host "Échec health: $($health.message)" -ForegroundColor Red
}

if ($JobId) {
    Format-Title "Statut du job $JobId"
    $status = Invoke-Endpoint -Path "/api/v1/status/$JobId"
    if ($status.status -eq 'Success') {
        Write-Host "Statut reçu" -ForegroundColor Green
        Write-Host ($status.data | ConvertTo-Json -Depth 4)
    } else {
        Write-Host "Erreur status: $($status.message)" -ForegroundColor Yellow
    }
} else {
    Format-Title 'Statut (Job ID manquant)'
    Write-Host 'Passez -JobId <id> pour récupérer l’avancement d’un montage.' -ForegroundColor Gray
}

Format-Title 'Rappels'
Write-Host "/api/v1/edit" -ForegroundColor Magenta
Write-Host "/api/v1/status/{jobId}" -ForegroundColor Magenta
Write-Host "/api/v1/download/{jobId}/{platform}" -ForegroundColor Magenta
Write-Host "Base URL: $BaseUrl" -ForegroundColor Yellow
