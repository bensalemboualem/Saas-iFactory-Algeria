<?php

require_once __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use Illuminate\Support\Facades\DB;

echo "🔍 RECHERCHE UTILISATEUR ADMIN BBC SCHOOL\n";
echo "=========================================\n\n";

try {
    // Chercher les utilisateurs admin
    $admins = DB::table('users')
        ->select('id', 'name', 'email', 'role_id', 'status')
        ->orderBy('role_id')
        ->limit(10)
        ->get();
    
    echo "👥 UTILISATEURS DANS LA BASE :\n";
    foreach ($admins as $user) {
        $role = $user->role_id == 1 ? 'ADMIN' : 'USER';
        $status = $user->status == 1 ? '✅' : '❌';
        echo "   $status ID:{$user->id} - {$user->name} ({$user->email}) - Role: $role\n";
    }
    
} catch (Exception $e) {
    echo "❌ Erreur: " . $e->getMessage() . "\n";
}

?>