"""Student API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.students.exceptions import (
    DuplicateAdmissionNumberError,
    DuplicateNINError,
    StudentArchivedError,
    StudentNotFoundError,
)
from edulafia.modules.students.repository import StudentRepository
from edulafia.modules.students.schemas import (
    StudentCreate,
    StudentFilters,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from edulafia.modules.students.service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    """Dependency to get StudentService."""
    repository = StudentRepository(db)
    return StudentService(repository)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
)
async def create_student(
    data: StudentCreate,
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Create a new student record."""
    try:
        return await service.create(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateAdmissionNumberError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except DuplicateNINError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=StudentListResponse,
    summary="List students",
)
async def list_students(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    class_id: UUID | None = Query(None),
    status: str | None = Query(None),
    gender: str | None = Query(None),
    search: str | None = Query(None),
    service: StudentService = Depends(get_student_service),
) -> StudentListResponse:
    """List students with optional filters and pagination."""
    filters = StudentFilters(
        class_id=class_id,
        status=status,
        gender=gender,
        search=search,
    )
    return await service.list_students(
        school_id=UUID(current_user["school_id"]),
        page=page,
        per_page=per_page,
        filters=filters,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by ID",
)
async def get_student(
    student_id: UUID,
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Get a student's details by ID."""
    student = await service.get_by_id(
        student_id=student_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student",
)
async def update_student(
    student_id: UUID,
    data: StudentUpdate,
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Update a student's information."""
    try:
        return await service.update(
            student_id=student_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    except StudentArchivedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify an archived student",
        )


@router.delete(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Archive a student",
)
async def archive_student(
    student_id: UUID,
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Archive a student (soft delete)."""
    try:
        return await service.archive(
            student_id=student_id,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    except StudentArchivedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already archived",
        )


@router.post(
    "/generate-admission-number",
    summary="Generate admission number",
)
async def generate_admission_number(
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> dict:
    """Generate a unique admission number for the school."""
    admission_number = await service.generate_admission_number(
        school_id=UUID(current_user["school_id"]),
    )
    return {"admission_number": admission_number}


@router.post(
    "/bulk",
    summary="Bulk create students",
)
async def bulk_create_students(
    data: list[StudentCreate],
    current_user: CurrentUser,
    service: StudentService = Depends(get_student_service),
) -> dict:
    """Bulk create student records."""
    return await service.bulk_create(
        data=data,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
    )


@router.post(
    "/import",
    summary="Import students from CSV",
)
async def import_students(
    current_user: CurrentUser,
    file: UploadFile = File(...),
    class_id: UUID | None = Query(None),
    service: StudentService = Depends(get_student_service),
) -> dict:
    """Import students from CSV file."""
    _validate_upload(file, allowed_extensions={".csv"})
    return await service.import_from_csv(
        file=file,
        class_id=class_id,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
    )


def _validate_upload(file: UploadFile, allowed_extensions: set[str] | None = None) -> None:
    MAX_FILE_SIZE = 10 * 1024 * 1024

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename missing")

    if allowed_extensions:
        import os
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File extension {ext} not allowed. Allowed: {', '.join(sorted(allowed_extensions))}",
            )

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {MAX_FILE_SIZE // (1024 * 1024)} MB",
        )
