from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.models.user import User
from app.repositories.todo_repository import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
)
from app.schemas.todo import TodoCreate


# OLD
# def create_todo_service(
#     db: Session,
#     todo: TodoCreate,
# ):
#     return create_todo(
#         db,
#         todo,
#     )

# NEW
# Pass the logged-in user so the todo is linked to its owner.
def create_todo_service(
    db: Session,
    todo: TodoCreate,
    current_user: User,
):
    return create_todo(
        db,
        todo,
        current_user,
    )


# OLD
# def get_all_todos_service(
#     db: Session,
# ):
#     return get_all_todos(db)

# NEW
# Return only todos that belong to the logged-in user.
def get_all_todos_service(
    db: Session,
    current_user: User,
):
    return get_all_todos(
        db,
        current_user,
    )


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