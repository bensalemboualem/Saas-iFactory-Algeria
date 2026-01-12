"""
BIG RAG - Query Router
=======================
Router intelligent pour diriger les requêtes vers les bonnes collections
Inspiré de awesome-llm-apps/rag_tutorials/rag_database_routing

Pattern: Analyse sémantique → Classification → Routing → Multi-collection search
"""

import os
import logging
import json
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from pydantic import BaseModel, Field
import httpx
import re

logger = logging.getLogger(__name__)


# ============================================
# MODELS
# ============================================

class CollectionType(str, Enum):
    """Types de collections disponibles"""
    # Par pays
    DZ = "rag_dz"           # Algérie
    CH = "rag_ch"           # Suisse
    FR = "rag_fr"           # France
    GLOBAL = "rag_global"   # International
    
    # Par domaine (extensible)
    LEGAL = "rag_legal"
    FINANCE = "rag_finance"
    HR = "rag_hr"
    TECH = "rag_tech"


class RoutingDecision(BaseModel):
    """Décision de routage"""
    primary_collection: str
    secondary_collections: List[str] = Field(default_factory=list)
    confidence: float
    reasoning: str
    detected_entities: List[str] = Field(default_factory=list)
    detected_country: Optional[str] = None
    detected_domain: Optional[str] = None


class CollectionConfig(BaseModel):
    """Configuration d'une collection"""
    name: str
    collection_id: str
    description: str
    keywords: List[str] = Field(default_factory=list)
    country: Optional[str] = None
    domain: Optional[str] = None
    priority: int = 0  # Plus haut = plus prioritaire


# ============================================
# COLLECTION REGISTRY
# ============================================

COLLECTION_REGISTRY: Dict[str, CollectionConfig] = {
    "rag_dz": CollectionConfig(
        name="Algérie",
        collection_id="rag_dz",
        description="Documents et réglementations algériennes (fiscalité, CNAS, CASNOS, droit du travail)",
        keywords=[
            "algérie", "algérien", "algérienne", "dz", "dinar", "dzd",
            "cnas", "casnos", "cnr", "dgi", "impôts algérie",
            "irg", "ibs", "tap", "tva algérie",
            "wilaya", "daïra", "commune",
            "registre commerce", "cnrc", "nis", "nif",
            "code travail algérie", "inspection travail",
            # Arabe
            "الجزائر", "الجزائرية", "دينار", "ضريبة",
            # Darija
            "dzayer", "dz",
        ],
        country="DZ",
        priority=10,
    ),
    "rag_ch": CollectionConfig(
        name="Suisse",
        collection_id="rag_ch",
        description="Documents et réglementations suisses (AVS, LPP, fiscalité cantonale)",
        keywords=[
            "suisse", "suisses", "helvétique", "ch", "chf", "franc suisse",
            "avs", "lpp", "ai", "apc", "suva", "lac",
            "afc", "impôt fédéral", "impôt cantonal",
            "canton", "commune suisse",
            "oasi", "lainf", "laca",
            "registre commerce suisse", "rc suisse",
            "code obligations", "co suisse",
            # Allemand
            "schweiz", "ahv", "bvg", "mwst",
            # Italien
            "svizzera",
        ],
        country="CH",
        priority=10,
    ),
    "rag_fr": CollectionConfig(
        name="France",
        collection_id="rag_fr",
        description="Documents et réglementations françaises (URSSAF, impôts, droit du travail)",
        keywords=[
            "france", "français", "française", "fr", "euro", "eur",
            "urssaf", "cpam", "caf", "pôle emploi",
            "impôt revenu", "impôt sociétés", "tva france",
            "smic", "code travail france",
            "siret", "siren", "kbis",
            "département", "région",
        ],
        country="FR",
        priority=8,
    ),
    "rag_global": CollectionConfig(
        name="International",
        collection_id="rag_global",
        description="Documents généraux, normes internationales, best practices",
        keywords=[
            "international", "mondial", "global",
            "iso", "ifrs", "ias",
            "ocde", "onu", "fmi",
            "général", "universel",
        ],
        country=None,
        priority=1,
    ),
}


# ============================================
# KEYWORD-BASED ROUTER (Fast)
# ============================================

class KeywordRouter:
    """
    Router basé sur les mots-clés
    Rapide, déterministe, pas de latence LLM
    """
    
    def __init__(self, registry: Dict[str, CollectionConfig] = None):
        self.registry = registry or COLLECTION_REGISTRY
        self._build_keyword_index()
    
    def _build_keyword_index(self):
        """Construire l'index inversé des mots-clés"""
        self.keyword_to_collection: Dict[str, List[Tuple[str, int]]] = {}
        
        for collection_id, config in self.registry.items():
            for keyword in config.keywords:
                kw_lower = keyword.lower()
                if kw_lower not in self.keyword_to_collection:
                    self.keyword_to_collection[kw_lower] = []
                self.keyword_to_collection[kw_lower].append(
                    (collection_id, config.priority)
                )
    
    def route(self, query: str) -> RoutingDecision:
        """Router une requête basé sur les mots-clés"""
        query_lower = query.lower()
        
        # Compter les matches par collection
        collection_scores: Dict[str, float] = {}
        matched_keywords: Dict[str, List[str]] = {}
        
        for keyword, collections in self.keyword_to_collection.items():
            if keyword in query_lower:
                for collection_id, priority in collections:
                    if collection_id not in collection_scores:
                        collection_scores[collection_id] = 0
                        matched_keywords[collection_id] = []
                    
                    # Score = nombre de matches * priorité
                    collection_scores[collection_id] += priority
                    matched_keywords[collection_id].append(keyword)
        
        if not collection_scores:
            # Aucun match → Global par défaut
            return RoutingDecision(
                primary_collection="rag_global",
                secondary_collections=[],
                confidence=0.3,
                reasoning="Aucun mot-clé spécifique détecté, utilisation de la collection globale",
                detected_entities=[],
            )
        
        # Trier par score
        sorted_collections = sorted(
            collection_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        
        primary = sorted_collections[0][0]
        primary_score = sorted_collections[0][1]
        
        # Calculer la confiance (normalisée)
        max_possible_score = sum(
            c.priority * len(c.keywords) 
            for c in self.registry.values()
        ) / 10
        confidence = min(primary_score / max_possible_score, 1.0)
        
        # Collections secondaires (score > 50% du primaire)
        secondary = [
            coll_id for coll_id, score in sorted_collections[1:4]
            if score >= primary_score * 0.5
        ]
        
        # Ajouter global si pas déjà inclus et confiance < 80%
        if "rag_global" not in [primary] + secondary and confidence < 0.8:
            secondary.append("rag_global")
        
        return RoutingDecision(
            primary_collection=primary,
            secondary_collections=secondary,
            confidence=confidence,
            reasoning=f"Mots-clés détectés: {', '.join(matched_keywords.get(primary, []))}",
            detected_entities=matched_keywords.get(primary, []),
            detected_country=self.registry.get(primary, CollectionConfig(
                name="", collection_id="", description=""
            )).country,
        )


# ============================================
# LLM-BASED ROUTER (Semantic)
# ============================================

LLM_ROUTING_PROMPT = """Tu es un expert en routage de requêtes. Analyse la question et détermine quelle(s) base(s) de données consulter.

Question: {query}

Collections disponibles:
{collections_desc}

Réponds en JSON:
{{
    "primary_collection": "id de la collection principale",
    "secondary_collections": ["ids des collections secondaires"],
    "confidence": 0.0-1.0,
    "reasoning": "Explication du choix",
    "detected_country": "DZ|CH|FR|null",
    "detected_domain": "legal|finance|hr|tech|null"
}}

JSON:"""


class LLMRouter:
    """
    Router basé sur LLM
    Plus intelligent, comprend le contexte sémantique
    Plus lent, nécessite un appel API
    """
    
    def __init__(
        self,
        registry: Dict[str, CollectionConfig] = None,
        llm_provider: str = "groq",
        model: str = "llama-3.1-8b-instant",
    ):
        self.registry = registry or COLLECTION_REGISTRY
        self.llm_provider = llm_provider
        self.model = model
        self.api_key = os.getenv("GROQ_API_KEY")
    
    async def route(self, query: str) -> RoutingDecision:
        """Router une requête via LLM"""
        
        # Construire la description des collections
        collections_desc = "\n".join([
            f"- {coll_id}: {config.description}"
            for coll_id, config in self.registry.items()
        ])
        
        prompt = LLM_ROUTING_PROMPT.format(
            query=query,
            collections_desc=collections_desc,
        )
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 300,
                        "temperature": 0.1,
                    },
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
            
            # Parser le JSON
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError("No JSON in response")
            
            return RoutingDecision(
                primary_collection=result.get("primary_collection", "rag_global"),
                secondary_collections=result.get("secondary_collections", []),
                confidence=float(result.get("confidence", 0.5)),
                reasoning=result.get("reasoning", "LLM routing"),
                detected_country=result.get("detected_country"),
                detected_domain=result.get("detected_domain"),
            )
            
        except Exception as e:
            logger.error(f"LLM routing failed: {e}")
            # Fallback to keyword router
            keyword_router = KeywordRouter(self.registry)
            return keyword_router.route(query)


# ============================================
# HYBRID ROUTER (Best of both)
# ============================================

class HybridQueryRouter:
    """
    Router hybride combinant keyword + LLM
    
    Stratégie:
    1. Keyword routing rapide
    2. Si confiance < seuil, utiliser LLM
    3. Fusionner les décisions
    """
    
    def __init__(
        self,
        registry: Dict[str, CollectionConfig] = None,
        confidence_threshold: float = 0.7,
        use_llm_fallback: bool = True,
    ):
        self.registry = registry or COLLECTION_REGISTRY
        self.confidence_threshold = confidence_threshold
        self.use_llm_fallback = use_llm_fallback
        
        self.keyword_router = KeywordRouter(self.registry)
        self.llm_router = LLMRouter(self.registry) if use_llm_fallback else None
    
    async def route(self, query: str) -> RoutingDecision:
        """
        Router une requête avec stratégie hybride
        
        Args:
            query: Question utilisateur
            
        Returns:
            RoutingDecision avec collections à interroger
        """
        # 1. Keyword routing (rapide)
        keyword_result = self.keyword_router.route(query)
        
        # 2. Si confiance suffisante, retourner directement
        if keyword_result.confidence >= self.confidence_threshold:
            logger.info(f"Keyword routing: {keyword_result.primary_collection} (conf={keyword_result.confidence:.2f})")
            return keyword_result
        
        # 3. Sinon, utiliser LLM si activé
        if self.use_llm_fallback and self.llm_router:
            try:
                llm_result = await self.llm_router.route(query)
                
                # Fusionner les résultats
                # Prioriser LLM si plus confiant
                if llm_result.confidence > keyword_result.confidence:
                    # Combiner les collections secondaires
                    all_secondary = list(set(
                        llm_result.secondary_collections + 
                        keyword_result.secondary_collections
                    ))
                    if keyword_result.primary_collection not in [llm_result.primary_collection] + all_secondary:
                        all_secondary.append(keyword_result.primary_collection)
                    
                    llm_result.secondary_collections = all_secondary[:3]
                    logger.info(f"LLM routing: {llm_result.primary_collection} (conf={llm_result.confidence:.2f})")
                    return llm_result
                
            except Exception as e:
                logger.warning(f"LLM routing failed, using keyword result: {e}")
        
        # Fallback: keyword result
        return keyword_result
    
    def get_collections_to_search(
        self, 
        decision: RoutingDecision,
        include_global: bool = True,
        max_collections: int = 3,
    ) -> List[str]:
        """
        Obtenir la liste des collections à chercher
        
        Args:
            decision: Décision de routage
            include_global: Toujours inclure rag_global
            max_collections: Nombre max de collections
            
        Returns:
            Liste des IDs de collections
        """
        collections = [decision.primary_collection]
        collections.extend(decision.secondary_collections)
        
        if include_global and "rag_global" not in collections:
            collections.append("rag_global")
        
        # Dédupliquer et limiter
        seen = set()
        unique_collections = []
        for coll in collections:
            if coll not in seen:
                seen.add(coll)
                unique_collections.append(coll)
        
        return unique_collections[:max_collections]


# Singleton instances
keyword_router = KeywordRouter()
hybrid_router = HybridQueryRouter()
