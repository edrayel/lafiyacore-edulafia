"""Finance webhooks API endpoints."""

import hmac
import hashlib
import json
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.modules.finance.repository import (
    FeeLedgerRepository,
    PaymentConfigurationRepository,
)
from edulafia.modules.finance.models import FeeLedger

router = APIRouter(prefix="/webhooks", tags=["Finance Webhooks"])

async def process_payment_webhook(
    db: AsyncSession,
    gateway: str,
    reference: str,
    signature: str,
    raw_body: bytes,
    payload: dict[str, Any]
):
    """Process a payment webhook."""
    ledger_repo = FeeLedgerRepository(db)
    config_repo = PaymentConfigurationRepository(db)

    # Find pending payment by reference
    payment: FeeLedger | None = await ledger_repo.get_by_gateway_reference(reference)
    if not payment:
        # Fallback to payment_reference
        from sqlalchemy import select
        stmt = select(FeeLedger).where(FeeLedger.payment_reference == reference)
        result = await db.execute(stmt)
        payment = result.scalar_one_or_none()

        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    # Get configuration for the school to verify signature
    config = await config_repo.get_by_school_gateway(payment.school_id, gateway)
    if not config:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment configuration not found")

    # Verify signature
    secret = config.webhook_secret or config.secret_key
    if not secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook secret not configured")

    secret_str = str(secret).encode('utf-8')

    is_valid = False
    if gateway == "paystack":
        expected_signature = hmac.new(secret_str, raw_body, hashlib.sha512).hexdigest()
        is_valid = hmac.compare_digest(expected_signature, signature)
    elif gateway == "flutterwave":
        expected_signature = hmac.new(secret_str, raw_body, hashlib.sha256).hexdigest()
        is_valid = hmac.compare_digest(expected_signature, signature)
    elif gateway == "remita":
        expected_signature = hmac.new(secret_str, raw_body, hashlib.sha512).hexdigest()
        is_valid = hmac.compare_digest(expected_signature, signature)
    else:
        is_valid = False

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    # Validate amount
    expected_amount = float(payment.amount)
    actual_amount = None

    if gateway == "paystack":
        payload_amount = payload.get("data", {}).get("amount", 0)
        actual_amount = float(payload_amount) / 100.0
    elif gateway == "flutterwave":
        payload_amount = payload.get("data", {}).get("amount", 0)
        actual_amount = float(payload_amount)
    elif gateway == "remita":
        payload_amount = payload.get("amount", 0)
        actual_amount = float(payload_amount)

    if actual_amount is not None and abs(actual_amount - expected_amount) > 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Amount mismatch. Expected {expected_amount}, received {actual_amount}"
        )

    # Mark completed
    if not payment.gateway_response:
        payment.gateway_response = {}

    payment.gateway_response = {
        **payment.gateway_response,
        "webhook_payload": payload,
        "status": "completed"
    }

    await db.flush()
    await db.commit()
    return {"status": "success"}


@router.post("/paystack", summary="Paystack Webhook")
async def paystack_webhook(
    request: Request,
    x_paystack_signature: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Handle Paystack webhooks."""
    if not x_paystack_signature:
        raise HTTPException(status_code=400, detail="Missing signature header")

    raw_body = await request.body()
    try:
        payload = await request.json()
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    data = payload.get("data", {})
    reference = data.get("reference")
    if not reference:
        return {"status": "ignored", "reason": "No reference"}

    event = payload.get("event")
    if event != "charge.success":
        return {"status": "ignored", "reason": f"Unhandled event {event}"}

    return await process_payment_webhook(
        db=db,
        gateway="paystack",
        reference=reference,
        signature=x_paystack_signature,
        raw_body=raw_body,
        payload=payload
    )


@router.post("/flutterwave", summary="Flutterwave Webhook")
async def flutterwave_webhook(
    request: Request,
    verif_hash: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Handle Flutterwave webhooks."""
    if not verif_hash:
        raise HTTPException(status_code=400, detail="Missing verif-hash header")

    raw_body = await request.body()
    try:
        payload = await request.json()
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    data = payload.get("data", {})
    reference = data.get("tx_ref")
    if not reference:
        return {"status": "ignored", "reason": "No reference"}

    status_str = data.get("status")
    if status_str != "successful":
        return {"status": "ignored", "reason": f"Unhandled status {status_str}"}

    return await process_payment_webhook(
        db=db,
        gateway="flutterwave",
        reference=reference,
        signature=verif_hash,
        raw_body=raw_body,
        payload=payload
    )


@router.post("/remita", summary="Remita Webhook")
async def remita_webhook(
    request: Request,
    authorization: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Handle Remita webhooks."""
    if not authorization:
        authorization = ""

    raw_body = await request.body()
    try:
        payload = await request.json()
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if isinstance(payload, list) and len(payload) > 0:
        event = payload[0]
    else:
        event = payload

    reference = event.get("orderId") or event.get("transactionId")
    if not reference:
        return {"status": "ignored", "reason": "No reference"}

    return await process_payment_webhook(
        db=db,
        gateway="remita",
        reference=reference,
        signature=authorization,
        raw_body=raw_body,
        payload=event
    )
