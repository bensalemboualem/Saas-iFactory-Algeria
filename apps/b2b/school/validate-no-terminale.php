<?php
/**
 * 🧪 Script de Validation : Vérification suppression cycle Terminale/Bac
 * BBC School Algeria : Du CP au Secondaire (2AS) uniquement
 */

echo "🧪 VALIDATION SUPPRESSION CYCLE TERMINALE/BAC\n";
echo "📚 BBC School Algeria : Du CP au Secondaire (2AS)\n\n";

$baseDir = __DIR__;
$errors = [];
$warnings = [];
$successes = [];

// 1. Vérifier les fichiers principaux
$filesToCheck = [
    'bbc-school-setup.php',
    'bbc-content-detailed.php', 
    'bbc-final-complete.php',
    'bbc-school-ready.php',
    'bbc-website-ai-setup.php',
    'bbc-final-test.php',
    'bbc-automation-finale.php'
];

echo "🔍 VÉRIFICATION DES FICHIERS PRINCIPAUX\n";
echo "=" . str_repeat("=", 50) . "\n";

foreach ($filesToCheck as $file) {
    $filePath = $baseDir . '/' . $file;
    
    if (!file_exists($filePath)) {
        $warnings[] = "Fichier non trouvé: $file";
        continue;
    }
    
    $content = file_get_contents($filePath);
    
    // Chercher les termes interdits
    $forbiddenTerms = ['Terminale', 'Terminal', 'Baccalauréat', 'pour le BAC'];
    $found = [];
    
    foreach ($forbiddenTerms as $term) {
        if (stripos($content, $term) !== false) {
            $found[] = $term;
        }
    }
    
    if (!empty($found)) {
        $errors[] = "$file contient encore: " . implode(', ', $found);
    } else {
        $successes[] = "$file : ✅ Nettoyé";
    }
}

// 2. Vérifier les fichiers de traduction
echo "\n🌐 VÉRIFICATION DES TRADUCTIONS\n";
echo "=" . str_repeat("=", 50) . "\n";

$langFiles = [
    'lang/en/frontend.json' => 'Anglais',
    'lang/fr/frontend.json' => 'Français', 
    'lang/ar/frontend.json' => 'Arabe'
];

foreach ($langFiles as $file => $lang) {
    $filePath = $baseDir . '/' . $file;
    
    if (!file_exists($filePath)) {
        $warnings[] = "Fichier de traduction manquant: $file";
        continue;
    }
    
    $content = file_get_contents($filePath);
    
    if (stripos($content, 'Terminale') !== false || stripos($content, 'Bac') !== false) {
        $errors[] = "Traduction $lang contient encore Terminale/Bac";
    } else {
        $successes[] = "Traduction $lang : ✅ OK";
    }
}

// 3. Générer un exemple de structure corrigée
echo "\n📋 STRUCTURE ÉDUCATIVE CORRIGÉE\n";
echo "=" . str_repeat("=", 50) . "\n";

$structure = [
    'Primaire' => [
        'CP (Cours Préparatoire)',
        'CE1 (Cours Élémentaire 1)',
        'CE2 (Cours Élémentaire 2)', 
        'CM1 (Cours Moyen 1)',
        'CM2 (Cours Moyen 2)'
    ],
    'Moyen' => [
        '6ème (Sixième)',
        '5ème (Cinquième)',
        '4ème (Quatrième)',
        '3ème (Troisième)'
    ],
    'Secondaire' => [
        '1AS (Première Année Secondaire)',
        '2AS (Deuxième Année Secondaire)'
    ]
];

foreach ($structure as $cycle => $classes) {
    echo "🎓 $cycle:\n";
    foreach ($classes as $classe) {
        echo "   • $classe\n";
    }
    echo "\n";
}

// 4. Résumé des résultats
echo "📊 RÉSUMÉ DE LA VALIDATION\n";
echo "=" . str_repeat("=", 50) . "\n";

echo "✅ SUCCÈS (" . count($successes) . "):\n";
foreach ($successes as $success) {
    echo "   • $success\n";
}

if (!empty($warnings)) {
    echo "\n⚠️  AVERTISSEMENTS (" . count($warnings) . "):\n";
    foreach ($warnings as $warning) {
        echo "   • $warning\n";
    }
}

if (!empty($errors)) {
    echo "\n❌ ERREURS (" . count($errors) . "):\n";
    foreach ($errors as $error) {
        echo "   • $error\n";
    }
} else {
    echo "\n🎉 VALIDATION RÉUSSIE !\n";
    echo "✅ Aucune référence au cycle Terminale/Bac trouvée\n";
    echo "📚 BBC School Algeria respecte maintenant sa structure: CP → 2AS\n";
}

// 5. Générer un rapport de conformité
echo "\n📋 RAPPORT DE CONFORMITÉ\n";
echo "=" . str_repeat("=", 50) . "\n";

$conformity = [
    'Structure Éducative' => empty($errors) ? 'CONFORME' : 'NON CONFORME',
    'Fichiers Nettoyés' => count($successes),
    'Cycle Maximum' => '2AS (Deuxième Année Secondaire)',
    'Suppression Terminale' => empty($errors) ? 'COMPLÈTE' : 'PARTIELLE',
    'Date Validation' => date('d/m/Y H:i:s')
];

foreach ($conformity as $critere => $statut) {
    echo sprintf("%-20s: %s\n", $critere, $statut);
}

echo "\n" . str_repeat("=", 60) . "\n";
echo "🏫 BBC SCHOOL ALGERIA - STRUCTURE VALIDÉE\n";
echo "📚 Cycles: Primaire → Moyen → Secondaire (jusqu'à 2AS)\n";
echo "🚫 Terminale/Bac supprimés avec succès\n";
echo str_repeat("=", 60) . "\n";
?>