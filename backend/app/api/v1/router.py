from fastapi import APIRouter

from app.api.v1.endpoints.directory import router as directory_router

router = APIRouter()

router.include_router(directory_router)