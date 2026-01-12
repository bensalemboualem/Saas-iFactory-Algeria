# -*- coding: utf-8 -*-
from providers.openai import openai_provider
from providers.anthropic import anthropic_provider
from providers.groq import groq_provider
from providers.deepseek import deepseek_provider
from providers.mistral import mistral_provider
from providers.gemini import gemini_provider
from providers.cohere import cohere_provider
from providers.together import together_provider
from providers.openrouter import openrouter_provider

def get_provider(model: str):
    model_lower = model.lower()
    if any(x in model_lower for x in ["gpt-3", "gpt-4", "gpt-4o"]):
        return openai_provider, "openai"
    if "claude" in model_lower:
        return anthropic_provider, "anthropic"
    if any(x in model_lower for x in ["llama", "mixtral", "gemma"]):
        return groq_provider, "groq"
    if "deepseek" in model_lower:
        return deepseek_provider, "deepseek"
    if "mistral" in model_lower:
        return mistral_provider, "mistral"
    if "gemini" in model_lower:
        return gemini_provider, "gemini"
    if "command" in model_lower:
        return cohere_provider, "cohere"
    if "/" in model:
        return openrouter_provider, "openrouter"
    return openai_provider, "openai"
