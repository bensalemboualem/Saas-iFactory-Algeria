<?php
/**
 * 🔧 Script de Correction : Suppression des références au cycle Terminale/Bac
 * BBC School Algeria s'arrête au secondaire (2AS)
 */

echo "🔧 SUPPRESSION DES RÉFÉRENCES AU CYCLE TERMINALE/BAC\n";
echo "📚 BBC School Algeria s'arrête au secondaire (2AS)\n\n";

// Fonction pour faire une sauvegarde
function backupFile($file) {
    $backup = $file . '.backup.' . date('Y-m-d-H-i-s');
    copy($file, $backup);
    echo "💾 Sauvegarde: $backup\n";
}

// Liste des fichiers à corriger
$filesToCorrect = [
    'bbc-school-setup.php',
    'bbc-content-detailed.php', 
    'bbc-final-complete.php',
    'bbc-school-ready.php',
    'bbc-website-ai-setup.php',
    'bbc-final-test.php',
    'bbc-automation-finale.php'
];

$corrections = [
    // Remplacements pour supprimer les références au Bac/Terminale
    'Terminale (Terminal)' => 'Seconde AS (2AS)',
    'Terminale-Sciences' => '2AS-Sciences', 
    'Terminale-Lettres' => '2AS-Lettres',
    'Terminale Sciences' => '2AS Sciences',
    'Terminale Lettres' => '2AS Lettres',
    'Algèbre et Analyse - Terminale S' => 'Algèbre - 2AS Sciences',
    'Frais Lycée (2AS-1AS-Terminale)' => 'Frais Lycée (1AS-2AS)',
    'Frais Lycée (2AS-Terminale)' => 'Frais Lycée (1AS-2AS)',
    'Du CP à la Terminale' => 'Du CP au Secondaire (2AS)',
    'CP à la Terminale' => 'CP au Secondaire (2AS)',
    'Enseignement Secondaire (2AS-Terminale)' => 'Enseignement Secondaire (1AS-2AS)',
    '2AS à Terminale' => '1AS à 2AS',
    'pour le Baccalauréat' => 'niveau secondaire',
    'pour préparer le BAC' => 'pour le niveau secondaire',
    'CP-Terminale' => 'CP-Secondaire',
    'Cursus Complet CP-Terminale' => 'Cursus Complet CP-Secondaire'
];

$totalCorrections = 0;

foreach ($filesToCorrect as $filename) {
    $filePath = __DIR__ . '/' . $filename;
    
    if (!file_exists($filePath)) {
        echo "⚠️  Fichier non trouvé: $filename\n";
        continue;
    }
    
    echo "📝 Traitement: $filename\n";
    
    // Sauvegarde
    backupFile($filePath);
    
    // Lecture du contenu
    $content = file_get_contents($filePath);
    $originalContent = $content;
    
    // Appliquer les corrections
    foreach ($corrections as $search => $replace) {
        $newContent = str_replace($search, $replace, $content);
        if ($newContent !== $content) {
            echo "   ✅ Corrigé: '$search' → '$replace'\n";
            $totalCorrections++;
        }
        $content = $newContent;
    }
    
    // Sauvegarder si des changements ont été faits
    if ($content !== $originalContent) {
        file_put_contents($filePath, $content);
        echo "   💾 Fichier mis à jour: $filename\n";
    } else {
        echo "   ℹ️  Aucune modification nécessaire\n";
    }
    
    echo "\n";
}

echo "🎯 RÉSUMÉ DES CORRECTIONS\n";
echo "=" . str_repeat("=", 40) . "\n";
echo "📊 Total des corrections appliquées: $totalCorrections\n";
echo "✅ BBC School Algeria maintenant limité au secondaire (2AS)\n";
echo "🚫 Références au Bac/Terminale supprimées\n\n";

// Vérification des fichiers de traduction
echo "🌐 VÉRIFICATION DES FICHIERS DE TRADUCTION\n";
echo "=" . str_repeat("=", 40) . "\n";

$langFiles = [
    'lang/en/frontend.json',
    'lang/fr/frontend.json', 
    'lang/ar/frontend.json'
];

foreach ($langFiles as $langFile) {
    $fullPath = __DIR__ . '/' . $langFile;
    
    if (file_exists($fullPath)) {
        $content = file_get_contents($fullPath);
        
        if (strpos($content, 'Terminale') !== false || strpos($content, 'Bac') !== false) {
            echo "⚠️  $langFile contient encore des références Terminale/Bac\n";
            echo "   Correction manuelle nécessaire\n";
        } else {
            echo "✅ $langFile : OK\n";
        }
    } else {
        echo "⚠️  $langFile : Fichier non trouvé\n";
    }
}

echo "\n🎉 CORRECTION TERMINÉE !\n";
echo "📚 BBC School Algeria : Du CP au Secondaire (2AS) uniquement\n";
?>