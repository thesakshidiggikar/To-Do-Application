from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserRegister,
    UserResponse,
)
from app.services.user_service import (
    register_user_service,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return register_user_service(
        db,
        user,
    )