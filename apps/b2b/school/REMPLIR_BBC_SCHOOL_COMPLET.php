<?php
/**
 * REMPLISSAGE COMPLET BBC SCHOOL ALGERIA
 * Remplit TOUS les modules avec des données réalistes
 * Pour présentation professionnelle
 */

require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

echo "\n========================================\n";
echo "REMPLISSAGE COMPLET BBC SCHOOL ALGERIA\n";
echo "========================================\n\n";

// Connexion à la base de données
try {
    DB::connection()->getPdo();
    echo "✅ Connexion base de données réussie\n\n";
} catch (\Exception $e) {
    die("❌ Erreur connexion: " . $e->getMessage() . "\n");
}

// ÉTAPE 1: VÉRIFIER LES DONNÉES EXISTANTES
echo "📊 VÉRIFICATION DES DONNÉES EXISTANTES\n";
echo "=====================================\n\n";

$stats = [
    'students' => DB::table('students')->count(),
    'parents' => DB::table('parents')->count(),
    'teachers' => DB::table('staffs')->where('role_id', 4)->count(), // Role 4 = Teacher
    'classes' => DB::table('classes')->count(),
    'sections' => DB::table('sections')->count(),
    'subjects' => DB::table('subjects')->count(),
    'sessions' => DB::table('academic_years')->count(),
];

echo "Étudiants: {$stats['students']}\n";
echo "Parents: {$stats['parents']}\n";
echo "Enseignants: {$stats['teachers']}\n";
echo "Classes: {$stats['classes']}\n";
echo "Sections: {$stats['sections']}\n";
echo "Matières: {$stats['subjects']}\n";
echo "Sessions: {$stats['sessions']}\n\n";

// ÉTAPE 2: CRÉER SESSION ACADÉMIQUE 2024-2025
echo "📅 CRÉATION SESSION ACADÉMIQUE 2024-2025\n";
echo "========================================\n\n";

$currentSession = DB::table('academic_years')->where('year', '2024-2025')->first();

if (!$currentSession) {
    $sessionId = DB::table('academic_years')->insertGetId([
        'year' => '2024-2025',
        'title' => 'Année Scolaire 2024-2025',
        'starting_date' => '2024-09-01',
        'ending_date' => '2025-06-30',
        'active_status' => 1,
        'created_at' => now(),
        'updated_at' => now(),
    ]);
    echo "✅ Session académique 2024-2025 créée (ID: $sessionId)\n\n";
} else {
    $sessionId = $currentSession->id;
    echo "✅ Session académique 2024-2025 existe déjà (ID: $sessionId)\n\n";
}

// ÉTAPE 3: CRÉER CLASSES POUR BBC SCHOOL ALGERIA
echo "🏫 CRÉATION DES CLASSES\n";
echo "=======================\n\n";

$classesData = [
    // Maternelle (3 niveaux)
    ['name' => 'Petite Section', 'name_ar' => 'القسم الصغير', 'section_number' => 2],
    ['name' => 'Moyenne Section', 'name_ar' => 'القسم المتوسط', 'section_number' => 2],
    ['name' => 'Grande Section', 'name_ar' => 'القسم الكبير', 'section_number' => 2],

    // Primaire (5 niveaux)
    ['name' => '1ère Année Primaire', 'name_ar' => 'السنة الأولى ابتدائي', 'section_number' => 3],
    ['name' => '2ème Année Primaire', 'name_ar' => 'السنة الثانية ابتدائي', 'section_number' => 3],
    ['name' => '3ème Année Primaire', 'name_ar' => 'السنة الثالثة ابتدائي', 'section_number' => 2],
    ['name' => '4ème Année Primaire', 'name_ar' => 'السنة الرابعة ابتدائي', 'section_number' => 2],
    ['name' => '5ème Année Primaire', 'name_ar' => 'السنة الخامسة ابتدائي', 'section_number' => 2],

    // Cycle Moyen (4 niveaux)
    ['name' => '1ère Année Moyenne', 'name_ar' => 'السنة الأولى متوسط', 'section_number' => 2],
    ['name' => '2ème Année Moyenne', 'name_ar' => 'السنة الثانية متوسط', 'section_number' => 2],
    ['name' => '3ème Année Moyenne', 'name_ar' => 'السنة الثالثة متوسط', 'section_number' => 2],
    ['name' => '4ème Année Moyenne', 'name_ar' => 'السنة الرابعة متوسط', 'section_number' => 2],
];

$createdClasses = [];
foreach ($classesData as $classData) {
    $existing = DB::table('classes')->where('name', $classData['name'])->first();

    if (!$existing) {
        $classId = DB::table('classes')->insertGetId([
            'name' => $classData['name'],
            'academic_year_id' => $sessionId,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        echo "✅ Classe créée: {$classData['name']}\n";

        // Créer les sections pour cette classe
        $sections = ['A', 'B', 'C', 'D'];
        for ($i = 0; $i < $classData['section_number']; $i++) {
            DB::table('sections')->insert([
                'name' => $sections[$i],
                'class_id' => $classId,
                'capacity' => 25,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
            echo "   ✓ Section {$sections[$i]} créée\n";
        }

        $createdClasses[] = $classId;
    } else {
        echo "⚠️  Classe existe déjà: {$classData['name']}\n";
        $createdClasses[] = $existing->id;
    }
}

echo "\n✅ " . count($createdClasses) . " classes vérifiées/créées\n\n";

// ÉTAPE 4: CRÉER MATIÈRES
echo "📚 CRÉATION DES MATIÈRES\n";
echo "========================\n\n";

$subjectsData = [
    // Matières Maternelle
    ['name' => 'Éveil', 'name_ar' => 'التفتح', 'type' => 'theory'],
    ['name' => 'Psychomotricité', 'name_ar' => 'التربية الحركية', 'type' => 'practical'],
    ['name' => 'Langage', 'name_ar' => 'اللغة', 'type' => 'theory'],

    // Matières Primaire
    ['name' => 'Langue Arabe', 'name_ar' => 'اللغة العربية', 'type' => 'theory'],
    ['name' => 'Langue Française', 'name_ar' => 'اللغة الفرنسية', 'type' => 'theory'],
    ['name' => 'Mathématiques', 'name_ar' => 'الرياضيات', 'type' => 'theory'],
    ['name' => 'Sciences', 'name_ar' => 'العلوم', 'type' => 'theory'],
    ['name' => 'Histoire-Géographie', 'name_ar' => 'التاريخ والجغرافيا', 'type' => 'theory'],
    ['name' => 'Éducation Islamique', 'name_ar' => 'التربية الإسلامية', 'type' => 'theory'],
    ['name' => 'Éducation Physique', 'name_ar' => 'التربية البدنية', 'type' => 'practical'],
    ['name' => 'Dessin', 'name_ar' => 'الرسم', 'type' => 'practical'],
    ['name' => 'Musique', 'name_ar' => 'الموسيقى', 'type' => 'practical'],

    // Matières Cycle Moyen
    ['name' => 'Langue Anglaise', 'name_ar' => 'اللغة الإنجليزية', 'type' => 'theory'],
    ['name' => 'Physique', 'name_ar' => 'الفيزياء', 'type' => 'theory'],
    ['name' => 'Technologie', 'name_ar' => 'التكنولوجيا', 'type' => 'theory'],
    ['name' => 'Informatique', 'name_ar' => 'الإعلام الآلي', 'type' => 'practical'],
];

$createdSubjects = [];
foreach ($subjectsData as $subject) {
    $existing = DB::table('subjects')->where('name', $subject['name'])->first();

    if (!$existing) {
        $subjectId = DB::table('subjects')->insertGetId([
            'name' => $subject['name'],
            'type' => $subject['type'],
            'code' => strtoupper(substr($subject['name'], 0, 3)),
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        echo "✅ Matière créée: {$subject['name']} ({$subject['type']})\n";
        $createdSubjects[] = $subjectId;
    } else {
        echo "⚠️  Matière existe déjà: {$subject['name']}\n";
        $createdSubjects[] = $existing->id;
    }
}

echo "\n✅ " . count($createdSubjects) . " matières vérifiées/créées\n\n";

echo "========================================\n";
echo "PHASE 1 TERMINÉE\n";
echo "========================================\n\n";

echo "Prochaines étapes à faire:\n";
echo "1. Créer enseignants (staffs)\n";
echo "2. Créer étudiants avec photos\n";
echo "3. Créer parents\n";
echo "4. Remplir présences\n";
echo "5. Créer emplois du temps\n";
echo "6. Créer examens et notes\n";
echo "7. Créer frais scolaires\n";
echo "8. Créer notices board\n";
echo "9. Créer événements\n";
echo "10. Activer live chat\n";
echo "11. Remplir forums\n";
echo "12. Créer messages SMS/Email\n\n";

echo "Voulez-vous continuer avec la Phase 2?\n";

?>
