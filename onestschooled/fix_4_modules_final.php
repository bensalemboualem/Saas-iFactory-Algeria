<?php
/**
 * CORRECTION FINALE - 4 MODULES
 * التواصل + إدارة الموظفين + المنتديات + الذكريات
 * Communication + Gestion du personnel + Forums + Souvenirs
 */

echo "\n========================================\n";
echo "CORRECTION 4 MODULES - AR + FR\n";
echo "========================================\n\n";

$langPathAr = __DIR__ . '/lang/ar';
$langPathFr = __DIR__ . '/lang/fr';

// ========================================
// ARABE - Corrections
// ========================================
$arabicCorrections = [
    'common.json' => [
        'Communication' => 'التواصل',
        'communication' => 'التواصل',
        'Staff' => 'الموظفون',
        'staff' => 'الموظفون',
        'Staff Management' => 'إدارة الموظفين',
        'Forums' => 'المنتديات',
        'forums' => 'المنتديات',
        'Memories' => 'الذكريات',
        'memories' => 'الذكريات',
        'Memory' => 'الذاكرة',
        'memory' => 'الذاكرة',
    ],

    'staff.json' => [
        'Staff' => 'الموظفون',
        'staff' => 'الموظفون',
        'Staff Management' => 'إدارة الموظفين',
        'Staff List' => 'قائمة الموظفين',
        'staff_list' => 'قائمة الموظفين',
        'Staff Details' => 'تفاصيل الموظف',
        'staff_details' => 'تفاصيل الموظف',
        'Add Staff' => 'إضافة موظف',
        'add_staff' => 'إضافة موظف',
        'Edit Staff' => 'تعديل الموظف',
        'edit_staff' => 'تعديل الموظف',
        'Update Staff' => 'تحديث الموظف',
        'update_staff' => 'تحديث الموظف',
    ],

    'settings.json' => [
        'Communication' => 'التواصل',
        'communication' => 'التواصل',
        'Staff' => 'الموظفون',
        'staff' => 'الموظفون',
        'Staff Management' => 'إدارة الموظفين',
    ],
];

// ========================================
// FRANÇAIS - Corrections
// ========================================
$frenchCorrections = [
    'common.json' => [
        'Communication' => 'Communication',
        'communication' => 'Communication',
        'Staff' => 'Personnel',
        'staff' => 'Personnel',
        'Staff Management' => 'Gestion du personnel',
        'Forums' => 'Forums',
        'forums' => 'Forums',
        'Memories' => 'Souvenirs',
        'memories' => 'Souvenirs',
        'Memory' => 'Souvenir',
        'memory' => 'Souvenir',
    ],

    'staff.json' => [
        'Staff' => 'Personnel',
        'staff' => 'Personnel',
        'Staff Management' => 'Gestion du personnel',
        'Staff List' => 'Liste du personnel',
        'staff_list' => 'Liste du personnel',
        'Staff Details' => 'Détails du personnel',
        'staff_details' => 'Détails du personnel',
        'Add Staff' => 'Ajouter personnel',
        'add_staff' => 'Ajouter personnel',
        'Edit Staff' => 'Modifier personnel',
        'edit_staff' => 'Modifier personnel',
        'Update Staff' => 'Mettre à jour personnel',
        'update_staff' => 'Mettre à jour personnel',
    ],

    'memory.json' => [
        'Memory List' => 'Liste des souvenirs',
        'memory_list' => 'Liste des souvenirs',
        'Memories' => 'Souvenirs',
        'memories' => 'Souvenirs',
        'Add Memory' => 'Ajouter souvenir',
        'add_memory' => 'Ajouter souvenir',
        'Edit Memory' => 'Modifier souvenir',
        'edit_memory' => 'Modifier souvenir',
    ],

    'settings.json' => [
        'Communication' => 'Communication',
        'communication' => 'Communication',
        'Staff' => 'Personnel',
        'staff' => 'Personnel',
        'Staff Management' => 'Gestion du personnel',
        'Forums' => 'Forums',
        'forums' => 'Forums',
    ],
];

// ========================================
// FONCTION DE CORRECTION
// ========================================
function applyCorrections($langPath, $corrections, $language) {
    $totalCorrections = 0;

    echo "\n🌍 CORRECTION $language\n";
    echo "==========================\n\n";

    foreach ($corrections as $fileName => $translations) {
        $filePath = $langPath . '/' . $fileName;

        echo "📝 Fichier: $fileName\n";

        if (!file_exists($filePath)) {
            echo "⚠️  Fichier non trouvé, création...\n";
            file_put_contents($filePath, json_encode([], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        }

        $content = file_get_contents($filePath);
        $data = json_decode($content, true);

        if ($data === null) {
            echo "❌ Erreur de décodage JSON\n\n";
            continue;
        }

        $corrected = 0;

        foreach ($translations as $key => $value) {
            if (!isset($data[$key]) || $data[$key] === $key || empty($data[$key]) || $data[$key] !== $value) {
                $data[$key] = $value;
                echo "  ✓ '$key' → '$value'\n";
                $corrected++;
            }
        }

        if ($corrected > 0) {
            $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
            file_put_contents($filePath, $json);
            echo "✅ $corrected correction(s)\n\n";
            $totalCorrections += $corrected;
        } else {
            echo "✅ Déjà à jour\n\n";
        }
    }

    return $totalCorrections;
}

// ========================================
// EXÉCUTION
// ========================================
$totalAr = applyCorrections($langPathAr, $arabicCorrections, 'ARABE 🇩🇿');
$totalFr = applyCorrections($langPathFr, $frenchCorrections, 'FRANÇAIS 🇫🇷');

echo "\n========================================\n";
echo "📊 RÉSUMÉ CORRECTIONS\n";
echo "========================================\n";
echo "🇩🇿 Arabe: $totalAr corrections\n";
echo "🇫🇷 Français: $totalFr corrections\n";
echo "📊 TOTAL: " . ($totalAr + $totalFr) . " corrections\n";
echo "========================================\n\n";

echo "✅ TERMINÉ!\n";
echo "⚠️  Nettoyez les caches et déconnectez-vous/reconnectez-vous:\n";
echo '   "C:/xampp/php/php.exe" artisan cache:clear' . "\n";
echo '   "C:/xampp/php/php.exe" artisan config:clear' . "\n";
echo '   "C:/xampp/php/php.exe" artisan view:clear' . "\n\n";
