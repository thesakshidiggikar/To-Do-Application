"""add user relationship to todos

Revision ID: fa7accc7b71b
Revises: 1ffcbb9f491b
Create Date: 2026-07-13 15:43:41.499443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa7accc7b71b'
down_revision: Union[str, Sequence[str], None] = '1ffcbb9f491b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # NEW
    # Add the owner of each todo.
    op.add_column(
        "todos",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.create_foreign_key(
        "fk_todos_user_id",
        "todos",
        "users",
        ["user_id"],
        ["id"],
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_todos_user_id",
        "todos",
        type_="foreignkey",
    )

    op.drop_column(
        "todos",
        "user_id",
    )