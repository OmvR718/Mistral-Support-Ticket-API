import re
from typing import List
from sqlalchemy.orm import Session

from app.ai.embeddings.nomic_embedder import embed_query
from app.db.models import KnowledgeDoc, DocChunk
from app.db.crud.knowledge_doc_crud import create_doc
from app.db.crud.doc_crud import create_many_chunks

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks for better context retention
    """
    # Clean text first
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        if len(chunk_words) >= 10:  # Minimum chunk size
            chunks.append(" ".join(chunk_words))
    
    return chunks

def count_tokens(text: str) -> int:
    """
    Simple token count (rough approximation)
    """
    return len(text.split())

def process_document_pipeline(db: Session, title: str, source: str, content: str, 
                            content_type: str = "txt", uploaded_by: int = 1) -> dict:
    """
    Complete pipeline to process a document:
    1. Create document record
    2. Split into chunks
    3. Generate embeddings for each chunk
    4. Store chunks with embeddings
    """
    
    # 1. Create document
    doc = create_doc(
        db=db,
        title=title,
        source=source,
        content_type=content_type,
        uploaded_by=uploaded_by
    )
    
    # 2. Split into chunks
    chunk_texts = chunk_text(content, chunk_size=300, overlap=50)
    
    # 3. Generate embeddings and create chunk objects
    chunks = []
    for i, chunk_text in enumerate(chunk_texts):
        # Generate embedding
        embedding = embed_query(chunk_text)
        
        # Count tokens
        token_count = count_tokens(chunk_text)
        
        # Create chunk object
        chunk = DocChunk(
            doc_id=doc.id,
            chunk_index=i,
            text=chunk_text,
            embedding=embedding,
            token_count=token_count
        )
        chunks.append(chunk)
    
    # 4. Store all chunks
    create_many_chunks(db, chunks)
    
    return {
        "document_id": doc.id,
        "title": doc.title,
        "chunks_created": len(chunks),
        "total_tokens": sum(c.token_count for c in chunks)
    }

