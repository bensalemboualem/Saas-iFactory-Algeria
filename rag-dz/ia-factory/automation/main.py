"""
IA Factory Automation - Main API
Agrège tous les modules d'automatisation
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime

# Import des modules
from workflows.lead_generation import router as leads_router
from workflows.proposal_automation import router as proposals_router
from workflows.social_media_manager import router as social_router
from workflows.digital_twin import router as twin_router
from teaching_assistant.module import router as teaching_router
from multi_tenant.infrastructure import router as infra_router
from analytics.dashboard import router as analytics_router

# Import des Claude Skills
from claude_skills.docx_generator import router as docx_router
from claude_skills.pptx_generator import router as pptx_router
from claude_skills.xlsx_generator import router as xlsx_router
from claude_skills.pdf_generator import router as pdf_router
from claude_skills.frontend_generator import router as frontend_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager"""
    print("🚀 IA Factory Automation API Starting...")
    print("📦 Modules loaded:")
    print("   - Lead Generation")
    print("   - Proposal Automation")
    print("   - Social Media Manager")
    print("   - Digital Twin Boualem")
    print("   - Teaching Assistant")
    print("   - Multi-tenant Infrastructure")
    print("   - Analytics Dashboard")
    print("🎨 Claude Skills loaded:")
    print("   - DOCX Generator")
    print("   - PPTX Generator")
    print("   - XLSX Generator")
    print("   - PDF Generator")
    print("   - Frontend Generator")
    yield
    print("👋 IA Factory Automation API Shutting down...")


app = FastAPI(
    title="IA Factory Automation API",
    description="""
# IA Factory - Système d'Automatisation Complet

API d'automatisation pour IA Factory couvrant:

## 🎯 Lead Generation
Capture, qualification et scoring automatique des prospects

## 📄 Proposal Automation  
Génération automatique de propositions commerciales avec pricing intelligent

## 📱 Social Media Manager
Création et planification de contenu réseaux sociaux style Boualem

## 🤖 Digital Twin Boualem
Clone IA authentique pour génération de contenu et conseil stratégique

## 📚 Teaching Assistant
Assistant pédagogique pour établissements scolaires DZ

## 🏗️ Multi-tenant Infrastructure
Gestion de l'infrastructure multi-clients (Proxmox + LXC)

## 📝 Claude Skills - Document Generation
- **DOCX**: Propositions, contrats, rapports, spécifications
- **PPTX**: Pitch decks, présentations commerciales, formations
- **XLSX**: Factures, budgets, tableaux de bord, CRM
- **PDF**: Rapports PDF, certificats, brochures
- **Frontend**: Composants UI, landing pages, dashboards

---
**Version:** 1.0.0  
**Contact:** contact@iafactory.ch  
**Documentation:** https://docs.iafactory.ch
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads_router)
app.include_router(proposals_router)
app.include_router(social_router)
app.include_router(twin_router)
app.include_router(teaching_router)
app.include_router(infra_router)
app.include_router(analytics_router)

# Claude Skills routers
app.include_router(docx_router)
app.include_router(pptx_router)
app.include_router(xlsx_router)
app.include_router(pdf_router)
app.include_router(frontend_router)


@app.get("/", tags=["Root"])
async def root():
    """Page d'accueil de l'API"""
    return {
        "name": "IA Factory Automation API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "modules": [
            {"name": "Lead Generation", "path": "/leads", "status": "active"},
            {"name": "Proposals", "path": "/proposals", "status": "active"},
            {"name": "Social Media", "path": "/social", "status": "active"},
            {"name": "Digital Twin", "path": "/twin", "status": "active"},
            {"name": "Teaching", "path": "/teaching", "status": "active"},
            {"name": "Infrastructure", "path": "/infra", "status": "active"},
        ],
        "skills": [
            {"name": "DOCX Generator", "path": "/skills/docx", "status": "active"},
            {"name": "PPTX Generator", "path": "/skills/pptx", "status": "active"},
            {"name": "XLSX Generator", "path": "/skills/xlsx", "status": "active"},
            {"name": "PDF Generator", "path": "/skills/pdf", "status": "active"},
            {"name": "Frontend Generator", "path": "/skills/frontend", "status": "active"},
        ],
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "contact": {
            "email": "contact@iafactory.ch",
            "website": "https://iafactory.ch"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "up",
            "database": "simulated",
            "cache": "simulated"
        }
    }


@app.get("/metrics", tags=["Metrics"])
async def get_metrics():
    """Métriques globales de l'API"""
    return {
        "timestamp": datetime.now().isoformat(),
        "uptime": "active",
        "requests": {
            "total": 0,
            "success": 0,
            "errors": 0
        },
        "modules": {
            "leads": {"status": "active", "processed": 0},
            "proposals": {"status": "active", "generated": 0},
            "social": {"status": "active", "posts_scheduled": 0},
            "teaching": {"status": "active", "content_generated": 0},
            "infra": {"status": "active", "tenants_active": 0}
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global des exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": str(request.url),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
