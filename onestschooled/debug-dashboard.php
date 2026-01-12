<?php

require_once 'vendor/autoload.php';

$app = require_once 'bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

echo "🔍 DIAGNOSTIC DASHBOARD BBC SCHOOL ALGERIA\n";
echo "=" . str_repeat("=", 50) . "\n\n";

try {
    echo "📊 Vérification des compteurs dashboard...\n\n";
    
    // Session actuelle
    $current_session = setting('session');
    echo "Session actuelle: " . ($current_session ?? 'NON DÉFINIE') . "\n";
    
    // Test direct des requêtes
    $students = \App\Models\StudentInfo\SessionClassStudent::where('session_id', $current_session)->count();
    $parents = \App\Models\StudentInfo\ParentGuardian::count();
    $teachers = \App\Models\Staff\Staff::where('role_id', 5)->count();
    $sessions = \App\Models\Session::count();
    
    echo "\n📈 RÉSULTATS DES COMPTEURS:\n";
    echo "✅ Étudiants actifs: $students\n";
    echo "✅ Parents: $parents\n";
    echo "✅ Enseignants: $teachers\n";
    echo "✅ Sessions: $sessions\n";
    
    // Vérifier les tables
    echo "\n🔍 VÉRIFICATION DES TABLES:\n";
    
    $total_students = \App\Models\StudentInfo\Student::count();
    echo "📚 Total étudiants (table students): $total_students\n";
    
    $total_session_students = \App\Models\StudentInfo\SessionClassStudent::count();
    echo "📚 Total session-class-students: $total_session_students\n";
    
    $total_staff = \App\Models\Staff\Staff::count();
    echo "👨‍🏫 Total staff: $total_staff\n";
    
    // Détails des enseignants
    $teachers_details = \App\Models\Staff\Staff::where('role_id', 5)->get(['id', 'first_name', 'last_name']);
    echo "👨‍🏫 Enseignants trouvés:\n";
    foreach($teachers_details as $teacher) {
        echo "   - {$teacher->first_name} {$teacher->last_name} (ID: {$teacher->id})\n";
    }
    
    // Test du DashboardRepository
    echo "\n🧪 TEST DU REPOSITORY:\n";
    $repo = new \App\Repositories\DashboardRepository();
    $data = $repo->index();
    
    echo "Repository résultats:\n";
    foreach($data as $key => $value) {
        if(is_array($value)) {
            echo "   $key: " . count($value) . " éléments\n";
        } else {
            echo "   $key: $value\n";
        }
    }
    
    echo "\n✅ Diagnostic terminé !\n";
    
} catch (Exception $e) {
    echo "❌ ERREUR: " . $e->getMessage() . "\n";
    echo "📍 Fichier: " . $e->getFile() . ":" . $e->getLine() . "\n";
}