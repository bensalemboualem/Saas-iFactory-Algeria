# Provider imports - 15 total providers
from .base import BaseProvider

# Tier 1: Premium (Original 4)
from .claude_provider import ClaudeProvider
from .openai_provider import OpenAIProvider
from .mistral_provider import MistralProvider
from .gemini_provider import GeminiProvider

# Tier 2: Cost-Optimized (Chinese Ecosystem)
from .qwen_provider import QwenProvider
from .deepseek_provider import DeepSeekProvider
from .kimi_provider import KimiProvider
from .glm_provider import GLMProvider

# Tier 3: Speed & Scale (US Advanced)
from .groq_provider import GroqProvider
from .grok_provider import GrokProvider
from .perplexity_provider import PerplexityProvider
from .openrouter_provider import OpenRouterProvider

# Tier 4: Developer & Enterprise
from .huggingface_provider import HuggingFaceProvider
from .github_provider import GitHubModelsProvider
from .copilot_provider import CopilotProvider

__all__ = [
    'BaseProvider',
    # Tier 1
    'ClaudeProvider',
    'OpenAIProvider',
    'MistralProvider',
    'GeminiProvider',
    # Tier 2
    'QwenProvider',
    'DeepSeekProvider',
    'KimiProvider',
    'GLMProvider',
    # Tier 3
    'GroqProvider',
    'GrokProvider',
    'PerplexityProvider',
    'OpenRouterProvider',
    # Tier 4
    'HuggingFaceProvider',
    'GitHubModelsProvider',
    'CopilotProvider'
]
