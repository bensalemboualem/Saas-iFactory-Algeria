#  IAFactory - SaaS Gateway IA Algérie

Gateway multi-providers IA + paiement monnaie locale

##  Status : 80% Opérationnel

###  Fonctionnel
- Gateway Python : http://localhost:3001
- Provider DeepSeek : E2E validé
- 4 backends : Academy, AI-Tools, Video
- Facturation automatique : 46 tokens débités
- PostgreSQL + crédits persistants

###  Composants
- 15 agents (134 fichiers Python)
- 2 apps core réelles (video-studio, api-portal)
- DeepSeek provider validé

###  Stack
- FastAPI + PostgreSQL
- 9 providers IA (1 validé)
- Docker

##  Reste (1-2h)
- Clés prod : OpenAI, Groq, Anthropic
- Fix Gemini
- Tests composants

##  Quick Start
bash
cd iafactory-gateway-python && docker-compose up -d
cd iafactory-academy && docker-compose up -d

Voir START-HERE.md
