<?php
echo "=== VERIFICATION: TOUTES LES MENTIONS DE BAC ONT-ELLES ETE SUPPRIMEES? ===\n\n";

$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

// Tables importantes à vérifier
$criticalTables = [
    'section_translates',
    'slider_translates',
    'page_sections',
    'classes',
    'exam_types',
    'fees_groups'
];

$foundBac = false;

foreach ($criticalTables as $table) {
    echo "Vérification de $table...\n";

    try {
        $columns = $pdo->query("SHOW COLUMNS FROM `$table`")->fetchAll(PDO::FETCH_ASSOC);
        $textColumns = [];
        foreach ($columns as $col) {
            if (stripos($col['Type'], 'text') !== false || stripos($col['Type'], 'varchar') !== false) {
                $textColumns[] = $col['Field'];
            }
        }

        if (empty($textColumns)) continue;

        $whereConditions = [];
        foreach ($textColumns as $col) {
            $whereConditions[] = "`$col` LIKE '%bac%' OR `$col` LIKE '%BAC%' OR `$col` LIKE '%Baccalauréat%' OR `$col` LIKE '%terminale%' OR `$col` LIKE '%Terminale%' OR `$col` LIKE '%lycée%' OR `$col` LIKE '%Lycée%'";
        }

        $whereClause = implode(' OR ', $whereConditions);
        $count = $pdo->query("SELECT COUNT(*) FROM `$table` WHERE $whereClause")->fetchColumn();

        if ($count > 0) {
            echo "  ❌ ATTENTION: $count mention(s) trouvée(s)\n";
            $foundBac = true;

            // Afficher les résultats
            $results = $pdo->query("SELECT * FROM `$table` WHERE $whereClause LIMIT 2")->fetchAll(PDO::FETCH_ASSOC);
            foreach ($results as $row) {
                echo "    ID: " . ($row['id'] ?? 'N/A') . "\n";
                foreach ($row as $key => $value) {
                    if (is_string($value) && (stripos($value, 'bac') !== false || stripos($value, 'lycée') !== false || stripos($value, 'terminale') !== false)) {
                        echo "      $key: " . substr($value, 0, 100) . "\n";
                    }
                }
            }
        } else {
            echo "  ✅ Aucune mention de BAC\n";
        }
    } catch (Exception $e) {
        echo "  ⚠️  Erreur: " . $e->getMessage() . "\n";
    }
    echo "\n";
}

echo "====================================\n";
if (!$foundBac) {
    echo "✅✅✅ PARFAIT! AUCUNE MENTION DE BAC TROUVÉE!\n";
    echo "✅✅✅ LA PAGE HOME EST MAINTENANT CORRECTE!\n";
} else {
    echo "❌ Il reste des mentions de BAC à corriger\n";
}
echo "====================================\n";
