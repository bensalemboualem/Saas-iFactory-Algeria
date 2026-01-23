# Migration depuis OpenAI

## Vue d'Ensemble

Si vous utilisez déjà l'API OpenAI, migrer vers IAFactory Algeria est simple et ne nécessite que quelques changements mineurs.

## Changements Requis

### 1. URL de Base

**Avant (OpenAI) :**
```
https://api.openai.com/v1
```

**Après (IAFactory Algeria) :**
```
https://api.iafactory-algeria.com/v1
```

### 2. Clé API

Remplacez votre clé OpenAI par votre clé IAFactory Algeria.

➡️ [Obtenez votre clé API](https://dashboard.iafactory-algeria.com/api)

### 3. Modèles

Tous les modèles OpenAI sont disponibles, plus d'autres :
- GPT-4, GPT-3.5-Turbo ✅
- Claude 3 (Opus, Sonnet, Haiku) ✅
- Mistral AI ✅
- Gemini Pro ✅
- Et plus encore...

[Voir tous les modèles disponibles](./models-pricing.md)

## Migration par Langage

### Python avec la bibliothèque OpenAI

**Avant :**
```python
import openai

openai.api_key = "sk-openai-abc123"
# api_base par défaut : https://api.openai.com/v1

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Après :**
```python
import openai

openai.api_base = "https://api.iafactory-algeria.com/v1"
openai.api_key = "votre-cle-iafactory"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Avec variables d'environnement :**
```python
import openai
import os

openai.api_base = os.getenv("IAFACTORY_API_BASE", "https://api.iafactory-algeria.com/v1")
openai.api_key = os.getenv("IAFACTORY_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### JavaScript/TypeScript

**Avant :**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'sk-openai-abc123',
});

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Hello' }],
});
```

**Après :**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'votre-cle-iafactory',
  baseURL: 'https://api.iafactory-algeria.com/v1',
});

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Hello' }],
});
```

### cURL

**Avant :**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer sk-openai-abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Après :**
```bash
curl https://api.iafactory-algeria.com/v1/chat/completions \
  -H "Authorization: Bearer votre-cle-iafactory" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Migration d'Applications Complètes

### Application Flask (Python)

**Avant :**
```python
# config.py
OPENAI_API_KEY = "sk-openai-abc123"
OPENAI_API_BASE = "https://api.openai.com/v1"

# app.py
import openai
from config import OPENAI_API_KEY, OPENAI_API_BASE

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE
```

**Après :**
```python
# config.py
IAFACTORY_API_KEY = os.getenv("IAFACTORY_API_KEY")
IAFACTORY_API_BASE = "https://api.iafactory-algeria.com/v1"

# app.py
import openai
from config import IAFACTORY_API_KEY, IAFACTORY_API_BASE

openai.api_key = IAFACTORY_API_KEY
openai.api_base = IAFACTORY_API_BASE
```

### Application Express.js (Node)

**Avant :**
```javascript
// config.js
module.exports = {
  openaiApiKey: process.env.OPENAI_API_KEY,
  openaiApiBase: 'https://api.openai.com/v1'
};

// app.js
const OpenAI = require('openai');
const config = require('./config');

const openai = new OpenAI({
  apiKey: config.openaiApiKey,
});
```

**Après :**
```javascript
// config.js
module.exports = {
  iafactoryApiKey: process.env.IAFACTORY_API_KEY,
  iafactoryApiBase: 'https://api.iafactory-algeria.com/v1'
};

// app.js
const OpenAI = require('openai');
const config = require('./config');

const openai = new OpenAI({
  apiKey: config.iafactoryApiKey,
  baseURL: config.iafactoryApiBase
});
```

## Compatibilité

### ✅ Fonctionnalités Compatibles

- Chat Completions
- Completions (legacy)
- Embeddings
- Moderation
- Models List
- Streaming
- Function Calling
- JSON Mode

### ⚠️ Différences

1. **Modèles supplémentaires disponibles**
   - Claude 3, Mistral, Gemini, etc.
   - [Voir la liste complète](./models-pricing.md)

2. **Tarification différente**
   - Généralement moins cher
   - [Voir les tarifs](./models-pricing.md)

3. **Rate limits différents**
   - Selon votre plan
   - [Voir les quotas](../legal/quotas.md)

### ❌ Non Supporté

- Fine-tuning (bientôt disponible)
- DALL-E (utilisez nos alternatives)
- Whisper (bientôt disponible)

## Outils et Frameworks

### LangChain

**Python :**
```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(
    openai_api_base="https://api.iafactory-algeria.com/v1",
    openai_api_key="votre-cle-iafactory",
    model_name="gpt-4"
)

messages = [HumanMessage(content="Hello")]
response = chat(messages)
```

**TypeScript :**
```typescript
import { ChatOpenAI } from "langchain/chat_models/openai";

const chat = new ChatOpenAI({
  openAIApiKey: "votre-cle-iafactory",
  configuration: {
    basePath: "https://api.iafactory-algeria.com/v1",
  },
  modelName: "gpt-4",
});
```

### LlamaIndex

```python
from llama_index import OpenAI

llm = OpenAI(
    api_base="https://api.iafactory-algeria.com/v1",
    api_key="votre-cle-iafactory",
    model="gpt-4"
)
```

### Semantic Kernel

```csharp
using Microsoft.SemanticKernel;

var kernel = Kernel.Builder
    .WithOpenAIChatCompletionService(
        modelId: "gpt-4",
        apiKey: "votre-cle-iafactory",
        endpoint: "https://api.iafactory-algeria.com/v1"
    )
    .Build();
```

## Variables d'Environnement

### Fichier .env

**Avant :**
```bash
OPENAI_API_KEY=sk-openai-abc123
OPENAI_API_BASE=https://api.openai.com/v1
```

**Après :**
```bash
IAFACTORY_API_KEY=votre-cle-iafactory
IAFACTORY_API_BASE=https://api.iafactory-algeria.com/v1
```

### Docker

**Avant :**
```yaml
# docker-compose.yml
environment:
  - OPENAI_API_KEY=sk-openai-abc123
  - OPENAI_API_BASE=https://api.openai.com/v1
```

**Après :**
```yaml
# docker-compose.yml
environment:
  - IAFACTORY_API_KEY=votre-cle-iafactory
  - IAFACTORY_API_BASE=https://api.iafactory-algeria.com/v1
```

## Checklist de Migration

- [ ] Obtenir une clé API IAFactory Algeria
- [ ] Mettre à jour l'URL de base dans le code
- [ ] Remplacer la clé API
- [ ] Mettre à jour les variables d'environnement
- [ ] Tester les endpoints principaux
- [ ] Vérifier les modèles utilisés
- [ ] Ajuster les rate limits si nécessaire
- [ ] Mettre à jour la documentation interne
- [ ] Former l'équipe sur les nouveaux modèles disponibles

## Script de Migration Automatique

### Python
```python
import os
import re

def migrate_code(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remplacer les URLs
    content = content.replace(
        'https://api.openai.com/v1',
        'https://api.iafactory-algeria.com/v1'
    )
    
    # Remplacer les variables
    content = content.replace('OPENAI_API_KEY', 'IAFACTORY_API_KEY')
    content = content.replace('OPENAI_API_BASE', 'IAFACTORY_API_BASE')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Migré: {file_path}")

# Utilisation
migrate_code('app.py')
```

## Support

Besoin d'aide pour la migration ?

- 📧 Email : migration@iafactory-algeria.com
- 💬 Discord : [Support Migration](https://discord.gg/iafactory)
- 📚 Documentation : [docs.iafactory-algeria.com](https://docs.iafactory-algeria.com)

---

[← Codes d'Erreur](./error-codes.md) | [Intégrations →](../integrations/n8n.md)
