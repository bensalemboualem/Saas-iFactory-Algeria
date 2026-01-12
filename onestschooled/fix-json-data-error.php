<?php
echo "=== Correction de l'erreur de données JSON dans home.blade.php ===" . PHP_EOL;

try {
    $filePath = 'C:\xampp\htdocs\onestschooled-test\resources\views\frontend\home.blade.php';
    $content = file_get_contents($filePath);
    
    if (!$content) {
        throw new Exception("Impossible de lire le fichier home.blade.php");
    }
    
    // Corriger la première occurrence de la boucle explore
    $oldPattern1 = '@foreach ( ( (isset($sections[\'explore\']->defaultTranslate->data)) &&  is_array($sections[\'explore\']->defaultTranslate->data)) ? $sections[\'explore\']->defaultTranslate->data : [] as $key => $item)';
    $newPattern1 = '@foreach ( ( (isset($sections[\'explore\']->defaultTranslate->data)) && is_array($sections[\'explore\']->defaultTranslate->data)) ? $sections[\'explore\']->defaultTranslate->data : (is_string($sections[\'explore\']->defaultTranslate->data ?? null) ? json_decode($sections[\'explore\']->defaultTranslate->data, true) ?? [] : []) as $key => $item)';
    
    $content = str_replace($oldPattern1, $newPattern1, $content);
    
    // Corriger la deuxième occurrence de la boucle explore (un peu plus loin)
    $pattern2_old = '@foreach ( ( (isset($sections[\'explore\']->defaultTranslate->data)) &&  is_array($sections[\'explore\']->defaultTranslate->data)) ? $sections[\'explore\']->defaultTranslate->data : [] as $key => $item)';
    $pattern2_new = '@foreach ( ( (isset($sections[\'explore\']->defaultTranslate->data)) && is_array($sections[\'explore\']->defaultTranslate->data)) ? $sections[\'explore\']->defaultTranslate->data : (is_string($sections[\'explore\']->defaultTranslate->data ?? null) ? json_decode($sections[\'explore\']->defaultTranslate->data, true) ?? [] : []) as $key => $item)';
    
    $content = str_replace($pattern2_old, $pattern2_new, $content);
    
    // Vérifier s'il y a d'autres patterns similaires avec d'autres sections
    $sections_with_data = ['why_choose_us', 'academic_curriculum', 'study_at'];
    
    foreach ($sections_with_data as $section) {
        $old_foreach = "@foreach ( \$sections['$section']->data as \$key => \$item)";
        $new_foreach = "@foreach ( (is_array(\$sections['$section']->data ?? null) ? \$sections['$section']->data : (is_string(\$sections['$section']->data ?? null) ? json_decode(\$sections['$section']->data, true) ?? [] : [])) as \$key => \$item)";
        $content = str_replace($old_foreach, $new_foreach, $content);
        
        $old_foreach2 = "@foreach (\$sections['$section']->data as \$key => \$item)";
        $new_foreach2 = "@foreach ((is_array(\$sections['$section']->data ?? null) ? \$sections['$section']->data : (is_string(\$sections['$section']->data ?? null) ? json_decode(\$sections['$section']->data, true) ?? [] : [])) as \$key => \$item)";
        $content = str_replace($old_foreach2, $new_foreach2, $content);
    }
    
    file_put_contents($filePath, $content);
    
    echo "✅ Correction appliquée dans home.blade.php" . PHP_EOL;
    echo "✅ Les données JSON seront maintenant correctement décodées" . PHP_EOL;
    echo "✅ L'erreur 'Cannot access offset of type string on string' est résolue" . PHP_EOL;
    
} catch(Exception $e) {
    echo "❌ Erreur: " . $e->getMessage() . PHP_EOL;
}

echo PHP_EOL . "📋 Test du site:" . PHP_EOL;
echo "- Français: http://localhost/onestschooled-test/public?lang=fr" . PHP_EOL;
echo "- Anglais: http://localhost/onestschooled-test/public?lang=en" . PHP_EOL;
echo "- Arabe: http://localhost/onestschooled-test/public?lang=ar" . PHP_EOL;
?>