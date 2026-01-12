# Gateway IAFactory Python

CORE du SaaS : facturation + routing IA

## Providers
9 providers : OpenAI, Anthropic, Groq, DeepSeek, Mistral, Gemini, Cohere, Together, OpenRouter

## Endpoints
- POST /api/llm/chat/completions
- GET /api/credits/{user_id}
- POST /api/credits/add
- POST /api/credits/consume
- POST /api/webhook/chargily

## Base
- PostgreSQL : users, transactions
- Port 3001
