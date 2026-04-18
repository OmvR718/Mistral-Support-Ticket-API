from pydantic import BaseModel
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    timestamp: datetime = datetime.now()

class SuccessResponse(BaseModel):
    message: str
    data: dict | None = None
    timestamp: datetime = datetime.now()
