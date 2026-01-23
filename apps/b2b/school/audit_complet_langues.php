<?php
/**
 * AUDIT COMPLET LIGNE PAR LIGNE - TOUTES LES LANGUES
 * Vérifie CHAQUE fichier JSON pour trouver TOUS les termes en anglais
 */

require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make('Illuminate\Contracts\Console\Kernel');
$kernel->bootstrap();

echo "=== AUDIT COMPLET DES LANGUES ===\n\n";
echo "Vérification ligne par ligne de TOUS les fichiers JSON...\n\n";

$langDirs = [
    'ar' => 'Arabe',
    'fr' => 'Français',
];

$totalIssues = 0;
$issuesByLang = [];

foreach ($langDirs as $langCode => $langName) {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
    echo "LANGUE: $langName ($langCode)\n";
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

    $langDir = __DIR__ . "/lang/$langCode/";
    $jsonFiles = glob($langDir . '*.json');

    $langIssues = 0;

    foreach ($jsonFiles as $filePath) {
        $fileName = basename($filePath);
        $content = file_get_contents($filePath);
        $json = json_decode($content, true);

        if ($json === null) {
            echo "⚠️  ERREUR DE DÉCODAGE: $fileName\n\n";
            continue;
        }

        $fileIssues = [];

        foreach ($json as $key => $value) {
            // Vérifier si la valeur est en anglais
            $isEnglish = false;

            // Critères pour détecter l'anglais:
            // 1. Ne contient pas de caractères arabes
            // 2. Ne contient pas de caractères français spéciaux
            // 3. Contient des mots anglais courants

            if ($langCode === 'ar') {
                // Pour l'arabe, vérifier absence de caractères arabes
                if (!preg_match('/[\x{0600}-\x{06FF}]/u', $value)) {
                    // Liste de mots anglais courants à détecter
                    $englishWords = [
                        'the', 'is', 'are', 'and', 'or', 'of', 'to', 'in', 'on', 'at',
                        'Add', 'Edit', 'Delete', 'Update', 'Save', 'Cancel', 'Submit',
                        'List', 'View', 'Show', 'Create', 'New', 'Search', 'Filter',
                        'Student', 'Teacher', 'Parent', 'Class', 'Section', 'Subject',
                        'Exam', 'Fee', 'Report', 'Attendance', 'Leave', 'Dashboard',
                        'Settings', 'Profile', 'Logout', 'Login', 'Register', 'Forgot',
                        'Password', 'Email', 'Phone', 'Address', 'Date', 'Time',
                        'Status', 'Active', 'Inactive', 'Pending', 'Approved', 'Rejected',
                        'Name', 'Description', 'Title', 'Content', 'Message', 'Note'
                    ];

                    foreach ($englishWords as $word) {
                        if (stripos($value, $word) !== false) {
                            $isEnglish = true;
                            break;
                        }
                    }
                }
            } elseif ($langCode === 'fr') {
                // Pour le français, vérifier si c'est de l'anglais pur
                $englishWords = [
                    'Student', 'Teacher', 'Parent', 'Class', 'Section', 'Subject',
                    'Exam', 'Fee', 'Report', 'Attendance', 'Leave', 'Dashboard',
                    'Settings', 'Profile', 'Logout', 'Login', 'Register',
                    'Add New', 'Edit', 'Delete', 'Update', 'Save', 'Cancel',
                    'List', 'View', 'Show', 'Create', 'Search', 'Filter'
                ];

                foreach ($englishWords as $word) {
                    if (stripos($value, $word) !== false && !preg_match('/[àâäéèêëïîôùûüÿçœæ]/i', $value)) {
                        $isEnglish = true;
                        break;
                    }
                }
            }

            if ($isEnglish) {
                $fileIssues[] = [
                    'key' => $key,
                    'value' => $value
                ];
                $langIssues++;
                $totalIssues++;
            }
        }

        // Afficher les problèmes du fichier
        if (!empty($fileIssues)) {
            echo "📄 FICHIER: $fileName\n";
            echo "   Problèmes trouvés: " . count($fileIssues) . "\n\n";

            foreach ($fileIssues as $issue) {
                echo "   ❌ \"{$issue['key']}\" → \"{$issue['value']}\"\n";
            }
            echo "\n";

            $issuesByLang[$langCode][$fileName] = $fileIssues;
        }
    }

    if ($langIssues === 0) {
        echo "✅ AUCUN PROBLÈME TROUVÉ!\n\n";
    } else {
        echo "⚠️  TOTAL: $langIssues terme(s) en anglais trouvé(s)\n\n";
    }
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
echo "RÉSUMÉ GLOBAL\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

if ($totalIssues > 0) {
    echo "⚠️  TOTAL: $totalIssues terme(s) en anglais trouvé(s)\n\n";

    echo "RÉPARTITION PAR LANGUE:\n";
    foreach ($issuesByLang as $lang => $files) {
        $count = 0;
        foreach ($files as $issues) {
            $count += count($issues);
        }
        echo "   $lang: $count terme(s) dans " . count($files) . " fichier(s)\n";
    }

    echo "\n";
    echo "GÉNÉRATION DU FICHIER DE CORRECTION...\n";

    // Créer un fichier avec toutes les corrections à faire
    $corrections = [];
    foreach ($issuesByLang as $lang => $files) {
        foreach ($files as $fileName => $issues) {
            foreach ($issues as $issue) {
                $corrections[] = [
                    'lang' => $lang,
                    'file' => $fileName,
                    'key' => $issue['key'],
                    'current' => $issue['value'],
                    'needed' => 'CORRECTION REQUISE'
                ];
            }
        }
    }

    file_put_contents(
        __DIR__ . '/CORRECTIONS_REQUISES.json',
        json_encode($corrections, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
    );

    echo "✅ Fichier créé: CORRECTIONS_REQUISES.json\n\n";

} else {
    echo "✅ ✅ ✅ PARFAIT! ✅ ✅ ✅\n";
    echo "Aucun terme anglais trouvé!\n";
    echo "Toutes les langues sont correctement traduites!\n\n";
}

echo "=== AUDIT TERMINÉ ===\n";
