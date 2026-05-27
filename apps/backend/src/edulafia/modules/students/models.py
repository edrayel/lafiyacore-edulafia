"""Student SQLAlchemy model."""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edulafia.core.encryption import EncryptedString
from edulafia.database import Base
from edulafia.modules.guardians.student_guardian import StudentGuardian


class StudentDocument(Base):
    """Student document model representing uploaded files attached to a student profile."""

    __tablename__ = "student_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="E.g., admission_letter, birth_certificate, medical_record, transfer_letter, other"
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    file_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
    file_size_bytes: Mapped[int | None] = mapped_column(
        nullable=True,
    )
    mime_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    
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
    
    # Audit
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="documents"
    )

    def __repr__(self) -> str:
        return f"<StudentDocument(id={self.id}, type={self.document_type}, title={self.title})>"


class Student(Base):
    """Student model representing a student in the school management system."""

    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("school_id", "admission_number", name="uq_student_admission_number"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id"),
        nullable=True,
        index=True,
    )

    # Required fields
    admission_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    gender: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        index=True,
    )
    admission_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Optional fields
    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    nationality: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Nigerian",
    )
    state_of_origin: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    lga: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Health information
    blood_group: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )
    genotype: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )
    chronic_conditions: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )
    allergies: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )

    # Identification
    nin: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
        unique=True,
    )

    # Transfer information
    previous_school: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    graduation_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    transfer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Audit fields
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Relationships
    guardians: Mapped[list["StudentGuardian"]] = relationship(
        "StudentGuardian",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    documents: Mapped[list["StudentDocument"]] = relationship(
        "StudentDocument",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name}, admission={self.admission_number})>"
