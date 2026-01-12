param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,

    [string]$BaseUrl = "https://www.iafactoryalgeria.com:8085",
    [int]$TargetDuration = 15,
    [string]$Platforms = "instagram_reels",
    [string]$Style = "algerian_minimal",
    [bool]$AddCaptions = $true,
    [string]$Language = "fr",
    [string]$OutputDirectory = "./video-operator-outputs",
    [int]$PollIntervalSeconds = 3,
    [int]$MaxPollAttempts = 40
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $VideoPath)) {
    throw "Fichier introuvable : $VideoPath"
}

$PlatformsList = ($Platforms -split ',') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
if ($PlatformsList.Count -eq 0) {
    throw "Au moins une plateforme doit être fournie via -Platforms"
}

Write-Host "[1/4] Vérification du service vidéo" -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Method Get -Uri "${BaseUrl.TrimEnd('/')}/health" -UseBasicParsing -TimeoutSec 15
    Write-Host "  ✅ Service : $($health.service) (jobs actifs : $($health.jobs_active))" -ForegroundColor Green
} catch {
    throw "Le service vidéo n'est pas joignable : $($_.Exception.Message)"
}

Write-Host "[2/4] Envoi du fichier" -ForegroundColor Cyan
$client = [System.Net.Http.HttpClient]::new()
$multipart = [System.Net.Http.MultipartFormDataContent]::new()
$fileStream = [System.IO.File]::OpenRead($VideoPath)
try {
    $mimeType = switch ([System.IO.Path]::GetExtension($VideoPath).ToLower()) {
        '.mp4' { 'video/mp4' }
        '.mov' { 'video/quicktime' }
        '.avi' { 'video/x-msvideo' }
        '.webm' { 'video/webm' }
        default { 'application/octet-stream' }
    }

    $videoContent = [System.Net.Http.StreamContent]::new($fileStream)
    $videoContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse($mimeType)
    $multipart.Add($videoContent, "video", [System.IO.Path]::GetFileName($VideoPath))
    $multipart.Add([System.Net.Http.StringContent]::new($TargetDuration.ToString()), "target_duration")
    $multipart.Add([System.Net.Http.StringContent]::new($Platforms), "platforms")
    $multipart.Add([System.Net.Http.StringContent]::new($Style), "style")
    $multipart.Add([System.Net.Http.StringContent]::new($AddCaptions.ToString().ToLower()), "add_captions")
    $multipart.Add([System.Net.Http.StringContent]::new($Language), "language")

    $response = $client.PostAsync("${BaseUrl.TrimEnd('/')}/api/v1/edit", $multipart).Result
    if (-not $response.IsSuccessStatusCode) {
        throw "Echec POST edit : $($response.StatusCode) - $($response.Content.ReadAsStringAsync().Result)"
    }

    $payload = $response.Content.ReadAsStringAsync().Result | ConvertFrom-Json
    $jobId = $payload.job_id
    Write-Host "  🚀 Job créé : $jobId" -ForegroundColor Green
} finally {
    $fileStream.Dispose()
}

if (-not $jobId) {
    throw "Impossible de récupérer l'identifiant du job"
}

Write-Host "[3/4] Polling du statut" -ForegroundColor Cyan
$attempt = 0
$status = $null
while ($attempt -lt $MaxPollAttempts) {
    $attempt++
    $status = Invoke-RestMethod -Method Get -Uri "${BaseUrl.TrimEnd('/')}/api/v1/status/$jobId" -UseBasicParsing
    Write-Host "  tentative $attempt / $MaxPollAttempts : $($status.status) ($($status.progress)%)"
    if ($status.status -eq 'completed') {
        Write-Host '  ✅ Job terminé' -ForegroundColor Green
        break
    } elseif ($status.status -eq 'failed') {
        throw "Le job a échoué : $($status.message)"
    }
    Start-Sleep -Seconds $PollIntervalSeconds
}
if ($status.status -ne 'completed') {
    throw "Timeout : le job n'a pas atteint l'état completed après $MaxPollAttempts essais"
}

if (-not $status.outputs) {
    throw "Aucun output disponible pour le job $jobId"
}

$platformToDownload = $PlatformsList | Where-Object { $status.outputs.ContainsKey($_) } | Select-Object -First 1
if (-not $platformToDownload) {
    $platformToDownload = $status.outputs.Keys | Select-Object -First 1
}

if (-not $platformToDownload) {
    throw "Aucune plateforme disponible pour le téléchargement"
}

$newDir = Resolve-Path -Path $OutputDirectory -ErrorAction SilentlyContinue
if (-not $newDir) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
    $newDir = Resolve-Path -Path $OutputDirectory
}

$outFile = Join-Path $newDir ([System.IO.Path]::GetFileName($status.outputs.$platformToDownload))
Write-Host "[4/4] Téléchargement ($platformToDownload) -> $outFile" -ForegroundColor Cyan
Invoke-WebRequest -Uri "${BaseUrl.TrimEnd('/')}/api/v1/download/$jobId/$platformToDownload" -OutFile $outFile -UseBasicParsing

Write-Host "✅ Vidéo prête : $outFile" -ForegroundColor Magenta
