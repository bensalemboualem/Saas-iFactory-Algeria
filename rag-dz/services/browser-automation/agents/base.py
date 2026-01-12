"""
Base Agent pour Browser Automation
Utilise Browser-Use + Ollama
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import os
import json

from browser_use import Agent
from langchain_ollama import ChatOllama

from config import settings


class BaseAutomationAgent(ABC):
    """Agent de base pour l'automatisation navigateur"""
    
    def __init__(self):
        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.1
        )
        
        self.screenshots_dir = settings.SCREENSHOTS_DIR
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    @property
    @abstractmethod
    def service_name(self) -> str:
        """Nom du service (sonelgaz, cnas, etc.)"""
        pass
    
    @property
    @abstractmethod
    def base_url(self) -> str:
        """URL de base du service"""
        pass
    
    async def run_task(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Exécuter une tâche d'automatisation
        
        Args:
            task: Description de la tâche en langage naturel
            context: Contexte additionnel (identifiants, etc.)
        
        Returns:
            Résultat de la tâche
        """
        try:
            agent = Agent(
                task=task,
                llm=self.llm
            )
            
            result = await agent.run()
            
            return {
                "success": True,
                "service": self.service_name,
                "task": task,
                "result": str(result),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "service": self.service_name,
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_result(self, data: Dict[str, Any], filename: str):
        """Sauvegarder résultat en JSON"""
        path = os.path.join(settings.DATA_DIR, filename)
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
