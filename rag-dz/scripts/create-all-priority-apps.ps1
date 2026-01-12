# Script de création automatique de toutes les apps prioritaires
# IAFactory Algeria - Création SaaS complet

Write-Host "🚀 Création automatique de toutes les apps prioritaires..." -ForegroundColor Green
Write-Host ""

# Liste des apps à créer (PRIORITÉ TRÈS HAUTE)
$apps = @(
    @{Name="agri-dz"; Port=8225; Icon="🌾"; Title="Agri-DZ Assistant"; Description="Assistant agricole intelligent pour l'Algérie"},
    @{Name="pharma-dz"; Port=8221; Icon="💊"; Title="Pharma-DZ Manager"; Description="Gestion complète pharmacie algérienne"},
    @{Name="industrie-dz"; Port=8231; Icon="🏭"; Title="Industrie-DZ Manager"; Description="Gestion production industrielle"},
    @{Name="agroalimentaire-dz"; Port=8234; Icon="🍞"; Title="Agroalimentaire DZ"; Description="Industrie agroalimentaire - HACCP & traçabilité"},
    @{Name="btp-dz"; Port=8245; Icon="🏗️"; Title="BTP-DZ Assistant"; Description="Devis, métré, RPA 99 pour BTP"},
    @{Name="douanes-dz"; Port=8251; Icon="🛃"; Title="Douanes-DZ Assistant"; Description="Déclarations douanières et calcul taxes"},
    @{Name="commerce-dz"; Port=8254; Icon="🛒"; Title="Commerce-DZ POS"; Description="Caisse enregistreuse conforme DGI"},
    @{Name="ecommerce-dz"; Port=8255; Icon="🛍️"; Title="E-Commerce DZ"; Description="Boutique en ligne - Satim, Yalidine"},
    @{Name="expert-comptable-dz"; Port=8263; Icon="📊"; Title="Expert Comptable DZ"; Description="Comptabilité PCN 2009 + déclarations fiscales"},
    @{Name="clinique-dz"; Port=8222; Icon="🏨"; Title="Clinique-DZ Pro"; Description="Gestion complète clinique privée"},
    @{Name="irrigation-dz"; Port=8226; Icon="💧"; Title="Irrigation & Eau DZ"; Description="Calcul besoins eau + autorisations ANRH"},
    @{Name="transport-dz"; Port=8250; Icon="🚛"; Title="Transport-DZ Manager"; Description="Gestion flotte + GPS tracking"},
    @{Name="universite-dz"; Port=8239; Icon="🎓"; Title="Université-DZ Assistant"; Description="Gestion emplois temps + PFE universitaires"},
    @{Name="formation-pro-dz"; Port=8240; Icon="💼"; Title="Formation Pro DZ"; Description="CFPA/INSFP - certifications métiers"}
)

$totalApps = $apps.Count
$current = 0

foreach ($app in $apps) {
    $current++
    $percent = [math]::Round(($current / $totalApps) * 100)

    Write-Host "[$current/$totalApps] Création de $($app.Title)..." -ForegroundColor Cyan
    Write-Host "    📁 apps/$($app.Name)" -ForegroundColor Gray
    Write-Host "    🌐 Port: $($app.Port)" -ForegroundColor Gray

    # Créer le dossier
    $appPath = "apps/$($app.Name)"
    New-Item -ItemType Directory -Force -Path $appPath | Out-Null

    # Créer index.html basique
    $indexContent = @"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$($app.Icon) $($app.Title) - IAFactory Algeria</title>
    <style>
        :root {
            --primary: #10b981;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --dz-green: #006233;
            --dz-red: #d21034;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, var(--dz-green) 0%, var(--primary) 100%);
            padding: 2rem;
            border-bottom: 3px solid var(--dz-red);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
            flex: 1;
        }
        h1 {
            font-size: 3rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: var(--text-secondary);
            margin-bottom: 3rem;
        }
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .btn {
            background: var(--primary);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            cursor: pointer;
            display: inline-block;
            text-decoration: none;
        }
        .btn:hover {
            background: #059669;
            transform: translateY(-2px);
        }
        .back-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.1);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            color: white;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <a href="../../landing-complete-responsive.html" class="back-btn">← Retour</a>

    <header class="header">
        <div class="container">
            <h1>$($app.Icon) $($app.Title)</h1>
            <p class="subtitle">$($app.Description)</p>
        </div>
    </header>

    <main class="container">
        <div class="card">
            <h2>🚀 Application en cours de développement</h2>
            <p style="margin: 1.5rem 0; font-size: 1.1rem; color: var(--text-secondary);">
                Cette application est actuellement en développement et sera bientôt disponible.<br>
                Elle fera partie de la plateforme complète IAFactory Algeria SaaS.
            </p>
            <a href="../../landing-complete-responsive.html" class="btn">
                📋 Voir toutes les applications
            </a>
        </div>

        <div class="card">
            <h3>💡 Fonctionnalités prévues</h3>
            <ul style="margin-top: 1rem; padding-left: 2rem; line-height: 2;">
                <li>Interface intuitive en français/arabe</li>
                <li>Intelligence artificielle intégrée</li>
                <li>Conforme réglementation algérienne</li>
                <li>Export PDF/Excel</li>
                <li>Support client dédié</li>
            </ul>
        </div>

        <div class="card">
            <h3>📞 Vous êtes intéressé ?</h3>
            <p style="margin: 1rem 0;">
                Contactez-nous pour être informé du lancement ou pour participer au programme bêta.
            </p>
            <p style="font-weight: 600;">
                📧 contact@iafactoryalgeria.com<br>
                🇩🇿 Algérie
            </p>
        </div>
    </main>

    <footer style="background: var(--bg-card); padding: 2rem; text-align: center; margin-top: auto;">
        <p>&copy; 2025 IAFactory Algeria - Plateforme SaaS pour l'Algérie 🇩🇿</p>
    </footer>
</body>
</html>
"@

    Set-Content -Path "$appPath/index.html" -Value $indexContent -Encoding UTF8

    # Créer README.md
    $readmeContent = @"
# $($app.Icon) $($app.Title)

**$($app.Description)**

## 📋 Description

Application en cours de développement pour la plateforme IAFactory Algeria SaaS.

## 🎯 Fonctionnalités prévues

- Interface multilingue (FR/AR)
- Intelligence artificielle
- Conformité réglementation algérienne
- Export de données
- Support client

## 🌐 Accès

- **Port:** $($app.Port)
- **URL locale:** http://localhost:$($app.Port)
- **URL production:** https://www.iafactoryalgeria.com/apps/$($app.Name)

## 🚀 Lancement

``````bash
# Développement
npm run dev -- --port $($app.Port)

# Production
docker-compose up -d
``````

## 📞 Support

Email: support@iafactoryalgeria.com

---

**Développé par IAFactory Algeria** 🇩🇿
"@

    Set-Content -Path "$appPath/README.md" -Value $readmeContent -Encoding UTF8

    Write-Host "    ✅ Créé avec succès" -ForegroundColor Green
    Write-Host ""
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ $totalApps applications créées avec succès !" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Résumé:" -ForegroundColor Yellow
Write-Host "   • Prof-DZ Assistant: ✅ COMPLET (app phare)" -ForegroundColor White
Write-Host "   • $totalApps apps prioritaires: ✅ Structure de base créée" -ForegroundColor White
Write-Host "   • Toutes les apps ont index.html + README.md" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "   1. Compléter les apps existantes incomplètes" -ForegroundColor White
Write-Host "   2. Créer landing page catalogue complet" -ForegroundColor White
Write-Host "   3. Intégrer backend RAG pour toutes les apps" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Votre SaaS est prêt à être présenté !" -ForegroundColor Green
