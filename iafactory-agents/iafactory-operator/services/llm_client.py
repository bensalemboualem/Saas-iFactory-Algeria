"""
IA Factory Operator - LLM Client
Claude/OpenAI API wrapper for edit planning
"""

import json
from typing import Optional, Dict, Any, List

import structlog
from anthropic import AsyncAnthropic

from core.config import settings

logger = structlog.get_logger(__name__)


class LLMClient:
    """
    LLM client for video edit planning.
    Primary: Claude (Anthropic)
    Fallback: OpenAI GPT-4
    """
    
    def __init__(
        self,
        anthropic_key: Optional[str] = None,
        openai_key: Optional[str] = None,
    ):
        self.anthropic_key = anthropic_key or settings.anthropic_api_key
        self.openai_key = openai_key or settings.openai_api_key
        
        self._anthropic_client = None
        self._openai_client = None
    
    @property
    def anthropic_client(self) -> AsyncAnthropic:
        if not self._anthropic_client and self.anthropic_key:
            self._anthropic_client = AsyncAnthropic(api_key=self.anthropic_key)
        return self._anthropic_client
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.3,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate text completion using Claude.
        Falls back to OpenAI if Claude fails.
        """
        # Try Claude first
        if self.anthropic_client:
            try:
                response = await self._generate_claude(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    model=model or settings.anthropic_model,
                )
                return response
            except Exception as e:
                logger.warning(f"Claude generation failed: {e}")
        
        # Fallback to OpenAI
        if self.openai_key:
            try:
                response = await self._generate_openai(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response
            except Exception as e:
                logger.error(f"OpenAI fallback also failed: {e}")
                raise
        
        raise RuntimeError("No LLM client available")
    
    async def _generate_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
        model: str,
    ) -> str:
        """Generate using Claude API"""
        logger.debug(f"Generating with Claude {model}")
        
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
        )
        
        # Extract text from response
        content = response.content[0]
        if hasattr(content, 'text'):
            return content.text
        return str(content)
    
    async def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Generate using OpenAI API"""
        import openai
        
        client = openai.AsyncOpenAI(api_key=self.openai_key)
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        
        return response.choices[0].message.content
    
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
