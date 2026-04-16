from sqlalchemy.orm import Session
from app.db.models import User

def get_user_by_email(db:Session,email:str)->User | None:
    return db.query(User).filter(User.email==email).first()

def get_user_by_username(db:Session,username:str)->User | None:
    return db.query(User).filter(User.username==username).first()
    
def create_user(db:Session,username:str,password:str,email:str)->User:
    db_user = User(
        username=username,
        password=password,
        email=email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user