"""
IAFactory Video Studio Pro - Base Agent
Classe abstraite pour tous les agents IA
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import asyncio
import logging

from pydantic import BaseModel, Field
from anthropic import AsyncAnthropic

from config import settings, agent_configs


# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    """Réponse standard d'un agent."""
    success: bool
    data: Any
    tokens_used: int = 0
    processing_time: float = 0.0
    agent_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None


class AgentConfig(BaseModel):
    """Configuration d'un agent."""
    name: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 4000
    retry_attempts: int = 3
    timeout: int = 120
    system_prompt: str = ""


class BaseAgent(ABC):
    """
    Classe abstraite de base pour tous les agents IA.
    
    Fournit:
    - Gestion des appels API Anthropic
    - Retry logic
    - Logging
    - Comptage des tokens
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.total_tokens_used = 0
        self.call_count = 0
        
    @property
    def name(self) -> str:
        return self.config.name
    
    @abstractmethod
    async def process(self, input_data: Any) -> AgentResponse:
        """
        Méthode principale de traitement.
        À implémenter par chaque agent spécialisé.
        """
        pass
    
    async def call_llm(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Appelle le LLM avec retry logic.
        
        Args:
            messages: Liste des messages de la conversation
            system_prompt: Prompt système (optionnel, utilise celui de la config sinon)
            temperature: Température (optionnel)
            max_tokens: Tokens maximum (optionnel)
            
        Returns:
            Réponse du LLM avec métadonnées
        """
        start_time = datetime.utcnow()
        
        # Utiliser les valeurs par défaut si non spécifiées
        system = system_prompt or self.config.system_prompt
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens or self.config.max_tokens
        
        for attempt in range(self.config.retry_attempts):
            try:
                logger.info(f"[{self.name}] Appel LLM (tentative {attempt + 1})")
                
                response = await asyncio.wait_for(
                    self.client.messages.create(
                        model=self.config.model,
                        max_tokens=tokens,
                        temperature=temp,
                        system=system,
                        messages=messages,
                    ),
                    timeout=self.config.timeout
                )
                
                # Calcul des tokens
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                total_tokens = input_tokens + output_tokens
                
                self.total_tokens_used += total_tokens
                self.call_count += 1
                
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                logger.info(
                    f"[{self.name}] Succès - "
                    f"Tokens: {total_tokens} ({input_tokens} in / {output_tokens} out) - "
                    f"Temps: {processing_time:.2f}s"
                )
                
                return {
                    "content": response.content[0].text,
                    "tokens_used": total_tokens,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "processing_time": processing_time,
                    "model": self.config.model,
                    "stop_reason": response.stop_reason,
                }
                
            except asyncio.TimeoutError:
                logger.warning(f"[{self.name}] Timeout (tentative {attempt + 1})")
                if attempt == self.config.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Backoff exponentiel
                
            except Exception as e:
                logger.error(f"[{self.name}] Erreur: {str(e)}")
                if attempt == self.config.retry_attempts - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
    
    async def call_llm_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Appelle le LLM avec des outils (function calling).
        """
        system = system_prompt or self.config.system_prompt
        
        response = await self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=system,
            messages=messages,
            tools=tools,
        )
        
        return {
            "content": response.content,
            "stop_reason": response.stop_reason,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de l'agent."""
        return {
            "agent_name": self.name,
            "model": self.config.model,
            "total_calls": self.call_count,
            "total_tokens_used": self.total_tokens_used,
            "average_tokens_per_call": (
                self.total_tokens_used / self.call_count 
                if self.call_count > 0 else 0
            ),
        }
    
    def reset_stats(self):
        """Réinitialise les statistiques."""
        self.total_tokens_used = 0
        self.call_count = 0
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, model={self.config.model})>"


# === MIXINS POUR FONCTIONNALITÉS SPÉCIFIQUES ===

class JSONOutputMixin:
    """Mixin pour les agents qui retournent du JSON."""
    
    import json
    
    async def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse une réponse JSON du LLM."""
        try:
            # Nettoyer la réponse (enlever les balises markdown si présentes)
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return self.json.loads(cleaned)
        except self.json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {e}")
            return {"error": "Invalid JSON response", "raw": response}


class MultilingualMixin:
    """Mixin pour les agents multilingues."""
    
    LANGUAGE_INSTRUCTIONS = {
        "fr": "Réponds en français standard.",
        "ar": "أجب بالعربية الفصحى.",
        "darija": "Jaweb bel darija l'jazairiya.",
        "en": "Respond in English.",
        "de": "Antworte auf Deutsch.",
        "it": "Rispondi in italiano.",
    }
    
    def get_language_instruction(self, language: str) -> str:
        """Retourne l'instruction de langue appropriée."""
        return self.LANGUAGE_INSTRUCTIONS.get(
            language, 
            self.LANGUAGE_INSTRUCTIONS["fr"]
        )
    
    def is_rtl(self, language: str) -> bool:
        """Vérifie si la langue est RTL (Right-to-Left)."""
        return language in ["ar", "darija"]


class CostTrackingMixin:
    """Mixin pour le suivi des coûts en IAF-Tokens."""
    
    def calculate_token_cost(self, service: str, quantity: float = 1) -> int:
        """Calcule le coût en IAF-Tokens."""
        from config import settings
        
        base_cost = settings.TOKEN_COSTS.get(service, 0)
        return int(base_cost * quantity)
    
    def estimate_project_cost(self, components: Dict[str, float]) -> Dict[str, Any]:
        """Estime le coût total d'un projet."""
        breakdown = {}
        total = 0
        
        for service, quantity in components.items():
            cost = self.calculate_token_cost(service, quantity)
            breakdown[service] = {
                "quantity": quantity,
                "cost": cost
            }
            total += cost
        
        return {
            "breakdown": breakdown,
            "total": total,
            "currency": "IAF-Tokens"
        }


# === EXPORT DES AGENTS ===

from .idea_researcher import IdeaResearcherAgent, ContentIdea, IdeaResearchRequest
from .trend_analyzer import TrendAnalyzerAgent, TrendAnalysisRequest, SocialTrend, TrendReport
from .script_coordinator import ScriptCoordinatorAgent, CoordinationRequest, CoordinationResult
from .quality_controller import QualityControllerAgent, QualityCheckRequest, QualityReport
from .scriptwriter import ScriptwriterAgent, VideoScript

__all__ = [
    # Base classes
    "BaseAgent",
    "AgentConfig",
    "AgentResponse",
    "JSONOutputMixin",
    "MultilingualMixin",
    "CostTrackingMixin",
    
    # Agents
    "IdeaResearcherAgent",
    "TrendAnalyzerAgent",
    "ScriptCoordinatorAgent",
    "QualityControllerAgent",
    "ScriptwriterAgent",
    
    # Models
    "ContentIdea",
    "IdeaResearchRequest",
    "TrendAnalysisRequest",
    "SocialTrend",
    "TrendReport",
    "CoordinationRequest",
    "CoordinationResult",
    "QualityCheckRequest",
    "QualityReport",
    "VideoScript",
]
