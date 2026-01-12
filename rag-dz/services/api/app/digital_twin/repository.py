"""
Repository pour Digital Twin (Agent Double)
Gestion du lexique personnalisé et analyses émotionnelles
"""

import logging
import psycopg
from psycopg import sql
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def save_emotion_analysis(
    tenant_id: str,
    user_id: int,
    transcription_id: str,
    emotion_data: Dict[str, Any],
    analysis_model: str = "rule-based-v1"
) -> str:
    """
    Sauvegarde une analyse émotionnelle

    Args:
        tenant_id: UUID du tenant
        user_id: ID de l'utilisateur
        transcription_id: UUID de la transcription
        emotion_data: Résultat de analyze_intent_and_emotion()
        analysis_model: Nom du modèle d'analyse

    Returns:
        UUID de l'analyse créée
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                # Insérer analyse émotionnelle
                cur.execute("""
                    INSERT INTO emotion_analysis_logs (
                        tenant_id, user_id, transcription_id,
                        detected_emotion, stress_level, cognitive_load,
                        heritage_detected, heritage_type, heritage_content,
                        recommended_summary_style, ai_confidence,
                        analysis_model, metadata
                    ) VALUES (
                        %s::uuid, %s, %s::uuid,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s::jsonb
                    )
                    RETURNING id
                """, (
                    tenant_id, user_id, transcription_id,
                    emotion_data.get('detected_emotion'),
                    emotion_data.get('stress_level'),
                    emotion_data.get('cognitive_load'),
                    emotion_data.get('heritage_detected', False),
                    emotion_data.get('heritage_type'),
                    emotion_data.get('heritage_content'),
                    emotion_data.get('recommended_summary_style'),
                    emotion_data.get('ai_confidence'),
                    analysis_model,
                    psycopg.adapters.types.json.Json({
                        'keywords': emotion_data.get('keywords_extracted', []),
                        'professional_terms': emotion_data.get('professional_terms', [])
                    })
                ))

                analysis_id = cur.fetchone()[0]
                conn.commit()

                logger.info(
                    f"Emotion analysis saved: id={analysis_id}, "
                    f"emotion={emotion_data.get('detected_emotion')}, "
                    f"stress={emotion_data.get('stress_level')}"
                )

                return str(analysis_id)

    except Exception as e:
        logger.error(f"Erreur sauvegarde emotion analysis: {e}")
        raise


def add_to_user_lexicon(
    tenant_id: str,
    user_id: int,
    term: str,
    professional_domain: Optional[str] = None,
    term_type: Optional[str] = None,
    definition: Optional[str] = None,
    emotional_tag: Optional[str] = None,
    cultural_context: Optional[str] = None,
    transcription_id: Optional[str] = None,
    confidence_score: float = 0.8
) -> str:
    """
    Ajoute un terme au lexique personnel de l'utilisateur
    Si le terme existe déjà, incrémente sa fréquence

    Args:
        tenant_id: UUID du tenant
        user_id: ID de l'utilisateur
        term: Mot ou expression à ajouter
        professional_domain: 'medical', 'legal', 'accounting', etc.
        term_type: 'abbreviation', 'medical_term', 'legal_jargon', etc.
        definition: Définition du terme
        emotional_tag: 'stress_indicator', 'calm', 'heritage_value', etc.
        cultural_context: 'algerian_heritage', 'swiss_formal', 'universal'
        transcription_id: UUID de la transcription source
        confidence_score: Score de confiance (0.0-1.0)

    Returns:
        UUID du terme (nouveau ou existant)
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                # Upsert: insérer ou incrémenter fréquence
                cur.execute("""
                    INSERT INTO user_preferences_lexicon (
                        tenant_id, user_id, term,
                        term_type, professional_domain, definition,
                        emotional_tag, cultural_context,
                        source_transcription_id, confidence_score,
                        frequency_count, last_used_at, first_detected_at
                    ) VALUES (
                        %s::uuid, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s::uuid, %s,
                        1, NOW(), NOW()
                    )
                    ON CONFLICT (user_id, term) DO UPDATE SET
                        frequency_count = user_preferences_lexicon.frequency_count + 1,
                        last_used_at = NOW(),
                        updated_at = NOW()
                    RETURNING id, frequency_count
                """, (
                    tenant_id, user_id, term.lower(),
                    term_type, professional_domain, definition,
                    emotional_tag, cultural_context,
                    transcription_id, confidence_score
                ))

                term_id, frequency = cur.fetchone()
                conn.commit()

                logger.info(f"Lexicon term saved: {term} (frequency={frequency})")

                return str(term_id)

    except Exception as e:
        logger.error(f"Erreur ajout lexicon: {e}")
        raise


def bulk_add_to_user_lexicon(
    tenant_id: str,
    user_id: int,
    terms: List[str],
    professional_domain: Optional[str] = None,
    transcription_id: Optional[str] = None
) -> int:
    """
    Ajoute plusieurs termes en bulk au lexique utilisateur

    Returns:
        Nombre de termes ajoutés/mis à jour
    """
    count = 0

    for term in terms:
        if len(term) >= 3:  # Filtrer les termes trop courts
            try:
                add_to_user_lexicon(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    term=term,
                    professional_domain=professional_domain,
                    transcription_id=transcription_id
                )
                count += 1
            except Exception as e:
                logger.warning(f"Impossible d'ajouter terme '{term}': {e}")
                continue

    logger.info(f"Bulk lexicon update: {count} terms added for user {user_id}")
    return count


def track_tokens_saved(
    tenant_id: str,
    user_id: int,
    transcription_id: str,
    audio_duration_seconds: float,
    audio_format: str,
    local_model: str = "faster-whisper-large-v3",
    cloud_provider_compared: str = "openai_whisper",
    transcription_quality_score: Optional[float] = None,
    processing_time_ms: Optional[int] = None
) -> str:
    """
    Track le ROI: tokens économisés en utilisant Faster-Whisper local
    au lieu des APIs Cloud

    Calcul simplifié:
    - OpenAI Whisper API: ~$0.006/minute → ~60 tokens/minute équivalent
    - Faster-Whisper local: GRATUIT → 0 tokens

    Returns:
        UUID du tracking créé
    """
    try:
        # Calcul coût équivalent Cloud
        duration_minutes = audio_duration_seconds / 60.0

        # OpenAI Whisper: $0.006/min → convertir en "tokens équivalents"
        # Approximation: 1 minute audio = 60 tokens équivalents
        cloud_equivalent_tokens = int(duration_minutes * 60)

        local_cost = 0  # Local = GRATUIT

        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                # Insérer tracking ROI
                cur.execute("""
                    INSERT INTO tokens_saved_tracking (
                        tenant_id, user_id, transcription_id,
                        audio_duration_seconds, audio_format,
                        local_cost_tokens, cloud_equivalent_cost_tokens,
                        local_model, cloud_provider_compared,
                        transcription_quality_score, processing_time_ms
                    ) VALUES (
                        %s::uuid, %s, %s::uuid,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s
                    )
                    RETURNING id, tokens_saved
                """, (
                    tenant_id, user_id, transcription_id,
                    audio_duration_seconds, audio_format,
                    local_cost, cloud_equivalent_tokens,
                    local_model, cloud_provider_compared,
                    transcription_quality_score, processing_time_ms
                ))

                tracking_id, tokens_saved = cur.fetchone()
                conn.commit()

                logger.info(
                    f"ROI tracked: {tokens_saved} tokens saved vs {cloud_provider_compared} "
                    f"({duration_minutes:.1f} min audio)"
                )

                return str(tracking_id)

    except Exception as e:
        logger.error(f"Erreur tracking tokens saved: {e}")
        raise


def get_user_lexicon(
    tenant_id: str,
    user_id: int,
    professional_domain: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Récupère le lexique personnel d'un utilisateur
    Trié par fréquence décroissante

    Returns:
        Liste de termes avec métadonnées
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                # Query avec filtre optionnel par domaine
                if professional_domain:
                    cur.execute("""
                        SELECT
                            term, term_type, professional_domain,
                            frequency_count, last_used_at, first_detected_at,
                            definition, emotional_tag, cultural_context,
                            confidence_score
                        FROM user_preferences_lexicon
                        WHERE user_id = %s AND professional_domain = %s
                        ORDER BY frequency_count DESC
                        LIMIT %s
                    """, (user_id, professional_domain, limit))
                else:
                    cur.execute("""
                        SELECT
                            term, term_type, professional_domain,
                            frequency_count, last_used_at, first_detected_at,
                            definition, emotional_tag, cultural_context,
                            confidence_score
                        FROM user_preferences_lexicon
                        WHERE user_id = %s
                        ORDER BY frequency_count DESC
                        LIMIT %s
                    """, (user_id, limit))

                rows = cur.fetchall()

                return [
                    {
                        "term": row[0],
                        "term_type": row[1],
                        "professional_domain": row[2],
                        "frequency_count": row[3],
                        "last_used_at": row[4].isoformat() if row[4] else None,
                        "first_detected_at": row[5].isoformat() if row[5] else None,
                        "definition": row[6],
                        "emotional_tag": row[7],
                        "cultural_context": row[8],
                        "confidence_score": row[9]
                    }
                    for row in rows
                ]

    except Exception as e:
        logger.error(f"Erreur get lexicon: {e}")
        return []


def get_total_tokens_saved_stats(
    tenant_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Calcule les statistiques ROI totales pour un tenant

    Returns:
        Dict avec total_saved, total_transcriptions, total_hours
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Set RLS context
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                # Utiliser la fonction PostgreSQL
                if start_date:
                    cur.execute(
                        "SELECT * FROM get_total_tokens_saved(%s::uuid, %s, %s)",
                        (tenant_id, start_date, end_date or datetime.now())
                    )
                else:
                    cur.execute(
                        "SELECT * FROM get_total_tokens_saved(%s::uuid)",
                        (tenant_id,)
                    )

                row = cur.fetchone()

                if row:
                    return {
                        "total_tokens_saved": row[0],
                        "total_transcriptions": row[1],
                        "total_hours_transcribed": round(row[2], 2)
                    }
                else:
                    return {
                        "total_tokens_saved": 0,
                        "total_transcriptions": 0,
                        "total_hours_transcribed": 0.0
                    }

    except Exception as e:
        logger.error(f"Erreur stats tokens saved: {e}")
        return {
            "total_tokens_saved": 0,
            "total_transcriptions": 0,
            "total_hours_transcribed": 0.0
        }
