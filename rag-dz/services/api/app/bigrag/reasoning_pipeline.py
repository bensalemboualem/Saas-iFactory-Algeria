"""
BIG RAG - Reasoning Pipeline
=============================
Step-by-step reasoning avant génération de réponse
Inspiré de awesome-llm-apps/rag_tutorials/agentic_rag_with_reasoning

Pattern: Query Analysis → Context Evaluation → Reasoning → Answer
"""

import os
import logging
import json
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
import httpx

logger = logging.getLogger(__name__)


# ============================================
# MODELS
# ============================================

class ReasoningStep(BaseModel):
    """Étape de raisonnement"""
    step_number: int
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None


class QueryAnalysis(BaseModel):
    """Analyse de la requête"""
    original_query: str
    intent: str  # question, instruction, clarification
    complexity: str  # simple, moderate, complex
    requires_context: bool
    key_entities: List[str]
    sub_questions: List[str] = Field(default_factory=list)


class ContextEvaluation(BaseModel):
    """Évaluation de la pertinence des contextes"""
    context_id: str
    relevance_score: float  # 0-1
    covers_query: bool
    missing_aspects: List[str] = Field(default_factory=list)
    key_facts: List[str] = Field(default_factory=list)


class ReasoningResult(BaseModel):
    """Résultat du raisonnement"""
    query_analysis: QueryAnalysis
    context_evaluations: List[ContextEvaluation]
    reasoning_steps: List[ReasoningStep]
    final_reasoning: str
    confidence: float
    suggested_answer_approach: str
    reasoning_time_ms: float


# ============================================
# PROMPTS
# ============================================

QUERY_ANALYSIS_PROMPT = """Tu es un expert en analyse de requêtes. Analyse la question suivante et fournis:

Question: {query}

Réponds en JSON avec:
{{
    "intent": "question|instruction|clarification",
    "complexity": "simple|moderate|complex",
    "requires_context": true/false,
    "key_entities": ["entité1", "entité2"],
    "sub_questions": ["sous-question1", "sous-question2"]
}}

JSON:"""


CONTEXT_EVALUATION_PROMPT = """Tu es un expert en évaluation de pertinence. Évalue si ce contexte répond à la question.

Question: {query}

Contexte #{context_id}:
{context_text}

Réponds en JSON:
{{
    "relevance_score": 0.0-1.0,
    "covers_query": true/false,
    "missing_aspects": ["aspect1", "aspect2"],
    "key_facts": ["fait1", "fait2"]
}}

JSON:"""


REASONING_PROMPT = """Tu es un assistant expert qui raisonne étape par étape avant de répondre.

Question: {query}

Contextes disponibles:
{contexts}

Évaluations des contextes:
{evaluations}

Raisonne étape par étape:
1. Que demande exactement la question?
2. Quels contextes sont les plus pertinents?
3. Quelles informations clés puis-je extraire?
4. Y a-t-il des contradictions ou des lacunes?
5. Quelle est la meilleure approche pour répondre?

Fournis ton raisonnement en JSON:
{{
    "reasoning_steps": [
        {{"step_number": 1, "thought": "...", "action": "...", "observation": "..."}},
        ...
    ],
    "final_reasoning": "Synthèse du raisonnement",
    "confidence": 0.0-1.0,
    "suggested_answer_approach": "Comment structurer la réponse"
}}

JSON:"""


# ============================================
# REASONING PIPELINE
# ============================================

class ReasoningPipeline:
    """
    Pipeline de raisonnement pour RAG agentic
    
    Étapes:
    1. Analyse de la requête (intent, complexité, entités)
    2. Évaluation des contextes (pertinence, couverture)
    3. Raisonnement step-by-step
    4. Génération de réponse guidée
    """
    
    def __init__(
        self,
        llm_provider: str = "groq",
        model: str = "llama-3.1-70b-versatile",
        enable_full_reasoning: bool = True,
    ):
        self.llm_provider = llm_provider
        self.model = model
        self.enable_full_reasoning = enable_full_reasoning
        
        # API configs
        self.api_keys = {
            "groq": os.getenv("GROQ_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
        }
    
    async def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
        """Appel LLM pour raisonnement"""
        
        if self.llm_provider == "groq":
            return await self._call_groq(prompt, max_tokens)
        elif self.llm_provider == "openai":
            return await self._call_openai(prompt, max_tokens)
        elif self.llm_provider == "anthropic":
            return await self._call_anthropic(prompt, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {self.llm_provider}")
    
    async def _call_groq(self, prompt: str, max_tokens: int) -> str:
        """Appel Groq API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_keys['groq']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def _call_openai(self, prompt: str, max_tokens: int) -> str:
        """Appel OpenAI API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_keys['openai']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def _call_anthropic(self, prompt: str, max_tokens: int) -> str:
        """Appel Anthropic API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_keys['anthropic'],
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": "claude-3-5-haiku-20241022",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Parse JSON depuis réponse LLM"""
        # Extraire le JSON du texte
        try:
            # Essayer directement
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Chercher le JSON dans le texte
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Fallback
        return {}
    
    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Étape 1: Analyser la requête"""
        prompt = QUERY_ANALYSIS_PROMPT.format(query=query)
        
        try:
            response = await self._call_llm(prompt, max_tokens=500)
            data = self._parse_json(response)
            
            return QueryAnalysis(
                original_query=query,
                intent=data.get("intent", "question"),
                complexity=data.get("complexity", "moderate"),
                requires_context=data.get("requires_context", True),
                key_entities=data.get("key_entities", []),
                sub_questions=data.get("sub_questions", []),
            )
        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return QueryAnalysis(
                original_query=query,
                intent="question",
                complexity="moderate",
                requires_context=True,
                key_entities=[],
            )
    
    async def evaluate_context(
        self, 
        query: str, 
        context_id: str, 
        context_text: str
    ) -> ContextEvaluation:
        """Étape 2: Évaluer un contexte"""
        prompt = CONTEXT_EVALUATION_PROMPT.format(
            query=query,
            context_id=context_id,
            context_text=context_text[:1500],  # Limiter la taille
        )
        
        try:
            response = await self._call_llm(prompt, max_tokens=400)
            data = self._parse_json(response)
            
            return ContextEvaluation(
                context_id=context_id,
                relevance_score=float(data.get("relevance_score", 0.5)),
                covers_query=data.get("covers_query", False),
                missing_aspects=data.get("missing_aspects", []),
                key_facts=data.get("key_facts", []),
            )
        except Exception as e:
            logger.error(f"Context evaluation failed: {e}")
            return ContextEvaluation(
                context_id=context_id,
                relevance_score=0.5,
                covers_query=False,
            )
    
    async def reason(
        self,
        query: str,
        contexts: List[Dict[str, Any]],  # [{id, text, score, ...}]
    ) -> ReasoningResult:
        """
        Pipeline complet de raisonnement
        
        Args:
            query: Question utilisateur
            contexts: Contextes récupérés par RAG
            
        Returns:
            ReasoningResult avec analyse et raisonnement
        """
        import time
        start = time.time()
        
        # 1. Analyse de la requête
        query_analysis = await self.analyze_query(query)
        
        # 2. Évaluation des contextes (en parallèle serait mieux)
        context_evaluations = []
        for ctx in contexts[:5]:  # Limiter à 5 contextes
            eval_result = await self.evaluate_context(
                query=query,
                context_id=str(ctx.get("id", "")),
                context_text=ctx.get("text", ""),
            )
            context_evaluations.append(eval_result)
        
        # 3. Raisonnement step-by-step
        if self.enable_full_reasoning:
            contexts_text = "\n\n".join([
                f"[{i+1}] {ctx.get('text', '')[:500]}..."
                for i, ctx in enumerate(contexts[:5])
            ])
            
            evaluations_text = "\n".join([
                f"- Contexte {e.context_id}: relevance={e.relevance_score:.2f}, "
                f"covers_query={e.covers_query}, key_facts={e.key_facts[:2]}"
                for e in context_evaluations
            ])
            
            prompt = REASONING_PROMPT.format(
                query=query,
                contexts=contexts_text,
                evaluations=evaluations_text,
            )
            
            try:
                response = await self._call_llm(prompt, max_tokens=1500)
                data = self._parse_json(response)
                
                reasoning_steps = [
                    ReasoningStep(**step)
                    for step in data.get("reasoning_steps", [])
                ]
                final_reasoning = data.get("final_reasoning", "")
                confidence = float(data.get("confidence", 0.5))
                suggested_approach = data.get("suggested_answer_approach", "")
                
            except Exception as e:
                logger.error(f"Reasoning failed: {e}")
                reasoning_steps = []
                final_reasoning = "Reasoning unavailable"
                confidence = 0.5
                suggested_approach = "Direct answer based on context"
        else:
            reasoning_steps = []
            final_reasoning = "Quick mode - no detailed reasoning"
            confidence = 0.7
            suggested_approach = "Direct answer"
        
        elapsed_ms = (time.time() - start) * 1000
        
        return ReasoningResult(
            query_analysis=query_analysis,
            context_evaluations=context_evaluations,
            reasoning_steps=reasoning_steps,
            final_reasoning=final_reasoning,
            confidence=confidence,
            suggested_answer_approach=suggested_approach,
            reasoning_time_ms=elapsed_ms,
        )
    
    def build_enhanced_prompt(
        self,
        query: str,
        contexts: List[Dict[str, Any]],
        reasoning: ReasoningResult,
    ) -> str:
        """
        Construire un prompt amélioré avec le raisonnement
        
        Le prompt final inclut:
        - L'analyse de la question
        - Les contextes les plus pertinents
        - Le raisonnement step-by-step
        - Des instructions de réponse
        """
        # Filtrer les contextes par pertinence
        relevant_contexts = []
        for ctx, eval_result in zip(contexts, reasoning.context_evaluations):
            if eval_result.relevance_score >= 0.5:
                relevant_contexts.append({
                    **ctx,
                    "relevance": eval_result.relevance_score,
                    "key_facts": eval_result.key_facts,
                })
        
        contexts_section = "\n\n".join([
            f"### Source {i+1} (pertinence: {ctx.get('relevance', 0):.0%})\n"
            f"{ctx.get('text', '')}\n"
            f"Faits clés: {', '.join(ctx.get('key_facts', []))}"
            for i, ctx in enumerate(relevant_contexts[:5])
        ])
        
        reasoning_section = ""
        if reasoning.reasoning_steps:
            reasoning_section = "\n".join([
                f"Étape {step.step_number}: {step.thought}"
                for step in reasoning.reasoning_steps[:5]
            ])
        
        prompt = f"""Tu es un assistant expert. Voici une analyse préalable de la question.

## Question
{query}

## Analyse de la question
- Intent: {reasoning.query_analysis.intent}
- Complexité: {reasoning.query_analysis.complexity}
- Entités clés: {', '.join(reasoning.query_analysis.key_entities)}

## Contextes pertinents
{contexts_section}

## Raisonnement préalable
{reasoning_section}

Synthèse: {reasoning.final_reasoning}
Approche suggérée: {reasoning.suggested_answer_approach}
Confiance: {reasoning.confidence:.0%}

## Instructions
1. Réponds de manière structurée et complète
2. Base-toi uniquement sur les contextes fournis
3. Si les contextes sont insuffisants, indique-le clairement
4. Cite tes sources quand pertinent

## Réponse"""
        
        return prompt


# Singleton instance
reasoning_pipeline = ReasoningPipeline()
