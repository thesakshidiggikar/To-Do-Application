from fastapi import FastAPI

from app.database.database import engine
from app.database.base import Base


app= FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Backend is running successfully"
        }