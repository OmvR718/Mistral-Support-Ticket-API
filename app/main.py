from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.api.auth import router as auth_router
from app.db.database import get_database

app = FastAPI()


@app.get("/health")
def check_health(db: Session = Depends(get_database)):
    return {"status": "ok"}


app.include_router(auth_router)