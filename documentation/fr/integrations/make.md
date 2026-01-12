# Intégration Make

## Introduction
Make est un outil d’automatisation qui permet d’intégrer l’API IAFactory dans vos workflows sans code. Cette page explique comment connecter IAFactory à Make, configurer vos scénarios et automatiser vos tâches IA.

## Prérequis
- Un compte IAFactory avec une clé API valide
- Un compte Make

## Démarrage rapide
1. Connectez-vous à Make et créez un nouveau scénario.
2. Ajoutez un module HTTP.
3. Configurez l’URL : `https://api.iafactory.com/v1/chat/completions`
4. Ajoutez les headers :
    - `Authorization: Bearer VOTRE_CLE_API`
    - `Content-Type: application/json`
5. Exemple de payload :
```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "Génère un résumé du projet IAFactory"}
  ]
}
```
6. Exécutez le scénario et récupérez la réponse IA.

## Exemple d’automatisation
- Génération automatique de rapports
- Analyse de texte en masse
- Envoi de réponses IA dans Slack, Email, etc.

## Conseils d’optimisation
- Utilisez le paramètre `temperature` pour ajuster la créativité des réponses
- Gérez les erreurs et quotas via les modules Make

## Ressources utiles
- [Documentation API IAFactory](https://iafactory.com/docs)
- [Tutoriel Make officiel](https://www.make.com/en/help)
- Support IAFactory : support@iafactory.com