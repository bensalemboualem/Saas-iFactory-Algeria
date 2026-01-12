"""
Cloud LLM Client - Support OpenAI, Anthropic, Groq
"""
import logging
from typing import List, Dict, Optional
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CloudLLMClient:
    """Universal cloud LLM client"""

    def __init__(self):
        self.provider = getattr(settings, 'llm_provider', 'openai')
        self.model = getattr(settings, 'llm_model', 'gpt-3.5-turbo')
        self.openai_api_key = getattr(settings, 'openai_api_key', '')
        self.anthropic_api_key = getattr(settings, 'anthropic_api_key', '')

        # Initialize client based on provider
        self.client = None
        if self.provider == 'openai' and self.openai_api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_api_key)
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("openai package not installed")
        elif self.provider == 'anthropic' and self.anthropic_api_key:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.anthropic_api_key)
                logger.info("Anthropic client initialized")
            except ImportError:
                logger.warning("anthropic package not installed")

    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.client is not None

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> Optional[str]:
        """
        Generate text using cloud LLM

        Args:
            prompt: User prompt
            system: System message
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text or None on error
        """
        if not self.client:
            logger.warning("No LLM client available")
            return None

        try:
            if self.provider == 'openai':
                return self._generate_openai(prompt, system, temperature, max_tokens)
            elif self.provider == 'anthropic':
                return self._generate_anthropic(prompt, system, temperature, max_tokens)
            else:
                logger.error(f"Unsupported provider: {self.provider}")
                return None
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return None

    def _generate_openai(self, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        """Generate using OpenAI API"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _generate_anthropic(self, prompt: str, system: Optional[str], temperature: float, max_tokens: int) -> str:
        """Generate using Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "You are a helpful assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

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
        if not self.is_available():
            return self._fallback_answer(context_chunks, language)

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

        # Fallback
        return self._fallback_answer(context_chunks, language)

    def _fallback_answer(self, context_chunks: List[Dict], language: str) -> str:
        """Fallback answer when LLM unavailable"""
        if not context_chunks:
            if language == "ar":
                return "لم يتم العثور على مستندات ذات صلة في قاعدة المعرفة."
            elif language == "en":
                return "No relevant documents found in the knowledge base."
            else:
                return "Aucun document pertinent trouvé dans la base de connaissances."

        context = context_chunks[0].get('text', '')[:400]

        if language == "ar":
            return f"بناءً على المستندات الموجودة:\n\n{context}..."
        elif language == "en":
            return f"Based on the found documents:\n\n{context}..."
        else:
            return f"Basé sur les documents trouvés:\n\n{context}..."


# Global client instance
llm_client = CloudLLMClient()
