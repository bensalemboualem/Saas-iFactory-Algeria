# Modèles et Tarifs

## Tableau des Prix

| Modèle | Entrée ($/M tokens) | Sortie ($/M tokens) |
|--------|--------------------|--------------------|
| gpt-5.2-chat | 1,75 | 14 |
| gpt-5.1-chat | 1,25 | 10 |
| gpt-5-mini | 0,25 | 2 |
| gpt-4.1 | 2 | 8 |
| gpt-4.1-mini | 0.4 | 1.6 |
| gpt-4.1-nano | 0.1 | 0.4 |
| gpt-4o | 2.5 | 10 |
| mistral-large-3 | 0.5 | 1.5 |
| mistral-medium-3.1 | 0.4 | 2 |
| mistral-small-3.2-24b-instruct | 0.1 | 0.3 |
| magistral-medium-2506 | 2 | 5 |
| codestral-2508 | 0.3 | 0.9 |
| grok-4 | 3 | 15 |
| grok-4-fast | 0.2 | 0.5 |
| grok-code-fast-1 | 0.2 | 1.5 |
| gemini-2.5-flash | 0.3 | 2.5 |
| gemini-3-pro | 2.5 | 15 |
| deepseek-r1-0528 | 3 | 8 |
| deepseek-v3.2 | 0.30 | 0.45 |
| kimi-k2-instruct | 0.4 | 2 |
| kimi-k2-thinking | 0.45 | 2.35 |
| qwen3-coder | 0.5 | 2 |
| qwen3-coder-flash | 0.5 | 2.5 |
| qwen3-coder-plus | 1.8 | 9 |
| llama-4-maverick | 0.22 | 0.88 |
| llama-4-scout | 0.15 | 0.6 |
| sonar-pro | 3 | 15 |
| sonar-deep-research | 2 | 8 |
| claude-haiku-4-5 | 0.8 | 4 |
| claude-opus-4-5 | 5 | 25 |
| claude-sonnet-4-5 | 3 | 15 |

⚠️ **Note :** Les prix peuvent varier et ne pas être à jour dans ce tableau.

## Alias de Modèles

💡 Nous avons ajouté des alias alignés avec l'app IAFactory pour faciliter la sélection de modèles :

- `mistral` → utilise `mistral-medium-3.1` automatiquement
- `gpt-4` → utilise `gpt-4.1` automatiquement
- `claude` → utilise `claude-sonnet-4-5` automatiquement

## Suivi de l'Utilisation

📜 L'utilisation et les coûts sont loggés dans vos [paramètres API](https://dashboard.iafactory-algeria.com/api/usage).

## Catégories de Modèles

### 🚀 Modèles Rapides
- **gpt-4.1-nano** : Ultra rapide, idéal pour les tâches simples
- **mistral-small-3.2-24b-instruct** : Bon rapport qualité/prix
- **llama-4-scout** : Open-source, performant

### 💎 Modèles Premium
- **gpt-5.2-chat** : Meilleure qualité, raisonnement avancé
- **claude-opus-4-5** : Excellence en analyse et créativité
- **grok-4** : Performance exceptionnelle

### 💻 Modèles de Code
- **codestral-2508** : Spécialisé en programmation
- **qwen3-coder-plus** : Code multilingue
- **grok-code-fast-1** : Génération rapide de code

### 🔬 Modèles de Recherche
- **deepseek-r1-0528** : Raisonnement profond
- **sonar-deep-research** : Analyse approfondie
- **kimi-k2-thinking** : Pensée structurée

## Recommandations

### Pour le Chat Général
✅ **gpt-4.1** : Meilleur équilibre qualité/prix
✅ **claude-sonnet-4-5** : Excellent pour les conversations longues

### Pour le Code
✅ **codestral-2508** : Spécialisé programmation
✅ **qwen3-coder** : Polyvalent et efficace

### Pour les Tâches Rapides
✅ **gpt-4.1-mini** : Rapide et économique
✅ **mistral-small-3.2-24b-instruct** : Très bon rapport qualité/prix

### Pour les Tâches Complexes
✅ **gpt-5.2-chat** : Maximum de capacités
✅ **claude-opus-4-5** : Raisonnement avancé

## Calculateur de Coûts

Exemple de calcul pour 1 million de tokens :

**Requête :** 100,000 tokens d'entrée + 50,000 tokens de sortie

Avec **gpt-4.1** :
- Entrée : 100,000 × $2 / 1M = $0.20
- Sortie : 50,000 × $8 / 1M = $0.40
- **Total : $0.60**

Avec **gpt-4.1-mini** :
- Entrée : 100,000 × $0.4 / 1M = $0.04
- Sortie : 50,000 × $1.6 / 1M = $0.08
- **Total : $0.12**

---

[← Retour au Démarrage Rapide](./quick-start.md) | [Paramètres →](./parameters.md)
