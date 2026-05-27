"""Parent notification service."""

from datetime import timezone, datetime
from uuid import UUID

from edulafia.modules.parent.exceptions import (
    NotificationDisabledError,
)
from edulafia.modules.parent.repository import (
    NotificationPreferenceRepository,
    ParentNotificationRepository,
)
from edulafia.modules.parent.schemas import (
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
    ParentNotificationResponse,
)

# Maximum non-urgent notifications per day
MAX_NON_URGENT_PER_DAY = 3


class ParentNotificationService:
    """Service for parent notifications."""

    def __init__(
        self,
        notification_repo: ParentNotificationRepository,
        preference_repo: NotificationPreferenceRepository,
    ):
        self.notification_repo = notification_repo
        self.preference_repo = preference_repo

    def _is_quiet_hours(self) -> bool:
        """Check if current time is during quiet hours (9PM-6AM)."""
        current_hour = datetime.now(timezone.utc).hour
        return current_hour >= 21 or current_hour < 6

    def _is_urgent(self, notification_type: str) -> bool:
        """Check if notification type is urgent."""
        urgent_types = ["health_emergency", "safety_alert", "health_notification", "critical"]
        return notification_type.lower() in urgent_types

    async def send_notification(
        self,
        guardian_id: UUID,
        student_id: UUID | None,
        notification_type: str,
        title: str,
        message: str,
        channel: str = "whatsapp",
        priority: str = "normal",
        metadata: dict | None = None,
        send_whatsapp_func=None,
        send_sms_func=None,
    ) -> ParentNotificationResponse:
        """Send notification to parent."""
        is_urgent = self._is_urgent(notification_type)

        # Check quiet hours for non-urgent
        if not is_urgent and self._is_quiet_hours():
            # Schedule for later instead of failing
            priority = "low"

        # Check daily limit for non-urgent
        if not is_urgent:
            today_count = await self.notification_repo.count_today(
                guardian_id, is_urgent=False
            )
            if today_count >= MAX_NON_URGENT_PER_DAY:
                # Lower priority but still send
                priority = "low"

        # Create notification record
        notification_data = {
            "guardian_id": guardian_id,
            "student_id": student_id,
            "notification_type": notification_type,
            "title": title,
            "message": message,
            "channel": channel,
            "priority": priority,
            "status": "pending",
            "notification_metadata": metadata,
        }
        notification = await self.notification_repo.create(notification_data)

        # Send via channel
        try:
            from edulafia.core.twilio_client import TwilioClient
            
            # Use SMS provider for SMS/WhatsApp currently
            if channel in ["whatsapp", "sms"]:
                guardian = await self.preference_repo.get_guardian_phone(guardian_id)
                if not guardian or not guardian.phone_number:
                    raise Exception("No phone number found for guardian")
                
                await TwilioClient.send_sms(guardian.phone_number, message)
                notification.status = "sent"
                notification.sent_at = datetime.now(timezone.utc)
            else:
                notification.status = "sent"
                notification.sent_at = datetime.now(timezone.utc)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Notification delivery failed: {e}")
            notification.status = "failed"

        return ParentNotificationResponse.model_validate(notification)

    async def send_absence_notification(
        self,
        guardian_id: UUID,
        student_id: UUID,
        student_name: str,
        absence_date: str,
        reason: str | None = None,
        send_whatsapp_func=None,
        send_sms_func=None,
    ) -> ParentNotificationResponse:
        """Send absence notification to parent."""
        message = f"Your child {student_name} was absent on {absence_date}."
        if reason:
            message += f" Reason: {reason}"

        return await self.send_notification(
            guardian_id=guardian_id,
            student_id=student_id,
            notification_type="absence",
            title="Absence Notification",
            message=message,
            channel="whatsapp",
            priority="high" if not reason else "normal",
            metadata={"student_name": student_name, "absence_date": absence_date, "reason": reason},
            send_whatsapp_func=send_whatsapp_func,
            send_sms_func=send_sms_func,
        )

    async def send_health_notification(
        self,
        guardian_id: UUID,
        student_id: UUID,
        student_name: str,
        visit_type: str,
        details: str,
        send_whatsapp_func=None,
        send_sms_func=None,
    ) -> ParentNotificationResponse:
        """Send health notification to parent."""
        message = f"Health update for {student_name}: {visit_type}. {details}"

        return await self.send_notification(
            guardian_id=guardian_id,
            student_id=student_id,
            notification_type="health_notification",
            title="Health Notification",
            message=message,
            channel="whatsapp",
            priority="urgent",
            metadata={"student_name": student_name, "visit_type": visit_type},
            send_whatsapp_func=send_whatsapp_func,
            send_sms_func=send_sms_func,
        )

    async def send_payment_receipt(
        self,
        guardian_id: UUID,
        student_id: UUID,
        student_name: str,
        amount: float,
        receipt_number: str,
        send_whatsapp_func=None,
    ) -> ParentNotificationResponse:
        """Send payment receipt to parent."""
        message = (
            f"Payment received for {student_name}. "
            f"Amount: ₦{amount:,.2f}. "
            f"Receipt: {receipt_number}"
        )

        return await self.send_notification(
            guardian_id=guardian_id,
            student_id=student_id,
            notification_type="payment_receipt",
            title="Payment Receipt",
            message=message,
            channel="whatsapp",
            priority="normal",
            metadata={"amount": amount, "receipt_number": receipt_number},
            send_whatsapp_func=send_whatsapp_func,
        )

    async def list_notifications(
        self,
        guardian_id: UUID,
        notification_type: str | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List notifications for guardian."""
        notifications, total = await self.notification_repo.list(
            guardian_id=guardian_id,
            notification_type=notification_type,
            status=status,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [ParentNotificationResponse.model_validate(n) for n in notifications],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def mark_as_read(
        self,
        notification_id: UUID,
        guardian_id: UUID,
    ) -> ParentNotificationResponse:
        """Mark notification as read."""
        notification = await self.notification_repo.mark_as_read(notification_id)
        return ParentNotificationResponse.model_validate(notification)

    async def get_preferences(
        self,
        guardian_id: UUID,
    ) -> list[NotificationPreferenceResponse]:
        """Get notification preferences for guardian."""
        preferences = await self.preference_repo.get_or_create_default(guardian_id)
        return [NotificationPreferenceResponse.model_validate(p) for p in preferences]

    async def update_preference(
        self,
        guardian_id: UUID,
        data: NotificationPreferenceUpdate,
    ) -> NotificationPreferenceResponse:
        """Update notification preference."""
        # Cannot disable urgent notifications
        if not data.is_enabled and self._is_urgent(data.notification_type):
            raise NotificationDisabledError(data.notification_type)

        preference = await self.preference_repo.update(
            guardian_id=guardian_id,
            notification_type=data.notification_type,
            channel=data.channel,
            is_enabled=data.is_enabled,
        )

        return NotificationPreferenceResponse.model_validate(preference)
