param(
    [array]$LandingPages = @()
)

if (-not $LandingPages -or $LandingPages.Count -eq 0) {
    $LandingPages = @(
        @{ File = 'landing-genspark.html'; Port = 8195; Label = 'Landing Genspark' },
        @{ File = 'landing-genspark-exact.html'; Port = 8196; Label = 'Landing Genspark Exact' },
        @{ File = 'landing-genspark-animated.html'; Port = 8197; Label = 'Landing Genspark Animée' },
        @{ File = 'landing-complete-responsive.html'; Port = 8199; Label = 'Landing Responsive' }
    )
}

$LandingPages | ForEach-Object {
    $fileMeta = $_
    try {
        $resolved = Resolve-Path -LiteralPath $fileMeta.File -ErrorAction Stop
    }
    catch {
        Write-Warning "Ne trouve pas $($fileMeta.File). Ignorée."
        return
    }

    $directory = Split-Path $resolved -Parent
    $url = "http://localhost:$($fileMeta.Port)/$($fileMeta.File)"
    $cmd = "cd `"$directory`"; python -m http.server $($fileMeta.Port)"

    Write-Host "> Démarrage de $($fileMeta.Label) sur le port $($fileMeta.Port) ( $url )"
    Start-Process pwsh -ArgumentList '-NoExit', '-Command', $cmd
}