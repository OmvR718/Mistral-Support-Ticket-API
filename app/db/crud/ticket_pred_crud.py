from sqlalchemy.orm import Session
from app.db.models import TicketPrediction


def create_prediction(
    db: Session,
    ticket_id: int,
    category: str,
    priority: str,
    confidence: float,
    model_name: str = "mistral"
) -> TicketPrediction:

    prediction = TicketPrediction(
        ticket_id=ticket_id,
        category=category,
        priority=priority,
        confidence=confidence,
        model_name=model_name
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction

def get_prediction_by_ticket(
    db: Session,
    ticket_id: int
) -> TicketPrediction | None:

    return (
        db.query(TicketPrediction)
        .filter(TicketPrediction.ticket_id == ticket_id)
        .first()
    )