# IAFactory Gateway Python

Gateway centralisé multi-providers IA

## Architecture
- FastAPI + PostgreSQL
- 9 providers IA : OpenAI , Anthropic, Groq, DeepSeek, Mistral, Gemini, Cohere, Together, OpenRouter
- Facturation automatique par token
- Webhook Chargily (paiements Algérie)

## Règles
- TOUTES les apps passent par gateway
- Jamais appels directs providers
- 1 token = 1 crédit

## Endpoints
- POST /api/llm/chat/completions
- GET /api/credits/{user_id}
- POST /api/credits/add
- POST /api/credits/consume
- POST /api/webhook/chargily

Port : 3001
