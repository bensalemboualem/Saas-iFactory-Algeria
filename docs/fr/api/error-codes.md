# Codes d'Erreur

## Vue d'Ensemble

L'API IAFactory Algeria utilise des codes de statut HTTP standard pour indiquer le succès ou l'échec des requêtes.

## Codes de Statut

| Code | Signification | Description |
|------|--------------|-------------|
| 200 | OK | Requête réussie |
| 400 | Bad Request | Requête incorrecte - Paramètres manquants ou invalides |
| 401 | Unauthorized | Non autorisé - Clé API invalide ou manquante |
| 403 | Forbidden | Interdit - Accès refusé ou quota dépassé |
| 404 | Not Found | Non trouvé - Endpoint ou ressource inexistante |
| 429 | Too Many Requests | Trop de requêtes - Limite de débit dépassée |
| 500 | Internal Server Error | Erreur serveur interne |
| 503 | Service Unavailable | Service indisponible temporairement |

## Format des Erreurs

Toutes les erreurs retournent un objet JSON avec la structure suivante :

```json
{
  "error": {
    "message": "Description de l'erreur",
    "type": "type_erreur",
    "code": "code_erreur",
    "param": "paramètre_concerné"
  }
}
```

## Erreurs Détaillées

### 400 Bad Request

**Causes communes :**
- Paramètres manquants
- Format JSON invalide
- Valeurs hors limites

**Exemples :**

```json
{
  "error": {
    "message": "Le paramètre 'messages' est requis",
    "type": "invalid_request_error",
    "code": "missing_parameter",
    "param": "messages"
  }
}
```

```json
{
  "error": {
    "message": "La valeur de 'temperature' doit être entre 0 et 2",
    "type": "invalid_request_error",
    "code": "invalid_value",
    "param": "temperature"
  }
}
```

**Solution :**
Vérifiez la structure de votre requête et assurez-vous que tous les paramètres requis sont présents et valides.

### 401 Unauthorized

**Causes communes :**
- Clé API invalide
- Clé API expirée
- En-tête Authorization manquant

**Exemple :**

```json
{
  "error": {
    "message": "Clé API invalide",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

**Solution :**
1. Vérifiez que votre clé API est correcte
2. Assurez-vous d'inclure l'en-tête `Authorization: Bearer VOTRE_CLE`
3. Générez une nouvelle clé si nécessaire

### 403 Forbidden

**Causes communes :**
- Permissions insuffisantes
- Quota dépassé
- Modèle non autorisé pour votre plan

**Exemples :**

```json
{
  "error": {
    "message": "Quota mensuel dépassé",
    "type": "quota_error",
    "code": "quota_exceeded"
  }
}
```

```json
{
  "error": {
    "message": "Modèle non disponible pour votre plan",
    "type": "permission_error",
    "code": "model_not_available"
  }
}
```

**Solution :**
- Vérifiez votre usage dans le dashboard
- Mettez à niveau votre plan
- Utilisez un modèle disponible pour votre plan

### 404 Not Found

**Causes communes :**
- Endpoint incorrect
- Modèle inexistant
- Ressource supprimée

**Exemple :**

```json
{
  "error": {
    "message": "Modèle 'gpt-99' non trouvé",
    "type": "not_found_error",
    "code": "model_not_found"
  }
}
```

**Solution :**
- Vérifiez l'URL de l'endpoint
- Consultez la liste des modèles disponibles
- Utilisez un modèle existant

### 429 Too Many Requests

**Causes communes :**
- Dépassement de la limite de requêtes par minute
- Dépassement de la limite de tokens par minute

**Exemple :**

```json
{
  "error": {
    "message": "Limite de débit dépassée. Réessayez dans 60 secondes",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

**En-têtes de réponse :**

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1234567890
Retry-After: 60
```

**Solution :**
- Attendez avant de refaire une requête
- Implémentez un système de retry avec backoff exponentiel
- Mettez à niveau vers un plan avec des limites plus élevées

### 500 Internal Server Error

**Causes communes :**
- Problème côté serveur
- Erreur inattendue

**Exemple :**

```json
{
  "error": {
    "message": "Une erreur interne s'est produite",
    "type": "server_error",
    "code": "internal_error"
  }
}
```

**Solution :**
- Réessayez la requête
- Si le problème persiste, contactez le support
- Vérifiez le statut sur status.iafactory-algeria.com

### 503 Service Unavailable

**Causes communes :**
- Maintenance planifiée
- Surcharge du serveur

**Exemple :**

```json
{
  "error": {
    "message": "Service temporairement indisponible",
    "type": "service_unavailable_error",
    "code": "service_unavailable"
  }
}
```

**Solution :**
- Attendez quelques minutes
- Réessayez avec un backoff exponentiel
- Consultez status.iafactory-algeria.com

## Gestion des Erreurs

### Python

```python
import requests
import time

def make_request_with_retry(url, headers, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limit atteint. Attente de {retry_after}s...")
                time.sleep(retry_after)
                
            elif response.status_code >= 500:
                wait_time = 2 ** attempt  # Backoff exponentiel
                print(f"Erreur serveur. Réessai dans {wait_time}s...")
                time.sleep(wait_time)
                
            else:
                error = response.json()
                print(f"Erreur: {error['error']['message']}")
                return None
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            
    return None
```

### JavaScript

```javascript
async function makeRequestWithRetry(url, headers, data, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                return await response.json();
            }
            
            if (response.status === 429) {
                const retryAfter = response.headers.get('Retry-After') || 60;
                console.log(`Rate limit atteint. Attente de ${retryAfter}s...`);
                await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
                continue;
            }
            
            if (response.status >= 500) {
                const waitTime = Math.pow(2, attempt) * 1000;
                console.log(`Erreur serveur. Réessai dans ${waitTime/1000}s...`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
                continue;
            }
            
            const error = await response.json();
            console.error('Erreur:', error.error.message);
            return null;
            
        } catch (e) {
            console.error('Exception:', e);
        }
    }
    
    return null;
}
```

## Codes d'Erreur Spécifiques

| Code | Description |
|------|-------------|
| `missing_parameter` | Paramètre requis manquant |
| `invalid_value` | Valeur de paramètre invalide |
| `invalid_api_key` | Clé API invalide |
| `expired_api_key` | Clé API expirée |
| `quota_exceeded` | Quota dépassé |
| `rate_limit_exceeded` | Limite de débit dépassée |
| `model_not_found` | Modèle non trouvé |
| `model_not_available` | Modèle non disponible pour votre plan |
| `context_length_exceeded` | Contexte trop long |
| `internal_error` | Erreur interne |
| `service_unavailable` | Service indisponible |

## Monitoring et Alertes

### Bonnes Pratiques

1. **Loggez toutes les erreurs**
   ```python
   import logging
   
   logging.error(f"API Error: {error['error']['code']} - {error['error']['message']}")
   ```

2. **Implémentez des métriques**
   - Taux d'erreur par type
   - Temps de réponse
   - Nombre de retries

3. **Configurez des alertes**
   - Quota proche de la limite
   - Taux d'erreur élevé
   - Latence élevée

4. **Utilisez le dashboard**
   - Consultez https://dashboard.iafactory-algeria.com/usage
   - Surveillez votre consommation
   - Configurez des limites

## Support

Si vous rencontrez des erreurs persistantes :

- 📧 Email : support@iafactory-algeria.com
- 💬 Discord : [Rejoindre notre serveur](https://discord.gg/iafactory)
- 📊 Status : [status.iafactory-algeria.com](https://status.iafactory-algeria.com)

---

[← Paramètres](./parameters.md) | [Migration OpenAI →](./migration-openai.md)
