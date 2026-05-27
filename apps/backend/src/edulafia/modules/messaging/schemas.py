"""Messaging Pydantic schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MessageBase(BaseModel):
    """Base schema for messages."""
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message content",
    )


class MessageCreate(MessageBase):
    """Schema for sending a new message."""
    
    receiver_id: UUID = Field(
        ...,
        description="ID of the user receiving the message",
    )


class MessageResponse(MessageBase):
    """Schema for message response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    read_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ConversationResponse(BaseModel):
    """Schema for a conversation summary."""
    
    user_id: UUID
    last_message: MessageResponse
    unread_count: int = 0
