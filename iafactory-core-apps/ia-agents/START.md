# 🚀 Démarrage rapide - Agent Motivation

## Installation

```bash
# 1. Aller dans le dossier
cd D:\IAFactory\rag-dz\apps\agents-ia

# 2. Installer les dépendances
npm install

# 3. Copier le fichier d'environnement
copy .env.local.example .env.local

# 4. Éditer .env.local et ajouter votre clé API Anthropic
# ANTHROPIC_API_KEY=sk-ant-...

# 5. Démarrer le serveur
npm run dev
```

## Accès

Ouvrir dans le navigateur: **http://localhost:3001**

## Fonctionnalités à tester

1. **Chat avec Amine**: Poser une question ou cliquer sur une question suggérée
2. **Mood Tracker**: Faire un check-in quotidien avec un emoji
3. **Streak Counter**: Voir les jours consécutifs
4. **Breathing Exercise**: Cliquer sur "Exercice de respiration"
5. **Achievements**: Débloquer des badges
6. **Usage Limit**: Envoyer 10 messages pour voir le modal de lead capture

## Structure du projet

```
apps/agents-ia/
├── app/
│   ├── agents/
│   │   └── motivation/
│   │       ├── components/      # Tous les composants React
│   │       ├── hooks/           # Hook useUsageLimit
│   │       ├── prompts/         # System prompt pour Amine
│   │       └── page.tsx         # Page principale
│   ├── api/
│   │   └── chat/
│   │       └── motivation/
│   │           └── route.ts     # API route streaming
│   ├── layout.tsx               # Layout racine
│   ├── page.tsx                 # Homepage
│   └── globals.css              # Styles globaux
├── package.json
├── tailwind.config.ts
└── .env.local                   # À créer avec votre API key
```

## Support

Pour toute question, consulter le fichier `AGENT_MOTIVATION_STATUS.md` qui contient tous les détails.
