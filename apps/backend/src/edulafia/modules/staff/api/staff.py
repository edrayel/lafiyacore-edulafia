"""Staff API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.staff.exceptions import (
    AssignmentNotFoundError,
    DuplicateAssignmentError,
    DuplicateStaffIdError,
    FormTeacherAlreadyAssignedError,
    MaxLoadExceededError,
    StaffNotFoundError,
)
from edulafia.modules.staff.repository import StaffAssignmentRepository, StaffRepository
from edulafia.modules.staff.schemas import (
    StaffAssignmentCreate,
    StaffAssignmentResponse,
    StaffCreate,
    StaffDeactivate,
    StaffResponse,
    StaffUpdate,
)
from edulafia.modules.staff.service import AssignmentService, StaffService

router = APIRouter(prefix="/staff", tags=["Staff"])


def get_staff_service(db: AsyncSession = Depends(get_db)) -> StaffService:
    """Dependency to get StaffService."""
    repository = StaffRepository(db)
    return StaffService(repository)


def get_assignment_service(db: AsyncSession = Depends(get_db)) -> AssignmentService:
    """Dependency to get AssignmentService."""
    assignment_repo = StaffAssignmentRepository(db)
    staff_repo = StaffRepository(db)
    return AssignmentService(assignment_repo, staff_repo)


# Staff Profile Endpoints

@router.post(
    "",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create staff member",
)
async def create_staff(
    data: StaffCreate,
    current_user: CurrentUser,
    service: StaffService = Depends(get_staff_service),
) -> StaffResponse:
    """Create a new staff member."""
    try:
        return await service.create_staff(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateStaffIdError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "",
    response_model=dict,
    summary="List staff",
)
async def list_staff(
    current_user: CurrentUser,
    role: str | None = Query(None),
    department: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    service: StaffService = Depends(get_staff_service),
) -> dict:
    """List staff with filters."""
    return await service.list_staff(
        school_id=UUID(current_user["school_id"]),
        role=role,
        department=department,
        status=status,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{staff_id}",
    response_model=StaffResponse,
    summary="Get staff by ID",
)
async def get_staff(
    staff_id: UUID,
    current_user: CurrentUser,
    service: StaffService = Depends(get_staff_service),
) -> StaffResponse:
    """Get staff details by ID."""
    try:
        return await service.get_staff(
            staff_id=staff_id,
            school_id=UUID(current_user["school_id"]),
        )
    except StaffNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")


@router.patch(
    "/{staff_id}",
    response_model=StaffResponse,
    summary="Update staff",
)
async def update_staff(
    staff_id: UUID,
    data: StaffUpdate,
    current_user: CurrentUser,
    service: StaffService = Depends(get_staff_service),
) -> StaffResponse:
    """Update staff information."""
    try:
        # Check if self-update
        is_self = str(staff_id) == current_user.get("staff_id")

        return await service.update_staff(
            staff_id=staff_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
            is_self=is_self,
        )
    except StaffNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")


@router.post(
    "/{staff_id}/deactivate",
    response_model=StaffResponse,
    summary="Deactivate staff",
)
async def deactivate_staff(
    staff_id: UUID,
    data: StaffDeactivate,
    current_user: CurrentUser,
    service: StaffService = Depends(get_staff_service),
) -> StaffResponse:
    """Deactivate a staff member."""
    try:
        return await service.deactivate_staff(
            staff_id=staff_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
        )
    except StaffNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")


@router.post(
    "/{staff_id}/documents",
    summary="Upload a staff document (e.g., CV, Credentials)",
)
async def upload_staff_document(
    staff_id: UUID,
    current_user: CurrentUser,
    document_type: str = Query(..., description="e.g., 'cv', 'degree', 'certification'"),
    file: UploadFile = File(...),
    service: StaffService = Depends(get_staff_service),
) -> dict:
    """Upload a staff document."""
    import logging
    logger = logging.getLogger(__name__)

    ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    import os
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File extension {ext} not allowed")

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    from edulafia.core.s3_client import S3StorageClient
    import uuid
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    file_key = f"schools/{current_user['school_id']}/staff/{staff_id}/{safe_filename}"
    
    file_url = await S3StorageClient.upload_file(
        file_bytes=file_content,
        file_key=file_key,
        content_type=file.content_type or "application/octet-stream"
    )
    
    file_size_kb = len(file_content) / 1024
    
    logger.info(f"Staff {staff_id} document '{document_type}' uploaded ({file_size_kb:.2f} KB) -> {file_url}")
    
    # We update the documents dictionary
    staff = await service.get_staff(staff_id, UUID(current_user["school_id"]))
    docs = staff.documents or {}
    docs[document_type] = file_url
    
    await service.update_staff(
        staff_id=staff_id,
        data=StaffUpdate(documents=docs),
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
        is_self=(str(staff_id) == current_user.get("staff_id"))
    )
    
    return {
        "status": "success",
        "message": f"Document {document_type} uploaded successfully",
        "data": {
            "document_type": document_type,
            "url": file_url
        }
    }


@router.delete(
    "/{staff_id}/documents/{document_type}",
    summary="Delete a staff document",
)
async def delete_staff_document(
    staff_id: UUID,
    document_type: str,
    current_user: CurrentUser,
    service: StaffService = Depends(get_staff_service),
) -> dict:
    """Delete a staff document."""
    staff = await service.get_staff(staff_id, UUID(current_user["school_id"]))
    docs = staff.documents or {}
    
    if document_type in docs:
        del docs[document_type]
        await service.update_staff(
            staff_id=staff_id,
            data=StaffUpdate(documents=docs),
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
            is_self=(str(staff_id) == current_user.get("staff_id"))
        )
        
    return {"status": "success", "message": f"Document {document_type} deleted successfully"}


# Assignment Endpoints

@router.post(
    "/assignments",
    response_model=StaffAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create staff assignment",
)
async def create_assignment(
    data: StaffAssignmentCreate,
    current_user: CurrentUser,
    service: AssignmentService = Depends(get_assignment_service),
) -> StaffAssignmentResponse:
    """Create a staff assignment."""
    try:
        return await service.create_assignment(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateAssignmentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except FormTeacherAlreadyAssignedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MaxLoadExceededError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/assignments",
    response_model=Page[StaffAssignmentResponse],
    summary="List assignments",
)
async def list_assignments(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    staff_id: UUID | None = Query(None),
    class_id: UUID | None = Query(None),
    academic_year_id: UUID | None = Query(None),
    service: AssignmentService = Depends(get_assignment_service),
) -> dict:
    """List staff assignments with pagination."""
    return await service.list_assignments(
        staff_id=staff_id,
        class_id=class_id,
        academic_year_id=academic_year_id,
        school_id=UUID(current_user["school_id"]),
        page=pag.page,
        per_page=pag.per_page,
    )


@router.delete(
    "/assignments/{assignment_id}",
    summary="Delete assignment",
)
async def delete_assignment(
    assignment_id: UUID,
    current_user: CurrentUser,
    service: AssignmentService = Depends(get_assignment_service),
) -> dict:
    """Delete a staff assignment."""
    try:
        success = await service.delete_assignment(
            assignment_id,
            school_id=UUID(current_user["school_id"])
        )
        return {"success": success}
    except AssignmentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")


@router.post(
    "/assignments/bulk",
    response_model=dict,
    summary="Bulk create assignments",
)
async def bulk_create_assignments(
    assignments: list[StaffAssignmentCreate],
    current_user: CurrentUser,
    service: AssignmentService = Depends(get_assignment_service),
) -> dict:
    """Bulk create staff assignments."""
    return await service.bulk_create_assignments(
        assignments=assignments,
        user_id=UUID(current_user["sub"]),
    )
