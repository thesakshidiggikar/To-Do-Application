from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.directory import DirectoryCreate, DirectoryResponse
from app.services.directory_service import create_directory_service

router = APIRouter()


@router.post(
    "/directories",
    response_model=DirectoryResponse,
    status_code=201,
)
def create_directory(
    directory: DirectoryCreate,
    db: Session = Depends(get_db),
):

    return create_directory_service(db, directory)