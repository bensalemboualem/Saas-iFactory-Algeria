"""
Geneva Multi-Cultural Repository
=================================

Database persistence pour Geneva Mode (110+ nationalités)
"""

import logging
import psycopg
from psycopg import sql
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def save_cultural_nuance(
    tenant_id: str,
    user_id: int,
    expression: str,
    language_code: str,
    nationality: str,
    cultural_meaning: str,
    literal_meaning: Optional[str] = None,
    politeness_level: Optional[str] = None,
    emotional_connotation: Optional[str] = None,
    confidence_score: float = 0.8
) -> str:
    """
    Sauvegarde une nuance culturelle détectée

    Args:
        tenant_id: UUID du tenant
        user_id: ID de l'utilisateur
        expression: Expression culturelle
        language_code: Code langue ('en', 'fr', 'ja', etc.)
        nationality: Nationalité ('japanese', 'spanish', 'algerian')
        cultural_meaning: Signification culturelle réelle
        literal_meaning: Sens littéral (optionnel)
        politeness_level: Niveau de politesse
        emotional_connotation: Connotation émotionnelle
        confidence_score: Score de confiance (0.0-1.0)

    Returns:
        UUID de la nuance créée
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(
                    sql.Literal(tenant_id) + sql.SQL("::uuid")
                )
                cur.execute(query)

                # Insérer nuance culturelle
                cur.execute("""
                    INSERT INTO cultural_nuances (
                        tenant_id, user_id, expression, language_code,
                        nationality, cultural_meaning, literal_meaning,
                        politeness_level, emotional_connotation,
                        business_appropriate, source, confidence_score
                    ) VALUES (
                        %s::uuid, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        true, 'ai_detected', %s
                    )
                    ON CONFLICT (expression, nationality, language_code) DO UPDATE SET
                        usage_frequency = cultural_nuances.usage_frequency + 1,
                        updated_at = NOW()
                    RETURNING id, usage_frequency
                """, (
                    tenant_id, user_id, expression, language_code,
                    nationality, cultural_meaning, literal_meaning,
                    politeness_level, emotional_connotation,
                    confidence_score
                ))

                nuance_id, frequency = cur.fetchone()
                conn.commit()

                logger.info(
                    f"🌍 Cultural nuance saved: {expression} ({nationality}) - frequency={frequency}"
                )

                return str(nuance_id)

    except Exception as e:
        logger.error(f"Erreur save_cultural_nuance: {e}")
        raise


def get_cultural_nuances_by_nationality(
    tenant_id: str,
    nationality: str,
    language_code: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Récupère les nuances culturelles d'une nationalité

    Args:
        tenant_id: UUID du tenant
        nationality: Nationalité à filtrer
        language_code: Code langue (optionnel)
        limit: Nombre maximum de résultats

    Returns:
        Liste de nuances culturelles
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(
                    sql.Literal(tenant_id) + sql.SQL("::uuid")
                )
                cur.execute(query)

                if language_code:
                    cur.execute("""
                        SELECT
                            expression, cultural_meaning, literal_meaning,
                            politeness_level, emotional_connotation,
                            usage_frequency, confidence_score
                        FROM cultural_nuances
                        WHERE nationality = %s AND language_code = %s
                        ORDER BY usage_frequency DESC
                        LIMIT %s
                    """, (nationality, language_code, limit))
                else:
                    cur.execute("""
                        SELECT
                            expression, cultural_meaning, literal_meaning,
                            politeness_level, emotional_connotation,
                            usage_frequency, confidence_score
                        FROM cultural_nuances
                        WHERE nationality = %s
                        ORDER BY usage_frequency DESC
                        LIMIT %s
                    """, (nationality, limit))

                rows = cur.fetchall()

                return [
                    {
                        "expression": row[0],
                        "cultural_meaning": row[1],
                        "literal_meaning": row[2],
                        "politeness_level": row[3],
                        "emotional_connotation": row[4],
                        "usage_frequency": row[5],
                        "confidence_score": row[6],
                    }
                    for row in rows
                ]

    except Exception as e:
        logger.error(f"Erreur get_cultural_nuances_by_nationality: {e}")
        return []


def save_multi_language_segments(
    tenant_id: str,
    transcription_id: str,
    language_segments: List[Dict[str, Any]]
) -> int:
    """
    Sauvegarde les segments multi-langues d'une transcription

    Args:
        tenant_id: UUID du tenant
        transcription_id: UUID de la transcription
        language_segments: Liste de segments avec langue détectée

    Returns:
        Nombre de segments sauvegardés
    """
    try:
        count = 0

        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(
                    sql.Literal(tenant_id) + sql.SQL("::uuid")
                )
                cur.execute(query)

                for segment in language_segments:
                    cur.execute("""
                        INSERT INTO multi_language_segments (
                            tenant_id, transcription_id,
                            segment_index, start_time, end_time,
                            detected_language, language_confidence,
                            text_content, accent_type, non_native_speaker
                        ) VALUES (
                            %s::uuid, %s::uuid,
                            %s, %s, %s,
                            %s, %s,
                            %s, %s, %s
                        )
                    """, (
                        tenant_id, transcription_id,
                        segment.get('segment_index'),
                        segment.get('start_time'),
                        segment.get('end_time'),
                        segment.get('detected_language'),
                        segment.get('language_confidence'),
                        segment.get('text_content'),
                        segment.get('accent_type'),
                        segment.get('non_native_speaker', False)
                    ))
                    count += 1

                conn.commit()

                logger.info(f"🌐 {count} language segments saved for transcription {transcription_id}")

                return count

    except Exception as e:
        logger.error(f"Erreur save_multi_language_segments: {e}")
        raise


def get_user_linguistic_profile(
    tenant_id: str,
    user_id: int
) -> Optional[Dict[str, Any]]:
    """
    Récupère le profil linguistique d'un utilisateur

    Args:
        tenant_id: UUID du tenant
        user_id: ID de l'utilisateur

    Returns:
        Profil linguistique ou None
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(
                    sql.Literal(tenant_id) + sql.SQL("::uuid")
                )
                cur.execute(query)

                cur.execute("""
                    SELECT
                        native_language, secondary_languages,
                        nationality, cultural_background,
                        geneva_mode_enabled, accent_sensitivity_level,
                        professional_context, typical_meeting_languages,
                        preferred_transcription_model, auto_detect_language
                    FROM user_linguistic_profile
                    WHERE user_id = %s
                """, (user_id,))

                row = cur.fetchone()

                if not row:
                    return None

                return {
                    "native_language": row[0],
                    "secondary_languages": row[1],
                    "nationality": row[2],
                    "cultural_background": row[3],
                    "geneva_mode_enabled": row[4],
                    "accent_sensitivity_level": row[5],
                    "professional_context": row[6],
                    "typical_meeting_languages": row[7],
                    "preferred_transcription_model": row[8],
                    "auto_detect_language": row[9],
                }

    except Exception as e:
        logger.error(f"Erreur get_user_linguistic_profile: {e}")
        return None


def create_or_update_user_linguistic_profile(
    tenant_id: str,
    user_id: int,
    native_language: str,
    nationality: str,
    secondary_languages: Optional[List[str]] = None,
    cultural_background: Optional[List[str]] = None,
    geneva_mode_enabled: bool = False,
    accent_sensitivity_level: int = 3,
    professional_context: Optional[str] = None
) -> str:
    """
    Crée ou met à jour le profil linguistique d'un utilisateur

    Args:
        tenant_id: UUID du tenant
        user_id: ID de l'utilisateur
        native_language: Langue maternelle ('fr', 'en', 'ar', etc.)
        nationality: Nationalité ('swiss', 'algerian', 'japanese', etc.)
        secondary_languages: Langues secondaires
        cultural_background: Contextes culturels
        geneva_mode_enabled: Activer Geneva Mode
        accent_sensitivity_level: Niveau sensibilité accent (1-5)
        professional_context: Contexte professionnel

    Returns:
        UUID du profil
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(
                    sql.Literal(tenant_id) + sql.SQL("::uuid")
                )
                cur.execute(query)

                cur.execute("""
                    INSERT INTO user_linguistic_profile (
                        tenant_id, user_id,
                        native_language, nationality,
                        secondary_languages, cultural_background,
                        geneva_mode_enabled, accent_sensitivity_level,
                        professional_context
                    ) VALUES (
                        %s::uuid, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s
                    )
                    ON CONFLICT (user_id) DO UPDATE SET
                        native_language = EXCLUDED.native_language,
                        nationality = EXCLUDED.nationality,
                        secondary_languages = EXCLUDED.secondary_languages,
                        cultural_background = EXCLUDED.cultural_background,
                        geneva_mode_enabled = EXCLUDED.geneva_mode_enabled,
                        accent_sensitivity_level = EXCLUDED.accent_sensitivity_level,
                        professional_context = EXCLUDED.professional_context,
                        updated_at = NOW()
                    RETURNING id
                """, (
                    tenant_id, user_id,
                    native_language, nationality,
                    secondary_languages, cultural_background,
                    geneva_mode_enabled, accent_sensitivity_level,
                    professional_context
                ))

                profile_id = cur.fetchone()[0]
                conn.commit()

                logger.info(f"👤 Linguistic profile saved: user={user_id}, nationality={nationality}")

                return str(profile_id)

    except Exception as e:
        logger.error(f"Erreur create_or_update_user_linguistic_profile: {e}")
        raise
