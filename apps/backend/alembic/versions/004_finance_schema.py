"""Add finance schema: fee_schedules, fee_ledger, scholarships, payment_configurations.

Revision ID: 004_finance_schema
Revises: 003_attendance_schema
Create Date: 2026-03-27 03:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "004_finance_schema"
down_revision: str | None = "003_attendance_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create finance tables."""

    # Fee schedules table
    op.create_table(
        "fee_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("academic_years.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )

    # Fee schedule items table
    op.create_table(
        "fee_schedule_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("fee_schedule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fee_schedules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("class_level", sa.String(20), nullable=False),
        sa.Column("fee_category", sa.String(100), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_mandatory", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("fee_schedule_id", "class_level", "fee_category", name="uq_fee_schedule_item_category"),
    )

    # Fee ledger table
    op.create_table(
        "fee_ledger",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("term_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("terms.id"), nullable=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("academic_years.id"), nullable=True),
        sa.Column("transaction_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("transaction_type", sa.String(20), nullable=False, comment="charge, payment, waiver, refund, adjustment"),
        sa.Column("fee_category", sa.String(100), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_method", sa.String(50), nullable=True),
        sa.Column("payment_reference", sa.String(255), nullable=True, index=True),
        sa.Column("receipt_number", sa.String(100), nullable=True, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("gateway_reference", sa.String(255), nullable=True, index=True),
        sa.Column("gateway_response", postgresql.JSONB, nullable=True),
        sa.Column("recorded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Scholarships table
    op.create_table(
        "scholarships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("percentage", sa.Numeric(5, 2), nullable=True),
        sa.Column("criteria", postgresql.JSONB, nullable=True),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("donor_name", sa.String(255), nullable=True),
        sa.Column("donor_contact", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Student scholarships table
    op.create_table(
        "student_scholarships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("scholarship_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("academic_year_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("academic_years.id"), nullable=False),
        sa.Column("amount_awarded", sa.Numeric(12, 2), nullable=False),
        sa.Column("awarded_date", sa.Date, nullable=False),
        sa.Column("awarded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("student_id", "scholarship_id", "academic_year_id", name="uq_student_scholarship_year"),
    )

    # Payment configurations table
    op.create_table(
        "payment_configurations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("payment_gateway", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("public_key", sa.String(255), nullable=True),
        sa.Column("secret_key", sa.String(255), nullable=True),
        sa.Column("merchant_id", sa.String(255), nullable=True),
        sa.Column("webhook_secret", sa.String(255), nullable=True),
        sa.Column("config", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("school_id", "payment_gateway", name="uq_payment_config_school_gateway"),
    )

    # Create indexes
    op.create_index("idx_fee_ledger_student_date", "fee_ledger", ["student_id", "transaction_date"])
    op.create_index("idx_fee_ledger_school_date", "fee_ledger", ["school_id", "transaction_date"])
    op.create_index("idx_fee_ledger_type_date", "fee_ledger", ["transaction_type", "transaction_date"])


def downgrade() -> None:
    """Drop finance tables."""
    op.drop_table("payment_configurations")
    op.drop_table("student_scholarships")
    op.drop_table("scholarships")
    op.drop_table("fee_ledger")
    op.drop_table("fee_schedule_items")
    op.drop_table("fee_schedules")
