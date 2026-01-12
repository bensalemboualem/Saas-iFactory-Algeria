# IAFactory Gateway Python

Gateway centralisé multi-providers IA

## Démarrage
docker-compose up -d
API : http://localhost:3001

## Providers
OpenAI , Anthropic, Groq, DeepSeek, Mistral, Gemini, Cohere, Together, OpenRouter

## Endpoints
POST /api/llm/chat/completions
GET /api/credits/{user_id}
POST /api/credits/add
POST /api/credits/consume
POST /api/webhook/chargily
