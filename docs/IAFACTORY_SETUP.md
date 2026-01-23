# IAFactory-Chat - Guide d'Installation

Fork personnalise de LobeChat pour le Programme National IA en Algerie.

## Pre-requis

- Node.js 18+ ou Bun
- pnpm 8+
- Ollama (pour les modeles IA locaux)
- Docker (optionnel, pour le deploiement)

## Installation Rapide

### Option 1: Developpement Local

```bash
# 1. Installer pnpm si necessaire
npm install -g pnpm

# 2. Installer les dependances
cd iafactory-chat
pnpm install

# 3. Copier le fichier .env
# Le fichier .env est deja configure pour Ollama

# 4. Lancer en mode developpement
pnpm dev
```

Ouvrir http://localhost:3010

### Option 2: Docker (Recommande pour Production)

```bash
# 1. Construire l'image Docker
docker build -t iafactory-chat .

# 2. Lancer avec docker-compose
docker-compose -f docker-compose.iafactory.yml up -d

# 3. Acceder
# http://localhost:3210
```

## Configuration Ollama

Avant de lancer IAFactory-Chat, assurez-vous qu'Ollama est en cours d'execution:

```bash
# Verifier qu'Ollama fonctionne
ollama list

# Telecharger un modele (si necessaire)
ollama pull qwen2:7b
```

## Personnalisation

### Changer le Logo

1. Remplacer `/public/images/iafactory-logo.svg` par votre logo
2. Supporter les formats: SVG, PNG, WebP

### Changer les Couleurs

Modifier les variables CSS dans le theme ou utiliser les parametres dans l'interface.

### Ajouter des Providers IA

Editer le fichier `.env`:

```env
# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxx

# OpenRouter (Qwen, Claude, etc.)
OPENROUTER_API_KEY=sk-xxxxx

# OpenAI
OPENAI_API_KEY=sk-xxxxx
```

## Structure du Projet

```
iafactory-chat/
├── packages/const/src/branding.ts  # Configuration du branding
├── public/images/                   # Logos et images
├── .env                             # Variables d'environnement
├── docker-compose.iafactory.yml    # Docker Compose pour production
└── src/                             # Code source
```

## Commandes Utiles

```bash
# Developpement
pnpm dev

# Build production
pnpm build

# Lancer en production
pnpm start

# Tests
pnpm test
```

## Support

- Site: https://www.iafactoryalgeria.com
- Email: support@iafactoryalgeria.com

---
IAFactory Algeria - Programme National IA pour l'Education
