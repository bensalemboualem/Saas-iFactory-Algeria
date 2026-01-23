<?php
echo "=== NETTOYAGE COMPLET DES CACHES ===\n\n";

$basePath = __DIR__;

// 1. Nettoyer les vues Blade
$viewCachePath = $basePath . '/storage/framework/views';
echo "1. Nettoyage des vues Blade...\n";
if (is_dir($viewCachePath)) {
    $files = glob($viewCachePath . '/*.php');
    $count = 0;
    foreach ($files as $file) {
        if (is_file($file)) {
            unlink($file);
            $count++;
        }
    }
    echo "   ✅ $count fichier(s) supprimé(s)\n";
} else {
    echo "   ⚠️  Dossier non trouvé\n";
}

// 2. Nettoyer le cache config
$configCachePath = $basePath . '/bootstrap/cache';
echo "\n2. Nettoyage du cache config...\n";
if (is_dir($configCachePath)) {
    $files = glob($configCachePath . '/*.php');
    $count = 0;
    foreach ($files as $file) {
        if (is_file($file) && basename($file) !== '.gitignore') {
            unlink($file);
            $count++;
        }
    }
    echo "   ✅ $count fichier(s) supprimé(s)\n";
} else {
    echo "   ⚠️  Dossier non trouvé\n";
}

// 3. Nettoyer le cache de données
$dataCachePath = $basePath . '/storage/framework/cache/data';
echo "\n3. Nettoyage du cache de données...\n";
if (is_dir($dataCachePath)) {
    $files = glob($dataCachePath . '/*');
    $count = 0;
    foreach ($files as $file) {
        if (is_file($file)) {
            unlink($file);
            $count++;
        }
    }
    echo "   ✅ $count fichier(s) supprimé(s)\n";
} else {
    echo "   ⚠️  Dossier non trouvé\n";
}

// 4. Vérification finale
echo "\n4. Vérification finale...\n";
$viewFiles = glob($viewCachePath . '/*.php');
if (count($viewFiles) === 0) {
    echo "   ✅ Tous les caches de vues sont nettoyés\n";
} else {
    echo "   ⚠️  Il reste " . count($viewFiles) . " fichier(s) de cache\n";
}

echo "\n=== NETTOYAGE TERMINÉ ===\n\n";
echo "MAINTENANT:\n";
echo "1. Ouvrez: http://localhost/onestschooled-test/public/contact\n";
echo "2. Appuyez sur Ctrl+Shift+R (ou Ctrl+F5) pour forcer le rechargement\n";
echo "3. Faites défiler vers le bas\n";
echo "4. Vous DEVEZ voir la section 'Nos Établissements BBC School Algeria'\n";
echo "   avec les 3 cartes:\n";
echo "   - 🏢 Direction Générale (Bouchaoui)\n";
echo "   - 🏫 École Principale (Ain Benian)\n";
echo "   - 🏠 Annexe Maternelle (Chéraga)\n";
