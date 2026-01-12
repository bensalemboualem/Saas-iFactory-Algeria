"""
SafeLLMRouter - Routing intelligent multi-niveaux avec fallback ZÉRO RISQUE
Génère TOUJOURS une réponse, même si tous les providers payants tombent.

Architecture:
- Tier FREE → 100% Groq (gratuit)
- Tier ÉTUDIANT → 85% Groq / 15% OpenRouter (optimisé coûts)
- Tier PRO → 70% Groq / 30% OpenRouter (plus de qualité)
- Budget cap journalier → Auto-switch Groq si dépassé
- Fallback 3 niveaux → OpenRouter → Groq → Gemini Flash (Google gratuit)
"""
from enum import Enum
from typing import Optional, Dict, Any
import httpx
import redis.asyncio as redis
import logging
import os
from datetime import datetime, timedelta
import random
import asyncpg

from .quota_manager import get_quota_manager, QuotaManager

logger = logging.getLogger(__name__)


class UserTier(str, Enum):
    """Tiers d'abonnement utilisateur"""
    FREE = "free"
    STUDENT = "student"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Provider(str, Enum):
    """Providers disponibles avec priorité fallback"""
    OPENROUTER = "openrouter"  # Payant - qualité premium
    GROQ = "groq"              # Gratuit - rapide
    GEMINI_FLASH = "gemini"    # Gratuit - backup Google
    DEEPSEEK = "deepseek"      # Très cheap - backup payant


class SafeLLMRouter:
    """
    Router LLM avec fallback automatique ZÉRO RISQUE

    Garanties:
    - TOUJOURS une réponse (même si tous payants tombent)
    - Budget cap strict (pas de surprise facturation)
    - Routing optimisé par tier (équilibre coût/qualité)
    - Monitoring temps réel (logs usage pour billing)
    """

    def __init__(self):
        # Clients HTTP
        self.groq_client = httpx.AsyncClient(
            base_url="https://api.groq.com/openai/v1",
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
            timeout=30.0
        )

        self.openrouter_client = httpx.AsyncClient(
            base_url="https://openrouter.ai/api/v1",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "HTTP-Referer": "https://iafactoryalgeria.com",
                "X-Title": "IA Factory Algeria"
            },
            timeout=30.0
        )

        self.gemini_client = httpx.AsyncClient(
            base_url="https://openrouter.ai/api/v1",  # Via OpenRouter (gratuit)
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "HTTP-Referer": "https://iafactoryalgeria.com",
                "X-Title": "IA Factory Algeria - Gemini Fallback"
            },
            timeout=30.0
        )

        # Redis pour cache + budget tracking
        self.redis = redis.from_url(
            os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0"),
            decode_responses=True
        )

        # Budget protection
        self.daily_budget_usd = float(os.getenv("DAILY_BUDGET_USD", "50.0"))

        # Quota Manager (gestion messages user-friendly)
        self.quota_manager = get_quota_manager()

        # Routing percentages par tier
        self.routing_config = {
            UserTier.FREE: {
                "groq": 100,
                "openrouter": 0
            },
            UserTier.STUDENT: {
                "groq": 85,
                "openrouter": 15
            },
            UserTier.PRO: {
                "groq": 70,
                "openrouter": 30
            },
            UserTier.ENTERPRISE: {
                "groq": 50,
                "openrouter": 50
            }
        }

        # Modèles par provider
        self.models = {
            Provider.GROQ: "llama-3.3-70b-versatile",
            Provider.OPENROUTER: {
                "claude-sonnet-4": "anthropic/claude-sonnet-4-20250514",
                "gpt-4o": "openai/gpt-4o",
                "grok-2": "x-ai/grok-2-1212",
                "default": "openai/gpt-4o"  # Meilleur ratio qualité/prix
            },
            Provider.GEMINI_FLASH: "google/gemini-2.0-flash-exp:free",
            Provider.DEEPSEEK: "deepseek/deepseek-chat"
        }

    async def generate(
        self,
        user_id: int,
        prompt: str,
        model_choice: str = "gpt-4o",
        user_tier: UserTier = UserTier.FREE,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Génération avec fallback automatique multi-niveaux

        Flow:
        1. Check quota user (rate limiting)
        2. Check budget quotidien (protection coûts)
        3. Routing selon tier (FREE=Groq, STUDENT=85% Groq, etc.)
        4. Tentative provider principal
        5. Fallback niveau 2 si échec
        6. Fallback niveau 3 (Groq/Gemini garanti)

        Args:
            user_id: ID utilisateur
            prompt: Prompt utilisateur
            model_choice: Modèle demandé (claude-sonnet-4, gpt-4o, grok-2)
            user_tier: Tier abonnement (FREE, STUDENT, PRO)
            max_tokens: Tokens max génération
            temperature: Température créativité

        Returns:
            {
                "response": str,
                "model": str,
                "provider": str,
                "tokens": {"input": int, "output": int},
                "cost": float,
                "cached": bool
            }

        Raises:
            HTTPException si quota dépassé (sera géré par middleware)
        """

        # NIVEAU 0: Vérifications préalables
        if not await self._check_user_quota(user_id, user_tier):
            return {
                "error": "quota_exceeded",
                "message": self._get_quota_message(user_tier),
                "upgrade_url": "https://iafactoryalgeria.com/pricing",
                "provider": "none",
                "cost": 0
            }

        # NIVEAU 1: Décision routing selon tier
        provider_choice = self._route_provider(user_tier, model_choice)

        try:
            if provider_choice == Provider.GROQ:
                # FREE tier OU routing vers Groq (85% STUDENT, 70% PRO)
                response = await self._groq_generate(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                await self._log_usage(user_id, Provider.GROQ, response["tokens"], cost_usd=0)
                return response

            elif provider_choice == Provider.OPENROUTER:
                # STUDENT/PRO tier avec budget disponible
                if not await self._check_daily_budget():
                    # Budget dépassé → Fallback Groq
                    logger.warning(f"Budget cap reached, falling back to Groq for user {user_id}")
                    response = await self._groq_generate(prompt, max_tokens, temperature)
                    await self._log_usage(user_id, Provider.GROQ, response["tokens"], cost_usd=0)
                    response["budget_fallback"] = True
                    return response

                # Budget OK → Utiliser OpenRouter
                model_id = self.models[Provider.OPENROUTER].get(
                    model_choice,
                    self.models[Provider.OPENROUTER]["default"]
                )

                response = await self._openrouter_generate(
                    prompt,
                    model_id,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                await self._log_usage(
                    user_id,
                    Provider.OPENROUTER,
                    response["tokens"],
                    cost_usd=response["cost"]
                )
                return response

        except Exception as e:
            logger.error(f"Primary provider {provider_choice} failed: {e}")
            # FALLBACK automatique

        # NIVEAU 2: Fallback Groq (TOUJOURS disponible)
        try:
            logger.info(f"Falling back to Groq for user {user_id}")
            response = await self._groq_generate(prompt, max_tokens, temperature)
            await self._log_usage(user_id, Provider.GROQ, response["tokens"], cost_usd=0)
            response["fallback"] = True
            return response

        except Exception as e:
            logger.error(f"Groq fallback failed: {e}")

        # NIVEAU 3: Fallback Gemini Flash (Google gratuit via OpenRouter)
        try:
            logger.warning(f"Falling back to Gemini Flash (free) for user {user_id}")
            response = await self._gemini_flash_generate(prompt, max_tokens, temperature)
            await self._log_usage(user_id, Provider.GEMINI_FLASH, response["tokens"], cost_usd=0)
            response["fallback"] = True
            response["fallback_level"] = 3
            return response

        except Exception as e:
            logger.critical(f"All providers failed for user {user_id}: {e}")
            # NIVEAU 4: Réponse d'urgence (dernier recours)
            return {
                "response": "Désolé, le service est temporairement indisponible. Veuillez réessayer dans 1 minute.",
                "error": "all_providers_failed",
                "provider": "none",
                "tokens": {"input": 0, "output": 0},
                "cost": 0,
                "fallback_level": 4
            }

    def _route_provider(self, tier: UserTier, model_choice: str) -> Provider:
        """
        Décide quel provider utiliser selon tier et probabilité

        Routing:
        - FREE → 100% Groq
        - STUDENT → 85% Groq / 15% OpenRouter
        - PRO → 70% Groq / 30% OpenRouter
        - ENTERPRISE → 50% Groq / 50% OpenRouter
        """
        if tier == UserTier.FREE:
            return Provider.GROQ

        percentages = self.routing_config[tier]
        rand = random.randint(1, 100)

        if rand <= percentages["groq"]:
            return Provider.GROQ
        else:
            return Provider.OPENROUTER

    async def _groq_generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Appel Groq (GRATUIT et RAPIDE)"""
        try:
            response = await self.groq_client.post(
                "/chat/completions",
                json={
                    "model": self.models[Provider.GROQ],
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()

            return {
                "response": data["choices"][0]["message"]["content"],
                "model": self.models[Provider.GROQ],
                "provider": "groq",
                "tokens": {
                    "input": data["usage"]["prompt_tokens"],
                    "output": data["usage"]["completion_tokens"]
                },
                "cost": 0.0,  # GRATUIT
                "cached": False
            }
        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            raise

    async def _openrouter_generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Appel OpenRouter (PAYANT premium)"""
        try:
            response = await self.openrouter_client.post(
                "/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()

            # OpenRouter retourne coût dans headers ou usage
            cost_usd = float(response.headers.get("X-Cost", 0))
            if cost_usd == 0:
                # Estimation si header manquant (GPT-4o pricing)
                tokens_total = data["usage"]["total_tokens"]
                cost_usd = (tokens_total / 1_000_000) * 2.5  # Estimation moyenne

            return {
                "response": data["choices"][0]["message"]["content"],
                "model": model,
                "provider": "openrouter",
                "tokens": {
                    "input": data["usage"]["prompt_tokens"],
                    "output": data["usage"]["completion_tokens"]
                },
                "cost": cost_usd,
                "cached": False
            }
        except Exception as e:
            logger.error(f"OpenRouter generation failed: {e}")
            raise

    async def _gemini_flash_generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Appel Gemini 2.0 Flash via OpenRouter (GRATUIT backup)"""
        try:
            response = await self.gemini_client.post(
                "/chat/completions",
                json={
                    "model": self.models[Provider.GEMINI_FLASH],
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()

            return {
                "response": data["choices"][0]["message"]["content"],
                "model": self.models[Provider.GEMINI_FLASH],
                "provider": "gemini-flash",
                "tokens": {
                    "input": data["usage"]["prompt_tokens"],
                    "output": data["usage"]["completion_tokens"]
                },
                "cost": 0.0,  # GRATUIT via OpenRouter
                "cached": False
            }
        except Exception as e:
            logger.error(f"Gemini Flash generation failed: {e}")
            raise

    async def _check_user_quota(self, user_id: int, tier: UserTier) -> bool:
        """Vérifie quota journalier user (rate limiting intégré)"""
        key = f"user:{user_id}:messages:today"
        count = await self.redis.get(key)
        count = int(count) if count else 0

        # Limites par tier
        limits = {
            UserTier.FREE: 3,
            UserTier.STUDENT: 200,
            UserTier.PRO: 400,
            UserTier.ENTERPRISE: 999999
        }

        max_messages = limits[tier]

        if count >= max_messages:
            logger.warning(f"User {user_id} exceeded quota: {count}/{max_messages}")
            return False

        # Incrémenter compteur
        pipeline = self.redis.pipeline()
        pipeline.incr(key)
        pipeline.expire(key, 86400)  # 24h
        await pipeline.execute()

        return True

    async def _check_daily_budget(self) -> bool:
        """Vérifie budget quotidien global (protection coûts)"""
        key = "budget:today:usd"
        spent = await self.redis.get(key)
        spent = float(spent) if spent else 0.0

        if spent >= self.daily_budget_usd:
            logger.warning(f"Daily budget cap reached: ${spent:.2f} / ${self.daily_budget_usd:.2f}")
            return False

        return True

    async def _log_usage(
        self,
        user_id: int,
        provider: Provider,
        tokens: Dict[str, int],
        cost_usd: float
    ):
        """
        Log usage pour analytics + billing

        Stocke dans:
        1. Redis (budget quotidien)
        2. PostgreSQL (analytics long terme)
        """
        # 1. Incrémenter budget quotidien (Redis)
        budget_key = "budget:today:usd"
        await self.redis.incrbyfloat(budget_key, cost_usd)
        await self.redis.expire(budget_key, 86400)

        # 2. Log dans PostgreSQL (asynchrone via asyncpg)
        # Sera fait dans le router FastAPI pour éviter circular import
        logger.info(
            f"LLM usage - User: {user_id}, Provider: {provider.value}, "
            f"Tokens: {tokens['input']}+{tokens['output']}, Cost: ${cost_usd:.4f}"
        )

    def _get_quota_message(self, tier: UserTier) -> str:
        """Message personnalisé selon tier"""
        if tier == UserTier.FREE:
            return (
                "Limite quotidienne atteinte (3 messages/jour). "
                "Upgrade vers ÉTUDIANT pour 200 messages/jour à seulement 1590 DA/mois!"
            )
        elif tier == UserTier.STUDENT:
            return (
                "Limite quotidienne atteinte (200 messages/jour). "
                "Upgrade vers PRO pour 400 messages/jour à 2590 DA/mois!"
            )
        else:
            return "Limite quotidienne atteinte. Veuillez contacter le support."

    async def close(self):
        """Ferme les connexions proprement"""
        await self.groq_client.aclose()
        await self.openrouter_client.aclose()
        await self.gemini_client.aclose()
        await self.redis.close()

    # ═══════════════════════════════════════════════════════════════════
    # INTÉGRATION SYSTÈME DE CRÉDITS
    # ═══════════════════════════════════════════════════════════════════

    async def route_with_credits(
        self,
        tenant_id: str,
        prompt: str,
        credit_service,  # CreditService instance
        preferred_model: str = None,
        user_tier: UserTier = UserTier.FREE,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Route une requête en vérifiant et déduisant les crédits

        Flow:
        1. Déterminer le modèle à utiliser
        2. Vérifier les crédits AVANT l'appel
        3. Si pas assez → Fallback vers modèle gratuit
        4. Faire l'appel LLM
        5. Déduire les crédits APRÈS succès

        Args:
            tenant_id: ID du tenant
            prompt: Prompt utilisateur
            credit_service: Instance du CreditService
            preferred_model: Modèle préféré (optionnel)
            user_tier: Tier utilisateur
            max_tokens: Tokens max
            temperature: Température

        Returns:
            Réponse LLM avec infos de crédits
        """
        # Déterminer le service/modèle à utiliser
        if preferred_model:
            service_name = self._model_to_service(preferred_model)
        else:
            # Routing automatique selon tier
            provider = self._route_provider(user_tier, "gpt-4o")
            if provider == Provider.GROQ:
                service_name = "groq-llama"
            else:
                service_name = "gpt-4o"

        # Vérifier les crédits AVANT l'appel
        can_afford = await credit_service.can_afford(tenant_id, service_name)

        if not can_afford:
            # Fallback vers modèle gratuit si pas de crédits
            logger.info(f"Crédits insuffisants pour {service_name}, fallback vers groq-llama")
            service_name = "groq-llama"

        # Faire l'appel LLM
        if service_name == "groq-llama":
            response = await self._groq_generate(prompt, max_tokens, temperature)
        elif service_name == "gemini-flash":
            response = await self._gemini_flash_generate(prompt, max_tokens, temperature)
        else:
            # Modèle payant via OpenRouter
            model_id = self._service_to_model(service_name)
            response = await self._openrouter_generate(prompt, model_id, max_tokens, temperature)

        # Déduire les crédits APRÈS succès (services gratuits = 0 déduction)
        credit_result = await credit_service.deduct_credits(
            tenant_id,
            service_name,
            metadata={
                "model": response.get("model"),
                "tokens_input": response.get("tokens", {}).get("input", 0),
                "tokens_output": response.get("tokens", {}).get("output", 0),
                "provider": response.get("provider")
            }
        )

        # Ajouter les infos de crédits à la réponse
        response["credits"] = {
            "service": service_name,
            "deducted": credit_result.get("deducted", 0),
            "remaining": credit_result.get("remaining", 0),
            "unlimited": credit_result.get("unlimited", False)
        }

        return response

    def _model_to_service(self, model: str) -> str:
        """
        Convertit un nom de modèle en nom de service pour le pricing

        Args:
            model: Nom du modèle (ex: "gpt-4o", "claude-sonnet-4")

        Returns:
            Nom du service pour le pricing (ex: "gpt-4o", "claude-sonnet")
        """
        mapping = {
            # Groq (gratuit)
            "llama-3.3-70b-versatile": "groq-llama",
            "llama3-70b-8192": "groq-llama",

            # Gemini (gratuit)
            "google/gemini-2.0-flash-exp:free": "gemini-flash",
            "gemini-flash": "gemini-flash",

            # Claude
            "claude-sonnet-4-20250514": "claude-sonnet",
            "anthropic/claude-sonnet-4-20250514": "claude-sonnet",
            "anthropic/claude-3.5-sonnet": "claude-sonnet",
            "claude-opus": "claude-opus",
            "anthropic/claude-3-opus": "claude-opus",

            # OpenAI
            "gpt-4o": "gpt-4o",
            "openai/gpt-4o": "gpt-4o",
            "gpt-4-turbo": "gpt-4-turbo",
            "openai/gpt-4-turbo": "gpt-4-turbo",
            "gpt-4o-mini": "gpt-4o-mini",
            "openai/gpt-4o-mini": "gpt-4o-mini",

            # xAI
            "grok-2": "grok-2",
            "x-ai/grok-2": "grok-2",
            "x-ai/grok-2-1212": "grok-2",

            # Mistral
            "mistral-large": "mistral-large",
            "mistralai/mistral-large": "mistral-large",

            # DeepSeek
            "deepseek-chat": "deepseek",
            "deepseek/deepseek-chat": "deepseek",
            "deepseek-reasoner": "deepseek-reasoner",

            # Qwen
            "qwen": "qwen",
            "qwen/qwen-72b": "qwen",
        }
        return mapping.get(model, "groq-llama")  # Défaut = gratuit

    def _service_to_model(self, service_name: str) -> str:
        """
        Convertit un nom de service en ID de modèle OpenRouter

        Args:
            service_name: Nom du service (ex: "gpt-4o")

        Returns:
            ID du modèle OpenRouter
        """
        mapping = {
            "groq-llama": "llama-3.3-70b-versatile",
            "gemini-flash": "google/gemini-2.0-flash-exp:free",
            "claude-sonnet": "anthropic/claude-sonnet-4-20250514",
            "claude-opus": "anthropic/claude-3-opus",
            "gpt-4o": "openai/gpt-4o",
            "gpt-4-turbo": "openai/gpt-4-turbo",
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "grok-2": "x-ai/grok-2-1212",
            "mistral-large": "mistralai/mistral-large-latest",
            "deepseek": "deepseek/deepseek-chat",
            "qwen": "qwen/qwen-2-72b-instruct",
        }
        return mapping.get(service_name, "openai/gpt-4o")


# Singleton instance
_router_instance: Optional[SafeLLMRouter] = None


def get_llm_router() -> SafeLLMRouter:
    """Dependency pour FastAPI"""
    global _router_instance
    if _router_instance is None:
        _router_instance = SafeLLMRouter()
    return _router_instance
