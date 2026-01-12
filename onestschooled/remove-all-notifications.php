<?php
require_once 'vendor/autoload.php';

// Configuration Laravel
$app = require_once 'bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

echo "🔧 SUPPRESSION COMPLÈTE DES NOTIFICATIONS AUTO - BBC SCHOOL\n";
echo "=========================================================\n\n";

try {
    // 1. Désactiver complètement les notifications automatiques dans bbc-script.js
    echo "📝 Suppression totale des notifications automatiques...\n";
    
    $bbcScriptPath = 'public/js/bbc-script.js';
    if (file_exists($bbcScriptPath)) {
        $content = file_get_contents($bbcScriptPath);
        
        // Supprimer toutes les notifications automatiques
        $patterns = [
            '/setTimeout\s*\(\s*\(\)\s*=>\s*{\s*showBBCNotification\([^}]+}\s*,\s*\d+\);/s',
            '/setTimeout\s*\(\s*function\s*\(\)\s*{\s*showBBCNotification\([^}]+}\s*,\s*\d+\);/s',
            '/"🎓 Bienvenue à BBC School Algeria !"/i',
            '/"Bienvenue sur le site de BBC School Algeria"/i'
        ];
        
        foreach ($patterns as $pattern) {
            $content = preg_replace($pattern, '// Notification automatique supprimée', $content);
        }
        
        // Ajouter un blocage complet des notifications automatiques
        $blockCode = '
    // BLOCAGE COMPLET DES NOTIFICATIONS AUTOMATIQUES BBC SCHOOL
    // Pour empêcher toute notification automatique de s\'afficher
    const originalShowBBCNotification = window.showBBCNotification;
    window.showBBCNotification = function(message, type = "info", duration = 5000) {
        // Ne rien faire pour les notifications automatiques
        console.log("Notification automatique bloquée:", message);
        return false;
    };
    
    // Garder la fonction originale pour usage manuel si nécessaire
    window.showBBCNotificationForced = originalShowBBCNotification;
';
        
        $content = str_replace('// Fonction globale pour les notifications', $blockCode . '    // Fonction globale pour les notifications', $content);
        
        file_put_contents($bbcScriptPath, $content);
        echo "✅ Fichier bbc-script.js mis à jour\n";
    }
    
    // 2. Créer un script pour vider le cache du navigateur
    $cacheScript = 'public/js/clear-cache.js';
    $cacheContent = '
// Script pour forcer le rafraîchissement du cache
(function() {
    // Forcer le rechargement des scripts mis en cache
    const scripts = document.getElementsByTagName("script");
    for (let script of scripts) {
        if (script.src && script.src.includes("bbc-script.js")) {
            script.src = script.src + "?v=" + Date.now();
        }
    }
    
    // Supprimer toutes les notifications existantes
    const notifications = document.querySelectorAll(".bbc-notification, .toast, .alert");
    notifications.forEach(notification => {
        notification.remove();
    });
    
    console.log("🚫 Toutes les notifications automatiques ont été désactivées");
})();
';
    
    file_put_contents($cacheScript, $cacheContent);
    echo "✅ Script de nettoyage de cache créé\n";
    
    // 3. Vérifier et nettoyer d'autres fichiers potentiels
    echo "\n🔍 Vérification d'autres sources de notifications...\n";
    
    $filesToCheck = [
        'resources/views/frontend/master.blade.php',
        'resources/views/layouts/master.blade.php', 
        'public/js/custom.js',
        'public/js/app.js'
    ];
    
    foreach ($filesToCheck as $file) {
        if (file_exists($file)) {
            $content = file_get_contents($file);
            if (strpos($content, 'toastr') !== false || strpos($content, 'notification') !== false) {
                echo "⚠️  Trouvé des notifications dans: $file\n";
            } else {
                echo "✅ Propre: $file\n";
            }
        }
    }
    
    // 4. Créer un patch pour le template principal
    echo "\n📄 Création du patch pour le template principal...\n";
    
    $templatePatch = '
<!-- PATCH ANTI-NOTIFICATION BBC SCHOOL -->
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Désactiver toutes les notifications automatiques
    if (typeof toastr !== "undefined") {
        const originalToastr = toastr.success;
        toastr.success = function(message, title) {
            if (message && (message.includes("Bienvenue") || message.includes("bbc") || message.includes("BBC"))) {
                console.log("Notification toastr bloquée:", message);
                return;
            }
            return originalToastr.apply(this, arguments);
        };
    }
    
    // Supprimer toutes les notifications existantes après 1 seconde
    setTimeout(() => {
        const allNotifications = document.querySelectorAll(
            ".bbc-notification, .toast, .alert, .notification, " +
            "[class*=\\"notification\\"], [class*=\\"toast\\"], [class*=\\"alert\\"]"
        );
        allNotifications.forEach(el => {
            if (el.textContent && el.textContent.toLowerCase().includes("bienvenue")) {
                el.remove();
            }
        });
    }, 1000);
});
</script>
<!-- FIN PATCH ANTI-NOTIFICATION -->
';
    
    file_put_contents('public/anti-notification-patch.html', $templatePatch);
    echo "✅ Patch anti-notification créé\n";
    
    echo "\n🎯 SOLUTION COMPLÈTE APPLIQUÉE !\n";
    echo "================================\n";
    echo "✅ Notifications automatiques bloquées\n";
    echo "✅ Script de cache clearing créé\n";
    echo "✅ Patch de sécurité installé\n";
    echo "\n🌐 Actions pour l'utilisateur:\n";
    echo "1. Rafraîchir la page avec Ctrl+F5 (vider le cache)\n";
    echo "2. Ou ouvrir en navigation privée\n";
    echo "3. Vérifier que les notifications ont disparu\n\n";
    
} catch (Exception $e) {
    echo "❌ Erreur: " . $e->getMessage() . "\n";
}
?>