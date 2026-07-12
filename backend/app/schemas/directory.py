from datetime import datetime 

from pydantic import BaseModel, ConfigDict

class DirectoryCreate(BaseModel):
    name:str

class DirectoryUpdate(BaseModel):
    name:str

class DirectoryResponse(BaseModel):
    id:int 
    name:str 
    created_at:datetime
    updated_at:datetime 

    model_config=ConfigDict(from_attributes=True)