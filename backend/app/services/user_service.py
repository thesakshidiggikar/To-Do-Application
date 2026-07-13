from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.schemas.user import (
    UserLogin,
    UserRegister,
)


def register_user_service(
    db: Session,
    user: UserRegister,
):
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    hashed_password = hash_password(
        user.password,
    )

    return create_user(
        db,
        user,
        hashed_password,
    )


def login_user_service(
    db: Session,
    user: UserLogin,
):
    db_user = get_user_by_email(
        db,
        user.email,
    )

    if (
        db_user is None
        or not verify_password(
            user.password,
            db_user.password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        {
            "sub": db_user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }