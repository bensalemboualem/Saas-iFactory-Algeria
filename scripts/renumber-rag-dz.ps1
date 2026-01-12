$projectPath = "D:\IAFactory\rag-dz"
$replacements = @{
    ':5432' = ':5433'
    '5432/' = '5433/'
    ':6379' = ':6380'
    '6379/' = '6380/'
    ':6333' = ':6334'
    '6333/' = '6334/'
    ':11434' = ':11435'
    '11434/' = '11435/'
    ':7700' = ':7701'
    '7700/' = '7701/'
}
$files = Get-ChildItem -Path $projectPath -Recurse -Include "docker-compose*.yml","*.env*" -File -ErrorAction SilentlyContinue
Write-Host "Renumeration: rag-dz (DB/Redis/Qdrant)" -ForegroundColor Cyan
$total = 0
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $modified = $false
    foreach ($old in $replacements.Keys) {
        if ($content -match [regex]::Escape($old)) {
            $content = $content -replace [regex]::Escape($old), $replacements[$old]
            $modified = $true
        }
    }
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  $($file.Name)" -ForegroundColor Green
        $total++
    }
}
Write-Host "Total: $total" -ForegroundColor Yellow
