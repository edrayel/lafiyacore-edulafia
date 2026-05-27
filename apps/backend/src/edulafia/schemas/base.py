"""Base Pydantic schemas for common patterns."""

from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

T = TypeVar("T")


class BaseModel(PydanticBaseModel):
    """Base model with ORM mode enabled."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class IDMixin(BaseModel):
    """Mixin that adds id and timestamp fields."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""

    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    detail: str
    code: str | None = None
    field: str | None = None


class MessageResponse(BaseModel):
    """Standard message response schema."""

    message: str
