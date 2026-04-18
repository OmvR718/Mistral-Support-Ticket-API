from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    username: str
    password_hash: str
