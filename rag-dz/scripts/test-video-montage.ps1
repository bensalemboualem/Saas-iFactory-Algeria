#!/usr/bin/env pwsh
# Test complet du système de montage vidéo IAFactory
# Usage: .\test-video-montage.ps1 [-VideoPath "chemin/video.mp4"]

param(
    [string]$VideoPath = "",
    [string]$BaseUrl = "https://www.iafactoryalgeria.com/video-operator"
)

Write-Host "`n🎬 TEST MONTAGE VIDEO IAFACTORY" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# 1. Test Health
Write-Host "1️⃣ Test Health API..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/health" -TimeoutSec 10
    Write-Host "   ✅ Service: $($health.service) v$($health.version)" -ForegroundColor Green
    Write-Host "   ✅ Status: $($health.status)" -ForegroundColor Green
    Write-Host "   ✅ Jobs actifs: $($health.jobs_active)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. Test Root endpoint
Write-Host "`n2️⃣ Test Root API..." -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "$BaseUrl/" -TimeoutSec 10
    Write-Host "   ✅ Service online: $($root.status)" -ForegroundColor Green
    Write-Host "   ✅ Langues: $($root.languages -join ', ')" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Root non accessible: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 3. Test création job (si vidéo fournie)
if ($VideoPath -and (Test-Path $VideoPath)) {
    Write-Host "`n3️⃣ Test Upload Vidéo..." -ForegroundColor Yellow
    Write-Host "   📁 Fichier: $VideoPath" -ForegroundColor Gray
    
    try {
        $boundary = [System.Guid]::NewGuid().ToString()
        $fileName = Split-Path $VideoPath -Leaf
        $fileBytes = [System.IO.File]::ReadAllBytes($VideoPath)
        $fileEnc = [System.Text.Encoding]::GetEncoding('iso-8859-1').GetString($fileBytes)
        
        $bodyLines = @(
            "--$boundary",
            "Content-Disposition: form-data; name=`"video`"; filename=`"$fileName`"",
            "Content-Type: video/mp4",
            "",
            $fileEnc,
            "--$boundary",
            "Content-Disposition: form-data; name=`"target_duration`"",
            "",
            "15",
            "--$boundary",
            "Content-Disposition: form-data; name=`"platforms`"",
            "",
            "instagram_reels,tiktok",
            "--$boundary",
            "Content-Disposition: form-data; name=`"style`"",
            "",
            "algerian_minimal",
            "--$boundary",
            "Content-Disposition: form-data; name=`"language`"",
            "",
            "fr",
            "--$boundary--"
        )
        $body = $bodyLines -join "`r`n"
        
        $response = Invoke-RestMethod -Uri "$BaseUrl/api/v1/edit" -Method POST -ContentType "multipart/form-data; boundary=$boundary" -Body $body -TimeoutSec 60
        
        Write-Host "   ✅ Job créé: $($response.job_id)" -ForegroundColor Green
        Write-Host "   ✅ Status: $($response.status)" -ForegroundColor Green
        
        # 4. Poll status
        Write-Host "`n4️⃣ Suivi du job..." -ForegroundColor Yellow
        $jobId = $response.job_id
        $maxAttempts = 30
        $attempt = 0
        
        do {
            Start-Sleep -Seconds 2
            $status = Invoke-RestMethod -Uri "$BaseUrl/api/v1/status/$jobId" -TimeoutSec 10
            $attempt++
            Write-Host "   ⏳ [$attempt/$maxAttempts] Progress: $($status.progress)% - $($status.message)" -ForegroundColor Gray
        } while ($status.status -eq "processing" -and $attempt -lt $maxAttempts)
        
        if ($status.status -eq "completed") {
            Write-Host "`n   ✅ MONTAGE TERMINÉ!" -ForegroundColor Green
            Write-Host "   📥 Outputs disponibles:" -ForegroundColor Cyan
            foreach ($key in $status.outputs.PSObject.Properties.Name) {
                Write-Host "      - $key : $BaseUrl$($status.outputs.$key)" -ForegroundColor White
            }
        } elseif ($status.status -eq "failed") {
            Write-Host "   ❌ Échec: $($status.message)" -ForegroundColor Red
        } else {
            Write-Host "   ⚠️ Timeout - job encore en cours" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "   ❌ Erreur upload: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "`n3️⃣ Test Upload Vidéo..." -ForegroundColor Yellow
    Write-Host "   ⏭️ Skipped - Pas de vidéo fournie" -ForegroundColor Gray
    Write-Host "   💡 Usage: .\test-video-montage.ps1 -VideoPath 'C:\path\to\video.mp4'" -ForegroundColor Gray
}

# Résumé
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "📋 RÉSUMÉ" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "API Health:    $BaseUrl/health" -ForegroundColor White
Write-Host "API Docs:      $BaseUrl/docs" -ForegroundColor White
Write-Host "Interface:     https://www.iafactoryalgeria.com/apps/dzirvideo-ai/" -ForegroundColor White
Write-Host "Page Test:     https://www.iafactoryalgeria.com/apps/dzirvideo-ai/testing.html" -ForegroundColor White
Write-Host "`n"
