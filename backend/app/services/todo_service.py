from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.repositories.todo_repository import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
)
from app.schemas.todo import TodoCreate


def create_todo_service(
    db: Session,
    todo: TodoCreate,
) -> Todo:
    return create_todo(db, todo)


def get_all_todos_service(
    db: Session,
) -> list[Todo]:
    return get_all_todos(db)


def get_todo_by_id_service(
    db: Session,
    todo_id: int,
) -> Todo | None:
    return get_todo_by_id(db, todo_id)


def update_todo_service(
    db: Session,
    db_todo: Todo,
    todo: TodoCreate,
) -> Todo:
    return update_todo(
        db,
        db_todo,
        todo,
    )


def delete_todo_service(
    db: Session,
    db_todo: Todo,
) -> None:
    delete_todo(
        db,
        db_todo,
    )