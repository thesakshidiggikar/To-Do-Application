from fastapi import APIRouter

from app.api.v1.endpoints.directory import router as directory_router
from app.api.v1.endpoints.todo import router as todo_router

router = APIRouter()

router.include_router(directory_router)
router.include_router(todo_router)