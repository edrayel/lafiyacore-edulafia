from __future__ import annotations
"""Library repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.library.models import Book, BookLending


class BookRepository:
    """Repository for book database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Book:
        """Create a new book."""
        book = Book(**data)
        self.db.add(book)
        await self.db.flush()
        await self.db.refresh(book)
        return book

    async def get_by_id(self, book_id: UUID) -> Book | None:
        """Get a book by ID."""
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, book_id: UUID, school_id: UUID) -> Book | None:
        """Get a book by ID scoped to school."""
        stmt = select(Book).where(
            Book.id == book_id,
            Book.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[Book], int]:
        """List books for a school with pagination."""
        stmt = select(Book).where(
            Book.school_id == school_id
        )

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Book.title)

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def update(self, book: Book, data: dict) -> Book:
        """Update a book."""
        for key, value in data.items():
            if value is not None:
                setattr(book, key, value)
        await self.db.flush()
        await self.db.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        """Delete a book."""
        await self.db.delete(book)
        await self.db.flush()


class BookLendingRepository:
    """Repository for book lending database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> BookLending:
        """Create a new book lending."""
        lending = BookLending(**data)
        self.db.add(lending)
        await self.db.flush()
        await self.db.refresh(lending)
        return lending

    async def get_by_id(self, lending_id: UUID) -> BookLending | None:
        """Get a book lending by ID."""
        stmt = select(BookLending).where(BookLending.id == lending_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_by_student(self, student_id: UUID) -> Sequence[BookLending]:
        """Get active lendings for a student."""
        stmt = select(BookLending).where(
            BookLending.student_id == student_id,
            BookLending.status == "active",
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_school(self, school_id: UUID) -> Sequence[BookLending]:
        """List all lendings for a school (joined with books)."""
        stmt = (
            select(BookLending)
            .join(Book, BookLending.book_id == Book.id)
            .where(Book.school_id == school_id)
            .order_by(BookLending.lend_date.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, lending: BookLending, data: dict) -> BookLending:
        """Update a book lending."""
        for key, value in data.items():
            if value is not None:
                setattr(lending, key, value)
        await self.db.flush()
        await self.db.refresh(lending)
        return lending
