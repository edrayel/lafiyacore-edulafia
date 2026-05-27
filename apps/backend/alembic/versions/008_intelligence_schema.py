"""Add intelligence schema: kpi_definitions, school_kpi_snapshots, lga_aggregates, state_aggregates, research_data_requests, report_templates, generated_reports.

Revision ID: 008_intelligence_schema
Revises: 007_parent_schema
Create Date: 2026-03-30 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "008_intelligence_schema"
down_revision: str | None = "007_parent_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create intelligence tables."""

    # KPI definitions table
    op.create_table(
        "kpi_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("unit", sa.String(20), nullable=False),
        sa.Column("source_module", sa.String(50), nullable=False),
        sa.Column("critical_threshold", sa.Numeric(10, 2), nullable=True),
        sa.Column("warning_threshold", sa.Numeric(10, 2), nullable=True),
        sa.Column("target_threshold", sa.Numeric(10, 2), nullable=True),
        sa.Column("higher_is_better", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # School KPI snapshots table
    op.create_table(
        "school_kpi_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("kpi_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("kpi_definitions.id"), nullable=False),
        sa.Column("snapshot_date", sa.Date, nullable=False, index=True),
        sa.Column("value", sa.Numeric(15, 2), nullable=False),
        sa.Column("previous_value", sa.Numeric(15, 2), nullable=True),
        sa.Column("trend", sa.String(10), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("calculation_metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("school_id", "kpi_id", "snapshot_date", name="uq_school_kpi_snapshot"),
    )

    # LGA aggregates table
    op.create_table(
        "lga_aggregates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lga", sa.String(100), nullable=False, index=True),
        sa.Column("state", sa.String(100), nullable=False, index=True),
        sa.Column("aggregate_date", sa.Date, nullable=False, index=True),
        sa.Column("aggregate_level", sa.String(20), nullable=False, server_default="daily"),
        sa.Column("total_schools", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_students", sa.Integer, nullable=False, server_default="0"),
        sa.Column("avg_attendance_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("total_sick_bay_visits", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_collections", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("open_alerts_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("lga", "state", "aggregate_date", name="uq_lga_aggregate"),
    )

    # State aggregates table
    op.create_table(
        "state_aggregates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("state", sa.String(100), nullable=False, index=True),
        sa.Column("aggregate_date", sa.Date, nullable=False, index=True),
        sa.Column("aggregate_level", sa.String(20), nullable=False, server_default="daily"),
        sa.Column("total_lgas", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_schools", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_students", sa.Integer, nullable=False, server_default="0"),
        sa.Column("avg_attendance_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("total_sick_bay_visits", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_collections", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("open_alerts_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("state", "aggregate_date", name="uq_state_aggregate"),
    )

    # Research data requests table
    op.create_table(
        "research_data_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("researcher_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("request_title", sa.String(255), nullable=False),
        sa.Column("research_purpose", sa.Text, nullable=False),
        sa.Column("data_categories", postgresql.JSONB, nullable=False),
        sa.Column("date_range_start", sa.Date, nullable=False),
        sa.Column("date_range_end", sa.Date, nullable=False),
        sa.Column("geographic_scope", postgresql.JSONB, nullable=True),
        sa.Column("ethics_approval_reference", sa.String(100), nullable=False),
        sa.Column("ethics_approval_date", sa.Date, nullable=False),
        sa.Column("institution", sa.String(255), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("review_notes", sa.Text, nullable=True),
        sa.Column("data_file_path", sa.String(500), nullable=True),
        sa.Column("data_file_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("download_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("max_downloads", sa.Integer, nullable=False, server_default="5"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Report templates table
    op.create_table(
        "report_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id"), nullable=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("report_type", sa.String(50), nullable=False),
        sa.Column("layout", postgresql.JSONB, nullable=False),
        sa.Column("is_default", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_system", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Generated reports table
    op.create_table(
        "generated_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("report_templates.id"), nullable=True),
        sa.Column("generated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("report_type", sa.String(50), nullable=False),
        sa.Column("parameters", postgresql.JSONB, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("file_path", sa.String(500), nullable=True),
        sa.Column("file_format", sa.String(10), nullable=True),
        sa.Column("file_size_bytes", sa.Integer, nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("progress_percent", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Drop intelligence tables."""
    op.drop_table("generated_reports")
    op.drop_table("report_templates")
    op.drop_table("research_data_requests")
    op.drop_table("state_aggregates")
    op.drop_table("lga_aggregates")
    op.drop_table("school_kpi_snapshots")
    op.drop_table("kpi_definitions")
