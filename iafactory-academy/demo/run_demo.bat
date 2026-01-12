@echo off
echo ========================================
echo    BBC School IA - Demo Ministre
echo    Lancement de l'interface Streamlit
echo ========================================
echo.

REM Activer l'environnement virtuel si existant
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Installer les dépendances si nécessaire
pip install -q streamlit pandas plotly

REM Lancer Streamlit
echo.
echo Ouverture du navigateur...
echo.
streamlit run minister_demo.py --server.port 8501 --browser.gatherUsageStats false

pause
