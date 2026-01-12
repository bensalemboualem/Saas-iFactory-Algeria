# Gestion des clés API

La sécurité des clés API est essentielle pour protéger l’accès à vos services IAFactory.

## Générer une clé API
- Connectez-vous à votre espace utilisateur IAFactory
- Accédez à la section « Clés API »
- Cliquez sur « Générer une nouvelle clé »
- Copiez et stockez la clé dans un endroit sécurisé

## Bonnes pratiques
- Ne partagez jamais votre clé API publiquement
- Ne stockez pas la clé dans un dépôt git ou un code source accessible
- Utilisez des variables d’environnement pour injecter la clé côté serveur
- Révoquez immédiatement toute clé compromise

## Rotation des clés
- Changez régulièrement vos clés API
- Supprimez les anciennes clés inutilisées

## Exemple d’utilisation
```bash
export API_KEY=VOTRE_CLE_API
curl -H "Authorization: Bearer $API_KEY" https://api.iafactory.dz/v1/endpoint
```

Pour toute question ou problème de sécurité, contactez support@iafactory.dz