from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DirectoryCreate(BaseModel):

    # OLD
    # name: str

    # NEW
    # Replaced with Annotated + Field to add production-level validation.
    # This ensures the directory name has a minimum and maximum length.
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
        ),
    ]

    # NEW
    # Strip leading/trailing spaces and reject empty names.
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Directory name cannot be empty.")

        return value


class DirectoryUpdate(BaseModel):

    # OLD
    # name: str

    # NEW
    # Apply the same validation rules during update.
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
        ),
    ]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Directory name cannot be empty.")

        return value


class DirectoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    # OLD (Pydantic v1)
    # class Config:
    #     orm_mode = True

    # NEW (Pydantic v2)
    # Replaced orm_mode=True with ConfigDict(from_attributes=True).
    model_config = ConfigDict(from_attributes=True)