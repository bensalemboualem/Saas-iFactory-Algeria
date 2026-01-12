<?php
/**
 * VÉRIFICATION FINALE - DASHBOARD 100% ARABE
 */

require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make('Illuminate\Contracts\Console\Kernel');
$kernel->bootstrap();

echo "=== VÉRIFICATION FINALE - DASHBOARD 100% ARABE ===\n\n";

$allGood = true;

// 1. Vérifier les paramètres de base de données
echo "1. PARAMÈTRES BASE DE DONNÉES:\n";
$params = DB::table('settings')->whereIn('name', ['language', 'default-language', 'rtl'])->get();
foreach ($params as $param) {
    $expected = [
        'language' => 'ar',
        'default-language' => 'ar',
        'rtl' => '1'
    ];

    if (isset($expected[$param->name])) {
        $isCorrect = $param->value === $expected[$param->name];
        $status = $isCorrect ? "✅" : "❌";
        echo "   $status {$param->name} = {$param->value}";

        if (!$isCorrect) {
            echo " (attendu: {$expected[$param->name]})";
            $allGood = false;
        }
        echo "\n";
    }
}

// 2. Vérifier la configuration Laravel
echo "\n2. CONFIGURATION LARAVEL:\n";
$locale = config('app.locale');
$fallback = config('app.fallback_locale');

$status = $locale === 'ar' ? "✅" : "❌";
echo "   $status app.locale = $locale";
if ($locale !== 'ar') {
    echo " (attendu: ar)";
    $allGood = false;
}
echo "\n";

$status = $fallback === 'ar' ? "✅" : "❌";
echo "   $status app.fallback_locale = $fallback";
if ($fallback !== 'ar') {
    echo " (attendu: ar)";
    $allGood = false;
}
echo "\n";

// 3. Vérifier le fichier .env
echo "\n3. FICHIER .ENV:\n";
$envContent = file_get_contents(__DIR__ . '/.env');
$hasRtl = preg_match("/APP_DIR\s*=\s*rtl/", $envContent);

$status = $hasRtl ? "✅" : "❌";
echo "   $status APP_DIR = rtl";
if (!$hasRtl) {
    echo " (non trouvé ou incorrect)";
    $allGood = false;
}
echo "\n";

// 4. Vérifier la fonction ___() fallback
echo "\n4. FONCTION ___() HELPER:\n";
$helperContent = file_get_contents(__DIR__ . '/app/Helpers/common-helpers.php');
$hasArFallback = preg_match("/Session::get\('locale'\)\s*\?:\s*'ar'/", $helperContent);

$status = $hasArFallback ? "✅" : "❌";
echo "   $status Fallback = 'ar'";
if (!$hasArFallback) {
    echo " (toujours sur 'bn' ou autre)";
    $allGood = false;
}
echo "\n";

// 5. Vérifier les fichiers JSON de traduction
echo "\n5. FICHIERS JSON DE TRADUCTION:\n";

$jsonTests = [
    'dashboard.json' => 'Student',
    'academic.json' => 'teacher',
    'settings.json' => 'Session',
];

foreach ($jsonTests as $file => $key) {
    $path = __DIR__ . '/lang/ar/' . $file;
    if (file_exists($path)) {
        $content = file_get_contents($path);
        $json = json_decode($content, true);

        if (isset($json[$key])) {
            $value = $json[$key];
            $hasArabic = preg_match('/[\x{0600}-\x{06FF}]/u', $value);

            $status = $hasArabic ? "✅" : "❌";
            echo "   $status $file → \"$key\" = \"$value\"";

            if (!$hasArabic) {
                echo " (devrait être en arabe!)";
                $allGood = false;
            }
            echo "\n";
        } else {
            echo "   ⚠️  $file → clé \"$key\" non trouvée\n";
        }
    } else {
        echo "   ❌ $file n'existe pas\n";
        $allGood = false;
    }
}

// 6. Test des traductions avec la fonction ___()
echo "\n6. TEST DES TRADUCTIONS ___():\n";
Session::put('locale', 'ar');

$translationTests = [
    'dashboard.Student',
    'dashboard.Parent',
    'academic.teacher',
    'settings.Session',
];

foreach ($translationTests as $key) {
    $result = ___($key);
    $hasArabic = preg_match('/[\x{0600}-\x{06FF}]/u', $result);

    $status = $hasArabic ? "✅" : "❌";
    echo "   $status ___('$key') = \"$result\"";

    if (!$hasArabic) {
        echo " (devrait être en arabe!)";
        $allGood = false;
    }
    echo "\n";
}

// 7. Vérifier les caches
echo "\n7. ÉTAT DES CACHES:\n";
$viewCacheDir = __DIR__ . '/storage/framework/views';
$configCacheDir = __DIR__ . '/bootstrap/cache';

$viewFiles = glob($viewCacheDir . '/*.php');
$configFiles = glob($configCacheDir . '/*.php');

echo "   Cache des vues: " . count($viewFiles) . " fichier(s)\n";
echo "   Cache de config: " . count($configFiles) . " fichier(s)\n";

if (count($viewFiles) > 0 || count($configFiles) > 0) {
    echo "   ⚠️  RECOMMANDATION: Nettoyer les caches avant de tester\n";
}

// RÉSULTAT FINAL
echo "\n" . str_repeat("=", 70) . "\n\n";

if ($allGood) {
    echo "✅ ✅ ✅ TOUT EST PARFAIT! ✅ ✅ ✅\n\n";
    echo "Le dashboard devrait être 100% en arabe.\n\n";
    echo "PROCHAINES ÉTAPES:\n";
    echo "1. Nettoyez les caches si nécessaire:\n";
    echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";
    echo "2. Déconnectez-vous du dashboard\n";
    echo "3. Reconnectez-vous\n";
    echo "4. Appuyez sur Ctrl+Shift+R pour forcer le rechargement\n\n";
    echo "Vous devriez voir:\n";
    echo "   - الطالب (Student)\n";
    echo "   - ولي الأمر (Parent)\n";
    echo "   - المعلم (Teacher)\n";
    echo "   - الدورة (Session)\n\n";
} else {
    echo "❌ ATTENTION: Des problèmes ont été détectés!\n\n";
    echo "Relancez les scripts de correction:\n";
    echo "   \"C:/xampp/php/php.exe\" set_default_language.php\n";
    echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";
}

echo str_repeat("=", 70) . "\n";
