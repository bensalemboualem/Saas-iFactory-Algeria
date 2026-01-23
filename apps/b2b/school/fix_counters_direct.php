<?php
$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

echo "=== CORRECTION DIRECTE DES COMPTEURS ===\n\n";

// 1. Voir la structure de la table counters
echo "1. STRUCTURE TABLE COUNTERS\n";
$result = $pdo->query("DESCRIBE counters");
foreach ($result as $row) {
    echo "   {$row['Field']} ({$row['Type']})\n";
}
echo "\n";

// 2. Voir le contenu
echo "2. CONTENU ACTUEL\n";
$result = $pdo->query("SELECT * FROM counters");
$counters = $result->fetchAll(PDO::FETCH_ASSOC);

foreach ($counters as $counter) {
    echo "   ID: {$counter['id']}\n";
    foreach ($counter as $key => $value) {
        if ($key != 'id') {
            echo "      {$key}: {$value}\n";
        }
    }
    echo "\n";
}

// 3. Chercher où est stocké "804"
echo "3. RECHERCHE DE '804'\n";
foreach ($counters as $counter) {
    foreach ($counter as $key => $value) {
        if ($value == 804 || strpos($value, '804') !== false) {
            echo "   ⚠️  TROUVÉ! ID: {$counter['id']}, Colonne: {$key}, Valeur: {$value}\n";
        }
    }
}
echo "\n";

// 4. Compter les vraies données
echo "4. VRAIES DONNÉES\n";
$students = $pdo->query("SELECT COUNT(*) as c FROM session_class_students WHERE session_id = (SELECT value FROM settings WHERE name = 'session')")->fetch()['c'];
$parents = $pdo->query("SELECT COUNT(*) as c FROM parent_guardians")->fetch()['c'];
$teachers = $pdo->query("SELECT COUNT(*) as c FROM staff WHERE role_id = 5")->fetch()['c'];
$sessions = $pdo->query("SELECT COUNT(*) as c FROM sessions")->fetch()['c'];

echo "   Étudiants: {$students}\n";
echo "   Parents: {$parents}\n";
echo "   Enseignants: {$teachers}\n";
echo "   Sessions: {$sessions}\n\n";

// 5. Chercher les tables de traduction
echo "5. TABLES DE TRADUCTION DISPONIBLES\n";
$result = $pdo->query("SHOW TABLES LIKE '%counter%'");
foreach ($result as $row) {
    $table = array_values($row)[0];
    echo "   - {$table}\n";
}
echo "\n";

// 6. Vérifier si c'est dans une colonne JSON 'data'
echo "6. VÉRIFICATION COLONNE DATA/JSON\n";
foreach ($counters as $counter) {
    if (isset($counter['data'])) {
        echo "   ID {$counter['id']}: data = {$counter['data']}\n";

        $data = json_decode($counter['data'], true);
        if ($data) {
            print_r($data);
        }
    }
}

echo "\n=== FIN DIAGNOSTIC ===\n";
