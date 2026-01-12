"""
IAFactory RAG Module - Phase 2
Répond avec structure 4 blocs + LLM Groq
Token tracking integre.
"""
from pathlib import Path
from typing import Literal, Optional
import os
import logging
from groq import Groq

# Token tracking
try:
    from app.tokens.llm_proxy import check_token_balance, deduct_after_llm_call, InsufficientTokensError
    TOKENS_AVAILABLE = True
except ImportError:
    TOKENS_AVAILABLE = False

logger = logging.getLogger(__name__)

Region = Literal["DZ", "CH"]

DOCS_PATH = Path(__file__).parent.parent.parent.parent / "documents"

CONTACTS = {
    "DZ": "contact@iafactory.dz | WhatsApp: +213660388800",
    "CH": "contact@iafactory.ch | Tel: +41789714705"
}

PROMPT_TEMPLATE = """Tu es l'assistant commercial IAFactory pour la région {region}.

Contexte des documents IAFactory :
{context}

Question : {question}

RÈGLES STRICTES :
1. Réponds UNIQUEMENT avec ces 4 sections :

💡 RÉPONSE DIRECTE
[2-3 phrases avec données précises des documents]

📊 DÉTAILS CLÉS
- [Point 1 avec chiffre tiré des docs]
- [Point 2 avec métrique des docs]
- [Point 3 technique ou business]

🚀 AVANTAGE IAFACTORY
[1 paragraphe : avantages avec métriques réelles des documents]

🎯 ACTION
Contact : {contact}
Prochaine étape : [Action concrète : démo/devis/essai]

2. Utilise SEULEMENT les infos des documents fournis
3. Si prix demandé : extrais de Pricing_{region}.md
4. Langue de réponse = langue de la question
5. Pas d'invention, que des faits documentés
"""

def load_docs(region: Region) -> str:
    """Charge les docs IAFactory pour la région"""
    docs = []
    for f in DOCS_PATH.glob("*.md"):
        if region in f.name or any(x in f.name for x in ["Products", "Team", "Company"]):
            try:
                docs.append(f.read_text(encoding="utf-8"))
            except:
                pass
    return "\n\n".join(docs)[:8000]

def answer(question: str, region: Region, tenant_id: Optional[str] = None) -> dict:
    """Répond avec structure 4 blocs avec token tracking"""
    context = load_docs(region)
    contact = CONTACTS[region]

    prompt = PROMPT_TEMPLATE.format(
        region=region,
        context=context,
        question=question,
        contact=contact
    )

    system_prompt = "Tu es l'assistant commercial IAFactory. Tu réponds toujours avec la structure 4 blocs demandée."

    # Token tracking: verifier solde AVANT l'appel
    if TOKENS_AVAILABLE and tenant_id:
        estimated_tokens = len((system_prompt + prompt).split()) * 2 + 500
        try:
            check_token_balance(tenant_id, estimated_tokens)
        except InsufficientTokensError:
            raise

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )

    answer_text = response.choices[0].message.content

    # Token tracking: deduire tokens APRES l'appel
    if TOKENS_AVAILABLE and tenant_id and response.usage:
        try:
            deduct_after_llm_call(
                tenant_id=tenant_id,
                provider="groq",
                model="llama-3.3-70b-versatile",
                tokens_input=response.usage.prompt_tokens,
                tokens_output=response.usage.completion_tokens
            )
        except Exception as e:
            logger.warning(f"Token deduction failed (iafactory_rag): {e}")

    return {
        "answer": answer_text,
        "sources": [f.name for f in DOCS_PATH.glob("*.md")],
        "region": region
    }
