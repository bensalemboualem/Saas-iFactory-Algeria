<?php
echo "=== CORRECTION FINALE DE LA SECTION 6 ===\n\n";

$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');

$section = $pdo->query("SELECT * FROM page_sections WHERE id = 6")->fetch(PDO::FETCH_ASSOC);

if (!$section) {
    echo "❌ Section 6 non trouvée\n";
    exit;
}

echo "Avant:\n";
echo $section['data'] . "\n\n";

$data = json_decode($section['data'], true);

if (is_array($data)) {
    // C'est une liste de programmes - les remplacer complètement
    $newData = [
        "Cycle Moyen - Sciences",
        "Cycle Moyen - Mathématiques",
        "Programme Français Renforcé",
        "Anglais International",
        "Arabe Littéraire",
        "Préparation BEM"
    ];

    $jsonData = json_encode($newData, JSON_UNESCAPED_UNICODE);
} else {
    // Si c'est du texte, remplacer directement
    $jsonData = str_replace('Bac ', '', $section['data']);
    $jsonData = str_replace('BAC', 'BEM', $jsonData);
}

$stmt = $pdo->prepare("UPDATE page_sections SET data = ? WHERE id = 6");
$stmt->execute([$jsonData]);

echo "Après:\n";
echo $jsonData . "\n\n";
echo "✅ Section 6 corrigée!\n";
