from sqlalchemy.orm import Session

from app.models.directory import Directory
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
) -> Directory:
    return create_directory(db, directory)


def get_all_directories_service(
    db: Session,
) -> list[Directory]:
    return get_all_directories(db)


def get_directory_by_id_service(
    db: Session,
    directory_id: int,
) -> Directory | None:
    return get_directory_by_id(db, directory_id)


def update_directory_service(
    db: Session,
    db_directory: Directory,
    name: str,
) -> Directory:
    return update_directory(
        db,
        db_directory,
        name,
    )


def delete_directory_service(
    db: Session,
    db_directory: Directory,
) -> None:
    delete_directory(
        db,
        db_directory,
    )