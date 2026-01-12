"""
Module de vérification de licence USB (Dongle)

Anticipe la protection par clé USB physique pour:
- Déploiement Suisse (clients premium)
- Déploiement Algérie (cabinets médicaux/juridiques)

TODO: Implémenter vérification réelle avec pyusb ou pySerial
"""

import logging
import platform
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class LicenceError(Exception):
    """Erreur de licence"""
    pass


class DongleLicenceChecker:
    """
    Vérificateur de licence USB (dongle)

    Fonctionnalités anticipées:
    - Détection clé USB avec UUID spécifique
    - Vérification date expiration
    - Contrôle features activées (Voice, RAG, Multi-LLM, etc.)
    - Logging tentatives accès non autorisées
    """

    def __init__(self):
        self.enabled = False  # Désactivé par défaut en dev
        self.usb_vendor_id = "0x1234"  # TODO: Remplacer par vrai vendor ID
        self.usb_product_id = "0x5678"  # TODO: Remplacer par vrai product ID

    def check_dongle_present(self) -> bool:
        """
        Vérifie présence de la clé USB dongle

        Returns:
            True si dongle présent et valide

        TODO: Implémenter avec pyusb
        """
        if not self.enabled:
            logger.debug("Licence check DISABLED (mode dev)")
            return True

        try:
            # TODO: Remplacer par vraie vérification USB
            # import usb.core
            # device = usb.core.find(idVendor=0x1234, idProduct=0x5678)
            # return device is not None

            logger.warning("Dongle check NOT IMPLEMENTED - returning True")
            return True
        except Exception as e:
            logger.error(f"Erreur vérification dongle: {e}")
            return False

    def get_licence_info(self) -> Dict[str, Any]:
        """
        Récupère informations de licence depuis le dongle

        Returns:
            Dict avec: client_id, expiration, features, region

        TODO: Lire vraies données depuis EEPROM du dongle
        """
        if not self.enabled:
            return {
                "client_id": "DEV-00000",
                "client_name": "Development Mode",
                "region": "DZ",  # Algérie par défaut
                "expiration": datetime.now() + timedelta(days=365),
                "features": ["voice", "rag", "multi_llm", "multi_tenant"],
                "max_users": 999,
                "dongle_present": False,
            }

        # TODO: Lire vraies données
        return {
            "client_id": "PROD-12345",
            "client_name": "Cabinet Example",
            "region": "CH",  # Suisse
            "expiration": datetime(2026, 12, 31),
            "features": ["voice", "rag"],
            "max_users": 10,
            "dongle_present": True,
        }

    def verify_feature_access(self, feature: str) -> bool:
        """
        Vérifie si une feature est autorisée par la licence

        Args:
            feature: Nom de la feature (voice, rag, multi_llm, etc.)

        Returns:
            True si feature autorisée

        Raises:
            LicenceError si licence invalide ou feature non autorisée
        """
        if not self.enabled:
            return True

        if not self.check_dongle_present():
            raise LicenceError("Dongle USB non détecté")

        licence_info = self.get_licence_info()

        # Check expiration
        if licence_info["expiration"] < datetime.now():
            raise LicenceError(
                f"Licence expirée le {licence_info['expiration'].strftime('%d/%m/%Y')}"
            )

        # Check feature
        if feature not in licence_info["features"]:
            raise LicenceError(
                f"Feature '{feature}' non autorisée par la licence"
            )

        return True

    def enable(self):
        """Active la vérification de licence (mode production)"""
        self.enabled = True
        logger.info("Licence check ENABLED")

    def disable(self):
        """Désactive la vérification (mode dev/test)"""
        self.enabled = False
        logger.info("Licence check DISABLED")


# Instance globale
_licence_checker: Optional[DongleLicenceChecker] = None


def get_licence_checker() -> DongleLicenceChecker:
    """Récupère l'instance du checker de licence"""
    global _licence_checker
    if _licence_checker is None:
        _licence_checker = DongleLicenceChecker()
    return _licence_checker


def check_voice_licence() -> bool:
    """
    Shortcut: Vérifie licence pour Voice Agent

    Returns:
        True si autorisé

    Usage dans voice_agent/router.py:
        from app.security.licence_check import check_voice_licence

        @router.post("/transcribe")
        async def transcribe(...):
            if not check_voice_licence():
                raise HTTPException(403, "Licence Voice Agent requise")
    """
    try:
        checker = get_licence_checker()
        return checker.verify_feature_access("voice")
    except LicenceError as e:
        logger.error(f"Licence error: {e}")
        return False


# Notes d'implémentation future:
"""
HARDWARE DONGLE USB - TODO LIST:

1. Choisir dongle compatible:
   - YubiKey (cher mais sécurisé)
   - Arduino Pro Micro (DIY, économique)
   - STM32 custom (milieu de gamme)

2. Installer dépendances:
   pip install pyusb pyserial cryptography

3. Générer clés RSA pour signature:
   from cryptography.hazmat.primitives.asymmetric import rsa
   private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

4. Écrire données dans EEPROM du dongle:
   - Client ID (16 bytes)
   - Expiration date (8 bytes timestamp)
   - Features bitmap (4 bytes)
   - Signature RSA (256 bytes)

5. Lire et vérifier signature au runtime

6. Logging sécurisé:
   - Journaliser tentatives accès sans dongle
   - Alerter admin si dongle retiré pendant utilisation

7. Fallback graceful:
   - Mode dégradé si dongle temporairement déconnecté (5 min grace period)
   - Sauvegarder état transcriptions en cours
"""
