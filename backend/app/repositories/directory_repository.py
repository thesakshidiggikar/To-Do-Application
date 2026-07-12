from sqlalchemy.orm import Session

from app.models.directory import Directory
from app.schemas.directory import DirectoryCreate


def create_directory(
    db: Session,
    directory: DirectoryCreate,
) -> Directory:
    db_directory = Directory(
        name=directory.name,
    )

    db.add(db_directory)
    db.commit()
    db.refresh(db_directory)

    return db_directory


def get_all_directories(
    db: Session,
) -> list[Directory]:
    return db.query(Directory).all()


def get_directory_by_id(
    db: Session,
    directory_id: int,
) -> Directory | None:
    return (
        db.query(Directory)
        .filter(Directory.id == directory_id)
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