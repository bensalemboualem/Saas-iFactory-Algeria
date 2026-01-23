# Authentification

## Vue d'Ensemble

L'API IAFactory Algeria utilise des clés API pour l'authentification. Toutes les requêtes doivent inclure votre clé API dans l'en-tête `Authorization`.

## Obtenir une Clé API

### 1. Créer un Compte

1. Allez sur [dashboard.iafactory-algeria.com](https://dashboard.iafactory-algeria.com)
2. Cliquez sur **S'inscrire**
3. Remplissez le formulaire d'inscription
4. Vérifiez votre email

### 2. Générer une Clé

1. Connectez-vous au dashboard
2. Allez dans **Paramètres** → **Clés API**
3. Cliquez sur **Créer une nouvelle clé**
4. Donnez un nom à votre clé
5. Sélectionnez les permissions
6. Cliquez sur **Générer**

⚠️ **Important :** Copiez et sauvegardez votre clé immédiatement. Elle ne sera plus visible après.

## Utilisation de la Clé API

### En-tête HTTP

```http
Authorization: Bearer sk_test_abc123xyz789
```

### Exemples

#### cURL

```bash
curl https://api.iafactory-algeria.com/v1/models \
  -H "Authorization: Bearer VOTRE_CLE_API"
```

#### JavaScript

```javascript
const headers = {
  'Authorization': 'Bearer VOTRE_CLE_API',
  'Content-Type': 'application/json'
};

fetch('https://api.iafactory-algeria.com/v1/models', { headers })
  .then(res => res.json())
  .then(console.log);
```

#### Python

```python
import requests

headers = {
    'Authorization': 'Bearer VOTRE_CLE_API',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.iafactory-algeria.com/v1/models',
    headers=headers
)
print(response.json())
```

## Types de Clés

### Clés de Test

- Préfixe : `sk_test_`
- Environnement : Test/Development
- Modèles limités
- Pas de facturation

### Clés de Production

- Préfixe : `sk_live_`
- Environnement : Production
- Tous les modèles disponibles
- Facturation active

## Permissions

Vous pouvez définir des permissions granulaires :

- ✅ **Lecture** : Lister les modèles, voir l'utilisation
- ✅ **Écriture** : Créer des completions, embeddings
- ✅ **Administration** : Gérer les clés, équipes, facturation

## Sécurité des Clés

### ✅ Bonnes Pratiques

1. **Ne jamais exposer vos clés**
   - ❌ Ne les committez pas dans Git
   - ❌ Ne les partagez pas publiquement
   - ❌ Ne les incluez pas côté client

2. **Utiliser des variables d'environnement**
   ```bash
   # .env
   IAFACTORY_API_KEY=sk_live_abc123
   ```

3. **Rotation régulière**
   - Changez vos clés tous les 90 jours
   - Utilisez plusieurs clés pour différents services

4. **Monitoring**
   - Surveillez l'utilisation dans le dashboard
   - Configurez des alertes

### 🔐 Stockage Sécurisé

#### Variables d'Environnement

```bash
# Linux/Mac
export IAFACTORY_API_KEY="sk_live_abc123"

# Windows
set IAFACTORY_API_KEY=sk_live_abc123
```

#### Fichiers de Configuration

```javascript
// config.js
require('dotenv').config();

module.exports = {
  apiKey: process.env.IAFACTORY_API_KEY
};
```

#### Gestionnaires de Secrets

- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Kubernetes Secrets

## Révoquer une Clé

### Via le Dashboard

1. Allez dans **Paramètres** → **Clés API**
2. Trouvez la clé à révoquer
3. Cliquez sur **Révoquer**
4. Confirmez l'action

### Via l'API

```bash
curl -X DELETE https://api.iafactory-algeria.com/v1/api-keys/sk_live_abc123 \
  -H "Authorization: Bearer VOTRE_CLE_ADMIN"
```

## Erreurs d'Authentification

### 401 Unauthorized

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

**Causes possibles :**
- Clé API invalide ou expirée
- Clé révoquée
- En-tête manquant ou mal formaté

### 403 Forbidden

```json
{
  "error": {
    "message": "Insufficient permissions",
    "type": "permission_error",
    "code": "insufficient_permissions"
  }
}
```

**Causes possibles :**
- Permissions insuffisantes
- Endpoint non autorisé pour ce plan
- Limite de quota atteinte

## Support

Besoin d'aide avec l'authentification ?
- 📧 security@iafactory-algeria.com
- 💬 [Discord Support](https://discord.gg/iafactory)
