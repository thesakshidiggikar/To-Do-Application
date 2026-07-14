"""add email verification field

Revision ID: 99a579bacd16
Revises: a2b7247f4141
Create Date: 2026-07-14 12:02:14.260709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '99a579bacd16'
down_revision: Union[str, Sequence[str], None] = 'a2b7247f4141'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "is_verified",
    )
