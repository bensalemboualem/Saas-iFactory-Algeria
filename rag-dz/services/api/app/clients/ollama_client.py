import os
import requests
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
DEFAULT_MODEL = "llama3.2:3b"

class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 60
    
    def generate_response(
        self, 
        query: str, 
        context: str, 
        language: str = "fr",
        model: str = DEFAULT_MODEL
    ) -> str:
        """Génère une réponse basée sur la question et le contexte"""
        
        # Prompts adaptés par langue
        prompts = {
            "fr": f"""Contexte: {context}

Question: {query}

Instructions: Réponds uniquement en français, de manière concise et précise, en te basant sur le contexte fourni. Si l'information n'est pas dans le contexte, dis-le clairement.

Réponse:""",
            "en": f"""Context: {context}

Question: {query}

Instructions: Answer only in English, concisely and accurately, based on the provided context. If the information is not in the context, state it clearly.

Answer:""",
            "ar": f"""السياق: {context}

السؤال: {query}

التعليمات: أجب باللغة العربية فقط، بشكل موجز ودقيق، بناءً على السياق المقدم. إذا لم تكن المعلومات في السياق، اذكر ذلك بوضوح.

الإجابة:"""
        }
        
        prompt = prompts.get(language, prompts["fr"])
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 512
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Erreur lors de la génération de réponse").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return f"Erreur API Ollama (status: {response.status_code})"
                
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return "Délai d'attente dépassé lors de la génération de réponse"
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            return "Service de génération temporairement indisponible"
        except Exception as e:
            logger.error(f"Ollama client error: {e}")
            return f"Erreur lors de la génération: {str(e)}"
    
    def is_available(self) -> bool:
        """Vérifie si Ollama est disponible"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """Liste les modèles disponibles"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return []

# Instance globale
ollama_client = OllamaClient()