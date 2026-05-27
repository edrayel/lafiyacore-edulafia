"""Attendance schema: attendance_records, attendance_patterns, attendance_notifications, attendance_configurations.

Revision ID: 003_attendance_schema
Revises: 002_academics_schema
Create Date: 2026-03-28 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "003_attendance_schema"
down_revision: str | None = "002_academics_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create attendance schema tables."""

    # Attendance records table
    op.create_table(
        "attendance_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("classes.id"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.Date, nullable=False, index=True),
        sa.Column("period", sa.Integer, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, index=True, comment="present, absent, late, excused"),
        sa.Column("reason_code", sa.String(50), nullable=True, comment="sick, family, unknown, excused, suspended"),
        sa.Column("symptom_codes", postgresql.ARRAY(sa.String), nullable=True, comment="Array of symptom codes for sick absences"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("recorded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("edited_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("edited_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("edit_reason", sa.Text, nullable=True),
        sa.Column("device_id", sa.String(255), nullable=True),
        sa.Column("sync_status", sa.String(20), nullable=False, server_default="synced"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("student_id", "date", "deleted_at", name="uq_attendance_student_date"),
    )

    # Attendance patterns table
    op.create_table(
        "attendance_patterns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("classes.id"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("pattern_type", sa.String(50), nullable=False, comment="chronic_absence, same_day_absence, illness_cluster"),
        sa.Column("pattern_details", postgresql.JSONB, nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("severity", sa.String(20), nullable=False, comment="low, medium, high, critical"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active", comment="active, acknowledged, resolved, false_positive"),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Attendance notifications table
    op.create_table(
        "attendance_notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("guardian_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("notification_type", sa.String(50), nullable=False, comment="daily_absence, consecutive_absence, weekly_summary"),
        sa.Column("channel", sa.String(20), nullable=False, comment="whatsapp, sms, both"),
        sa.Column("message_content", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending", comment="pending, sent, delivered, failed"),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("retry_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Attendance configurations table
    op.create_table(
        "attendance_configurations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("marking_method", sa.String(50), nullable=False, server_default="dropdown", comment="dropdown, swipe, qr_code"),
        sa.Column("require_reason_for_absence", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("require_symptoms_for_sick", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("edit_window_hours", sa.Integer, nullable=False, server_default="24"),
        sa.Column("notification_delay_minutes", sa.Integer, nullable=False, server_default="30"),
        sa.Column("consecutive_absence_alert_days", sa.Integer, nullable=False, server_default="3"),
        sa.Column("chronic_absence_threshold_percent", sa.Numeric(5, 2), nullable=False, server_default="20.0"),
        sa.Column("notification_enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Indexes for performance
    op.create_index("idx_attendance_record_date", "attendance_records", ["school_id", "date"])
    op.create_index("idx_attendance_pattern_type", "attendance_patterns", ["school_id", "pattern_type"])
    op.create_index("idx_attendance_notification_status", "attendance_notifications", ["status"])


def downgrade() -> None:
    """Drop attendance schema tables."""
    op.drop_table("attendance_configurations")
    op.drop_table("attendance_notifications")
    op.drop_table("attendance_patterns")
    op.drop_table("attendance_records")
