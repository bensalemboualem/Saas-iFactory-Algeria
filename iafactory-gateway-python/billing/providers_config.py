"""
IAFactory - Configuration Multi-Provider LLM
=============================================
Intégration: MiMo-V2-Flash, Apertus, Groq, OpenAI, etc.
Basé sur IntuitionLabs 2025 + nouveaux providers
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import httpx
import os

# ==============================================
# PROVIDERS LLM - Configuration complète
# ==============================================

@dataclass
class LLMProvider:
    name: str
    display_name: str
    base_url: str
    models: List[str]
    input_cost: float  # $/1M tokens
    output_cost: float  # $/1M tokens
    speed: int  # tokens/sec
    context_window: int
    features: List[str]
    region: str  # Pour compliance GDPR
    priority: int  # 1 = highest
    active: bool = True

PROVIDERS = {
    # ===========================================
    # ULTRA LOW COST - Pour volume Algérie
    # ===========================================
    "mimo_v2_flash": LLMProvider(
        name="mimo_v2_flash",
        display_name="Xiaomi MiMo-V2-Flash",
        base_url="https://api.mimo.xiaomi.com/v1",
        models=["mimo-v2-flash", "mimo-v2-flash-thinking"],
        input_cost=0.10,   # $0.1/1M - LE MOINS CHER!
        output_cost=0.30,  # $0.3/1M
        speed=150,  # 150 tok/s - très rapide
        context_window=128000,
        features=["chat", "code", "reasoning", "multilingual"],
        region="global",
        priority=1,
        active=True
    ),

    "groq_llama": LLMProvider(
        name="groq_llama",
        display_name="Groq (Llama 3.3 70B)",
        base_url="https://api.groq.com/openai/v1",
        models=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        input_cost=0.59,
        output_cost=0.79,
        speed=800,  # Groq = ultra rapide
        context_window=128000,
        features=["chat", "code", "function_calling"],
        region="us",
        priority=2,
        active=True
    ),

    "deepseek_v3": LLMProvider(
        name="deepseek_v3",
        display_name="DeepSeek V3",
        base_url="https://api.deepseek.com/v1",
        models=["deepseek-chat", "deepseek-coder"],
        input_cost=0.14,
        output_cost=0.28,
        speed=60,
        context_window=64000,
        features=["chat", "code", "reasoning"],
        region="cn",
        priority=3,
        active=True
    ),

    # ===========================================
    # SUISSE / EUROPE - Compliance GDPR
    # ===========================================
    "apertus_swiss": LLMProvider(
        name="apertus_swiss",
        display_name="Apertus (Swiss AI)",
        base_url="https://api.publicai.co/v1",
        models=["apertus-70b", "apertus-8b"],
        input_cost=0.50,   # Estimé - hébergé en Suisse
        output_cost=1.50,
        speed=40,
        context_window=32000,
        features=["chat", "multilingual", "privacy", "gdpr_compliant"],
        region="switzerland",  # GDPR + Swiss data protection
        priority=1,  # Priorité pour clients Suisse
        active=True
    ),

    "mistral_eu": LLMProvider(
        name="mistral_eu",
        display_name="Mistral Large EU",
        base_url="https://api.mistral.ai/v1",
        models=["mistral-large-latest", "mistral-small-latest"],
        input_cost=2.00,
        output_cost=6.00,
        speed=50,
        context_window=128000,
        features=["chat", "code", "function_calling", "eu_hosted"],
        region="eu",
        priority=2,
        active=True
    ),

    # ===========================================
    # PREMIUM - Haute qualité
    # ===========================================
    "openai_gpt4": LLMProvider(
        name="openai_gpt4",
        display_name="OpenAI GPT-4o",
        base_url="https://api.openai.com/v1",
        models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        input_cost=5.00,
        output_cost=15.00,
        speed=80,
        context_window=128000,
        features=["chat", "code", "vision", "function_calling", "json_mode"],
        region="us",
        priority=5,
        active=True
    ),

    "anthropic_claude": LLMProvider(
        name="anthropic_claude",
        display_name="Claude Sonnet 4",
        base_url="https://api.anthropic.com/v1",
        models=["claude-sonnet-4-20250514", "claude-haiku-3-20240307"],
        input_cost=3.00,
        output_cost=15.00,
        speed=70,
        context_window=200000,
        features=["chat", "code", "vision", "reasoning", "long_context"],
        region="us",
        priority=4,
        active=True
    ),

    "google_gemini": LLMProvider(
        name="google_gemini",
        display_name="Google Gemini 2.5",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        models=["gemini-2.5-pro", "gemini-2.5-flash"],
        input_cost=1.25,
        output_cost=10.00,
        speed=100,
        context_window=2000000,  # 2M tokens!
        features=["chat", "code", "vision", "multimodal", "long_context"],
        region="us",
        priority=3,
        active=True
    ),

    # ===========================================
    # VOICE & AUDIO
    # ===========================================
    "elevenlabs": LLMProvider(
        name="elevenlabs",
        display_name="ElevenLabs TTS",
        base_url="https://api.elevenlabs.io/v1",
        models=["eleven_multilingual_v2", "eleven_turbo_v2_5"],
        input_cost=0.30,  # Per 1K characters
        output_cost=0.0,
        speed=0,
        context_window=0,
        features=["tts", "voice_clone", "multilingual"],
        region="us",
        priority=1,
        active=True
    ),

    "openai_whisper": LLMProvider(
        name="openai_whisper",
        display_name="OpenAI Whisper",
        base_url="https://api.openai.com/v1",
        models=["whisper-1"],
        input_cost=0.006,  # Per minute
        output_cost=0.0,
        speed=0,
        context_window=0,
        features=["stt", "transcription", "translation"],
        region="us",
        priority=1,
        active=True
    ),
}

# ==============================================
# ROUTING INTELLIGENT
# ==============================================

class ProviderRouter:
    """Route les requêtes vers le provider optimal"""

    def __init__(self):
        self.providers = PROVIDERS

    def get_best_provider(
        self,
        task_type: str = "chat",
        region: str = "global",
        budget: str = "low",  # low, medium, high
        speed_priority: bool = False
    ) -> LLMProvider:
        """
        Sélectionne le meilleur provider selon les critères
        """
        candidates = []

        for name, provider in self.providers.items():
            if not provider.active:
                continue

            # Filtre par feature
            if task_type not in provider.features and task_type != "chat":
                continue

            # Filtre par région pour GDPR
            if region == "switzerland" and provider.region not in ["switzerland", "eu"]:
                # Pour Suisse, préférer providers EU/CH
                continue

            candidates.append(provider)

        if not candidates:
            # Fallback
            return self.providers["groq_llama"]

        # Tri selon budget
        if budget == "low":
            # Moins cher d'abord
            candidates.sort(key=lambda p: p.input_cost + p.output_cost)
        elif budget == "high":
            # Meilleure qualité (priorité basse = meilleur)
            candidates.sort(key=lambda p: -p.priority)
        else:
            # Équilibre coût/qualité
            candidates.sort(key=lambda p: (p.input_cost + p.output_cost) * p.priority)

        # Si vitesse prioritaire
        if speed_priority:
            candidates.sort(key=lambda p: -p.speed)

        return candidates[0]

    def get_provider_for_region(self, region: str) -> LLMProvider:
        """Retourne le provider optimal pour une région"""
        if region in ["ch", "switzerland"]:
            return self.providers.get("apertus_swiss", self.providers["mistral_eu"])
        elif region in ["dz", "algeria", "africa"]:
            return self.providers.get("mimo_v2_flash", self.providers["groq_llama"])
        elif region in ["eu", "europe"]:
            return self.providers.get("mistral_eu", self.providers["openai_gpt4"])
        else:
            return self.providers["groq_llama"]

    def get_cheapest_provider(self) -> LLMProvider:
        """Retourne le provider le moins cher"""
        return min(
            [p for p in self.providers.values() if p.active],
            key=lambda p: p.input_cost + p.output_cost
        )

    def estimate_cost(
        self,
        provider_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estime le coût d'une requête"""
        provider = self.providers.get(provider_name)
        if not provider:
            return 0.0

        input_cost = (input_tokens / 1_000_000) * provider.input_cost
        output_cost = (output_tokens / 1_000_000) * provider.output_cost

        return round(input_cost + output_cost, 6)


# ==============================================
# COST COMPARISON TABLE
# ==============================================

def print_cost_comparison():
    """Affiche la comparaison des coûts"""
    print("\n" + "=" * 70)
    print("COMPARAISON DES COÛTS LLM - IAFactory 2025")
    print("=" * 70)
    print(f"{'Provider':<25} {'Input $/1M':<12} {'Output $/1M':<12} {'Speed':<10} {'Region':<10}")
    print("-" * 70)

    sorted_providers = sorted(
        PROVIDERS.values(),
        key=lambda p: p.input_cost + p.output_cost
    )

    for p in sorted_providers:
        if not p.active:
            continue
        print(f"{p.display_name:<25} ${p.input_cost:<11.2f} ${p.output_cost:<11.2f} {p.speed:<10} {p.region:<10}")

    print("-" * 70)
    print("\n💡 Recommandations:")
    print("   🇩🇿 Algérie: MiMo-V2-Flash ($0.10 input) - Volume maximum")
    print("   🇨🇭 Suisse: Apertus Swiss AI - Compliance GDPR, data en Suisse")
    print("   🚀 Vitesse: Groq (800 tok/s) - Réponses instantanées")
    print("   🎯 Qualité: Claude Sonnet 4 - Raisonnement avancé")


if __name__ == "__main__":
    print_cost_comparison()

    # Test router
    router = ProviderRouter()

    print("\n" + "=" * 70)
    print("TEST ROUTING INTELLIGENT")
    print("=" * 70)

    # Test différents scénarios
    scenarios = [
        ("Client Algérie, budget faible", "chat", "dz", "low", False),
        ("Client Suisse, compliance GDPR", "chat", "switzerland", "medium", False),
        ("Tâche urgente, vitesse max", "chat", "global", "medium", True),
        ("Code generation premium", "code", "global", "high", False),
    ]

    for desc, task, region, budget, speed in scenarios:
        best = router.get_best_provider(task, region, budget, speed)
        print(f"\n{desc}:")
        print(f"   → {best.display_name} (${best.input_cost + best.output_cost:.2f}/1M)")
