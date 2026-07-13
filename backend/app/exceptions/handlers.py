from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    DirectoryNotFoundException,
    TodoNotFoundException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(DirectoryNotFoundException)
    async def directory_not_found_handler(
        request: Request,
        exc: DirectoryNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(TodoNotFoundException)
    async def todo_not_found_handler(
        request: Request,
        exc: TodoNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.message,
            },
        )