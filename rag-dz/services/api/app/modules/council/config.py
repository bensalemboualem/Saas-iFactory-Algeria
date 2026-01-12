"""
Configuration pour LLM Council
"""
import os
from typing import List, Dict, Any
from pydantic import BaseModel


class CouncilConfig(BaseModel):
    """Configuration du LLM Council"""

    # Providers disponibles - Configuration étendue
    PROVIDERS: Dict[str, Dict[str, Any]] = {
        # Anthropic Claude
        "claude-opus-4": {
            "name": "Claude Opus 4",
            "provider": "anthropic",
            "model": "claude-opus-4-20250514",
            "role": "premium",
            "tier": "premium",
            "cost_per_1k": 0.015,
            "speed": "medium",
            "strengths": ["Analyse profonde", "Écriture", "Nuance"],
            "icon": "🎯",
            "enabled": True
        },
        "claude": {
            "name": "Claude Sonnet 4",
            "provider": "anthropic",
            "model": "claude-sonnet-4-20250514",
            "role": "chairman",
            "tier": "standard",
            "cost_per_1k": 0.003,
            "speed": "fast",
            "strengths": ["Équilibré", "Rapide", "Précis"],
            "icon": "🎵",
            "enabled": True
        },
        # OpenAI
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "provider": "openai",
            "model": "gpt-4-turbo-preview",
            "role": "premium",
            "tier": "premium",
            "cost_per_1k": 0.01,
            "speed": "medium",
            "strengths": ["Raisonnement complexe", "Code", "Analyse"],
            "icon": "🧠",
            "enabled": True
        },
        "chatgpt": {
            "name": "GPT-3.5 Turbo",
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "role": "member",
            "tier": "standard",
            "cost_per_1k": 0.0005,
            "speed": "very_fast",
            "strengths": ["Rapide", "Économique", "Polyvalent"],
            "icon": "⚡",
            "enabled": True
        },
        # Google Gemini
        "gemini": {
            "name": "Gemini 2.5 Flash",
            "provider": "google",
            "model": "gemini-2.5-flash",
            "role": "member",
            "tier": "standard",
            "cost_per_1k": 0.00125,
            "speed": "very_fast",
            "strengths": ["Multimodal", "Très rapide", "Efficace"],
            "icon": "💎",
            "enabled": True
        },
        "gemini-pro": {
            "name": "Gemini 1.5 Pro",
            "provider": "google",
            "model": "gemini-1.5-pro",
            "role": "member",
            "tier": "standard",
            "cost_per_1k": 0.00125,
            "speed": "fast",
            "strengths": ["Multimodal", "Long contexte", "Recherche"],
            "icon": "💎",
            "enabled": True
        },
        # Mistral
        "mistral-large": {
            "name": "Mistral Large",
            "provider": "mistral",
            "model": "mistral-large-latest",
            "role": "member",
            "tier": "standard",
            "cost_per_1k": 0.002,
            "speed": "fast",
            "strengths": ["Multilingue", "Code", "FR natif"],
            "icon": "🇫🇷",
            "enabled": False  # Nécessite clé API
        },
        # Perplexity
        "perplexity": {
            "name": "Perplexity",
            "provider": "perplexity",
            "model": "llama-3.1-sonar-large-128k-online",
            "role": "member",
            "tier": "standard",
            "cost_per_1k": 0.001,
            "speed": "medium",
            "strengths": ["Recherche web", "Sources", "Actualité"],
            "icon": "🔍",
            "enabled": False
        },
        # Ollama - Local models
        "ollama": {
            "name": "Llama 3.1 8B",
            "provider": "ollama",
            "model": "llama3.1:8b",
            "role": "member",
            "tier": "local",
            "cost_per_1k": 0.0,
            "speed": "fast",
            "strengths": ["Gratuit", "Privé", "Souverain"],
            "icon": "🦙",
            "enabled": True
        },
        "ollama-70b": {
            "name": "Llama 3.1 70B",
            "provider": "ollama",
            "model": "llama3.1:70b",
            "role": "member",
            "tier": "local",
            "cost_per_1k": 0.0,
            "speed": "medium",
            "strengths": ["Gratuit", "Performant", "Privé"],
            "icon": "🦙",
            "enabled": True
        },
        "mixtral": {
            "name": "Mixtral 8x7B",
            "provider": "ollama",
            "model": "mixtral:8x7b",
            "role": "member",
            "tier": "local",
            "cost_per_1k": 0.0,
            "speed": "medium",
            "strengths": ["Gratuit", "Multilingue", "Équilibré"],
            "icon": "🎯",
            "enabled": True
        }
    }

    # Presets recommandés
    RECOMMENDED_PRESETS: Dict[str, Dict[str, Any]] = {
        "balanced": {
            "name": "Équilibré",
            "description": "Bon rapport qualité/prix/vitesse",
            "members": ["claude", "gemini", "ollama"],
            "chairman": "claude",
            "icon": "⚖️",
            "estimated_cost_dzd": 500
        },
        "premium": {
            "name": "Premium",
            "description": "Maximum de qualité, analyses profondes",
            "members": ["claude-opus-4", "gpt-4-turbo", "gemini-pro"],
            "chairman": "claude-opus-4",
            "icon": "👑",
            "estimated_cost_dzd": 2000
        },
        "economy": {
            "name": "Économique",
            "description": "Maximise qualité locale gratuite",
            "members": ["ollama", "mixtral", "ollama-70b"],
            "chairman": "ollama-70b",
            "icon": "💰",
            "estimated_cost_dzd": 0
        },
        "fast": {
            "name": "Rapide",
            "description": "Réponses en moins de 15 secondes",
            "members": ["chatgpt", "gemini", "ollama"],
            "chairman": "chatgpt",
            "icon": "⚡",
            "estimated_cost_dzd": 200
        },
        "research": {
            "name": "Recherche",
            "description": "Optimisé pour recherche et sources",
            "members": ["perplexity", "gemini-pro", "claude"],
            "chairman": "claude",
            "icon": "🔍",
            "estimated_cost_dzd": 600
        }
    }

    # Configuration par défaut - priorité Ollama local (gratuit)
    DEFAULT_COUNCIL: List[str] = ["ollama", "mistral", "qwen"]
    CHAIRMAN: str = "ollama"

    # Timeouts (secondes)
    STAGE1_TIMEOUT: int = 30
    STAGE2_TIMEOUT: int = 20
    STAGE3_TIMEOUT: int = 15
    TOTAL_TIMEOUT: int = 90

    # Options
    ENABLE_REVIEW: bool = True
    ANONYMIZE_MODELS: bool = True

    # API Keys (lues depuis env)
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPEN_ROUTER_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://iaf-ollama:11434"

    class Config:
        extra = "allow"

    @classmethod
    def from_env(cls) -> "CouncilConfig":
        """Crée une config depuis les variables d'environnement"""
        return cls(
            ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY", ""),
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", ""),
            GOOGLE_API_KEY=os.getenv("GOOGLE_GENERATIVE_AI_API_KEY", ""),
            MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY", ""),
            PERPLEXITY_API_KEY=os.getenv("PERPLEXITY_API_KEY", ""),
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            OPEN_ROUTER_API_KEY=os.getenv("OPEN_ROUTER_API_KEY", ""),
            OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL", "http://iaf-ollama:11434"),
            ENABLE_REVIEW=os.getenv("COUNCIL_ENABLE_REVIEW", "true").lower() == "true",
            CHAIRMAN=os.getenv("COUNCIL_CHAIRMAN", "groq-llama")
        )

    def get_available_providers(self) -> List[str]:
        """Retourne la liste des providers disponibles avec clés API configurées"""
        available = []

        if self.OPENAI_API_KEY:
            available.extend(["chatgpt", "gpt-4-turbo"])

        if self.ANTHROPIC_API_KEY:
            available.extend(["claude", "claude-opus-4"])

        if self.GOOGLE_API_KEY:
            available.extend(["gemini", "gemini-pro"])

        if self.MISTRAL_API_KEY:
            available.append("mistral-large")

        if self.PERPLEXITY_API_KEY:
            available.append("perplexity")
            
        if self.GROQ_API_KEY:
            available.extend(["groq-llama", "groq-mixtral", "groq-gemma"])
            
        if self.OPEN_ROUTER_API_KEY:
            available.extend([
                "or-gpt4o", "or-gpt4", "or-gpt35",
                "or-claude", "or-claude-opus",
                "deepseek", "deepseek-coder",
                "qwen-72b", "qwen-coder",
                "kimi",
                "or-llama", "or-mistral", "or-gemini"
            ])

        # Ollama local models
        available.extend(["ollama", "mistral", "qwen", "llama"])

        return available


# Instance globale
council_config = CouncilConfig.from_env()
