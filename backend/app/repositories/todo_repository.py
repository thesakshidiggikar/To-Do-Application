from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate


def create_todo(
    db: Session,
    todo: TodoCreate,
) -> Todo:
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        directory_id=todo.directory_id,
        important=todo.important,
        completed=todo.completed,
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def get_all_todos(
    db: Session,
) -> list[Todo]:
    return db.query(Todo).all()


def get_todo_by_id(
    db: Session,
    todo_id: int,
) -> Todo | None:
    return (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .first()
    )


def update_todo(
    db: Session,
    db_todo: Todo,
    todo: TodoCreate,
) -> Todo:

    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.due_date = todo.due_date
    db_todo.directory_id = todo.directory_id
    db_todo.important = todo.important
    db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo(
    db: Session,
    db_todo: Todo,
) -> None:

    db.delete(db_todo)
    db.commit()