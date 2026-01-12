$chatbot = Get-Content "D:\IAFactory\rag-dz\apps\shared\chatbot-help.html" -Raw

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
        $content = Get-Content $file -Raw
        if ($content -notmatch 'help-bubble') {
            $newContent = $content.Replace('</body>', "$chatbot`n</body>")
            Set-Content $file $newContent
            Write-Host "Added chatbot to: $app"
        } else {
            Write-Host "Already has chatbot: $app"
        }
    } else {
        Write-Host "File not found: $app"
    }
}

Write-Host "Done!"
