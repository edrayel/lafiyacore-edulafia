"""Application configuration using pydantic-settings."""

import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# Resolve .env path relative to project root
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ENV_FILE = os.path.join(_BACKEND_DIR, "..", "..", ".env")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "EduLafia"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    APP_SECRET_KEY: str = ""

    # Database
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    REDIS_URL: str = ""
    COUCHDB_URL: str = ""
    COUCHDB_USER: str = ""
    COUCHDB_PASSWORD: str = ""

    # Encryption
    ENCRYPTION_KEY: str = ""

    # JWT
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://localhost:3000",
        "https://edulafia.lafiyacore.com",
    ]

    # AWS
    AWS_REGION: str = "af-south-1"
    AWS_S3_BUCKET: str = "edulafia-uploads-dev"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_KMS_KEY_ID: str = ""

    # External Services
    APP_URL: str = "http://localhost:5173"
    SENTINEL_ALERT_EMAIL: str = "admin@edulafia.lafiyacore.com"
    TERMII_API_KEY: str = ""
    TERMII_SENDER_ID: str = "EduLafia"
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    PAYSTACK_SECRET_KEY: str = ""
    PAYSTACK_PUBLIC_KEY: str = ""

    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Email
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    def model_post_init(self, __context) -> None:
        """Validate secrets after model initialization."""
        if self.is_production and self.APP_DEBUG:
            self.APP_DEBUG = False
            logger.warning("APP_DEBUG forced to False in production environment")
        self._validate_secrets()

    def _validate_secrets(self) -> None:
        """Check for placeholder secrets and warn or raise error."""
        REQUIRED_SECRETS = {
            "JWT_SECRET_KEY": self.JWT_SECRET_KEY,
            "APP_SECRET_KEY": self.APP_SECRET_KEY,
            "DATABASE_URL": self.DATABASE_URL,
        }

        issues = []

        for name, value in REQUIRED_SECRETS.items():
            if not value:
                issues.append(f"{name} is empty")
            elif name != "DATABASE_URL" and value in ("change-me", "change_me"):
                issues.append(f"{name} is a placeholder")

        if not self.COUCHDB_PASSWORD or self.COUCHDB_PASSWORD == "password":
            issues.append("COUCHDB_PASSWORD is a placeholder")

        if not self.ENCRYPTION_KEY:
            issues.append("ENCRYPTION_KEY is empty - database encryption will be unavailable")

        if self.is_production:
            if any("localhost" in origin or "127.0.0.1" in origin for origin in self.CORS_ORIGINS):
                issues.append("CORS_ORIGINS contains localhost in production")

        if issues:
            message = (
                f"Security warning: {'; '.join(issues)}. "
                "Set all required environment variables in .env before deploying."
            )
            if self.is_production:
                raise ValueError(message)
            else:
                logger.warning(message)


settings = Settings()
