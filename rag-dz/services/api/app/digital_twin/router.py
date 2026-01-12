"""
FastAPI Router pour Digital Twin (Agent Double)
API endpoints pour lexique personnel, ROI, et analyses émotionnelles
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from datetime import datetime
import logging

from . import repository as twin_repo
from ..dependencies import get_current_tenant_id

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/digital-twin",
    tags=["digital-twin"],
)


@router.get("/lexicon")
async def get_user_lexicon(
    tenant_id: str = Depends(get_current_tenant_id),
    user_id: int = Query(1, description="User ID"),
    professional_domain: Optional[str] = Query(None, description="Filter by domain: medical, legal, accounting"),
    limit: int = Query(100, description="Maximum number of terms to return", ge=1, le=500),
):
    """
    Récupère le lexique personnel d'un utilisateur

    **Lexique Privé**: Vocabulaire professionnel extrait automatiquement
    des transcriptions (médecins, avocats, experts-comptables)

    **Paramètres**:
    - `user_id`: ID de l'utilisateur
    - `professional_domain`: Filtrer par domaine (medical, legal, accounting)
    - `limit`: Nombre maximum de termes (défaut: 100, max: 500)

    **Réponse**:
    ```json
    {
      "lexicon": [
        {
          "term": "anamnèse",
          "term_type": "medical_term",
          "professional_domain": "medical",
          "frequency_count": 23,
          "last_used_at": "2025-01-16T14:30:00Z",
          "definition": "Historique médical du patient",
          "emotional_tag": "technical",
          "cultural_context": "universal",
          "confidence_score": 0.95
        }
      ],
      "total_terms": 156,
      "user_id": 1
    }
    ```

    **Use Cases**:
    - **Médecins**: Termes médicaux spécialisés (anamnèse, dyspnée, érythème)
    - **Avocats**: Jargon juridique (conclusions, requête, ordonnance)
    - **Experts-comptables**: Terminologie fiscale (provisions, amortissement)
    """
    try:
        lexicon = twin_repo.get_user_lexicon(
            tenant_id=tenant_id,
            user_id=user_id,
            professional_domain=professional_domain,
            limit=limit,
        )

        logger.info(
            f"📚 Lexique récupéré: user={user_id}, tenant={tenant_id}, "
            f"domain={professional_domain}, count={len(lexicon)}"
        )

        return jsonable_encoder({
            "lexicon": lexicon,
            "total_terms": len(lexicon),
            "user_id": user_id,
            "professional_domain": professional_domain,
        })

    except Exception as e:
        logger.error(f"Erreur get_user_lexicon: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roi/stats")
async def get_roi_statistics(
    tenant_id: str = Depends(get_current_tenant_id),
    start_date: Optional[str] = Query(None, description="Start date (ISO 8601)"),
    end_date: Optional[str] = Query(None, description="End date (ISO 8601)"),
):
    """
    Calcule les statistiques ROI: Tokens économisés

    **ROI Faster-Whisper vs Cloud APIs**:
    - Local Faster-Whisper: **GRATUIT** (0 tokens)
    - OpenAI Whisper API: ~$0.006/minute → 60 tokens/minute équivalent

    **Métriques**:
    - `total_tokens_saved`: Total tokens économisés
    - `total_transcriptions`: Nombre de transcriptions
    - `total_hours_transcribed`: Heures totales transcrites

    **Réponse**:
    ```json
    {
      "total_tokens_saved": 145000,
      "total_transcriptions": 423,
      "total_hours_transcribed": 40.5,
      "period": {
        "start_date": "2025-01-01T00:00:00Z",
        "end_date": "2025-01-16T23:59:59Z"
      },
      "cost_comparison": {
        "local_cost_usd": 0.0,
        "cloud_equivalent_cost_usd": 870.0,
        "savings_usd": 870.0
      }
    }
    ```

    **Use Cases**:
    - **Tableau de bord client**: Montrer l'économie réalisée
    - **Argument de vente**: Prouver le ROI de la solution souveraine
    - **Reporting financier**: Justifier l'investissement IA
    """
    try:
        # Parse dates si fournies
        parsed_start = None
        parsed_end = None

        if start_date:
            try:
                parsed_start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO 8601.")

        if end_date:
            try:
                parsed_end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid end_date format. Use ISO 8601.")

        # Récupérer stats ROI
        stats = twin_repo.get_total_tokens_saved_stats(
            tenant_id=tenant_id,
            start_date=parsed_start,
            end_date=parsed_end,
        )

        # Calcul coût Cloud équivalent (approximation: $0.006/minute)
        total_minutes = stats["total_hours_transcribed"] * 60
        cloud_cost_usd = total_minutes * 0.006

        logger.info(
            f"💰 ROI stats: tenant={tenant_id}, saved={stats['total_tokens_saved']} tokens, "
            f"hours={stats['total_hours_transcribed']:.1f}, savings=${cloud_cost_usd:.2f}"
        )

        return jsonable_encoder({
            "total_tokens_saved": stats["total_tokens_saved"],
            "total_transcriptions": stats["total_transcriptions"],
            "total_hours_transcribed": stats["total_hours_transcribed"],
            "period": {
                "start_date": start_date or "all_time",
                "end_date": end_date or datetime.now().isoformat(),
            },
            "cost_comparison": {
                "local_cost_usd": 0.0,
                "cloud_equivalent_cost_usd": round(cloud_cost_usd, 2),
                "savings_usd": round(cloud_cost_usd, 2),
            },
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur get_roi_statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check du service Digital Twin

    **Réponse**:
    ```json
    {
      "status": "healthy",
      "service": "digital-twin",
      "features": [
        "personal_lexicon",
        "emotion_analysis",
        "roi_tracking",
        "cultural_context"
      ],
      "ready": true
    }
    ```
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "digital-twin",
            "features": [
                "personal_lexicon",
                "emotion_analysis",
                "roi_tracking",
                "cultural_context",
                "heritage_detection",
                "stress_analysis",
            ],
            "ready": True,
        }
    )
