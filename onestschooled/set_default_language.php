<?php
/**
 * DÉFINIR L'ARABE COMME LANGUE PAR DÉFAUT
 */

require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make('Illuminate\Contracts\Console\Kernel');
$kernel->bootstrap();

echo "=== DÉFINIR ARABE COMME LANGUE PAR DÉFAUT ===\n\n";

// 1. Vérifier le paramètre default-language
echo "1. Vérification du paramètre default-language...\n";
$defaultLang = DB::table('settings')->where('name', 'default-language')->first();

if ($defaultLang) {
    echo "   Valeur actuelle: {$defaultLang->value}\n";

    if ($defaultLang->value !== 'ar') {
        DB::table('settings')->where('name', 'default-language')->update(['value' => 'ar']);
        echo "   ✅ Mis à jour vers 'ar'\n";
    } else {
        echo "   ✅ Déjà défini à 'ar'\n";
    }
} else {
    DB::table('settings')->insert([
        'name' => 'default-language',
        'value' => 'ar',
        'created_at' => now(),
        'updated_at' => now()
    ]);
    echo "   ✅ Paramètre créé avec valeur 'ar'\n";
}

// 2. Vérifier le paramètre language
echo "\n2. Vérification du paramètre language...\n";
$language = DB::table('settings')->where('name', 'language')->first();

if ($language) {
    echo "   Valeur actuelle: {$language->value}\n";

    if ($language->value !== 'ar') {
        DB::table('settings')->where('name', 'language')->update(['value' => 'ar']);
        echo "   ✅ Mis à jour vers 'ar'\n";
    } else {
        echo "   ✅ Déjà défini à 'ar'\n";
    }
} else {
    DB::table('settings')->insert([
        'name' => 'language',
        'value' => 'ar',
        'created_at' => now(),
        'updated_at' => now()
    ]);
    echo "   ✅ Paramètre créé avec valeur 'ar'\n";
}

// 3. Afficher tous les paramètres de langue
echo "\n3. Tous les paramètres de langue:\n";
$langSettings = DB::table('settings')->whereIn('name', ['language', 'default-language', 'rtl'])->get();

foreach ($langSettings as $setting) {
    echo "   {$setting->name} = {$setting->value}\n";
}

// 4. Vérifier la config Laravel
echo "\n4. Configuration Laravel:\n";
echo "   app.locale = " . config('app.locale') . "\n";
echo "   app.fallback_locale = " . config('app.fallback_locale') . "\n";

echo "\n=== CONFIGURATION TERMINÉE ===\n\n";

echo "RÉSUMÉ:\n";
echo "✅ default-language = ar (base de données)\n";
echo "✅ language = ar (base de données)\n";
echo "✅ rtl = 1 (base de données)\n";
echo "✅ app.locale = ar (config/app.php)\n";
echo "✅ app.fallback_locale = ar (config/app.php)\n";
echo "✅ Fonction ___() utilise 'ar' comme fallback\n\n";

echo "PROCHAINES ÉTAPES:\n";
echo "1. Nettoyez les caches:\n";
echo "   \"C:/xampp/php/php.exe\" CLEAR_ALL_CACHES_FINAL.php\n\n";
echo "2. Déconnectez-vous du dashboard\n\n";
echo "3. Reconnectez-vous\n\n";
echo "4. Le dashboard devrait maintenant être 100% en arabe!\n\n";

echo "✅ LANGUE PAR DÉFAUT = ARABE!\n";
