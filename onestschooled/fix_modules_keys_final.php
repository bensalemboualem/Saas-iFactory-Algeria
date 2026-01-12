<?php
/**
 * CORRECTION FINALE DES CLÉS DE MODULES
 * Ajoute les traductions manquantes dans settings.json et setting.json
 */

echo "\n========================================\n";
echo "CORRECTION CLÉS MODULES\n";
echo "========================================\n\n";

$corrections = [
    // ARABE
    'ar/settings.json' => [
        'Forums' => 'المنتديات',
        'forums' => 'المنتديات',
        'Memories' => 'الذكريات',
        'memories' => 'الذكريات',
        'Live Chat' => 'الدردشة المباشرة',
        'live_chat' => 'الدردشة المباشرة',
        'LiveChat' => 'الدردشة المباشرة',
        'Messaging' => 'المراسلة',
        'All Conversations' => 'جميع المحادثات',
    ],

    'ar/setting.json' => [
        'Forums' => 'المنتديات',
        'My Forums' => 'منتدياتي',
        'Forum Feeds' => 'تغذية المنتدى',
        'Memories' => 'الذكريات',
        'My Memories' => 'ذكرياتي',
    ],

    // FRANÇAIS
    'fr/settings.json' => [
        'Forums' => 'Forums',
        'forums' => 'Forums',
        'Memories' => 'Souvenirs',
        'memories' => 'Souvenirs',
        'Live Chat' => 'Chat en direct',
        'live_chat' => 'Chat en direct',
        'LiveChat' => 'Chat en direct',
        'Messaging' => 'Messagerie',
        'All Conversations' => 'Toutes les conversations',
    ],

    'fr/setting.json' => [
        'Forums' => 'Forums',
        'My Forums' => 'Mes forums',
        'Forum Feeds' => 'Flux du forum',
        'Memories' => 'Souvenirs',
        'My Memories' => 'Mes souvenirs',
    ],
];

$totalCorrections = 0;

foreach ($corrections as $filePath => $translations) {
    $fullPath = __DIR__ . '/lang/' . $filePath;

    echo "📝 Fichier: $filePath\n";

    if (!file_exists($fullPath)) {
        echo "⚠️  Fichier non trouvé, création...\n";
        $dir = dirname($fullPath);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        file_put_contents($fullPath, json_encode([], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    }

    $content = file_get_contents($fullPath);
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
        file_put_contents($fullPath, $json);
        echo "✅ $corrected correction(s)\n\n";
        $totalCorrections += $corrected;
    } else {
        echo "✅ Déjà à jour\n\n";
    }
}

echo "========================================\n";
echo "📊 TOTAL: $totalCorrections corrections\n";
echo "========================================\n\n";

echo "✅ TERMINÉ!\n";
echo "⚠️  DERNIÈRE ÉTAPE:\n";
echo "   1. Nettoyez les caches:\n";
echo '      "C:/xampp/php/php.exe" artisan cache:clear' . "\n";
echo '      "C:/xampp/php/php.exe" artisan config:clear' . "\n";
echo '      "C:/xampp/php/php.exe" artisan view:clear' . "\n";
echo "   2. DÉCONNECTEZ-VOUS du dashboard\n";
echo "   3. RECONNECTEZ-VOUS\n";
echo "   4. Appuyez sur Ctrl+Shift+R\n\n";
