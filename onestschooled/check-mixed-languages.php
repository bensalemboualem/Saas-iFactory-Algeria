<?php
try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    
    echo "=== Contenu réel de section_translates ===" . PHP_EOL;
    $translates = $pdo->query('SELECT * FROM section_translates ORDER BY section_id, locale')->fetchAll();
    foreach($translates as $trans) {
        echo "ID: " . $trans['id'] . " - Section: " . $trans['section_id'] . " - Locale: " . $trans['locale'] . " - Name: " . substr($trans['name'], 0, 30) . "..." . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Contenu réel de page_sections ===" . PHP_EOL;
    $page_sections = $pdo->query('SELECT * FROM page_sections')->fetchAll();
    foreach($page_sections as $ps) {
        echo "ID: " . $ps['id'] . " - Key: " . $ps['key'] . " - Name: " . substr($ps['name'], 0, 30) . "..." . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Vérification mélange de langues ===" . PHP_EOL;
    // Vérifier s'il y a des problèmes de traductions mélangées
    $mixed_content = $pdo->query("
        SELECT st.section_id, st.locale, st.name, st.description
        FROM section_translates st
        WHERE st.locale = 'fr' AND (st.name LIKE '%English%' OR st.name LIKE '%arabic%')
        OR st.locale = 'ar' AND (st.name LIKE '%French%' OR st.name LIKE '%english%')
        OR st.locale = 'en' AND (st.name LIKE '%français%' OR st.name LIKE '%عربي%')
    ")->fetchAll();
    
    if(empty($mixed_content)) {
        echo "Aucun mélange de langue détecté dans section_translates." . PHP_EOL;
    } else {
        echo "Mélange de langues détecté:" . PHP_EOL;
        foreach($mixed_content as $mc) {
            echo "Section " . $mc['section_id'] . " - Locale: " . $mc['locale'] . " - Name: " . $mc['name'] . PHP_EOL;
        }
    }
    
} catch(Exception $e) {
    echo "Erreur: " . $e->getMessage() . PHP_EOL;
}
?>