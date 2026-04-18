from app.db.models import DocChunk
from sqlalchemy.orm import Session

def create_chunk(db:Session,
                doc_id:int,
                chunk_index:int,
                text:str,
                embedding:list[float],
                token_count:int)->DocChunk:
    doc_chunk=DocChunk(
        doc_id=doc_id,
        chunk_index=chunk_index,
        text=text,
        embedding=embedding,
        token_count=token_count
    )
    db.add(doc_chunk)
    db.commit()
    db.refresh(doc_chunk)
    return doc_chunk

def create_many_chunks(db:Session,chunks:list[DocChunk]):
    db.add_all(chunks)
    db.commit()

def get_chunk_by_doc(db:Session,doc_id:int)->DocChunk:
    return db.query(DocChunk).filter(DocChunk.doc_id==doc_id).first()

def delete_chunks_by_doc(db: Session, doc_id: int) -> None:
    db.query(DocChunk).filter(DocChunk.doc_id == doc_id).delete()
    db.commit()