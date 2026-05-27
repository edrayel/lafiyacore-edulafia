"""Add health schema: student_health_profiles, sick_bay_visits, health_screenings, referrals, vaccination_records, sentinel_signals, sentinel_configurations.

Revision ID: 005_health_schema
Revises: 004_finance_schema
Create Date: 2026-03-30 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "005_health_schema"
down_revision: str | None = "004_finance_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create health tables."""

    # Student health profiles table
    op.create_table(
        "student_health_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("blood_group", sa.String(5), nullable=True),
        sa.Column("genotype", sa.String(5), nullable=True),
        sa.Column("chronic_conditions", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("allergies", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("current_medications", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("disability_status", sa.String(100), nullable=True),
        sa.Column("emergency_notes", sa.Text, nullable=True),
        sa.Column("family_health_history", postgresql.JSONB, nullable=True),
        sa.Column("vision_left", sa.Numeric(4, 2), nullable=True),
        sa.Column("vision_right", sa.Numeric(4, 2), nullable=True),
        sa.Column("hearing_left", sa.String(20), nullable=True),
        sa.Column("hearing_right", sa.String(20), nullable=True),
        sa.Column("parental_consent_given", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("consent_date", sa.Date, nullable=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.UniqueConstraint("student_id", name="uq_student_health_profile"),
    )

    # Sick bay visits table
    op.create_table(
        "sick_bay_visits",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("visit_date", sa.Date, nullable=False, index=True),
        sa.Column("visit_time", sa.Time, nullable=False),
        sa.Column("presenting_complaint_codes", postgresql.ARRAY(sa.String), nullable=False),
        sa.Column("presenting_complaint_notes", sa.Text, nullable=True),
        sa.Column("temperature", sa.Numeric(4, 1), nullable=True),
        sa.Column("blood_pressure_systolic", sa.Integer, nullable=True),
        sa.Column("blood_pressure_diastolic", sa.Integer, nullable=True),
        sa.Column("pulse_rate", sa.Integer, nullable=True),
        sa.Column("treatment_given", sa.Text, nullable=True),
        sa.Column("outcome", sa.String(50), nullable=False),
        sa.Column("referred_to", sa.String(255), nullable=True),
        sa.Column("parent_notified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("parent_notified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_sentinel_relevant", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("recorded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Health screenings table
    op.create_table(
        "health_screenings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("term_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("terms.id"), nullable=True),
        sa.Column("screening_date", sa.Date, nullable=False, index=True),
        sa.Column("screening_type", sa.String(50), nullable=False),
        sa.Column("height", sa.Numeric(5, 2), nullable=True),
        sa.Column("weight", sa.Numeric(5, 2), nullable=True),
        sa.Column("bmi", sa.Numeric(4, 1), nullable=True),
        sa.Column("muac", sa.Numeric(4, 1), nullable=True),
        sa.Column("vision_left", sa.Numeric(4, 2), nullable=True),
        sa.Column("vision_right", sa.Numeric(4, 2), nullable=True),
        sa.Column("hearing_left", sa.String(20), nullable=True),
        sa.Column("hearing_right", sa.String(20), nullable=True),
        sa.Column("blood_pressure_systolic", sa.Integer, nullable=True),
        sa.Column("blood_pressure_diastolic", sa.Integer, nullable=True),
        sa.Column("dental_notes", sa.Text, nullable=True),
        sa.Column("sickle_cell_test_result", sa.String(20), nullable=True),
        sa.Column("flags", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("follow_up_required", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("follow_up_notes", sa.Text, nullable=True),
        sa.Column("conducted_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Referrals table
    op.create_table(
        "referrals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("sick_bay_visit_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sick_bay_visits.id"), nullable=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("referral_date", sa.Date, nullable=False, index=True),
        sa.Column("destination_facility", sa.String(255), nullable=False),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("follow_up_due_date", sa.Date, nullable=False),
        sa.Column("outcome_notes", sa.Text, nullable=True),
        sa.Column("outcome_date", sa.Date, nullable=True),
        sa.Column("reminder_sent", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("reminder_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Vaccination records table
    op.create_table(
        "vaccination_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("vaccine_name", sa.String(100), nullable=False),
        sa.Column("vaccine_code", sa.String(20), nullable=True),
        sa.Column("dose_number", sa.Integer, nullable=False, server_default="1"),
        sa.Column("administration_date", sa.Date, nullable=False, index=True),
        sa.Column("lot_number", sa.String(50), nullable=True),
        sa.Column("administering_facility", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Sentinel signals table
    op.create_table(
        "sentinel_signals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("school_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False),
        sa.Column("lga", sa.String(100), nullable=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("date_generated", sa.DateTime(timezone=True), nullable=False),
        sa.Column("symptom_profile", postgresql.JSONB, nullable=False),
        sa.Column("students_affected", sa.Integer, nullable=False),
        sa.Column("threshold_type", sa.String(50), nullable=False),
        sa.Column("alert_tier", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("response_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Sentinel configurations table
    op.create_table(
        "sentinel_configurations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("lga", sa.String(100), nullable=True),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("schools.id"), nullable=True),
        sa.Column("symptom_category", sa.String(100), nullable=False),
        sa.Column("time_window_hours", sa.Integer, nullable=False, server_default="48"),
        sa.Column("cluster_threshold", sa.Integer, nullable=False, server_default="3"),
        sa.Column("school_threshold_percent", sa.Numeric(5, 2), nullable=False, server_default="10.0"),
        sa.Column("baseline_illness_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Composite indexes for performance
    op.create_index("idx_sick_bay_visits_student_date", "sick_bay_visits", ["student_id", "visit_date"])
    op.create_index("idx_sick_bay_visits_school_date", "sick_bay_visits", ["school_id", "visit_date"])
    op.create_index("idx_health_screenings_student_date", "health_screenings", ["student_id", "screening_date"])
    op.create_index("idx_health_screenings_school_date", "health_screenings", ["school_id", "screening_date"])
    op.create_index("idx_referrals_student_date", "referrals", ["student_id", "referral_date"])
    op.create_index("idx_referrals_school_date", "referrals", ["school_id", "referral_date"])
    op.create_index("idx_vaccination_records_student_date", "vaccination_records", ["student_id", "administration_date"])
    op.create_index("idx_sentinel_signals_state_date", "sentinel_signals", ["state", "date_generated"])


def downgrade() -> None:
    """Drop health tables."""
    op.drop_table("sentinel_configurations")
    op.drop_table("sentinel_signals")
    op.drop_table("vaccination_records")
    op.drop_table("referrals")
    op.drop_table("health_screenings")
    op.drop_table("sick_bay_visits")
    op.drop_table("student_health_profiles")
