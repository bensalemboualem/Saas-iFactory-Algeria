# IAFactory - SaaS Gateway IA Algérie

Gateway multi-providers IA + paiement monnaie locale pour marché algérien (2M étudiants + PME)

## Stack
- Gateway Python : FastAPI + PostgreSQL
- 9 providers IA : OpenAI, Anthropic, Groq, DeepSeek, Mistral, etc.
- Facturation automatique par token
- 4 backends : Gateway, Academy (LMS), AI-Tools, Video

## Démarrage
bash
cd iafactory-gateway-python
docker-compose up -d

Gateway : http://localhost:3001

Voir BILAN-FINAL-16H.md pour détails
