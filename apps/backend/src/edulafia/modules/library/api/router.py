"""Library API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.library.repository import BookLendingRepository, BookRepository
from edulafia.modules.library.schemas import (
    BookCreate,
    BookLendingCreate,
    BookLendingResponse,
    BookResponse,
    BookUpdate,
)
from edulafia.modules.library.service import BookLendingService, BookService

router = APIRouter(prefix="/library", tags=["Library"])


def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    """Dependency to get BookService."""
    repository = BookRepository(db)
    return BookService(repository)


def get_lending_service(db: AsyncSession = Depends(get_db)) -> BookLendingService:
    """Dependency to get BookLendingService."""
    book_repo = BookRepository(db)
    lending_repo = BookLendingRepository(db)
    return BookLendingService(lending_repo, book_repo)


@router.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
)
async def create_book(
    data: BookCreate,
    current_user: CurrentUser,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Create a new book record."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
)
async def get_book(
    book_id: UUID,
    current_user: CurrentUser,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Get a book by ID."""
    book = await service.get_by_id(
        book_id=book_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.get(
    "/books",
    response_model=Page[BookResponse],
    summary="List books",
)
async def list_books(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    service: BookService = Depends(get_book_service),
) -> dict:
    """List books for the school with pagination."""
    return await service.list_by_school(
        school_id=UUID(current_user["school_id"]),
        page=pag.page,
        per_page=pag.per_page,
    )


@router.patch(
    "/books/{book_id}",
    response_model=BookResponse,
    summary="Update a book",
)
async def update_book(
    book_id: UUID,
    data: BookUpdate,
    current_user: CurrentUser,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Update a book."""
    try:
        return await service.update(
            book_id=book_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/books/{book_id}",
    summary="Delete a book",
)
async def delete_book(
    book_id: UUID,
    current_user: CurrentUser,
    service: BookService = Depends(get_book_service),
) -> dict:
    """Delete a book."""
    try:
        await service.delete(
            book_id=book_id,
            school_id=UUID(current_user["school_id"]),
        )
        return {"message": "Book deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/lend",
    response_model=BookLendingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lend a book",
)
async def lend_book(
    data: BookLendingCreate,
    current_user: CurrentUser,
    service: BookLendingService = Depends(get_lending_service),
) -> BookLendingResponse:
    """Lend a book to a student."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/lend/{lending_id}/return",
    response_model=BookLendingResponse,
    summary="Return a book",
)
async def return_book(
    lending_id: UUID,
    current_user: CurrentUser,
    service: BookLendingService = Depends(get_lending_service),
) -> BookLendingResponse:
    """Return a borrowed book."""
    try:
        return await service.return_book(lending_id=lending_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
