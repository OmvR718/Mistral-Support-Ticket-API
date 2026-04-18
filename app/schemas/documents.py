from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class DocumentUploadRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Document title")
    source: str = Field(..., min_length=1, max_length=255, description="Document source or URL")
    content: str = Field(..., min_length=10, description="Document content")
    content_type: str = Field(default="txt", description="Content type (txt, md, html, etc)")

class DocumentResponse(BaseModel):
    id: int
    title: str
    source: str
    content_type: str
    uploaded_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentChunkResponse(BaseModel):
    id: int
    doc_id: int
    chunk_index: int
    text: str
    token_count: int
    
    class Config:
        from_attributes = True

class DocumentIndexResponse(BaseModel):
    document: DocumentResponse
    chunks_created: int
    message: str
    metadata: Dict[str, Any] = {}
