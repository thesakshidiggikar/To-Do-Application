from app.database.database import Base

# Import all models here so Alembic can detect them.
from app.models.directory import Directory
from app.models.todo import Todo
from app.models.user import User