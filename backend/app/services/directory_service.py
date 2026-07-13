from sqlalchemy.orm import Session

from app.models.directory import Directory
from app.models.user import User
from app.repositories.directory_repository import (
    create_directory,
    delete_directory,
    get_all_directories,
    get_directory_by_id,
    update_directory,
)
from app.schemas.directory import DirectoryCreate


def create_directory_service(
    db: Session,
    directory: DirectoryCreate,
    current_user: User,
) -> Directory:
    return create_directory(
        db=db,
        directory=directory,
        user_id=current_user.id,
    )


def get_all_directories_service(
    db: Session,
    current_user: User,
) -> list[Directory]:
    return get_all_directories(
        db=db,
        user_id=current_user.id,
    )


def get_directory_by_id_service(
    db: Session,
    directory_id: int,
    current_user: User,
) -> Directory | None:
    return get_directory_by_id(
        db=db,
        directory_id=directory_id,
        user_id=current_user.id,
    )


def update_directory_service(
    db: Session,
    db_directory: Directory,
    name: str,
) -> Directory:
    return update_directory(
        db=db,
        db_directory=db_directory,
        name=name,
    )


def delete_directory_service(
    db: Session,
    db_directory: Directory,
) -> None:
    delete_directory(
        db=db,
        db_directory=db_directory,
    )