from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    directory_id: int
    important: bool = False
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    directory_id: int
    important: bool = False
    completed: bool = False


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    due_date: date | None
    directory_id: int
    important: bool
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)