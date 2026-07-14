from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
# OLD
# RefreshTokenRequest missing

# NEW
from app.schemas.user import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterResponse,
    ResetPasswordRequest,
    UserLogin,
    UserRegister,
    UserResponse,
    VerifyEmailRequest,
)
# OLD
# refresh_access_token_service missing

# NEW
from app.services.user_service import (
    change_password_service,
    forgot_password_service,
    login_user_service,
    logout_user_service,
    refresh_access_token_service,
    register_user_service,
    reset_password_service,
    verify_email_service,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
)

def register_user(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return register_user_service(
        db=db,
        user=user,
    )

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return forgot_password_service(
        db=db,
        request=request,
    )
@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return reset_password_service(
        db=db,
        request=request,
    )

@router.post("/verify-email")
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    return verify_email_service(
        db=db,
        token=request.token,
    )

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    return login_user_service(
        db=db,
        user=user,
    )
@router.post("/refresh")
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token_service(
        db=db,
        request=request,
    )
@router.post("/logout")
def logout_user(
    request: LogoutRequest,
    db: Session = Depends(get_db),
):
    return logout_user_service(
        db=db,
        request=request,
    )

@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return change_password_service(
        db=db,
        current_user=current_user,
        request=request,
    )
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_details(
    current_user: User = Depends(get_current_user),
):
    return current_user