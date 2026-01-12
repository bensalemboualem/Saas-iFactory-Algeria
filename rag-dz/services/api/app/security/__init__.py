"""
Module sécurité IAFactory

- licence_check: Vérification dongle USB (anticipation)
- middleware: Auth, rate limiting, CORS
"""

# Licence check (USB dongle)
from .licence_check import (
    DongleLicenceChecker,
    get_licence_checker,
    check_voice_licence,
    LicenceError,
)

# Middleware (auth, rate limiting)
from .middleware import (
    EnhancedAuthMiddleware,
    RateLimitMiddleware,
    RateLimiter,
    rate_limiter,
    hash_api_key,
    validate_api_key_format,
)

__all__ = [
    # Licence check
    "DongleLicenceChecker",
    "get_licence_checker",
    "check_voice_licence",
    "LicenceError",
    # Middleware
    "EnhancedAuthMiddleware",
    "RateLimitMiddleware",
    "RateLimiter",
    "rate_limiter",
    "hash_api_key",
    "validate_api_key_format",
]
