<?php
echo "=== CORRECTION FINALE DE PAGE_SECTIONS ===\n\n";

$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

// Récupérer toutes les sections avec BAC
$sections = $pdo->query("SELECT * FROM page_sections WHERE data LIKE '%bac%' OR data LIKE '%BAC%' OR data LIKE '%Baccalauréat%' OR data LIKE '%lycée%' OR data LIKE '%Lycée%' OR data LIKE '%terminale%' OR data LIKE '%Terminale%'")->fetchAll(PDO::FETCH_ASSOC);

if (empty($sections)) {
    echo "✅ Aucune mention de BAC trouvée!\n";
    exit;
}

echo "Trouvé " . count($sections) . " section(s) à corriger:\n\n";

foreach ($sections as $section) {
    echo "Section ID: {$section['id']}\n";
    echo "Avant: " . substr($section['data'], 0, 200) . "...\n";

    $data = $section['data'];

    // Remplacements
    $data = str_ireplace('Baccalauréat', 'BEM', $data);
    $data = str_ireplace(' BAC ', ' BEM ', $data);
    $data = str_ireplace('BAC,', 'BEM,', $data);
    $data = str_ireplace('Lycée', 'Cycle Moyen', $data);
    $data = str_ireplace('lycée', 'cycle moyen', $data);
    $data = str_ireplace('Terminale', '4ème Année Moyenne', $data);
    $data = str_ireplace('terminale', '4ème année moyenne', $data);
    $data = str_ireplace('au BAC', 'au BEM', $data);
    $data = str_ireplace('du BAC', 'du BEM', $data);
    $data = str_ireplace('le BAC', 'le BEM', $data);

    $stmt = $pdo->prepare("UPDATE page_sections SET data = ? WHERE id = ?");
    $stmt->execute([$data, $section['id']]);

    echo "Après: " . substr($data, 0, 200) . "...\n";
    echo "✅ Corrigé!\n\n";
}

echo "=== CORRECTION TERMINÉE ===\n";
