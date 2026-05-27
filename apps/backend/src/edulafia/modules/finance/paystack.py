import logging
from typing import Any
import httpx
from fastapi import HTTPException, status

from edulafia.config import settings

logger = logging.getLogger(__name__)


class PaystackClient:
    """Async client for Paystack API."""

    BASE_URL = "https://api.paystack.co"

    @classmethod
    async def initialize_transaction(
        cls,
        email: str,
        amount: float,
        reference: str,
        currency: str = "NGN"
    ) -> str:
        """Initialize a transaction and return the authorization URL."""
        secret_key = settings.PAYSTACK_SECRET_KEY
        if not secret_key:
            logger.error("PAYSTACK_SECRET_KEY not set. Payment gateway is unavailable.")
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Payment gateway is not configured. Set PAYSTACK_SECRET_KEY to enable payments."
            )

        url = f"{cls.BASE_URL}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "amount": int(amount * 100),  # Paystack expects lowest denomination (kobo/cents)
            "reference": reference,
            "currency": currency,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["data"]["authorization_url"]
        except httpx.HTTPStatusError as e:
            logger.error(f"Paystack API Error: {e.response.text}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Payment gateway initialization failed"
            )
        except Exception as e:
            logger.exception("Failed to initialize Paystack transaction")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during payment initialization"
            )

    @classmethod
    async def verify_transaction(cls, reference: str) -> dict[str, Any]:
        """Verify a transaction status with Paystack."""
        secret_key = settings.PAYSTACK_SECRET_KEY
        if not secret_key:
            logger.error("PAYSTACK_SECRET_KEY not set. Payment verification is unavailable.")
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Payment gateway is not configured. Set PAYSTACK_SECRET_KEY to enable payments."
            )

        url = f"{cls.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {secret_key}",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["data"]
        except httpx.HTTPStatusError as e:
            logger.error(f"Paystack API Error: {e.response.text}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Payment gateway verification failed"
            )
        except Exception as e:
            logger.exception("Failed to verify Paystack transaction")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during payment verification"
            )