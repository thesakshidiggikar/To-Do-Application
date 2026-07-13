from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.exceptions.custom_exceptions import (
    TodoNotFoundException,
)
from app.database.database import get_db

# NEW
# Get the currently authenticated user.
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.todo import (
    TodoCreate,

    # OLD
    # TodoResponse,

    # NEW
    # Separate schema for update requests.
    TodoUpdate,
    TodoResponse,
)
from app.services.todo_service import (
    create_todo_service,
    get_all_todos_service,
    get_todo_by_id_service,
    update_todo_service,
    delete_todo_service,
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
# OLD
# def create_todo(
#     todo: TodoCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     return create_todo_service(
#         db,
#         todo,
#     )

# NEW
# Pass the logged-in user to the service layer.
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo_service(
        db,
        todo,
        current_user,
    )


@router.get(
    "",
    response_model=list[TodoResponse],
)
# OLD
# def get_all_todos(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     todos = get_all_todos_service(db)

# NEW
# Return only the logged-in user's todos.
def get_all_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todos = get_all_todos_service(
        db,
        current_user,
    )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
)
def get_todo(
    todo_id: int,
    # db: Session = Depends(get_db),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = get_todo_by_id_service(db, todo_id)

    # if todo is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Todo not found",
    #     )
    if todo is None:
        raise TodoNotFoundException()
    return todo


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = get_todo_by_id_service(db, todo_id)

    # if db_todo is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Todo not found",
    #     )
    if todo is None:
        raise TodoNotFoundException()

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
    current_user: User = Depends(get_current_user),
):
    db_todo = get_todo_by_id_service(db, todo_id)

    # if db_todo is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Todo not found",
    #     )
    if todo is None:
        raise TodoNotFoundException()

    delete_todo_service(
        db,
        db_todo,
    )

    return None