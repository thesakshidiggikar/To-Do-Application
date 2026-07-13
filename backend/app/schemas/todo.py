from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoCreate(BaseModel):

    # OLD
    # title: str

    # NEW
    # Added validation for title length.
    title: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
        ),
    ]

    # OLD
    # description: str

    # NEW
    # Description is optional with a maximum length.
    description: Annotated[
        str | None,
        Field(
            max_length=500,
        ),
    ] = None

    due_date: date

    completed: bool = False

    important: bool = False

    directory_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty.")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return value

        value = value.strip()

        if value == "":
            return None

        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Due date cannot be in the past.")

        return value


class TodoUpdate(BaseModel):

    # OLD
    # title: str

    # NEW
    title: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
        ),
    ]

    # OLD
    # description: str

    # NEW
    description: Annotated[
        str | None,
        Field(
            max_length=500,
        ),
    ] = None

    due_date: date

    completed: bool

    important: bool

    directory_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty.")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return value

        value = value.strip()

        if value == "":
            return None

        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Due date cannot be in the past.")

        return value


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    due_date: date
    completed: bool
    important: bool
    directory_id: int

    # NEW
    # Return the owner of the todo.
    user_id: int

    created_at: datetime
    updated_at: datetime

    # OLD (Pydantic v1)
    # class Config:
    #     orm_mode = True

    # NEW (Pydantic v2)
    model_config = ConfigDict(from_attributes=True)