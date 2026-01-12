from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    tokens_used: int
    cost: float
    latency_ms: int

class BaseProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
    
    @abstractmethod
    async def generate(
        self, 
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        """Generate completion from messages"""
        pass
    
    @abstractmethod
    def calculate_cost(self, tokens_used: int) -> float:
        """Calculate cost based on tokens used"""
        pass
    
    def format_messages(self, messages: List[Message]) -> Any:
        """Format messages for provider-specific API"""
        return [{role: msg.role, content: msg.content} for msg in messages]
