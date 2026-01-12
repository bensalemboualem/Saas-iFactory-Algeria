<?php
try {
    $pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
    echo "Tables de traductions:" . PHP_EOL;
    $tables = $pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN);
    foreach($tables as $table) {
        if(strpos($table, 'translat') !== false || strpos($table, 'lang') !== false) {
            echo "- " . $table . PHP_EOL;
        }
    }
} catch(Exception $e) {
    echo "Erreur: " . $e->getMessage() . PHP_EOL;
}
?>