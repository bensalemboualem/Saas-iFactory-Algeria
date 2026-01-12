/**
 * IAFactory Footer Auto-Injection System
 * 
 * Usage: Add <div data-iaf-footer></div> anywhere in your page
 * The footer will be automatically loaded and injected
 * 
 * OR add <script src="../shared/footer-inject.js" data-iaf-footer-auto></script>
 * to automatically append footer at end of body
 */

(function() {
    'use strict';
    
    /**
     * Détecte le chemin relatif correct selon la profondeur du fichier
     */
    function getFooterPath() {
        // Essaye de détecter le chemin en fonction du script
        const currentScript = document.currentScript || document.querySelector('script[src*="footer-inject"]');
        
        if (currentScript && currentScript.src) {
            // Extrait le chemin du script et construit le chemin du footer
            const scriptSrc = currentScript.src;
            const scriptDir = scriptSrc.substring(0, scriptSrc.lastIndexOf('/'));
            return scriptDir + '/footer.html';
        }
        
        // Fallback: essaye plusieurs chemins possibles
        return '../../shared/footer.html'; // Pour _archived
    }
    
    /**
     * Charge et injecte le footer
     */
    async function injectFooter(targetElement) {
        const possiblePaths = [
            '../../shared/footer.html',  // Pour _archived
            '../shared/footer.html',      // Pour apps direct
            './shared/footer.html',       // Pour racine
            getFooterPath()               // Détection auto
        ];
        
        let footerHTML = null;
        let successPath = null;
        
        // Détecte si on est en file:// (nécessite XMLHttpRequest)
        const isFileProtocol = window.location.protocol === 'file:';
        
        // Essaye chaque chemin jusqu'à ce qu'un fonctionne
        for (const path of possiblePaths) {
            try {
                console.log('🔍 Trying footer path:', path);
                
                if (isFileProtocol) {
                    // XMLHttpRequest pour file:// (fetch bloqué par CORS)
                    footerHTML = await new Promise((resolve, reject) => {
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', path, true);
                        xhr.onload = () => {
                            if (xhr.status === 200 || xhr.status === 0) {
                                resolve(xhr.responseText);
                            } else {
                                reject();
                            }
                        };
                        xhr.onerror = reject;
                        xhr.send();
                    });
                } else {
                    // fetch pour http/https
                    const response = await fetch(path);
                    if (response.ok) {
                        footerHTML = await response.text();
                    }
                }
                
                if (footerHTML) {
                    successPath = path;
                    break;
                }
            } catch (error) {
                // Continue avec le prochain chemin
                footerHTML = null;
                continue;
            }
        }
        
        if (!footerHTML) {
            console.error('❌ Failed to load IAFactory Footer from any path');
            const serverHint = isFileProtocol ? '<p style="font-size:0.875rem;margin-top:0.5rem;color:#c00;">💡 Use local server: <code>python -m http.server 8000</code> or run START_SERVER.bat</p>' : '';
            targetElement.innerHTML = `<footer class="iaf-footer"><div style="text-align:center;padding:2rem;color:#ef4444;">
                <p>⚠️ Footer failed to load</p>
                <p style="font-size:0.875rem;margin-top:0.5rem;">Paths tried: ${possiblePaths.join(', ')}</p>
                ${serverHint}
            </div></footer>`;
            return;
        }
        
        try {
            targetElement.innerHTML = footerHTML;
            
            // Exécute les scripts du footer
            const scripts = targetElement.querySelectorAll('script');
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                document.body.appendChild(newScript);
                script.remove();
            });
            
            console.log('✅ IAFactory Footer loaded successfully from:', successPath);
        } catch (error) {
            console.error('❌ Error injecting footer:', error);
            targetElement.innerHTML = '<footer class="iaf-footer"><p style="text-align:center;padding:2rem;color:#ef4444;">Footer injection error</p></footer>';
        }
    }
    
    /**
     * Initialise le footer
     */
    function initFooter() {
        // Mode 1: Cherche les éléments avec data-iaf-footer
        const footerPlaceholders = document.querySelectorAll('[data-iaf-footer]');
        footerPlaceholders.forEach(placeholder => {
            injectFooter(placeholder);
        });
        
        // Mode 2: Auto-injection si data-iaf-footer-auto sur le script
        const currentScript = document.currentScript;
        if (currentScript && currentScript.hasAttribute('data-iaf-footer-auto')) {
            const autoPlaceholder = document.createElement('div');
            autoPlaceholder.setAttribute('data-iaf-footer', '');
            document.body.appendChild(autoPlaceholder);
            injectFooter(autoPlaceholder);
        }
    }
    
    // Attendre que le DOM soit prêt
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFooter);
    } else {
        initFooter();
    }
})();
