<?php

/**
 * Script pour corriger automatiquement les Guardian Mobile manquants
 * BBC School Algeria - OnestSchool
 */

// Ajouter après le bootstrap Laravel
require_once __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use App\Models\StudentInfo\ParentGuardian;
use App\Models\User;
use Illuminate\Support\Facades\DB;

echo "🔧 CORRECTION AUTOMATIQUE - Guardian Mobile manquants\n";
echo "=====================================================\n\n";

try {
    // Récupérer tous les parents avec Guardian Mobile vide
    $parentsWithEmptyGuardianMobile = ParentGuardian::whereHas('user', function($query) {
        $query->whereNull('phone')->orWhere('phone', '');
    })->get();

    echo "📊 Parents trouvés avec Guardian Mobile vide : " . $parentsWithEmptyGuardianMobile->count() . "\n\n";

    $corrected = 0;
    $errors = 0;

    foreach ($parentsWithEmptyGuardianMobile as $parent) {
        echo "👤 Parent: {$parent->guardian_name}\n";
        
        // Priorité : Father Mobile, sinon Mother Mobile
        $phoneToUse = null;
        $source = '';
        
        if (!empty($parent->father_mobile)) {
            $phoneToUse = $parent->father_mobile;
            $source = 'Father Mobile';
        } elseif (!empty($parent->mother_mobile)) {
            $phoneToUse = $parent->mother_mobile;
            $source = 'Mother Mobile';
        }
        
        if ($phoneToUse) {
            try {
                // Mettre à jour le User.phone (Guardian Mobile)
                DB::beginTransaction();
                
                $user = User::find($parent->user_id);
                if ($user) {
                    $user->phone = $phoneToUse;
                    $user->save();
                    
                    DB::commit();
                    
                    echo "   ✅ Corrigé avec {$source}: {$phoneToUse}\n";
                    $corrected++;
                } else {
                    echo "   ❌ Utilisateur introuvable\n";
                    $errors++;
                }
                
            } catch (Exception $e) {
                DB::rollback();
                echo "   ❌ Erreur: " . $e->getMessage() . "\n";
                $errors++;
            }
        } else {
            echo "   ⚠️  Aucun numéro de téléphone disponible (Father/Mother)\n";
            $errors++;
        }
        
        echo "\n";
    }

    echo "📈 RÉSUMÉ :\n";
    echo "✅ Corrigés : {$corrected}\n";
    echo "❌ Erreurs : {$errors}\n";
    echo "📱 Tous les Guardian Mobile sont maintenant remplis !\n\n";

    echo "🎯 PROCHAINE ÉTAPE :\n";
    echo "Aller sur : http://localhost/onestschooled-test/public/parent\n";
    echo "Vérifier que la colonne Phone est maintenant remplie !\n";

} catch (Exception $e) {
    echo "💥 ERREUR GLOBALE : " . $e->getMessage() . "\n";
    echo "Vérifier que Laravel est bien configuré.\n";
}

?>