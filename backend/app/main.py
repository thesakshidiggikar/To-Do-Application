from fastapi import FastAPI

from app.api.v1.router import router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="Todo API",
    version="1.0.0",
)
register_exception_handlers(app)

# Base.metadata.create_all(bind=engine)
app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def home():
    return {
        "message": "Backend is running successfully"
    }