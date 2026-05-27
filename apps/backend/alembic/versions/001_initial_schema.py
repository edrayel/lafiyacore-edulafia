"""Initial schema: schools, classes, users, students, guardians.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-03-27 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create initial schema with all core tables."""

    # Schools table (dependency for students)
    op.create_table(
        "schools",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(20), nullable=False, unique=True),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("lga", sa.String(100), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Classes table
    op.create_table(
        "classes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("section", sa.String(50), nullable=True),
        sa.Column("level", sa.String(50), nullable=True),
        sa.Column("academic_year", sa.String(20), nullable=False),
        sa.Column("capacity", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mfa_enabled", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("mfa_secret", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Students table
    op.create_table(
        "students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("classes.id"), nullable=True, index=True),
        sa.Column("admission_number", sa.String(50), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("date_of_birth", sa.Date, nullable=False),
        sa.Column("gender", sa.String(10), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active", index=True),
        sa.Column("admission_date", sa.Date, nullable=False),
        sa.Column("nationality", sa.String(100), nullable=False, server_default="Nigerian"),
        sa.Column("state_of_origin", sa.String(100), nullable=True),
        sa.Column("lga", sa.String(100), nullable=True),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("photo_url", sa.String(500), nullable=True),
        sa.Column("blood_group", sa.String(5), nullable=True),
        sa.Column("genotype", sa.String(5), nullable=True),
        sa.Column("chronic_conditions", sa.Text, nullable=True),
        sa.Column("allergies", sa.Text, nullable=True),
        sa.Column("nin", sa.String(11), nullable=True, unique=True),
        sa.Column("previous_school", sa.String(255), nullable=True),
        sa.Column("graduation_date", sa.Date, nullable=True),
        sa.Column("transfer_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.UniqueConstraint("school_id", "admission_number", name="uq_student_admission_number"),
    )

    # Guardians table
    op.create_table(
        "guardians",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("phone_number", sa.String(20), nullable=False),
        sa.Column("relationship_type", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("whatsapp_number", sa.String(20), nullable=True),
        sa.Column("occupation", sa.String(100), nullable=True),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("nin", sa.String(11), nullable=True, unique=True),
        sa.Column("portal_access", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Student-Guardian relationship table
    op.create_table(
        "student_guardians",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("guardian_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("is_primary", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_emergency_contact", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("can_pickup", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Create indexes for performance
    op.create_index("idx_student_school_status", "students", ["school_id", "status"])
    op.create_index("idx_student_class", "students", ["class_id", "status"])
    op.create_index("idx_guardian_school", "guardians", ["school_id"])
    op.create_index("idx_student_guardian_student", "student_guardians", ["student_id"])
    op.create_index("idx_student_guardian_guardian", "student_guardians", ["guardian_id"])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("student_guardians")
    op.drop_table("guardians")
    op.drop_table("students")
    op.drop_table("users")
    op.drop_table("classes")
    op.drop_table("schools")
