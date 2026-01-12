"""
Context Window Optimizer - Intelligent Token Management
Handles context compression, sliding windows, and summarization for long conversations
Token tracking integre.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import tiktoken
from pydantic import BaseModel

from app.config import get_settings

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    TOKENS_AVAILABLE = True
except ImportError:
    TOKENS_AVAILABLE = False

logger = logging.getLogger(__name__)
settings = get_settings()


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """Chat message with token count"""
    role: MessageRole
    content: str
    tokens: int = 0
    importance: float = 1.0  # 0-1, higher = more important
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TokenizerService:
    """
    Token counting and encoding service
    Supports multiple models
    """

    MODEL_ENCODINGS = {
        "gpt-4": "cl100k_base",
        "gpt-4o": "o200k_base",
        "gpt-4o-mini": "o200k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "claude-3": "cl100k_base",  # Approximation
        "llama": "cl100k_base",     # Approximation
    }

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self._encoder = None

    @property
    def encoder(self):
        if self._encoder is None:
            encoding_name = self.MODEL_ENCODINGS.get(
                self.model.split("-")[0] + "-" + self.model.split("-")[1] if "-" in self.model else self.model,
                "cl100k_base"
            )
            try:
                self._encoder = tiktoken.get_encoding(encoding_name)
            except Exception:
                self._encoder = tiktoken.get_encoding("cl100k_base")
        return self._encoder

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoder.encode(text))

    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens for chat messages with overhead
        Based on OpenAI's token counting guidelines
        """
        tokens = 0
        for message in messages:
            tokens += 4  # Message overhead
            for key, value in message.items():
                tokens += self.count_tokens(str(value))
                if key == "name":
                    tokens += -1
        tokens += 2  # Reply priming
        return tokens

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to max tokens"""
        tokens = self.encoder.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoder.decode(tokens[:max_tokens])


class ContextCompressor:
    """
    Compress context using various strategies
    """

    def __init__(self, tokenizer: TokenizerService):
        self.tokenizer = tokenizer

    async def compress_by_importance(
        self,
        messages: List[Message],
        target_tokens: int
    ) -> List[Message]:
        """
        Compress by removing low-importance messages
        """
        # Sort by importance (keep system and recent messages)
        def message_score(msg: Message, idx: int, total: int) -> float:
            # System messages are always important
            if msg.role == MessageRole.SYSTEM:
                return 1000

            # Recent messages are more important
            recency_score = (idx + 1) / total

            # Combine with explicit importance
            return msg.importance * 0.5 + recency_score * 0.5

        scored = [
            (msg, message_score(msg, i, len(messages)))
            for i, msg in enumerate(messages)
        ]

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        # Add messages until we hit token limit
        result = []
        current_tokens = 0
        for msg, score in scored:
            if current_tokens + msg.tokens <= target_tokens:
                result.append(msg)
                current_tokens += msg.tokens

        # Restore original order
        result.sort(key=lambda x: messages.index(x) if x in messages else 0)

        return result

    async def compress_by_summarization(
        self,
        messages: List[Message],
        target_tokens: int,
        tenant_id: Optional[str] = None
    ) -> List[Message]:
        """
        Compress old messages by summarizing them with token tracking
        """
        # Separate system message and recent messages
        system_msgs = [m for m in messages if m.role == MessageRole.SYSTEM]
        recent_msgs = messages[-4:]  # Keep last 4 messages
        old_msgs = messages[len(system_msgs):-4] if len(messages) > len(system_msgs) + 4 else []

        if not old_msgs:
            return messages

        # Summarize old messages
        old_content = "\n".join([
            f"{m.role.value}: {m.content}"
            for m in old_msgs
        ])

        summary = await self._generate_summary(old_content, tenant_id=tenant_id)

        # Create summary message
        summary_message = Message(
            role=MessageRole.SYSTEM,
            content=f"[Résumé de la conversation précédente]\n{summary}",
            tokens=self.tokenizer.count_tokens(summary) + 10,
            importance=0.8
        )

        result = system_msgs + [summary_message] + recent_msgs

        # Check if we're under target
        total_tokens = sum(m.tokens for m in result)
        if total_tokens > target_tokens:
            # Need more aggressive compression
            return await self.compress_by_importance(result, target_tokens)

        return result

    async def _generate_summary(self, content: str, max_tokens: int = 200, tenant_id: Optional[str] = None) -> str:
        """Generate summary of conversation content with token tracking"""
        try:
            import openai

            system_prompt = "Résume cette conversation de manière concise, en gardant les points clés et les décisions prises."

            # Token tracking: verifier solde AVANT l'appel
            if TOKENS_AVAILABLE and tenant_id:
                estimated_tokens = len((system_prompt + content).split()) + 300
                try:
                    check_token_balance(tenant_id, estimated_tokens)
                except InsufficientTokensError:
                    # Fall back to truncation if insufficient tokens
                    logger.warning("Insufficient tokens for summarization, falling back to truncation")
                    return self.tokenizer.truncate_to_tokens(content, max_tokens)

            client = openai.OpenAI(api_key=settings.openai_api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )

            # Token tracking: deduire tokens APRES l'appel
            if TOKENS_AVAILABLE and tenant_id and response.usage:
                try:
                    deduct_after_llm_call(
                        tenant_id=tenant_id,
                        provider="openai",
                        model="gpt-4o-mini",
                        tokens_input=response.usage.prompt_tokens,
                        tokens_output=response.usage.completion_tokens
                    )
                except Exception as e:
                    logger.warning(f"Token deduction failed (context_optimizer): {e}")

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            # Fallback: truncate
            return self.tokenizer.truncate_to_tokens(content, max_tokens)


class SlidingWindowManager:
    """
    Manages sliding context window for very long conversations
    """

    def __init__(
        self,
        max_tokens: int = 8000,
        window_overlap: int = 500,
        model: str = "gpt-4o"
    ):
        self.max_tokens = max_tokens
        self.window_overlap = window_overlap
        self.tokenizer = TokenizerService(model)
        self.compressor = ContextCompressor(self.tokenizer)

    async def process_messages(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None,
        tenant_id: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Process messages to fit within context window with token tracking
        """
        # Convert to Message objects
        msg_objects = []

        if system_prompt:
            msg_objects.append(Message(
                role=MessageRole.SYSTEM,
                content=system_prompt,
                tokens=self.tokenizer.count_tokens(system_prompt),
                importance=1.0
            ))

        for msg in messages:
            role = MessageRole(msg.get("role", "user"))
            content = msg.get("content", "")
            msg_objects.append(Message(
                role=role,
                content=content,
                tokens=self.tokenizer.count_tokens(content),
                importance=self._calculate_importance(role, content)
            ))

        # Calculate total tokens
        total_tokens = sum(m.tokens for m in msg_objects)

        if total_tokens <= self.max_tokens:
            # No compression needed
            return self._to_dict_list(msg_objects)

        # Need compression
        logger.info(f"Compressing context: {total_tokens} tokens -> {self.max_tokens} max")

        # Try importance-based first
        compressed = await self.compressor.compress_by_importance(
            msg_objects,
            self.max_tokens
        )

        compressed_tokens = sum(m.tokens for m in compressed)

        # If still too large, use summarization (with token tracking)
        if compressed_tokens > self.max_tokens:
            compressed = await self.compressor.compress_by_summarization(
                msg_objects,
                self.max_tokens,
                tenant_id=tenant_id
            )

        return self._to_dict_list(compressed)

    def _calculate_importance(self, role: MessageRole, content: str) -> float:
        """Calculate message importance score"""
        importance = 0.5

        # User messages slightly more important
        if role == MessageRole.USER:
            importance += 0.1

        # Longer messages more important
        word_count = len(content.split())
        if word_count > 50:
            importance += 0.2
        elif word_count > 20:
            importance += 0.1

        # Code blocks are important
        if "```" in content:
            importance += 0.2

        # Questions are important
        if "?" in content:
            importance += 0.1

        return min(importance, 1.0)

    def _to_dict_list(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert Message objects to dict list"""
        return [
            {"role": m.role.value, "content": m.content}
            for m in messages
        ]


class ContextOptimizer:
    """
    Main context optimizer with full feature set
    """

    # Model context limits
    MODEL_LIMITS = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-4o": 128000,
        "gpt-4o-mini": 128000,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
        "claude-3-opus": 200000,
        "claude-3-sonnet": 200000,
        "claude-3-haiku": 200000,
        "llama-3.3-70b": 128000,
    }

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.tokenizer = TokenizerService(model)
        self.max_context = self.MODEL_LIMITS.get(model, 8192)
        self.window_manager = SlidingWindowManager(
            max_tokens=int(self.max_context * 0.8),  # Leave room for response
            model=model
        )

    async def optimize(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None,
        max_response_tokens: int = 2000,
        rag_context: str = None,
        tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize context for LLM call with token tracking

        Args:
            messages: Chat history
            system_prompt: System prompt
            max_response_tokens: Reserved tokens for response
            rag_context: Optional RAG context to include
            tenant_id: Tenant ID for token tracking

        Returns:
            Dict with optimized messages and metadata
        """
        # Calculate available tokens
        available_tokens = self.max_context - max_response_tokens

        # Count fixed tokens
        fixed_tokens = 0
        if system_prompt:
            fixed_tokens += self.tokenizer.count_tokens(system_prompt)
        if rag_context:
            fixed_tokens += self.tokenizer.count_tokens(rag_context)

        # Available for conversation
        conversation_budget = available_tokens - fixed_tokens

        # Optimize messages (with token tracking for summarization)
        optimized_messages = await self.window_manager.process_messages(
            messages,
            system_prompt=None,  # Handle separately
            tenant_id=tenant_id
        )

        # Count final tokens
        final_tokens = self.tokenizer.count_message_tokens(optimized_messages)

        # Build final message list
        final_messages = []

        # Add system prompt with RAG context
        if system_prompt or rag_context:
            system_content = ""
            if system_prompt:
                system_content = system_prompt
            if rag_context:
                system_content += f"\n\n[Contexte RAG]\n{rag_context}"
            final_messages.append({"role": "system", "content": system_content})

        final_messages.extend(optimized_messages)

        return {
            "messages": final_messages,
            "original_count": len(messages),
            "optimized_count": len(optimized_messages),
            "total_tokens": final_tokens + fixed_tokens,
            "available_tokens": available_tokens,
            "tokens_used_pct": round((final_tokens + fixed_tokens) / available_tokens * 100, 1),
            "model": self.model,
            "max_context": self.max_context
        }

    def get_token_stats(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get token statistics for messages"""
        total_tokens = self.tokenizer.count_message_tokens(messages)
        tokens_per_message = [
            {
                "role": m.get("role"),
                "tokens": self.tokenizer.count_tokens(m.get("content", ""))
            }
            for m in messages
        ]

        return {
            "total_tokens": total_tokens,
            "tokens_per_message": tokens_per_message,
            "average_tokens": total_tokens / len(messages) if messages else 0,
            "max_context": self.max_context,
            "utilization_pct": round(total_tokens / self.max_context * 100, 1)
        }


# Factory function
def get_context_optimizer(model: str = "gpt-4o") -> ContextOptimizer:
    """Get context optimizer for a model"""
    return ContextOptimizer(model)
