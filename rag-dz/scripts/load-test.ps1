#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param(
    [string]$Scenario = "orchestrator-smoke"
)

$scriptPath = Join-Path "tests/load/k6" "$Scenario.js"
if (-not (Test-Path $scriptPath)) {
    Write-Error "Scénario introuvable: $scriptPath"
}

$k6Image = $env:K6_IMAGE
if (-not $k6Image) { $k6Image = "grafana/k6:latest" }

$baseUrl = $env:K6_BASE_URL
if (-not $baseUrl) { $baseUrl = "http://host.docker.internal:8180" }

$apiKey = $env:K6_API_KEY
if (-not $apiKey) { $apiKey = "change-me-in-production" }

$vus = $env:K6_VUS
if (-not $vus) { $vus = "10" }

$duration = $env:K6_DURATION
if (-not $duration) { $duration = "1m" }

Write-Host "🚀 Lancement k6 ($Scenario) contre $baseUrl..." -ForegroundColor Cyan

docker run --rm -i `
  -e K6_BASE_URL="$baseUrl" `
  -e K6_API_KEY="$apiKey" `
  -e K6_VUS="$vus" `
  -e K6_DURATION="$duration" `
  -v "${PWD}/tests/load/k6:/scripts" `
  $k6Image run "/scripts/$Scenario.js"

