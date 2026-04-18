from sqlalchemy.orm import Session
from app.db.models import KnowledgeDoc

def create_doc(db:Session,title:str,source:str,content_type:str,uploaded_by:int)->KnowledgeDoc:
    knowledgedoc_obj=KnowledgeDoc(
        title=title,
        source=source,
        content_type=content_type,
        uploaded_by=uploaded_by,
    )
    db.add(knowledgedoc_obj)
    db.commit()
    db.refresh(knowledgedoc_obj)
    return knowledgedoc_obj

def get_doc_by_id(db:Session,doc_id)->KnowledgeDoc | None:
    return db.query(KnowledgeDoc).filter(KnowledgeDoc.id==doc_id).first()

def get_all_docs(db:Session)->list[KnowledgeDoc]:
    return db.query(KnowledgeDoc).all()

def delete_doc(db:Session,doc_id:int)->None:
    db.query(KnowledgeDoc).filter(KnowledgeDoc.id==doc_id).delete()
    db.commit()