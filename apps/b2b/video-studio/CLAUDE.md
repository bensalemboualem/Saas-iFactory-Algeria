# CLAUDE.md - Instructions pour Claude Code

## 🎯 Projet: IA Factory Video Studio

### Vue d'ensemble
Application de génération vidéo IA pour IA Factory, ciblant le marché algérien/MENA avec support du Darija.

### Stack technique
- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: Python FastAPI + Redis (queue) + PostgreSQL
- **APIs IA**: Fal.ai (Kling, Runway), Replicate, ElevenLabs
- **Déploiement**: Docker + Docker Compose

---

## 📁 Structure du projet

```
apps/video-studio/
├── frontend/                 # Next.js 14 App
│   ├── app/
│   │   ├── (dashboard)/     # Routes protégées
│   │   │   ├── studio/      # Éditeur vidéo principal
│   │   │   ├── templates/   # Bibliothèque de templates
│   │   │   ├── projects/    # Mes projets
│   │   │   └── credits/     # Gestion des crédits
│   │   ├── api/             # API Routes Next.js
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/              # Composants UI réutilisables
│   │   └── studio/          # Composants de l'éditeur
│   └── lib/                 # Utilities & API client
│
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/            # Config & security
│   │   ├── schemas/         # Pydantic models
│   │   └── services/        # External API services
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Commandes de développement

### Setup
```bash
cd apps/video-studio
cp .env.example .env
docker-compose up -d
```

### Dev local
```bash
# Frontend (port 3000)
cd frontend && npm install && npm run dev

# Backend (port 8000)
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🔌 APIs

- **Fal.ai**: Text-to-Video (Kling 1.6), Image-to-Video
- **ElevenLabs**: TTS avec voix Darija
- **Replicate**: Modèles additionnels

---

## ⚡ Règles de code

- Server Components par défaut (Next.js)
- Async/await partout (FastAPI)
- Tailwind CSS pour les styles
- Pydantic pour la validation
