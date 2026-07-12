from fastapi import FastAPI
from app.api.v1.router import router
from app.database.database import engine
from app.database.base import Base


app= FastAPI()
app.include_router(router, prefix="/api/v1")
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Backend is running successfully"
        }