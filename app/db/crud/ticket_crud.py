from app.db.models import Ticket,User
from sqlalchemy.orm import Session
def create_ticket(db:Session,subject:str,body:str)->Ticket:
    db_ticket=Ticket(
        subject=subject,
        body=body,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_created_tickets(db:Session,ticket_id:int)-> Ticket | None:
    return db.query(Ticket).filter(Ticket.id==ticket_id).first()

def get_user_created_tickets(db:Session,user_id:int)->list[Ticket]:
    return db.query(Ticket).filter(Ticket.created_by==user_id).all()

def get_assigned_tickets(db:Session,user_id:int)->list[Ticket]:
    return db.query(Ticket).filter(Ticket.assigned_to==user_id).all()


     