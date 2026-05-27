"""Add admin schema: sync_status, sync_history, sentinel_thresholds, system_updates, training_resources, school_training_assignments, usage_analytics.

Revision ID: 009_admin_schema
Revises: 008_intelligence_schema
Create Date: 2026-03-30 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "009_admin_schema"
down_revision: str | None = "008_intelligence_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create admin tables."""

    # Device sync status table
    op.create_table(
        "sync_status",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("device_id", sa.String(255), nullable=False),
        sa.Column("device_info", postgresql.JSONB, nullable=True),
        sa.Column("last_sync_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sync_status", sa.String(20), nullable=False, server_default="unknown"),
        sa.Column("pending_operations", sa.Integer, nullable=False, server_default="0"),
        sa.Column("sync_duration_ms", sa.Integer, nullable=True),
        sa.Column("data_size_bytes", sa.Integer, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("retry_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Sync history table
    op.create_table(
        "sync_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("device_id", sa.String(255), nullable=False),
        sa.Column("sync_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sync_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("operations_sent", sa.Integer, nullable=False, server_default="0"),
        sa.Column("operations_received", sa.Integer, nullable=False, server_default="0"),
        sa.Column("conflicts_detected", sa.Integer, nullable=False, server_default="0"),
        sa.Column("conflicts_resolved", sa.Integer, nullable=False, server_default="0"),
        sa.Column("data_size_bytes", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_details", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Sentinel thresholds table (admin-configurable)
    op.create_table(
        "sentinel_thresholds",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("state", sa.String(100), nullable=True, index=True),
        sa.Column("lga", sa.String(100), nullable=True),
        sa.Column("symptom_category", sa.String(100), nullable=False),
        sa.Column("time_window_hours", sa.Integer, nullable=False, server_default="48"),
        sa.Column("cluster_threshold", sa.Integer, nullable=False, server_default="3"),
        sa.Column("school_threshold_percent", sa.Numeric(5, 2), nullable=False, server_default="10.0"),
        sa.Column("lga_threshold_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("baseline_illness_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("effective_from", sa.Date, nullable=False),
        sa.Column("effective_to", sa.Date, nullable=True),
        sa.Column("change_reason", sa.Text, nullable=True),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # System updates table
    op.create_table(
        "system_updates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("release_type", sa.String(20), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("release_notes", sa.Text, nullable=False),
        sa.Column("deployment_type", sa.String(20), nullable=False, server_default="global"),
        sa.Column("target_schools", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=True),
        sa.Column("target_states", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deployed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rolled_back_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deployed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("rollback_reason", sa.Text, nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Training resources table
    op.create_table(
        "training_resources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("target_role", sa.String(50), nullable=True),
        sa.Column("target_module", sa.String(50), nullable=True),
        sa.Column("language", sa.String(20), nullable=False, server_default="en"),
        sa.Column("content_url", sa.String(500), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=True),
        sa.Column("file_size_bytes", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("version", sa.String(20), nullable=False, server_default="1.0"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # School training assignments table
    op.create_table(
        "school_training_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("training_resources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assigned_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("due_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="assigned"),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("school_id", "resource_id", name="uq_school_training_assignment"),
    )

    # Usage analytics table
    op.create_table(
        "usage_analytics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("metric_date", sa.Date, nullable=False, index=True),
        sa.Column("metric_name", sa.String(100), nullable=False),
        sa.Column("metric_value", sa.Numeric(15, 4), nullable=False),
        sa.Column("analytics_metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("school_id", "metric_date", "metric_name", name="uq_usage_analytics"),
    )


def downgrade() -> None:
    """Drop admin tables."""
    op.drop_table("usage_analytics")
    op.drop_table("school_training_assignments")
    op.drop_table("training_resources")
    op.drop_table("system_updates")
    op.drop_table("sentinel_thresholds")
    op.drop_table("sync_history")
    op.drop_table("sync_status")
