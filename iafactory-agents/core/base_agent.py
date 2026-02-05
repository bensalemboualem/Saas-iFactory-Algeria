"""
Base Agent Class for IA Factory
All LLM calls route through the gateway (http://localhost:3001)
"""
from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
import httpx
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:3001")

class AgentConfig(BaseModel):
    name: str
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 2000
    tools: List[str] = Field(default_factory=list)
    memory_enabled: bool = True
    language: str = "fr"
    system_prompt: Optional[str] = None

class AgentMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentResponse(BaseModel):
    content: str
    tools_used: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: Optional[int] = None
    duration_ms: Optional[float] = None

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory: List[AgentMessage] = [] if config.memory_enabled else None
        self.tools_registry: Dict[str, Callable] = {}
        logger.info(f"Initialized {config.name} with model {config.model} via gateway {GATEWAY_URL}")

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        pass

    def add_memory(self, message: AgentMessage):
        if self.memory is not None:
            self.memory.append(message)
            if len(self.memory) > 50:
                self.memory = self.memory[-50:]

    async def _call_llm(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{GATEWAY_URL}/api/llm/chat/completions",
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "temperature": self.config.temperature,
                        "max_tokens": self.config.max_tokens,
                    },
                )
                response.raise_for_status()
                data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return {"content": content, "tokens": tokens}
        except Exception as e:
            logger.error(f"LLM call via gateway failed: {e}")
            return {"content": f"Erreur: {str(e)}", "tokens": 0}

class MultiAgentTeam:
    def __init__(self, agents: List[BaseAgent], orchestrator: str = "sequential"):
        self.agents = agents
        self.orchestrator = orchestrator
    
    async def execute_all(self, input_data: Dict[str, Any]) -> List[AgentResponse]:
        results = []
        for agent in self.agents:
            result = await agent.execute(input_data)
            results.append(result)
        return results
