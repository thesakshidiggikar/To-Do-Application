from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.user_service import (
    login_user_service,
    register_user_service,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/login",
)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user_service(
        db,
        user,
    )