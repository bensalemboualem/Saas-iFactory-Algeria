"""
Translation API Endpoint
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from app.models.requests import TranslateRequest, BatchTranslateRequest
from app.models.responses import TranslateResponse, BatchTranslateResponse, ErrorResponse
from app.services.ai_providers.openai_service import OpenAIService
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/translator", tags=["Translation"])


# Dependency
def get_openai_service() -> OpenAIService:
    """Get OpenAI service instance"""
    return OpenAIService()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate text",
    description="""
    Translate text between supported languages.
    
    **Supported languages**: FR, AR, EN, ES, DE, IT
    
    **Use cases**:
    - rag-dz: FR ↔ AR translations for Algerian market
    - Helvetia: FR ↔ EN translations for Swiss market
    
    **Rate limit**: 60 requests/minute per user
    """
)
async def translate_text(
    request: TranslateRequest,
    service: OpenAIService = Depends(get_openai_service)
) -> TranslateResponse:
    """
    Translate text from source language to target language
    
    Example:
    ```json
    {
        "text": "Bonjour le monde",
        "source_language": "fr",
        "target_language": "ar",
        "preserve_formatting": true,
        "tenant_id": "rag-dz"
    }
    ```
    """
    try:
        # Check if tool is enabled
        if not settings.ENABLE_TRANSLATOR:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Translation service is currently disabled"
            )
        
        # Validate languages are supported
        if request.source_language.value not in settings.supported_languages_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Source language '{request.source_language}' not supported"
            )
        
        if request.target_language.value not in settings.supported_languages_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Target language '{request.target_language}' not supported"
            )
        
        # Perform translation
        result = await service.translate(request)
        
        logger.info(
            f"Translation completed: {request.source_language} -> {request.target_language}, "
            f"chars: {result.character_count}, tenant: {request.tenant_id}"
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.post(
    "/translate/batch",
    response_model=BatchTranslateResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch translate multiple texts",
    description="Translate multiple texts in a single request (max 100 texts)"
)
async def batch_translate(
    request: BatchTranslateRequest,
    service: OpenAIService = Depends(get_openai_service)
) -> BatchTranslateResponse:
    """
    Batch translate multiple texts
    
    Example:
    ```json
    {
        "texts": [
            "Bonjour",
            "Comment allez-vous?",
            "Merci beaucoup"
        ],
        "source_language": "fr",
        "target_language": "ar",
        "tenant_id": "rag-dz"
    }
    ```
    """
    try:
        if not settings.ENABLE_TRANSLATOR:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Translation service is currently disabled"
            )
        
        # Perform batch translation
        translations = await service.batch_translate(
            texts=request.texts,
            source_language=request.source_language,
            target_language=request.target_language
        )
        
        total_chars = sum(t.character_count for t in translations)
        
        logger.info(
            f"Batch translation completed: {len(translations)} texts, "
            f"total chars: {total_chars}, tenant: {request.tenant_id}"
        )
        
        return BatchTranslateResponse(
            translations=translations,
            total_characters=total_chars,
            provider="openai"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch translation failed: {str(e)}"
        )


@router.get(
    "/languages",
    summary="Get supported languages",
    description="List all supported languages for translation"
)
async def get_supported_languages():
    """Get list of supported languages"""
    languages = {
        "fr": {"name": "French", "native": "Français"},
        "ar": {"name": "Arabic", "native": "العربية"},
        "en": {"name": "English", "native": "English"},
        "es": {"name": "Spanish", "native": "Español"},
        "de": {"name": "German", "native": "Deutsch"},
        "it": {"name": "Italian", "native": "Italiano"}
    }
    
    return {
        "supported_languages": [
            {
                "code": code,
                "name": details["name"],
                "native_name": details["native"]
            }
            for code, details in languages.items()
            if code in settings.supported_languages_list
        ]
    }


@router.get(
    "/health",
    summary="Translation service health check"
)
async def translation_health(
    service: OpenAIService = Depends(get_openai_service)
):
    """Check if translation service is operational"""
    try:
        is_healthy = await service.health_check()
        
        if is_healthy:
            return {
                "status": "healthy",
                "provider": "openai",
                "enabled": settings.ENABLE_TRANSLATOR
            }
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "provider": "openai",
                    "enabled": settings.ENABLE_TRANSLATOR
                }
            )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "error": str(e)
            }
        )
