"""
Cloud LLM Client for RAG generation (OpenAI/Anthropic/Groq)
"""
import logging
import os
from typing import List, Dict, Optional
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CloudLLMClient:
    """Client for Ollama LLM API"""

    def __init__(self):
        self.base_url = getattr(settings, 'ollama_base_url', 'http://ollama:11434')
        self.model = getattr(settings, 'ollama_model', 'llama3.2')
        self.timeout = 60

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> Optional[str]:
        """
        Generate text using Ollama

        Args:
            prompt: User prompt
            system: System message
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None on error
        """
        try:
            # Build messages
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                logger.error(f"Ollama error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            return None
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return None

    def generate_rag_answer(
        self,
        query: str,
        context_chunks: List[Dict],
        language: str = "fr"
    ) -> str:
        """
        Generate RAG answer from query and context

        Args:
            query: User question
            context_chunks: List of relevant document chunks
            language: Language for response

        Returns:
            Generated answer
        """
        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks[:3], 1):
            title = chunk.get('title', f'Document {i}')
            text = chunk.get('text', '')[:500]
            context_parts.append(f"[{title}]\n{text}")

        context = "\n\n".join(context_parts)

        # Language-specific system prompts
        system_prompts = {
            "fr": "Tu es un assistant IA qui répond précisément aux questions en te basant uniquement sur les documents fournis. Si l'information n'est pas dans les documents, dis-le clairement.",
            "ar": "أنت مساعد ذكاء اصطناعي يجيب على الأسئلة بدقة بناءً على المستندات المقدمة فقط. إذا لم تكن المعلومات في المستندات، قل ذلك بوضوح.",
            "en": "You are an AI assistant that answers questions precisely based only on the provided documents. If the information is not in the documents, state it clearly."
        }

        prompts = {
            "fr": f"""Documents de référence :
{context}

Question : {query}

Réponds à la question en te basant sur les documents ci-dessus. Sois précis et concis.""",
            "ar": f"""المستندات المرجعية:
{context}

السؤال: {query}

أجب على السؤال بناءً على المستندات أعلاه. كن دقيقاً وموجزاً.""",
            "en": f"""Reference documents:
{context}

Question: {query}

Answer the question based on the documents above. Be precise and concise."""
        }

        system_prompt = system_prompts.get(language, system_prompts["fr"])
        user_prompt = prompts.get(language, prompts["fr"])

        # Generate answer
        answer = self.generate(
            prompt=user_prompt,
            system=system_prompt,
            temperature=0.3,  # Lower temperature for factual answers
            max_tokens=512
        )

        if answer:
            return answer

        # Fallback to basic context extraction
        if language == "ar":
            return f"بناءً على المستندات الموجودة:\n\n{context[:400]}..."
        elif language == "en":
            return f"Based on the found documents:\n\n{context[:400]}..."
        else:
            return f"Basé sur les documents trouvés:\n\n{context[:400]}..."


# Global client instance
ollama_client = OllamaClient()
