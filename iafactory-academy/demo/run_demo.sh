#!/bin/bash

echo "========================================"
echo "   BBC School IA - Demo Ministre"
echo "   Lancement de l'interface Streamlit"
echo "========================================"
echo

# Activer l'environnement virtuel si existant
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Installer les dépendances si nécessaire
pip install -q streamlit pandas plotly

# Lancer Streamlit
echo
echo "Ouverture du navigateur..."
echo
streamlit run minister_demo.py --server.port 8501 --browser.gatherUsageStats false
