<?php

require_once 'vendor/autoload.php';

$app = require_once 'bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

echo "🔍 TEST COMPLET DASHBOARD BBC SCHOOL ALGERIA\n";
echo "=" . str_repeat("=", 50) . "\n\n";

try {
    echo "🧪 TEST DU CONTROLLER:\n";
    
    // Simuler l'appel du controller
    $controller = new \App\Http\Controllers\Backend\DashboardController(
        new \App\Repositories\DashboardRepository()
    );
    
    // Appeler la méthode index (comme sur la vraie page)
    $data = $controller->index();
    
    echo "Type de retour: " . gettype($data) . "\n";
    
    if (is_object($data) && method_exists($data, 'getData')) {
        $viewData = $data->getData();
        echo "Données passées à la vue:\n";
        if (isset($viewData['data'])) {
            foreach($viewData['data'] as $key => $value) {
                if(is_array($value)) {
                    echo "   $key: [array avec " . count($value) . " éléments]\n";
                } else {
                    echo "   $key: $value\n";
                }
            }
        }
    }
    
    echo "\n🔍 TEST DIRECT DU REPOSITORY:\n";
    $repo = new \App\Repositories\DashboardRepository();
    $repoData = $repo->index();
    
    echo "Repository data:\n";
    foreach($repoData as $key => $value) {
        if(is_array($value)) {
            echo "   $key: [array avec " . count($value) . " éléments]\n";
        } else {
            echo "   $key: $value\n";
        }
    }
    
    echo "\n📊 VÉRIFICATION TEMPLATE:\n";
    // Simuler le passage à la vue
    $templateData = compact('data');
    echo "Data disponible pour le template:\n";
    foreach($templateData['data'] as $key => $value) {
        if(is_array($value)) {
            echo "   \$data['$key']: [array avec " . count($value) . " éléments]\n";
        } else {
            echo "   \$data['$key']: $value\n";
        }
    }
    
    echo "\n🎯 CODE BLADE ÉQUIVALENT:\n";
    echo "{{ \$data['student'] }} -> " . $repoData['student'] . "\n";
    echo "{{ \$data['parent'] }} -> " . $repoData['parent'] . "\n";
    echo "{{ \$data['teacher'] }} -> " . $repoData['teacher'] . "\n";
    echo "{{ \$data['session'] }} -> " . $repoData['session'] . "\n";
    
    echo "\n✅ Test terminé !\n";
    
} catch (Exception $e) {
    echo "❌ ERREUR: " . $e->getMessage() . "\n";
    echo "📍 Fichier: " . $e->getFile() . ":" . $e->getLine() . "\n";
    echo "📚 Stack trace:\n" . $e->getTraceAsString() . "\n";
}