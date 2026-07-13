from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.exceptions.custom_exceptions import DirectoryNotFoundException
from app.models.user import User
from app.schemas.directory import (
    DirectoryCreate,
    DirectoryResponse,
    DirectoryUpdate,
)
from app.services.directory_service import (
    create_directory_service,
    delete_directory_service,
    get_all_directories_service,
    get_directory_by_id_service,
    update_directory_service,
)

router = APIRouter(
    prefix="/directories",
    tags=["Directories"],
)


@router.post(
    "",
    response_model=DirectoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_directory(
    directory: DirectoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_directory_service(
        db=db,
        directory=directory,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[DirectoryResponse],
)
def get_all_directories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_directories_service(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{directory_id}",
    response_model=DirectoryResponse,
)
def get_directory(
    directory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    directory = get_directory_by_id_service(
        db=db,
        directory_id=directory_id,
        current_user=current_user,
    )

    if directory is None:
        raise DirectoryNotFoundException()

    return directory


@router.put(
    "/{directory_id}",
    response_model=DirectoryResponse,
)
def update_directory(
    directory_id: int,
    directory: DirectoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_directory = get_directory_by_id_service(
        db=db,
        directory_id=directory_id,
        current_user=current_user,
    )

    if db_directory is None:
        raise DirectoryNotFoundException()

    return update_directory_service(
        db=db,
        db_directory=db_directory,
        name=directory.name,
    )


@router.delete(
    "/{directory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_directory(
    directory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_directory = get_directory_by_id_service(
        db=db,
        directory_id=directory_id,
        current_user=current_user,
    )

    if db_directory is None:
        raise DirectoryNotFoundException()

    delete_directory_service(
        db=db,
        db_directory=db_directory,
    )

    return None