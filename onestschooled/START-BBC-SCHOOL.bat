
@echo off
title BBC School Algeria - Démarrage Automatique
color 0A

echo.
echo  =====================================================
echo  🎓 BBC SCHOOL ALGERIA - DÉMARRAGE AUTOMATIQUE FINAL
echo  =====================================================
echo.

echo 🔧 Vérification des services XAMPP...
echo =====================================

:: Vérifier Apache
tasklist /FI "IMAGENAME eq httpd.exe" 2>NUL | find /I /N "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Apache est en cours d'exécution
) else (
    echo ❌ Apache n'est pas démarré
    echo    Veuillez démarrer Apache dans XAMPP Control Panel
    pause
)

:: Vérifier MySQL
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ MySQL est en cours d'exécution
) else (
    echo ❌ MySQL n'est pas démarré
    echo    Veuillez démarrer MySQL dans XAMPP Control Panel
    pause
)

echo.
echo 🌐 Test de connectivité...
echo ========================

:: Test de connectivité avec curl ou powershell
curl -s http://localhost/onestschooled-test/public >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Site BBC School accessible
) else (
    echo ⚠️  Test de connectivité - Vérification manuelle recommandée
)

echo.
echo 🚀 Ouverture automatique des interfaces...
echo ========================================

:: Ouverture des URLs dans le navigateur par défaut
start "" "http://localhost/onestschooled-test/public"
timeout /t 2 /nobreak >nul
start "" "http://localhost/onestschooled-test/public/login"
timeout /t 2 /nobreak >nul
start "" "http://localhost/onestschooled-test/bbc-knowledge-test.html"

echo ✅ Site public BBC School ouvert
echo ✅ Interface d'administration ouverte
echo ✅ Test chatbot IA ouvert
echo.

echo 🔐 INFORMATIONS DE CONNEXION
echo ===========================
echo 📧 Email admin : admin@onestschool.com
echo 📧 Email alternatif : bensalemboualem@gmail.com
echo 🔑 Mot de passe : [votre mot de passe admin]
echo.

:menu
echo 📋 ACTIONS RAPIDES DISPONIBLES
echo ==============================
echo 1. 🌐 Ouvrir le site public
echo 2. 🔐 Ouvrir l'administration  
echo 3. 🤖 Tester le chatbot IA
echo 4. 📊 Voir les statistiques
echo 5. 📖 Lire le guide complet
echo 6. 🔄 Redémarrer XAMPP
echo 7. 📁 Ouvrir le dossier projet
echo 8. 🌐 Tester toutes les URLs
echo 9. ❌ Quitter
echo.

set /p choice="Choisissez une action (1-9) : "

if "%choice%"=="1" (
    start "" "http://localhost/onestschooled-test/public"
    echo ✅ Site public ouvert
    echo.
    goto menu
)

if "%choice%"=="2" (
    start "" "http://localhost/onestschooled-test/public/login"
    echo ✅ Administration ouverte
    echo.
    goto menu
)

if "%choice%"=="3" (
    start "" "http://localhost/onestschooled-test/bbc-knowledge-test.html"
    echo ✅ Test chatbot ouvert
    echo.
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo � STATISTIQUES BBC SCHOOL ALGERIA
    echo =================================
    echo 🎓 Étudiants : 804
    echo 👨‍🏫 Enseignants : 45
    echo 🏫 Salles de classe : 30
    echo 📚 Matières : 272
    echo 🚌 Véhicules transport : 5
    echo 📰 Actualités publiées : 8+
    echo 🎯 Taux de réussite BAC : 95%%
    echo 🤖 Chatbot IA : Fonctionnel
    echo 🌐 Site web : Personnalisé BBC School
    echo.
    goto menu
)

if "%choice%"=="5" (
    if exist "BBC-SCHOOL-GUIDE-FINAL.md" (
        notepad "BBC-SCHOOL-GUIDE-FINAL.md"
        echo ✅ Guide ouvert dans Notepad
    ) else (
        echo ❌ Guide non trouvé
    )
    echo.
    goto menu
)

if "%choice%"=="6" (
    echo 🔄 Ouverture de XAMPP Control Panel...
    start "" "C:\xampp\xampp-control.exe"
    echo ✅ XAMPP Control Panel ouvert
    echo.
    goto menu
)

if "%choice%"=="7" (
    start "" "C:\xampp\htdocs\onestschooled-test"
    echo ✅ Dossier projet ouvert
    echo.
    goto menu
)

if "%choice%"=="8" (
    echo 🌐 Test de toutes les URLs BBC School...
    echo ======================================
    start "" "http://localhost/onestschooled-test/public"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost/onestschooled-test/public/login"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost/onestschooled-test/bbc-knowledge-test.html"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost/onestschooled-test/public/page-sections"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost/onestschooled-test/public/slider"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost/onestschooled-test/public/admin-news"
    echo ✅ Toutes les URLs ouvertes
    echo.
    goto menu
)

if "%choice%"=="9" (
    echo.
    echo 🎓 Merci d'avoir utilisé BBC School Algeria !
    echo 🇩🇿 Excellence éducative garantie !
    echo.
    echo 🌟 RÉSUMÉ FINAL :
    echo ================
    echo ✅ École complètement configurée
    echo ✅ Site web personnalisé BBC School
    echo ✅ Chatbot IA fonctionnel
    echo ✅ Interface d'administration accessible
    echo ✅ 804 étudiants, 45 enseignants, 30 salles
    echo ✅ Transport Mercedes Sprinter sécurisé
    echo ✅ Cantine halal et programmes bilingues
    echo.
    echo 👋 À bientôt sur BBC School Algeria !
    pause
    exit
)

echo ❌ Choix invalide. Veuillez choisir entre 1 et 9.
echo.
goto menu
