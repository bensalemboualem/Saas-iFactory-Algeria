# Script de remplacement des imports billing par GatewayClient
$files = @(
    "D:\IAFactory\rag-dz\apps\video-studio\backend\api\routes\tokens.py",
    "D:\IAFactory\rag-dz\apps\video-studio\backend\app\api\routes\credits.py",
    "D:\IAFactory\rag-dz\billing-credits\backend\main.py",
    "D:\IAFactory\rag-dz\services\api\app\multi_llm\multi_llm_service.py",
    "D:\IAFactory\rag-dz\services\api\app\routers\billing_v2.py",
    "D:\IAFactory\rag-dz\services\api\app\routers\payment.py"
)

$replacements = @{
    'from.*\.services\.billing_service import.*' = 'from app.clients.gateway_client import gateway'
    'from.*\.services\.credits_service import.*' = 'from app.clients.gateway_client import gateway'
    'from.*\.services\.payment_service import.*' = 'from app.clients.gateway_client import gateway'
    'from.*\.core\.credit_service import.*' = 'from app.clients.gateway_client import gateway'
}

$total = 0
foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $modified = $false
        
        foreach ($pattern in $replacements.Keys) {
            if ($content -match $pattern) {
                $content = $content -replace $pattern, $replacements[$pattern]
                $modified = $true
            }
        }
        
        if ($modified) {
            Set-Content -Path $file -Value $content -NoNewline
            Write-Host "Modifie: $($file.Split('\')[-1])" -ForegroundColor Green
            $total++
        }
    }
}

Write-Host "`nTotal: $total fichiers modifies" -ForegroundColor Yellow
