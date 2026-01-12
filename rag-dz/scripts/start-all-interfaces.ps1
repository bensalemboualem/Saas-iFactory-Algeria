<#
.SYNOPSIS
    Start all docker services, ensure env files exist, wait for backend health, and open frontends in browser.

.DESCRIPTION
    This script attempts to bring up all services with docker compose, ensures the backend gets environment variables
    (by copying .env to .env.local if needed), and opens the main UI URLs when the backend reports healthy.

    The script is cautious: it creates backups before writing files; it prints helpful logs and stops on error.

.NOTES
    - Requires Docker and Docker Compose installed
    - Run in project root (where docker-compose.yml is located)
    - Uses pwsh (PowerShell Core) semantics
#>

param(
    [int]$TimeoutSeconds = 240,
    [int]$PollIntervalSeconds = 4,
    [switch]$OpenBrowser = $true
)

function Write-Header($msg){
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host $msg -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan
}

Write-Header "IAFactory - Start all interfaces"

<#
    Determine repository root by searching upwards for docker-compose.yml.
    Start from the script directory and climb the tree until we find a docker-compose.yml file or reach filesystem root.
#>
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = $scriptDir
while ((-not (Test-Path -Path (Join-Path $repoRoot 'docker-compose.yml'))) -and $repoRoot -ne (Get-Item $repoRoot).Parent.FullName){
    $repoRoot = (Get-Item $repoRoot).Parent.FullName
}

if (-not (Test-Path -Path (Join-Path $repoRoot 'docker-compose.yml'))){
    Write-Error "docker-compose.yml not found in repository. Ensure you're running this under the project repository."
    exit 1
}

Push-Location -Path $repoRoot

# Back up existing .env.local, then copy .env -> .env.local if missing
$envLocalPath = Join-Path -Path (Get-Location) -ChildPath '.env.local'
$envPath = Join-Path -Path (Get-Location) -ChildPath '.env'

if (Test-Path -Path $envLocalPath){
    $timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
    $bakName = ".env.local.bak.$timestamp"
    Write-Host "Backing up existing .env.local -> $bakName"
    Copy-Item -Path $envLocalPath -Destination $bakName -Force
}

if (-not (Test-Path -Path $envLocalPath)){
    if (-not (Test-Path -Path $envPath)){
        Write-Warning ".env not found at project root. Create .env or adjust compose env_file settings before continuing."
    } else {
        Write-Host "Creating .env.local from existing .env"
        Copy-Item -Path $envPath -Destination $envLocalPath -Force
    }
}

# Bring up docker stack
Write-Host "Building docker images (pull latest), then starting services (detached)..."
try{
    docker compose build --pull | Out-Host
} catch {
    Write-Warning "Warning: 'docker compose build --pull' failed or not supported; attempting 'docker compose up -d --build' instead.";
}

try{
    docker compose up -d --build | Out-Host
} catch {
    Write-Warning "Warning: 'docker compose up' failed; retrying with 'docker-compose up -d' for compatibility.";
    docker-compose up -d --build | Out-Host
}

Write-Host "Waiting for backend health (http://localhost:8180/health) to be healthy..."

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $deadline){
    try{
        $res = Invoke-RestMethod -Uri http://localhost:8180/health -TimeoutSec 5
        if ($res -and $res.status -eq 'healthy'){
            Write-Host "Backend is healthy: $($res | ConvertTo-Json -Depth 2)" -ForegroundColor Green
            break
        } else {
            Write-Host "Backend responded, but not healthy yet: $($res | ConvertTo-Json -Depth 2)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host -NoNewline "."
    }
    Start-Sleep -Seconds $PollIntervalSeconds
}

if ((Get-Date) -ge $deadline){
    Write-Warning "Timeout waiting for backend. Gathering logs..."
    docker compose ps
    docker compose logs iafactory-backend --tail 200
    Pop-Location
    exit 1
}

# Open frontend URLs (common ports mapping in docker-compose.yml)
if ($OpenBrowser){
    $urls = @(
        'http://localhost:8182', # Hub (archon)
        'http://localhost:8183', # Docs (rag-ui)
        'http://localhost:8184'  # Studio
    )
    foreach ($u in $urls){
        Write-Host "Opening $u"
        Start-Process $u
    }
}

Write-Host "All done. Monitor 'docker compose ps' and 'docker compose logs' for details." -ForegroundColor Green

Pop-Location

Exit 0
