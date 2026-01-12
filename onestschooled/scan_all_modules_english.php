<?php
/**
 * SCAN COMPLET DE TOUS LES MODULES
 * Détecte tous les termes anglais non traduits
 */

echo "\n========================================\n";
echo "SCAN COMPLET DES MODULES\n";
echo "========================================\n\n";

$langPath = __DIR__ . '/lang';

// Liste des fichiers de traduction
$arFiles = glob($langPath . '/ar/*.json');
$frFiles = glob($langPath . '/fr/*.json');

echo "📊 STATISTIQUES:\n";
echo "   Fichiers AR: " . count($arFiles) . "\n";
echo "   Fichiers FR: " . count($frFiles) . "\n\n";

// Patterns de termes anglais courants
$englishPatterns = [
    // Common terms
    '/\b(Add|Edit|Delete|Update|Save|Cancel|Submit|Search|View|Print|Export|Import|Download|Upload|Back|Next|Previous|Close|Select|Action|Actions|Status|Active|Inactive|Yes|No|All|Name|Email|Phone|Address|Date|Time|Description|Details|Type|Category|Amount|Total|Created|Updated|From|To)\b/',

    // Module names
    '/\b(Student|Students|Parent|Parents|Teacher|Teachers|Staff|Department|Designation|Class|Classes|Section|Sections|Subject|Subjects|Exam|Examination|Attendance|Fee|Fees|Library|Book|Books|Report|Reports|Account|Accounts|Communication|Notice|Board|SMS|Mail|Template|Transportation|Driver|Drivers|Vehicle|Vehicles|Route|Routes|Schedule|Enrollment|Forum|Forums|Memory|Memories|Live|Chat|Message|Messaging|Conversation|Conversations)\b/',

    // Actions
    '/\b(Manage|Management|List|Create|Show|Display|Generate|Assign|Collect|Issue|Register|Settings|Setup|Configuration|Information|Contact|Notification|Request|Approval|Approved|Rejected|Pending|Complete|Incomplete)\b/',
];

$allIssues = [];

// Scan tous les fichiers AR
echo "🔍 SCAN ARABE (lang/ar/):\n";
echo "========================================\n\n";

foreach ($arFiles as $file) {
    $fileName = basename($file);
    $content = file_get_contents($file);
    $data = json_decode($content, true);

    if ($data === null) continue;

    $issues = [];

    foreach ($data as $key => $value) {
        // Vérifier si la valeur contient des mots anglais
        foreach ($englishPatterns as $pattern) {
            if (preg_match($pattern, $value, $matches)) {
                $issues[] = [
                    'key' => $key,
                    'value' => $value,
                    'match' => $matches[0]
                ];
            }
        }
    }

    if (!empty($issues)) {
        echo "📝 $fileName: " . count($issues) . " terme(s) anglais\n";

        foreach (array_slice($issues, 0, 5) as $issue) {
            echo "   • '$issue[key]' = '$issue[value]' (contient: $issue[match])\n";
        }

        if (count($issues) > 5) {
            echo "   ... et " . (count($issues) - 5) . " autre(s)\n";
        }
        echo "\n";

        $allIssues[$fileName] = $issues;
    }
}

// Scan tous les fichiers FR
echo "\n🔍 SCAN FRANÇAIS (lang/fr/):\n";
echo "========================================\n\n";

$frIssues = [];

foreach ($frFiles as $file) {
    $fileName = basename($file);
    $content = file_get_contents($file);
    $data = json_decode($content, true);

    if ($data === null) continue;

    $issues = [];

    foreach ($data as $key => $value) {
        // Vérifier si la valeur est identique à la clé (non traduit)
        if ($key === $value) {
            $issues[] = [
                'key' => $key,
                'value' => $value,
                'type' => 'non-traduit'
            ];
        }
    }

    if (!empty($issues)) {
        echo "📝 $fileName: " . count($issues) . " terme(s) non traduit(s)\n";

        foreach (array_slice($issues, 0, 5) as $issue) {
            echo "   • '$issue[key]' = '$issue[value]'\n";
        }

        if (count($issues) > 5) {
            echo "   ... et " . (count($issues) - 5) . " autre(s)\n";
        }
        echo "\n";

        $frIssues[$fileName] = $issues;
    }
}

// Résumé
echo "\n========================================\n";
echo "📊 RÉSUMÉ DU SCAN\n";
echo "========================================\n";
echo "🇩🇿 ARABE: " . count($allIssues) . " fichier(s) avec termes anglais\n";
echo "🇫🇷 FRANÇAIS: " . count($frIssues) . " fichier(s) avec termes non traduits\n";

$totalArIssues = array_sum(array_map('count', $allIssues));
$totalFrIssues = array_sum(array_map('count', $frIssues));

echo "\n📊 TOTAL:\n";
echo "   • Termes anglais en AR: $totalArIssues\n";
echo "   • Termes non traduits en FR: $totalFrIssues\n";
echo "   • TOTAL À CORRIGER: " . ($totalArIssues + $totalFrIssues) . "\n";

echo "\n========================================\n";
echo "✅ SCAN TERMINÉ\n";
echo "========================================\n\n";

// Sauvegarder le rapport
$report = [
    'date' => date('Y-m-d H:i:s'),
    'arabic_issues' => $allIssues,
    'french_issues' => $frIssues,
    'total_ar' => $totalArIssues,
    'total_fr' => $totalFrIssues,
    'total' => $totalArIssues + $totalFrIssues
];

file_put_contents(__DIR__ . '/SCAN_MODULES_REPORT.json', json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo "📄 Rapport sauvegardé: SCAN_MODULES_REPORT.json\n\n";
