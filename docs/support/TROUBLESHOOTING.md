# Guide de Dépannage / Troubleshooting Guide

**IAFACTORY - Résolution des Problèmes Courants**

*Dernière mise à jour : 19 janvier 2026*

---

## Table des matières

1. [Problèmes de connexion](#1-problèmes-de-connexion)
2. [Problèmes de performance](#2-problèmes-de-performance)
3. [Erreurs IA](#3-erreurs-ia)
4. [Problèmes de paiement](#4-problèmes-de-paiement)
5. [Problèmes API](#5-problèmes-api)
6. [Problèmes mobile/desktop](#6-problèmes-mobiledesktop)
7. [Codes d'erreur](#7-codes-derreur)

---

## 1. Problèmes de connexion

### 1.1 Impossible de se connecter

**Symptômes :**
- Page de login qui recharge en boucle
- Message "Identifiants incorrects"
- Écran blanc après login

**Solutions :**

1. **Vérifier les identifiants**
   ```
   - Email correct (vérifier les espaces)
   - Mot de passe sensible à la casse
   ```

2. **Vider le cache du navigateur**
   ```
   Chrome: Ctrl+Shift+Delete > Tout le temps > Vider
   Firefox: Ctrl+Shift+Delete > Tout > Effacer
   Safari: Cmd+Alt+E
   ```

3. **Désactiver les extensions**
   - AdBlockers peuvent bloquer les requêtes
   - VPN/Proxy peuvent causer des problèmes

4. **Essayer en navigation privée**
   ```
   Chrome: Ctrl+Shift+N
   Firefox: Ctrl+Shift+P
   ```

5. **Réinitialiser le mot de passe**
   - [Lien de réinitialisation](https://app.iafactory.ai/forgot-password)

### 1.2 Session expirée fréquemment

**Cause possible :** Cookies bloqués ou supprimés automatiquement

**Solution :**
1. Autoriser les cookies pour `*.iafactory.ai`
2. Vérifier que le navigateur ne supprime pas les cookies à la fermeture
3. Désactiver les extensions de nettoyage automatique

### 1.3 Erreur "Trop de tentatives"

**Solution :**
- Attendre 15 minutes
- Utiliser "Mot de passe oublié" si besoin
- Contacter le support si le problème persiste

---

## 2. Problèmes de performance

### 2.1 Interface lente

**Diagnostic :**

```javascript
// Ouvrir la console (F12) et exécuter :
performance.now()
// Puis après navigation :
performance.now()
// Différence > 3000ms = problème
```

**Solutions :**

1. **Vérifier la connexion internet**
   ```bash
   # Test de latence
   ping api.iafactory.ai
   ```

2. **Réduire les conversations actives**
   - Archiver les anciennes conversations
   - Limiter à 20 conversations visibles

3. **Mettre à jour le navigateur**
   - Chrome, Firefox, Safari dernière version

4. **Désactiver les animations (accessibilité)**
   ```
   Paramètres > Accessibilité > Réduire les animations
   ```

### 2.2 Chargement des messages lent

**Causes possibles :**
- Conversation avec beaucoup de messages (>100)
- Messages avec images/fichiers volumineux

**Solutions :**
1. Créer une nouvelle conversation
2. Exporter et archiver l'ancienne
3. Activer "Chargement progressif" dans les paramètres

### 2.3 Mémoire élevée

**Symptôme :** Navigateur qui consomme > 2GB de RAM

**Solutions :**
1. Fermer les onglets inutiles
2. Recharger la page (F5)
3. Utiliser l'application desktop (plus optimisée)

---

## 3. Erreurs IA

### 3.1 "Erreur de génération"

**Code : `AI_GENERATION_ERROR`**

**Causes et solutions :**

| Cause | Solution |
|-------|----------|
| Serveur IA surchargé | Réessayer dans 1 minute |
| Prompt trop long | Réduire à < 4000 tokens |
| Contenu filtré | Reformuler sans termes sensibles |
| Timeout | Diviser la demande en parties |

### 3.2 "Modèle non disponible"

**Code : `MODEL_UNAVAILABLE`**

**Solutions :**
1. Vérifier le statut : [status.iafactory.ai](https://status.iafactory.ai)
2. Essayer un autre modèle
3. Attendre la maintenance (généralement < 1h)

### 3.3 Réponse tronquée

**Symptôme :** La réponse s'arrête brusquement

**Causes :**
- Limite de tokens atteinte
- Timeout de génération

**Solutions :**
1. Demander "Continue" ou "Suite"
2. Augmenter la limite de tokens (Paramètres > Modèle)
3. Demander une réponse plus courte

### 3.4 Réponse incorrecte / Hallucinations

**L'IA peut parfois :**
- Inventer des faits
- Donner des infos obsolètes
- Se contredire

**Bonnes pratiques :**
1. Toujours vérifier les informations importantes
2. Demander des sources
3. Reformuler avec plus de contexte
4. Utiliser un modèle plus récent (GPT-4, Claude 3)

---

## 4. Problèmes de paiement

### 4.1 Paiement refusé

**Chargily Pay (Algérie) :**

| Erreur | Solution |
|--------|----------|
| Carte non reconnue | Vérifier CIB/EDAHABIA activée pour e-commerce |
| Solde insuffisant | Vérifier le solde bancaire |
| Limite atteinte | Contacter votre banque |
| Code OTP invalide | Demander un nouveau code |

**Carte internationale :**

| Erreur | Solution |
|--------|----------|
| 3D Secure échoué | Autoriser les transactions en ligne |
| Carte expirée | Mettre à jour les infos de carte |
| Adresse invalide | Utiliser l'adresse de facturation exacte |

### 4.2 Abonnement non activé

**Après paiement réussi mais pas de crédits :**

1. Attendre 5 minutes (synchronisation)
2. Déconnexion/Reconnexion
3. Vérifier dans Paramètres > Facturation
4. Contacter support avec le reçu de paiement

### 4.3 Facturation erronée

**Procédure :**
1. Télécharger la facture concernée
2. Envoyer à billing@iafactory.ai avec :
   - Numéro de facture
   - Description du problème
   - Montant attendu vs facturé
3. Délai de traitement : 5 jours ouvrés

---

## 5. Problèmes API

### 5.1 Erreur 401 Unauthorized

```json
{
  "error": "unauthorized",
  "message": "Invalid API key"
}
```

**Solutions :**
1. Vérifier que la clé API est correcte
2. Vérifier qu'elle n'a pas été révoquée
3. Régénérer une nouvelle clé si nécessaire

### 5.2 Erreur 429 Too Many Requests

```json
{
  "error": "rate_limited",
  "message": "Too many requests",
  "retry_after": 60
}
```

**Solutions :**
1. Implémenter un backoff exponentiel
2. Respecter les limites de votre plan
3. Upgrader si besoin de plus de requêtes

**Limites par plan :**

| Plan | Requêtes/minute |
|------|-----------------|
| Free | 10 |
| Pro | 60 |
| Pro+ | 300 |
| Enterprise | Custom |

### 5.3 Erreur 500 Internal Server Error

```json
{
  "error": "internal_error",
  "message": "Something went wrong",
  "request_id": "req_abc123"
}
```

**Actions :**
1. Réessayer la requête
2. Vérifier status.iafactory.ai
3. Si persistant, contacter support avec `request_id`

### 5.4 Timeouts

**Symptôme :** Requête qui n'aboutit pas

**Solutions :**
1. Augmenter le timeout client (recommandé : 120s pour génération)
2. Utiliser le streaming pour les longues réponses
3. Diviser les requêtes volumineuses

```typescript
// Exemple avec streaming
const response = await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ stream: true, ... }),
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // Process chunk
}
```

---

## 6. Problèmes mobile/desktop

### 6.1 Application desktop - Écran blanc

**Windows :**
```bash
# Supprimer le cache
rmdir /s /q "%APPDATA%\iafactory"
# Relancer l'application
```

**macOS :**
```bash
rm -rf ~/Library/Application\ Support/iafactory
rm -rf ~/Library/Caches/iafactory
```

**Linux :**
```bash
rm -rf ~/.config/iafactory
rm -rf ~/.cache/iafactory
```

### 6.2 Application desktop - Ne démarre pas

**Solutions :**
1. Vérifier les prérequis système
   - Windows 10+ / macOS 10.15+ / Ubuntu 20.04+
   - 4GB RAM minimum
2. Exécuter en tant qu'administrateur (Windows)
3. Réinstaller l'application

### 6.3 Synchronisation entre appareils

**Symptôme :** Conversations différentes sur web et desktop

**Solutions :**
1. Vérifier la connexion internet sur les deux appareils
2. Forcer la synchronisation : Paramètres > Données > Synchroniser
3. Se déconnecter/reconnecter

---

## 7. Codes d'erreur

### Référence rapide

| Code | Description | Solution rapide |
|------|-------------|-----------------|
| `AUTH_001` | Token expiré | Reconnexion |
| `AUTH_002` | Compte désactivé | Contacter support |
| `AUTH_003` | 2FA requis | Entrer le code 2FA |
| `CRED_001` | Crédits insuffisants | Acheter des crédits |
| `CRED_002` | Limite quotidienne | Attendre 24h ou upgrader |
| `AI_001` | Modèle indisponible | Essayer autre modèle |
| `AI_002` | Prompt trop long | Raccourcir le prompt |
| `AI_003` | Contenu filtré | Reformuler la demande |
| `AI_004` | Timeout génération | Réessayer ou diviser |
| `API_001` | Clé invalide | Vérifier/régénérer clé |
| `API_002` | Rate limit | Attendre ou upgrader |
| `API_003` | Endpoint non trouvé | Vérifier l'URL |
| `PAY_001` | Paiement refusé | Vérifier carte/compte |
| `PAY_002` | Abonnement expiré | Renouveler |
| `FILE_001` | Fichier trop volumineux | Réduire la taille |
| `FILE_002` | Format non supporté | Convertir le fichier |

---

## 8. Diagnostic avancé

### 8.1 Collecter les informations de debug

Ouvrez la console (F12) et exécutez :

```javascript
// Copier ces infos pour le support
console.log({
  userAgent: navigator.userAgent,
  platform: navigator.platform,
  language: navigator.language,
  cookies: navigator.cookieEnabled,
  localStorage: typeof localStorage !== 'undefined',
  online: navigator.onLine,
  memory: navigator.deviceMemory,
});
```

### 8.2 Exporter les logs

**Dans l'application :**
1. Paramètres > Avancé > Exporter les logs
2. Fichier `iafactory-logs-YYYYMMDD.zip` téléchargé

### 8.3 Vérifier la connectivité

```bash
# Test API
curl -I https://api.iafactory.ai/health

# Test WebSocket
wscat -c wss://ws.iafactory.ai/connect
```

---

## Contact Support

Si le problème persiste après avoir essayé ces solutions :

- **Email** : support@iafactory.ai
- **Chat en direct** : app.iafactory.ai (Pro+ et Enterprise)
- **Discord** : discord.gg/iafactory

**Informations à fournir :**
1. Description du problème
2. Étapes pour reproduire
3. Code d'erreur (si applicable)
4. Captures d'écran
5. Navigateur/OS/Version de l'app
6. Résultat du diagnostic (section 8.1)

---

*Ce guide est mis à jour régulièrement. Dernière révision : 19 janvier 2026*
