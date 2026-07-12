from datetime import datetime
from sqlalchemy import DateTime , String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List,TYPE_CHECKING
from app.database.database import Base

if TYPE_CHECKING:
    from app.models.todo import Base
    
class Directory(Base):
    __tablename__="directories"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(100),
                                   nullable=False)
    
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow
    
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.now,
    )

    todos:Mapped[List["Todo"]]=relationship(
        back_populates="directory",
        cascade="all, delete-orphan",
    )