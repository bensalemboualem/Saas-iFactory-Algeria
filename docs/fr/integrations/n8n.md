# Intégration n8n

## Introduction

n8n est une plateforme d'automatisation open-source qui permet de connecter différents services. IAFactory Algeria peut être facilement intégré à n8n pour créer des workflows d'IA puissants.

## Configuration de Base

### Méthode 1 : Nœud HTTP Request

1. **Ajoutez un nœud HTTP Request**
   - Dans votre workflow, cliquez sur `+`
   - Recherchez "HTTP Request"
   - Ajoutez le nœud

2. **Configurez le nœud**
   - **Method** : `POST`
   - **URL** : `https://api.iafactory-algeria.com/v1/chat/completions`

3. **Ajoutez l'authentification**
   - **Authentication** : `Generic Credential Type`
   - **Generic Auth Type** : `Header Auth`
   - **Credentials** :
     - **Name** : `Authorization`
     - **Value** : `Bearer VOTRE_CLE_API`

4. **Configurez le body**
   - **Body Content Type** : `JSON`
   - **Specify Body** : `Using JSON`
   - **JSON** :
   ```json
   {
     "model": "gpt-4.1",
     "messages": [
       {
         "role": "user",
         "content": "{{ $json.message }}"
       }
     ]
   }
   ```

## Exemples de Workflows

### Workflow 1 : Chatbot Telegram

```json
{
  "name": "IAFactory Telegram Bot",
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "parameters": {
        "updates": ["message"]
      }
    },
    {
      "name": "IAFactory API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.iafactory-algeria.com/v1/chat/completions",
        "authentication": "genericCredentialType",
        "genericAuthType": "headerAuth",
        "bodyParametersJson": "={\n  \"model\": \"gpt-4.1\",\n  \"messages\": [\n    {\n      \"role\": \"user\",\n      \"content\": \"{{ $json.message.text }}\"\n    }\n  ]\n}"
      }
    },
    {
      "name": "Send Response",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "operation": "sendMessage",
        "chatId": "={{ $node['Telegram Trigger'].json.message.chat.id }}",
        "text": "={{ $json.choices[0].message.content }}"
      }
    }
  ]
}
```

### Workflow 2 : Résumé d'Emails

```json
{
  "name": "Email Summarizer",
  "nodes": [
    {
      "name": "Email Trigger",
      "type": "n8n-nodes-base.emailReadImap",
      "parameters": {
        "mailbox": "INBOX",
        "options": {}
      }
    },
    {
      "name": "IAFactory Summarize",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.iafactory-algeria.com/v1/chat/completions",
        "bodyParametersJson": "={\n  \"model\": \"gpt-4.1-mini\",\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"Tu es un assistant qui résume les emails de manière concise.\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Résume cet email:\\n\\n{{ $json.text }}\"\n    }\n  ],\n  \"max_tokens\": 200\n}"
      }
    },
    {
      "name": "Send Summary",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "toEmail": "vous@example.com",
        "subject": "Résumé: {{ $node['Email Trigger'].json.subject }}",
        "text": "={{ $json.choices[0].message.content }}"
      }
    }
  ]
}
```

### Workflow 3 : Analyse de Sentiment Twitter

```json
{
  "name": "Twitter Sentiment Analysis",
  "nodes": [
    {
      "name": "Twitter",
      "type": "n8n-nodes-base.twitter",
      "parameters": {
        "resource": "search",
        "operation": "search",
        "searchText": "#votreHashtag"
      }
    },
    {
      "name": "Analyze Sentiment",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.iafactory-algeria.com/v1/chat/completions",
        "bodyParametersJson": "={\n  \"model\": \"gpt-4.1-mini\",\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"Analyse le sentiment de ce tweet. Réponds uniquement: Positif, Négatif ou Neutre.\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"{{ $json.full_text }}\"\n    }\n  ],\n  \"temperature\": 0.3\n}"
      }
    },
    {
      "name": "Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "append",
        "sheetId": "VOTRE_SHEET_ID",
        "range": "A:C",
        "valueInputMode": "USER_ENTERED",
        "values": "={{ [[$node['Twitter'].json.user.screen_name, $node['Twitter'].json.full_text, $json.choices[0].message.content]] }}"
      }
    }
  ]
}
```

### Workflow 4 : Traduction Automatique

```json
{
  "name": "Auto Translator",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "translate",
        "method": "POST"
      }
    },
    {
      "name": "Translate",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.iafactory-algeria.com/v1/chat/completions",
        "bodyParametersJson": "={\n  \"model\": \"gpt-4.1\",\n  \"messages\": [\n    {\n      \"role\": \"user\",\n      \"content\": \"Traduis ce texte en {{ $json.body.target_language }}:\\n\\n{{ $json.body.text }}\"\n    }\n  ]\n}"
      }
    },
    {
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "options": {
          "responseData": "={{ $json.choices[0].message.content }}"
        }
      }
    }
  ]
}
```

## Fonctionnalités Avancées

### Streaming (Réponses en Temps Réel)

Pour activer le streaming dans n8n :

```json
{
  "bodyParametersJson": {
    "model": "gpt-4.1",
    "messages": [...],
    "stream": true
  },
  "options": {
    "response": {
      "fullResponse": true
    }
  }
}
```

**Note :** Le streaming nécessite un traitement spécial des SSE (Server-Sent Events).

### Gestion des Erreurs

Ajoutez un nœud **Error Trigger** pour gérer les erreurs :

```json
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.errorTrigger",
  "parameters": {},
  "continueOnFail": false
}
```

### Retry Logic

Configurez les retries automatiques :

```json
{
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000
}
```

## Modèles de Prompts

### Extraction de Données

```javascript
{
  "role": "system",
  "content": "Extrait les informations suivantes du texte et retourne-les en JSON: nom, email, téléphone"
},
{
  "role": "user",
  "content": "{{ $json.text }}"
}
```

### Génération de Contenu

```javascript
{
  "role": "system",
  "content": "Tu es un expert en marketing. Génère un post LinkedIn professionnel."
},
{
  "role": "user",
  "content": "Sujet: {{ $json.topic }}"
}
```

### Classification

```javascript
{
  "role": "system",
  "content": "Classe ce texte dans une des catégories: Support, Vente, Feedback, Autre"
},
{
  "role": "user",
  "content": "{{ $json.message }}"
}
```

## Credentials n8n

### Créer un Credential IAFactory

1. Allez dans **Credentials** → **New**
2. Cherchez **Header Auth**
3. Configurez :
   - **Credential Name** : `IAFactory Algeria`
   - **Name** : `Authorization`
   - **Value** : `Bearer VOTRE_CLE_API`
4. Sauvegardez

### Réutiliser le Credential

Dans chaque nœud HTTP Request :
- **Authentication** : `Generic Credential Type`
- **Credential Type** : `Header Auth`
- **Credential for Header Auth** : Sélectionnez `IAFactory Algeria`

## Optimisations

### Cache des Réponses

Utilisez un nœud **Set** pour cacher les réponses fréquentes :

```json
{
  "name": "Cache Response",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "name": "cached_response",
          "value": "={{ $json.choices[0].message.content }}",
          "type": "string"
        },
        {
          "name": "timestamp",
          "value": "={{ DateTime.now().toISO() }}",
          "type": "string"
        }
      ]
    }
  }
}
```

### Batch Processing

Traitez plusieurs items en parallèle :

```json
{
  "name": "Split In Batches",
  "type": "n8n-nodes-base.splitInBatches",
  "parameters": {
    "batchSize": 10,
    "options": {}
  }
}
```

## Débogage

### Afficher les Requêtes

Activez "Include Response Headers and Status" dans les options du nœud HTTP Request.

### Logs

Ajoutez un nœud **Function** pour logger :

```javascript
console.log('Request:', $input.all());
console.log('Response:', $json);
return $input.all();
```

## Ressources

- 📚 [Documentation n8n](https://docs.n8n.io)
- 🎥 [Tutoriel vidéo n8n + IAFactory](https://youtube.com/iafactory-n8n)
- 💬 [Communauté n8n](https://community.n8n.io)
- 📦 [Templates n8n IAFactory](https://n8n.io/workflows?search=iafactory)

---

[← Migration OpenAI](../api/migration-openai.md) | [VS Code / Cline →](./vscode-cline.md)
