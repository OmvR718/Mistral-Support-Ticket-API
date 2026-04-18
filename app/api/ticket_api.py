from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_database
from app.schemas.tickets import TicketCreate
from app.services.ticket_services import check_ticket_unique, list_tickets
from app.core.dependencies import get_current_user_id
from app.db.crud.user_crud import get_id_from_username

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_database), user_id: int = Depends(get_current_user_id)):
    return check_ticket_unique(db, payload, user_id)

@router.get("/")
def list_user_tickets(db: Session = Depends(get_database), user_id: int = Depends(get_current_user_id)):
    return list_tickets(db, user_id)

@router.get("/user/{username}")
def list_tickets_by_user(username: str, db: Session = Depends(get_database), current_user_id: int = Depends(get_current_user_id)):
    user_id = get_id_from_username(db, username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return list_tickets(db, user_id)