/**
 * Icon Theme Switcher
 * Bascule les icônes providers entre /light/ et /dark/ selon le thème
 */

function updateProviderIcons() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const fromPath = isDark ? '/light/' : '/dark/';
    const toPath = isDark ? '/dark/' : '/light/';

    // Sélectionner toutes les images des providers et modèles
    const images = document.querySelectorAll('.provider-item img, .model-half img');

    images.forEach(img => {
        if (img.src && img.src.includes('lobehub/icons-static-png')) {
            img.src = img.src.replace(fromPath, toPath);
        }
    });
}

// Observer les changements de thème
const themeObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
            updateProviderIcons();
        }
    });
});

// Démarrer l'observation
themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
});

// Appliquer au chargement initial
document.addEventListener('DOMContentLoaded', () => {
    // Attendre un peu pour que le contenu legacy soit chargé
    setTimeout(updateProviderIcons, 100);
});

// Appliquer immédiatement si le DOM est déjà prêt
if (document.readyState !== 'loading') {
    setTimeout(updateProviderIcons, 100);
}
