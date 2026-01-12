<?php
try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    
    echo "=== Structure de section_translates ===" . PHP_EOL;
    $columns = $pdo->query('DESCRIBE section_translates')->fetchAll();
    foreach($columns as $col) {
        echo $col['Field'] . ' (' . $col['Type'] . ')' . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Contenu de section_translates ===" . PHP_EOL;
    $translates = $pdo->query('SELECT * FROM section_translates')->fetchAll();
    foreach($translates as $trans) {
        echo "ID: " . $trans['id'] . " - Section: " . $trans['section_id'] . " - Lang: " . $trans['language_id'] . " - Title: " . substr($trans['title'], 0, 30) . "..." . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Structure de page_sections ===" . PHP_EOL;
    $columns = $pdo->query('DESCRIBE page_sections')->fetchAll();
    foreach($columns as $col) {
        echo $col['Field'] . ' (' . $col['Type'] . ')' . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Contenu de page_sections ===" . PHP_EOL;
    $page_sections = $pdo->query('SELECT * FROM page_sections LIMIT 10')->fetchAll();
    foreach($page_sections as $ps) {
        echo "ID: " . $ps['id'] . " - Page: " . $ps['page_name'] . " - Section: " . $ps['section_name'] . " - Content: " . substr($ps['content'], 0, 50) . "..." . PHP_EOL;
    }
    
} catch(Exception $e) {
    echo "Erreur: " . $e->getMessage() . PHP_EOL;
}
?>