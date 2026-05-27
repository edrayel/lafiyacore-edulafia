"""LMS Router endpoints."""

import os
import shutil
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.lms.repository import LMSRepository
from edulafia.modules.lms.schemas import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentUpdateRequest,
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdateRequest,
)
from edulafia.modules.lms.service import LMSService

router = APIRouter(prefix="/lms", tags=["LMS"])

UPLOAD_DIR = "/app/uploads/assignments/"


def get_lms_service(db: AsyncSession = Depends(get_db)) -> LMSService:
    repository = LMSRepository(db)
    return LMSService(repository)


@router.post(
    "/assignments",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an assignment",
)
async def create_assignment(
    data: AssignmentCreate,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> AssignmentResponse:
    return await service.create_assignment(data, UUID(current_user["school_id"]))

@router.get(
    "/assignments",
    response_model=Page[AssignmentResponse],
    summary="List assignments",
)
async def list_assignments(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    class_id: UUID | None = Query(None),
    subject_id: UUID | None = Query(None),
    service: LMSService = Depends(get_lms_service),
) -> dict:
    return await service.list_assignments(
        school_id=UUID(current_user["school_id"]),
        class_id=class_id,
        subject_id=subject_id,
        page=pag.page,
        per_page=pag.per_page,
    )

@router.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Get an assignment",
)
async def get_assignment(
    assignment_id: UUID,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> AssignmentResponse:
    assignment = await service.get_assignment(assignment_id, UUID(current_user["school_id"]))
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment

@router.patch(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Update an assignment",
)
async def update_assignment(
    assignment_id: UUID,
    data: AssignmentUpdateRequest,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> AssignmentResponse:
    assignment = await service.update_assignment(assignment_id, data, UUID(current_user["school_id"]))
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment

@router.delete(
    "/assignments/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an assignment",
)
async def delete_assignment(
    assignment_id: UUID,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> None:
    deleted = await service.delete_assignment(assignment_id, UUID(current_user["school_id"]))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

@router.post(
    "/assignments/{assignment_id}/submissions",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a submission",
)
async def create_submission(
    assignment_id: UUID,
    data: SubmissionCreate,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> SubmissionResponse:
    if data.assignment_id != assignment_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignment ID mismatch")
    return await service.create_submission(data, UUID(current_user["school_id"]))

@router.get(
    "/assignments/{assignment_id}/submissions",
    response_model=list[SubmissionResponse],
    summary="List submissions for an assignment",
)
async def list_submissions(
    assignment_id: UUID,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> list[SubmissionResponse]:
    return await service.list_submissions(assignment_id, UUID(current_user["school_id"]))

@router.patch(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse,
    summary="Update a submission",
)
async def update_submission(
    submission_id: UUID,
    data: SubmissionUpdateRequest,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> SubmissionResponse:
    submission = await service.update_submission(submission_id, data, UUID(current_user["school_id"]))
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission

@router.delete(
    "/submissions/{submission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a submission",
)
async def delete_submission(
    submission_id: UUID,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> None:
    deleted = await service.delete_submission(submission_id, UUID(current_user["school_id"]))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")


@router.post(
    "/uploads/assignments",
    summary="Upload an assignment file",
)
async def upload_assignment_file(
    current_user: CurrentUser,
    file: UploadFile = File(...),
) -> dict:
    import uuid
    
    ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".zip"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")
        
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File extension {ext} not allowed")

    # Read to check size
    content = bytearray()
    while chunk := await file.read(1024 * 1024):
        content.extend(chunk)
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
            
    # Generate safe random filename
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    
    # Upload to S3
    from edulafia.core.s3_client import S3StorageClient
    
    file_key = f"schools/{current_user['school_id']}/assignments/{safe_filename}"
    file_url = await S3StorageClient.upload_file(
        file_bytes=content,
        file_key=file_key,
        content_type=file.content_type or "application/octet-stream"
    )
        
    return {"file_path": file_url, "filename": file.filename}