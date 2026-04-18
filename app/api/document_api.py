from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import re
from typing import Dict, Any

from app.db.database import get_database
from app.ai.pipelines.index_document import process_document_pipeline
from app.db.crud.knowledge_doc_crud import get_doc_by_id, get_all_docs, delete_doc
from app.core.dependencies import get_current_user_id
from app.schemas.documents import (
    DocumentUploadRequest, 
    DocumentResponse, 
    DocumentIndexResponse,
    DocumentChunkResponse
)
from app.db.models import DocChunk

router = APIRouter(prefix="/documents", tags=["documents"])

def extract_document_metadata(content: str, content_type: str = "txt") -> Dict[str, Any]:
    """Extract structured metadata from document content"""
    metadata = {
        "word_count": len(content.split()),
        "char_count": len(content),
        "line_count": len(content.split('\n')),
        "content_type": content_type,
        "language": "en"  # Default assumption
    }
    
    # Extract potential entities (simple keyword matching)
    entities = []
    common_keywords = [
        "password", "login", "account", "server", "database", 
        "billing", "payment", "subscription", "feature", "bug",
        "error", "issue", "problem", "help", "support", "ticket"
    ]
    
    for keyword in common_keywords:
        if keyword.lower() in content.lower():
            entities.append({"type": "keyword", "value": keyword})
    
    metadata["entities"] = entities
    
    # Extract potential categories based on content
    if any(word in content.lower() for word in ["billing", "payment", "invoice"]):
        metadata["category"] = "billing"
    elif any(word in content.lower() for word in ["password", "login", "account"]):
        metadata["category"] = "authentication"
    elif any(word in content.lower() for word in ["server", "database", "system"]):
        metadata["category"] = "technical"
    else:
        metadata["category"] = "general"
    
    return metadata

@router.post("/upload", response_model=DocumentIndexResponse)
def upload_document(
    payload: DocumentUploadRequest,
    db: Session = Depends(get_database),
    user_id: int = Depends(get_current_user_id)
):
    """
    Upload and process a document for the knowledge base
    """
    try:
        result = process_document_pipeline(
            db=db,
            title=payload.title,
            source=payload.source,
            content=payload.content,
            content_type=payload.content_type,
            uploaded_by=user_id
        )
        
        # Extract metadata from content
        metadata = extract_document_metadata(payload.content, payload.content_type)
        
        return DocumentIndexResponse(
            document=get_doc_by_id(db, result["document_id"]),
            chunks_created=result["chunks_created"],
            message=f"Document '{payload.title}' processed successfully",
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.post("/upload-file")
def upload_document_file(
    file: UploadFile = File(...),
    title: str = None,
    source: str = None,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_database)
):
    """
    Upload a document file and process it
    """
    try:
        # Read file content
        content = file.file.read().decode('utf-8')
        
        # Use filename as title if not provided
        if not title:
            title = file.filename.split('.')[0]
        
        # Use filename as source if not provided
        if not source:
            source = f"file_upload/{file.filename}"
        
        # Determine content type from file extension
        content_type = "txt"
        if file.filename.endswith('.pdf'):
            content_type = "pdf"
        elif file.filename.endswith('.docx'):
            content_type = "docx"
        elif file.filename.endswith('.md'):
            content_type = "markdown"
        
        # Process the document
        result = process_document_pipeline(
            db=db,
            title=title,
            source=source,
            content=content,
            content_type=content_type,
            uploaded_by=user_id
        )
        
        # Extract metadata
        metadata = extract_document_metadata(content, content_type)
        
        return DocumentIndexResponse(
            document=get_doc_by_id(db, result["document_id"]),
            chunks_created=result["chunks_created"],
            message=f"File '{file.filename}' processed successfully",
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_database),
    user_id: int = Depends(get_current_user_id)
):
    """
    List all documents in the knowledge base
    """
    return get_all_docs(db)

@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(
    doc_id: int,
    db: Session = Depends(get_database),
    user_id: int = Depends(get_current_user_id)
):
    """
    Get a specific document by ID
    """
    doc = get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return doc

@router.get("/{doc_id}/chunks", response_model=list[DocumentChunkResponse])
def get_document_chunks(
    doc_id: int,
    db: Session = Depends(get_database),
    user_id: int = Depends(get_current_user_id)
):
    """
    Get all chunks for a specific document
    """
    doc = get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    chunks = db.query(DocChunk).filter(DocChunk.doc_id == doc_id).order_by(DocChunk.chunk_index).all()
    return chunks

@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_database),
    user_id: int = Depends(get_current_user_id)
):
    """
    Delete a document and all its chunks
    """
    doc = get_doc_by_id(db, doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    delete_doc(db, doc_id)
    return {"message": f"Document '{doc.title}' deleted successfully"}
