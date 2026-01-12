"""
Repository pour la gestion des tokens (Carburant)
Isolation stricte multi-tenant avec RLS
"""
import logging
import json
import psycopg
from psycopg import sql
import uuid
from typing import Dict, Any, Optional
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def get_balance(tenant_id: str) -> Dict[str, Any]:
    """
    Récupère le solde tokens d'un tenant

    Args:
        tenant_id: UUID du tenant

    Returns:
        Dict avec balance_tokens, total_purchased, total_consumed
    """
    try:
        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                # Utiliser sql.SQL pour éviter les problèmes de prepared statement
                query = sql.SQL("SELECT set_tenant({})").format(sql.Literal(tenant_id) + sql.SQL("::uuid"))
                cur.execute(query)

                cur.execute("""
                    SELECT
                        balance_tokens, total_purchased, total_consumed,
                        last_purchase_at, last_usage_at
                    FROM tenant_token_balances
                    WHERE tenant_id = %s::uuid
                """, (tenant_id,))

                row = cur.fetchone()

                if not row:
                    # Créer solde à 0 si inexistant
                    cur.execute("""
                        INSERT INTO tenant_token_balances (tenant_id, balance_tokens)
                        VALUES (%s, 0)
                        RETURNING balance_tokens, total_purchased, total_consumed,
                                  last_purchase_at, last_usage_at
                    """, (tenant_id,))
                    row = cur.fetchone()
                    conn.commit()

                # Debug: check types
                logger.info(f"DEBUG row[3] type: {type(row[3])}, value: {row[3]}")
                logger.info(f"DEBUG row[4] type: {type(row[4])}, value: {row[4]}")

                result = {
                    "balance_tokens": row[0],
                    "total_purchased": row[1],
                    "total_consumed": row[2],
                    "last_purchase_at": row[3].isoformat() if row[3] else None,
                    "last_usage_at": row[4].isoformat() if row[4] else None,
                }

                logger.info(f"DEBUG result last_purchase_at type: {type(result['last_purchase_at'])}")
                return result

    except Exception as e:
        logger.error(f"Erreur récupération balance: {e}")
        return {
            "balance_tokens": 0,
            "total_purchased": 0,
            "total_consumed": 0,
            "last_purchase_at": None,
            "last_usage_at": None,
        }


def redeem_code(code: str, tenant_id: str) -> Dict[str, Any]:
    """
    Échanger un code licence contre des tokens

    Args:
        code: Code de recharge (ex: IAFACTORY-WELCOME-1000)
        tenant_id: UUID du tenant

    Returns:
        Dict avec success, tokens_credited, new_balance, error
    """
    try:
        tenant_uuid = uuid.UUID(tenant_id)  # Convertir string → UUID Python

        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT set_tenant(%s)", (tenant_uuid,))

                # Appeler fonction PostgreSQL
                cur.execute(
                    "SELECT redeem_licence_code(%s, %s)",
                    (code, tenant_uuid)
                )

                result = cur.fetchone()[0]
                conn.commit()

                logger.info(
                    f"Code redeem: {code} for tenant {tenant_id} - "
                    f"Result: {result.get('success')}"
                )

                return result

    except Exception as e:
        logger.error(f"Erreur redeem code: {e}")
        return {
            "success": False,
            "error": f"Erreur technique: {str(e)}"
        }


def deduct_tokens_for_llm(
    tenant_id: str,
    provider: str,
    model: str,
    tokens_input: int,
    tokens_output: int,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Déduire tokens pour un appel LLM

    Args:
        tenant_id: UUID du tenant
        provider: Provider LLM (openai, groq, anthropic, google)
        model: Modèle utilisé (gpt-4o, llama-3.3-70b, etc.)
        tokens_input: Tokens consommés en input
        tokens_output: Tokens générés en output
        metadata: Métadonnées additionnelles

    Returns:
        Dict avec success, tokens_deducted, new_balance, error
    """
    # Calcul coût total (1:1 pour l'instant, peut être majoré plus tard)
    cost_tokens = tokens_input + tokens_output

    try:
        tenant_uuid = uuid.UUID(tenant_id)  # Convertir string → UUID Python

        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT set_tenant(%s)", (tenant_uuid,))

                # Appeler fonction PostgreSQL
                cur.execute(
                    "SELECT deduct_tokens(%s, %s, %s, %s, %s, %s, %s)",
                    (
                        tenant_uuid,
                        cost_tokens,
                        provider,
                        model,
                        tokens_input,
                        tokens_output,
                        json.dumps(metadata or {})
                    )
                )

                result = cur.fetchone()[0]
                conn.commit()

                if result.get("success"):
                    logger.info(
                        f"Tokens deducted: {cost_tokens} from tenant {tenant_id} "
                        f"({provider}/{model}) - Balance: {result['new_balance']}"
                    )
                else:
                    logger.warning(
                        f"Insufficient tokens for tenant {tenant_id}: "
                        f"required {cost_tokens}, balance {result.get('balance', 0)}"
                    )

                return result

    except Exception as e:
        logger.error(f"Erreur deduct tokens: {e}")
        return {
            "success": False,
            "error": f"Erreur technique: {str(e)}"
        }


def get_usage_history(
    tenant_id: str,
    limit: int = 20,
    offset: int = 0
) -> list[Dict[str, Any]]:
    """
    Récupère l'historique d'utilisation tokens

    Args:
        tenant_id: UUID du tenant
        limit: Nombre max de résultats
        offset: Offset pour pagination

    Returns:
        Liste des logs d'utilisation
    """
    try:
        tenant_uuid = uuid.UUID(tenant_id)  # Convertir string → UUID Python

        with psycopg.connect(settings.postgres_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT set_tenant(%s)", (tenant_uuid,))

                cur.execute("""
                    SELECT
                        id, provider, model,
                        tokens_input, tokens_output, tokens_total,
                        cost_tokens, balance_after,
                        latency_ms, created_at, metadata
                    FROM token_usage_logs
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                rows = cur.fetchall()

                return [
                    {
                        "id": str(row[0]),
                        "provider": row[1],
                        "model": row[2],
                        "tokens_input": row[3],
                        "tokens_output": row[4],
                        "tokens_total": row[5],
                        "cost_tokens": row[6],
                        "balance_after": row[7],
                        "latency_ms": row[8],
                        "created_at": row[9].isoformat() if row[9] else None,
                        "metadata": row[10],
                    }
                    for row in rows
                ]

    except Exception as e:
        logger.error(f"Erreur get usage history: {e}")
        return []
