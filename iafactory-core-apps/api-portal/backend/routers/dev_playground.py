"""
iaFactory API Portal - Playground
Module 16 - Console de test API sécurisée
"""

from datetime import datetime
from typing import Optional, Literal, Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import httpx
import json

from ..database import get_db
from ..auth import get_current_user
from ..models import User, ApiKey
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/dev/playground", tags=["Developer - Playground"])


# ==============================================
# SCHEMAS
# ==============================================

class PlaygroundRequest(BaseModel):
    """Requête pour le playground"""
    endpoint: Literal[
        "/api/v1/rag/query",
        "/api/v1/legal/ask",
        "/api/v1/fiscal/simulate",
        "/api/v1/park/sparkpage",
        "/api/v1/fiscal/g50",
        "/api/v1/legal/contract"
    ] = Field(..., description="Endpoint à tester")
    method: Literal["GET", "POST"] = Field("POST", description="Méthode HTTP")
    body: Optional[Dict[str, Any]] = Field(None, description="Corps de la requête JSON")
    api_key_id: Optional[str] = Field(None, description="ID de la clé API à utiliser (optionnel)")


class PlaygroundResponse(BaseModel):
    """Réponse du playground"""
    success: bool
    status_code: int
    latency_ms: int
    response_body: Any
    headers: Dict[str, str]
    credits_used: int
    timestamp: str


# ==============================================
# ENDPOINT CONFIGS
# ==============================================

ENDPOINT_CONFIGS = {
    "/api/v1/rag/query": {
        "description": "Interroger le système RAG",
        "method": "POST",
        "example_body": {
            "query": "Quels sont les taux de TVA en Algérie ?",
            "sources": ["dgi", "joradp"],
            "language": "fr",
            "max_results": 5
        },
        "credits_cost": 2
    },
    "/api/v1/legal/ask": {
        "description": "Poser une question juridique",
        "method": "POST",
        "example_body": {
            "question": "Comment créer une EURL en Algérie ?",
            "domain": "commercial",
            "include_sources": True
        },
        "credits_cost": 3
    },
    "/api/v1/fiscal/simulate": {
        "description": "Simuler des calculs fiscaux",
        "method": "POST",
        "example_body": {
            "type": "irg_salarie",
            "salaire_brut": 150000,
            "regime": "general",
            "annee": 2025
        },
        "credits_cost": 1
    },
    "/api/v1/park/sparkpage": {
        "description": "Générer une SparkPage (landing page)",
        "method": "POST",
        "example_body": {
            "title": "Mon Entreprise DZ",
            "description": "Services professionnels en Algérie",
            "theme": "business",
            "language": "fr"
        },
        "credits_cost": 5
    },
    "/api/v1/fiscal/g50": {
        "description": "Générer un formulaire G50",
        "method": "POST",
        "example_body": {
            "periode": "2025-11",
            "chiffre_affaires": 5000000,
            "tva_collectee": 950000,
            "tva_deductible": 450000
        },
        "credits_cost": 2
    },
    "/api/v1/legal/contract": {
        "description": "Générer un modèle de contrat",
        "method": "POST",
        "example_body": {
            "type": "travail_cdi",
            "parties": {
                "employeur": "SARL ABC",
                "employe": "Ahmed Ben Ali"
            },
            "clauses": ["confidentialite", "non_concurrence"]
        },
        "credits_cost": 4
    }
}


# ==============================================
# ENDPOINTS
# ==============================================

@router.get("/endpoints")
async def get_available_endpoints():
    """
    Liste les endpoints disponibles pour le playground
    avec leurs configurations et exemples
    """
    return {
        "endpoints": [
            {
                "path": path,
                "description": config["description"],
                "method": config["method"],
                "example_body": config["example_body"],
                "credits_cost": config["credits_cost"]
            }
            for path, config in ENDPOINT_CONFIGS.items()
        ]
    }


@router.post("/execute", response_model=PlaygroundResponse)
async def execute_playground(
    request: PlaygroundRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Exécute une requête API via le playground
    
    Cette route permet de tester l'API sans exposer la clé API dans le frontend.
    Le backend utilise une clé de l'utilisateur ou en crée une temporaire.
    """
    import time
    import os
    
    # Récupérer une clé active de l'utilisateur
    if request.api_key_id:
        import uuid
        try:
            key_uuid = uuid.UUID(request.api_key_id)
            key_result = await db.execute(
                select(ApiKey)
                .where(ApiKey.id == key_uuid)
                .where(ApiKey.user_id == current_user.id)
                .where(ApiKey.status == "active")
            )
            api_key = key_result.scalar_one_or_none()
        except ValueError:
            api_key = None
    else:
        # Utiliser la première clé active
        key_result = await db.execute(
            select(ApiKey)
            .where(ApiKey.user_id == current_user.id)
            .where(ApiKey.status == "active")
            .limit(1)
        )
        api_key = key_result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="Aucune clé API active. Créez une clé dans la section 'API Keys'."
        )
    
    # Configuration de l'endpoint
    endpoint_config = ENDPOINT_CONFIGS.get(request.endpoint)
    if not endpoint_config:
        raise HTTPException(
            status_code=400,
            detail=f"Endpoint non supporté: {request.endpoint}"
        )
    
    # URL de l'API interne
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8180")
    full_url = f"{api_base_url}{request.endpoint}"
    
    # Préparer le body
    body = request.body or endpoint_config["example_body"]
    
    # Exécuter la requête
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Note: On utilise le key_hash pour reconstituer une clé de test
            # En production, il faudrait un système de clés internes
            headers = {
                "Authorization": f"Bearer PLAYGROUND_TOKEN_{current_user.id}",
                "Content-Type": "application/json",
                "X-Playground-Request": "true",
                "X-User-ID": str(current_user.id)
            }
            
            if request.method == "POST":
                response = await client.post(full_url, json=body, headers=headers)
            else:
                response = await client.get(full_url, headers=headers)
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Parser la réponse
            try:
                response_body = response.json()
            except json.JSONDecodeError:
                response_body = {"raw": response.text}
            
            # Extraire les headers pertinents
            response_headers = {
                k: v for k, v in response.headers.items()
                if k.lower() in ["x-request-id", "x-credits-used", "x-rate-limit-remaining"]
            }
            
            # Crédits utilisés
            credits_used = int(response.headers.get("X-Credits-Used", endpoint_config["credits_cost"]))
            
            return PlaygroundResponse(
                success=response.status_code < 400,
                status_code=response.status_code,
                latency_ms=latency_ms,
                response_body=response_body,
                headers=response_headers,
                credits_used=credits_used,
                timestamp=datetime.utcnow().isoformat()
            )
            
    except httpx.TimeoutException:
        latency_ms = int((time.time() - start_time) * 1000)
        return PlaygroundResponse(
            success=False,
            status_code=504,
            latency_ms=latency_ms,
            response_body={"error": "Request timeout after 30 seconds"},
            headers={},
            credits_used=0,
            timestamp=datetime.utcnow().isoformat()
        )
    except httpx.RequestError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return PlaygroundResponse(
            success=False,
            status_code=503,
            latency_ms=latency_ms,
            response_body={"error": f"Connection error: {str(e)}"},
            headers={},
            credits_used=0,
            timestamp=datetime.utcnow().isoformat()
        )


@router.get("/docs/{endpoint_name}")
async def get_endpoint_documentation(
    endpoint_name: str,
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la documentation détaillée d'un endpoint
    """
    # Mapper le nom vers le path
    endpoint_map = {
        "rag": "/api/v1/rag/query",
        "legal": "/api/v1/legal/ask",
        "fiscal": "/api/v1/fiscal/simulate",
        "park": "/api/v1/park/sparkpage",
        "g50": "/api/v1/fiscal/g50",
        "contract": "/api/v1/legal/contract"
    }
    
    endpoint_path = endpoint_map.get(endpoint_name)
    if not endpoint_path:
        raise HTTPException(status_code=404, detail="Endpoint non trouvé")
    
    config = ENDPOINT_CONFIGS.get(endpoint_path)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration non trouvée")
    
    # Documentation détaillée
    docs = {
        "/api/v1/rag/query": {
            "title": "RAG Query",
            "description": "Interroge le système RAG (Retrieval-Augmented Generation) avec des sources officielles algériennes.",
            "authentication": "Bearer token requis (Header: Authorization: Bearer IAFK_XXXXX)",
            "rate_limit": "100 requêtes/minute",
            "request_body": {
                "query": {"type": "string", "required": True, "description": "Question à poser"},
                "sources": {"type": "array", "required": False, "description": "Sources à interroger: dgi, joradp, cnrc, cnas"},
                "language": {"type": "string", "required": False, "description": "Langue de réponse: fr, ar"},
                "max_results": {"type": "integer", "required": False, "description": "Nombre max de sources (1-10)"}
            },
            "response": {
                "answer": "Réponse générée par l'IA",
                "sources": "Liste des sources utilisées avec citations",
                "confidence": "Score de confiance (0-1)"
            },
            "curl_example": """curl -X POST https://api.iafactoryalgeria.com/api/v1/rag/query \\
  -H "Authorization: Bearer IAFK_live_xxxxx" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "Quels sont les taux de TVA en Algérie ?", "sources": ["dgi"]}'""",
            "js_example": """const response = await fetch('https://api.iafactoryalgeria.com/api/v1/rag/query', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer IAFK_live_xxxxx',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'Quels sont les taux de TVA en Algérie ?',
    sources: ['dgi']
  })
});
const data = await response.json();"""
        },
        "/api/v1/legal/ask": {
            "title": "Legal Assistant",
            "description": "Assistant juridique IA spécialisé dans le droit algérien.",
            "authentication": "Bearer token requis",
            "rate_limit": "50 requêtes/minute",
            "request_body": {
                "question": {"type": "string", "required": True, "description": "Question juridique"},
                "domain": {"type": "string", "required": False, "description": "Domaine: commercial, travail, fiscal, civil"},
                "include_sources": {"type": "boolean", "required": False, "description": "Inclure les références légales"}
            },
            "curl_example": """curl -X POST https://api.iafactoryalgeria.com/api/v1/legal/ask \\
  -H "Authorization: Bearer IAFK_live_xxxxx" \\
  -H "Content-Type: application/json" \\
  -d '{"question": "Comment créer une EURL ?", "domain": "commercial"}'"""
        },
        "/api/v1/fiscal/simulate": {
            "title": "Fiscal Simulator",
            "description": "Simulateur fiscal pour calculs d'impôts et taxes en Algérie.",
            "authentication": "Bearer token requis",
            "rate_limit": "200 requêtes/minute",
            "request_body": {
                "type": {"type": "string", "required": True, "description": "Type: irg_salarie, irg_independant, ibs, tva, tap"},
                "salaire_brut": {"type": "number", "required": False, "description": "Pour IRG salarié"},
                "chiffre_affaires": {"type": "number", "required": False, "description": "Pour IBS/TAP"},
                "regime": {"type": "string", "required": False, "description": "Régime fiscal"}
            },
            "curl_example": """curl -X POST https://api.iafactoryalgeria.com/api/v1/fiscal/simulate \\
  -H "Authorization: Bearer IAFK_live_xxxxx" \\
  -H "Content-Type: application/json" \\
  -d '{"type": "irg_salarie", "salaire_brut": 150000}'"""
        }
    }
    
    return {
        "path": endpoint_path,
        "config": config,
        "documentation": docs.get(endpoint_path, {
            "title": endpoint_name.upper(),
            "description": config["description"]
        })
    }
