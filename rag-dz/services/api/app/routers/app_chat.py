"""
App Chat Router - Secure backend for all IAFactory Algeria apps
Provides secure chat endpoints for: Business DZ, Med DZ, Agri DZ, Commerce DZ, Prof DZ, Legal Assistant
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import Optional

router = APIRouter(prefix="/api/app-chat", tags=["app-chat"])


class AppChatMessage(BaseModel):
    app_name: str  # business-dz, med-dz, agri-dz, commerce-dz, prof-dz, legal-assistant
    message: str
    conversation_history: Optional[list] = []


class AppChatResponse(BaseModel):
    response: str
    app_name: str


# App-specific system prompts
APP_PROMPTS = {
    "business-dz": """Tu es l'assistant intelligent de Business DZ, une application IAFactory Algeria dédiée aux entreprises algériennes.
Tu aides les entrepreneurs et les PME algériennes avec:
- Gestion d'entreprise et comptabilité
- Conseils business et stratégie
- Conformité réglementaire algérienne
- Marketing et croissance

Réponds de manière professionnelle, concise et pratique.
Tu comprends et réponds en français, arabe, darija algérienne et anglais.""",

    "med-dz": """Tu es l'assistant médical intelligent de Med DZ, une application IAFactory Algeria pour le secteur de la santé algérien.
Tu aides avec:
- Informations médicales générales
- Gestion de dossiers patients
- Rappels de rendez-vous
- Conseils santé généraux (JAMAIS de diagnostic médical)

IMPORTANT: Tu ne poses JAMAIS de diagnostic. Tu recommandes toujours de consulter un médecin pour les problèmes de santé.
Réponds de manière professionnelle, empathique et claire.
Tu comprends et réponds en français, arabe, darija algérienne et anglais.""",

    "agri-dz": """Tu es l'assistant agricole intelligent d'Agri DZ, une application IAFactory Algeria pour l'agriculture algérienne.
Tu aides les agriculteurs algériens avec:
- Conseils sur les cultures adaptées au climat algérien
- Gestion des exploitations agricoles
- Techniques d'irrigation et optimisation de l'eau
- Prévention des maladies des plantes

Réponds de manière pratique, accessible et adaptée au contexte algérien.
Tu comprends et réponds en français, arabe, darija algérienne et anglais.""",

    "commerce-dz": """Tu es l'assistant e-commerce intelligent de Commerce DZ, une application IAFactory Algeria pour le commerce électronique algérien.
Tu aides les commerçants avec:
- Création et gestion de boutique en ligne
- Stratégies de vente en ligne
- Marketing digital et réseaux sociaux
- Gestion des stocks et commandes

Réponds de manière pratique, orientée résultats et adaptée au marché algérien.
Tu comprends et réponds en français, arabe, darija algérienne et anglais.""",

    "prof-dz": """Tu es l'assistant éducatif intelligent de Prof DZ, une application IAFactory Algeria pour les enseignants et établissements scolaires algériens.
Tu aides avec:
- Préparation de cours et supports pédagogiques
- Gestion de classe et suivi des élèves
- Conformité au programme algérien
- Conseils pédagogiques

Réponds de manière pédagogique, claire et adaptée au système éducatif algérien.
Tu comprends et réponds en français, arabe, darija algérienne et anglais.""",

    "legal-assistant": """Tu es l'assistant juridique intelligent Legal Assistant, une application IAFactory Algeria pour le droit algérien.
Tu aides avec:
- Information sur le droit algérien (Code civil, Code de commerce, etc.)
- Rédaction de documents juridiques
- Conseils juridiques généraux
- Procédures administratives algériennes

IMPORTANT: Tu fournis des informations juridiques générales, PAS de conseils juridiques personnalisés. Tu recommandes toujours de consulter un avocat pour des cas spécifiques.
Réponds de manière précise, factuelle et conforme au droit algérien.
Tu comprends et réponds en français, arabe et anglais."""
}


@router.post("/send", response_model=AppChatResponse)
async def send_app_message(chat: AppChatMessage):
    """
    Send a message to an IAFactory Algeria app chatbot

    - **app_name**: App identifier (business-dz, med-dz, agri-dz, commerce-dz, prof-dz, legal-assistant)
    - **message**: User's message
    - **conversation_history**: Optional conversation history
    """

    # Validation
    if not chat.message or len(chat.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if len(chat.message) > 5000:
        raise HTTPException(status_code=400, detail="Message too long (max 5000 characters)")

    if chat.app_name not in APP_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Invalid app_name. Must be one of: {', '.join(APP_PROMPTS.keys())}")

    try:
        # Use Groq API with secure backend key
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            # Fallback to hardcoded key (should be in .env in production)
            groq_api_key = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")

        if not groq_api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        # Get app-specific system prompt
        system_prompt = APP_PROMPTS[chat.app_name]

        # Build messages for Groq
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history if provided
        if chat.conversation_history:
            messages.extend(chat.conversation_history[-10:])  # Last 10 messages only

        # Add current user message
        messages.append({"role": "user", "content": chat.message})

        # Call Groq API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",  # Fast and powerful
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "top_p": 1,
                    "stream": False
                }
            )

            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Groq API error: {error_detail}"
                )

            data = response.json()
            ai_response = data["choices"][0]["message"]["content"]

            return AppChatResponse(
                response=ai_response,
                app_name=chat.app_name
            )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout - AI service took too long to respond")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error calling AI service: {str(e)}")
    except KeyError as e:
        raise HTTPException(status_code=502, detail=f"Unexpected response format from AI service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for app chat service"""
    groq_api_key = os.getenv("GROQ_API_KEY")
    return {
        "status": "healthy",
        "service": "IAFactory Algeria App Chat",
        "apps_supported": list(APP_PROMPTS.keys()),
        "api_key_configured": bool(groq_api_key)
    }
