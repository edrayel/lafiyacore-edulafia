"""Services for messaging business logic operations."""

from uuid import UUID

from edulafia.modules.messaging.repository import MessageRepository
from edulafia.modules.messaging.schemas import (
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)


class MessagingService:
    """Service for messaging business logic."""

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def send_message(
        self,
        data: MessageCreate,
        sender_id: UUID,
        school_id: UUID,
    ) -> MessageResponse:
        """Send a new message."""
        # Verify receiver belongs to the same school
        # In a real scenario, this would check User table directly.
        from sqlalchemy import select
        from edulafia.modules.auth.models import User
        
        stmt = select(User.school_id).where(User.id == data.receiver_id)
        result = await self.repository.db.execute(stmt)
        receiver_school_id = result.scalar_one_or_none()
        
        if not receiver_school_id or receiver_school_id != school_id:
            raise ValueError("Receiver not found or belongs to a different school")

        message_data = {
            "sender_id": sender_id,
            "receiver_id": data.receiver_id,
            "content": data.content,
        }

        message = await self.repository.create(message_data)
        return MessageResponse.model_validate(message)

    async def get_conversations(self, user_id: UUID) -> list[ConversationResponse]:
        """Get all conversations for a user."""
        latest_messages = await self.repository.get_conversations(user_id)
        
        conversations = []
        for msg in latest_messages:
            partner_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
            unread_count = await self.repository.get_unread_count(user_id, partner_id)
            
            conversations.append(
                ConversationResponse(
                    user_id=partner_id,
                    last_message=MessageResponse.model_validate(msg),
                    unread_count=unread_count,
                )
            )
            
        return conversations

    async def get_messages(
        self,
        user_id: UUID,
        partner_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[MessageResponse]:
        """Get messages between the current user and a partner."""
        messages = await self.repository.get_messages_between(
            user_id_1=user_id,
            user_id_2=partner_id,
            limit=limit,
            offset=offset,
        )
        return [MessageResponse.model_validate(msg) for msg in messages]
