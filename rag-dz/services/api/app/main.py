from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
import logging

from .middleware import RequestIDMiddleware
from .security import EnhancedAuthMiddleware, RateLimitMiddleware
from .monitoring import init_metrics
from .tenant_middleware import TenantContextMiddleware
from .routers import test, upload, query, websocket_router, knowledge, progress, bmad, bmad_chat, bmad_orchestration, coordination, orchestrator, auth, bolt, agent_chat, calendar, voice, google, email_agent, twilio, whatsapp, user_keys, studio_video, rag_public, credentials, council, council_custom, ithy, billing, crm, pme, pme_v2, billing_v2, crm_pro, dzirvideo, growth_grid, notebook_lm, prompt_creator, promo_codes, agents, tenants, chat_rooms
from .bigrag import bigrag_router
from .bigrag_ingest import ingest_router
from .ocr import ocr_router
from .darija import darija_router
from .voice.stt_router import router as stt_router
from .voice.tts_router import router as tts_router
from .voice.voice_agent_router import router as voice_agent_router
from .multi_llm import multi_llm_router
from .team_seats import team_seats_router
from .config import get_settings

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

init_metrics()

app = FastAPI(
    title="IAFactory API",
    version=settings.service_version,
    description="Plateforme IA complète - Chat, Voice, Calendar, Automations",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# CORS avec configuration sécurisée
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-Id", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
        max_age=3600,
    )

# Middlewares (ordre important!)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantContextMiddleware)  # Multi-tenant RLS context
app.add_middleware(EnhancedAuthMiddleware)
app.add_middleware(RequestIDMiddleware)

# Routes
app.include_router(auth.router, tags=["Auth"])  # Auth routes (no prefix - already has /api/auth)
app.include_router(test.router, prefix="/api", tags=["Test"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(knowledge.router, tags=["Knowledge"])
app.include_router(progress.router, tags=["Progress"])
app.include_router(bmad.router, tags=["BMAD"])
app.include_router(bmad_chat.router, tags=["BMAD Chat"])
app.include_router(bmad_orchestration.router, tags=["BMAD Orchestration"])
app.include_router(coordination.router, tags=["Coordination"])
app.include_router(orchestrator.router, tags=["Orchestrator"])
app.include_router(bolt.router, tags=["Bolt SuperPower"])
app.include_router(agent_chat.router, tags=["Agent Chat"])  # Compatibilité Archon-UI
app.include_router(calendar.router, tags=["Calendar"])  # Gestion des rendez-vous
app.include_router(voice.router, tags=["Voice Agent"])  # Agent vocal Vapi.ai
app.include_router(google.router, tags=["Google Integration"])  # Google Calendar & Gmail
app.include_router(email_agent.router, tags=["Email Agent"])  # Agent Email (6ème agent)
app.include_router(twilio.router, tags=["Twilio SMS"])  # SMS et rappels Twilio
app.include_router(whatsapp.router, tags=["WhatsApp"])  # WhatsApp Business via Twilio
app.include_router(user_keys.router, tags=["User Keys"])  # Gestion clés API (Key Reselling)
app.include_router(studio_video.router, tags=["Creative Studio"])  # Studio Creatif (Video/Image/Presentation)
app.include_router(rag_public.router, tags=["RAG Public"])  # RAG API publique pour Bolt
app.include_router(credentials.router, tags=["Credentials"])  # Gestion des credentials AI providers
app.include_router(council.router, tags=["Council"])  # LLM Council - Multi-AI deliberation
app.include_router(council_custom.router, tags=["Council Custom"])  # Council personnalisable
app.include_router(ithy.router, tags=["Ithy MoA"])  # Mixture-of-Agents research assistant
app.include_router(billing.router, tags=["Billing"])  # Gestion crédits et facturation
app.include_router(crm.router, tags=["CRM"])  # Gestion des leads
app.include_router(pme.router, tags=["PME Copilot"])  # Analyse PME DZ (v1)
app.include_router(pme_v2.router, tags=["PME Analyzer PRO V2"])  # Analyse PME DZ PRO
app.include_router(billing_v2.router, tags=["Billing PRO V2"])  # Gestion crédits SaaS PRO
app.include_router(crm_pro.router, tags=["CRM PRO"])  # CRM HubSpot-like DZ/CH powered by IA
app.include_router(bigrag_router, tags=["BIG RAG Multi-Pays"])  # RAG Multi-Pays DZ/CH/GLOBAL 🌍
app.include_router(ingest_router, tags=["BigRAG Ingest"])  # Ingestion documents RAG 🌱
app.include_router(ocr_router, tags=["OCR Multilingue DZ"])  # OCR arabe/français/anglais 📄
app.include_router(darija_router, tags=["Darija NLP"])  # NLP Darija algérienne 🇩🇿
app.include_router(stt_router, tags=["STT Voice DZ"])  # Speech-to-Text arabe/darija 🎙️
app.include_router(tts_router, tags=["TTS Voice DZ"])  # Text-to-Speech arabe/darija 🔊
app.include_router(voice_agent_router, tags=["Voice Agent DZ"])  # Agent vocal complet 🤖🎤
app.include_router(multi_llm_router, tags=["Multi-LLM"])  # Multi-providers IA + Crédit Manager 🤖💳
app.include_router(team_seats_router, tags=["Team Seats"])  # ChatGPT Team Seats Manager 👥
app.include_router(dzirvideo.router, prefix="/api", tags=["Dzir IA Video"])  # Dzir IA Video - Génération vidéo IA 🎬🇩🇿
app.include_router(growth_grid.router, tags=["Growth Grid"])  # Business Plan Generator IA 📈
app.include_router(notebook_lm.router, tags=["Notebook LM"])  # Document Q&A avec RAG 📚
app.include_router(prompt_creator.router, tags=["Prompt Creator"])  # Générateur de prompts pro ✨
app.include_router(promo_codes.router, tags=["Promo Codes"])  # Codes promo lancement 30 clients 🎉
app.include_router(agents.router, tags=["IA Factory Agents"])  # 7 Agents IA Pro (Finance, Legal, Recruitment, Real Estate, Travel, Teaching) 🤖
app.include_router(tenants.router, tags=["Tenants"])  # Multi-Tenant Management 🏢
app.include_router(chat_rooms.router, tags=["Chat Rooms"])  # Chat Multi-User Rooms 💬
app.include_router(websocket_router.router, tags=["WebSocket"])

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time(), "service": "IAFactory"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def root():
    return {"message": "IAFactory API", "docs": "/docs"}
