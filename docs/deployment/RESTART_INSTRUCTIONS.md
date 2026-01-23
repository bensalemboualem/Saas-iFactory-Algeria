# INSTRUCTIONS DE REDÉMARRAGE (RESTART)

**Date :** 13/01/2026
**État :** Nexus fonctionne en mode "Lite" (Backend sans base de données complexe).

## 1. Au redémarrage de Windows
1.  Oouvrez un terminal / CMD.
2.  Allez dans le dossier du projet :
    ```cmd
    cd D:\iafactorychatgpt
    ```
3.  Lancez le script de démarrage unique :
    ```cmd
    start-nexus.bat
    ```

## 2. Ce qui va se passer
- Le script va **nettoyer** automatiquement les ports (5173, 5174, 8181).
- Il va lancer :
    - **App (Bolt)** sur `http://localhost:5174`
    - **Backend (Lite)** sur `http://localhost:8181`
- La **Landing Page** sera accessible via le bouton "Sortir" de l'app.

## 3. Prochaine Étape
- Si vous avez installé **Visual Studio Build Tools** pendant le redémarrage, dites-le moi ! Je pourrai réactiver le mode "Complet" (avec Base de Données et PDF parsing).
- Sinon, on continue le développement des fonctionnalités d'équipe sur le mode Lite.

**Bon redémarrage !** 🚀
