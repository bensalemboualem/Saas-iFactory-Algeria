$projectPath = "D:\IAFactory\onestschooled"
$replacements = @{
    ':8000' = ':8260'
    '8000/' = '8260/'
    'localhost:8000' = 'localhost:8260'
    ':3000' = ':3130'
    '3000/' = '3130/'
    'localhost:3000' = 'localhost:3130'
    ':3306' = ':3307'
    '3306/' = '3307/'
    ':6379' = ':6386'
    '6379/' = '6386/'
}
$files = Get-ChildItem -Path $projectPath -Recurse -Include "docker-compose*.yml","*.env*",".env" -File -ErrorAction SilentlyContinue
Write-Host "Renumeration: onestschooled" -ForegroundColor Cyan
$total = 0
foreach ($file in $files) {
    try {
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
    } catch { }
}
Write-Host "Total: $total" -ForegroundColor Yellow
