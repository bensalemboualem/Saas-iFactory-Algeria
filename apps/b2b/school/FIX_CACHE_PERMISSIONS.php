<?php
/**
 * FIX CACHE PERMISSIONS - Résout les problèmes de permissions Windows
 */

echo "\n========================================\n";
echo "CORRECTION DES PERMISSIONS CACHE\n";
echo "========================================\n\n";

// Chemins
$bootstrapCache = __DIR__ . '/bootstrap/cache';
$storageFramework = __DIR__ . '/storage/framework';

// Fonction pour supprimer les fichiers en toute sécurité
function deleteFiles($dir, $pattern = '*') {
    $files = glob($dir . '/' . $pattern);
    $count = 0;
    foreach ($files as $file) {
        if (is_file($file)) {
            try {
                // Essayer de donner les permissions en écriture
                @chmod($file, 0777);

                // Essayer de supprimer
                if (@unlink($file)) {
                    $count++;
                } else {
                    echo "⚠️  Impossible de supprimer: " . basename($file) . "\n";
                }
            } catch (Exception $e) {
                echo "⚠️  Erreur: " . $e->getMessage() . "\n";
            }
        }
    }
    return $count;
}

// Fonction pour donner les permissions à un dossier
function setPermissions($dir) {
    if (!is_dir($dir)) {
        echo "⚠️  Dossier introuvable: $dir\n";
        return false;
    }

    try {
        @chmod($dir, 0777);

        // Permissions récursives
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
            RecursiveIteratorIterator::SELF_FIRST
        );

        foreach ($iterator as $item) {
            @chmod($item, 0777);
        }

        return true;
    } catch (Exception $e) {
        echo "⚠️  Erreur permissions: " . $e->getMessage() . "\n";
        return false;
    }
}

echo "1. Nettoyage bootstrap/cache...\n";
$count1 = deleteFiles($bootstrapCache, '*.php');
echo "   ✅ $count1 fichier(s) supprimé(s)\n\n";

echo "2. Nettoyage storage/framework/cache...\n";
$cacheDataDir = $storageFramework . '/cache/data';
if (is_dir($cacheDataDir)) {
    $count2 = deleteFiles($cacheDataDir, '*');
    echo "   ✅ $count2 fichier(s) supprimé(s)\n";
} else {
    echo "   ⚠️  Dossier non trouvé\n";
}
echo "\n";

echo "3. Nettoyage storage/framework/views...\n";
$viewsDir = $storageFramework . '/views';
$count3 = deleteFiles($viewsDir, '*.php');
echo "   ✅ $count3 fichier(s) supprimé(s)\n\n";

echo "4. Attribution des permissions...\n";
if (setPermissions($bootstrapCache)) {
    echo "   ✅ Permissions bootstrap/cache\n";
}
if (setPermissions($storageFramework)) {
    echo "   ✅ Permissions storage/framework\n";
}
echo "\n";

echo "========================================\n";
echo "CORRECTION TERMINÉE!\n";
echo "========================================\n\n";

echo "MAINTENANT:\n";
echo "1. Rechargez la page dans le navigateur: Ctrl+Shift+R\n";
echo "2. Si le problème persiste, exécutez en tant qu'administrateur:\n";
echo "   FIX_PERMISSIONS_WINDOWS.bat\n\n";

// Créer un fichier .gitignore pour éviter les problèmes futurs
$gitignoreBootstrap = $bootstrapCache . '/.gitignore';
if (!file_exists($gitignoreBootstrap)) {
    file_put_contents($gitignoreBootstrap, "*\n!.gitignore\n");
    echo "✅ .gitignore créé dans bootstrap/cache\n";
}

$gitignoreViews = $viewsDir . '/.gitignore';
if (!file_exists($gitignoreViews)) {
    file_put_contents($gitignoreViews, "*\n!.gitignore\n");
    echo "✅ .gitignore créé dans storage/framework/views\n";
}

echo "\n";

?>
