"""
LLM Router Configuration - 15 Providers Complete
Defines available providers, models, and routing rules
"""
from enum import Enum
from typing import Dict, List
from pydantic import BaseModel


class Provider(str, Enum):
    """Available LLM providers - 15 total"""
    # Tier 1: Premium (Original 4)
    CLAUDE = "claude"
    OPENAI = "openai"
    MISTRAL = "mistral"
    GEMINI = "gemini"

    # Tier 2: Cost-Optimized (Chinese Ecosystem)
    QWEN = "qwen"           # Alibaba - $0.08-$1.20/1M (CHEAPEST)
    DEEPSEEK = "deepseek"   # DeepSeek - $0.14/1M (Code specialist)
    KIMI = "kimi"           # Moonshot - $0.12-$0.60/1M (200K context)
    GLM = "glm"             # Zhipu AI - $0.10/1M (Chinese GPT)

    # Tier 3: Speed & Scale (US Advanced)
    GROQ = "groq"           # Groq - 100-300ms latency (FASTEST)
    GROK = "grok"           # xAI - $5/1M (X/Twitter data)
    PERPLEXITY = "perplexity"  # Perplexity - $0.20-$1/1M (Web search)
    OPENROUTER = "openrouter"  # OpenRouter - Universal gateway

    # Tier 4: Developer & Enterprise
    HUGGINGFACE = "huggingface"  # 400K+ models
    GITHUB = "github"            # GitHub Models Marketplace
    COPILOT = "copilot"          # Microsoft Azure OpenAI


class TaskComplexity(str, Enum):
    """Task complexity levels for routing"""
    SIMPLE = "simple"         # Classification, short answers
    MODERATE = "moderate"     # Analysis, summaries
    COMPLEX = "complex"       # Reasoning, planning
    EXPERT = "expert"         # Legal, medical, deep analysis


class UseCaseType(str, Enum):
    """Use case categories"""
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    ANALYSIS = "analysis"
    CODE_GENERATION = "code_generation"
    REASONING = "reasoning"
    TRANSLATION = "translation"
    EXTRACTION = "extraction"
    CONVERSATION = "conversation"
    WEB_SEARCH = "web_search"
    LONG_CONTEXT = "long_context"


# Model configurations for all 15 providers
MODELS_CONFIG = {
    # === TIER 1: PREMIUM PROVIDERS ===

    Provider.CLAUDE: {
        "haiku": {
            "name": "claude-haiku-4-5-20251001",
            "cost_per_1m_tokens": 0.80,
            "context_window": 200000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        },
        "sonnet": {
            "name": "claude-sonnet-4-5-20250929",
            "cost_per_1m_tokens": 3.00,
            "context_window": 200000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "opus": {
            "name": "claude-opus-4-1-20250805",
            "cost_per_1m_tokens": 15.00,
            "context_window": 200000,
            "speed": "slow",
            "best_for": [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]
        }
    },

    Provider.OPENAI: {
        "gpt4o-mini": {
            "name": "gpt-4o-mini",
            "cost_per_1m_tokens": 0.15,
            "context_window": 128000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        },
        "gpt4o": {
            "name": "gpt-4o",
            "cost_per_1m_tokens": 2.50,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        }
    },

    Provider.MISTRAL: {
        "small": {
            "name": "mistral-small-latest",
            "cost_per_1m_tokens": 0.20,
            "context_window": 32000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        },
        "large": {
            "name": "mistral-large-latest",
            "cost_per_1m_tokens": 2.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        }
    },

    Provider.GEMINI: {
        "flash": {
            "name": "gemini-2.0-flash",
            "cost_per_1m_tokens": 0.10,
            "context_window": 128000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        },
        "pro": {
            "name": "gemini-pro",
            "cost_per_1m_tokens": 0.50,
            "context_window": 32000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "ultra": {
            "name": "gemini-ultra",
            "cost_per_1m_tokens": 2.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]
        }
    },

    # === TIER 2: COST-OPTIMIZED (CHINESE ECOSYSTEM) ===

    Provider.QWEN: {
        "turbo": {
            "name": "qwen-turbo",
            "cost_per_1m_tokens": 0.08,  # CHEAPEST!
            "context_window": 8000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        },
        "plus": {
            "name": "qwen-plus",
            "cost_per_1m_tokens": 0.40,
            "context_window": 32000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]
        },
        "max": {
            "name": "qwen-max",
            "cost_per_1m_tokens": 1.20,
            "context_window": 8000,
            "speed": "medium",
            "best_for": [TaskComplexity.COMPLEX]
        }
    },

    Provider.DEEPSEEK: {
        "chat": {
            "name": "deepseek-chat",
            "cost_per_1m_tokens": 0.14,
            "context_window": 64000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        },
        "coder": {
            "name": "deepseek-coder",
            "cost_per_1m_tokens": 0.14,
            "context_window": 16000,
            "speed": "fast",
            "best_for": [TaskComplexity.COMPLEX]  # Code specialist
        }
    },

    Provider.KIMI: {
        "8k": {
            "name": "moonshot-v1-8k",
            "cost_per_1m_tokens": 0.12,
            "context_window": 8000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        },
        "32k": {
            "name": "moonshot-v1-32k",
            "cost_per_1m_tokens": 0.24,
            "context_window": 32000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]
        },
        "128k": {
            "name": "moonshot-v1-128k",
            "cost_per_1m_tokens": 0.60,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.COMPLEX]  # Long context
        }
    },

    Provider.GLM: {
        "4": {
            "name": "glm-4",
            "cost_per_1m_tokens": 0.10,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "4-air": {
            "name": "glm-4-air",
            "cost_per_1m_tokens": 0.001,  # Ultra cheap!
            "context_window": 8000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        },
        "4-flash": {
            "name": "glm-4-flash",
            "cost_per_1m_tokens": 0.0001,  # Nearly free!
            "context_window": 4000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        }
    },

    # === TIER 3: SPEED & SCALE (US ADVANCED) ===

    Provider.GROQ: {
        "llama-70b": {
            "name": "llama-3.1-70b-versatile",
            "cost_per_1m_tokens": 0.59,
            "context_window": 128000,
            "speed": "ultra_fast",  # 100-300ms!
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "mixtral": {
            "name": "mixtral-8x7b-32768",
            "cost_per_1m_tokens": 0.27,
            "context_window": 32000,
            "speed": "ultra_fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        }
    },

    Provider.GROK: {
        "beta": {
            "name": "grok-beta",
            "cost_per_1m_tokens": 5.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "vision": {
            "name": "grok-vision-beta",
            "cost_per_1m_tokens": 5.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.COMPLEX]
        }
    },

    Provider.PERPLEXITY: {
        "sonar-small": {
            "name": "sonar-small-online",
            "cost_per_1m_tokens": 0.20,
            "context_window": 8000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]  # Web search
        },
        "sonar-medium": {
            "name": "sonar-medium-online",
            "cost_per_1m_tokens": 0.60,
            "context_window": 16000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]  # Web search
        }
    },

    Provider.OPENROUTER: {
        "auto": {
            "name": "auto",
            "cost_per_1m_tokens": 1.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]
        },
        "claude-opus": {
            "name": "anthropic/claude-3-opus",
            "cost_per_1m_tokens": 15.00,
            "context_window": 200000,
            "speed": "slow",
            "best_for": [TaskComplexity.EXPERT]
        }
    },

    # === TIER 4: DEVELOPER & ENTERPRISE ===

    Provider.HUGGINGFACE: {
        "llama-70b": {
            "name": "meta-llama/Meta-Llama-3-70B-Instruct",
            "cost_per_1m_tokens": 0.50,
            "context_window": 8000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "mixtral": {
            "name": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "cost_per_1m_tokens": 0.40,
            "context_window": 32000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]
        },
        "zephyr": {
            "name": "HuggingFaceH4/zephyr-7b-beta",
            "cost_per_1m_tokens": 0.08,
            "context_window": 8000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        }
    },

    Provider.GITHUB: {
        "gpt-4o": {
            "name": "gpt-4o",
            "cost_per_1m_tokens": 2.50,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "llama-70b": {
            "name": "llama-3.1-70b",
            "cost_per_1m_tokens": 0.60,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE]
        },
        "phi-3": {
            "name": "phi-3-mini-128k",
            "cost_per_1m_tokens": 0.05,
            "context_window": 128000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE]
        }
    },

    Provider.COPILOT: {
        "gpt-4o": {
            "name": "gpt-4o",
            "cost_per_1m_tokens": 5.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        },
        "gpt-4o-mini": {
            "name": "gpt-4o-mini",
            "cost_per_1m_tokens": 0.15,
            "context_window": 128000,
            "speed": "fast",
            "best_for": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]
        },
        "gpt-4-turbo": {
            "name": "gpt-4-turbo",
            "cost_per_1m_tokens": 10.00,
            "context_window": 128000,
            "speed": "medium",
            "best_for": [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]
        }
    }
}


# Enhanced routing rules with new providers
ROUTING_RULES = {
    UseCaseType.CLASSIFICATION: {
        "primary": (Provider.QWEN, "turbo"),  # CHEAPEST at $0.08/1M
        "fallback": (Provider.GLM, "4-air"),
        "complexity": TaskComplexity.SIMPLE
    },
    UseCaseType.SUMMARIZATION: {
        "primary": (Provider.GROQ, "mixtral"),  # FASTEST
        "fallback": (Provider.QWEN, "plus"),
        "complexity": TaskComplexity.MODERATE
    },
    UseCaseType.ANALYSIS: {
        "primary": (Provider.CLAUDE, "sonnet"),
        "fallback": (Provider.OPENAI, "gpt4o"),
        "complexity": TaskComplexity.COMPLEX
    },
    UseCaseType.CODE_GENERATION: {
        "primary": (Provider.DEEPSEEK, "coder"),  # CODE SPECIALIST
        "fallback": (Provider.CLAUDE, "sonnet"),
        "complexity": TaskComplexity.COMPLEX
    },
    UseCaseType.REASONING: {
        "primary": (Provider.CLAUDE, "opus"),
        "fallback": (Provider.OPENAI, "gpt4o"),
        "complexity": TaskComplexity.EXPERT
    },
    UseCaseType.EXTRACTION: {
        "primary": (Provider.QWEN, "turbo"),  # CHEAPEST
        "fallback": (Provider.GLM, "4-flash"),
        "complexity": TaskComplexity.SIMPLE
    },
    UseCaseType.CONVERSATION: {
        "primary": (Provider.GROQ, "llama-70b"),  # FASTEST
        "fallback": (Provider.KIMI, "32k"),
        "complexity": TaskComplexity.MODERATE
    },
    UseCaseType.WEB_SEARCH: {
        "primary": (Provider.PERPLEXITY, "sonar-medium"),  # WEB SEARCH
        "fallback": (Provider.PERPLEXITY, "sonar-small"),
        "complexity": TaskComplexity.MODERATE
    },
    UseCaseType.LONG_CONTEXT: {
        "primary": (Provider.KIMI, "128k"),  # 128K CONTEXT
        "fallback": (Provider.CLAUDE, "sonnet"),
        "complexity": TaskComplexity.COMPLEX
    },
    UseCaseType.TRANSLATION: {
        "primary": (Provider.QWEN, "plus"),  # Chinese ecosystem
        "fallback": (Provider.GLM, "4"),
        "complexity": TaskComplexity.MODERATE
    }
}


# Cost tiers for clients (updated)
COST_TIERS = {
    "ultra_economy": {
        "max_cost_per_request": 0.001,  # $0.001 max
        "prefer_providers": [Provider.GLM, Provider.QWEN, Provider.DEEPSEEK],
        "avoid_models": ["opus", "gpt-4", "grok"]
    },
    "economy": {
        "max_cost_per_request": 0.01,  # $0.01 max
        "prefer_providers": [Provider.QWEN, Provider.GROQ, Provider.GITHUB],
        "avoid_models": ["opus", "gpt-4-turbo"]
    },
    "standard": {
        "max_cost_per_request": 0.05,  # $0.05 max
        "prefer_providers": [Provider.CLAUDE, Provider.OPENAI, Provider.GROQ],
        "avoid_models": ["opus"]
    },
    "premium": {
        "max_cost_per_request": 0.20,  # $0.20 max
        "prefer_providers": [Provider.CLAUDE, Provider.OPENAI],
        "avoid_models": []
    },
    "enterprise": {
        "max_cost_per_request": 1.00,  # $1.00 max
        "prefer_providers": [Provider.COPILOT, Provider.CLAUDE],
        "avoid_models": []
    }
}
