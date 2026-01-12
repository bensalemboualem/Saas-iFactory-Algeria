
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
