# IAFactory AI Gateway

OpenAI-compatible AI Gateway with multi-provider routing, credit management, and rate limiting.

## Features

- ✅ **OpenAI-Compatible API** - `/v1/models` and `/v1/chat/completions`
- ✅ **Multi-Provider Support** - Groq, OpenRouter, DeepSeek, Ollama
- ✅ **SSE Streaming** - Real-time streaming responses
- ✅ **Credit System** - Usage tracking and billing
- ✅ **Rate Limiting** - Redis-based rate limiting
- ✅ **Model Profiles** - Preconfigured model profiles (iaf-fast, iaf-smart, iaf-cheap, iaf-local)
- ✅ **Automatic Fallback** - Provider failover on errors
- ✅ **Usage Analytics** - Detailed usage logging and ledger

## Architecture

```
Client (Bolt/Frontend)
    ↓
IAFactory Gateway (Node/TS + Fastify)
    ↓
[Auth + Credits + Rate Limit]
    ↓
Router → Profiles
    ↓
Providers:
  - Groq (ultra-fast)
  - OpenRouter (premium models)
  - DeepSeek (cheap)
  - Ollama (local)
```

## Quick Start

### 1. Prerequisites

- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

### 2. Installation

```bash
# Clone repository
git clone <repo-url>
cd iafactory-gateway

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### 3. Database Setup

```bash
# Generate Prisma client
npm run db:generate

# Run migrations
npm run db:migrate

# (Optional) Open Prisma Studio
npm run db:studio
```

### 4. Run Development Server

```bash
npm run dev
```

Gateway will be available at `http://localhost:3001`

### 5. Docker Compose (Recommended)

```bash
# Start all services (Postgres, Redis, Gateway)
docker-compose up -d

# View logs
docker-compose logs -f gateway

# Stop services
docker-compose down
```

## API Usage

### Authentication

All requests require authentication via API key or JWT:

```bash
curl http://localhost:3001/v1/models \
  -H "Authorization: Bearer iaf_your_api_key"
```

### List Models

```bash
GET /v1/models
```

Returns all available IAFactory model profiles:
- `iaf-fast-llama` - Ultra-fast with Groq
- `iaf-smart-claude` - Best reasoning with OpenRouter
- `iaf-cheap-deepseek` - Best price/performance
- `iaf-local-llama` - On-premise RGPD-compliant

### Chat Completions

```bash
POST /v1/chat/completions
Content-Type: application/json
Authorization: Bearer iaf_your_api_key

{
  "model": "iaf-fast-llama",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": true
}
```

## Model Profiles

| Profile | Provider | Latency | Cost | Use Case |
|---------|----------|---------|------|----------|
| `iaf-fast-llama` | Groq | Ultra-fast | Very cheap | Interactive chat |
| `iaf-fast-mixtral` | Groq | Ultra-fast | Cheapest | Multilingual |
| `iaf-smart-claude` | OpenRouter | Normal | Premium | Reasoning, code quality |
| `iaf-smart-gpt4` | OpenRouter | Normal | Expensive | Complex tasks |
| `iaf-cheap-deepseek` | DeepSeek | Fast | Very cheap | Coding, general use |
| `iaf-cheap-qwen` | OpenRouter | Fast | Cheap | Chinese + multilingual |
| `iaf-local-llama` | Ollama | Slow | Free | RGPD, on-premise |

## Credit System

Credits are debited atomically per request:

1. **Reserve** - Check if user has enough credits
2. **Debit** - Charge actual tokens used after response
3. **Ledger** - Log usage for analytics and billing

## Configuration

Key environment variables:

```bash
# Server
PORT=3001
API_BASE_URL=http://localhost:3001

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Redis
REDIS_URL=redis://localhost:6379

# Provider Keys (server-side only)
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-v1-...
DEEPSEEK_API_KEY=sk-...
```

## Production Deployment

### 1. Build

```bash
npm run build
```

### 2. Run Migrations

```bash
npm run db:push
```

### 3. Start

```bash
NODE_ENV=production npm start
```

### 4. Docker Production

```bash
docker build -t iafactory-gateway .
docker run -p 3001:3001 --env-file .env iafactory-gateway
```

## Connecting Bolt.diy

Configure Bolt to use IAFactory Gateway:

```bash
# In bolt.diy/.env.local
OPENAI_LIKE_API_BASE_URL=http://localhost:3001/v1
OPENAI_LIKE_API_KEY=iaf_your_api_key
```

Bolt will now route all requests through your gateway with credit management.

## Scripts

- `npm run dev` - Development server with hot reload
- `npm run build` - Build TypeScript
- `npm start` - Production server
- `npm run db:generate` - Generate Prisma client
- `npm run db:migrate` - Run database migrations
- `npm run db:studio` - Open Prisma Studio
- `npm test` - Run tests
- `npm run lint` - Lint code
- `npm run format` - Format code

## API Reference

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2026-01-03T...",
  "uptime": 123.45,
  "environment": "production",
  "version": "1.0.0"
}
```

### Models

```bash
GET /v1/models
Authorization: Bearer iaf_xxx
```

### Chat Completions

```bash
POST /v1/chat/completions
Authorization: Bearer iaf_xxx
Content-Type: application/json

{
  "model": "iaf-fast-llama",
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 2000,
  "stream": true
}
```

## License

MIT

## Support

For issues or questions: [support@iafactory.dz](mailto:support@iafactory.dz)
