from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings

# OLD
# create_access_token

# NEW
# OLD
# verify_refresh_token missing

# NEW
# OLD
# create_reset_token missing

# NEW
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    create_verification_token,
    hash_password,
    verify_password,
    verify_refresh_token,
    verify_reset_token,
    verify_verification_token,
)
# OLD
# create_user
# get_user_by_email
# get_user_by_id

# NEW
from app.repositories.user_repository import (
    create_user,
    delete_refresh_token,
    get_refresh_token,
    get_user_by_email,
    save_refresh_token,
    update_user_password,
    verify_user_email,
)
from datetime import datetime, timedelta, timezone

from app.schemas.user import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LogoutRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
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

    db_user = create_user(
        db,
        user,
        hashed_password,
    )

    verification_token = create_verification_token(
        {
            "sub": db_user.email,
        }
    )

    return {
        "user": db_user,
        "verification_token": verification_token,
    }


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
    # NEW
    # Block login until email is verified.
    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in.",
        )

# OLD
# access_token = create_access_token(...)

    # NEW
    payload = {
        "sub": db_user.email,
    }

    access_token = create_access_token(
        payload,
    )

    refresh_token = create_refresh_token(
        payload,
    )

    # NEW
    # Calculate refresh token expiry before saving it.
    expires_at = datetime.now(
        timezone.utc,
    ) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    # NEW
    # Save refresh token in database.
    save_refresh_token(
        db=db,
        token=refresh_token,
        user_id=db_user.id,
        expires_at=expires_at,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

def refresh_access_token_service(
    db: Session,
    request: RefreshTokenRequest,
):
    # NEW
    # Check whether the refresh token still exists in the database.
    db_refresh_token = get_refresh_token(
        db=db,
        token=request.refresh_token,
    )

    if db_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found.",
        )

    # NEW
    # Verify JWT signature and expiry.
    payload = verify_refresh_token(
        request.refresh_token,
    )

    email = payload.get("sub")

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        )

    access_token = create_access_token(
        {
            "sub": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

def logout_user_service(
    db: Session,
    request: LogoutRequest,
):
    db_refresh_token = get_refresh_token(
        db=db,
        token=request.refresh_token,
    )

    if db_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found.",
        )

    delete_refresh_token(
        db=db,
        db_token=db_refresh_token,
    )

    return {
        "message": "Logout successful.",
    }

def change_password_service(
    db: Session,
    current_user,
    request: ChangePasswordRequest,
):
    # Verify old password
    if not verify_password(
        request.old_password,
        current_user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect.",
        )

    # Hash new password
    hashed_password = hash_password(
        request.new_password,
    )

    # Update password
    return update_user_password(
        db=db,
        user=current_user,
        hashed_password=hashed_password,
    )

def forgot_password_service(
    db: Session,
    request: ForgotPasswordRequest,
):
    user = get_user_by_email(
        db=db,
        email=request.email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    reset_token = create_reset_token(
        {
            "sub": user.email,
        }
    )

    # TODO
    # Send reset token via email.
    # For now, return it for testing.
    return {
        "reset_token": reset_token,
    }
def reset_password_service(
    db: Session,
    request: ResetPasswordRequest,
):
    payload = verify_reset_token(
        request.token,
    )

    email = payload.get("sub")

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    hashed_password = hash_password(
        request.new_password,
    )

    update_user_password(
        db=db,
        user=user,
        hashed_password=hashed_password,
    )

    return {
        "message": "Password reset successful.",
    }

def verify_email_service(
    db: Session,
    token: str,
):
    payload = verify_verification_token(
        token,
    )

    email = payload.get("sub")

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    verify_user_email(
        db=db,
        user=user,
    )

    return {
        "message": "Email verified successfully.",
    }