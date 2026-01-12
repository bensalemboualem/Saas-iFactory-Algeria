"""
Service d'achat de tokens via Chargily (DZD) ou Stripe (CHF)
Integration avec le systeme de tokens existant
"""
import logging
import uuid
import json
import psycopg
from psycopg import sql
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..config import get_settings
from ..services.chargily_service import chargily_service

logger = logging.getLogger(__name__)
settings = get_settings()


class TokenPurchaseService:
    """Service pour l'achat de tokens"""

    def __init__(self):
        self.db_url = settings.postgres_url

    # ============================================================
    # Packs de tokens
    # ============================================================

    def get_available_packs(self, currency: str = "dzd") -> List[Dict[str, Any]]:
        """
        Liste les packs de tokens disponibles

        Args:
            currency: 'dzd' ou 'chf'

        Returns:
            Liste des packs avec prix
        """
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            id, slug, name, description,
                            tokens, bonus_tokens,
                            price_dzd, price_chf,
                            is_featured, sort_order
                        FROM token_packs
                        WHERE is_active = true
                          AND (valid_from IS NULL OR valid_from <= NOW())
                          AND (valid_until IS NULL OR valid_until > NOW())
                        ORDER BY sort_order ASC
                    """)

                    rows = cur.fetchall()

                    packs = []
                    for row in rows:
                        price = row[6] if currency == "dzd" else row[7]
                        if price is None:
                            continue  # Pack non disponible dans cette devise

                        packs.append({
                            "id": str(row[0]),
                            "slug": row[1],
                            "name": row[2],
                            "description": row[3],
                            "tokens": row[4],
                            "bonus_tokens": row[5],
                            "total_tokens": row[4] + row[5],
                            "price": float(price),
                            "currency": currency,
                            "is_featured": row[8],
                        })

                    return packs

        except Exception as e:
            logger.error(f"Erreur get_available_packs: {e}")
            return []

    def get_pack_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Recupere un pack par son slug"""
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            id, slug, name, description,
                            tokens, bonus_tokens,
                            price_dzd, price_chf
                        FROM token_packs
                        WHERE slug = %s AND is_active = true
                    """, (slug,))

                    row = cur.fetchone()
                    if not row:
                        return None

                    return {
                        "id": str(row[0]),
                        "slug": row[1],
                        "name": row[2],
                        "description": row[3],
                        "tokens": row[4],
                        "bonus_tokens": row[5],
                        "total_tokens": row[4] + row[5],
                        "price_dzd": row[6],
                        "price_chf": float(row[7]) if row[7] else None,
                    }

        except Exception as e:
            logger.error(f"Erreur get_pack_by_slug: {e}")
            return None

    # ============================================================
    # Achat via Chargily (DZD)
    # ============================================================

    async def create_chargily_checkout(
        self,
        tenant_id: str,
        pack_slug: str,
        user_id: Optional[str] = None,
        success_url: str = None,
        failure_url: str = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cree un checkout Chargily pour achat de tokens

        Args:
            tenant_id: UUID du tenant
            pack_slug: Slug du pack (starter, pro, business, dev, enterprise)
            user_id: UUID de l'utilisateur (optionnel)
            success_url: URL de redirection succes
            failure_url: URL de redirection echec
            ip_address: IP du client
            user_agent: User agent du client

        Returns:
            Dict avec checkout_url et purchase_id
        """
        # 1. Recuperer le pack
        pack = self.get_pack_by_slug(pack_slug)
        if not pack:
            return {
                "success": False,
                "error": f"Pack non trouve: {pack_slug}"
            }

        if not pack["price_dzd"]:
            return {
                "success": False,
                "error": "Pack non disponible en DZD"
            }

        # 2. Creer l'enregistrement d'achat (pending)
        purchase_id = str(uuid.uuid4())

        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO token_purchases (
                            id, tenant_id, user_id, pack_id, pack_slug,
                            tokens_amount, bonus_amount,
                            amount_dzd, currency,
                            payment_provider, payment_status,
                            ip_address, user_agent, metadata
                        ) VALUES (
                            %s, %s, %s, %s, %s,
                            %s, %s,
                            %s, 'dzd',
                            'chargily', 'pending',
                            %s, %s, %s
                        )
                    """, (
                        purchase_id,
                        tenant_id,
                        user_id,
                        pack["id"],
                        pack["slug"],
                        pack["tokens"],
                        pack["bonus_tokens"],
                        pack["price_dzd"],
                        ip_address,
                        user_agent,
                        json.dumps({"pack_name": pack["name"]})
                    ))
                    conn.commit()

        except Exception as e:
            logger.error(f"Erreur creation purchase: {e}")
            return {
                "success": False,
                "error": f"Erreur creation achat: {str(e)}"
            }

        # 3. Creer checkout Chargily
        try:
            base_url = settings.frontend_url or "https://iafactory.dz"
            checkout = await chargily_service.create_checkout(
                amount=pack["price_dzd"],
                description=f"{pack['name']} - {pack['total_tokens']:,} tokens IA Factory",
                success_url=success_url or f"{base_url}/payment/success?purchase_id={purchase_id}",
                failure_url=failure_url or f"{base_url}/payment/failure?purchase_id={purchase_id}",
                webhook_endpoint=f"{settings.api_url}/api/tokens/webhook/chargily",
                metadata={
                    "purchase_id": purchase_id,
                    "tenant_id": tenant_id,
                    "pack_slug": pack_slug,
                    "tokens": pack["total_tokens"],
                },
                locale="fr"
            )

            # 4. Mettre a jour avec checkout_id
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE token_purchases
                        SET chargily_checkout_id = %s
                        WHERE id = %s
                    """, (checkout.id, purchase_id))
                    conn.commit()

            logger.info(
                f"Checkout Chargily cree: {checkout.id} pour tenant {tenant_id} "
                f"- Pack: {pack_slug} ({pack['total_tokens']} tokens) - {pack['price_dzd']} DZD"
            )

            return {
                "success": True,
                "purchase_id": purchase_id,
                "checkout_id": checkout.id,
                "checkout_url": checkout.checkout_url,
                "pack": {
                    "name": pack["name"],
                    "tokens": pack["total_tokens"],
                    "price_dzd": pack["price_dzd"],
                }
            }

        except Exception as e:
            logger.error(f"Erreur Chargily checkout: {e}")

            # Marquer l'achat comme failed
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE token_purchases
                        SET payment_status = 'failed',
                            metadata = metadata || %s
                        WHERE id = %s
                    """, (json.dumps({"error": str(e)}), purchase_id))
                    conn.commit()

            return {
                "success": False,
                "error": f"Erreur creation checkout: {str(e)}"
            }

    # ============================================================
    # Webhook Chargily
    # ============================================================

    async def process_chargily_webhook(
        self,
        event_type: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Traite un webhook Chargily

        Args:
            event_type: Type d'evenement (checkout.paid, checkout.failed, etc.)
            data: Donnees de l'evenement

        Returns:
            Dict avec status du traitement
        """
        checkout_id = data.get("id")
        metadata = data.get("metadata", {})
        purchase_id = metadata.get("purchase_id")

        logger.info(f"Webhook Chargily: {event_type} - checkout {checkout_id}")

        if not purchase_id:
            logger.warning(f"Webhook sans purchase_id: {checkout_id}")
            return {"status": "ignored", "reason": "no_purchase_id"}

        if event_type == "checkout.paid":
            return await self._process_paid_checkout(purchase_id, checkout_id, data)

        elif event_type == "checkout.failed":
            return await self._process_failed_checkout(purchase_id, checkout_id, data)

        elif event_type == "checkout.expired":
            return await self._process_expired_checkout(purchase_id, checkout_id)

        else:
            logger.warning(f"Event type non gere: {event_type}")
            return {"status": "ignored", "reason": f"unknown_event: {event_type}"}

    async def _process_paid_checkout(
        self,
        purchase_id: str,
        checkout_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Traite un paiement reussi"""
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Mettre a jour avec payment_id
                    cur.execute("""
                        UPDATE token_purchases
                        SET chargily_payment_id = %s
                        WHERE id = %s AND payment_status = 'pending'
                    """, (data.get("payment_id"), purchase_id))

                    # Appeler la fonction PostgreSQL pour crediter
                    cur.execute(
                        "SELECT process_token_purchase(%s)",
                        (purchase_id,)
                    )
                    result = cur.fetchone()[0]
                    conn.commit()

                    if result.get("success"):
                        logger.info(
                            f"Paiement traite: {purchase_id} - "
                            f"{result.get('tokens_credited')} tokens credites"
                        )
                        return {
                            "status": "success",
                            "purchase_id": purchase_id,
                            "tokens_credited": result.get("tokens_credited"),
                            "new_balance": result.get("new_balance")
                        }
                    else:
                        logger.error(f"Erreur traitement paiement: {result.get('error')}")
                        return {
                            "status": "error",
                            "error": result.get("error")
                        }

        except Exception as e:
            logger.error(f"Erreur process_paid_checkout: {e}")
            return {"status": "error", "error": str(e)}

    async def _process_failed_checkout(
        self,
        purchase_id: str,
        checkout_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Traite un paiement echoue"""
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE token_purchases
                        SET payment_status = 'failed',
                            metadata = metadata || %s
                        WHERE id = %s
                    """, (
                        json.dumps({
                            "failure_reason": data.get("failure_reason", "unknown"),
                            "failed_at": datetime.utcnow().isoformat()
                        }),
                        purchase_id
                    ))
                    conn.commit()

            logger.warning(f"Paiement echoue: {purchase_id}")
            return {"status": "failed", "purchase_id": purchase_id}

        except Exception as e:
            logger.error(f"Erreur process_failed_checkout: {e}")
            return {"status": "error", "error": str(e)}

    async def _process_expired_checkout(
        self,
        purchase_id: str,
        checkout_id: str
    ) -> Dict[str, Any]:
        """Traite un checkout expire"""
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE token_purchases
                        SET payment_status = 'failed',
                            metadata = metadata || '{"expired": true}'::jsonb
                        WHERE id = %s AND payment_status = 'pending'
                    """, (purchase_id,))
                    conn.commit()

            logger.info(f"Checkout expire: {purchase_id}")
            return {"status": "expired", "purchase_id": purchase_id}

        except Exception as e:
            logger.error(f"Erreur process_expired_checkout: {e}")
            return {"status": "error", "error": str(e)}

    # ============================================================
    # Historique achats
    # ============================================================

    def get_purchase_history(
        self,
        tenant_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Recupere l'historique des achats d'un tenant"""
        try:
            with psycopg.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            p.id, p.pack_slug, p.tokens_amount, p.bonus_amount,
                            p.amount_dzd, p.amount_chf, p.currency,
                            p.payment_provider, p.payment_status,
                            p.created_at, p.paid_at,
                            t.name as pack_name
                        FROM token_purchases p
                        LEFT JOIN token_packs t ON t.id = p.pack_id
                        WHERE p.tenant_id = %s
                        ORDER BY p.created_at DESC
                        LIMIT %s OFFSET %s
                    """, (tenant_id, limit, offset))

                    rows = cur.fetchall()

                    return [
                        {
                            "id": str(row[0]),
                            "pack_slug": row[1],
                            "tokens": row[2] + row[3],
                            "tokens_base": row[2],
                            "tokens_bonus": row[3],
                            "amount": row[4] or row[5],
                            "currency": row[6],
                            "payment_provider": row[7],
                            "status": row[8],
                            "created_at": row[9].isoformat() if row[9] else None,
                            "paid_at": row[10].isoformat() if row[10] else None,
                            "pack_name": row[11],
                        }
                        for row in rows
                    ]

        except Exception as e:
            logger.error(f"Erreur get_purchase_history: {e}")
            return []


# Instance globale
token_purchase_service = TokenPurchaseService()
