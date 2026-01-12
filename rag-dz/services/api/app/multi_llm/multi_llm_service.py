"""
Multi-LLM Service
=================
Logique métier pour gestion des appels LLM multi-providers avec comptage crédits
"""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any
from collections import defaultdict

from .multi_llm_models import (
    AIModel, AIUsageLog, LLMModelInfo,
    ChatRequest, ChatResponse, ChatMessage,
    ModelsListResponse, UsageHistoryItem, UsageHistoryResponse, UsageSummaryResponse,
    DEFAULT_MODELS, MODELS_BY_CODE, LLMModelTier, LLMProviderType, LLMModelType,
)
from .providers_client import call_llm, LLMResponse

# Import Billing V2 service
from app.clients.gateway_client import gateway
from ..models.billing_models import ServiceType

logger = logging.getLogger(__name__)


# ============================================
# In-Memory Storage (MVP - à migrer vers PostgreSQL)
# ============================================

usage_logs: List[AIUsageLog] = []


# ============================================
# Multi-LLM Service
# ============================================

class MultiLLMService:
    """Service principal pour Multi-LLM avec gestion des crédits"""
    
    def __init__(self):
        self.models = {m.code: m for m in DEFAULT_MODELS}
        self.default_model = "openai.gpt-4o-mini"  # Économique par défaut
    
    # ========================================
    # Models Management
    # ========================================
    
    def list_models(
        self,
        tier: Optional[LLMModelTier] = None,
        provider: Optional[LLMProviderType] = None,
        model_type: Optional[LLMModelType] = None,
        include_inactive: bool = False,
    ) -> ModelsListResponse:
        """
        Lister les modèles disponibles
        
        Args:
            tier: Filtrer par tier (FREE, BASIC, STANDARD, PREMIUM, ULTRA)
            provider: Filtrer par provider (openai, anthropic, groq, etc.)
            model_type: Filtrer par type (chat, image_gen, video_gen, tts, etc.)
            include_inactive: Inclure les modèles désactivés
        
        Returns:
            ModelsListResponse avec la liste des modèles
        """
        models = list(self.models.values())
        
        # Filtres
        if not include_inactive:
            models = [m for m in models if m.is_active]
        
        if tier:
            models = [m for m in models if m.tier == tier]
        
        if provider:
            models = [m for m in models if m.code.startswith(provider.value)]
        
        if model_type:
            models = [m for m in models if m.type == model_type]
        
        # Convertir en ModelInfo
        model_infos = []
        for m in models:
            provider_type = LLMProviderType(m.code.split(".")[0]) if "." in m.code else LLMProviderType.OPENAI
            
            model_infos.append(LLMModelInfo(
                code=m.code,
                display_name=m.display_name,
                provider=provider_type,
                type=m.type,
                tier=m.tier,
                cost_credits_per_1k=m.cost_credits_per_1k,
                max_tokens=m.max_tokens,
                context_window=m.context_window,
                supports_vision=m.supports_vision,
                supports_tools=m.supports_tools,
                supports_streaming=m.supports_streaming,
                is_default=m.is_default,
                description=m.description,
            ))
        
        # Trouver le modèle par défaut
        default = next((m.code for m in models if m.is_default), self.default_model)
        
        return ModelsListResponse(
            success=True,
            models=model_infos,
            total=len(model_infos),
            default_model=default,
        )
    
    def get_model(self, model_code: str) -> Optional[AIModel]:
        """Récupérer un modèle par son code"""
        return self.models.get(model_code)
    
    # ========================================
    # Chat Completion
    # ========================================
    
    async def chat(
        self,
        user_id: str,
        request: ChatRequest,
        check_credits: bool = True,
    ) -> ChatResponse:
        """
        Exécuter une requête chat avec comptage des crédits
        
        Args:
            user_id: ID de l'utilisateur
            request: ChatRequest avec model et messages
            check_credits: Vérifier et déduire les crédits (True par défaut)
        
        Returns:
            ChatResponse avec la réponse et les métriques
        
        Raises:
            ValueError: Si modèle inconnu ou crédits insuffisants
        """
        import uuid
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        
        # 1. Vérifier que le modèle existe
        model = self.get_model(request.model)
        if not model:
            # Fallback: essayer sans le préfixe provider
            for code, m in self.models.items():
                if request.model in code or code.endswith(request.model):
                    model = m
                    request.model = code
                    break
        
        if not model:
            raise ValueError(f"Unknown model: {request.model}")
        
        if not model.is_active:
            raise ValueError(f"Model {request.model} is not active")
        
        # 2. Estimer les tokens (approximation avant appel)
        estimated_input_tokens = self._estimate_tokens(request.messages)
        estimated_total = estimated_input_tokens + (request.max_tokens or model.max_tokens)
        estimated_credits = max(1, int((estimated_total / 1000) * model.cost_credits_per_1k))
        
        # 3. Vérifier les crédits
        if check_credits:
            can_consume, cost, available = billing_service.can_consume(user_id, ServiceType.RAG_QUERY)
            user_credits = billing_service.get_or_create_user_credits(user_id)
            
            if user_credits.total_available < estimated_credits:
                raise ValueError(
                    f"Crédits insuffisants: {user_credits.total_available} disponibles, "
                    f"~{estimated_credits} requis pour {model.display_name}"
                )
        
        # 4. Appeler le LLM
        messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
        
        try:
            llm_response: LLMResponse = await call_llm(
                model_code=request.model,
                messages=messages_dict,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
        except Exception as e:
            logger.error(f"LLM call failed for {request.model}: {e}")
            raise ValueError(f"LLM call failed: {str(e)}")
        
        # 5. Calculer les crédits réels
        tokens_total = llm_response.tokens_total
        credits_consumed = max(1, int((tokens_total / 1000) * model.cost_credits_per_1k))
        
        # Coût USD estimé
        cost_usd = (
            (Decimal(llm_response.tokens_input) / 1000) * model.cost_usd_input_per_1k +
            (Decimal(llm_response.tokens_output) / 1000) * model.cost_usd_output_per_1k
        )
        
        # 6. Déduire les crédits via Billing V2
        if check_credits:
            consume_result = billing_service.consume_credits(
                user_id=user_id,
                service_type=ServiceType.RAG_QUERY,  # TODO: Ajouter ServiceType.LLM_CHAT
                credits_override=credits_consumed,
                metadata={
                    "model": request.model,
                    "tokens_input": llm_response.tokens_input,
                    "tokens_output": llm_response.tokens_output,
                    "request_id": request_id,
                },
            )
            remaining_credits = consume_result.balance_after
        else:
            remaining_credits = billing_service.get_or_create_user_credits(user_id).total_available
        
        # 7. Logger l'usage
        usage_log = AIUsageLog(
            user_id=user_id,
            model_id=model.id,
            model_code=model.code,
            tokens_input=llm_response.tokens_input,
            tokens_output=llm_response.tokens_output,
            tokens_total=tokens_total,
            credits_consumed=credits_consumed,
            cost_usd_estimated=cost_usd,
            latency_ms=llm_response.latency_ms,
            success=True,
        )
        usage_logs.append(usage_log)
        
        logger.info(
            f"User {user_id} used {model.code}: "
            f"{tokens_total} tokens, {credits_consumed} credits, ${cost_usd:.4f}"
        )
        
        # 8. Retourner la réponse
        return ChatResponse(
            success=True,
            request_id=request_id,
            answer=llm_response.content,
            model=llm_response.model,
            model_display_name=model.display_name,
            tokens_input=llm_response.tokens_input,
            tokens_output=llm_response.tokens_output,
            tokens_total=tokens_total,
            credits_used=credits_consumed,
            credits_remaining=remaining_credits,
            cost_usd_estimated=float(cost_usd),
            latency_ms=llm_response.latency_ms,
            finish_reason=llm_response.finish_reason,
        )
    
    # ========================================
    # Usage Statistics
    # ========================================
    
    def get_usage_history(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> UsageHistoryResponse:
        """
        Récupérer l'historique d'usage d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            limit: Nombre max de résultats
            offset: Pagination
            start_date: Filtrer depuis cette date
            end_date: Filtrer jusqu'à cette date
        
        Returns:
            UsageHistoryResponse avec l'historique
        """
        # Filtrer par user
        user_logs = [log for log in usage_logs if log.user_id == user_id]
        
        # Filtrer par date
        if start_date:
            user_logs = [log for log in user_logs if log.created_at >= start_date]
        if end_date:
            user_logs = [log for log in user_logs if log.created_at <= end_date]
        
        # Trier par date décroissante
        user_logs.sort(key=lambda x: x.created_at, reverse=True)
        
        # Totaux
        total_credits = sum(log.credits_consumed for log in user_logs)
        total_cost = sum(float(log.cost_usd_estimated) for log in user_logs)
        
        # Paginer
        paginated = user_logs[offset:offset + limit]
        
        # Convertir en items
        items = []
        for log in paginated:
            model = self.get_model(log.model_code)
            items.append(UsageHistoryItem(
                id=log.id,
                model_code=log.model_code,
                model_display_name=model.display_name if model else log.model_code,
                tokens_input=log.tokens_input,
                tokens_output=log.tokens_output,
                credits_consumed=log.credits_consumed,
                cost_usd=float(log.cost_usd_estimated),
                success=log.success,
                latency_ms=log.latency_ms,
                created_at=log.created_at,
            ))
        
        return UsageHistoryResponse(
            success=True,
            user_id=user_id,
            items=items,
            total_items=len(user_logs),
            total_credits_used=total_credits,
            total_cost_usd=total_cost,
            period_start=start_date,
            period_end=end_date,
        )
    
    def get_usage_summary(
        self,
        user_id: str,
        period: str = "7d",  # "7d", "30d", "all"
    ) -> UsageSummaryResponse:
        """
        Récupérer le résumé d'usage d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            period: Période ("7d", "30d", "all")
        
        Returns:
            UsageSummaryResponse avec le résumé
        """
        # Filtrer par user
        user_logs = [log for log in usage_logs if log.user_id == user_id]
        
        # Filtrer par période
        now = datetime.now()
        if period == "7d":
            cutoff = now - timedelta(days=7)
            user_logs = [log for log in user_logs if log.created_at >= cutoff]
        elif period == "30d":
            cutoff = now - timedelta(days=30)
            user_logs = [log for log in user_logs if log.created_at >= cutoff]
        
        # Totaux
        total_requests = len(user_logs)
        total_tokens = sum(log.tokens_total for log in user_logs)
        total_credits = sum(log.credits_consumed for log in user_logs)
        total_cost = sum(float(log.cost_usd_estimated) for log in user_logs)
        
        # Par modèle
        usage_by_model: Dict[str, Dict] = defaultdict(lambda: {"requests": 0, "tokens": 0, "credits": 0})
        for log in user_logs:
            usage_by_model[log.model_code]["requests"] += 1
            usage_by_model[log.model_code]["tokens"] += log.tokens_total
            usage_by_model[log.model_code]["credits"] += log.credits_consumed
        
        # Par jour (7 derniers jours)
        daily_usage = []
        for i in range(7):
            day = (now - timedelta(days=i)).date()
            day_logs = [log for log in user_logs if log.created_at.date() == day]
            daily_usage.append({
                "date": day.isoformat(),
                "requests": len(day_logs),
                "tokens": sum(log.tokens_total for log in day_logs),
                "credits": sum(log.credits_consumed for log in day_logs),
            })
        
        daily_usage.reverse()  # Chronologique
        
        return UsageSummaryResponse(
            success=True,
            user_id=user_id,
            total_requests=total_requests,
            total_tokens=total_tokens,
            total_credits=total_credits,
            total_cost_usd=total_cost,
            usage_by_model=dict(usage_by_model),
            daily_usage=daily_usage,
            period=period,
        )
    
    # ========================================
    # Helpers
    # ========================================
    
    def _estimate_tokens(self, messages: List[ChatMessage]) -> int:
        """Estimer le nombre de tokens d'entrée (approximation simple)"""
        total_chars = sum(len(m.content) for m in messages)
        # Approximation: 1 token ≈ 4 caractères en anglais, 2-3 en français/arabe
        return int(total_chars / 3)
    
    def get_pricing_table(self) -> Dict[str, Any]:
        """
        Obtenir la grille tarifaire IAFactory
        
        Returns:
            Dict avec les prix par tier et par modèle
        """
        pricing = {
            "currency": "DZD",
            "credits_to_dzd": 10,  # 1 crédit = 10 DA
            "tiers": {},
            "models": {},
        }
        
        # Par tier
        for tier in LLMModelTier:
            tier_models = [m for m in self.models.values() if m.tier == tier]
            if tier_models:
                avg_credits = sum(m.cost_credits_per_1k for m in tier_models) / len(tier_models)
                pricing["tiers"][tier.value] = {
                    "name": tier.value.title(),
                    "avg_credits_per_1k": avg_credits,
                    "models_count": len(tier_models),
                }
        
        # Par modèle
        for code, model in self.models.items():
            pricing["models"][code] = {
                "display_name": model.display_name,
                "tier": model.tier.value,
                "credits_per_1k": model.cost_credits_per_1k,
                "dzd_per_1k": model.cost_credits_per_1k * 10,
            }
        
        return pricing


# Singleton
multi_llm_service = MultiLLMService()
