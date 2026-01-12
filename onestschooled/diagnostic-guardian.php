<?php

// Test simple pour diagnostiquer le problème Guardian Mobile

// Simuler les données du formulaire
$test_data = [
    'guardian_name' => 'Test Parent',
    'guardian_mobile' => '+213123456789',
    'guardian_email' => 'test@example.com',
    'father_name' => 'Test Father',
    'father_mobile' => '+213987654321',
    'mother_name' => 'Test Mother', 
    'mother_mobile' => '+213111222333',
    'status' => '1'
];

echo "🧪 Test Diagnostic - Guardian Mobile\n";
echo "=====================================\n\n";

echo "📋 Données de test :\n";
foreach($test_data as $key => $value) {
    echo "  $key: $value\n";
}

echo "\n🔍 Problèmes potentiels identifiés :\n";
echo "1. ❌ Validation unique:users,phone sur guardian_mobile\n";
echo "2. ❌ IDs dupliqués dans le formulaire HTML (exampleDataList)\n";
echo "3. ❌ Erreurs de syntaxe required>> au lieu de required>\n";
echo "4. ❌ Validation incohérente entre create/update\n";

echo "\n✅ Corrections appliquées :\n";
echo "1. ✅ Supprimé unique:users,phone de la validation create\n";
echo "2. ✅ IDs uniques pour chaque champ (father_name_input, etc.)\n";
echo "3. ✅ Corrigé toutes les erreurs de syntaxe required>>\n";
echo "4. ✅ Aligné validation create/update\n";

echo "\n🎯 À tester maintenant :\n";
echo "1. Aller sur: http://localhost/onestschooled-test/public/parent/create\n";
echo "2. Remplir tous les champs obligatoires (*)\n";
echo "3. Vérifier que Guardian Mobile ne se vide plus\n";
echo "4. Soumettre le formulaire\n";

echo "\n⚠️  Si le problème persiste :\n";
echo "- Vérifier les erreurs JavaScript dans la console navigateur\n";
echo "- Vérifier les erreurs Laravel dans storage/logs/laravel.log\n";
echo "- Tester avec un numéro complètement différent\n";

?>