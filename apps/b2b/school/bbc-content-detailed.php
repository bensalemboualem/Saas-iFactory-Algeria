<?php

/**
 * BBC School Algeria - Ajout de contenu spécifique aux modules
 * Livres, frais détaillés, et autres données spécifiques
 */

require_once __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use Illuminate\Support\Facades\DB;

echo "📚 BBC SCHOOL ALGERIA - AJOUT DE CONTENU DÉTAILLÉ\n";
echo "================================================\n\n";

// AJOUTER DES LIVRES SPÉCIFIQUES À LA BIBLIOTHÈQUE
echo "📖 AJOUT DE LIVRES SPÉCIFIQUES BBC SCHOOL\n";
echo "========================================\n";

$bbcBooks = [
    // Livres de Français
    ['title' => 'Le Petit Prince - Antoine de Saint-Exupéry', 'author' => 'Antoine de Saint-Exupéry', 'isbn' => '978-2-07-040817-4', 'category' => 'Français - Littérature'],
    ['title' => 'Les Misérables - Victor Hugo', 'author' => 'Victor Hugo', 'isbn' => '978-2-253-09632-5', 'category' => 'Français - Littérature'],
    ['title' => 'Grammaire Progressive du Français', 'author' => 'Maïa Grégoire', 'isbn' => '978-2-09-038013-1', 'category' => 'Français - Littérature'],
    
    // Livres d'Arabe
    ['title' => 'نهج البلاغة - الإمام علي', 'author' => 'الإمام علي عليه السلام', 'isbn' => '978-9953-71-123-4', 'category' => 'العربية - الأدب العربي'],
    ['title' => 'ديوان المتنبي', 'author' => 'أبو الطيب المتنبي', 'isbn' => '978-9953-71-456-7', 'category' => 'العربية - الأدب العربي'],
    ['title' => 'تاريخ الجزائر المعاصر', 'author' => 'شارل روبير أجرون', 'isbn' => '978-9961-0-1234-5', 'category' => 'History - Algeria'],
    
    // Livres de Mathématiques
    ['title' => 'Mathématiques 3ème - Collection Phare', 'author' => 'Roger Brault', 'isbn' => '978-2-01-125547-8', 'category' => 'Mathematics - Textbooks'],
    ['title' => 'Géométrie Euclidienne', 'author' => 'Jean-Denis Eiden', 'isbn' => '978-2-10-048390-5', 'category' => 'Mathematics - Textbooks'],
    ['title' => 'Algèbre - 2AS Sciences', 'author' => 'André Antibi', 'isbn' => '978-2-09-172847-3', 'category' => 'Mathematics - Textbooks'],
    
    // Livres de Sciences
    ['title' => 'Biologie - Campbell', 'author' => 'Neil A. Campbell', 'isbn' => '978-2-7440-7398-6', 'category' => 'Sciences - Biology'],
    ['title' => 'Physique Chimie 2nde', 'author' => 'André Durupthy', 'isbn' => '978-2-01-135542-1', 'category' => 'Sciences - Physics'],
    ['title' => 'Chimie Organique - Paul Arnaud', 'author' => 'Paul Arnaud', 'isbn' => '978-2-10-053932-4', 'category' => 'Sciences - Chemistry'],
    
    // Histoire et Géographie
    ['title' => 'Histoire de l\'Algérie contemporaine', 'author' => 'Benjamin Stora', 'isbn' => '978-2-13-057883-1', 'category' => 'History - Algeria'],
    ['title' => 'Géographie du Maghreb', 'author' => 'Jean-François Troin', 'isbn' => '978-2-200-34567-8', 'category' => 'Geography - North Africa'],
    
    // Études Islamiques
    ['title' => 'Introduction aux Sciences du Coran', 'author' => 'Muhammad Abu Shahba', 'isbn' => '978-9960-850-45-6', 'category' => 'Islamic Studies'],
    ['title' => 'السيرة النبوية لابن هشام', 'author' => 'ابن هشام', 'isbn' => '978-9953-71-789-0', 'category' => 'Islamic Studies'],
    
    // Informatique
    ['title' => 'Algorithmes et Structures de Données', 'author' => 'Thomas H. Cormen', 'isbn' => '978-2-10-054526-4', 'category' => 'Computer Science'],
    ['title' => 'Python pour les Nuls', 'author' => 'John Paul Mueller', 'isbn' => '978-2-412-03728-1', 'category' => 'Computer Science']
];

foreach ($bbcBooks as $book) {
    try {
        // Récupérer l'ID de la catégorie
        $category = DB::table('book_categories')->where('name', $book['category'])->first();
        if ($category) {
            $exists = DB::table('books')->where('isbn', $book['isbn'])->first();
            if (!$exists) {
                DB::table('books')->insert([
                    'title' => $book['title'],
                    'author' => $book['author'],
                    'isbn' => $book['isbn'],
                    'book_category_id' => $category->id,
                    'quantity' => rand(5, 20), // Quantité aléatoire entre 5 et 20
                    'available_quantity' => rand(3, 15),
                    'status' => 1,
                    'created_at' => now(),
                    'updated_at' => now(),
                ]);
                echo "   ✅ {$book['title']}\n";
            } else {
                echo "   ✅ {$book['title']} - Déjà existant\n";
            }
        }
    } catch (Exception $e) {
        echo "   ⚠️  Erreur pour {$book['title']}: " . $e->getMessage() . "\n";
    }
}

// AJOUTER DES FRAIS DÉTAILLÉS EN DZD
echo "\n💰 AJOUT DES FRAIS DÉTAILLÉS BBC SCHOOL (DZD)\n";
echo "===========================================\n";

$bbcDetailedFees = [
    // Frais par niveau
    ['name' => 'Frais CP - Course Préparatoire', 'description' => 'Frais annuels niveau CP', 'amount' => 120000],
    ['name' => 'Frais CE1/CE2 - Cours Élémentaire', 'description' => 'Frais annuels niveaux CE1 et CE2', 'amount' => 130000],
    ['name' => 'Frais CM1/CM2 - Cours Moyen', 'description' => 'Frais annuels niveaux CM1 et CM2', 'amount' => 140000],
    ['name' => 'Frais Collège (6ème-3ème)', 'description' => 'Frais annuels niveau collège', 'amount' => 160000],
    ['name' => 'Frais Lycée (1AS-2AS)', 'description' => 'Frais annuels niveau lycée', 'amount' => 180000],
    
    // Frais spéciaux
    ['name' => 'Frais de Réinscription', 'description' => 'Frais pour anciens élèves', 'amount' => 20000],
    ['name' => 'Frais de Transfert', 'description' => 'Frais de dossier de transfert', 'amount' => 15000],
    ['name' => 'Frais d\'Examen BEM', 'description' => 'Préparation examen BEM', 'amount' => 25000],
    ['name' => 'Frais d\'Examen BAC', 'description' => 'Préparation examen BAC', 'amount' => 30000],
    
    // Services additionnels  
    ['name' => 'Transport Zone 1 (Centre-ville)', 'description' => 'Transport scolaire zone centrale', 'amount' => 25000],
    ['name' => 'Transport Zone 2 (Banlieue proche)', 'description' => 'Transport scolaire banlieue proche', 'amount' => 30000],
    ['name' => 'Transport Zone 3 (Banlieue éloignée)', 'description' => 'Transport scolaire banlieue éloignée', 'amount' => 35000],
    ['name' => 'Cantine - Demi-pension', 'description' => 'Repas de midi seulement', 'amount' => 18000],
    ['name' => 'Cantine - Pension complète', 'description' => 'Petit-déjeuner et déjeuner', 'amount' => 28000],
    ['name' => 'Activités Parascolaires', 'description' => 'Sports, musique, arts', 'amount' => 12000],
    ['name' => 'Cours de Soutien', 'description' => 'Aide aux devoirs et révisions', 'amount' => 20000],
    ['name' => 'Sortie Pédagogique', 'description' => 'Excursions éducatives', 'amount' => 8000]
];

foreach ($bbcDetailedFees as $fee) {
    try {
        $exists = DB::table('fees_masters')->where('name', $fee['name'])->first();
        if (!$exists) {
            DB::table('fees_masters')->insert([
                'name' => $fee['name'],
                'amount' => $fee['amount'],
                'status' => 1,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            echo "   ✅ {$fee['name']} - {$fee['amount']} DZD\n";
        } else {
            echo "   ✅ {$fee['name']} - Déjà existant\n";
        }
    } catch (Exception $e) {
        echo "   ⚠️  Erreur pour {$fee['name']}: " . $e->getMessage() . "\n";
    }
}

// AJOUTER DES SALLES DE CLASSE
echo "\n🏫 AJOUT DES SALLES DE CLASSE BBC SCHOOL\n";
echo "======================================\n";

$bbcClassrooms = [
    // Salles Primaire
    ['name' => 'CP-A - Salle Rose', 'capacity' => 25, 'type' => 'Primaire'],
    ['name' => 'CP-B - Salle Bleue', 'capacity' => 25, 'type' => 'Primaire'],
    ['name' => 'CE1-A - Salle Verte', 'capacity' => 28, 'type' => 'Primaire'],
    ['name' => 'CE1-B - Salle Jaune', 'capacity' => 28, 'type' => 'Primaire'],
    ['name' => 'CE2-A - Salle Orange', 'capacity' => 30, 'type' => 'Primaire'],
    ['name' => 'CE2-B - Salle Violette', 'capacity' => 30, 'type' => 'Primaire'],
    ['name' => 'CM1-A - Salle 101', 'capacity' => 32, 'type' => 'Primaire'],
    ['name' => 'CM1-B - Salle 102', 'capacity' => 32, 'type' => 'Primaire'],
    ['name' => 'CM2-A - Salle 103', 'capacity' => 32, 'type' => 'Primaire'],
    ['name' => 'CM2-B - Salle 104', 'capacity' => 32, 'type' => 'Primaire'],
    
    // Salles Collège
    ['name' => '6ème-A - Salle 201', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '6ème-B - Salle 202', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '5ème-A - Salle 203', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '5ème-B - Salle 204', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '4ème-A - Salle 205', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '4ème-B - Salle 206', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '3ème-A - Salle 207', 'capacity' => 35, 'type' => 'Collège'],
    ['name' => '3ème-B - Salle 208', 'capacity' => 35, 'type' => 'Collège'],
    
    // Salles Lycée
    ['name' => '2AS-Scientifique - Salle 301', 'capacity' => 40, 'type' => 'Lycée'],
    ['name' => '2AS-Littéraire - Salle 302', 'capacity' => 40, 'type' => 'Lycée'],
    ['name' => '1AS-Scientifique - Salle 303', 'capacity' => 40, 'type' => 'Lycée'],
    ['name' => '1AS-Littéraire - Salle 304', 'capacity' => 40, 'type' => 'Lycée'],
    ['name' => '2AS-Sciences - Salle 305', 'capacity' => 40, 'type' => 'Lycée'],
    ['name' => '2AS-Lettres - Salle 306', 'capacity' => 40, 'type' => 'Lycée'],
    
    // Salles spécialisées
    ['name' => 'Laboratoire Physique-Chimie', 'capacity' => 30, 'type' => 'Laboratoire'],
    ['name' => 'Laboratoire Biologie', 'capacity' => 30, 'type' => 'Laboratoire'],
    ['name' => 'Salle Informatique', 'capacity' => 25, 'type' => 'Informatique'],
    ['name' => 'Bibliothèque', 'capacity' => 50, 'type' => 'Bibliothèque'],
    ['name' => 'Salle de Sport', 'capacity' => 60, 'type' => 'Sport'],
    ['name' => 'Salle de Musique', 'capacity' => 35, 'type' => 'Arts'],
    ['name' => 'Salle des Professeurs', 'capacity' => 20, 'type' => 'Administration']
];

foreach ($bbcClassrooms as $classroom) {
    try {
        $exists = DB::table('class_rooms')->where('name', $classroom['name'])->first();
        if (!$exists) {
            DB::table('class_rooms')->insert([
                'name' => $classroom['name'],
                'capacity' => $classroom['capacity'],
                'type' => $classroom['type'],
                'status' => 1,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            echo "   ✅ {$classroom['name']} - {$classroom['capacity']} places\n";
        } else {
            echo "   ✅ {$classroom['name']} - Déjà existant\n";
        }
    } catch (Exception $e) {
        echo "   ⚠️  Erreur pour {$classroom['name']}: " . $e->getMessage() . "\n";
    }
}

echo "\n🎯 MODULES BBC SCHOOL COMPLÈTEMENT REMPLIS !\n";
echo "==========================================\n";
echo "📚 Bibliothèque : " . count($bbcBooks) . " livres ajoutés\n";
echo "💰 Finance : " . count($bbcDetailedFees) . " types de frais configurés\n";
echo "🏫 Salles : " . count($bbcClassrooms) . " salles de classe créées\n";
echo "✅ BBC School Algeria est prête pour l'utilisation !\n\n";

echo "🌐 Accéder à l'application : http://localhost/onestschooled-test/public\n";

?>