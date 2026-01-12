from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, anthropic, openai

router = APIRouter(prefix="/api/prompt-creator", tags=["prompt-creator"])

class PromptRequest(BaseModel):
    input: str

class PromptResponse(BaseModel):
    prompt: str

@router.post("/generate", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    system_prompt = f"""Tu es un expert en prompt engineering. Transforme l'idée de l'utilisateur en prompt professionnel optimisé.

IDÉE UTILISATEUR: {request.input}

Crée un prompt structuré avec:
- CONTEXTE clair
- TÂCHE précise
- CONTRAINTES définies
- INSTRUCTIONS étape par étape
- RÉSULTAT ATTENDU
- EXEMPLES si pertinent

Le prompt doit être prêt à utiliser avec Claude ou GPT."""

    try:
        if anthropic_key:
            client = anthropic.Anthropic(api_key=anthropic_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": system_prompt}]
            )
            return PromptResponse(prompt=message.content[0].text)
        elif openai_key:
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": system_prompt}],
                max_tokens=2000
            )
            return PromptResponse(prompt=response.choices[0].message.content)
    except:
        pass
    
    return PromptResponse(prompt=f"""PROMPT PROFESSIONNEL

CONTEXTE:
{request.input}

TÂCHE:
[Définir la tâche principale basée sur le contexte]

CONTRAINTES:
- Langue: Français
- Ton: Professionnel
- Format: Structuré

INSTRUCTIONS:
1. Analyser le contexte
2. Identifier les besoins
3. Fournir une réponse complète

RÉSULTAT ATTENDU:
[Format de sortie souhaité]""")

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "prompt-creator"}
