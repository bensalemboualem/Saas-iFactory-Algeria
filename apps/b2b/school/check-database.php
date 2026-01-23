<?php
try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    
    echo "=== Tables liées aux traductions ===" . PHP_EOL;
    $tables = $pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN);
    foreach($tables as $table) {
        if(strpos($table, 'translation') !== false || strpos($table, 'lang') !== false || strpos($table, 'section') !== false) {
            echo "- " . $table . PHP_EOL;
        }
    }
    
    echo PHP_EOL . "=== Structure de la table sections ===" . PHP_EOL;
    $columns = $pdo->query('DESCRIBE sections')->fetchAll();
    foreach($columns as $col) {
        echo $col['Field'] . ' (' . $col['Type'] . ')' . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Contenu actuel des sections ===" . PHP_EOL;
    $sections = $pdo->query('SELECT * FROM sections LIMIT 5')->fetchAll();
    foreach($sections as $section) {
        echo "ID: " . $section['id'] . " - Title: " . $section['title'] . " - Content: " . substr($section['details'], 0, 50) . "..." . PHP_EOL;
    }
    
    echo PHP_EOL . "=== Tables de langues ===" . PHP_EOL;
    $languages = $pdo->query('SELECT * FROM languages')->fetchAll();
    foreach($languages as $lang) {
        echo "ID: " . $lang['id'] . " - Name: " . $lang['name'] . " - Code: " . $lang['code'] . PHP_EOL;
    }
    
} catch(Exception $e) {
    echo "Erreur: " . $e->getMessage() . PHP_EOL;
}
?>