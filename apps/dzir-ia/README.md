# Dzir IA - Second Brain

> Your personal AI-powered knowledge management system integrated with IAFACTORY Gateway.

## Overview

Dzir IA ("My Brain" in Algerian Arabic) is a second-brain application that helps you capture, organize, and query your knowledge using AI. Similar to Notion + Rewind + Mem.ai.

### Features

- **Capture** - Save URLs, PDFs, text from anywhere
- **Organize** - Collections with custom colors/icons
- **Search** - Semantic search across all your knowledge
- **Ask** - RAG-powered Q&A with citations
- **Timeline** - Activity history and insights
- **Offline-first** - Works without internet, syncs when online

## Tech Stack

### Backend
- **Runtime**: Node.js 20+ (TypeScript)
- **Framework**: Hono
- **Vector DB**: Qdrant
- **Metadata DB**: SQLite (better-sqlite3)
- **File Storage**: MinIO
- **Auth**: JWT (via IAFACTORY Gateway)

### Frontend
- **Framework**: React 19 + TypeScript
- **Build**: Vite
- **Router**: React Router v7
- **State**: Zustand
- **Offline**: Dexie (IndexedDB)

## Quick Start

### Prerequisites

- Node.js 20+
- Docker & Docker Compose
- pnpm (recommended) or npm

### 1. Start Infrastructure

```bash
cd docker
docker-compose up -d
```

This starts:
- Qdrant on `http://localhost:6333`
- MinIO on `http://localhost:9000` (Console: `http://localhost:9001`)

### 2. Start Backend

```bash
cd backend
npm install
npm run dev
```

Backend runs on `http://localhost:4000`

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with service status |
| `/api/collections` | GET/POST | List/create collections |
| `/api/collections/:id` | GET/DELETE | Get/delete collection |
| `/api/capture` | POST | Capture new document |
| `/api/search` | GET/POST | Search documents |
| `/api/ask` | POST | Ask question (RAG) |
| `/api/sync` | POST | Sync offline changes |

## Environment Variables

### Backend

```env
PORT=4000
NODE_ENV=development
QDRANT_URL=http://localhost:6333
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
GATEWAY_URL=http://localhost:3000
SQLITE_PATH=./data/dzir.db
JWT_PUBLIC_KEY=<optional>
```

### Frontend

```env
VITE_API_URL=/api
```

## Project Structure

```
dzir-ia/
├── backend/
│   ├── src/
│   │   ├── index.ts          # Entry point
│   │   ├── routes/           # API routes
│   │   ├── middleware/       # Auth, credits
│   │   ├── services/         # DB, vector, storage
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx          # Entry point
│   │   ├── App.tsx           # Router setup
│   │   ├── components/       # UI components
│   │   ├── pages/            # Page components
│   │   ├── store/            # Zustand stores
│   │   ├── api/              # API client
│   │   ├── types/            # TypeScript types
│   │   └── styles/           # Global CSS
│   ├── package.json
│   └── vite.config.ts
├── docker/
│   └── docker-compose.yml    # Infrastructure
└── README.md
```

## Roadmap

### MVP (Current)
- [x] Project scaffold
- [ ] Basic CRUD for collections
- [ ] Document capture (text only)
- [ ] Simple chunking
- [ ] Search (placeholder embeddings)
- [ ] Ask endpoint (stub)
- [ ] Offline queue

### Phase 2
- [ ] Real embeddings (OpenAI/local)
- [ ] URL fetching & parsing
- [ ] PDF extraction
- [ ] Gateway integration (auth + credits)
- [ ] Browser extension

### Phase 3
- [ ] Graph visualization
- [ ] Memory consolidation
- [ ] Tauri desktop app
- [ ] Mobile PWA

## Integration with IAFACTORY

Dzir IA integrates with IAFACTORY Gateway for:

1. **Authentication** - JWT validation
2. **Credits** - Check/deduct per operation
3. **BYOK** - User's own API keys for embeddings

The Gateway URL is configured via `GATEWAY_URL` environment variable.

## License

Proprietary - IAFACTORY Algeria
