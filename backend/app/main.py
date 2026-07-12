from fastapi import FastAPI
from app.core.config import settings
print(settings.DATABASE_URL)

app= FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running successfully"}