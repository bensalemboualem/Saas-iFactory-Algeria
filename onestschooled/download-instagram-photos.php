<?php
/**
 * 📸 BBC School Algeria - Photos d'exemple pour Instagram
 * Téléchargement automatique de photos d'école pour démonstration
 */

echo "📸 TÉLÉCHARGEMENT PHOTOS D'EXEMPLE POUR BBC SCHOOL\n";
echo "================================================\n\n";

$uploadDir = __DIR__ . '/public/backend/uploads/instagram/';

// Nettoyer le dossier des fichiers HTML
echo "🧹 Nettoyage du dossier...\n";
$files = glob($uploadDir . '*');
foreach($files as $file) {
    if(is_file($file)) {
        unlink($file);
        echo "   🗑️ Supprimé: " . basename($file) . "\n";
    }
}

// Supprimer les dossiers
$dirs = glob($uploadDir . '*', GLOB_ONLYDIR);
foreach($dirs as $dir) {
    $iterator = new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS);
    $files = new RecursiveIteratorIterator($iterator, RecursiveIteratorIterator::CHILD_FIRST);
    foreach($files as $file) {
        if ($file->isDir()) {
            rmdir($file->getRealPath());
        } else {
            unlink($file->getRealPath());
        }
    }
    rmdir($dir);
    echo "   📁 Dossier supprimé: " . basename($dir) . "\n";
}

echo "\n📥 Téléchargement de photos d'école...\n";

// Photos d'école réelles (Unsplash - libres de droits)
$schoolPhotos = [
    [
        'url' => 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_campus_001.jpg',
        'description' => 'Campus d\'école moderne'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_students_002.jpg', 
        'description' => 'Étudiants en classe'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_classes_003.jpg',
        'description' => 'Salle de classe moderne'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_transport_004.jpg',
        'description' => 'Bus scolaire'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_lab_005.jpg',
        'description' => 'Laboratoire scientifique'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_library_007.jpg',
        'description' => 'Bibliothèque'
    ],
    [
        'url' => 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop&crop=center',
        'filename' => 'bbc_sports_008.jpg',
        'description' => 'Terrain de sport'
    ]
];

$successful = 0;
$failed = 0;

foreach($schoolPhotos as $photo) {
    echo "📸 {$photo['description']}... ";
    
    try {
        $imageData = @file_get_contents($photo['url']);
        
        if($imageData !== false && strlen($imageData) > 1000) {
            file_put_contents($uploadDir . $photo['filename'], $imageData);
            
            if(file_exists($uploadDir . $photo['filename'])) {
                $size = round(filesize($uploadDir . $photo['filename']) / 1024, 1);
                echo "✅ OK ({$size}KB)\n";
                $successful++;
            } else {
                echo "❌ Erreur sauvegarde\n";
                $failed++;
            }
        } else {
            echo "❌ Téléchargement échoué\n";
            $failed++;
        }
    } catch(Exception $e) {
        echo "❌ Erreur: " . $e->getMessage() . "\n";
        $failed++;
    }
    
    // Délai pour éviter de surcharger l'API
    usleep(200000); // 0.2 seconde
}

echo "\n📊 RÉSULTATS:\n";
echo "✅ Photos téléchargées: $successful\n";
echo "❌ Échecs: $failed\n";

echo "\n📁 CONTENU DU DOSSIER:\n";
$files = glob($uploadDir . '*.jpg');
foreach($files as $file) {
    $filename = basename($file);
    $size = round(filesize($file) / 1024, 1);
    echo "   📸 $filename ({$size}KB)\n";
}

echo "\n🔗 URLs D'ACCÈS:\n";
foreach($files as $file) {
    $filename = basename($file);
    echo "   http://localhost:8000/backend/uploads/instagram/$filename\n";
}

echo "\n✅ PHOTOS D'EXEMPLE INSTALLÉES!\n";
echo "🚀 Démarre le serveur: php artisan serve --host=127.0.0.1 --port=8000\n";
echo "🌐 Puis va sur: http://localhost:8000/instagram\n";
?>