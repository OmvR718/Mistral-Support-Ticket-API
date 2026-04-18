from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.database import get_database
from app.schemas.schemas import TicketCreate
from app.services.ticket_services import check_ticket_unique,list_tickets
from app.core.security import get_current_user_id_from_token
from app.db.crud.user_crud import get_id_from_username

router=APIRouter(prefix="/ticket",tags=["ticket"])

@router.post("check")
def insert_ticket(payload:TicketCreate,db:Session=Depends(get_database),user_id:int=Depends(get_current_user_id_from_token)):
    return check_ticket_unique(db,payload,user_id)

@router.get('listickets')
def ticket_list(user_name:str,db:Session=Depends(get_database)):
    user_id = get_id_from_username(db,user_name)
    return list_tickets(db,user_id)