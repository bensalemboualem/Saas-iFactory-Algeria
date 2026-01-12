"""
DZ-LegalAssistant Backend API
=============================
Assistant juridique & administratif spécialisé Algérie

Endpoints:
- POST /api/dz-legal/answer - Répondre à une question juridique/administrative
- GET /api/dz-legal/categories - Liste des catégories disponibles
- GET /api/dz-legal/examples - Exemples de questions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
import json
import os
import logging
import httpx
from datetime import datetime

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dz-legal-assistant")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
RAG_API_URL = os.getenv("RAG_API_URL", "http://iaf-dz-connectors-prod:8195")

app = FastAPI(
    title="DZ-LegalAssistant API",
    description="Assistant juridique & administratif spécialisé Algérie",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== MODÈLES PYDANTIC ==============

CategoryType = Literal[
    "procédure_administrative",
    "droit_des_affaires", 
    "social_cnas_casnos",
    "impôts_dgi",
    "douane_import_export",
    "autre"
]

class DZLegalRequest(BaseModel):
    """Requête utilisateur"""
    question: str = Field(..., min_length=10, description="Question juridique ou administrative")
    category: CategoryType = Field(default="autre", description="Catégorie de la question")
    user_context: Optional[str] = Field(None, description="Contexte additionnel (situation spécifique)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Quelles sont les étapes pour créer une EURL en Algérie ?",
                "category": "droit_des_affaires",
                "user_context": "Je suis développeur freelance et je veux formaliser mon activité"
            }
        }


class Step(BaseModel):
    """Étape d'une procédure"""
    title: str
    description: str
    checklist: List[str] = []


class ReferenceItem(BaseModel):
    """Référence documentaire"""
    label: str
    source_name: str
    source_url: Optional[str] = None
    date: Optional[str] = None


class DZLegalAnswer(BaseModel):
    """Réponse structurée de l'assistant"""
    summary: str = Field(..., description="Résumé en 3-8 phrases")
    category: str
    steps: List[Step] = Field(..., description="Étapes de la procédure")
    important_notes: List[str] = Field(default=[], description="Points critiques")
    risks_and_limits: List[str] = Field(default=[], description="Limites et incertitudes")
    references: List[ReferenceItem] = Field(default=[], description="Sources documentaires")
    disclaimer: str = Field(..., description="Avertissement légal")
    followup_questions: List[str] = Field(default=[], description="Questions de suivi suggérées")


# ============== PROMPTS SYSTÈME ==============

SYSTEM_PROMPT = """Tu es DZ-LegalAssistant, un assistant spécialisé en procédures administratives et aspects juridiques de base pour l'Algérie, intégré dans la plateforme iaFactory Algeria.

TON RÔLE :
- Expliquer de manière claire et structurée les démarches administratives (registre de commerce, CNAS, CASNOS, impôts, douanes, etc.).
- Proposer une synthèse accessible des textes applicables et des procédures.
- T'aider de documents de contexte (RAG DZ) lorsqu'ils sont fournis.

LIMITES IMPORTANTES :
- Tu n'es PAS un avocat.
- Tu ne fournis PAS de conseil juridique professionnel.
- Tu peux aider à comprendre les textes et les démarches, mais tu dois toujours encourager l'utilisateur à vérifier auprès des autorités compétentes ou d'un professionnel.

FORMAT DE SORTIE :
Tu dois TOUJOURS répondre en JSON strictement valide selon ce schéma :
{
  "summary": "string (résumé en 3-8 phrases)",
  "category": "procédure_administrative" | "droit_des_affaires" | "social_cnas_casnos" | "impôts_dgi" | "douane_import_export" | "autre",
  "steps": [
    {
      "title": "string",
      "description": "string",
      "checklist": ["string"]
    }
  ],
  "important_notes": ["string"],
  "risks_and_limits": ["string"],
  "references": [
    {
      "label": "string",
      "source_name": "string",
      "source_url": "string ou null",
      "date": "string ou null"
    }
  ],
  "disclaimer": "string",
  "followup_questions": ["string"]
}

CONSIGNES :
- Adapte ton langage au contexte algérien (exemples, autorités, formulaires).
- Si les documents RAG sont clairs, appuie-toi dessus et cite-les dans "references".
- Si le sujet est incertain ou que le contexte manque, explique-le clairement dans "risks_and_limits" et dans "disclaimer".
- Le "disclaimer" doit rappeler que tu n'es pas un avocat et que l'utilisateur doit vérifier auprès d'un professionnel ou de l'administration.
- Propose 3 à 6 étapes pratiques avec des checklists concrètes.
- Les "important_notes" doivent mentionner les délais, documents requis, frais éventuels.
- Les "followup_questions" doivent être des questions naturelles que l'utilisateur pourrait poser ensuite.

IMPORTANT :
- AUCUN texte hors du JSON final.
- JSON strictement valide, sans commentaires.
- Réponds en français."""


def build_user_prompt(question: str, category: str, user_context: Optional[str], rag_docs: List[dict]) -> str:
    """Construit le prompt utilisateur avec le contexte RAG"""
    
    # Formater les documents RAG
    rag_context = ""
    if rag_docs:
        rag_context = "\n\nContexte RAG (documents algériens) :\n"
        for i, doc in enumerate(rag_docs, 1):
            rag_context += f"""
[DOC {i} - {doc.get('source', 'Source inconnue')}]
Titre : {doc.get('title', 'Sans titre')}
Extrait : {doc.get('text', '')[:500]}...
Date : {doc.get('date', 'Non datée')}
URL : {doc.get('url', 'N/A')}
"""
    
    prompt = f"""Question utilisateur :
{question}

Catégorie : {category}
"""
    
    if user_context:
        prompt += f"""
Contexte utilisateur :
{user_context}
"""
    
    prompt += rag_context
    
    prompt += """
Tâche :
1. Analyser la question dans le contexte algérien.
2. Utiliser les documents RAG si pertinents.
3. Générer une réponse structurée en JSON selon le schéma décrit dans le system prompt.
4. Mettre en avant les étapes pratiques et les points à risque.
5. Mentionner clairement les limites de ton aide.

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""
    
    return prompt


# ============== SERVICES ==============

async def search_rag(question: str, category: str, limit: int = 5) -> List[dict]:
    """Interroge le RAG DZ pour obtenir des documents pertinents"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Mapper les catégories vers les types de documents
            type_mapping = {
                "procédure_administrative": "procedure",
                "droit_des_affaires": "law",
                "social_cnas_casnos": "procedure",
                "impôts_dgi": "tax",
                "douane_import_export": "procedure",
                "autre": None
            }
            doc_type = type_mapping.get(category)
            
            params = {
                "query": question,
                "limit": limit
            }
            if doc_type:
                params["doc_type"] = doc_type
            
            response = await client.get(
                f"{RAG_API_URL}/api/search",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                logger.warning(f"RAG search failed: {response.status_code}")
                return []
                
    except Exception as e:
        logger.error(f"Error searching RAG: {e}")
        return []


async def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Appelle le LLM (GROQ) pour générer la réponse"""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"LLM call failed: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail="LLM_CALL_FAILED")
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM_TIMEOUT")
    except Exception as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM_ERROR: {str(e)}")


def parse_llm_response(raw_response: str) -> dict:
    """Parse et valide la réponse JSON du LLM"""
    try:
        # Nettoyer la réponse
        cleaned = raw_response.strip()
        
        # Tenter de parser
        data = json.loads(cleaned)
        
        # Valider les champs requis
        required_fields = ["summary", "category", "steps", "disclaimer"]
        for field in required_fields:
            if field not in data:
                data[field] = get_default_value(field)
        
        # Assurer que les listes existent
        for field in ["steps", "important_notes", "risks_and_limits", "references", "followup_questions"]:
            if field not in data or not isinstance(data[field], list):
                data[field] = []
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        logger.debug(f"Raw response: {raw_response[:500]}")
        raise HTTPException(status_code=500, detail="LLM_RESPONSE_PARSE_ERROR")


def get_default_value(field: str):
    """Retourne une valeur par défaut pour un champ manquant"""
    defaults = {
        "summary": "Réponse générée avec des informations limitées.",
        "category": "autre",
        "steps": [],
        "disclaimer": "Cette réponse est fournie à titre informatif uniquement. Elle ne constitue pas un conseil juridique professionnel. Veuillez consulter un avocat ou les autorités compétentes pour toute démarche officielle."
    }
    return defaults.get(field, "")


# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "DZ-LegalAssistant",
        "version": "1.0.0",
        "status": "running",
        "description": "Assistant juridique & administratif Algérie"
    }


@app.get("/health")
async def health():
    """Vérification de santé détaillée"""
    return {
        "status": "healthy",
        "llm_configured": bool(GROQ_API_KEY),
        "rag_url": RAG_API_URL,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/dz-legal/categories")
async def get_categories():
    """Liste des catégories disponibles"""
    return {
        "categories": [
            {
                "id": "procédure_administrative",
                "name": "Procédure administrative",
                "icon": "📋",
                "description": "Démarches auprès des administrations publiques",
                "examples": ["Registre de commerce", "Carte d'artisan", "Agrément"]
            },
            {
                "id": "droit_des_affaires",
                "name": "Droit des affaires",
                "icon": "🏢",
                "description": "Création et gestion d'entreprise",
                "examples": ["EURL", "SARL", "SPA", "Statuts", "Dissolution"]
            },
            {
                "id": "social_cnas_casnos",
                "name": "Social (CNAS/CASNOS)",
                "icon": "👥",
                "description": "Sécurité sociale, cotisations, déclarations",
                "examples": ["Affiliation CNAS", "CASNOS indépendants", "Déclarations"]
            },
            {
                "id": "impôts_dgi",
                "name": "Impôts (DGI)",
                "icon": "💰",
                "description": "Fiscalité, déclarations, obligations",
                "examples": ["IRG", "IBS", "TVA", "TAP", "G50"]
            },
            {
                "id": "douane_import_export",
                "name": "Douane / Import-Export",
                "icon": "🛃",
                "description": "Commerce international, dédouanement",
                "examples": ["Domiciliation", "Licence d'import", "Dédouanement"]
            },
            {
                "id": "autre",
                "name": "Autre",
                "icon": "❓",
                "description": "Questions diverses",
                "examples": []
            }
        ]
    }


@app.get("/api/dz-legal/examples")
async def get_examples():
    """Exemples de questions fréquentes"""
    return {
        "examples": [
            {
                "question": "Quelles sont les étapes pour créer une EURL en Algérie ?",
                "category": "droit_des_affaires"
            },
            {
                "question": "Quelles sont les obligations CNAS pour un employeur ?",
                "category": "social_cnas_casnos"
            },
            {
                "question": "Comment fermer une SARL en Algérie ?",
                "category": "droit_des_affaires"
            },
            {
                "question": "Comment déclarer un salarié à la CNAS ?",
                "category": "social_cnas_casnos"
            },
            {
                "question": "Quels sont les documents nécessaires pour le registre de commerce ?",
                "category": "procédure_administrative"
            },
            {
                "question": "Comment obtenir un NIF (Numéro d'Identification Fiscale) ?",
                "category": "impôts_dgi"
            },
            {
                "question": "Quelles sont les étapes pour importer des marchandises en Algérie ?",
                "category": "douane_import_export"
            },
            {
                "question": "Comment s'affilier à la CASNOS en tant qu'indépendant ?",
                "category": "social_cnas_casnos"
            },
            {
                "question": "Quelles déclarations fiscales mensuelles dois-je faire (G50) ?",
                "category": "impôts_dgi"
            },
            {
                "question": "Quels sont les avantages fiscaux pour les startups en Algérie ?",
                "category": "impôts_dgi"
            }
        ]
    }


@app.post("/api/dz-legal/answer", response_model=DZLegalAnswer)
async def dz_legal_answer(payload: DZLegalRequest):
    """
    Endpoint principal : répondre à une question juridique/administrative
    
    1. Interroge le RAG DZ pour récupérer des documents pertinents
    2. Construit un prompt spécialisé pour le LLM
    3. Génère une réponse structurée
    """
    logger.info(f"Question reçue: {payload.question[:100]}... | Catégorie: {payload.category}")
    
    # 1. Rechercher dans le RAG DZ
    rag_docs = await search_rag(payload.question, payload.category)
    logger.info(f"Documents RAG trouvés: {len(rag_docs)}")
    
    # 2. Construire les prompts
    user_prompt = build_user_prompt(
        question=payload.question,
        category=payload.category,
        user_context=payload.user_context,
        rag_docs=rag_docs
    )
    
    # 3. Appeler le LLM
    llm_raw = await call_llm(SYSTEM_PROMPT, user_prompt)
    
    # 4. Parser la réponse
    data = parse_llm_response(llm_raw)
    
    # 5. Ajouter les références RAG si manquantes
    if not data.get("references") and rag_docs:
        data["references"] = [
            {
                "label": doc.get("title", "Document")[:50],
                "source_name": doc.get("source", "RAG DZ"),
                "source_url": doc.get("url"),
                "date": doc.get("date")
            }
            for doc in rag_docs[:3]
        ]
    
    # 6. S'assurer du disclaimer
    if not data.get("disclaimer"):
        data["disclaimer"] = (
            "Cette réponse est fournie à titre informatif uniquement par DZ-LegalAssistant. "
            "Elle ne constitue pas un conseil juridique professionnel. "
            "Pour toute démarche officielle, veuillez consulter un avocat, un notaire ou "
            "les autorités compétentes (CNRC, DGI, CNAS, CASNOS, etc.)."
        )
    
    # 7. Valider et retourner
    try:
        answer = DZLegalAnswer(**data)
        logger.info(f"Réponse générée avec {len(answer.steps)} étapes")
        return answer
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail=f"INVALID_SCHEMA: {str(e)}")


# ============== FALLBACK (si pas de clé API) ==============

@app.post("/api/dz-legal/answer-demo")
async def dz_legal_answer_demo(payload: DZLegalRequest):
    """Version démo sans LLM - retourne une réponse pré-formatée"""
    
    demo_responses = {
        "droit_des_affaires": {
            "summary": f"Pour votre question sur '{payload.question[:50]}...', voici les informations générales sur les démarches en Algérie. La création d'entreprise nécessite plusieurs étapes auprès du CNRC, des impôts et de la sécurité sociale.",
            "category": "droit_des_affaires",
            "steps": [
                {
                    "title": "1. Rédaction des statuts",
                    "description": "Préparer les statuts de la société avec l'aide d'un notaire",
                    "checklist": ["Définir l'objet social", "Fixer le capital social", "Désigner le gérant", "Choisir le siège social"]
                },
                {
                    "title": "2. Dépôt au CNRC",
                    "description": "Déposer le dossier au Centre National du Registre de Commerce",
                    "checklist": ["Formulaire de demande", "Statuts notariés", "CNI du gérant", "Justificatif de domicile du siège"]
                },
                {
                    "title": "3. Obtention du NIF",
                    "description": "S'inscrire auprès de la Direction Générale des Impôts",
                    "checklist": ["Registre de commerce", "Statuts", "CNI", "Formulaire G8"]
                },
                {
                    "title": "4. Affiliation CNAS/CASNOS",
                    "description": "S'affilier à la sécurité sociale",
                    "checklist": ["Registre de commerce", "NIF", "CNI du gérant"]
                }
            ],
            "important_notes": [
                "Le capital minimum pour une EURL est de 100 000 DA",
                "Les délais varient de 1 à 4 semaines selon les wilayas",
                "Prévoir environ 30 000 à 50 000 DA de frais de création"
            ],
            "risks_and_limits": [
                "Les délais peuvent être plus longs en période de forte affluence",
                "Certaines activités nécessitent des agréments spécifiques",
                "Cette information est donnée à titre indicatif"
            ],
            "references": [
                {"label": "Code de commerce algérien", "source_name": "JORADP", "source_url": None, "date": None},
                {"label": "Site CNRC", "source_name": "CNRC", "source_url": "https://cnrc.dz", "date": None}
            ],
            "disclaimer": "Cette réponse est fournie à titre informatif uniquement. Elle ne constitue pas un conseil juridique professionnel. Veuillez consulter un avocat ou un notaire pour toute démarche officielle.",
            "followup_questions": [
                "Quel est le capital minimum requis ?",
                "Combien de temps prend la procédure ?",
                "Quels sont les frais de création ?",
                "Ai-je besoin d'un comptable dès le départ ?"
            ]
        }
    }
    
    # Retourner une réponse démo
    response = demo_responses.get(payload.category, demo_responses["droit_des_affaires"])
    response["summary"] = f"Pour votre question: '{payload.question[:80]}...'\n\n" + response["summary"]
    
    return DZLegalAnswer(**response)


# ============== MAIN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8197)
