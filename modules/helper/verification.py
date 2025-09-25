import time
from typing import Dict

from flask import jsonify, request
from flask_api import status


class VerificationCache:
    """In-memory TTL cache for phone number verifications.

    Note: For multi-instance deployments, replace with Redis/Memcached.
    """

    def __init__(self, ttl_seconds: int = 600):
        self._phone_to_expiry_epoch_ms: Dict[str, int] = {}
        self._ttl_ms = ttl_seconds * 1000

    def mark_verified(self, phone_number: str) -> None:
        now_ms = int(time.time() * 1000)
        self._phone_to_expiry_epoch_ms[normalize(phone_number)] = now_ms + self._ttl_ms

    def is_verified(self, phone_number: str) -> bool:
        normalized = normalize(phone_number)
        expiry = self._phone_to_expiry_epoch_ms.get(normalized)
        if not expiry:
            return False
        if int(time.time() * 1000) > expiry:
            # Expired; cleanup entry
            try:
                del self._phone_to_expiry_epoch_ms[normalized]
            except KeyError:
                pass
            return False
        return True


def normalize(phone_number: str) -> str:
    return (phone_number or "").strip().replace(" ", "")


verification_cache = VerificationCache(ttl_seconds=600)


def require_verified_number(func):
    """Decorator to enforce that a valid, recently verified phone number is provided.

    Expects header: x-phone-number: +91XXXXXXXXXX
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        phone_number = request.headers.get("x-phone-number")
        if not phone_number:
            return jsonify({"message": "x-phone-number header is required"}), status.HTTP_401_UNAUTHORIZED
        if not verification_cache.is_verified(phone_number):
            return jsonify({
                "message": "Phone number not verified or verification expired",
                "action": "POST /hitaya/api/v1/network/verify with { phoneNumber }"
            }), status.HTTP_403_FORBIDDEN
        return func(*args, **kwargs)

    return wrapper


