"""Add staff schema: staff, staff_class_assignments, timetables, timetable_entries, teacher_attendance, staff_communications, communication_recipients.

Revision ID: 006_staff_schema
Revises: 005_health_schema
Create Date: 2026-03-30 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "006_staff_schema"
down_revision: str | None = "005_health_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create staff schema tables."""

    # Staff table
    op.create_table(
        "staff",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("staff_id", sa.String(50), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("whatsapp_phone", sa.String(20), nullable=True),
        sa.Column("date_of_birth", sa.Date, nullable=True),
        sa.Column("gender", sa.String(10), nullable=False),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("photo_url", sa.String(500), nullable=True),
        sa.Column("role", sa.String(50), nullable=False, comment="teacher, nurse, bursar, admin"),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("qualifications", postgresql.JSONB, nullable=True),
        sa.Column("subjects", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=True),
        sa.Column("employment_type", sa.String(20), nullable=False, server_default="permanent"),
        sa.Column("employment_date", sa.Date, nullable=True),
        sa.Column("exit_date", sa.Date, nullable=True),
        sa.Column("exit_reason", sa.String(100), nullable=True),
        sa.Column("salary", sa.Numeric(12, 2), nullable=True),
        sa.Column("bank_details", postgresql.JSONB, nullable=True),
        sa.Column("next_of_kin", postgresql.JSONB, nullable=True),
        sa.Column("emergency_contact", postgresql.JSONB, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.UniqueConstraint("school_id", "staff_id", name="uq_staff_school_staff_id"),
    )

    # Staff class assignments table
    op.create_table(
        "staff_class_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("subjects.id"), nullable=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("academic_years.id"), nullable=False),
        sa.Column("term_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("terms.id"), nullable=True),
        sa.Column("assignment_type", sa.String(20), nullable=False, server_default="regular"),
        sa.Column("is_form_teacher", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("staff_id", "class_id", "subject_id", "academic_year_id", name="uq_staff_class_subject_year"),
    )

    # Timetables table
    op.create_table(
        "timetables",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("academic_years.id"), nullable=False),
        sa.Column("term_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("terms.id"), nullable=False),
        sa.Column("effective_from", sa.Date, nullable=False),
        sa.Column("effective_to", sa.Date, nullable=True),
        sa.Column("is_published", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("version_number", sa.Integer, nullable=False, server_default="1"),
        sa.Column("is_draft", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("class_id", "academic_year_id", "term_id", "version_number", name="uq_timetable_class_year_term_version"),
    )

    # Timetable entries table
    op.create_table(
        "timetable_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("timetable_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("timetables.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("day_of_week", sa.Integer, nullable=False, comment="1=Monday, 7=Sunday"),
        sa.Column("period_number", sa.Integer, nullable=False),
        sa.Column("start_time", sa.Time, nullable=False),
        sa.Column("end_time", sa.Time, nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("subjects.id"), nullable=False),
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id"), nullable=False, index=True),
        sa.Column("room_number", sa.String(50), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("is_break", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("timetable_id", "day_of_week", "period_number", name="uq_timetable_entry_period"),
    )

    # Teacher attendance table
    op.create_table(
        "teacher_attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.Date, nullable=False, index=True),
        sa.Column("check_in_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("check_out_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("check_in_method", sa.String(20), nullable=True),
        sa.Column("late_minutes", sa.Integer, nullable=True),
        sa.Column("early_departure_minutes", sa.Integer, nullable=True),
        sa.Column("reason_code", sa.String(50), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("recorded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("staff_id", "date", name="uq_teacher_attendance_staff_date"),
    )

    # Staff communications table
    op.create_table(
        "staff_communications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("sender_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("communication_type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("target_audience", postgresql.JSONB, nullable=True),
        sa.Column("channels", postgresql.ARRAY(sa.String), nullable=False, server_default="{}"),
        sa.Column("requires_acknowledgement", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Communication recipients table
    op.create_table(
        "communication_recipients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("communication_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff_communications.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="sent"),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("communication_id", "staff_id", name="uq_communication_recipient"),
    )

    # Additional indexes for performance
    op.create_index("idx_staff_role", "staff", ["school_id", "role"])
    op.create_index("idx_staff_status", "staff", ["school_id", "status"])
    op.create_index("idx_staff_employment_type", "staff", ["school_id", "employment_type"])


def downgrade() -> None:
    """Drop staff schema tables."""
    op.drop_table("communication_recipients")
    op.drop_table("staff_communications")
    op.drop_table("teacher_attendance")
    op.drop_table("timetable_entries")
    op.drop_table("timetables")
    op.drop_table("staff_class_assignments")
    op.drop_table("staff")
