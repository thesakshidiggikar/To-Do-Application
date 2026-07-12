from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.directory import (
    DirectoryCreate,
    DirectoryUpdate,
    DirectoryResponse,
)
from app.services.directory_service import (
    create_directory_service,
    get_all_directories_service,
    get_directory_by_id_service,
    update_directory_service,
    delete_directory_service,
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
):
    return create_directory_service(db, directory)


@router.get(
    "",
    response_model=list[DirectoryResponse],
)
def get_all_directories(
    db: Session = Depends(get_db),
):
    return get_all_directories_service(db)


@router.get(
    "/{directory_id}",
    response_model=DirectoryResponse,
)
def get_directory(
    directory_id: int,
    db: Session = Depends(get_db),
):
    directory = get_directory_by_id_service(
        db,
        directory_id,
    )

    if directory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directory not found",
        )

    return directory


@router.put(
    "/{directory_id}",
    response_model=DirectoryResponse,
)
def update_directory(
    directory_id: int,
    directory: DirectoryUpdate,
    db: Session = Depends(get_db),
):
    db_directory = get_directory_by_id_service(
        db,
        directory_id,
    )

    if db_directory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directory not found",
        )

    return update_directory_service(
        db,
        db_directory,
        directory.name,
    )


@router.delete(
    "/{directory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_directory(
    directory_id: int,
    db: Session = Depends(get_db),
):
    db_directory = get_directory_by_id_service(
        db,
        directory_id,
    )

    if db_directory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directory not found",
        )

    delete_directory_service(
        db,
        db_directory,
    )

    return None