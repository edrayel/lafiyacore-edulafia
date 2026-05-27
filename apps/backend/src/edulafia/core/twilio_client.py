import logging
from typing import Any
import httpx
from fastapi import HTTPException, status

from edulafia.config import settings

logger = logging.getLogger(__name__)


class TwilioClient:
    """Async client for Twilio SMS API."""

    @classmethod
    async def send_sms(cls, to_phone: str, body: str) -> dict[str, Any]:
        """Send an SMS using Twilio API."""
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        phone_number = settings.TWILIO_PHONE_NUMBER

        if not all([account_sid, auth_token, phone_number]):
            logger.error("Twilio credentials are not fully configured. SMS delivery failed.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SMS provider is not configured."
            )

        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        auth = (account_sid, auth_token)
        data = {
            "To": to_phone,
            "From": phone_number,
            "Body": body
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, auth=auth)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Twilio API Error: {e.response.text}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="SMS delivery failed via upstream provider."
            )
        except Exception as e:
            logger.exception("Failed to connect to Twilio")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during SMS delivery."
            )