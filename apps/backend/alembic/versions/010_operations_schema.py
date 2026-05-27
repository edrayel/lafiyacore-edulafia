"""Migration 010: admissions, emergency, special_needs, custody tables.

Revision ID: 010_operations_schema
Revises: 009_admin_schema
Create Date: 2026-04-05
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "010_operations_schema"
down_revision: str | None = "009_admin_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Applications
    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("date_of_birth", sa.Date, nullable=False),
        sa.Column("gender", sa.String(10), nullable=False),
        sa.Column("nationality", sa.String(100), nullable=True),
        sa.Column("state_of_origin", sa.String(100), nullable=True),
        sa.Column("lga_of_origin", sa.String(100), nullable=True),
        sa.Column("previous_school", sa.String(255), nullable=True),
        sa.Column("class_applied_for", sa.String(50), nullable=False),
        sa.Column("admission_year", sa.Integer, nullable=False),
        sa.Column("parent_name", sa.String(200), nullable=False),
        sa.Column("parent_phone", sa.String(20), nullable=False),
        sa.Column("parent_email", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("exam_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("interview_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("interview_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )

    # Emergency modes
    op.create_table(
        "emergency_modes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active", index=True),
        sa.Column("protocols", postgresql.JSONB, nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Individual Education Plans
    op.create_table(
        "individual_education_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("disability_type", sa.String(50), nullable=False),
        sa.Column("diagnosis_date", sa.Date, nullable=True),
        sa.Column("diagnosed_by", sa.String(255), nullable=True),
        sa.Column("goals", postgresql.JSONB, nullable=True),
        sa.Column("accommodations", postgresql.JSONB, nullable=True),
        sa.Column("support_staff", postgresql.JSONB, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft", index=True),
        sa.Column("review_date", sa.Date, nullable=True),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Custody orders
    op.create_table(
        "custody_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("custodial_parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id"), nullable=False),
        sa.Column("non_custodial_parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("guardians.id"), nullable=True),
        sa.Column("court_order_number", sa.String(100), nullable=True),
        sa.Column("court_name", sa.String(255), nullable=True),
        sa.Column("order_date", sa.Date, nullable=False),
        sa.Column("restrictions", postgresql.JSONB, nullable=True),
        sa.Column("expiry_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active", index=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("custody_orders")
    op.drop_table("individual_education_plans")
    op.drop_table("emergency_modes")
    op.drop_table("applications")
