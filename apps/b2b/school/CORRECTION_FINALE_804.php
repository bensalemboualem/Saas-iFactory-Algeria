<?php
$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

echo "=== CORRECTION FINALE 804 ===\n\n";

// Corriger tous les 804
$pdo->exec("UPDATE counter_translates SET total_count = '4' WHERE total_count = '804' OR total_count = '804+'");
echo "✅ 804 corrigé en 4\n";

// Corriger tous les 57
$pdo->exec("UPDATE counter_translates SET total_count = '54' WHERE total_count = '57' OR total_count = '57+'");
echo "✅ 57 corrigé en 54\n";

// Corriger tous les 238
$pdo->exec("UPDATE counter_translates SET total_count = '22' WHERE total_count = '238' OR total_count = '238+'");
echo "✅ 238 corrigé en 22\n";

// Corriger 180 en 304
$pdo->exec("UPDATE counter_translates SET total_count = '304' WHERE total_count = '180'");
echo "✅ 180 corrigé en 304\n\n";

// Vérification finale
echo "RÉSULTAT FINAL:\n";
$result = $pdo->query("SELECT name, total_count FROM counter_translates WHERE counter_id IN (1,2,3,4,5) ORDER BY counter_id, id");
foreach($result as $row) {
    echo "   {$row['name']}: {$row['total_count']}\n";
}

echo "\n✅ TERMINÉ! Rechargez la page maintenant.\n";
