import base64
import json
import os
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy.types import String, TypeDecorator

from edulafia.config import settings


class EncryptedString(TypeDecorator):
    """
    SQLAlchemy TypeDecorator that encrypts strings using AES-256-GCM.
    
    The data is stored in the database as a base64 encoded string containing
    both the initialization vector (nonce) and the ciphertext.
    """
    impl = String
    cache_ok = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        key_str = getattr(settings, "ENCRYPTION_KEY", None)
        if not key_str:
            if getattr(settings, "is_production", False):
                raise ValueError(
                    "ENCRYPTION_KEY is not set. Database encryption requires a 32-byte key "
                    "in production. Generate one with: openssl rand -hex 32"
                )
            import logging
            logging.getLogger(__name__).info(
                "ENCRYPTION_KEY not set — using JWT_SECRET_KEY as encryption fallback "
                "(acceptable for development; for production, set ENCRYPTION_KEY)"
            )
            key_str = getattr(settings, "JWT_SECRET_KEY", "0" * 32)

        # Ensure key is exactly 32 bytes for AES-256
        key_bytes = key_str.encode("utf-8")
        if len(key_bytes) < 32:
            key_bytes = key_bytes.ljust(32, b"0")
        elif len(key_bytes) > 32:
            key_bytes = key_bytes[:32]

        self._aesgcm = AESGCM(key_bytes)

    def process_bind_param(self, value: str | None, dialect: Any) -> str | None:
        """Encrypt the value before storing in the database."""
        if value is None:
            return None

        nonce = os.urandom(12)  # 96-bit nonce recommended for GCM
        ciphertext = self._aesgcm.encrypt(nonce, value.encode("utf-8"), None)

        # Store as base64(nonce + ciphertext)
        combined = nonce + ciphertext
        return base64.b64encode(combined).decode("utf-8")

    def process_result_value(self, value: str | None, dialect: Any) -> str | None:
        """Decrypt the value after retrieving from the database."""
        if value is None:
            return None

        try:
            combined = base64.b64decode(value.encode("utf-8"))
            nonce = combined[:12]
            ciphertext = combined[12:]

            plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Failed to decrypt field: {str(e)}") from e


class EncryptedJSON(EncryptedString):
    """
    SQLAlchemy TypeDecorator that encrypts JSON structures using AES-256-GCM.
    
    The data is serialized to JSON string, encrypted, and stored as a base64 string.
    """

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """Serialize and encrypt the JSON value."""
        if value is None:
            return None

        json_str = json.dumps(value)
        return super().process_bind_param(json_str, dialect)

    def process_result_value(self, value: str | None, dialect: Any) -> Any:
        """Decrypt and deserialize the JSON value."""
        if value is None:
            return None

        decrypted_str = super().process_result_value(value, dialect)
        if decrypted_str is None:
            return None

        return json.loads(decrypted_str)
