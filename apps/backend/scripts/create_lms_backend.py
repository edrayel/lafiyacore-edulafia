import os

base_dir = "/Users/edrayel/GitHub/edward_rajah/lafiyacore-edulafia/apps/backend/src/edulafia/modules/lms"
os.makedirs(f"{base_dir}/api", exist_ok=True)

models_code = '''"""LMS and Homework models."""

import uuid
from datetime import datetime, date

from sqlalchemy import DateTime, ForeignKey, String, Text, func, Date, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edulafia.database import Base


class Assignment(Base):
    """Assignment model for the LMS module."""

    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="assignment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Assignment(id={self.id}, title={self.title})>"


class Submission(Base):
    """Submission model for assignments."""

    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    assignment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
    )
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    grade: Mapped[float | None] = mapped_column(Float, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    assignment: Mapped["Assignment"] = relationship(
        "Assignment",
        back_populates="submissions",
    )

    def __repr__(self) -> str:
        return f"<Submission(id={self.id}, assignment_id={self.assignment_id}, student_id={self.student_id})>"
'''

schemas_code = '''"""LMS Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssignmentBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    due_date: datetime
    class_id: UUID
    subject_id: UUID
    file_path: str | None = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = Field(None, max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    class_id: UUID | None = None
    subject_id: UUID | None = None
    file_path: str | None = None


class AssignmentResponse(AssignmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class SubmissionBase(BaseModel):
    assignment_id: UUID
    student_id: UUID
    file_path: str | None = None
    grade: float | None = None
    feedback: str | None = None


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_path: str | None = None
    grade: float | None = None
    feedback: str | None = None


class SubmissionResponse(SubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
'''

repository_code = '''"""LMS Repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.lms.models import Assignment, Submission


class LMSRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Assignments
    async def create_assignment(self, data: dict) -> Assignment:
        assignment = Assignment(**data)
        self.db.add(assignment)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def get_assignment_by_id(self, assignment_id: UUID) -> Assignment | None:
        stmt = select(Assignment).where(Assignment.id == assignment_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_assignments(self, class_id: UUID | None = None, subject_id: UUID | None = None) -> Sequence[Assignment]:
        stmt = select(Assignment)
        if class_id:
            stmt = stmt.where(Assignment.class_id == class_id)
        if subject_id:
            stmt = stmt.where(Assignment.subject_id == subject_id)
        stmt = stmt.order_by(Assignment.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_assignment(self, assignment: Assignment, data: dict) -> Assignment:
        for key, value in data.items():
            if value is not None:
                setattr(assignment, key, value)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def delete_assignment(self, assignment: Assignment) -> None:
        await self.db.delete(assignment)
        await self.db.flush()

    # Submissions
    async def create_submission(self, data: dict) -> Submission:
        submission = Submission(**data)
        self.db.add(submission)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def get_submission_by_id(self, submission_id: UUID) -> Submission | None:
        stmt = select(Submission).where(Submission.id == submission_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_submissions(self, assignment_id: UUID) -> Sequence[Submission]:
        stmt = select(Submission).where(Submission.assignment_id == assignment_id).order_by(Submission.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_submission(self, submission: Submission, data: dict) -> Submission:
        for key, value in data.items():
            if value is not None:
                setattr(submission, key, value)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def delete_submission(self, submission: Submission) -> None:
        await self.db.delete(submission)
        await self.db.flush()
'''

service_code = '''"""LMS Service."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.lms.models import Assignment, Submission
from edulafia.modules.lms.repository import LMSRepository
from edulafia.modules.lms.schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    SubmissionCreate,
    SubmissionUpdate,
)


class LMSService:
    def __init__(self, repository: LMSRepository):
        self.repository = repository

    # Assignments
    async def create_assignment(self, data: AssignmentCreate) -> Assignment:
        return await self.repository.create_assignment(data.model_dump())

    async def get_assignment(self, assignment_id: UUID) -> Assignment | None:
        return await self.repository.get_assignment_by_id(assignment_id)

    async def list_assignments(self, class_id: UUID | None = None, subject_id: UUID | None = None) -> Sequence[Assignment]:
        return await self.repository.list_assignments(class_id=class_id, subject_id=subject_id)

    async def update_assignment(self, assignment_id: UUID, data: AssignmentUpdate) -> Assignment | None:
        assignment = await self.get_assignment(assignment_id)
        if not assignment:
            return None
        return await self.repository.update_assignment(assignment, data.model_dump(exclude_unset=True))

    async def delete_assignment(self, assignment_id: UUID) -> bool:
        assignment = await self.get_assignment(assignment_id)
        if not assignment:
            return False
        await self.repository.delete_assignment(assignment)
        return True

    # Submissions
    async def create_submission(self, data: SubmissionCreate) -> Submission:
        return await self.repository.create_submission(data.model_dump())

    async def get_submission(self, submission_id: UUID) -> Submission | None:
        return await self.repository.get_submission_by_id(submission_id)

    async def list_submissions(self, assignment_id: UUID) -> Sequence[Submission]:
        return await self.repository.list_submissions(assignment_id)

    async def update_submission(self, submission_id: UUID, data: SubmissionUpdate) -> Submission | None:
        submission = await self.get_submission(submission_id)
        if not submission:
            return None
        return await self.repository.update_submission(submission, data.model_dump(exclude_unset=True))

    async def delete_submission(self, submission_id: UUID) -> bool:
        submission = await self.get_submission(submission_id)
        if not submission:
            return False
        await self.repository.delete_submission(submission)
        return True
'''

router_code = '''"""LMS Router endpoints."""

import os
import shutil
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.lms.repository import LMSRepository
from edulafia.modules.lms.schemas import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentUpdate,
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdate,
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
    return await service.create_assignment(data)


@router.get(
    "/assignments",
    response_model=list[AssignmentResponse],
    summary="List assignments",
)
async def list_assignments(
    current_user: CurrentUser,
    class_id: UUID | None = Query(None),
    subject_id: UUID | None = Query(None),
    service: LMSService = Depends(get_lms_service),
) -> list[AssignmentResponse]:
    return await service.list_assignments(class_id=class_id, subject_id=subject_id)


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
    assignment = await service.get_assignment(assignment_id)
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
    data: AssignmentUpdate,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> AssignmentResponse:
    assignment = await service.update_assignment(assignment_id, data)
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
    deleted = await service.delete_assignment(assignment_id)
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
    return await service.create_submission(data)


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
    return await service.list_submissions(assignment_id)


@router.patch(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse,
    summary="Update a submission",
)
async def update_submission(
    submission_id: UUID,
    data: SubmissionUpdate,
    current_user: CurrentUser,
    service: LMSService = Depends(get_lms_service),
) -> SubmissionResponse:
    submission = await service.update_submission(submission_id, data)
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
    deleted = await service.delete_submission(submission_id)
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
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
        
    return {"file_path": file_path, "filename": file.filename}
'''

init_code = '"""LMS module."""\n'
api_init_code = '"""LMS API module."""\n'

with open(f"{base_dir}/models.py", "w") as f:
    f.write(models_code)

with open(f"{base_dir}/schemas.py", "w") as f:
    f.write(schemas_code)

with open(f"{base_dir}/repository.py", "w") as f:
    f.write(repository_code)

with open(f"{base_dir}/service.py", "w") as f:
    f.write(service_code)

with open(f"{base_dir}/api/router.py", "w") as f:
    f.write(router_code)

with open(f"{base_dir}/__init__.py", "w") as f:
    f.write(init_code)

with open(f"{base_dir}/api/__init__.py", "w") as f:
    f.write(api_init_code)

print("Backend files created successfully.")
