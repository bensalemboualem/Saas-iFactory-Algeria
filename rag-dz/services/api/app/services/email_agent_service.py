"""
Email Agent Service
6th Agent - Assistant Email for reading, summarizing, and drafting emails
"""

from typing import Optional, Dict, Any, List
import os
from pydantic import BaseModel

# LLM Provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


class EmailAssistRequest(BaseModel):
    draft: str
    context: Optional[str] = None
    action: str = "improve"  # improve, summarize, reply, formalize, translate


class EmailAnalysisRequest(BaseModel):
    content: str
    from_email: str
    subject: str
    task: str = "analyze_email_for_appointment"


class EmailAssistResponse(BaseModel):
    improved_text: Optional[str] = None
    summary: Optional[str] = None
    can_auto_reply: bool = False
    auto_reply_content: Optional[str] = None
    reason_no_auto_reply: Optional[str] = None
    detected_intent: Optional[str] = None
    extracted_info: Optional[Dict[str, Any]] = None


# Email Agent System Prompt
EMAIL_AGENT_SYSTEM_PROMPT = """Tu es un assistant email professionnel pour IA Factory.

CAPACITÉS:
- Lire et comprendre les emails
- Résumer les conversations email
- Rédiger des réponses professionnelles
- Améliorer le style et la clarté des emails
- Adapter le ton au contexte (médical, juridique, commercial)

RÈGLES:
1. Utilise un ton professionnel et courtois
2. Sois concis mais complet
3. Adapte le niveau de formalité au contexte
4. Respecte la confidentialité des informations
5. Pour le contexte médical: utilise un ton rassurant et empathique
6. Pour le contexte juridique: sois précis et factuel

FORMATS DE SORTIE:
- Pour amélioration: retourne le texte amélioré directement
- Pour résumé: bullet points des points clés
- Pour analyse: JSON structuré avec les informations extraites"""


async def call_llm(messages: List[Dict[str, str]], system_prompt: str = EMAIL_AGENT_SYSTEM_PROMPT) -> str:
    """Call LLM provider for email assistance"""
    import httpx

    if LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 2048,
                    "system": system_prompt,
                    "messages": messages,
                },
                timeout=60.0
            )
            if response.is_success:
                data = response.json()
                return data["content"][0]["text"]
            raise Exception(f"Anthropic API error: {response.text}")

    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "system", "content": system_prompt}] + messages,
                    "max_tokens": 2048,
                },
                timeout=60.0
            )
            if response.is_success:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            raise Exception(f"OpenAI API error: {response.text}")

    elif LLM_PROVIDER == "groq" and GROQ_API_KEY:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-70b-versatile",
                    "messages": [{"role": "system", "content": system_prompt}] + messages,
                    "max_tokens": 2048,
                },
                timeout=60.0
            )
            if response.is_success:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            raise Exception(f"Groq API error: {response.text}")

    raise Exception("No valid LLM provider configured")


async def improve_email(draft: str, context: Optional[str] = None) -> str:
    """Improve email draft"""
    prompt = f"""Améliore cet email en le rendant plus professionnel, clair et concis.
Garde le même sens mais améliore le style et la formulation.

{f'Contexte/Sujet: {context}' if context else ''}

Email à améliorer:
{draft}

Retourne uniquement l'email amélioré, sans explication."""

    messages = [{"role": "user", "content": prompt}]
    return await call_llm(messages)


async def summarize_email(content: str) -> str:
    """Summarize email content"""
    prompt = f"""Résume cet email en 3-5 points clés. Sois concis.

Email:
{content}

Format de sortie: bullet points (- point 1, - point 2, etc.)"""

    messages = [{"role": "user", "content": prompt}]
    return await call_llm(messages)


async def draft_reply(original_email: str, reply_intent: str) -> str:
    """Draft a reply to an email"""
    prompt = f"""Rédige une réponse professionnelle à cet email.

Email original:
{original_email}

Intention de la réponse: {reply_intent}

Rédige une réponse appropriée et professionnelle."""

    messages = [{"role": "user", "content": prompt}]
    return await call_llm(messages)


async def analyze_email_for_appointment(
    content: str,
    from_email: str,
    subject: str
) -> EmailAssistResponse:
    """Analyze email to detect appointment requests and auto-reply capability"""
    prompt = f"""Analyse cet email pour détecter s'il concerne une demande de rendez-vous.

De: {from_email}
Sujet: {subject}
Contenu:
{content}

Réponds en JSON avec:
{{
    "detected_intent": "appointment_request" | "appointment_change" | "appointment_cancel" | "question" | "other",
    "can_auto_reply": true | false,
    "reason_no_auto_reply": "raison si can_auto_reply est false",
    "auto_reply_content": "contenu de la réponse automatique si possible",
    "summary": "résumé court de l'email",
    "extracted_info": {{
        "requested_date": "date si mentionnée",
        "requested_time": "heure si mentionnée",
        "patient_name": "nom si mentionné",
        "phone": "téléphone si mentionné",
        "reason": "motif si mentionné"
    }}
}}

Règles pour auto-reply:
- Peut répondre auto si: simple confirmation de réception, demande d'info basique
- Ne peut PAS répondre auto si: demande de RDV spécifique, question médicale, urgence, plainte"""

    messages = [{"role": "user", "content": prompt}]
    response = await call_llm(messages)

    # Parse JSON response
    import json
    try:
        # Extract JSON from response (handle markdown code blocks)
        json_str = response
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0]

        data = json.loads(json_str.strip())

        return EmailAssistResponse(
            detected_intent=data.get("detected_intent"),
            can_auto_reply=data.get("can_auto_reply", False),
            reason_no_auto_reply=data.get("reason_no_auto_reply"),
            auto_reply_content=data.get("auto_reply_content"),
            summary=data.get("summary"),
            extracted_info=data.get("extracted_info"),
        )
    except json.JSONDecodeError:
        return EmailAssistResponse(
            detected_intent="unknown",
            can_auto_reply=False,
            reason_no_auto_reply="Impossible d'analyser l'email",
            summary=response[:200] if response else None,
        )


async def formalize_email(draft: str) -> str:
    """Make email more formal"""
    prompt = f"""Transforme cet email en version plus formelle et professionnelle.
Utilise un langage soutenu et des formules de politesse appropriées.

Email:
{draft}

Retourne uniquement l'email formalisé."""

    messages = [{"role": "user", "content": prompt}]
    return await call_llm(messages)


async def translate_email(content: str, target_language: str = "en") -> str:
    """Translate email to target language"""
    lang_names = {"en": "anglais", "fr": "français", "ar": "arabe", "es": "espagnol"}
    lang_name = lang_names.get(target_language, target_language)

    prompt = f"""Traduis cet email en {lang_name}. Garde le même ton et style.

Email:
{content}

Retourne uniquement la traduction."""

    messages = [{"role": "user", "content": prompt}]
    return await call_llm(messages)


# Agent definition for registration
EMAIL_AGENT_CONFIG = {
    "name": "Assistant Email",
    "icon": "Mail",
    "description": "Lire, résumer, et rédiger des emails professionnels",
    "system_prompt": EMAIL_AGENT_SYSTEM_PROMPT,
    "tools": ["read_email", "send_email", "search_emails", "improve_draft", "summarize"],
    "color": "#EA4335",  # Gmail red
}
