"""add school_id to lms models

Revision ID: 9cf313d669ed
Revises: 41745a2b1bf7
Create Date: 2026-04-19 12:57:18.605728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql


# revision identifiers, used by Alembic.
revision: str = '9cf313d669ed'
down_revision: Union[str, None] = '41745a2b1bf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add school_id to assignments
    op.add_column('assignments', sa.Column('school_id', sqlalchemy.dialects.postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_assignments_school_id'), 'assignments', ['school_id'], unique=False)
    
    # Add school_id to submissions
    op.add_column('submissions', sa.Column('school_id', sqlalchemy.dialects.postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_submissions_school_id'), 'submissions', ['school_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_submissions_school_id'), table_name='submissions')
    op.drop_column('submissions', 'school_id')
    
    op.drop_index(op.f('ix_assignments_school_id'), table_name='assignments')
    op.drop_column('assignments', 'school_id')
