# Paramètres de l'API

## Paramètres Requis

| Paramètre | Type | Description |
|-----------|------|-------------|
| `messages` | array | Liste des messages dans la conversation |
| `model` | string | Identificateur du modèle à utiliser |

## Paramètres Optionnels

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `temperature` | number | 0.7 | Contrôle la créativité (0.0 à 2.0) |
| `max_tokens` | integer | 2048 | Nombre maximum de tokens à générer |
| `top_p` | number | 1.0 | Contrôle la diversité des réponses (nucleus sampling) |
| `stream` | boolean | false | Active le streaming de réponse en temps réel |
| `frequency_penalty` | number | 0 | Pénalité pour les tokens fréquents (-2.0 à 2.0) |
| `presence_penalty` | number | 0 | Pénalité pour les nouveaux tokens (-2.0 à 2.0) |
| `stop` | string/array | null | Séquences où l'API arrêtera de générer |
| `n` | integer | 1 | Nombre de réponses à générer |
| `user` | string | null | Identifiant unique pour l'utilisateur final |

## Structure des Messages

### Types de Rôles

```json
{
  "messages": [
    {
      "role": "system",
      "content": "Vous êtes un assistant IA spécialisé en programmation."
    },
    {
      "role": "user",
      "content": "Comment optimiser une boucle for en Python ?"
    },
    {
      "role": "assistant",
      "content": "Voici plusieurs façons d'optimiser..."
    }
  ]
}
```

**Rôles disponibles :**
- `system` : Définit le comportement et le contexte de l'assistant
- `user` : Représente les messages de l'utilisateur
- `assistant` : Représente les réponses précédentes de l'IA

## Paramètres Détaillés

### Temperature

Contrôle l'aléatoire des réponses.

**Valeurs :**
- `0.0` : Déterministe, répétitif
- `0.7` : Équilibré (défaut)
- `1.0` : Plus créatif
- `2.0` : Très aléatoire

**Exemples d'utilisation :**

```python
# Pour du code : température basse
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "temperature": 0.2
}

# Pour du contenu créatif : température élevée
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "temperature": 1.2
}
```

### Max Tokens

Limite le nombre de tokens dans la réponse.

**Limites par modèle :**
- GPT-4.1 : jusqu'à 128,000 tokens
- GPT-4o : jusqu'à 128,000 tokens
- Claude Sonnet : jusqu'à 200,000 tokens

```python
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "max_tokens": 500  # Limite la réponse à 500 tokens
}
```

### Top P (Nucleus Sampling)

Alternative à temperature. Contrôle la diversité en sélectionnant les tokens dont la probabilité cumulée atteint P.

**Recommandations :**
- Utilisez `temperature` **OU** `top_p`, pas les deux
- `0.1` : Très déterministe
- `0.9` : Très diversifié
- `1.0` : Tous les tokens possibles (défaut)

```python
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "top_p": 0.9
}
```

### Frequency Penalty

Réduit la répétition de tokens fréquents.

**Valeurs :**
- `-2.0` à `2.0`
- Valeurs positives : diminuent la répétition
- Valeurs négatives : augmentent la répétition

```python
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "frequency_penalty": 0.5  # Réduit les répétitions
}
```

### Presence Penalty

Encourage l'IA à parler de nouveaux sujets.

**Valeurs :**
- `-2.0` à `2.0`
- Valeurs positives : favorisent la nouveauté
- Valeurs négatives : favorisent les sujets connus

```python
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "presence_penalty": 0.6  # Encourage de nouveaux sujets
}
```

### Stop Sequences

Arrête la génération quand une séquence spécifique est rencontrée.

```python
# Simple stop
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "stop": "\n"
}

# Multiple stops
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "stop": ["\n", "END", "###"]
}
```

### Streaming

Active le streaming en temps réel des réponses.

```python
data = {
    "model": "gpt-4.1",
    "messages": [...],
    "stream": True
}
```

**Gestion du stream :**

```python
import requests

response = requests.post(
    url,
    headers=headers,
    json=data,
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

## Exemples de Cas d'Usage

### Chat Classique

```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "system", "content": "Tu es un assistant serviable."},
    {"role": "user", "content": "Bonjour!"}
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
```

### Génération de Code

```json
{
  "model": "codestral-2508",
  "messages": [
    {"role": "user", "content": "Écris une fonction Python pour trier une liste"}
  ],
  "temperature": 0.2,
  "max_tokens": 500
}
```

### Contenu Créatif

```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "Écris un poème sur l'océan"}
  ],
  "temperature": 1.3,
  "presence_penalty": 0.6
}
```

### Extraction d'Informations

```json
{
  "model": "gpt-4.1-mini",
  "messages": [
    {"role": "user", "content": "Extrais les dates de ce texte: ..."}
  ],
  "temperature": 0,
  "max_tokens": 100
}
```

## Conseils d'Optimisation

### ✅ Bonnes Pratiques

1. **Utilisez des messages système clairs**
   ```json
   {"role": "system", "content": "Tu es un expert en Python avec 10 ans d'expérience"}
   ```

2. **Limitez max_tokens pour économiser**
   ```json
   {"max_tokens": 100}  // Pour des réponses courtes
   ```

3. **Ajustez temperature selon le besoin**
   - Code : 0.0 - 0.3
   - Analyse : 0.3 - 0.7
   - Créativité : 0.7 - 1.5

4. **Utilisez stop sequences pour du formatage**
   ```json
   {"stop": ["```", "END"]}
   ```

### ❌ À Éviter

1. **Ne combinez pas temperature et top_p**
2. **N'utilisez pas max_tokens trop élevé inutilement**
3. **Évitez frequency_penalty > 1.0 pour du texte naturel**

---

[← Modèles et Tarifs](./models-pricing.md) | [Codes d'Erreur →](./error-codes.md)
