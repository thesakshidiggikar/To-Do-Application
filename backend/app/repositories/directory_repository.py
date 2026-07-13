from sqlalchemy.orm import Session

from app.models.directory import Directory
from app.schemas.directory import DirectoryCreate


def create_directory(
    db: Session,
    directory: DirectoryCreate,
    user_id: int,
) -> Directory:
    db_directory = Directory(
        name=directory.name,
        user_id=user_id,
    )

    db.add(db_directory)
    db.commit()
    db.refresh(db_directory)

    return db_directory


def get_all_directories(
    db: Session,
    user_id: int,
) -> list[Directory]:
    return (
        db.query(Directory)
        .filter(Directory.user_id == user_id)
        .all()
    )


def get_directory_by_id(
    db: Session,
    directory_id: int,
    user_id: int,
) -> Directory | None:
    return (
        db.query(Directory)
        .filter(
            Directory.id == directory_id,
            Directory.user_id == user_id,
        )
        .first()
    )


def update_directory(
    db: Session,
    db_directory: Directory,
    name: str,
) -> Directory:
    db_directory.name = name

    db.commit()
    db.refresh(db_directory)

    return db_directory


def delete_directory(
    db: Session,
    db_directory: Directory,
) -> None:
    db.delete(db_directory)
    db.commit()