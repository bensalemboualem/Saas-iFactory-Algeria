"""
Help Chatbot Router - Dzir IA Assistant
Provides secure chat endpoint for the landing page help chatbot
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import Optional

router = APIRouter(prefix="/api/help-chat", tags=["help-chat"])


class ChatMessage(BaseModel):
    message: str
    mode: Optional[str] = "chat"  # chat, rag, support
    rag_context: Optional[str] = None  # DZ, CH, GLOBAL, ALL


class ChatResponse(BaseModel):
    response: str
    mode: str


@router.post("/send", response_model=ChatResponse)
async def send_help_message(chat: ChatMessage):
    """
    Send a message to Dzir IA chatbot assistant

    - **message**: User's message
    - **mode**: Chat mode (chat, rag, support)
    - **rag_context**: RAG context if mode is "rag"
    """

    if not chat.message or len(chat.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if len(chat.message) > 2000:
        raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")

    try:
        # Use Groq API with secure backend key
        groq_api_key = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")

        if not groq_api_key:
            raise HTTPException(status_code=500, detail="API key not configured")

        # Customize system prompt based on mode
        if chat.mode == "rag":
            system_prompt = f"""Tu es Dzir IA, l'assistant intelligent de IAFactory Algeria.
Tu es en mode Recherche RAG avec le contexte: {chat.rag_context or 'ALL'}.
Tu aides les utilisateurs à trouver des informations dans notre base de connaissances.
Réponds de manière concise, précise et factuelle.
Tu comprends et réponds en français, anglais, arabe standard, darija algérienne et amazigh.
Réponds dans la même langue que l'utilisateur."""

        elif chat.mode == "support":
            system_prompt = """Tu es Dzir IA en mode Support.
Tu redirigeras vers un agent humain si nécessaire, mais d'abord essaie d'aider l'utilisateur avec les problèmes techniques courants.
Sois patient, empathique et professionnel.
Tu comprends et réponds en français, anglais, arabe standard, darija algérienne et amazigh.
Réponds dans la même langue que l'utilisateur."""

        else:  # chat mode
            system_prompt = """Tu es Dzir IA, l'assistant intelligent de IAFactory Algeria.
Tu aides les utilisateurs à découvrir les applications et services de la plateforme.
IAFactory Algeria propose:
- 30+ applications IA pour le marché algérien (Business DZ, Med DZ, Agri DZ, Commerce DZ, Prof DZ, Legal Assistant, etc.)
- Support multilingue (français, arabe, darija, amazigh, anglais)
- 15+ providers d'IA (OpenAI, Claude, Gemini, Groq, GLM-4, Mistral, etc.)
- Modèles gratuits (Ollama, LM Studio, SillyTavern GPT)
- Agents IA spécialisés et workflows automatisés

Réponds de manière concise, amicale et professionnelle.
Tu comprends et réponds en français, anglais, arabe standard, darija algérienne et amazigh.
Réponds dans la même langue que l'utilisateur."""

        # Call Groq API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {groq_api_key}"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat.message}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )

            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Groq API error: {error_detail}"
                )

            data = response.json()
            bot_response = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not bot_response:
                bot_response = "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer."

            return ChatResponse(response=bot_response, mode=chat.mode)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout - please try again")

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "help-chat"}
