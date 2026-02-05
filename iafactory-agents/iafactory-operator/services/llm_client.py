"""
IA Factory Operator - LLM Client
All LLM calls route through the gateway (http://localhost:3001)
"""

import json
import os
from typing import Optional, Dict, Any, List

import httpx
import structlog

logger = structlog.get_logger(__name__)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:3001")


class LLMClient:
    """
    LLM client for video edit planning.
    Routes all calls through the IA Factory gateway.
    """

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.model = model

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.3,
        model: Optional[str] = None,
    ) -> str:
        """Generate text completion via gateway."""
        use_model = model or self.model
        logger.debug(f"Generating via gateway with model {use_model}")

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{GATEWAY_URL}/api/llm/chat/completions",
                json={
                    "model": use_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
    
    async def analyze_video_content(
        self,
        transcript: str,
        scene_descriptions: List[str],
        target_platform: str,
        language: str = "fr",
    ) -> Dict[str, Any]:
        """
        Analyze video content for better edit planning.
        Returns structured analysis with key moments, themes, etc.
        """
        system_prompt = """Tu es un expert en analyse de contenu vidéo pour les réseaux sociaux.
Analyse le contenu fourni et identifie:
1. Les moments clés à garder
2. Le thème principal
3. L'émotion dominante
4. Les segments les plus engageants

Réponds en JSON."""

        user_prompt = f"""Analyse ce contenu vidéo pour {target_platform}:

**Transcription:**
{transcript[:3000]}

**Scènes détectées:**
{chr(10).join(scene_descriptions[:10])}

**Langue cible:** {language}

Donne ton analyse en JSON."""

        response = await self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=1500,
            temperature=0.2,
        )
        
        try:
            # Parse JSON from response
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end]
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_analysis": response}


# =============================================================================
# SINGLETON
# =============================================================================

_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client singleton"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
