<?php
$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

echo "=== FIX FINAL - COMPTEURS 804 ===\n\n";

// 1. Vérifier counter_translates
echo "1. CONTENU DE counter_translates\n";
$result = $pdo->query("SELECT * FROM counter_translates");
$translates = $result->fetchAll(PDO::FETCH_ASSOC);

foreach ($translates as $trans) {
    echo "   ID: {$trans['id']}, Counter ID: {$trans['counter_id']}\n";
    echo "      Name: {$trans['name']}\n";
    echo "      Total: {$trans['total_count']}\n";

    if ($trans['total_count'] == 804 || strpos($trans['name'], '804') !== false) {
        echo "      ⚠️  PROBLÈME TROUVÉ ICI!\n";
    }
    echo "\n";
}

// 2. Vraies données
$students = $pdo->query("SELECT COUNT(*) as c FROM session_class_students WHERE session_id = (SELECT value FROM settings WHERE name = 'session')")->fetch()['c'];
$parents = $pdo->query("SELECT COUNT(*) as c FROM parent_guardians")->fetch()['c'];
$teachers = $pdo->query("SELECT COUNT(*) as c FROM staff WHERE role_id = 5")->fetch()['c'];
$sessions = $pdo->query("SELECT COUNT(*) as c FROM sessions")->fetch()['c'];

echo "2. VRAIES DONNÉES\n";
echo "   Étudiants: {$students}\n";
echo "   Parents: {$parents}\n";
echo "   Enseignants: {$teachers}\n";
echo "   Sessions: {$sessions}\n\n";

// 3. CORRECTION - Mettre à jour avec les vraies données
echo "3. CORRECTION EN COURS\n";

// Mise à jour de tous les compteurs
$pdo->exec("UPDATE counters SET total_count = {$students} WHERE name LIKE '%student%' OR name LIKE '%étudiant%'");
echo "   ✅ Compteur Students mis à jour: {$students}\n";

$pdo->exec("UPDATE counters SET total_count = {$parents} WHERE name LIKE '%parent%'");
echo "   ✅ Compteur Parents mis à jour: {$parents}\n";

$pdo->exec("UPDATE counters SET total_count = {$teachers} WHERE name LIKE '%teacher%' OR name LIKE '%enseignant%'");
echo "   ✅ Compteur Teachers mis à jour: {$teachers}\n";

$pdo->exec("UPDATE counters SET total_count = {$sessions} WHERE name LIKE '%user%' OR name LIKE '%class%'");
echo "   ✅ Compteur Classes/Users mis à jour: {$sessions}\n";

// Mise à jour des traductions
$pdo->exec("UPDATE counter_translates SET total_count = {$students} WHERE name LIKE '%student%' OR name LIKE '%étudiant%'");
echo "   ✅ Traductions Students mises à jour\n";

$pdo->exec("UPDATE counter_translates SET total_count = {$parents} WHERE name LIKE '%parent%'");
echo "   ✅ Traductions Parents mises à jour\n";

$pdo->exec("UPDATE counter_translates SET total_count = {$teachers} WHERE name LIKE '%teacher%' OR name LIKE '%enseignant%' OR name LIKE '%expert%'");
echo "   ✅ Traductions Teachers mises à jour\n";

$pdo->exec("UPDATE counter_translates SET total_count = {$sessions} WHERE name LIKE '%user%' OR name LIKE '%class%'");
echo "   ✅ Traductions Classes mises à jour\n\n";

// 4. Supprimer les lignes vides (ID 6, 7, 8)
echo "4. NETTOYAGE DES LIGNES VIDES\n";
$pdo->exec("DELETE FROM counters WHERE name IS NULL OR name = ''");
echo "   ✅ Lignes vides supprimées\n\n";

// 5. Vérification finale
echo "5. VÉRIFICATION FINALE\n";
echo "TABLE counters:\n";
$result = $pdo->query("SELECT id, name, total_count FROM counters ORDER BY serial");
foreach ($result as $row) {
    echo "   {$row['name']}: {$row['total_count']}\n";
}

echo "\nTABLE counter_translates:\n";
$result = $pdo->query("SELECT id, name, total_count FROM counter_translates");
foreach ($result as $row) {
    echo "   {$row['name']}: {$row['total_count']}\n";
}

echo "\n=== CORRECTION TERMINÉE ===\n\n";
echo "ACTIONS:\n";
echo "1. Rechargez: http://localhost/onestschooled-test/public/home\n";
echo "2. Ctrl+Shift+R (hard refresh)\n";
echo "3. Les compteurs doivent afficher les bonnes valeurs\n";
