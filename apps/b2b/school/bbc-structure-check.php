<?php

/**
 * BBC School Algeria - Script pour vérifier et adapter la structure des tables
 */

require_once __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use Illuminate\Support\Facades\DB;

echo "🔍 VÉRIFICATION STRUCTURE DES TABLES BBC SCHOOL\n";
echo "===============================================\n\n";

$tablesToCheck = ['books', 'fees_masters', 'class_rooms', 'book_categories', 'exam_types'];

foreach ($tablesToCheck as $tableName) {
    echo "📋 Table: $tableName\n";
    echo str_repeat('-', strlen($tableName) + 10) . "\n";
    
    try {
        $columns = DB::getSchemaBuilder()->getColumnListing($tableName);
        echo "Colonnes disponibles: " . implode(', ', $columns) . "\n";
        
        // Montrer quelques exemples de données
        $sample = DB::table($tableName)->limit(3)->get();
        if ($sample->count() > 0) {
            echo "Exemple de données:\n";
            foreach ($sample as $row) {
                $data = (array)$row;
                $displayData = [];
                foreach ($data as $key => $value) {
                    if (strlen($value) > 50) {
                        $value = substr($value, 0, 47) . '...';
                    }
                    $displayData[] = "$key: $value";
                }
                echo "  " . implode(' | ', array_slice($displayData, 0, 3)) . "\n";
            }
        } else {
            echo "Table vide\n";
        }
    } catch (Exception $e) {
        echo "Erreur: " . $e->getMessage() . "\n";
    }
    
    echo "\n";
}

echo "🚗 TENTATIVE D'AJOUT DE VÉHICULES (SI TABLES EXISTENT)\n";
echo "=====================================================\n";

// Vérifier si une table vehicles existe
$allTables = [];
$tables = DB::select('SHOW TABLES');
foreach($tables as $table) {
    $tableName = array_values((array)$table)[0];
    $allTables[] = $tableName;
}

// Chercher des tables liées aux véhicules/transport
$transportTables = array_filter($allTables, function($table) {
    return stripos($table, 'vehicle') !== false || 
           stripos($table, 'transport') !== false || 
           stripos($table, 'driver') !== false ||
           stripos($table, 'route') !== false;
});

if (!empty($transportTables)) {
    echo "Tables transport trouvées: " . implode(', ', $transportTables) . "\n";
    
    // Essayer de créer une table vehicles simple si elle n'existe pas
    if (!in_array('vehicles', $allTables)) {
        try {
            DB::statement("
                CREATE TABLE vehicles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    model VARCHAR(255),
                    registration_number VARCHAR(100) UNIQUE,
                    capacity INT DEFAULT 0,
                    status TINYINT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ");
            echo "✅ Table vehicles créée avec succès!\n";
        } catch (Exception $e) {
            echo "⚠️ Erreur création table vehicles: " . $e->getMessage() . "\n";
        }
    }
} else {
    echo "❌ Aucune table de transport trouvée\n";
    echo "💡 Suggestion: Créer une table vehicles simple\n";
    
    try {
        DB::statement("
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                model VARCHAR(255),
                registration_number VARCHAR(100) UNIQUE,
                capacity INT DEFAULT 0,
                status TINYINT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ");
        echo "✅ Table vehicles créée!\n";
        
        // Ajouter les véhicules BBC School
        $bbcVehicles = [
            ['name' => 'Mercedes Sprinter 24 places', 'model' => 'Mercedes Sprinter 515', 'capacity' => 24, 'registration' => 'BBC-001-DZ'],
            ['name' => 'Mercedes Sprinter 20 places', 'model' => 'Mercedes Sprinter 416', 'capacity' => 20, 'registration' => 'BBC-002-DZ'],
            ['name' => 'Ford Transit 16 places', 'model' => 'Ford Transit 350', 'capacity' => 16, 'registration' => 'BBC-003-DZ'],
            ['name' => 'Iveco Daily 30 places', 'model' => 'Iveco Daily 70C', 'capacity' => 30, 'registration' => 'BBC-004-DZ'],
            ['name' => 'Renault Master 25 places', 'model' => 'Renault Master L3H2', 'capacity' => 25, 'registration' => 'BBC-005-DZ']
        ];
        
        foreach ($bbcVehicles as $vehicle) {
            $exists = DB::table('vehicles')->where('registration_number', $vehicle['registration'])->first();
            if (!$exists) {
                DB::table('vehicles')->insert([
                    'name' => $vehicle['name'],
                    'model' => $vehicle['model'],
                    'capacity' => $vehicle['capacity'],
                    'registration_number' => $vehicle['registration'],
                    'status' => 1,
                    'created_at' => now(),
                    'updated_at' => now(),
                ]);
                echo "✅ Véhicule ajouté: {$vehicle['name']} - {$vehicle['registration']}\n";
            }
        }
        
    } catch (Exception $e) {
        echo "⚠️ Erreur: " . $e->getMessage() . "\n";
    }
}

echo "\n📚 AJOUT DE LIVRES AVEC STRUCTURE ADAPTÉE\n";
echo "=======================================\n";

// Vérifier structure table books
if (in_array('books', $allTables)) {
    $bookColumns = DB::getSchemaBuilder()->getColumnListing('books');
    echo "Colonnes table books: " . implode(', ', $bookColumns) . "\n";
    
    // Livres simples adaptés à la structure existante
    $simpleBooks = [
        ['title' => 'Le Petit Prince', 'author' => 'Antoine de Saint-Exupéry'],
        ['title' => 'Les Misérables', 'author' => 'Victor Hugo'],
        ['title' => 'Mathématiques 3ème', 'author' => 'Collection Phare'],
        ['title' => 'Sciences Physiques', 'author' => 'Durupthy'],
        ['title' => 'Histoire de l\'Algérie', 'author' => 'Benjamin Stora'],
        ['title' => 'نهج البلاغة', 'author' => 'الإمام علي'],
        ['title' => 'ديوان المتنبي', 'author' => 'أبو الطيب المتنبي']
    ];
    
    foreach ($simpleBooks as $book) {
        try {
            $exists = DB::table('books')->where('title', $book['title'])->first();
            if (!$exists) {
                $insertData = [
                    'title' => $book['title'],
                    'status' => 1,
                    'created_at' => now(),
                    'updated_at' => now(),
                ];
                
                // Ajouter les colonnes qui existent
                if (in_array('author', $bookColumns)) {
                    $insertData['author'] = $book['author'];
                }
                if (in_array('book_category_id', $bookColumns)) {
                    $insertData['book_category_id'] = 1; // Première catégorie par défaut
                }
                if (in_array('quantity', $bookColumns)) {
                    $insertData['quantity'] = rand(5, 15);
                }
                if (in_array('available_quantity', $bookColumns)) {
                    $insertData['available_quantity'] = rand(3, 10);
                }
                
                DB::table('books')->insert($insertData);
                echo "✅ Livre ajouté: {$book['title']}\n";
            } else {
                echo "✅ Livre existant: {$book['title']}\n";
            }
        } catch (Exception $e) {
            echo "⚠️ Erreur livre {$book['title']}: " . $e->getMessage() . "\n";
        }
    }
}

echo "\n💰 CONFIGURATION FINANCES ADAPTÉE\n";
echo "===============================\n";

// Vérifier structure fees_masters
if (in_array('fees_masters', $allTables)) {
    $feeColumns = DB::getSchemaBuilder()->getColumnListing('fees_masters');
    echo "Colonnes fees_masters: " . implode(', ', $feeColumns) . "\n";
    
    $simpleFees = [
        ['name' => 'Frais de scolarité primaire', 'amount' => 120000],
        ['name' => 'Frais de scolarité collège', 'amount' => 160000], 
        ['name' => 'Frais de scolarité lycée', 'amount' => 180000],
        ['name' => 'Transport scolaire', 'amount' => 30000],
        ['name' => 'Cantine', 'amount' => 25000],
        ['name' => 'Activités parascolaires', 'amount' => 15000]
    ];
    
    foreach ($simpleFees as $fee) {
        try {
            $insertData = [
                'status' => 1,
                'created_at' => now(),
                'updated_at' => now(),
            ];
            
            // Ajouter les colonnes qui existent
            if (in_array('name', $feeColumns)) {
                $insertData['name'] = $fee['name'];
                $exists = DB::table('fees_masters')->where('name', $fee['name'])->first();
            } else {
                $insertData['title'] = $fee['name']; // Essayer title au lieu de name
                $exists = DB::table('fees_masters')->where('title', $fee['name'])->first();
            }
            
            if (in_array('amount', $feeColumns)) {
                $insertData['amount'] = $fee['amount'];
            }
            
            if (!$exists) {
                DB::table('fees_masters')->insert($insertData);
                echo "✅ Frais ajouté: {$fee['name']} - {$fee['amount']} DZD\n";
            } else {
                echo "✅ Frais existant: {$fee['name']}\n";
            }
        } catch (Exception $e) {
            echo "⚠️ Erreur frais {$fee['name']}: " . $e->getMessage() . "\n";
        }
    }
}

echo "\n🎯 RÉSUMÉ FINAL\n";
echo "==============\n";
echo "✅ Toutes les vérifications terminées\n";
echo "🚗 Module transport: Tables vérifiées et véhicules ajoutés si possible\n";
echo "📚 Bibliothèque: Livres ajoutés avec structure adaptée\n";
echo "💰 Finance: Frais configurés selon colonnes disponibles\n";
echo "🏫 BBC School Algeria optimisée selon la structure existante!\n\n";

echo "🌐 Accéder à l'application : http://localhost/onestschooled-test/public\n";

?>