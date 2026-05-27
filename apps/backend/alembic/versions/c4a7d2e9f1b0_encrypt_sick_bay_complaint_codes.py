"""Encrypt sick bay complaint codes.

Revision ID: c4a7d2e9f1b0
Revises: b9f2a7c1d0e3
Create Date: 2026-04-30 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from edulafia.core.encryption import EncryptedJSON

revision: str = "c4a7d2e9f1b0"
down_revision: str | None = "b9f2a7c1d0e3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()

    op.add_column(
        "sick_bay_visits",
        sa.Column("presenting_complaint_codes_encrypted", sa.Text(), nullable=True),
    )

    encryptor = EncryptedJSON()
    rows = bind.execute(
        sa.text("SELECT id, presenting_complaint_codes FROM sick_bay_visits")
    ).fetchall()

    for row in rows:
        encrypted = encryptor.process_bind_param(row.presenting_complaint_codes, bind.dialect)
        bind.execute(
            sa.text(
                "UPDATE sick_bay_visits SET presenting_complaint_codes_encrypted = :val WHERE id = :id"
            ),
            {"val": encrypted, "id": row.id},
        )

    op.drop_column("sick_bay_visits", "presenting_complaint_codes")
    op.alter_column(
        "sick_bay_visits",
        "presenting_complaint_codes_encrypted",
        new_column_name="presenting_complaint_codes",
        existing_type=sa.Text(),
        nullable=False,
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.add_column(
        "sick_bay_visits",
        sa.Column(
            "presenting_complaint_codes_array",
            postgresql.ARRAY(sa.String()),
            nullable=True,
        ),
    )

    encryptor = EncryptedJSON()
    rows = bind.execute(
        sa.text("SELECT id, presenting_complaint_codes FROM sick_bay_visits")
    ).fetchall()

    for row in rows:
        decrypted = encryptor.process_result_value(row.presenting_complaint_codes, bind.dialect)
        bind.execute(
            sa.text(
                "UPDATE sick_bay_visits SET presenting_complaint_codes_array = :val WHERE id = :id"
            ),
            {"val": decrypted, "id": row.id},
        )

    op.drop_column("sick_bay_visits", "presenting_complaint_codes")
    op.alter_column(
        "sick_bay_visits",
        "presenting_complaint_codes_array",
        new_column_name="presenting_complaint_codes",
        existing_type=postgresql.ARRAY(sa.String()),
        nullable=False,
    )
