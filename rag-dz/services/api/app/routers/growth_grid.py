"""
Growth Grid API Router
Business Plan & Pitch Generator avec IA
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import sys
import os

# Add growth-grid backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../apps/growth-grid/backend'))

try:
    from growth_grid_service import growth_grid_service
except ImportError:
    growth_grid_service = None

router = APIRouter(
    prefix="/api/growth-grid",
    tags=["growth-grid"],
    responses={404: {"description": "Not found"}},
)

# Models
class BusinessPlanRequest(BaseModel):
    """Requête de génération de business plan"""
    projectType: str = Field(..., description="Type de projet (tech, ecommerce, food, etc.)")
    companyName: str = Field(..., description="Nom de l'entreprise")
    legalForm: Optional[str] = Field(None, description="Forme juridique")
    location: Optional[str] = Field(None, description="Localisation")
    shortDescription: str = Field(..., description="Description courte du projet")
    missionVision: Optional[str] = Field(None, description="Mission et vision")
    targetMarket: str = Field(..., description="Marché cible")
    problemSolved: Optional[str] = Field(None, description="Problème résolu")
    competition: Optional[str] = Field(None, description="Analyse concurrentielle")
    competitiveAdvantage: Optional[str] = Field(None, description="Avantages compétitifs")
    initialCapital: Optional[float] = Field(None, description="Capital initial (DZD)")
    fundingNeeded: Optional[float] = Field(None, description="Besoin de financement (DZD)")
    revenueModel: Optional[str] = Field(None, description="Modèle de revenus")
    revenueYear1: Optional[float] = Field(None, description="CA prévisionnel An 1")
    revenueYear3: Optional[float] = Field(None, description="CA prévisionnel An 3")
    monthlyExpenses: Optional[float] = Field(None, description="Charges mensuelles")
    language: str = Field("fr", description="Langue du plan (fr/ar/en)")
    detailLevel: str = Field("standard", description="Niveau de détail (concise/standard/detailed)")

class BusinessPlanResponse(BaseModel):
    """Réponse avec business plan généré"""
    content: str = Field(..., description="Contenu HTML du business plan")
    generated_at: str = Field(..., description="Date de génération")
    language: str = Field(..., description="Langue du plan")
    detail_level: str = Field(..., description="Niveau de détail")

class TemplateListResponse(BaseModel):
    """Liste des templates disponibles"""
    templates: List[Dict[str, str]]

# Endpoints
@router.post("/generate", response_model=BusinessPlanResponse)
async def generate_business_plan(request: BusinessPlanRequest):
    """
    Génère un business plan complet avec IA

    **Fonctionnalités:**
    - Génération avec Claude (Anthropic) ou GPT-4 (OpenAI)
    - Adaptation au marché algérien
    - Templates par secteur
    - Plusieurs langues (FR/AR/EN)
    - Niveaux de détail ajustables

    **Exemple:**
    ```json
    {
        "projectType": "tech",
        "companyName": "TechStart DZ",
        "shortDescription": "Plateforme SaaS pour PME algériennes",
        "targetMarket": "PME algériennes de 5-50 employés",
        "language": "fr",
        "detailLevel": "standard"
    }
    ```
    """

    if growth_grid_service is None:
        raise HTTPException(
            status_code=500,
            detail="Growth Grid service not available"
        )

    try:
        # Convert request to dict
        data = request.dict()

        # Generate business plan
        result = await growth_grid_service.generate_business_plan(
            data=data,
            language=request.language,
            detail_level=request.detailLevel
        )

        return BusinessPlanResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating business plan: {str(e)}"
        )

@router.get("/templates", response_model=TemplateListResponse)
async def list_templates():
    """
    Liste les templates disponibles par secteur

    Retourne la liste des secteurs supportés avec leurs templates pré-configurés.
    """

    templates = [
        {
            "id": "tech",
            "name": "Technologie & IT",
            "description": "SaaS, Apps, Web, Intelligence Artificielle",
            "icon": "💻"
        },
        {
            "id": "ecommerce",
            "name": "E-commerce",
            "description": "Boutique en ligne, Marketplace, Dropshipping",
            "icon": "🛒"
        },
        {
            "id": "food",
            "name": "Restauration",
            "description": "Restaurant, Café, Fast-food, Traiteur",
            "icon": "🍽️"
        },
        {
            "id": "retail",
            "name": "Commerce de détail",
            "description": "Boutique physique, Franchise, Distribution",
            "icon": "🏪"
        },
        {
            "id": "service",
            "name": "Services",
            "description": "Consulting, Agence, Freelance, B2B",
            "icon": "🤝"
        },
        {
            "id": "education",
            "name": "Éducation & Formation",
            "description": "Centre de formation, École, E-learning",
            "icon": "🎓"
        }
    ]

    return TemplateListResponse(templates=templates)

@router.get("/health")
async def health_check():
    """Vérifie le statut du service Growth Grid"""

    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    return {
        "status": "healthy",
        "service": "growth-grid",
        "ai_providers": {
            "anthropic": has_anthropic,
            "openai": has_openai
        },
        "fallback_templates": True
    }

@router.post("/export/pdf")
async def export_pdf(content: str):
    """
    Exporte le business plan en PDF

    TODO: Implémenter génération PDF avec WeasyPrint ou reportlab
    """

    raise HTTPException(
        status_code=501,
        detail="PDF export not implemented yet"
    )

@router.post("/export/docx")
async def export_docx(content: str):
    """
    Exporte le business plan en Word (DOCX)

    TODO: Implémenter génération DOCX avec python-docx
    """

    raise HTTPException(
        status_code=501,
        detail="DOCX export not implemented yet"
    )

@router.post("/export/pptx")
async def export_pptx(content: str):
    """
    Génère un pitch deck PowerPoint

    TODO: Implémenter génération PPTX avec python-pptx
    """

    raise HTTPException(
        status_code=501,
        detail="PPTX export not implemented yet"
    )
