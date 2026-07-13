# OLD
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# NEW
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.directory import Directory
    from app.models.todo import Todo


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    # OLD
    directories: Mapped[List["Directory"]] = relationship(
        back_populates="user",
    )

    # NEW
    # A user can own multiple directories.
    directories: Mapped[List["Directory"]] = relationship(
        back_populates="user",
    )
    # NEW
    # One user can own multiple todos.
    # OLD
    todos = relationship(
        "Todo",
        back_populates="user",
        cascade="all, delete",
    )

    # NEW
    # One user can own multiple todos.
    todos: Mapped[List["Todo"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )