#!/bin/bash

# BBC School Algeria - Script de Démarrage Automatique Final
# Automatise toutes les tâches de démarrage et vérification

clear
echo "🎓 BBC SCHOOL ALGERIA - DÉMARRAGE AUTOMATIQUE FINAL"
echo "=================================================="
echo ""

# 1. Vérification des prérequis
echo "🔧 Vérification des prérequis système..."
echo "======================================="

# Vérifier XAMPP
if pgrep -x "httpd" > /dev/null || pgrep -x "apache2" > /dev/null; then
    echo "✅ Apache est en cours d'exécution"
else
    echo "❌ Apache n'est pas démarré"
    echo "   Veuillez démarrer XAMPP Control Panel"
    read -p "Appuyez sur Entrée quand Apache sera démarré..."
fi

if pgrep -x "mysqld" > /dev/null; then
    echo "✅ MySQL est en cours d'exécution"
else
    echo "❌ MySQL n'est pas démarré"
    echo "   Veuillez démarrer MySQL dans XAMPP"
    read -p "Appuyez sur Entrée quand MySQL sera démarré..."
fi

echo ""

# 2. Test de connectivité
echo "🌐 Test de connectivité..."
echo "========================"

if curl -s http://localhost/onestschooled-test/public > /dev/null; then
    echo "✅ Site BBC School accessible"
else
    echo "❌ Site non accessible - Vérifiez XAMPP"
fi

echo ""

# 3. Ouverture automatique des liens
echo "🚀 Ouverture automatique des interfaces..."
echo "========================================="

# Détecter l'OS et ouvrir le navigateur approprié
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost/onestschooled-test/public
    open http://localhost/onestschooled-test/public/login
    open http://localhost/onestschooled-test/bbc-knowledge-test.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost/onestschooled-test/public
    xdg-open http://localhost/onestschooled-test/public/login
    xdg-open http://localhost/onestschooled-test/bbc-knowledge-test.html
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash/Cygwin)
    start http://localhost/onestschooled-test/public
    start http://localhost/onestschooled-test/public/login
    start http://localhost/onestschooled-test/bbc-knowledge-test.html
fi

echo "✅ Site public BBC School ouvert"
echo "✅ Interface d'administration ouverte"
echo "✅ Test chatbot IA ouvert"
echo ""

# 4. Informations de connexion
echo "🔐 INFORMATIONS DE CONNEXION"
echo "==========================="
echo "📧 Email admin : admin@onestschool.com"
echo "📧 Email alternatif : bensalemboualem@gmail.com"
echo "🔑 Mot de passe : [votre mot de passe admin]"
echo ""

# 5. Menu d'actions rapides
echo "📋 ACTIONS RAPIDES DISPONIBLES"
echo "=============================="
echo "1. 🌐 Ouvrir le site public"
echo "2. 🔐 Ouvrir l'administration"
echo "3. 🤖 Tester le chatbot IA"
echo "4. 📊 Voir les statistiques"
echo "5. 📖 Lire le guide complet"
echo "6. 🔄 Redémarrer les services"
echo "7. ❌ Quitter"
echo ""

while true; do
    read -p "Choisissez une action (1-7) : " choice
    case $choice in
        1)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open http://localhost/onestschooled-test/public
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open http://localhost/onestschooled-test/public
            else
                start http://localhost/onestschooled-test/public
            fi
            echo "✅ Site public ouvert"
            ;;
        2)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open http://localhost/onestschooled-test/public/login
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open http://localhost/onestschooled-test/public/login
            else
                start http://localhost/onestschooled-test/public/login
            fi
            echo "✅ Administration ouverte"
            ;;
        3)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open http://localhost/onestschooled-test/bbc-knowledge-test.html
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open http://localhost/onestschooled-test/bbc-knowledge-test.html
            else
                start http://localhost/onestschooled-test/bbc-knowledge-test.html
            fi
            echo "✅ Test chatbot ouvert"
            ;;
        4)
            echo ""
            echo "📊 STATISTIQUES BBC SCHOOL ALGERIA"
            echo "================================="
            echo "🎓 Étudiants : 804"
            echo "👨‍🏫 Enseignants : 45"
            echo "🏫 Salles de classe : 30"
            echo "📚 Matières : 272"
            echo "🚌 Véhicules transport : 5"
            echo "📰 Actualités publiées : 8+"
            echo "🎯 Taux de réussite BAC : 95%"
            echo ""
            ;;
        5)
            if [[ -f "BBC-SCHOOL-GUIDE-FINAL.md" ]]; then
                if command -v cat > /dev/null; then
                    echo ""
                    echo "📖 APERÇU DU GUIDE BBC SCHOOL"
                    echo "============================"
                    head -20 BBC-SCHOOL-GUIDE-FINAL.md
                    echo ""
                    echo "... (guide complet dans BBC-SCHOOL-GUIDE-FINAL.md)"
                    echo ""
                fi
            else
                echo "❌ Guide non trouvé"
            fi
            ;;
        6)
            echo "🔄 Redémarrage des services recommandé via XAMPP Control Panel"
            ;;
        7)
            echo ""
            echo "🎓 Merci d'avoir utilisé BBC School Algeria !"
            echo "🇩🇿 Excellence éducative garantie !"
            echo ""
            break
            ;;
        *)
            echo "❌ Choix invalide. Veuillez choisir entre 1 et 7."
            ;;
    esac
    echo ""
done

echo "👋 À bientôt sur BBC School Algeria !"