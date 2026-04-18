from app.db.models import DocChunk
from sqlalchemy.orm import Session

def retrieve_similar_chunks(
    db:Session,
    query_embedding:list[float],
    top_k:int = 5,
    
)->list["DocChunk"]:
    chunks=(
        db.query(DocChunk)
        .order_by(
            DocChunk.embedding.cosine_distance(query_embedding)
        ).limit(top_k)
        .all()
    )
    return chunks
