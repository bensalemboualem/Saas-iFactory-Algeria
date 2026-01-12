"""
Configuration complète de tous les modèles LLM disponibles pour le Council
"""
from enum import Enum
from typing import Dict, Any, List, Tuple
import os


class ModelTier(str, Enum):
    """Catégories de modèles"""
    PREMIUM = "premium"
    STANDARD = "standard"
    LOCAL = "local"
    SPECIALIZED = "specialized"


class AvailableModels:
    """Catalogue complet des LLMs disponibles"""

    MODELS: Dict[str, Dict[str, Any]] = {
        # ==================== OpenAI ====================
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "provider": "openai",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.01,
            "speed": "medium",
            "strengths": ["Raisonnement", "Code", "Analyse"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🧠"
        },
        "gpt-4o": {
            "name": "GPT-4o",
            "provider": "openai",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.005,
            "speed": "fast",
            "strengths": ["Multimodal", "Rapide", "Performant"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🚀"
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "provider": "openai",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.0005,
            "speed": "fast",
            "strengths": ["Rapide", "Économique"],
            "languages": ["FR", "EN", "AR"],
            "icon": "⚡"
        },

        # ==================== Anthropic Claude ====================
        "claude-3-opus-20240229": {
            "name": "Claude Opus 3",
            "provider": "anthropic",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.015,
            "speed": "medium",
            "strengths": ["Analyse profonde", "Écriture"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🎯"
        },
        "claude-3-5-sonnet-20241022": {
            "name": "Claude Sonnet 3.5",
            "provider": "anthropic",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.003,
            "speed": "fast",
            "strengths": ["Équilibré", "Rapide"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🎵"
        },

        # ==================== Google Gemini ====================
        "gemini-2.0-flash": {
            "name": "Gemini 2.0 Flash",
            "provider": "google",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.0005,
            "speed": "very_fast",
            "strengths": ["Très rapide", "Multimodal"],
            "languages": ["FR", "EN", "AR"],
            "icon": "💎"
        },
        "gemini-1.5-pro": {
            "name": "Gemini 1.5 Pro",
            "provider": "google",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.00125,
            "speed": "fast",
            "strengths": ["Long contexte", "Recherche"],
            "languages": ["FR", "EN", "AR"],
            "icon": "💎"
        },
        "gemini-1.5-flash": {
            "name": "Gemini Flash",
            "provider": "google",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.00035,
            "speed": "very_fast",
            "strengths": ["Rapide", "Économique"],
            "languages": ["FR", "EN", "AR"],
            "icon": "⚡"
        },

        # ==================== xAI Grok ====================
        "grok-2": {
            "name": "Grok 2",
            "provider": "xai",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.005,
            "speed": "medium",
            "strengths": ["Données temps réel", "Analyse"],
            "languages": ["EN", "FR"],
            "icon": "🤖"
        },

        # ==================== Mistral ====================
        "mistral-large": {
            "name": "Mistral Large",
            "provider": "mistral",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.002,
            "speed": "fast",
            "strengths": ["FR natif", "Code"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🇫🇷"
        },
        "mistral-small": {
            "name": "Mistral Small",
            "provider": "mistral",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.0006,
            "speed": "very_fast",
            "strengths": ["Rapide", "Économique"],
            "languages": ["FR", "EN"],
            "icon": "🇫🇷"
        },

        # ==================== DeepSeek ====================
        "deepseek-chat": {
            "name": "DeepSeek Chat",
            "provider": "deepseek",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.0001,
            "speed": "fast",
            "strengths": ["Très économique", "Code"],
            "languages": ["EN", "FR", "CN"],
            "icon": "🔍"
        },

        # ==================== Qwen ====================
        "qwen-2.5-72b": {
            "name": "Qwen 2.5 72B",
            "provider": "qwen",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.0008,
            "speed": "medium",
            "strengths": ["Multilingue", "Performant"],
            "languages": ["EN", "FR", "CN", "AR"],
            "icon": "🌏"
        },

        # ==================== Perplexity ====================
        "perplexity-online": {
            "name": "Perplexity Online",
            "provider": "perplexity",
            "tier": ModelTier.PREMIUM,
            "cost_per_1k_tokens": 0.005,
            "speed": "medium",
            "strengths": ["Web search", "Citations"],
            "languages": ["EN", "FR"],
            "icon": "🔎"
        },

        # ==================== Moonshot (Kimi) ====================
        "kimi-k2": {
            "name": "Kimi K2",
            "provider": "moonshot",
            "tier": ModelTier.STANDARD,
            "cost_per_1k_tokens": 0.0012,
            "speed": "fast",
            "strengths": ["Long context", "Multilingue"],
            "languages": ["CN", "EN", "FR"],
            "icon": "🌙"
        },

        # ==================== Meta Llama (Ollama - Local) ====================
        "llama3.1-70b": {
            "name": "Llama 3.1 70B",
            "provider": "ollama",
            "tier": ModelTier.LOCAL,
            "cost_per_1k_tokens": 0.0,
            "speed": "medium",
            "strengths": ["Gratuit", "Privé"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🦙",
            "ollama_model": "llama3.1:70b"
        },
        "llama3.1-8b": {
            "name": "Llama 3.1 8B",
            "provider": "ollama",
            "tier": ModelTier.LOCAL,
            "cost_per_1k_tokens": 0.0,
            "speed": "fast",
            "strengths": ["Rapide", "Gratuit"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🦙",
            "ollama_model": "llama3.1:8b"
        },
        "mixtral-8x7b": {
            "name": "Mixtral 8x7B",
            "provider": "ollama",
            "tier": ModelTier.LOCAL,
            "cost_per_1k_tokens": 0.0,
            "speed": "medium",
            "strengths": ["Gratuit", "Multilingue"],
            "languages": ["FR", "EN", "AR"],
            "icon": "🎯",
            "ollama_model": "mixtral:8x7b"
        },
        "codellama-34b": {
            "name": "CodeLlama 34B",
            "provider": "ollama",
            "tier": ModelTier.SPECIALIZED,
            "cost_per_1k_tokens": 0.0,
            "speed": "medium",
            "strengths": ["Code expert", "Debug"],
            "languages": ["EN"],
            "icon": "💻",
            "ollama_model": "codellama:34b"
        },
    }

    @classmethod
    def get_by_tier(cls, tier: ModelTier) -> Dict[str, Dict]:
        """Récupère modèles par tier"""
        return {
            k: v for k, v in cls.MODELS.items()
            if v["tier"] == tier
        }

    @classmethod
    def get_by_provider(cls, provider: str) -> Dict[str, Dict]:
        """Récupère modèles par provider"""
        return {
            k: v for k, v in cls.MODELS.items()
            if v["provider"] == provider
        }

    @classmethod
    def get_available_models(cls) -> List[str]:
        """Retourne la liste des IDs de modèles disponibles"""
        available = []

        for model_id, model_info in cls.MODELS.items():
            provider = model_info["provider"]

            # Vérifier si les clés API sont présentes
            if provider == "openai" and os.getenv("OPENAI_API_KEY"):
                available.append(model_id)
            elif provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
                available.append(model_id)
            elif provider == "google" and os.getenv("GOOGLE_API_KEY"):
                available.append(model_id)
            elif provider == "mistral" and os.getenv("MISTRAL_API_KEY"):
                available.append(model_id)
            elif provider == "xai" and os.getenv("XAI_API_KEY"):
                available.append(model_id)
            elif provider == "deepseek" and os.getenv("DEEPSEEK_API_KEY"):
                available.append(model_id)
            elif provider == "qwen" and os.getenv("QWEN_API_KEY"):
                available.append(model_id)
            elif provider == "perplexity" and os.getenv("PERPLEXITY_API_KEY"):
                available.append(model_id)
            elif provider == "ollama" and os.getenv("OLLAMA_BASE_URL"):
                available.append(model_id)

        return available

    @classmethod
    def estimate_cost(cls, model_ids: List[str], avg_tokens: int = 2000) -> float:
        """Estime le coût d'une combinaison"""
        total = 0.0
        for model_id in model_ids:
            if model_id in cls.MODELS:
                cost_per_1k = cls.MODELS[model_id]["cost_per_1k_tokens"]
                total += (avg_tokens / 1000) * cost_per_1k
        return total

    @classmethod
    def estimate_time(cls, model_ids: List[str]) -> Tuple[int, int]:
        """Estime le temps d'exécution (min, max) en secondes"""
        speed_map = {
            "very_fast": 3,
            "fast": 5,
            "medium": 10,
            "slow": 20
        }

        max_time = 0
        for model_id in model_ids:
            if model_id in cls.MODELS:
                speed = cls.MODELS[model_id].get("speed", "medium")
                max_time = max(max_time, speed_map.get(speed, 10))

        min_time = max_time + 5
        max_time_with_review = int(min_time * 1.5)

        return (min_time, max_time_with_review)


# ==================== Presets Recommandés ====================

RECOMMENDED_COUNCILS = {
    "balanced": {
        "name": "Équilibré",
        "description": "Bon rapport qualité/prix/vitesse",
        "members": ["claude-3-5-sonnet-20241022", "gemini-1.5-pro", "llama3.1-70b"],
        "chairman": "claude-3-5-sonnet-20241022",
        "icon": "⚖️"
    },
    "premium": {
        "name": "Premium",
        "description": "Maximum qualité",
        "members": ["claude-3-opus-20240229", "gpt-4-turbo", "gemini-2.0-flash"],
        "chairman": "claude-3-opus-20240229",
        "icon": "👑"
    },
    "economy": {
        "name": "Économique",
        "description": "100% local gratuit",
        "members": ["llama3.1-70b", "mixtral-8x7b", "llama3.1-8b"],
        "chairman": "llama3.1-70b",
        "icon": "💰"
    },
    "fast": {
        "name": "Rapide",
        "description": "< 15 secondes",
        "members": ["gpt-3.5-turbo", "gemini-1.5-flash", "llama3.1-8b"],
        "chairman": "gpt-4o",
        "icon": "⚡"
    }
}
