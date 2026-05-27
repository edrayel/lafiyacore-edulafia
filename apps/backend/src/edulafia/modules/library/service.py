"""Library service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.library.repository import BookLendingRepository, BookRepository
from edulafia.modules.library.schemas import (
    BookCreate,
    BookLendingCreate,
    BookLendingResponse,
    BookResponse,
    BookUpdate,
)


class BookService:
    """Service for book business logic."""

    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create(self, data: BookCreate, user_id: UUID) -> BookResponse:
        """Create a new book."""
        book_data = data.model_dump()
        book = await self.repository.create(book_data)
        return BookResponse.model_validate(book)

    async def get_by_id(self, book_id: UUID, school_id: UUID) -> BookResponse | None:
        """Get a book by ID."""
        book = await self.repository.get_by_id_and_school(book_id, school_id)
        if book:
            return BookResponse.model_validate(book)
        return None

    async def list_by_school(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List books for a school with pagination."""
        books, total = await self.repository.list_by_school(
            school_id, page=page, per_page=per_page,
        )

        return {
            "items": [BookResponse.model_validate(b) for b in books],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def update(self, book_id: UUID, data: BookUpdate, school_id: UUID, user_id: UUID) -> BookResponse:
        """Update a book."""
        book = await self.repository.get_by_id_and_school(book_id, school_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_book = await self.repository.update(book, update_data)
        return BookResponse.model_validate(updated_book)

    async def delete(self, book_id: UUID, school_id: UUID) -> None:
        """Delete a book."""
        book = await self.repository.get_by_id_and_school(book_id, school_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")

        await self.repository.delete(book)


class BookLendingService:
    """Service for book lending business logic."""

    def __init__(self, repository: BookLendingRepository, book_repository: BookRepository):
        self.repository = repository
        self.book_repository = book_repository

    async def create(self, data: BookLendingCreate, user_id: UUID) -> BookLendingResponse:
        """Create a new book lending."""
        book = await self.book_repository.get_by_id(data.book_id)
        if not book:
            raise ValueError(f"Book {data.book_id} not found")
        if book.available_quantity <= 0:
            raise ValueError("No copies available for lending")

        lending_data = data.model_dump()
        lending = await self.repository.create(lending_data)

        await self.book_repository.update(book, {"available_quantity": book.available_quantity - 1})

        return BookLendingResponse.model_validate(lending)

    async def get_by_id(self, lending_id: UUID) -> BookLendingResponse | None:
        """Get a book lending by ID."""
        lending = await self.repository.get_by_id(lending_id)
        if lending:
            return BookLendingResponse.model_validate(lending)
        return None

    async def get_active_by_student(self, student_id: UUID) -> Sequence[BookLendingResponse]:
        """Get active lendings for a student."""
        lendings = await self.repository.get_active_by_student(student_id)
        return [BookLendingResponse.model_validate(l) for l in lendings]

    async def return_book(self, lending_id: UUID) -> BookLendingResponse:
        """Return a borrowed book."""
        lending = await self.repository.get_by_id(lending_id)
        if not lending:
            raise ValueError(f"Book lending {lending_id} not found")
        if lending.status == "returned":
            raise ValueError("Book already returned")

        update_data = {"status": "returned", "return_date": lending.return_date}
        updated_lending = await self.repository.update(lending, update_data)

        book = await self.book_repository.get_by_id(lending.book_id)
        if book:
            await self.book_repository.update(book, {"available_quantity": book.available_quantity + 1})

        return BookLendingResponse.model_validate(updated_lending)
