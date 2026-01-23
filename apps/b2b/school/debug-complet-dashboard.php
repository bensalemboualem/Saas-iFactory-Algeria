<?php

require_once 'vendor/autoload.php';

$app = require_once 'bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

echo "🔧 DEBUG COMPLET DASHBOARD BBC SCHOOL\n";
echo "=" . str_repeat("=", 50) . "\n\n";

// 1. Test des données
$repo = new \App\Repositories\DashboardRepository();
$data = $repo->index();

echo "1. ✅ DONNÉES RÉCUPÉRÉES:\n";
foreach($data as $key => $value) {
    echo "   $key: " . (is_array($value) ? '['.count($value).' items]' : $value) . "\n";
}

// 2. Test de la vue
echo "\n2. ✅ TEST RENDU VUE:\n";
try {
    $view = view('backend.dashboard', compact('data'));
    $html = $view->render();
    
    echo "   ✅ Vue rendue avec succès\n";
    echo "   📏 Taille HTML: " . strlen($html) . " chars\n";
    
    // Chercher les compteurs
    if (strpos($html, 'ot_crm_summeryBox2') !== false) {
        echo "   ✅ Classes CSS ot_crm_summeryBox2 trouvées\n";
    } else {
        echo "   ❌ Classes CSS ot_crm_summeryBox2 MANQUANTES\n";
    }
    
    // Chercher les données
    if (strpos($html, '804') !== false) {
        echo "   ✅ Donnée 804 trouvée dans HTML\n";
    } else {
        echo "   ❌ Donnée 804 MANQUANTE dans HTML\n";
    }
    
    // Chercher les icônes
    if (strpos($html, '🎓') !== false) {
        echo "   ✅ Émojis trouvés dans HTML\n";
    } else {
        echo "   ❌ Émojis MANQUANTS dans HTML\n";
    }
    
} catch (Exception $e) {
    echo "   ❌ ERREUR RENDU: " . $e->getMessage() . "\n";
}

// 3. Test de la route
echo "\n3. ✅ TEST ROUTE:\n";
try {
    $request = \Illuminate\Http\Request::create('/dashboard', 'GET');
    $controller = new \App\Http\Controllers\Backend\DashboardController($repo);
    $response = $controller->index();
    
    echo "   ✅ Route dashboard accessible\n";
    echo "   📄 Type réponse: " . get_class($response) . "\n";
    
} catch (Exception $e) {
    echo "   ❌ ERREUR ROUTE: " . $e->getMessage() . "\n";
}

// 4. Test des assets
echo "\n4. ✅ TEST ASSETS:\n";
$cssFile = 'public/backend/assets/css/style2.css';
if (file_exists($cssFile)) {
    echo "   ✅ Fichier CSS existe\n";
    
    $css = file_get_contents($cssFile);
    if (strpos($css, 'ot_crm_summeryBox2') !== false) {
        echo "   ✅ Classes CSS ot_crm_summeryBox2 dans le fichier\n";
    } else {
        echo "   ❌ Classes CSS ot_crm_summeryBox2 MANQUANTES du fichier\n";
    }
} else {
    echo "   ❌ Fichier CSS style2.css MANQUANT\n";
}

echo "\n✅ DEBUG TERMINÉ !\n";
echo "\nSI TOUT EST ✅ MAIS QUE ÇA NE MARCHE PAS:\n";
echo "- Le problème vient du navigateur/cache\n";
echo "- Ou d'une redirection vers un autre dashboard\n";
echo "- Ou d'un problème de permissions/middleware\n";

?>