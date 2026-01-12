$apps = @(
    'ai-searcher', 'billing-panel', 'bmad', 'business-dz', 'council', 
    'crm-ia', 'data-dz', 'dev-portal', 'dzirvideo-ai', 'fiscal-assistant', 
    'islam-dz', 'ithy', 'legal-assistant', 'med-dz', 'pme-copilot', 
    'pmedz-sales', 'prof-dz', 'prompt-creator', 'seo-dz', 'startup-dz', 
    'voice-assistant'
)

foreach ($app in $apps) {
    $file = "D:\IAFactory\rag-dz\apps\$app\index.html"
    if (Test-Path $file) {
        Write-Host "Deploying: $app"
        scp $file "root@46.224.3.125:/opt/iafactory-rag-dz/apps/$app/index.html"
    }
}

Write-Host "Done!"
