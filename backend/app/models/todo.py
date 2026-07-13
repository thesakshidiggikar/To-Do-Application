from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    important: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    directory_id: Mapped[int] = mapped_column(
        ForeignKey("directories.id"),
        nullable=False,
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

    directory: Mapped["Directory"] = relationship(
        back_populates="todos",
    )