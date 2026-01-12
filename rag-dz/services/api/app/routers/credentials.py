"""
Router pour la gestion des credentials des providers AI
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/credentials", tags=["Credentials"])


class CredentialBase(BaseModel):
    """Modèle de base pour un credential"""
    provider: str
    api_key: str
    is_encrypted: bool = False


class CredentialResponse(BaseModel):
    """Réponse pour un credential (clé masquée)"""
    id: str
    provider: str
    api_key_preview: str
    is_encrypted: bool
    has_key: bool
    created_at: str
    updated_at: str


class CredentialUpdate(BaseModel):
    """Modèle pour mettre à jour un credential"""
    api_key: str
    is_encrypted: bool = False


def mask_api_key(api_key: str) -> str:
    """Masque une clé API pour l'affichage"""
    if not api_key or len(api_key) == 0:
        return ""
    if len(api_key) <= 10:
        return "***" + api_key[-3:]
    return api_key[:10] + "..." + api_key[-4:]


@router.get("/", response_model=List[CredentialResponse])
async def list_credentials():
    """Liste tous les credentials configurés (avec clés masquées)"""
    try:
        from ..db import get_db_connection

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id::text,
                    provider,
                    api_key,
                    is_encrypted,
                    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS')
                FROM provider_credentials
                ORDER BY provider
            """)
            rows = cur.fetchall()

            credentials = []
            for row in rows:
                has_key = row[2] is not None and len(row[2]) > 0
                credentials.append({
                    "id": row[0],
                    "provider": row[1],
                    "api_key_preview": mask_api_key(row[2]) if has_key else "(empty)",
                    "is_encrypted": row[3] or False,
                    "has_key": has_key,
                    "created_at": row[4] or "",
                    "updated_at": row[5] or ""
                })

            return credentials

    except Exception as e:
        logger.warning(f"Database error, falling back to environment variables: {e}")

        # Fallback: Return credentials from environment variables
        import os
        from datetime import datetime

        env_credentials = []
        providers = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_GENERATIVE_AI_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY"),
            "mistral": os.getenv("MISTRAL_API_KEY"),
            "cohere": os.getenv("COHERE_API_KEY")
        }

        for provider, api_key in providers.items():
            has_key = api_key is not None and len(api_key) > 10 and not api_key.startswith("your-") and not api_key.startswith("sk-your")
            env_credentials.append({
                "id": provider,
                "provider": provider,
                "api_key_preview": mask_api_key(api_key) if has_key else "(not configured)",
                "is_encrypted": False,
                "has_key": has_key,
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        return env_credentials


@router.get("/{provider}", response_model=CredentialResponse)
async def get_credential(provider: str):
    """Récupère un credential spécifique (avec clé masquée)"""
    try:
        from ..db import get_db_connection

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id::text,
                    provider,
                    api_key,
                    is_encrypted,
                    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS')
                FROM provider_credentials
                WHERE provider = %s
            """, (provider,))
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail=f"Credential for {provider} not found")

            has_key = row[2] is not None and len(row[2]) > 0

            return {
                "id": row[0],
                "provider": row[1],
                "api_key_preview": mask_api_key(row[2]) if has_key else "(empty)",
                "is_encrypted": row[3] or False,
                "has_key": has_key,
                "created_at": row[4] or "",
                "updated_at": row[5] or ""
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting credential for {provider}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting credential: {str(e)}")


@router.post("/", response_model=CredentialResponse)
async def create_or_update_credential(credential: CredentialBase):
    """Crée ou met à jour un credential"""
    try:
        from ..db import get_db_connection

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO provider_credentials (provider, api_key, is_encrypted)
                VALUES (%s, %s, %s)
                ON CONFLICT (provider)
                DO UPDATE SET
                    api_key = EXCLUDED.api_key,
                    is_encrypted = EXCLUDED.is_encrypted,
                    updated_at = NOW()
                RETURNING
                    id::text,
                    provider,
                    api_key,
                    is_encrypted,
                    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS')
            """, (credential.provider, credential.api_key, credential.is_encrypted))

            row = cur.fetchone()
            has_key = row[2] is not None and len(row[2]) > 0

            return {
                "id": row[0],
                "provider": row[1],
                "api_key_preview": mask_api_key(row[2]) if has_key else "(empty)",
                "is_encrypted": row[3] or False,
                "has_key": has_key,
                "created_at": row[4] or "",
                "updated_at": row[5] or ""
            }

    except Exception as e:
        logger.error(f"Error creating/updating credential: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving credential: {str(e)}")


@router.put("/{provider}", response_model=CredentialResponse)
async def update_credential(provider: str, credential: CredentialUpdate):
    """Met à jour un credential existant"""
    try:
        from ..db import get_db_connection

        with get_db_connection() as conn, conn.cursor() as cur:
            # Vérifier que le credential existe
            cur.execute("SELECT id FROM provider_credentials WHERE provider = %s", (provider,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail=f"Credential for {provider} not found")

            # Mettre à jour
            cur.execute("""
                UPDATE provider_credentials
                SET
                    api_key = %s,
                    is_encrypted = %s,
                    updated_at = NOW()
                WHERE provider = %s
                RETURNING
                    id::text,
                    provider,
                    api_key,
                    is_encrypted,
                    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                    TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS')
            """, (credential.api_key, credential.is_encrypted, provider))

            row = cur.fetchone()
            has_key = row[2] is not None and len(row[2]) > 0

            return {
                "id": row[0],
                "provider": row[1],
                "api_key_preview": mask_api_key(row[2]) if has_key else "(empty)",
                "is_encrypted": row[3] or False,
                "has_key": has_key,
                "created_at": row[4] or "",
                "updated_at": row[5] or ""
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating credential: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating credential: {str(e)}")


@router.delete("/{provider}")
async def delete_credential(provider: str):
    """Supprime un credential (met la clé à vide)"""
    try:
        from ..db import get_db_connection

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                UPDATE provider_credentials
                SET api_key = '', updated_at = NOW()
                WHERE provider = %s
                RETURNING id
            """, (provider,))

            if not cur.fetchone():
                raise HTTPException(status_code=404, detail=f"Credential for {provider} not found")

            return {"message": f"Credential for {provider} cleared successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting credential: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting credential: {str(e)}")
