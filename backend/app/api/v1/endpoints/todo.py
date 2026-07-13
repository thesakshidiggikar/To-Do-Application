from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.todo import (
    TodoCreate,
    TodoResponse,
)
from app.services.todo_service import (
    create_todo_service,
    get_all_todos_service,
    get_todo_by_id_service,
    update_todo_service,
    delete_todo_service,
)

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
):
    return create_todo_service(db, todo)


@router.get(
    "",
    response_model=list[TodoResponse],
)
def get_all_todos(
    db: Session = Depends(get_db),
):
    return get_all_todos_service(db)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    todo = get_todo_by_id_service(db, todo_id)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return todo


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
)
def update_todo(
    todo_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db),
):
    db_todo = get_todo_by_id_service(db, todo_id)

    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return update_todo_service(
        db,
        db_todo,
        todo,
    )


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    db_todo = get_todo_by_id_service(db, todo_id)

    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    delete_todo_service(
        db,
        db_todo,
    )

    return None