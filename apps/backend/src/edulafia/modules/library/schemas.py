"""Library Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    """Base schema for book."""

    school_id: UUID = Field(..., description="ID of the school")
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str | None = Field(None, max_length=20)
    category: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1)
    available_quantity: int = Field(default=1, ge=0)
    shelf_location: str | None = Field(None, max_length=100)


class BookCreate(BookBase):
    """Schema for creating a book."""


class BookUpdate(BaseModel):
    """Schema for updating a book."""

    model_config = ConfigDict(from_attributes=True)

    title: str | None = Field(None, max_length=255)
    author: str | None = Field(None, max_length=255)
    isbn: str | None = Field(None, max_length=20)
    category: str | None = Field(None, max_length=100)
    quantity: int | None = Field(None, ge=1)
    available_quantity: int | None = Field(None, ge=0)
    shelf_location: str | None = Field(None, max_length=100)


class BookResponse(BaseModel):
    """Schema for book response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    title: str
    author: str
    isbn: str | None = None
    category: str
    quantity: int
    available_quantity: int
    shelf_location: str | None = None
    created_at: datetime
    updated_at: datetime


class BookLendingBase(BaseModel):
    """Base schema for book lending."""

    book_id: UUID = Field(..., description="ID of the book")
    student_id: UUID = Field(..., description="ID of the student")
    lend_date: date = Field(...)
    due_date: date = Field(...)
    status: str = Field(default="active")


class BookLendingCreate(BookLendingBase):
    """Schema for creating a book lending."""


class BookLendingUpdate(BaseModel):
    """Schema for updating a book lending."""

    model_config = ConfigDict(from_attributes=True)

    return_date: date | None = None
    status: str | None = None


class BookLendingResponse(BaseModel):
    """Schema for book lending response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    book_id: UUID
    student_id: UUID
    lend_date: date
    due_date: date
    return_date: date | None = None
    status: str
    created_at: datetime
    updated_at: datetime
