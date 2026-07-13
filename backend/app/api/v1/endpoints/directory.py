from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.exceptions.custom_exceptions import DirectoryNotFoundException
from app.schemas.directory import (
    DirectoryCreate,

    # OLD
    # DirectoryResponse,

    # NEW
    # Use a separate schema for update requests.
    DirectoryUpdate,
    DirectoryResponse,
)
from app.services.directory_service import (
    create_directory_service,
    delete_directory_service,
    get_all_directories_service,
    get_directory_by_id_service,
    update_directory_service,
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
    # OLD (Response Wrapper)
    # directory = create_directory_service(db, directory)
    # return success_response(
    #     message="Directory created successfully",
    #     data=directory,
    # )

    # NEW (Final)
    # FastAPI already serializes the response according to response_model.
    # Returning the ORM object directly is the recommended REST approach.
    return create_directory_service(
        db,
        directory,
    )


@router.get(
    "",
    response_model=list[DirectoryResponse],
)
def get_all_directories(
    db: Session = Depends(get_db),
):
    # OLD (Response Wrapper)
    # directories = get_all_directories_service(db)
    # return success_response(
    #     message="Directories fetched successfully",
    #     data=directories,
    # )

    # NEW (Final)
    # response_model expects a list, so return the list directly.
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
        raise DirectoryNotFoundException()

    # OLD (Response Wrapper)
    # return success_response(
    #     message="Directory fetched successfully",
    #     data=directory,
    # )

    # NEW (Final)
    # Return the resource directly.
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
        raise DirectoryNotFoundException()

    # OLD (Response Wrapper)
    # updated_directory = update_directory_service(
    #     db,
    #     db_directory,
    #     directory,
    # )
    # return success_response(
    #     message="Directory updated successfully",
    #     data=updated_directory,
    # )

    # NEW (Final)
    # Return the updated resource directly.
    return update_directory_service(
        db,
        db_directory,
        directory,
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
        raise DirectoryNotFoundException()

    delete_directory_service(
        db,
        db_directory,
    )

    # OLD (Response Wrapper)
    # return success_response(
    #     message="Directory deleted successfully",
    # )

    # NEW (Final)
    # HTTP 204 means the request succeeded and no response body is returned.
    return None