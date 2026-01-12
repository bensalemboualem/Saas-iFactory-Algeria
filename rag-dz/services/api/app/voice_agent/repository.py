"""
Repository pour les transcriptions vocales avec isolation multi-tenant
"""
import logging
import json
import psycopg
from typing import Dict, Any, Optional
from uuid import UUID
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def save_transcription(
    tenant_id: str,
    filename: str,
    text_raw: str,
    duration_seconds: float,
    language: str,
    language_confidence: float,
    user_id: Optional[int] = None,
    file_size_bytes: Optional[int] = None,
    audio_format: Optional[str] = None,
    used_model: Optional[str] = None,
    processing_time_ms: Optional[int] = None,
    keywords: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Sauvegarde une transcription en DB avec isolation tenant

    Args:
        tenant_id: UUID du tenant (isolation multi-tenant)
        filename: Nom du fichier audio
        text_raw: Texte brut transcrit
        duration_seconds: Durée audio en secondes
        language: Code langue (fr, en, ar)
        language_confidence: Confiance de détection (0.0-1.0)
        user_id: ID utilisateur (optionnel)
        file_size_bytes: Taille fichier en octets
        audio_format: Format audio (mp4, m4a, wav, etc.)
        used_model: Modèle Whisper utilisé (base, large-v3, etc.)
        processing_time_ms: Temps de traitement en millisecondes
        keywords: Mots-clés générés par IA (3 mots séparés par virgule)
        metadata: Métadonnées JSON additionnelles

    Returns:
        UUID de la transcription créée (str)

    Raises:
        Exception si l'insertion échoue (ex: violation RLS)
    """
    try:
        # Préparer métadonnées
        meta = metadata or {}
        if keywords:
            meta["keywords"] = keywords

        # Connection PostgreSQL
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Définir le tenant pour RLS
                cur.execute("SELECT set_tenant(%s)", (tenant_id,))

                # SQL INSERT avec RETURNING id
                cur.execute("""
                    INSERT INTO voice_transcriptions (
                        tenant_id,
                        user_id,
                        filename,
                        file_size_bytes,
                        duration_seconds,
                        audio_format,
                        text_raw,
                        language,
                        language_confidence,
                        used_model,
                        processing_time_ms,
                        status,
                        metadata
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id
                """, (
                    tenant_id,
                    user_id,
                    filename,
                    file_size_bytes,
                    duration_seconds,
                    audio_format,
                    text_raw,
                    language,
                    language_confidence,
                    used_model,
                    processing_time_ms,
                    'completed',
                    json.dumps(meta),
                ))

                transcription_id = cur.fetchone()[0]
                conn.commit()

                logger.info(
                    f"✅ Transcription saved: {transcription_id} (tenant={tenant_id}, file={filename})"
                )

                return str(transcription_id)

    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde transcription: {e}")
        raise


def get_transcription(transcription_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """
    Récupère une transcription par ID (filtré par RLS tenant)

    Args:
        transcription_id: UUID de la transcription
        tenant_id: UUID du tenant (pour RLS)

    Returns:
        Dict avec les données ou None si introuvable/autre tenant
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Définir le tenant pour RLS
                cur.execute("SELECT set_tenant(%s)", (tenant_id,))

                cur.execute("""
                    SELECT
                        id, tenant_id, filename, text_raw,
                        duration_seconds, language, language_confidence,
                        used_model, metadata, created_at
                    FROM voice_transcriptions
                    WHERE id = %s
                """, (transcription_id,))

                row = cur.fetchone()

                if not row:
                    return None

                return {
                    "id": str(row[0]),
                    "tenant_id": str(row[1]),
                    "filename": row[2],
                    "text_raw": row[3],
                    "duration_seconds": row[4],
                    "language": row[5],
                    "language_confidence": row[6],
                    "used_model": row[7],
                    "metadata": row[8],
                    "created_at": row[9],
                }

    except Exception as e:
        logger.error(f"Erreur récupération transcription: {e}")
        return None


def list_transcriptions(
    tenant_id: str,
    limit: int = 10,
    offset: int = 0
) -> list[Dict[str, Any]]:
    """
    Liste les transcriptions du tenant courant (filtré par RLS)

    Args:
        tenant_id: UUID du tenant (pour RLS)
        limit: Nombre max de résultats
        offset: Offset pour pagination

    Returns:
        Liste de transcriptions du tenant
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Définir le tenant pour RLS
                cur.execute("SELECT set_tenant(%s)", (tenant_id,))

                cur.execute("""
                    SELECT
                        id, tenant_id, filename, text_raw,
                        duration_seconds, language, metadata, created_at
                    FROM voice_transcriptions
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                rows = cur.fetchall()

                return [
                    {
                        "id": str(row[0]),
                        "tenant_id": str(row[1]),
                        "filename": row[2],
                        "text_raw": row[3],
                        "duration_seconds": row[4],
                        "language": row[5],
                        "metadata": row[6],
                        "created_at": row[7],
                    }
                    for row in rows
                ]

    except Exception as e:
        logger.error(f"Erreur liste transcriptions: {e}")
        return []
