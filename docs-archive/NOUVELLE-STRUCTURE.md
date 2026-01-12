# Nouvelle Structure IAFactory - 11 janvier 2026

## Reorganisation complete

### iafactory-core-apps/ (10 apps principales)
Apps de production prioritaires :
- cockpit, crm-ia, cv-builder, ia-chatbot
- legal-assistant, video-studio
- dev-portal, api-portal
- ia-agents, workflow-studio

### iafactory-agents/ (15 agents)
Tous les agents IA :
- business, finance, legal, rag
- recruitment, teaching, video-operator
- etc.

### iafactory-experimental/ (8 apps)
Apps en test/developpement :
- cockpit-voice, cv-ia, dzirvideo
- ia-notebook, ia-searcher, ia-voice
- interview, prompt-creator

### rag-dz-legacy/
Ancien monorepo archive (reference seulement)

## Migration terminee
- 10 apps principales extraites
- 8 apps experimentales separees
- 15 agents reorganises
- Ancien rag-dz preserve en legacy

Total : 33 composants reorganises
