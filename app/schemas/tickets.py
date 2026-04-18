from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=255, description="Ticket subject")
    body: str = Field(..., min_length=10, max_length=10000, description="Ticket body content")

class TicketResponse(BaseModel):
    id: int
    subject: str
    body: str
    status: str
    created_by: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TicketPredictionResponse(BaseModel):
    id: int
    ticket_id: int
    category: str
    priority: str
    confidence: float
    model_name: str = Field(..., description="Name of the AI model used for prediction")
    created_at: datetime
    
    class Config:
        from_attributes = True
        protected_namespaces = ()

class ClassificationResponse(BaseModel):
    ticket_id: int
    prediction: TicketPredictionResponse
    citations: list[dict]
