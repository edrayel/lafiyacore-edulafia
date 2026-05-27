"""Messaging API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.messaging.repository import MessageRepository
from edulafia.modules.messaging.schemas import (
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from edulafia.modules.messaging.service import MessagingService

router = APIRouter(prefix="/messaging", tags=["Messaging"])


def get_messaging_service(db: AsyncSession = Depends(get_db)) -> MessagingService:
    """Dependency to get MessagingService."""
    repository = MessageRepository(db)
    return MessagingService(repository)


@router.post(
    "/send",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a new message",
)
async def send_message(
    data: MessageCreate,
    current_user: CurrentUser,
    service: MessagingService = Depends(get_messaging_service),
) -> MessageResponse:
    """Send a message to another user."""
    return await service.send_message(
        data=data,
        sender_id=UUID(current_user["sub"]),
        school_id=UUID(current_user["school_id"]),
    )


@router.get(
    "/conversations",
    response_model=list[ConversationResponse],
    summary="Get all conversations for current user",
)
async def get_conversations(
    current_user: CurrentUser,
    service: MessagingService = Depends(get_messaging_service),
) -> list[ConversationResponse]:
    """Get list of conversations with the latest message and unread count."""
    return await service.get_conversations(
        user_id=UUID(current_user["sub"]),
    )


@router.get(
    "/conversations/{partner_id}",
    response_model=list[MessageResponse],
    summary="Get messages between current user and a partner",
)
async def get_messages(
    partner_id: UUID,
    current_user: CurrentUser,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MessagingService = Depends(get_messaging_service),
) -> list[MessageResponse]:
    """Get full message history between current user and a partner."""
    return await service.get_messages(
        user_id=UUID(current_user["sub"]),
        partner_id=partner_id,
        limit=limit,
        offset=offset,
    )
