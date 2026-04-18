from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.api.auth_api import router as auth_router
from app.db.database import get_database
from app.api.ticket_api import router as ticket_router
from app.api.ticket_pred_api import router as ticket_pred_router
app = FastAPI()


@app.get("/health")
def check_health(db: Session = Depends(get_database)):
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(ticket_pred_router)