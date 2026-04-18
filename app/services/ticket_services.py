from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.crud.ticket_crud import (
    get_assigned_tickets,
    create_ticket,
    get_created_ticket,
    get_user_created_tickets,
)
from app.schemas.tickets import TicketCreate

def check_ticket_unique(db:Session,payload:TicketCreate,user_id:int):
    if get_created_ticket(db,payload.subject):
        raise HTTPException(status_code=400,detail="Ticket already Exists")
    ticket=create_ticket(db,payload.subject,payload.body,created_by=user_id)
    return {"id": ticket.id,"subject": ticket.subject}

def list_tickets(db:Session,user_id:int):
    return get_user_created_tickets(db,user_id) 