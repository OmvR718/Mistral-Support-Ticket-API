from sqlalchemy import URL,create_engine,text
from sqlalchemy.orm import sessionmaker
from .models import Base

url_object=URL.create(
    "postgresql+pg8000",
    username="postgres",
    password="omarkassem",
    host="localhost",
    database="app"
)
engine = create_engine(url_object)
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS app_schema"))
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
Base.metadata.create_all(bind=engine)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_database():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()