# MIGRATION APPS VERS GATEWAY

## Fait
- gateway_helper.py créé et copié
- Academy : 3 fichiers identifiés
- AI-Tools : fichiers identifiés
- Video : fichiers identifiés

## Utilisation
\\\python
from app.gateway_helper import call_llm_sync

response = call_llm_sync(
    model="gpt-3.5-turbo",
    messages=[{"role":"user","content":"Hello"}]
)
\\\

## Prochaine étape
Remplacer appels dans les fichiers identifiés
