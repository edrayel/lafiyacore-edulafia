"""Student service for business logic operations."""

from datetime import date
import uuid
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from edulafia.modules.students.exceptions import (
    DuplicateAdmissionNumberError,
    DuplicateNINError,
    StudentArchivedError,
    StudentNotFoundError,
)
from edulafia.modules.students.models import StudentDocument
from edulafia.modules.students.repository import StudentDocumentRepository, StudentRepository
from edulafia.modules.students.schemas import (
    StudentCreate,
    StudentDocumentCreate,
    StudentFilters,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)


class StudentService:
    """Service for student business logic."""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def create(
        self,
        data: StudentCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> StudentResponse:
        """Create a new student."""
        # Check for duplicate admission number
        if await self.repository.exists_by_admission(data.admission_number, school_id):
            raise DuplicateAdmissionNumberError(data.admission_number)

        # Check for duplicate NIN if provided
        if data.nin and await self.repository.exists_by_nin(data.nin):
            raise DuplicateNINError(data.nin)

        # Prepare data
        student_data = data.model_dump()
        student_data["school_id"] = school_id
        student_data["created_by"] = user_id
        student_data["updated_by"] = user_id

        # Create student
        student = await self.repository.create(student_data)
        return StudentResponse.model_validate(student)

    async def get_by_id(
        self,
        student_id: UUID,
        school_id: UUID,
    ) -> StudentResponse | None:
        """Get a student by ID."""
        student = await self.repository.get_by_id(student_id, school_id)
        if student:
            return StudentResponse.model_validate(student)
        return None

    async def list_students(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
        filters: StudentFilters | None = None,
    ) -> StudentListResponse:
        """List students with pagination and filters."""
        students, total = await self.repository.list(
            school_id=school_id,
            page=page,
            per_page=per_page,
            filters=filters,
        )

        pages = (total + per_page - 1) // per_page

        return StudentListResponse(
            items=[StudentResponse.model_validate(s) for s in students],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

    async def update(
        self,
        student_id: UUID,
        data: StudentUpdate,
        school_id: UUID,
        user_id: UUID,
    ) -> StudentResponse:
        """Update a student."""
        student = await self.repository.get_by_id(student_id, school_id)
        if not student:
            raise StudentNotFoundError(str(student_id))

        if student.deleted_at is not None:
            raise StudentArchivedError(str(student_id))

        # Prepare update data (exclude None values)
        update_data = data.model_dump(exclude_none=True)
        update_data["updated_by"] = user_id

        updated_student = await self.repository.update(student, update_data)
        return StudentResponse.model_validate(updated_student)

    async def archive(
        self,
        student_id: UUID,
        school_id: UUID,
        user_id: UUID,
    ) -> StudentResponse:
        """Archive (soft delete) a student."""
        student = await self.repository.get_by_id(student_id, school_id)
        if not student:
            raise StudentNotFoundError(str(student_id))

        if student.deleted_at is not None:
            raise StudentArchivedError(str(student_id))

        archived_student = await self.repository.soft_delete(student, user_id)
        return StudentResponse.model_validate(archived_student)

    async def bulk_create(
        self,
        data: list[StudentCreate],
        school_id: UUID,
        user_id: UUID,
    ) -> dict:
        """Bulk create students in a single transaction."""
        results = {"success": [], "errors": []}
        for item in data:
            try:
                student = await self.create(item, school_id, user_id)
                results["success"].append(student)
            except Exception as e:
                results["errors"].append({
                    "admission_number": item.admission_number,
                    "error": str(e)
                })
        return results

    async def generate_admission_number(
        self,
        school_id: UUID,
        school_code: str = "EDU",
    ) -> str:
        """Generate a unique admission number for a school."""
        sequence = await self.repository.get_next_admission_number(school_id)
        year = date.today().year
        return f"{school_code}/{year}/{sequence:04d}"

    async def import_from_csv(
        self,
        file: UploadFile,
        class_id: UUID | None,
        school_id: UUID,
        user_id: UUID,
    ) -> dict:
        """Import students from CSV file."""
        import csv
        from io import StringIO

        _MAX_ROWS = 500

        # Read CSV file
        contents = await file.read()
        csv_text = contents.decode("utf-8")
        csv_reader = csv.DictReader(StringIO(csv_text))

        rows = list(csv_reader)
        if len(rows) > _MAX_ROWS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"CSV exceeds maximum of {_MAX_ROWS} rows ({len(rows)} provided)",
            )

        # Prepare results
        results = {"success": [], "errors": []}

        # Process each row
        for i, row in enumerate(rows, start=2):
            try:
                # Parse row data
                student_data = {
                    "first_name": row.get("first_name", "").strip(),
                    "last_name": row.get("last_name", "").strip(),
                    "date_of_birth": row.get("date_of_birth", "").strip(),
                    "gender": row.get("gender", "male").strip().lower(),
                    "admission_number": row.get("admission_number", "").strip(),
                    "nin": row.get("nin", "").strip() or None,
                    "class_id": class_id,
                    "guardian_name": row.get("guardian_name", "").strip(),
                    "guardian_phone": row.get("guardian_phone", "").strip(),
                    "guardian_email": row.get("guardian_email", "").strip() or None,
                    "admission_date": row.get("admission_date", date.today().isoformat()),
                    "status": "active",
                }
                
                # Validate required fields
                if not student_data["first_name"] or not student_data["last_name"]:
                    raise ValueError("First name and last name are required")
                
                # Generate admission number if not provided
                if not student_data["admission_number"]:
                    student_data["admission_number"] = await self.generate_admission_number(school_id)
                
                # Create student
                schema = StudentCreate(**student_data)
                student = await self.create(schema, school_id, user_id)
                results["success"].append(student)
                
            except Exception as e:
                results["errors"].append({
                    "row": i,
                    "data": dict(row),
                    "error": str(e)
                })
        
        return results


class StudentDocumentService:
    """Service for student document business logic."""

    def __init__(self, repository: StudentDocumentRepository):
        self.repository = repository

    async def get_student_documents(
        self,
        db: AsyncSession,
        student_id: uuid.UUID,
    ) -> list[StudentDocument]:
        """Get all documents for a student.
        
        Args:
            db: Database session
            student_id: ID of the student
            
        Returns:
            List of student documents
        """
        return await self.repository.get_by_student(db, student_id)

    async def add_document(
        self,
        db: AsyncSession,
        student_id: uuid.UUID,
        document_in: StudentDocumentCreate,
        uploaded_by: uuid.UUID | None = None,
    ) -> StudentDocument:
        """Add a new document to a student's profile.
        
        Args:
            db: Database session
            student_id: ID of the student
            document_in: Document creation data
            uploaded_by: User ID who uploaded the document
            
        Returns:
            Created document
        """
        doc_data = document_in.model_dump()
        return await self.repository.create(
            db, 
            student_id, 
            doc_data,
            uploaded_by=uploaded_by
        )

    async def delete_document(
        self,
        db: AsyncSession,
        document_id: uuid.UUID,
    ) -> bool:
        """Delete a student document.
        
        Args:
            db: Database session
            document_id: ID of the document
            
        Returns:
            True if deleted
            
        Raises:
            ValueError if document not found
        """
        deleted = await self.repository.delete(db, document_id)
        if not deleted:
            raise ValueError(f"Document with id {document_id} not found")
        return True
