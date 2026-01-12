import hashlib
import psycopg
from contextlib import contextmanager
import logging
from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

@contextmanager
def get_db_connection():
    with psycopg.connect(settings.postgres_url, autocommit=True) as conn:
        yield conn

def get_tenant_by_key(api_key: str):
    if not api_key:
        return None
    key_hash = sha256(api_key)
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT t.id, t.name, k.plan, k.rate_limit_per_minute,
                       k.quota_tokens_monthly, k.quota_audio_seconds_monthly, 
                       k.quota_ocr_pages_monthly
                FROM api_keys k 
                JOIN tenants t ON k.tenant_id = t.id
                WHERE k.key_hash = %s AND k.revoked = false AND t.status = 'active'
            """, (key_hash,))
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": str(row[0]), "name": row[1], "plan": row[2],
                "rate_limit_per_minute": row[3], "quota_tokens": row[4],
                "quota_audio_seconds": row[5], "quota_ocr_pages": row[6]
            }
    except Exception as e:
        logger.error(f"Database error: {e}")
        return None

def insert_usage(event: dict):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usage_events (tenant_id, request_id, route, method, 
                tokens_input, tokens_output, audio_seconds, ocr_pages, 
                latency_ms, model_used, status_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (event.get("tenant_id"), event.get("request_id"), 
                  event.get("route"), event.get("method", "POST"),
                  event.get("tokens_input", 0), event.get("tokens_output", 0),
                  event.get("audio_seconds", 0), event.get("ocr_pages", 0),
                  event.get("latency_ms", 0), event.get("model_used", "unknown"),
                  event.get("status_code", 200)))
    except Exception as e:
        logger.error(f"Failed to insert usage: {e}")
