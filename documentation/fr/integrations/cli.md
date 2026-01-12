# Intégration CLI

## Introduction
La CLI IAFactory permet d’interagir avec l’API IAFactory directement depuis votre terminal. Cette page explique comment installer, configurer et utiliser la CLI pour automatiser vos tâches IA.

## Prérequis
- Un compte IAFactory avec une clé API valide
- Node.js ou Python installé sur votre machine

## Installation
### Via npm (Node.js)
```bash
npm install -g iafactory-cli
```
### Via pip (Python)
```bash
pip install iafactory-cli
```

## Démarrage rapide
1. Configurez votre clé API :
```bash
iafactory config set api_key VOTRE_CLE_API
```
2. Lancez une requête simple :
```bash
iafactory chat "Explique les avantages de l’automatisation IA"
```

## Commandes principales
- `iafactory chat <message>` : Génère une réponse IA
- `iafactory models` : Liste les modèles disponibles
- `iafactory quota` : Affiche votre quota d’utilisation

## Conseils d’utilisation
- Utilisez des prompts clairs pour des réponses précises
- Consultez la documentation des options avancées

## Ressources utiles
- [Documentation CLI IAFactory](https://iafactory.com/docs/cli)
- Support IAFactory : support@iafactory.com