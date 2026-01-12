"""
Multi-LLM + Crédit Manager
==========================
Module de gestion multi-providers IA avec comptage de tokens et crédits
Permet aux clients algériens d'utiliser OpenAI, Anthropic, Groq, etc. via IAFactory
"""

from .multi_llm_router import router as multi_llm_router
from .multi_llm_service import MultiLLMService, multi_llm_service
from .multi_llm_models import (
    AIProvider, AIModel, AIUsageLog,
    LLMModelInfo, ChatRequest, ChatResponse,
    LLMProviderType, LLMModelType,
)

__all__ = [
    "multi_llm_router",
    "MultiLLMService",
    "multi_llm_service",
    "AIProvider",
    "AIModel", 
    "AIUsageLog",
    "LLMModelInfo",
    "ChatRequest",
    "ChatResponse",
    "LLMProviderType",
    "LLMModelType",
]
