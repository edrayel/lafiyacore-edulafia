"""Migration 013: exam_registration, girl_child, discipline, inspection, accreditation tables.

Revision ID: 013_compliance_schema
Revises: 012_hr_operations_schema
Create Date: 2026-04-05
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "013_compliance_schema"
down_revision: str | None = "012_hr_operations_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Exam registrations
    op.create_table(
        "exam_registrations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("exam_type", sa.String(20), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False, index=True),
        sa.Column("candidate_number", sa.String(50), nullable=True),
        sa.Column("subjects", postgresql.JSONB, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="registered"),
        sa.Column("registration_date", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Girl-child records
    op.create_table(
        "girl_child_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True, index=True),
        sa.Column("enrollment_source", sa.String(100), nullable=True),
        sa.Column("risk_factors", postgresql.JSONB, nullable=True),
        sa.Column("interventions", postgresql.JSONB, nullable=True),
        sa.Column("attendance_trend", sa.String(50), nullable=True),
        sa.Column("dropout_risk", sa.String(20), nullable=False, server_default="low"),
        sa.Column("counselor_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )

    # Discipline records
    op.create_table(
        "discipline_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("offense_type", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("action_taken", sa.String(50), nullable=False),
        sa.Column("reported_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("parent_notified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("follow_up_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # School inspections
    op.create_table(
        "school_inspections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("inspector_name", sa.String(255), nullable=False),
        sa.Column("ministry", sa.String(255), nullable=False),
        sa.Column("inspection_date", sa.Date, nullable=False),
        sa.Column("findings", postgresql.JSONB, nullable=True),
        sa.Column("recommendations", postgresql.JSONB, nullable=True),
        sa.Column("compliance_status", sa.String(30), nullable=False),
        sa.Column("follow_up_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )

    # Accreditation checklists
    op.create_table(
        "accreditation_checklists",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("requirement", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="not_met"),
        sa.Column("evidence_path", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("inspected_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("inspected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("accreditation_checklists")
    op.drop_table("school_inspections")
    op.drop_table("discipline_records")
    op.drop_table("girl_child_records")
    op.drop_table("exam_registrations")
