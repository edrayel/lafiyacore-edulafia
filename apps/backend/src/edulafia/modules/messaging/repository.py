from __future__ import annotations
"""Repository for messaging database operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, or_, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from edulafia.modules.messaging.models import Message


class MessageRepository:
    """Repository for message database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Message:
        """Create a new message."""
        message = Message(**data)
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_conversations(self, user_id: UUID) -> Sequence[Message]:
        """
        Get latest messages for all conversations of a user.
        This is a simplified approach fetching the latest message per conversation.
        """
        # Create an alias to join message to itself for finding latest
        m1 = aliased(Message)
        m2 = aliased(Message)

        # Get all messages where user is sender or receiver
        stmt = select(Message).where(
            or_(
                Message.sender_id == user_id,
                Message.receiver_id == user_id
            ),
            Message.deleted_at.is_(None)
        ).order_by(desc(Message.created_at))

        result = await self.db.execute(stmt)
        messages = result.scalars().all()
        
        # Deduplicate to get only the latest message per conversation partner
        conversations = []
        seen_partners = set()
        
        for msg in messages:
            partner_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
            if partner_id not in seen_partners:
                seen_partners.add(partner_id)
                conversations.append(msg)
                
        return conversations

    async def get_messages_between(
        self, user_id_1: UUID, user_id_2: UUID, limit: int = 50, offset: int = 0
    ) -> Sequence[Message]:
        """Get messages between two users."""
        stmt = select(Message).where(
            or_(
                (Message.sender_id == user_id_1) & (Message.receiver_id == user_id_2),
                (Message.sender_id == user_id_2) & (Message.receiver_id == user_id_1),
            ),
            Message.deleted_at.is_(None)
        ).order_by(desc(Message.created_at)).limit(limit).offset(offset)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_unread_count(self, user_id: UUID, partner_id: UUID) -> int:
        """Get count of unread messages from a specific partner."""
        stmt = select(func.count()).select_from(Message).where(
            Message.receiver_id == user_id,
            Message.sender_id == partner_id,
            Message.read_at.is_(None),
            Message.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0
