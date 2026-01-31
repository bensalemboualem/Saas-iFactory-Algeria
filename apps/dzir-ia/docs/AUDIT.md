# Dzir IA - Audit (2026-01-30)

## État actuel (constaté dans le code)

### Backend
- Framework Hono, routes montées dans `apps/dzir-ia/backend/src/app.ts`.
- Endpoints exposés: `/api/collections`, `/api/documents`, `/api/capture`, `/api/search`, `/api/ask`, `/api/sync`.
- RAG: embeddings + Qdrant + citations (voir `apps/dzir-ia/backend/src/routes/ask.ts`).
- Auth: middleware JWT présent (`apps/dzir-ia/backend/src/middleware/auth.ts`).
- Storage: MinIO + SQLite + Qdrant (voir services dans `apps/dzir-ia/backend/src/services/*`).

### Frontend
- Vite + React Router (`apps/dzir-ia/frontend/src/App.tsx`).
- Pages: Chat, Collections, Search, Timeline + Graph placeholder.
- UI orientée “knowledge app” basique (pas de landing Remio-like).
- Sidebar et Layout présents, mais design/UX encore génériques.

### Infra
- Stack dédiée dans `apps/dzir-ia/docker/docker-compose.yml` (Qdrant + MinIO).
- Backend/Frontend démarrables localement (ports 4000 / 5173).

## Écarts vs objectif “Clone Remio.ai + mieux”
- UX actuelle trop “dev/basic” (pas d’onboarding clair, pas de workflow capture → ask).
- Pas de landing marketing style Remio.
- Capture limitée (pas d’auto-capture web/email/desktop).
- Pas de vraie timeline “activity” riche.
- Pas d’espace “sources” détaillé (collections ok, mais pas de provenance fine).

## Risques
- Trop de features backend sans UX claire (risque de produit confus).
- Manque de marketing/positionnement.
- Pas de “local-first”/BYOK mis en avant dans l’UI.

## Priorités techniques (court terme)
1. Refonte UX (Home + Ask + Sources + Timeline) et design cohérent.
2. Flow capture clair (manuel puis auto-capture).
3. Monitoring simple (log captures + recherches + asks).
