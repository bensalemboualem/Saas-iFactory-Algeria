# ==============================================
# 🧪 IAFactory DZ/CH - Test Rapide Local (PowerShell)
# ==============================================
# Usage: .\test_local.ps1
# ==============================================

$HOST = "localhost"
$PORT = 8180
$BASE_URL = "http://${HOST}:${PORT}"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🧪 IAFactory DZ/CH - Test Rapide Local                    ║" -ForegroundColor Cyan
Write-Host "║     Target: $BASE_URL                                  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$passed = 0
$failed = 0

function Test-Endpoint {
    param (
        [string]$Name,
        [string]$Endpoint,
        [string]$Method = "GET",
        [string]$Body = $null
    )
    
    try {
        if ($Method -eq "POST" -and $Body) {
            $response = Invoke-RestMethod -Uri "${BASE_URL}${Endpoint}" -Method POST -ContentType "application/json" -Body $Body -TimeoutSec 10
        } else {
            $response = Invoke-RestMethod -Uri "${BASE_URL}${Endpoint}" -Method GET -TimeoutSec 10
        }
        Write-Host "  ✓ $Name" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  ✗ $Name ($Endpoint)" -ForegroundColor Red
        return $false
    }
}

# ==============================================
# CORE SERVICES
# ==============================================
Write-Host "═══ CORE SERVICES ═══" -ForegroundColor Blue
if (Test-Endpoint "API Health" "/health") { $passed++ } else { $failed++ }
if (Test-Endpoint "API Root" "/") { $passed++ } else { $failed++ }

# ==============================================
# BILLING & CRM
# ==============================================
Write-Host ""
Write-Host "═══ BILLING & CRM ═══" -ForegroundColor Blue
if (Test-Endpoint "Billing V2" "/api/billing/v2/health") { $passed++ } else { $failed++ }
if (Test-Endpoint "CRM PRO" "/api/crm-pro/health") { $passed++ } else { $failed++ }
if (Test-Endpoint "PME V2" "/api/pme/v2/health") { $passed++ } else { $failed++ }

# ==============================================
# BIG RAG MULTI-PAYS
# ==============================================
Write-Host ""
Write-Host "═══ BIG RAG MULTI-PAYS 🌍 ═══" -ForegroundColor Blue
if (Test-Endpoint "BIG RAG Status" "/api/rag/multi/status") { $passed++ } else { $failed++ }
if (Test-Endpoint "BIG RAG Collections" "/api/rag/multi/collections") { $passed++ } else { $failed++ }
if (Test-Endpoint "Ingest Status" "/api/rag/multi/ingest/status") { $passed++ } else { $failed++ }

# Test search
Write-Host "  Testing BIG RAG Search..." -ForegroundColor Yellow
$searchBody = '{"query":"fiscalite algerie", "collection":"rag_dz", "top_k":3}'
if (Test-Endpoint "BIG RAG Search DZ" "/api/rag/multi/seed/search" "POST" $searchBody) { $passed++ } else { $failed++ }

# ==============================================
# VOICE AI
# ==============================================
Write-Host ""
Write-Host "═══ VOICE AI 🎙️ ═══" -ForegroundColor Blue
if (Test-Endpoint "STT Status" "/api/voice/stt/status") { $passed++ } else { $failed++ }
if (Test-Endpoint "TTS Status" "/api/voice/tts/status") { $passed++ } else { $failed++ }
if (Test-Endpoint "Voice Agent" "/api/voice/agent/status") { $passed++ } else { $failed++ }

# ==============================================
# NLP & OCR
# ==============================================
Write-Host ""
Write-Host "═══ NLP & OCR 📄 ═══" -ForegroundColor Blue
if (Test-Endpoint "Darija NLP" "/api/darija/status") { $passed++ } else { $failed++ }
if (Test-Endpoint "OCR Status" "/api/ocr/status") { $passed++ } else { $failed++ }

# Test Darija detection
Write-Host "  Testing Darija Detection..." -ForegroundColor Yellow
$darijaBody = '{"text":"wach kayen chi haja jdida fel khedma?"}'
if (Test-Endpoint "Darija Detection" "/api/darija/detect" "POST" $darijaBody) { $passed++ } else { $failed++ }

# ==============================================
# SUMMARY
# ==============================================
$total = $passed + $failed
$percent = [math]::Round(($passed / $total) * 100)

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📊 RÉSUMÉ" -ForegroundColor Blue
Write-Host "   Total tests:  $total"
Write-Host "   Passés:       $passed" -ForegroundColor Green
Write-Host "   Échoués:      $failed" -ForegroundColor Red
Write-Host ""

if ($failed -eq 0) {
    Write-Host "✅ TOUS LES SERVICES SONT OPÉRATIONNELS ($percent%)" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Prêt pour le déploiement VPS!" -ForegroundColor Cyan
    Write-Host "   1. git push origin main"
    Write-Host "   2. ssh root@46.224.3.125"
    Write-Host "   3. ./deploy.sh"
} elseif ($percent -ge 80) {
    Write-Host "⚠️ SYSTÈME PARTIELLEMENT OPÉRATIONNEL ($percent%)" -ForegroundColor Yellow
} else {
    Write-Host "❌ SYSTÈME EN ERREUR ($percent%)" -ForegroundColor Red
    Write-Host "   Vérifiez: docker compose logs -f iafactory-backend"
}

Write-Host ""
