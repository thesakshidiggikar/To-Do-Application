"""add refresh tokens table

Revision ID: a2b7247f4141
Revises: c853f595255e
Create Date: 2026-07-14 01:10:26.636280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2b7247f4141'
down_revision: Union[str, Sequence[str], None] = 'c853f595255e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )

    op.create_index(
        op.f("ix_refresh_tokens_id"),
        "refresh_tokens",
        ["id"],
        unique=False,
    )

def downgrade() -> None:
    op.drop_index(
        op.f("ix_refresh_tokens_id"),
        table_name="refresh_tokens",
    )

    op.drop_table("refresh_tokens")
