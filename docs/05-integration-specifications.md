# EduLafia Platform - Integration Specifications

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. Integration Overview

### 1.1 Integration Architecture
The EduLafia platform integrates with multiple external services for communication, payments, and government reporting. All integrations follow a consistent pattern with proper error handling, retry logic, and monitoring.

### 1.2 Integration Principles
1. **Resilience**: All integrations must handle failures gracefully
2. **Retry Logic**: Exponential backoff for failed requests
3. **Fallback Mechanisms**: Alternative channels when primary fails
4. **Monitoring**: All integration calls logged and monitored
5. **Security**: API keys encrypted, webhooks validated
6. **Idempotency**: All payment webhooks must be idempotent

## 2. SMS Integration (Termii)

### 2.1 Overview
Termii is the primary SMS gateway for EduLafia, used for OTP delivery, absence notifications, payment receipts, and urgent alerts.

### 2.2 Configuration
```python
# Termii configuration
TERMII_CONFIG = {
    "api_key": os.getenv("TERMII_API_KEY"),
    "sender_id": "EduLafia",
    "base_url": "https://api.termii.com/api",
    "channels": ["sms"],  # Can also use ['dnd', 'generic']
    "type": "plain",  # or 'unicode' for special characters
    "retry_attempts": 3,
    "retry_delay": 5,  # seconds
    "timeout": 30  # seconds
}
```

### 2.3 SMS Templates
```python
# SMS template definitions
SMS_TEMPLATES = {
    "otp_verification": {
        "template": "Your EduLafia verification code is: {{otp_code}}. Valid for 10 minutes. Do not share this code with anyone.",
        "use_case": "Parent portal login, password reset"
    },
    "absence_alert": {
        "template": "EduLafia Alert: {{student_name}} was marked absent from {{school_name}} today ({{date}}). Reason: {{reason}}. Login to excuse or view details.",
        "use_case": "Daily absence notifications to parents"
    },
    "payment_receipt": {
        "template": "EduLafia Payment Receipt: ₦{{amount}} received for {{student_name}} ({{fee_category}}). Receipt: {{receipt_number}}. Balance: ₦{{balance}}.",
        "use_case": "Payment confirmation to parents"
    },
    "urgent_health_alert": {
        "template": "URGENT: {{school_name}} health alert - {{alert_message}}. Please contact the school immediately.",
        "use_case": "Urgent health notifications"
    },
    "welcome_message": {
        "template": "Welcome to EduLafia! Your portal access is ready. Login URL: {{login_url}}. Use your phone number to login.",
        "use_case": "New parent onboarding"
    },
    "password_reset": {
        "template": "Your EduLafia password reset code: {{otp_code}}. Valid for 10 minutes. If you didn't request this, ignore.",
        "use_case": "Password reset flow"
    },
    "consecutive_absence": {
        "template": "EduLafia Alert: {{student_name}} has been absent for {{days}} consecutive days from {{school_name}}. Please contact the school.",
        "use_case": "3-day consecutive absence alert"
    }
}
```

### 2.4 Implementation
```python
import aiohttp
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TermiiService:
    """Service for sending SMS via Termii API."""
    
    def __init__(self, api_key: str, sender_id: str = "EduLafia"):
        self.api_key = api_key
        self.sender_id = sender_id
        self.base_url = "https://api.termii.com/api"
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def send_sms(
        self,
        to: str,
        message: str,
        message_type: str = "plain"
    ) -> Dict[str, Any]:
        """Send SMS message."""
        
        # Validate phone number
        to = self._format_phone_number(to)
        
        payload = {
            "to": to,
            "from": self.sender_id,
            "sms": message,
            "type": message_type,
            "api_key": self.api_key
        }
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/sms/send",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    logger.info(f"SMS sent successfully to {to}")
                    return {
                        "success": True,
                        "message_id": result.get("message_id"),
                        "balance": result.get("balance")
                    }
                else:
                    logger.error(f"SMS failed: {result}")
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error"),
                        "status_code": response.status
                    }
        
        except Exception as e:
            logger.error(f"SMS exception: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_otp(
        self,
        phone: str,
        otp_code: str,
        template: str = "otp_verification"
    ) -> Dict[str, Any]:
        """Send OTP via SMS."""
        
        message = self._render_template(template, {"otp_code": otp_code})
        return await self.send_sms(phone, message)
    
    async def send_bulk_sms(
        self,
        recipients: List[Dict[str, str]],
        message: str
    ) -> Dict[str, Any]:
        """Send bulk SMS to multiple recipients."""
        
        # Termii bulk endpoint
        payload = {
            "to": [r["phone"] for r in recipients],
            "from": self.sender_id,
            "sms": message,
            "type": "plain",
            "api_key": self.api_key
        }
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/sms/send/bulk",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "success": True,
                        "total_sent": len(recipients),
                        "message_ids": result.get("message_ids", [])
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error")
                    }
        
        except Exception as e:
            logger.error(f"Bulk SMS exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_balance(self) -> Dict[str, Any]:
        """Get Termii account balance."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/balance",
                params={"api_key": self.api_key}
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "success": True,
                        "balance": result.get("balance"),
                        "currency": result.get("currency")
                    }
                else:
                    return {"success": False, "error": result.get("message")}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_phone_number(self, phone: str) -> str:
        """Format phone number to Termii format."""
        # Remove spaces and special characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Add country code if not present
        if phone.startswith('0'):
            phone = '234' + phone[1:]
        elif not phone.startswith('234'):
            phone = '234' + phone
        
        return phone
    
    def _render_template(self, template_name: str, context: Dict) -> str:
        """Render SMS template with context."""
        templates = {
            "otp_verification": "Your EduLafia verification code is: {otp_code}. Valid for 10 minutes. Do not share this code with anyone.",
            "absence_alert": "EduLafia Alert: {student_name} was marked absent from {school_name} today ({date}). Reason: {reason}.",
            "payment_receipt": "EduLafia Payment Receipt: ₦{amount} received for {student_name} ({fee_category}). Receipt: {receipt_number}.",
            "urgent_health_alert": "URGENT: {school_name} health alert - {alert_message}. Please contact the school immediately.",
            "welcome_message": "Welcome to EduLafia! Your portal access is ready. Login URL: {login_url}.",
            "password_reset": "Your EduLafia password reset code: {otp_code}. Valid for 10 minutes.",
            "consecutive_absence": "EduLafia Alert: {student_name} has been absent for {days} consecutive days from {school_name}."
        }
        
        template = templates.get(template_name, "")
        return template.format(**context)
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

### 2.5 Error Handling
```python
class TermiiErrorHandler:
    """Handle Termii API errors."""
    
    ERROR_CODES = {
        400: "Bad request - check parameters",
        401: "Unauthorized - invalid API key",
        402: "Payment required - insufficient balance",
        404: "Not found - invalid endpoint",
        429: "Too many requests - rate limit exceeded",
        500: "Server error - try again later"
    }
    
    @staticmethod
    def handle_error(status_code: int, response: dict) -> str:
        """Get user-friendly error message."""
        base_message = TermiiErrorHandler.ERROR_CODES.get(
            status_code, 
            "Unknown error"
        )
        
        api_message = response.get("message", "")
        
        return f"{base_message}. Details: {api_message}"
    
    @staticmethod
    def should_retry(status_code: int) -> bool:
        """Determine if request should be retried."""
        retryable_codes = [429, 500, 502, 503, 504]
        return status_code in retryable_codes
```

## 3. WhatsApp Integration

### 3.1 Overview
WhatsApp Business API integration via a Nigerian Business Solution Provider (BSP) for parent communication, report card delivery, and notifications.

### 3.2 Configuration
```python
# WhatsApp configuration
WHATSAPP_CONFIG = {
    "api_url": os.getenv("WHATSAPP_API_URL"),
    "phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    "access_token": os.getenv("WHATSAPP_ACCESS_TOKEN"),
    "webhook_verify_token": os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN"),
    "app_secret": os.getenv("WHATSAPP_APP_SECRET"),
    "retry_attempts": 3,
    "retry_delay": 5,
    "timeout": 30
}
```

### 3.3 Message Templates
```python
# WhatsApp message templates (pre-approved by Meta)
WHATSAPP_TEMPLATES = {
    "absence_notification": {
        "name": "edulafia_absence_notification",
        "language": "en",
        "components": [
            {
                "type": "header",
                "parameters": [
                    {"type": "text", "text": "📋 Attendance Alert"}
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "{{1}}"},  # Student name
                    {"type": "text", "text": "{{2}}"},  # School name
                    {"type": "text", "text": "{{3}}"},  # Date
                    {"type": "text", "text": "{{4}}"}   # Reason
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "0",
                "parameters": [
                    {"type": "text", "text": "Excuse Absence"}
                ]
            }
        ]
    },
    "report_card_delivery": {
        "name": "edulafia_report_card",
        "language": "en",
        "components": [
            {
                "type": "header",
                "parameters": [
                    {"type": "text", "text": "📊 Report Card Available"}
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "{{1}}"},  # Student name
                    {"type": "text", "text": "{{2}}"},  # Overall average
                    {"type": "text", "text": "{{3}}"}   # Class position
                ]
            }
        ]
    },
    "payment_receipt": {
        "name": "edulafia_payment_receipt",
        "language": "en",
        "components": [
            {
                "type": "header",
                "parameters": [
                    {"type": "text", "text": "✅ Payment Receipt"}
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "{{1}}"},  # Student name
                    {"type": "text", "text": "{{2}}"},  # Amount
                    {"type": "text", "text": "{{3}}"},  # Fee category
                    {"type": "text", "text": "{{4}}"}   # Receipt number
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "0",
                "parameters": [
                    {"type": "text", "text": "View Details"}
                ]
            }
        ]
    },
    "health_notification": {
        "name": "edulafia_health_notification",
        "language": "en",
        "components": [
            {
                "type": "header",
                "parameters": [
                    {"type": "text", "text": "🏥 Health Update"}
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "{{1}}"},  # Student name
                    {"type": "text", "text": "{{2}}"},  # Notification type
                    {"type": "text", "text": "{{3}}"}   # Details
                ]
            }
        ]
    },
    "otp_verification": {
        "name": "edulafia_otp",
        "language": "en",
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "{{1}}"}  # OTP code
                ]
            }
        ]
    }
}
```

### 3.4 Implementation
```python
import aiohttp
import hmac
import hashlib
import json
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service for WhatsApp Business API integration."""
    
    def __init__(
        self,
        api_url: str,
        phone_number_id: str,
        access_token: str,
        app_secret: str
    ):
        self.api_url = api_url
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.app_secret = app_secret
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with auth headers."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "en",
        components: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Send template message via WhatsApp."""
        
        to = self._format_phone_number(to)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    message_id = result["messages"][0]["id"]
                    logger.info(f"WhatsApp message sent: {message_id}")
                    return {
                        "success": True,
                        "message_id": message_id
                    }
                else:
                    error = result.get("error", {})
                    logger.error(f"WhatsApp send failed: {error}")
                    return {
                        "success": False,
                        "error": error.get("message", "Unknown error"),
                        "code": error.get("code")
                    }
        
        except Exception as e:
            logger.error(f"WhatsApp exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_text_message(
        self,
        to: str,
        text: str
    ) -> Dict[str, Any]:
        """Send free-form text message."""
        
        to = self._format_phone_number(to)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "success": True,
                        "message_id": result["messages"][0]["id"]
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get("message")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_document(
        self,
        to: str,
        document_url: str,
        filename: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send document via WhatsApp."""
        
        to = self._format_phone_number(to)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "document",
            "document": {
                "link": document_url,
                "filename": filename
            }
        }
        
        if caption:
            payload["document"]["caption"] = caption
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "success": True,
                        "message_id": result["messages"][0]["id"]
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get("message")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_image(
        self,
        to: str,
        image_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send image via WhatsApp."""
        
        to = self._format_phone_number(to)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": {"link": image_url}
        }
        
        if caption:
            payload["image"]["caption"] = caption
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "success": True,
                        "message_id": result["messages"][0]["id"]
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get("message")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def send_absence_notification(
        self,
        guardian_phone: str,
        student_name: str,
        school_name: str,
        date: str,
        reason: str
    ) -> Dict[str, Any]:
        """Send absence notification to guardian."""
        
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": student_name},
                    {"type": "text", "text": school_name},
                    {"type": "text", "text": date},
                    {"type": "text", "text": reason}
                ]
            }
        ]
        
        return await self.send_template_message(
            to=guardian_phone,
            template_name="edulafia_absence_notification",
            components=components
        )
    
    async def send_report_card(
        self,
        guardian_phone: str,
        student_name: str,
        overall_average: str,
        class_position: str,
        document_url: str
    ) -> Dict[str, Any]:
        """Send report card to guardian."""
        
        # First send notification
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": student_name},
                    {"type": "text", "text": overall_average},
                    {"type": "text", "text": class_position}
                ]
            }
        ]
        
        notification_result = await self.send_template_message(
            to=guardian_phone,
            template_name="edulafia_report_card",
            components=components
        )
        
        # Then send PDF document
        if notification_result["success"]:
            document_result = await self.send_document(
                to=guardian_phone,
                document_url=document_url,
                filename=f"Report_Card_{student_name.replace(' ', '_')}.pdf",
                caption=f"Report card for {student_name}"
            )
            return document_result
        
        return notification_result
    
    async def send_payment_receipt(
        self,
        guardian_phone: str,
        student_name: str,
        amount: str,
        fee_category: str,
        receipt_number: str,
        document_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send payment receipt to guardian."""
        
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": student_name},
                    {"type": "text", "text": amount},
                    {"type": "text", "text": fee_category},
                    {"type": "text", "text": receipt_number}
                ]
            }
        ]
        
        result = await self.send_template_message(
            to=guardian_phone,
            template_name="edulafia_payment_receipt",
            components=components
        )
        
        # Send receipt PDF if provided
        if result["success"] and document_url:
            await self.send_document(
                to=guardian_phone,
                document_url=document_url,
                filename=f"Receipt_{receipt_number}.pdf"
            )
        
        return result
    
    def verify_webhook_signature(
        self,
        signature: str,
        payload: bytes
    ) -> bool:
        """Verify WhatsApp webhook signature."""
        
        expected_signature = hmac.new(
            self.app_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(
            f"sha256={expected_signature}",
            signature
        )
    
    def _format_phone_number(self, phone: str) -> str:
        """Format phone number to WhatsApp format."""
        phone = ''.join(filter(str.isdigit, phone))
        
        if phone.startswith('0'):
            phone = '234' + phone[1:]
        elif not phone.startswith('234'):
            phone = '234' + phone
        
        return phone
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

### 3.5 Webhook Handler
```python
from fastapi import APIRouter, Request, HTTPException
import json

router = APIRouter()

@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request):
    """Handle WhatsApp webhook events."""
    
    # Get signature
    signature = request.headers.get("X-Hub-Signature-256")
    
    # Get body
    body = await request.body()
    
    # Verify signature
    if not whatsapp_service.verify_webhook_signature(signature, body):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse payload
    payload = json.loads(body)
    
    # Handle different webhook types
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            
            # Handle messages
            if "messages" in value:
                for message in value["messages"]:
                    await handle_incoming_message(message)
            
            # Handle status updates
            if "statuses" in value:
                for status in value["statuses"]:
                    await handle_status_update(status)
    
    return {"status": "ok"}

async def handle_incoming_message(message: dict):
    """Handle incoming WhatsApp message."""
    
    message_type = message.get("type")
    from_number = message.get("from")
    
    if message_type == "text":
        text = message["text"]["body"]
        await process_text_message(from_number, text)
    elif message_type == "button":
        button_text = message["button"]["text"]
        await process_button_response(from_number, button_text)
    # Handle other message types

async def handle_status_update(status: dict):
    """Handle message status update."""
    
    message_id = status.get("id")
    status_type = status.get("status")  # delivered, read, failed
    
    # Update notification status in database
    await update_notification_status(message_id, status_type)
```

## 4. Payment Integration (Paystack)

### 4.1 Overview
Paystack is the primary payment gateway for private school fee collection. It supports card payments, bank transfers, and USSD.

### 4.2 Configuration
```python
# Paystack configuration
PAYSTACK_CONFIG = {
    "secret_key": os.getenv("PAYSTACK_SECRET_KEY"),
    "public_key": os.getenv("PAYSTACK_PUBLIC_KEY"),
    "base_url": "https://api.paystack.co",
    "webhook_secret": os.getenv("PAYSTACK_WEBHOOK_SECRET"),
    "retry_attempts": 3,
    "timeout": 30
}
```

### 4.3 Implementation
```python
import aiohttp
import hashlib
import hmac
import json
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PaystackService:
    """Service for Paystack payment integration."""
    
    def __init__(self, secret_key: str, public_key: str, webhook_secret: str):
        self.secret_key = secret_key
        self.public_key = public_key
        self.webhook_secret = webhook_secret
        self.base_url = "https://api.paystack.co"
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with auth headers."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.secret_key}",
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def initialize_transaction(
        self,
        email: str,
        amount: int,  # Amount in kobo
        reference: str,
        metadata: Optional[Dict] = None,
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Initialize a payment transaction."""
        
        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "currency": "NGN"
        }
        
        if metadata:
            payload["metadata"] = metadata
        
        if callback_url:
            payload["callback_url"] = callback_url
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/transaction/initialize",
                json=payload
            ) as response:
                result = await response.json()
                
                if result.get("status"):
                    data = result["data"]
                    logger.info(f"Transaction initialized: {reference}")
                    return {
                        "success": True,
                        "authorization_url": data["authorization_url"],
                        "reference": data["reference"],
                        "access_code": data["access_code"]
                    }
                else:
                    logger.error(f"Initialize failed: {result}")
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error")
                    }
        
        except Exception as e:
            logger.error(f"Initialize exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def verify_transaction(
        self,
        reference: str
    ) -> Dict[str, Any]:
        """Verify a payment transaction."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/transaction/verify/{reference}"
            ) as response:
                result = await response.json()
                
                if result.get("status"):
                    data = result["data"]
                    return {
                        "success": True,
                        "reference": data["reference"],
                        "amount": data["amount"] / 100,  # Convert from kobo
                        "status": data["status"],  # success, failed, abandoned
                        "gateway_response": data["gateway_response"],
                        "paid_at": data["paid_at"],
                        "metadata": data.get("metadata", {})
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("message", "Verification failed")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_transactions(
        self,
        per_page: int = 50,
        page: int = 1,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List transactions."""
        
        params = {
            "perPage": per_page,
            "page": page
        }
        
        if status:
            params["status"] = status
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/transaction",
                params=params
            ) as response:
                result = await response.json()
                
                if result.get("status"):
                    return {
                        "success": True,
                        "transactions": result["data"],
                        "meta": result["meta"]
                    }
                else:
                    return {"success": False, "error": result.get("message")}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_balance(self) -> Dict[str, Any]:
        """Get Paystack balance."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/balance"
            ) as response:
                result = await response.json()
                
                if result.get("status"):
                    return {
                        "success": True,
                        "balance": result["data"]
                    }
                else:
                    return {"success": False, "error": result.get("message")}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_webhook_signature(
        self,
        signature: str,
        payload: bytes
    ) -> bool:
        """Verify Paystack webhook signature."""
        
        computed_hash = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(computed_hash, signature)
    
    def generate_reference(self, prefix: str = "EDU") -> str:
        """Generate unique payment reference."""
        import uuid
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = uuid.uuid4().hex[:8]
        return f"{prefix}-{timestamp}-{unique_id}"
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

### 4.4 Webhook Handler
```python
@router.post("/webhooks/paystack")
async def paystack_webhook(request: Request):
    """Handle Paystack webhook events."""
    
    # Get signature
    signature = request.headers.get("x-paystack-signature")
    
    # Get body
    body = await request.body()
    
    # Verify signature
    if not paystack_service.verify_webhook_signature(signature, body):
        logger.error("Invalid Paystack signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse payload
    payload = json.loads(body)
    event = payload.get("event")
    data = payload.get("data", {})
    
    logger.info(f"Paystack webhook: {event}")
    
    # Handle different events
    if event == "charge.success":
        await handle_successful_charge(data)
    elif event == "charge.failed":
        await handle_failed_charge(data)
    elif event == "transfer.success":
        await handle_successful_transfer(data)
    elif event == "transfer.failed":
        await handle_failed_transfer(data)
    else:
        logger.info(f"Unhandled event: {event}")
    
    return {"status": "success"}

async def handle_successful_charge(data: dict):
    """Handle successful payment."""
    
    reference = data.get("reference")
    amount = data["amount"] / 100  # Convert from kobo
    status = data.get("status")
    metadata = data.get("metadata", {})
    
    # Find ledger entry
    ledger_entry = await get_ledger_entry_by_reference(reference)
    
    if not ledger_entry:
        logger.error(f"Reference not found: {reference}")
        return
    
    if ledger_entry.status == "completed":
        logger.info(f"Already processed: {reference}")
        return
    
    # Update ledger entry
    ledger_entry.status = "completed"
    ledger_entry.gateway_reference = data.get("id")
    ledger_entry.gateway_response = data
    ledger_entry.receipt_number = generate_receipt_number()
    
    # Get student and guardians
    student = await get_student(ledger_entry.student_id)
    guardians = await get_student_guardians(student.id)
    
    # Send receipt to guardians
    for guardian in guardians:
        await send_payment_receipt(
            guardian=guardian,
            student=student,
            ledger_entry=ledger_entry
        )
    
    await db.commit()
    
    logger.info(f"Payment processed: {reference}, Amount: ₦{amount}")

async def handle_failed_charge(data: dict):
    """Handle failed payment."""
    
    reference = data.get("reference")
    error_message = data.get("gateway_response", "Payment failed")
    
    # Update ledger entry
    ledger_entry = await get_ledger_entry_by_reference(reference)
    
    if ledger_entry:
        ledger_entry.status = "failed"
        ledger_entry.gateway_response = data
        await db.commit()
    
    logger.info(f"Payment failed: {reference}")
```

## 5. Payment Integration (Flutterwave)

### 5.1 Overview
Flutterwave serves as an alternative payment gateway providing redundancy and additional payment options.

### 5.2 Configuration
```python
# Flutterwave configuration
FLUTTERWAVE_CONFIG = {
    "secret_key": os.getenv("FLUTTERWAVE_SECRET_KEY"),
    "public_key": os.getenv("FLUTTERWAVE_PUBLIC_KEY"),
    "encryption_key": os.getenv("FLUTTERWAVE_ENCRYPTION_KEY"),
    "base_url": "https://api.flutterwave.com/v3",
    "webhook_hash": os.getenv("FLUTTERWAVE_WEBHOOK_HASH"),
    "retry_attempts": 3,
    "timeout": 30
}
```

### 5.3 Implementation
```python
class FlutterwaveService:
    """Service for Flutterwave payment integration."""
    
    def __init__(
        self,
        secret_key: str,
        public_key: str,
        encryption_key: str,
        webhook_hash: str
    ):
        self.secret_key = secret_key
        self.public_key = public_key
        self.encryption_key = encryption_key
        self.webhook_hash = webhook_hash
        self.base_url = "https://api.flutterwave.com/v3"
        self.session = None
    
    async def initialize_payment(
        self,
        email: str,
        amount: float,
        tx_ref: str,
        customer_name: str,
        callback_url: str,
        meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Initialize payment."""
        
        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": "NGN",
            "redirect_url": callback_url,
            "payment_options": "card,bank_transfer,ussd",
            "customer": {
                "email": email,
                "name": customer_name
            },
            "customizations": {
                "title": "EduLafia School Fees",
                "description": f"Payment for {customer_name}",
                "logo": "https://edulafia.ng/logo.png"
            }
        }
        
        if meta:
            payload["meta"] = meta
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/payments",
                json=payload
            ) as response:
                result = await response.json()
                
                if result.get("status") == "success":
                    return {
                        "success": True,
                        "payment_link": result["data"]["link"],
                        "tx_ref": tx_ref
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def verify_transaction(
        self,
        transaction_id: str
    ) -> Dict[str, Any]:
        """Verify transaction by ID."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/transactions/{transaction_id}/verify"
            ) as response:
                result = await response.json()
                
                if result.get("status") == "success":
                    data = result["data"]
                    return {
                        "success": True,
                        "tx_ref": data["tx_ref"],
                        "amount": data["amount"],
                        "status": data["status"],
                        "currency": data["currency"],
                        "customer": data["customer"],
                        "created_at": data["created_at"]
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("message")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_webhook_signature(
        self,
        signature: str,
        payload: bytes
    ) -> bool:
        """Verify Flutterwave webhook signature."""
        
        computed_hash = hmac.new(
            self.webhook_hash.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(computed_hash, signature)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.secret_key}",
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

## 6. Payment Integration (Remita)

### 6.1 Overview
Remita integration for government and public school payments where Remita is the mandated payment channel.

### 6.2 Configuration
```python
# Remita configuration
REMITA_CONFIG = {
    "merchant_id": os.getenv("REMITA_MERCHANT_ID"),
    "api_key": os.getenv("REMITA_API_KEY"),
    "service_type_id": os.getenv("REMITA_SERVICE_TYPE_ID"),
    "base_url": "https://api.remita.net/v3",
    "payment_url": "https://remita.net/rmi/v3",
    "api_hash": os.getenv("REMITA_API_HASH")
}
```

### 6.3 Implementation
```python
class RemitaService:
    """Service for Remita payment integration."""
    
    def __init__(
        self,
        merchant_id: str,
        api_key: str,
        service_type_id: str,
        api_hash: str
    ):
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.service_type_id = service_type_id
        self.api_hash = api_hash
        self.base_url = "https://api.remita.net/v3"
        self.payment_url = "https://remita.net/rmi/v3"
        self.session = None
    
    def generate_payment_url(
        self,
        payment_id: str,
        amount: float,
        payer_name: str,
        payer_email: str,
        description: str
    ) -> str:
        """Generate Remita payment URL."""
        
        # Generate RRR (Remita Retrieval Reference)
        rrr = self.generate_rrr(payment_id, amount)
        
        # Build payment URL
        payment_url = (
            f"{self.payment_url}/{self.merchant_id}/{rrr}/{amount}/{description}"
        )
        
        return payment_url
    
    def generate_rrr(self, payment_id: str, amount: float) -> str:
        """Generate Remita Retrieval Reference (RRR)."""
        
        import hashlib
        import time
        
        # Generate RRR based on merchant ID, payment ID, and timestamp
        timestamp = str(int(time.time()))
        data = f"{self.merchant_id}{payment_id}{amount}{timestamp}"
        rrr_hash = hashlib.sha256(data.encode()).hexdigest()[:12]
        
        return f"{self.merchant_id}{rrr_hash}"
    
    async def verify_payment(
        self,
        rrr: str
    ) -> Dict[str, Any]:
        """Verify Remita payment status."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/api/v3/transaction/status/{rrr}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "api-key": self.api_key
                }
            ) as response:
                result = await response.json()
                
                if result.get("statuscode") == "00":
                    return {
                        "success": True,
                        "rrr": rrr,
                        "amount": result.get("amount"),
                        "status": result.get("status"),
                        "transaction_date": result.get("transactiontime")
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("statusmessage", "Payment not found")
                    }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_webhook_signature(
        self,
        signature: str,
        payload: bytes
    ) -> bool:
        """Verify Remita webhook signature."""
        
        computed_hash = hmac.new(
            self.api_hash.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(computed_hash, signature)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

## 7. EMIS Integration

### 7.1 Overview
EMIS (Education Management Information System) integration for reporting attendance, enrolment, and academic data to the Federal Ministry of Education.

### 7.2 EMIS Data Format
```python
# EMIS CSV format specifications
EMIS_FORMAT = {
    "attendance": {
        "filename": "ATTENDANCE_{school_code}_{term}.csv",
        "headers": [
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "TERM",
            "ACADEMIC_YEAR",
            "CLASS",
            "TOTAL_STUDENTS",
            "MALE_STUDENTS",
            "FEMALE_STUDENTS",
            "TOTAL_ATTENDANCE_DAYS",
            "PRESENT_DAYS",
            "ABSENT_DAYS",
            "ATTENDANCE_RATE",
            "DATE_GENERATED"
        ],
        "encoding": "utf-8"
    },
    "enrolment": {
        "filename": "ENROLMENT_{school_code}_{year}.csv",
        "headers": [
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "ACADEMIC_YEAR",
            "CLASS_LEVEL",
            "TOTAL_ENROLLED",
            "MALE_ENROLLED",
            "FEMALE_ENROLLED",
            "NEW_ADMISSIONS",
            "TRANSFERS_IN",
            "TRANSFERS_OUT",
            "DATE_GENERATED"
        ]
    },
    "academic": {
        "filename": "ACADEMIC_{school_code}_{term}.csv",
        "headers": [
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "TERM",
            "ACADEMIC_YEAR",
            "CLASS_LEVEL",
            "SUBJECT",
            "TOTAL_STUDENTS",
            "STUDENTS_EXAMINED",
            "AVERAGE_SCORE",
            "PASS_RATE",
            "A1_COUNT",
            "B2_COUNT",
            "C4_COUNT",
            "D7_COUNT",
            "F9_COUNT",
            "DATE_GENERATED"
        ]
    }
}
```

### 7.3 Implementation
```python
import csv
import io
from datetime import datetime
from typing import List, Dict, Any

class EMIService:
    """Service for EMIS data export."""
    
    async def generate_attendance_report(
        self,
        school_id: UUID,
        term_id: UUID
    ) -> str:
        """Generate EMIS attendance report CSV."""
        
        # Get school info
        school = await get_school(school_id)
        term = await get_term(term_id)
        
        # Get attendance data
        attendance_data = await get_attendance_summary(school_id, term_id)
        
        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "TERM",
            "ACADEMIC_YEAR",
            "CLASS",
            "TOTAL_STUDENTS",
            "MALE_STUDENTS",
            "FEMALE_STUDENTS",
            "TOTAL_ATTENDANCE_DAYS",
            "PRESENT_DAYS",
            "ABSENT_DAYS",
            "ATTENDANCE_RATE",
            "DATE_GENERATED"
        ])
        
        # Write data rows
        for class_data in attendance_data:
            writer.writerow([
                school.code,
                school.name,
                term.name,
                term.academic_year.name,
                class_data["class_name"],
                class_data["total_students"],
                class_data["male_students"],
                class_data["female_students"],
                class_data["total_days"],
                class_data["present_days"],
                class_data["absent_days"],
                f"{class_data['attendance_rate']:.2f}",
                datetime.now().strftime("%Y-%m-%d")
            ])
        
        return output.getvalue()
    
    async def generate_enrolment_report(
        self,
        school_id: UUID,
        academic_year_id: UUID
    ) -> str:
        """Generate EMIS enrolment report CSV."""
        
        school = await get_school(school_id)
        academic_year = await get_academic_year(academic_year_id)
        
        # Get enrolment data
        enrolment_data = await get_enrolment_summary(school_id, academic_year_id)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "ACADEMIC_YEAR",
            "CLASS_LEVEL",
            "TOTAL_ENROLLED",
            "MALE_ENROLLED",
            "FEMALE_ENROLLED",
            "NEW_ADMISSIONS",
            "TRANSFERS_IN",
            "TRANSFERS_OUT",
            "DATE_GENERATED"
        ])
        
        for level_data in enrolment_data:
            writer.writerow([
                school.code,
                school.name,
                academic_year.name,
                level_data["class_level"],
                level_data["total_enrolled"],
                level_data["male_enrolled"],
                level_data["female_enrolled"],
                level_data["new_admissions"],
                level_data["transfers_in"],
                level_data["transfers_out"],
                datetime.now().strftime("%Y-%m-%d")
            ])
        
        return output.getvalue()
    
    async def generate_academic_report(
        self,
        school_id: UUID,
        term_id: UUID
    ) -> str:
        """Generate EMIS academic performance report CSV."""
        
        school = await get_school(school_id)
        term = await get_term(term_id)
        
        # Get academic data
        academic_data = await get_academic_summary(school_id, term_id)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            "SCHOOL_CODE",
            "SCHOOL_NAME",
            "TERM",
            "ACADEMIC_YEAR",
            "CLASS_LEVEL",
            "SUBJECT",
            "TOTAL_STUDENTS",
            "STUDENTS_EXAMINED",
            "AVERAGE_SCORE",
            "PASS_RATE",
            "A1_COUNT",
            "B2_COUNT",
            "C4_COUNT",
            "D7_COUNT",
            "F9_COUNT",
            "DATE_GENERATED"
        ])
        
        for subject_data in academic_data:
            writer.writerow([
                school.code,
                school.name,
                term.name,
                term.academic_year.name,
                subject_data["class_level"],
                subject_data["subject_name"],
                subject_data["total_students"],
                subject_data["students_examined"],
                f"{subject_data['average_score']:.2f}",
                f"{subject_data['pass_rate']:.2f}",
                subject_data["a1_count"],
                subject_data["b2_count"],
                subject_data["c4_count"],
                subject_data["d7_count"],
                subject_data["f9_count"],
                datetime.now().strftime("%Y-%m-%d")
            ])
        
        return output.getvalue()
    
    async def export_emis_data(
        self,
        school_id: UUID,
        term_id: UUID,
        report_type: str
    ) -> Dict[str, Any]:
        """Export EMIS data and generate downloadable file."""
        
        # Generate CSV content
        if report_type == "attendance":
            csv_content = await self.generate_attendance_report(school_id, term_id)
            filename = f"EMIS_ATTENDANCE_{school_id}_{term_id}.csv"
        elif report_type == "enrolment":
            csv_content = await self.generate_enrolment_report(school_id, term_id)
            filename = f"EMIS_ENROLMENT_{school_id}_{term_id}.csv"
        elif report_type == "academic":
            csv_content = await self.generate_academic_report(school_id, term_id)
            filename = f"EMIS_ACADEMIC_{school_id}_{term_id}.csv"
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Upload to storage
        file_url = await upload_to_storage(
            content=csv_content.encode('utf-8'),
            filename=filename,
            content_type='text/csv'
        )
        
        return {
            "success": True,
            "download_url": file_url,
            "filename": filename,
            "generated_at": datetime.now().isoformat()
        }
```

## 8. DHIS2 Integration

### 8.1 Overview
DHIS2 (District Health Information Software 2) integration for sharing school health and Sentinel surveillance data with the National Health Management Information System (NHMIS).

### 8.2 DHIS2 Data Mapping
```python
# DHIS2 data element mapping for EduLafia
DHIS2_MAPPING = {
    "school_health": {
        "data_elements": {
            "sick_bay_visits": "EDU_SBV_001",
            "referrals_made": "EDU_REF_001",
            "screenings_conducted": "EDU_SCR_001",
            "vaccinations_administered": "EDU_VAC_001",
            "mental_health_flags": "EDU_MHF_001"
        },
        "disaggregation": {
            "gender": ["male", "female"],
            "age_group": ["10-14", "15-19"],
            "class_level": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"]
        }
    },
    "sentinel_surveillance": {
        "data_elements": {
            "illness_signals": "EDU_SIG_001",
            "clusters_detected": "EDU_CLU_001",
            "alerts_generated": "EDU_ALT_001",
            "investigations_conducted": "EDU_INV_001"
        },
        "disaggregation": {
            "symptom_category": ["respiratory", "gastrointestinal", "fever", "rash"],
            "alert_tier": ["school", "lga", "state"]
        }
    },
    "attendance": {
        "data_elements": {
            "daily_attendance": "EDU_ATT_001",
            "absence_rate": "EDU_ABS_001",
            "illness_absence": "EDU_IAB_001"
        },
        "disaggregation": {
            "gender": ["male", "female"],
            "class_level": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"]
        }
    }
}
```

### 8.2 Implementation
```python
import aiohttp
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DHIS2Service:
    """Service for DHIS2 data integration."""
    
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        org_unit_id: str
    ):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.org_unit_id = org_unit_id
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with auth."""
        if self.session is None or self.session.closed:
            import base64
            auth_string = base64.b64encode(
                f"{self.username}:{self.password}".encode()
            ).decode()
            
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Basic {auth_string}",
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=60)
            )
        return self.session
    
    async def send_health_data(
        self,
        school_id: UUID,
        period: str,  # YYYYMM format
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send school health data to DHIS2."""
        
        # Map EduLafia data to DHIS2 format
        data_values = self._map_to_dhis2_format(school_id, period, data)
        
        payload = {
            "dataSet": "EDU_HEALTHDataSet",  # Configure in DHIS2
            "completeDate": datetime.now().strftime("%Y-%m-%d"),
            "period": period,
            "orgUnit": self.org_unit_id,
            "dataValues": data_values
        }
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/api/dataValueSets",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status in [200, 201]:
                    logger.info(f"DHIS2 data sent successfully for {period}")
                    return {
                        "success": True,
                        "import_response": result.get("response", {})
                    }
                else:
                    logger.error(f"DHIS2 send failed: {result}")
                    return {
                        "success": False,
                        "error": result.get("message", "Unknown error")
                    }
        
        except Exception as e:
            logger.error(f"DHIS2 exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_sentinel_data(
        self,
        school_ids: List[UUID],
        period: str,
        signals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Send Sentinel surveillance data to DHIS2."""
        
        data_values = []
        
        for signal in signals:
            # Map each signal to DHIS2 data elements
            data_values.extend(self._map_sentinel_to_dhis2(signal, period))
        
        payload = {
            "dataSet": "EDU_SentinelDataSet",
            "completeDate": datetime.now().strftime("%Y-%m-%d"),
            "period": period,
            "orgUnit": self.org_unit_id,
            "dataValues": data_values
        }
        
        session = await self._get_session()
        
        try:
            async with session.post(
                f"{self.base_url}/api/dataValueSets",
                json=payload
            ) as response:
                result = await response.json()
                
                if response.status in [200, 201]:
                    return {"success": True, "import_response": result}
                else:
                    return {"success": False, "error": result.get("message")}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _map_to_dhis2_format(
        self,
        school_id: UUID,
        period: str,
        data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Map EduLafia data to DHIS2 data values format."""
        
        data_values = []
        mapping = DHIS2_MAPPING["school_health"]["data_elements"]
        
        # Sick bay visits
        if "sick_bay_visits" in data:
            for gender, count in data["sick_bay_visits"].items():
                data_values.append({
                    "dataElement": mapping["sick_bay_visits"],
                    "period": period,
                    "orgUnit": str(school_id),
                    "value": count,
                    "categoryOptionCombo": self._get_category_combo("gender", gender)
                })
        
        # Referrals
        if "referrals" in data:
            data_values.append({
                "dataElement": mapping["referrals_made"],
                "period": period,
                "orgUnit": str(school_id),
                "value": data["referrals"]
            })
        
        # Screenings
        if "screenings" in data:
            for screening_type, count in data["screenings"].items():
                data_values.append({
                    "dataElement": mapping["screenings_conducted"],
                    "period": period,
                    "orgUnit": str(school_id),
                    "value": count,
                    "categoryOptionCombo": self._get_category_combo("screening_type", screening_type)
                })
        
        return data_values
    
    def _map_sentinel_to_dhis2(
        self,
        signal: Dict[str, Any],
        period: str
    ) -> List[Dict[str, Any]]:
        """Map Sentinel signal to DHIS2 data values."""
        
        data_values = []
        mapping = DHIS2_MAPPING["sentinel_surveillance"]["data_elements"]
        
        # Illness signals
        data_values.append({
            "dataElement": mapping["illness_signals"],
            "period": period,
            "orgUnit": signal["school_id"],
            "value": signal["affected_students"],
            "categoryOptionCombo": self._get_category_combo(
                "symptom_category", 
                signal["symptom_category"]
            )
        })
        
        # Clusters detected
        if signal.get("is_cluster"):
            data_values.append({
                "dataElement": mapping["clusters_detected"],
                "period": period,
                "orgUnit": signal["school_id"],
                "value": 1
            })
        
        # Alerts generated
        if signal.get("alert_generated"):
            data_values.append({
                "dataElement": mapping["alerts_generated"],
                "period": period,
                "orgUnit": signal["school_id"],
                "value": 1,
                "categoryOptionCombo": self._get_category_combo(
                    "alert_tier",
                    signal.get("alert_tier", "school")
                )
            })
        
        return data_values
    
    def _get_category_combo(self, category: str, value: str) -> str:
        """Get DHIS2 category option combo ID."""
        
        # This should be configured based on your DHIS2 instance
        category_combos = {
            "gender": {"male": "male_combo_id", "female": "female_combo_id"},
            "symptom_category": {
                "respiratory": "resp_combo_id",
                "gastrointestinal": "gi_combo_id",
                "fever": "fever_combo_id",
                "rash": "rash_combo_id"
            },
            "alert_tier": {
                "school": "school_tier_id",
                "lga": "lga_tier_id",
                "state": "state_tier_id"
            }
        }
        
        return category_combos.get(category, {}).get(value, "")
    
    async def verify_org_unit(
        self,
        org_unit_id: str
    ) -> Dict[str, Any]:
        """Verify organization unit exists in DHIS2."""
        
        session = await self._get_session()
        
        try:
            async with session.get(
                f"{self.base_url}/api/organisationUnits/{org_unit_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "exists": True,
                        "name": data.get("name"),
                        "code": data.get("code"),
                        "level": data.get("level")
                    }
                else:
                    return {"exists": False}
        
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
```

## 9. Integration Service Manager

### 9.1 Unified Integration Manager
```python
class IntegrationManager:
    """Central manager for all external integrations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize services
        self.termii = TermiiService(
            api_key=config["termii"]["api_key"],
            sender_id=config["termii"].get("sender_id", "EduLafia")
        )
        
        self.whatsapp = WhatsAppService(
            api_url=config["whatsapp"]["api_url"],
            phone_number_id=config["whatsapp"]["phone_number_id"],
            access_token=config["whatsapp"]["access_token"],
            app_secret=config["whatsapp"]["app_secret"]
        )
        
        self.paystack = PaystackService(
            secret_key=config["paystack"]["secret_key"],
            public_key=config["paystack"]["public_key"],
            webhook_secret=config["paystack"]["webhook_secret"]
        )
        
        self.flutterwave = FlutterwaveService(
            secret_key=config["flutterwave"]["secret_key"],
            public_key=config["flutterwave"]["public_key"],
            encryption_key=config["flutterwave"]["encryption_key"],
            webhook_hash=config["flutterwave"]["webhook_hash"]
        )
        
        self.remita = RemitaService(
            merchant_id=config["remita"]["merchant_id"],
            api_key=config["remita"]["api_key"],
            service_type_id=config["remita"]["service_type_id"],
            api_hash=config["remita"]["api_hash"]
        )
        
        self.dhis2 = DHIS2Service(
            base_url=config["dhis2"]["base_url"],
            username=config["dhis2"]["username"],
            password=config["dhis2"]["password"],
            org_unit_id=config["dhis2"]["org_unit_id"]
        )
        
        self.emis = EMIService()
    
    async def send_notification(
        self,
        channel: str,
        to: str,
        template: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send notification via specified channel."""
        
        if channel == "sms":
            return await self.termii.send_sms(to, template.format(**context))
        elif channel == "whatsapp":
            return await self.whatsapp.send_template_message(to, template)
        else:
            return {"success": False, "error": f"Unknown channel: {channel}"}
    
    async def send_parent_notification(
        self,
        guardian: Guardian,
        notification_type: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send notification to parent via preferred channel."""
        
        # Get guardian preferences
        preferences = await get_guardian_preferences(guardian.id)
        
        results = []
        
        # Try WhatsApp first
        if preferences.whatsapp_enabled and guardian.whatsapp_phone:
            result = await self.send_whatsapp_notification(
                guardian.whatsapp_phone,
                notification_type,
                context
            )
            results.append({"channel": "whatsapp", "result": result})
        
        # Fallback to SMS
        if preferences.sms_enabled and guardian.phone:
            result = await self.send_sms_notification(
                guardian.phone,
                notification_type,
                context
            )
            results.append({"channel": "sms", "result": result})
        
        # Return first successful result
        for result in results:
            if result["result"].get("success"):
                return result["result"]
        
        return {"success": False, "error": "All channels failed"}
    
    async def process_payment_webhook(
        self,
        gateway: str,
        signature: str,
        payload: bytes
    ) -> Dict[str, Any]:
        """Process payment webhook from any gateway."""
        
        if gateway == "paystack":
            if not self.paystack.verify_webhook_signature(signature, payload):
                return {"success": False, "error": "Invalid signature"}
            
            data = json.loads(payload)
            return await self.process_paystack_webhook(data)
        
        elif gateway == "flutterwave":
            if not self.flutterwave.verify_webhook_signature(signature, payload):
                return {"success": False, "error": "Invalid signature"}
            
            data = json.loads(payload)
            return await self.process_flutterwave_webhook(data)
        
        elif gateway == "remita":
            if not self.remita.verify_webhook_signature(signature, payload):
                return {"success": False, "error": "Invalid signature"}
            
            data = json.loads(payload)
            return await self.process_remita_webhook(data)
        
        else:
            return {"success": False, "error": f"Unknown gateway: {gateway}"}
    
    async def close_all(self):
        """Close all service sessions."""
        await self.termii.close()
        await self.whatsapp.close()
        await self.paystack.close()
        await self.flutterwave.close()
        await self.remita.close()
        await self.dhis2.close()
```

### 9.2 Integration Health Monitoring
```python
class IntegrationHealthMonitor:
    """Monitor health of all integrations."""
    
    def __init__(self, integration_manager: IntegrationManager):
        self.manager = integration_manager
    
    async def check_all_health(self) -> Dict[str, Any]:
        """Check health of all integrations."""
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        # Check Termii
        termii_balance = await self.manager.termii.get_balance()
        health["services"]["termii"] = {
            "status": "healthy" if termii_balance.get("success") else "unhealthy",
            "balance": termii_balance.get("balance"),
            "details": termii_balance
        }
        
        # Check Paystack
        paystack_balance = await self.manager.paystack.get_balance()
        health["services"]["paystack"] = {
            "status": "healthy" if paystack_balance.get("success") else "unhealthy",
            "details": paystack_balance
        }
        
        # Check DHIS2 connectivity
        dhis2_status = await self.manager.dhis2.verify_org_unit(
            self.manager.dhis2.org_unit_id
        )
        health["services"]["dhis2"] = {
            "status": "healthy" if dhis2_status.get("exists") else "unhealthy",
            "details": dhis2_status
        }
        
        # Calculate overall health
        healthy_count = sum(
            1 for s in health["services"].values() 
            if s["status"] == "healthy"
        )
        total_count = len(health["services"])
        
        health["overall_status"] = (
            "healthy" if healthy_count == total_count 
            else "degraded" if healthy_count > 0 
            else "unhealthy"
        )
        health["healthy_services"] = healthy_count
        health["total_services"] = total_count
        
        return health
    
    async def send_test_messages(self) -> Dict[str, Any]:
        """Send test messages to verify integrations."""
        
        test_results = {}
        
        # Test SMS
        test_phone = self.manager.config.get("test_phone")
        if test_phone:
            sms_result = await self.manager.termii.send_sms(
                test_phone,
                "EduLafia integration test message"
            )
            test_results["sms"] = sms_result
        
        # Test WhatsApp (if configured)
        if test_phone:
            whatsapp_result = await self.manager.whatsapp.send_text_message(
                test_phone,
                "EduLafia integration test message"
            )
            test_results["whatsapp"] = whatsapp_result
        
        return test_results
```

## 10. Integration Testing

### 10.1 Test Suite
```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

class TestTermiiIntegration:
    """Test Termii SMS integration."""
    
    @pytest.fixture
    def termii_service(self):
        return TermiiService(
            api_key="test_key",
            sender_id="EduLafia"
        )
    
    @pytest.mark.asyncio
    async def test_send_sms_success(self, termii_service):
        """Test successful SMS sending."""
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "status": "success",
            "message_id": "test_message_id",
            "balance": 1000
        })
        
        with patch.object(
            termii_service, 
            '_get_session',
            return_value=AsyncMock(post=AsyncMock(return_value=mock_response))
        ):
            result = await termii_service.send_sms(
                "+2348012345678",
                "Test message"
            )
        
        assert result["success"] is True
        assert result["message_id"] == "test_message_id"
    
    @pytest.mark.asyncio
    async def test_send_otp(self, termii_service):
        """Test OTP sending."""
        
        with patch.object(termii_service, 'send_sms') as mock_send:
            mock_send.return_value = {"success": True}
            
            result = await termii_service.send_otp(
                "+2348012345678",
                "123456"
            )
            
            assert result["success"] is True
            mock_send.assert_called_once()
    
    def test_format_phone_number(self, termii_service):
        """Test phone number formatting."""
        
        assert termii_service._format_phone_number("08012345678") == "2348012345678"
        assert termii_service._format_phone_number("8012345678") == "2348012345678"
        assert termii_service._format_phone_number("2348012345678") == "2348012345678"

class TestPaystackIntegration:
    """Test Paystack payment integration."""
    
    @pytest.fixture
    def paystack_service(self):
        return PaystackService(
            secret_key="test_secret",
            public_key="test_public",
            webhook_secret="test_webhook"
        )
    
    @pytest.mark.asyncio
    async def test_initialize_transaction(self, paystack_service):
        """Test transaction initialization."""
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "status": True,
            "data": {
                "authorization_url": "https://checkout.paystack.com/test",
                "reference": "test_ref",
                "access_code": "test_code"
            }
        })
        
        with patch.object(
            paystack_service,
            '_get_session',
            return_value=AsyncMock(post=AsyncMock(return_value=mock_response))
        ):
            result = await paystack_service.initialize_transaction(
                email="test@example.com",
                amount=500000,  # ₦5,000
                reference="TEST-001"
            )
        
        assert result["success"] is True
        assert "authorization_url" in result
    
    def test_verify_webhook_signature(self, paystack_service):
        """Test webhook signature verification."""
        
        payload = b'{"event": "charge.success"}'
        signature = hmac.new(
            b"test_webhook",
            payload,
            hashlib.sha512
        ).hexdigest()
        
        assert paystack_service.verify_webhook_signature(signature, payload) is True
        assert paystack_service.verify_webhook_signature("invalid", payload) is False

class TestWhatsAppIntegration:
    """Test WhatsApp integration."""
    
    @pytest.fixture
    def whatsapp_service(self):
        return WhatsAppService(
            api_url="https://graph.facebook.com/v17.0",
            phone_number_id="test_phone_id",
            access_token="test_token",
            app_secret="test_secret"
        )
    
    @pytest.mark.asyncio
    async def test_send_template_message(self, whatsapp_service):
        """Test template message sending."""
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "messages": [{"id": "test_message_id"}]
        })
        
        with patch.object(
            whatsapp_service,
            '_get_session',
            return_value=AsyncMock(post=AsyncMock(return_value=mock_response))
        ):
            result = await whatsapp_service.send_template_message(
                to="+2348012345678",
                template_name="test_template"
            )
        
        assert result["success"] is True
        assert result["message_id"] == "test_message_id"

class TestEMISIntegration:
    """Test EMIS data export."""
    
    @pytest.fixture
    def emis_service(self):
        return EMIService()
    
    @pytest.mark.asyncio
    async def test_generate_attendance_report(self, emis_service):
        """Test attendance report generation."""
        
        with patch('app.integrations.emis.get_school') as mock_get_school, \
             patch('app.integrations.emis.get_term') as mock_get_term, \
             patch('app.integrations.emis.get_attendance_summary') as mock_get_summary:
            
            mock_get_school.return_value = MagicMock(
                code="TEST001",
                name="Test School"
            )
            mock_get_term.return_value = MagicMock(
                name="First Term 2026",
                academic_year=MagicMock(name="2026/2027")
            )
            mock_get_summary.return_value = [
                {
                    "class_name": "JSS1A",
                    "total_students": 30,
                    "male_students": 15,
                    "female_students": 15,
                    "total_days": 20,
                    "present_days": 18,
                    "absent_days": 2,
                    "attendance_rate": 90.0
                }
            ]
            
            csv_content = await emis_service.generate_attendance_report(
                school_id=uuid4(),
                term_id=uuid4()
            )
            
            assert "SCHOOL_CODE" in csv_content
            assert "TEST001" in csv_content
            assert "JSS1A" in csv_content

class TestDHIS2Integration:
    """Test DHIS2 integration."""
    
    @pytest.fixture
    def dhis2_service(self):
        return DHIS2Service(
            base_url="https://dhis2.example.com",
            username="admin",
            password="district",
            org_unit_id="test_org_unit"
        )
    
    @pytest.mark.asyncio
    async def test_verify_org_unit(self, dhis2_service):
        """Test organization unit verification."""
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "name": "Test School",
            "code": "TEST001",
            "level": 5
        })
        
        with patch.object(
            dhis2_service,
            '_get_session',
            return_value=AsyncMock(get=AsyncMock(return_value=mock_response))
        ):
            result = await dhis2_service.verify_org_unit("test_org_unit")
        
        assert result["exists"] is True
        assert result["name"] == "Test School"
```

## 11. Configuration and Environment Variables

### 11.1 Environment Variables
```env
# Termii Configuration
TERMII_API_KEY=your_termii_api_key
TERMII_SENDER_ID=EduLafia

# WhatsApp Configuration
WHATSAPP_API_URL=https://graph.facebook.com/v17.0
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token
WHATSAPP_APP_SECRET=your_app_secret

# Paystack Configuration
PAYSTACK_SECRET_KEY=your_secret_key
PAYSTACK_PUBLIC_KEY=your_public_key
PAYSTACK_WEBHOOK_SECRET=your_webhook_secret

# Flutterwave Configuration
FLUTTERWAVE_SECRET_KEY=your_secret_key
FLUTTERWAVE_PUBLIC_KEY=your_public_key
FLUTTERWAVE_ENCRYPTION_KEY=your_encryption_key
FLUTTERWAVE_WEBHOOK_HASH=your_webhook_hash

# Remita Configuration
REMITA_MERCHANT_ID=your_merchant_id
REMITA_API_KEY=your_api_key
REMITA_SERVICE_TYPE_ID=your_service_type_id
REMITA_API_HASH=your_api_hash

# DHIS2 Configuration
DHIS2_BASE_URL=https://dhis2.example.com
DHIS2_USERNAME=admin
DHIS2_PASSWORD=district
DHIS2_ORG_UNIT_ID=your_org_unit_id
```

### 11.2 Docker Configuration
```yaml
# docker-compose.yml additions for integrations
services:
  backend:
    environment:
      # Termii
      - TERMII_API_KEY=${TERMII_API_KEY}
      - TERMII_SENDER_ID=${TERMII_SENDER_ID}
      
      # WhatsApp
      - WHATSAPP_API_URL=${WHATSAPP_API_URL}
      - WHATSAPP_PHONE_NUMBER_ID=${WHATSAPP_PHONE_NUMBER_ID}
      - WHATSAPP_ACCESS_TOKEN=${WHATSAPP_ACCESS_TOKEN}
      - WHATSAPP_WEBHOOK_VERIFY_TOKEN=${WHATSAPP_WEBHOOK_VERIFY_TOKEN}
      - WHATSAPP_APP_SECRET=${WHATSAPP_APP_SECRET}
      
      # Paystack
      - PAYSTACK_SECRET_KEY=${PAYSTACK_SECRET_KEY}
      - PAYSTACK_PUBLIC_KEY=${PAYSTACK_PUBLIC_KEY}
      - PAYSTACK_WEBHOOK_SECRET=${PAYSTACK_WEBHOOK_SECRET}
      
      # Flutterwave
      - FLUTTERWAVE_SECRET_KEY=${FLUTTERWAVE_SECRET_KEY}
      - FLUTTERWAVE_PUBLIC_KEY=${FLUTTERWAVE_PUBLIC_KEY}
      - FLUTTERWAVE_ENCRYPTION_KEY=${FLUTTERWAVE_ENCRYPTION_KEY}
      - FLUTTERWAVE_WEBHOOK_HASH=${FLUTTERWAVE_WEBHOOK_HASH}
      
      # Remita
      - REMITA_MERCHANT_ID=${REMITA_MERCHANT_ID}
      - REMITA_API_KEY=${REMITA_API_KEY}
      - REMITA_SERVICE_TYPE_ID=${REMITA_SERVICE_TYPE_ID}
      - REMITA_API_HASH=${REMITA_API_HASH}
      
      # DHIS2
      - DHIS2_BASE_URL=${DHIS2_BASE_URL}
      - DHIS2_USERNAME=${DHIS2_USERNAME}
      - DHIS2_PASSWORD=${DHIS2_PASSWORD}
      - DHIS2_ORG_UNIT_ID=${DHIS2_ORG_UNIT_ID}
```

## 12. Best Practices

### 12.1 Error Handling
1. Always wrap external API calls in try-except blocks
2. Log errors with sufficient context
3. Implement retry logic with exponential backoff
4. Use circuit breaker pattern for failing services
5. Provide fallback mechanisms where possible

### 12.2 Security
1. Never log API keys or sensitive data
2. Store credentials in environment variables
3. Rotate API keys regularly
4. Validate all webhook signatures
5. Use HTTPS for all external communications

### 12.3 Performance
1. Use connection pooling for HTTP clients
2. Implement caching for frequently accessed data
3. Use async/await for non-blocking operations
4. Batch operations where possible
5. Monitor API rate limits

### 12.4 Monitoring
1. Log all integration calls (success and failure)
2. Track response times
3. Monitor API quotas and limits
4. Set up alerts for integration failures
5. Regular health checks

---

*This integration specification provides comprehensive guidance for implementing all external service integrations for the EduLafia platform.*

---

**End of Integration Specifications**