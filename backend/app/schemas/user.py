from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):

    # OLD
    # name: str

    # NEW
    # Added validation for name length.
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
        ),
    ]

    email: EmailStr

    # OLD
    # password: str

    # NEW
    # Password must contain at least 8 characters.
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
        ),
    ]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty.")

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    # OLD (Pydantic v1)
    # class Config:
    #     orm_mode = True

    # NEW (Pydantic v2)
    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    old_password: str

    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
        ),
    ]

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordRequest(BaseModel):
    token: str

    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
        ),
    ]

class RegisterResponse(BaseModel):
    user: UserResponse
    verification_token: str

class VerifyEmailRequest(BaseModel):
    token: str