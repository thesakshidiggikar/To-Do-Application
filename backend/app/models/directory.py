from datetime import datetime
from sqlalchemy import DateTime , String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List,TYPE_CHECKING
from app.database.database import Base

# OLD
# from app.models.todo import Base

# NEW
# Import models only for type hints to avoid circular imports.
if TYPE_CHECKING:
    from app.models.todo import Todo
    from app.models.user import User
    
class Directory(Base):
    __tablename__="directories"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(100),
                                   nullable=False)
    
        # NEW
    # Every directory belongs to one user.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow
    
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.now,
    )
    # NEW
    # Relationship to the owner of this directory.
    user: Mapped["User"] = relationship(
        back_populates="directories",
    )

    todos:Mapped[List["Todo"]]=relationship(
        back_populates="directory",
        cascade="all, delete-orphan",
    )
